"""
Decompose PathHit@80=1 failures: ranking/selection vs extractor-limited.
Re-runs retrieval for selection-gap questions and compares path-tail pipeline vs
gold-bearing-path oracle extraction (same rules as comparison_experiment._select_answer).

Output: results/paper/selection_gap_oracle_n500.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "memotime"
PROJECT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROJECT))

from comparison_experiment import (  # noqa: E402
    VARIANT_SPECS,
    _hits,
    _norm,
    _path_entities,
    _path_times,
    _select_answer,
    paired_bootstrap_ci,
    run_variant,
)


def _path_contains_gold(path: dict, golds: list[str]) -> bool:
    gold_n = {_norm(g) for g in golds if g}
    for e in _path_entities(path) + _path_times(path):
        en = _norm(e)
        for g in gold_n:
            if en == g or g in en or en in g:
                return True
            if len(g) == 4 and g.isdigit() and en.startswith(g):
                return True
    return False


def main():
    import os
    import torch

    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    assert torch.cuda.is_available(), "CUDA required"

    buckets_path = PROJECT / "results/paper/comparison_20261108_195018/failure_buckets_n500.json"
    with open(buckets_path, encoding="utf-8") as f:
        buckets = json.load(f)
    gap_qids = {a["qid"] for a in buckets["annotations"] if a["bucket"] == "selection_gap"}

    from config import apply_config, TPKGConfig
    from sentence_transformers import SentenceTransformer
    from kg_agent.bibfs_temporal import BiBFSTemporalRetriever
    from kg_agent.experience_operator_routing import get_egor_router
    from kg_agent.temporal_faithfulness_critic import get_tfc

    apply_config({"dataset": "MultiTQ", "max_depth": 3, "max_questions": 500, "skip_questions": 0})
    test_path = TPKGConfig.get_test_data_path()
    db_path = TPKGConfig.get_db_path()
    with open(test_path, encoding="utf-8") as f:
        all_q = json.load(f)[:500]
    questions = [q for q in all_q if str(q.get("quid") or q.get("id")) in gap_qids]

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")
    cache: dict = {}

    def encode(text: str):
        if text not in cache:
            cache[text] = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return cache[text]

    retriever = BiBFSTemporalRetriever(db_path, max_branch_factor=64)
    router = get_egor_router()
    critic = get_tfc()

    n_gap = len(questions)

    # FULL stack with paths for oracle decomposition on selection-gap subset only
    from types import SimpleNamespace
    import re
    from kg_agent.bibfs_temporal import estimate_d_pred
    from kg_agent.temporal_faithfulness_critic import get_tfc as _

    critic = get_tfc()
    oracle_hits = pipeline_hits = rank1_has_gold = gold_only_deep = 0
    details = []

    for item in questions:
        qid = str(item.get("quid") or item.get("id"))
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
        d_pred = estimate_d_pred(
            num_seeds=len(seeds), qtype=decision.qtype, egor_d_pred=decision.d_pred
        )
        paths = retriever.retrieve_paths(
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
        ) if seeds else []
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
        pipe_hit = _hits(pred, golds)
        if pipe_hit:
            pipeline_hits += 1

        gold_paths = [p for p in paths[:80] if _path_contains_gold(p, golds)]
        pred_oracle = _select_answer(gold_paths, seeds, cands, decision, answer_type, time_level, question)
        or_hit = _hits(pred_oracle, golds)
        if or_hit:
            oracle_hits += 1

        if paths and _path_contains_gold(paths[0], golds):
            rank1_has_gold += 1
        elif gold_paths:
            gold_only_deep += 1

        details.append(
            {
                "qid": qid,
                "pipeline_hit": pipe_hit,
                "oracle_gold_paths_hit": or_hit,
                "n_gold_paths": len(gold_paths),
                "rank1_has_gold": bool(paths and _path_contains_gold(paths[0], golds)),
            }
        )

    ranking_dominated = sum(
        1 for d in details if not d["pipeline_hit"] and d["oracle_gold_paths_hit"]
    )
    extractor_limited = sum(
        1 for d in details if not d["pipeline_hit"] and not d["oracle_gold_paths_hit"]
    )

    out = {
        "selection_gap_n": n_gap,
        "decomposition_on_gap_FULL_rerun": {
            "pipeline_correct_on_gap_subset": pipeline_hits,
            "oracle_gold_paths_correct": oracle_hits,
            "ranking_or_selection_fixable": ranking_dominated,
            "extractor_limited": extractor_limited,
            "rank1_has_gold": rank1_has_gold,
            "gold_only_beyond_rank1": gold_only_deep,
            "pct_ranking_fixable_of_gap": 100.0 * ranking_dominated / n_gap if n_gap else 0,
            "pct_extractor_limited_of_gap": 100.0 * extractor_limited / n_gap if n_gap else 0,
        },
        "full_multitq_failure_mix_from_saved_FULL_54584": {
            "n": 54584,
            "selection_gap": 19957,
            "evidence_miss": 21355,
            "selection_gap_pct_of_errors": 48.31,
            "note": "from comparison_20261108_002112/FULL.json",
        },
        "details_head": details[:5],
    }
    out_path = PROJECT / "results/paper/selection_gap_oracle_n500.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
