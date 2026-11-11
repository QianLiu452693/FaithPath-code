"""Compare FULL routing with gold qtype vs blind qtype on n=200 (LLM-Select proxy)."""
from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "memotime"
PROJECT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROJECT))

from comparison_experiment import VARIANT_SPECS, paired_bootstrap_ci, run_variant  # noqa: E402


def main():
    import torch
    from config import apply_config, TPKGConfig
    from sentence_transformers import SentenceTransformer
    from kg_agent.bibfs_temporal import BiBFSTemporalRetriever
    from kg_agent.experience_operator_routing import get_egor_router
    from kg_agent.temporal_faithfulness_critic import get_tfc

    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
    n = 200
    apply_config({"dataset": "MultiTQ", "max_depth": 3, "max_questions": n, "skip_questions": 0})
    with open(TPKGConfig.get_test_data_path(), encoding="utf-8") as f:
        gold_q = json.load(f)[:n]
    blind_q = []
    for item in gold_q:
        b = copy.deepcopy(item)
        b["qtype"] = ""
        b["Quid"] = item.get("quid") or item.get("id")
        blind_q.append(b)

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
    spec = VARIANT_SPECS["FULL"]

    p_gold = run_variant("FULL_gold", spec, gold_q, db, encode, retriever, router, critic)
    p_blind = run_variant("FULL_blind", spec, blind_q, db, encode, retriever, router, critic)

    h_g = [r["is_correct"] for r in p_gold["results"]]
    h_b = [r["is_correct"] for r in p_blind["results"]]
    ph_g = [r["path_hit@80"] for r in p_gold["results"]]
    ph_b = [r["path_hit@80"] for r in p_blind["results"]]
    ci = paired_bootstrap_ci(h_g, h_b)

    out = {
        "n": n,
        "gold_type_FULL": {
            "hits@1": 100 * sum(h_g) / n,
            "path_hit@80": 100 * sum(ph_g) / n,
        },
        "blind_type_FULL": {
            "hits@1": 100 * sum(h_b) / n,
            "path_hit@80": 100 * sum(ph_b) / n,
        },
        "paired_gold_minus_blind_pp": ci,
        "note": "Blind qtype exercises lexical/memory routing; LLM-Select branch still not invoked.",
    }
    path = PROJECT / "results/paper/egor_unlabeled_pilot_n200.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
