"""Oracle Hits@1 (gold-bearing paths only) for FULL vs A1 on MultiTQ prefix."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "memotime"
PROJECT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROJECT))

from comparison_experiment import VARIANT_SPECS, _hits, _select_answer, paired_bootstrap_ci, run_variant
from analyze_selection_gap_oracle import _path_contains_gold


def oracle_hits_for_questions(questions, spec, encode, retriever, router, critic, db_path):
    from kg_agent.bibfs_temporal import estimate_d_pred

    use_egor = spec["egor"]
    use_tfc = spec["tfc"]
    use_tf = spec.get("temporal_first", True)
    lam_prox = 0.4 if use_tf else 0.0
    hits = []
    for item in questions:
        question = item.get("question", "")
        golds = item.get("answers") or []
        qtype = item.get("qtype", "unknown")
        answer_type = item.get("answer_type", "entity")
        time_level = item.get("time_level", "unknown")
        cands = item.get("candidates") or []
        seeds = [c["name"] for c in cands[:3] if isinstance(c, dict) and c.get("name")]
        if use_egor:
            decision = router.route(question=question, qtype=qtype)
        else:
            from types import SimpleNamespace
            decision = SimpleNamespace(
                qtype=qtype or "general",
                time_mode="general",
                select="all",
                d_pred=1,
            )
        years = re.findall(r"\b(19\d{2}|20\d{2})\b", question)
        after_time = years[0] if use_tf and decision.time_mode == "after" and years else None
        before_time = years[0] if use_tf and decision.time_mode == "before" and years else None
        d_pred = estimate_d_pred(
            num_seeds=len(seeds),
            qtype=decision.qtype if use_egor else qtype,
            egor_d_pred=decision.d_pred if use_egor else None,
        )
        if not use_egor:
            d_pred = min(d_pred, spec["d_max"])
        paths = (
            retriever.retrieve_paths(
                seeds=seeds,
                d_pred=d_pred,
                d_max=int(spec["d_max"]),
                after_time=after_time,
                before_time=before_time,
                reference_time=(years[0] if years and use_tf else None),
                indicator_text=question,
                embedding_fn=encode if spec["embed"] else None,
                w1=80,
                lambda_sem=0.6,
                lambda_prox=lam_prox,
                use_temporal_first=use_tf,
                quiet=True,
            )
            if seeds
            else []
        )
        if use_tfc and paths:
            report = critic.critique_candidates(
                paths,
                time_mode=decision.time_mode,
                select=decision.select,
                anchor_times=[after_time or before_time] if (after_time or before_time) else None,
                answer_type=answer_type if answer_type in ("entity", "time") else "entity",
            )
            if report.best_path:
                paths = [report.best_path] + [p for p in paths if p is not report.best_path]
        gold_paths = [p for p in paths[:80] if _path_contains_gold(p, golds)]
        pred = _select_answer(gold_paths, seeds, cands, decision, answer_type, time_level, question)
        hits.append(_hits(pred, golds))
    return hits


def main():
    import os
    import torch
    from config import apply_config, TPKGConfig
    from sentence_transformers import SentenceTransformer
    from kg_agent.bibfs_temporal import BiBFSTemporalRetriever
    from kg_agent.experience_operator_routing import get_egor_router
    from kg_agent.temporal_faithfulness_critic import get_tfc

    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    n = 500
    apply_config({"dataset": "MultiTQ", "max_depth": 3, "max_questions": n, "skip_questions": 0})
    with open(TPKGConfig.get_test_data_path(), encoding="utf-8") as f:
        questions = json.load(f)[:n]
    db_path = TPKGConfig.get_db_path()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")
    cache = {}

    def encode(text: str):
        if text not in cache:
            cache[text] = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return cache[text]

    retriever = BiBFSTemporalRetriever(db_path, max_branch_factor=64)
    router = get_egor_router()
    critic = get_tfc()

    pipe = {}
    oracle = {}
    for vid in ("FULL", "A1"):
        spec = VARIANT_SPECS[vid]
        payload = run_variant(vid, spec, questions, db_path, encode, retriever, router, critic, quiet=True)
        pipe[vid] = [bool(r["is_correct"]) for r in payload["results"]]
        oracle[vid] = oracle_hits_for_questions(
            questions, spec, encode, retriever, router, critic, db_path
        )

    ci_pipe = paired_bootstrap_ci(pipe["FULL"], pipe["A1"])
    ci_oracle = paired_bootstrap_ci(oracle["FULL"], oracle["A1"])
    out = {
        "n": n,
        "hits@1_pipeline": {
            "FULL": 100 * sum(pipe["FULL"]) / n,
            "A1": 100 * sum(pipe["A1"]) / n,
            "FULL_minus_A1_pp": ci_pipe["delta"],
            "ci": [ci_pipe["ci_low"], ci_pipe["ci_high"]],
        },
        "hits@1_oracle_gold_paths": {
            "FULL": 100 * sum(oracle["FULL"]) / n,
            "A1": 100 * sum(oracle["A1"]) / n,
            "FULL_minus_A1_pp": ci_oracle["delta"],
            "ci": [ci_oracle["ci_low"], ci_oracle["ci_high"]],
            "includes_0": ci_oracle["includes_0"],
        },
    }
    path = PROJECT / "results/paper/oracle_module_gap_n500.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
