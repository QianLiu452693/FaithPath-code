#!/usr/bin/env python3
"""FULL vs F_noprox Hits@1 delta by qlabel and qtype."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMP = ROOT / "results/paper/comparison_20261108_180343"


def load(v):
    data = json.loads((COMP / f"{v}.json").read_text(encoding="utf-8"))
    return {r["qid"]: r for r in data["results"]}


def stats(full, nop, key_fn):
    buckets = defaultdict(lambda: {"n": 0, "full_ok": 0, "nop_ok": 0})
    for qid, r in full.items():
        k = key_fn(r)
        buckets[k]["n"] += 1
        if r.get("is_correct"):
            buckets[k]["full_ok"] += 1
        if nop[qid].get("is_correct"):
            buckets[k]["nop_ok"] += 1
    out = {}
    for k, o in sorted(buckets.items()):
        out[k] = {
            **o,
            "full_hits1_pct": 100.0 * o["full_ok"] / o["n"],
            "noprox_hits1_pct": 100.0 * o["nop_ok"] / o["n"],
            "delta_pp": 100.0 * (o["nop_ok"] - o["full_ok"]) / o["n"],
        }
    return out


def main():
    full = load("FULL")
    nop = load("F_noprox")
    payload = {
        "comparison_dir": str(COMP),
        "by_qlabel": stats(full, nop, lambda r: r.get("qlabel") or "unknown"),
        "by_qtype": stats(full, nop, lambda r: r.get("qtype") or "unknown"),
        "overall_delta_pp": 100.0
        * (sum(1 for q in full if nop[q].get("is_correct")) - sum(1 for q in full if full[q].get("is_correct")))
        / len(full),
    }
    out = ROOT / "results/paper/proximity_breakdown_n500.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["by_qlabel"], indent=2))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
