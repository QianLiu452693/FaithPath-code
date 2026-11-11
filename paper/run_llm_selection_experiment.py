#!/usr/bin/env python3
"""
LLM answer selection over FaithPath FULL retrieval (MultiTQ prefix).

Compares path-tail extractor vs top-k path LLM selection, with optional ELDB gates
(PathHit@80, PathHit + TFC>=0.93). Requires Ollama or cloud LLM via kg_agent.llm.

Usage (from MemoTime-main):
  python paper/run_llm_selection_experiment.py --n 200 --top-paths 5
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1] / "memotime"
PROJECT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROJECT))

from comparison_experiment import (  # noqa: E402
    VARIANT_SPECS,
    _hits,
    _path_hit,
    _select_answer,
    paired_bootstrap_ci,
)
from load_env import load_dotenv  # noqa: E402


def _path_line(p: dict, rank: int) -> str:
    parts = []
    for hop in p.get("path") or []:
        if isinstance(hop, dict):
            parts.append(
                f"{hop.get('head','?')} -[{hop.get('relation','?')}, {hop.get('time','')}]→ {hop.get('tail','?')}"
            )
    if not parts:
        h, r, t = p.get("head"), p.get("relation"), p.get("tail")
        if h or r or t:
            parts.append(f"{h} -[{r}, {p.get('time','')}]→ {t}")
    score = p.get("score")
    extra = f" score={score:.3f}" if isinstance(score, (int, float)) else ""
    return f"{rank}. " + " | ".join(parts) + extra


def _llm_pick_answer(
    llm,
    question: str,
    paths: List[dict],
    answer_type: str,
    model: str,
) -> Optional[str]:
    if not paths:
        return None
    lines = [_path_line(p, i + 1) for i, p in enumerate(paths)]
    kind = "timestamp (year/month/day as in path)" if answer_type == "time" else "entity name"
    prompt = (
        f"Question: {question}\n"
        f"Ranked evidence paths from a temporal knowledge graph:\n"
        + "\n".join(lines)
        + f"\n\nTask: choose the single best {kind} that answers the question using ONLY the paths above.\n"
        "Reply with the answer string only, no explanation."
    )
    try:
        out = llm.call(
            "You answer temporal KG questions using only given paths.",
            prompt,
            model=model,
            temperature=0.1,
        )
    except Exception as e:
        return None
    out = (out or "").strip().split("\n")[0].strip().strip('"').strip("'")
  # strip markdown
    out = re.sub(r"^```.*", "", out).strip()
    return out or None


def retrieve_full(item, encode, retriever, router, critic, spec):
    import re as re_mod
    from kg_agent.bibfs_temporal import estimate_d_pred

    question = item.get("question", "")
    qtype = item.get("qtype", "unknown")
    answer_type = item.get("answer_type", "entity")
    time_level = item.get("time_level", "unknown")
    cands = item.get("candidates") or []
    golds = item.get("answers") or []
    seeds = [c["name"] for c in cands[:3] if isinstance(c, dict) and c.get("name")]

    decision = router.route(question=question, qtype=qtype)
    years = re_mod.findall(r"\b(19\d{2}|20\d{2})\b", question)
    use_tf = bool(spec.get("temporal_first", True))
    after_time = years[0] if use_tf and decision.time_mode == "after" and years else None
    before_time = years[0] if use_tf and decision.time_mode == "before" and years else None
    d_pred = estimate_d_pred(
        num_seeds=len(seeds), qtype=decision.qtype, egor_d_pred=decision.d_pred
    )
    paths = (
        retriever.retrieve_paths(
            seeds=seeds,
            d_pred=d_pred,
            d_max=int(spec["d_max"]),
            after_time=after_time,
            before_time=before_time,
            reference_time=(years[0] if years and use_tf else None),
            indicator_text=question,
            embedding_fn=encode,
            w1=80,
            lambda_sem=0.6,
            lambda_prox=0.4,
            use_temporal_first=True,
            quiet=True,
        )
        if seeds
        else []
    )
    tfc_score = None
    tfc_faithful = None
    if spec["tfc"] and paths:
        report = critic.critique_candidates(
            paths,
            time_mode=decision.time_mode,
            select=decision.select,
            anchor_times=[after_time or before_time] if (after_time or before_time) else None,
            answer_type=answer_type if answer_type in ("entity", "time") else "entity",
        )
        tfc_score = float(report.score)
        tfc_faithful = bool(report.faithful)
        if report.best_path:
            paths = [report.best_path] + [p for p in paths if p is not report.best_path]
    tail = _select_answer(paths, seeds, cands, decision, answer_type, time_level, question)
    ph80 = _path_hit(paths, golds, 80) if paths else False
    return {
        "paths": paths,
        "tail": tail,
        "tfc_score": tfc_score,
        "tfc_faithful": tfc_faithful,
        "path_hit@80": ph80,
        "golds": golds,
        "answer_type": answer_type,
        "question": question,
    }


def main():
    load_dotenv(PROJECT / ".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--top-paths", type=int, default=5)
    ap.add_argument("--model", default=None, help="LLM model (default: env LLM_MODEL)")
    ap.add_argument("--tfc-threshold", type=float, default=0.93)
    ap.add_argument("--out", default=None, help="Output JSON (default: results/paper/llm_selection_n{n}.json)")
    args = ap.parse_args()

    import torch
    from config import apply_config, TPKGConfig
    from kg_agent.bibfs_temporal import BiBFSTemporalRetriever
    from kg_agent.experience_operator_routing import get_egor_router
    from kg_agent.temporal_faithfulness_critic import get_tfc
    from kg_agent.llm import LLM
    from sentence_transformers import SentenceTransformer

    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    assert torch.cuda.is_available(), "CUDA required for retrieval encoder"
    model = args.model or os.getenv("LLM_MODEL", "qwen2.5:3b")

    apply_config({"dataset": "MultiTQ", "max_depth": 3, "max_questions": args.n, "skip_questions": 0})
    with open(TPKGConfig.get_test_data_path(), encoding="utf-8") as f:
        questions = json.load(f)[: args.n]
    db = TPKGConfig.get_db_path()
    spec = VARIANT_SPECS["FULL"]

    enc_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")
    cache: dict = {}

    def encode(text: str):
        if text not in cache:
            cache[text] = enc_model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return cache[text]

    retriever = BiBFSTemporalRetriever(db, max_branch_factor=64)
    router = get_egor_router()
    critic = get_tfc()

    t0 = time.time()
    records = []
    for i, item in enumerate(questions):
        if (i + 1) % 20 == 0:
            print(f"retrieve {i+1}/{len(questions)}", flush=True)
        records.append(retrieve_full(item, encode, retriever, router, critic, spec))

    hits = {"path_tail": [], "llm_always": [], "llm_pathhit_gate": [], "llm_combined_gate": []}
    coverage = {"llm_pathhit_gate": [], "llm_combined_gate": []}

    for i, (item, rec) in enumerate(zip(questions, records)):
        if (i + 1) % 10 == 0:
            print(f"llm {i+1}/{len(questions)}", flush=True)
        golds = rec["golds"]
        top = rec["paths"][: args.top_paths]
        tail = rec["tail"]
        hits["path_tail"].append(_hits(tail, golds))

        llm_ans = _llm_pick_answer(LLM, rec["question"], top, rec["answer_type"], model)
        hits["llm_always"].append(_hits(llm_ans, golds))

        gate_ph = bool(rec["path_hit@80"])
        gate_comb = gate_ph and (rec["tfc_score"] or 0) >= args.tfc_threshold
        coverage["llm_pathhit_gate"].append(gate_ph)
        coverage["llm_combined_gate"].append(gate_comb)
        hits["llm_pathhit_gate"].append(_hits(llm_ans, golds) if gate_ph else False)
        hits["llm_combined_gate"].append(_hits(llm_ans, golds) if gate_comb else False)

    n = len(questions)

    def rate(arr):
        return 100.0 * sum(arr) / n if n else 0.0

    def answered_rate(arr, cov):
        ans = [a for a, c in zip(arr, cov) if c]
        return 100.0 * sum(ans) / len(ans) if ans else 0.0

    rep = {
        "n": n,
        "llm_model": model,
        "top_paths": args.top_paths,
        "tfc_threshold": args.tfc_threshold,
        "wall_sec": time.time() - t0,
        "hits@1_all_n": {
            "path_tail": rate(hits["path_tail"]),
            "llm_always_topk": rate(hits["llm_always"]),
            "llm_with_pathhit_gate": rate(hits["llm_pathhit_gate"]),
            "llm_with_combined_gate": rate(hits["llm_combined_gate"]),
        },
        "coverage": {
            "pathhit_gate": 100.0 * sum(coverage["llm_pathhit_gate"]) / n,
            "combined_gate": 100.0 * sum(coverage["llm_combined_gate"]) / n,
        },
        "hits@1_on_answered_only": {
            "llm_pathhit_gate": answered_rate(hits["llm_pathhit_gate"], coverage["llm_pathhit_gate"]),
            "llm_combined_gate": answered_rate(hits["llm_combined_gate"], coverage["llm_combined_gate"]),
        },
        "paired_delta_pp": {
            "llm_always_minus_path_tail": paired_bootstrap_ci(
                hits["llm_always"], hits["path_tail"]
            ),
        },
    }
    out = Path(args.out) if args.out else PROJECT / f"results/paper/llm_selection_n{n}.json"
    if not out.is_absolute():
        out = PROJECT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
