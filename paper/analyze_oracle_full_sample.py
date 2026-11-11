"""Oracle gold-path Hits@1 on a random sample of full-test selection-gap questions."""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "memotime"
PROJECT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROJECT))

from analyze_selection_gap_oracle import _path_contains_gold  # noqa: E402
from comparison_experiment import _hits, _select_answer  # noqa: E402


def main():
    import os
    import torch
    from config import apply_config, TPKGConfig
    from sentence_transformers import SentenceTransformer
    from kg_agent.bibfs_temporal import BiBFSTemporalRetriever, estimate_d_pred
    from kg_agent.experience_operator_routing import get_egor_router
    from kg_agent.temporal_faithfulness_critic import get_tfc

    sample_n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    seed = 0

    full_rows = json.loads(
        (PROJECT / "results/paper/comparison_20261108_002112/FULL.json").read_text(encoding="utf-8")
    )["results"]
    gap_qids = set(
        r["qid"] for r in full_rows if r.get("path_hit@80") and not r["is_correct"]
    )

    apply_config({"dataset": "MultiTQ", "max_depth": 3, "max_questions": 54584, "skip_questions": 0})
    with open(TPKGConfig.get_test_data_path(), encoding="utf-8") as f:
        all_q = json.load(f)
    by_qid = {str(q.get("quid") or q.get("id")): q for q in all_q}

    rng = random.Random(seed)
    pick = rng.sample(sorted(gap_qids), min(sample_n, len(gap_qids)))

    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")
    cache = {}

    def encode(text: str):
        if text not in cache:
            cache[text] = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return cache[text]

    db = TPKGConfig.get_db_path()
    retriever = BiBFSTemporalRetriever(db, max_branch_factor=64)
    router = get_egor_router()
    critic = get_tfc()

    pipe_ok = oracle_ok = 0
    fixable = 0
    n = 0
    for qid in pick:
        item = by_qid.get(str(qid))
        if not item:
            continue
        n += 1
        question = item.get("question", "")
        golds = item.get("answers") or []
        qtype = item.get("qtype", "unknown")
        answer_type = item.get("answer_type", "entity")
        time_level = item.get("time_level", "unknown")
        cands = item.get("candidates") or []
        seeds = [c["name"] for c in cands[:3] if isinstance(c, dict) and c.get("name")]
        decision = router.route(question=question, qtype=qtype)
        years = re.findall(r"\b(19\d{2}|20\d{2})\b", question)
        after_time = years[0] if decision.time_mode == "after" and years else None
        before_time = years[0] if decision.time_mode == "before" and years else None
        d_pred = estimate_d_pred(num_seeds=len(seeds), qtype=decision.qtype, egor_d_pred=decision.d_pred)
        paths = (
            retriever.retrieve_paths(
                seeds=seeds,
                d_pred=d_pred,
                d_max=3,
                after_time=after_time,
                before_time=before_time,
                reference_time=(years[0] if years else None),
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
        report = critic.critique_candidates(
            paths,
            time_mode=decision.time_mode,
            select=decision.select,
            anchor_times=[after_time or before_time] if (after_time or before_time) else None,
            answer_type=answer_type if answer_type in ("entity", "time") else "entity",
        )
        if report.best_path:
            paths = [report.best_path] + [p for p in paths if p is not report.best_path]
        pred = _select_answer(paths, seeds, cands, decision, answer_type, time_level, question)
        gold_paths = [p for p in paths[:80] if _path_contains_gold(p, golds)]
        pred_o = _select_answer(gold_paths, seeds, cands, decision, answer_type, time_level, question)
        if _hits(pred, golds):
            pipe_ok += 1
        if _hits(pred_o, golds):
            oracle_ok += 1
        if not _hits(pred, golds) and _hits(pred_o, golds):
            fixable += 1

    out = {
        "sample_n": n,
        "population_selection_gaps_full": len(gap_qids),
        "pipeline_hits@1_on_gap_sample": 100 * pipe_ok / n if n else 0,
        "oracle_gold_path_hits@1_on_gap_sample": 100 * oracle_ok / n if n else 0,
        "pct_ranking_fixable_in_sample": 100 * fixable / n if n else 0,
        "seed": seed,
    }
    path = PROJECT / "results/paper/oracle_full_selection_gap_sample.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
