#!/usr/bin/env python3
"""
Force EGOR LLM-Select branch (skip symbolic _egor_route) and measure operator agreement
with gold-qtype EGOR priors on MultiTQ prefix.

Usage:
  python paper/run_egor_llm_select_pilot.py --n 200
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

ROOT = Path(__file__).resolve().parents[1] / "memotime"
PROJECT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROJECT))

from load_env import load_dotenv  # noqa: E402


# LLM toolkit names → EGOR operator names (subset)
TOOLKIT_TO_EGOR = {
    "OneHop": "OneHop",
    "AfterFirst": "OneHopAfter",
    "BeforeLast": "OneHopBefore",
    "BetweenRange": "Between",
    "DayEvents": "SameDay",
    "MonthEvents": "SameMonth",
    "YearEvents": "When",
    "Timeline": "Timeline",
}


def _egor_equiv(llm_name: Optional[str], gold_ops: Set[str]) -> bool:
    if not llm_name:
        return False
    if llm_name in gold_ops:
        return True
    mapped = TOOLKIT_TO_EGOR.get(llm_name, llm_name)
    if mapped in gold_ops:
        return True
    # soft: OneHop family matches any OneHop*
    if llm_name == "OneHop" and any(o.startswith("OneHop") or o == "OneHop" for o in gold_ops):
        return True
    return False


def main():
    load_dotenv(PROJECT / ".env")
    os.environ.setdefault("LLM_VERBOSE", "0")
    os.environ.setdefault("LLM_BACKEND", "ollama")

    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--skip", type=int, default=0)
    ap.add_argument("--compact", action="store_true", help="Omit per-question rows in JSON")
    args = ap.parse_args()

    from config import apply_config, TPKGConfig
    from kg_agent.experience_operator_routing import get_egor_router
    from kg_agent.intelligent_toolkit_selector import IntelligentToolkitSelector

    apply_config({"dataset": "MultiTQ", "max_depth": 3, "max_questions": args.n, "skip_questions": args.skip})
    with open(TPKGConfig.get_test_data_path(), encoding="utf-8") as f:
        questions = json.load(f)[args.skip : args.skip + args.n]

    router = get_egor_router()
    selector = IntelligentToolkitSelector()
    # Never take symbolic EGOR path inside selector — exercise LLM-Select only.
    selector._egor_route = lambda *a, **k: []  # type: ignore[method-assign]

    def _seed_names(self, seeds, _names=None):
        if _names:
            return _names
        return IntelligentToolkitSelector._seed_ids_to_names(self, seeds)

    t0 = time.time()
    rows: List[Dict[str, Any]] = []
    n_match = 0
    n_fail = 0

    for i, item in enumerate(questions):
        if (i + 1) % 20 == 0:
            print(f"llm-select {i+1}/{len(questions)}", flush=True)
        q = item.get("question", "")
        qtype_gold = item.get("qtype") or ""
        cands = item.get("candidates") or []
        names = [c["name"] for c in cands[:3] if isinstance(c, dict) and c.get("name")]
        gold = router.route(question=q, qtype=qtype_gold)
        gold_ops = set(gold.operators or [])
        gold_primary = (gold.operators or [None])[0]

        from types import MethodType

        selector._seed_ids_to_names = MethodType(lambda self, seeds, n=names: _seed_names(self, seeds, n), selector)  # type: ignore

        try:
            picks = selector.select_toolkits(q, [0] * max(1, len(names)), {}, question_type="")
            llm_op = (picks[0].get("original_name") if picks else None)
            reasoning = (picks[0].get("reasoning") if picks else "")
            hit = _egor_equiv(llm_op, gold_ops)
            if hit:
                n_match += 1
            rows.append(
                {
                    "qid": item.get("quid") or item.get("id"),
                    "qtype_gold": qtype_gold,
                    "gold_primary": gold_primary,
                    "gold_ops": list(gold_ops),
                    "llm_op": llm_op,
                    "match": hit,
                    "reasoning": reasoning[:200],
                }
            )
        except Exception as e:
            n_fail += 1
            rows.append({"qid": item.get("quid"), "error": str(e), "match": False})

    n = len(questions)
    rep: Dict[str, Any] = {
        "n": n,
        "llm_model": os.getenv("TOOLKIT_SELECTION_LLM_MODEL") or os.getenv("LLM_MODEL"),
        "wall_sec": time.time() - t0,
        "operator_agreement_pct": 100.0 * n_match / n if n else 0.0,
        "n_match": n_match,
        "n_fail": n_fail,
        "note": "Forced LLM-Select (_egor_route disabled); agreement = LLM primary op vs gold EGOR operator set.",
    }
    if not args.compact:
        rep["per_question"] = rows
    out = PROJECT / f"results/paper/egor_llm_select_pilot_n{n}.json"
    out.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    summary = {k: rep[k] for k in rep if k != "per_question"}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
