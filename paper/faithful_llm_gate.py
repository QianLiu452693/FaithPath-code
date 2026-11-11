#!/usr/bin/env python3
"""
Minimal closed-loop gate study (retrieval layer): compare always-answer vs PathHit/TFC gates on n<=500.
Optional: --ollama-model for top-path + LLM rerank (requires Ollama).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def gate_study(rows: list[dict], n: int) -> dict:
    rows = rows[:n]
    policies = {
        "always": lambda r: True,
        "pathhit": lambda r: r.get("path_hit@80"),
        "combined": lambda r: r.get("path_hit@80") and (r.get("tfc_score") or 0) >= 0.93,
    }
    out = {}
    for name, fn in policies.items():
        ans = [r for r in rows if fn(r)]
        cor = sum(1 for r in ans if r["is_correct"])
        out[name] = {
            "n_eval": len(rows),
            "coverage": len(ans) / len(rows) if rows else 0,
            "hits@1_answered": cor / len(ans) if ans else 0,
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="results/paper/comparison_20261108_203409/FULL.json")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--ollama-model", default=None)
    args = ap.parse_args()
    inp = ROOT / args.input
    rows = json.loads(inp.read_text(encoding="utf-8"))["results"]
    rep = {"subset_n": args.n, "retrieval_gates": gate_study(rows, args.n)}
    llm_path = ROOT / "results/paper/llm_selection_n200.json"
    if llm_path.is_file() and args.n <= 200:
        rep["llm_closed_loop"] = json.loads(llm_path.read_text(encoding="utf-8"))
    elif args.ollama_model:
        rep["llm"] = {
            "status": "run",
            "cmd": "python paper/run_llm_selection_experiment.py --n 200",
        }
    out = inp.parent / f"gate_subset_n{args.n}.json"
    out.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
