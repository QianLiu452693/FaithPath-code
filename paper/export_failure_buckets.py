#!/usr/bin/env python3
"""Export protocol-defined failure buckets for the n=500 MultiTQ diagnostic prefix."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent


def bucket_row(r: dict) -> str:
    if r.get("is_correct"):
        return "correct"
    if r.get("path_hit@80"):
        return "selection_gap"
    return "evidence_miss"


def sub_tags(r: dict) -> list[str]:
    tags = []
    if r.get("qlabel") == "Multiple":
        tags.append("multi_seed")
    qtype = r.get("qtype") or ""
    if qtype in ("before_last", "after_first", "first_last"):
        tags.append("hard_operator")
    if r.get("n_paths", 0) == 0:
        tags.append("empty_pool")
    elif r.get("n_paths", 0) < 20:
        tags.append("shallow_pool")
    return tags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="e.g. results/paper/.../FULL.json")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    inp = Path(args.input)
    if not inp.is_absolute():
        inp = ROOT / inp
    data = json.loads(inp.read_text(encoding="utf-8"))
    rows = data.get("results") or []
    out_rows = []
    counts = Counter()
    for r in rows:
        b = bucket_row(r)
        counts[b] += 1
        out_rows.append({
            "qid": r.get("qid"),
            "bucket": b,
            "qtype": r.get("qtype"),
            "qlabel": r.get("qlabel"),
            "answer_type": r.get("answer_type"),
            "n_paths": r.get("n_paths"),
            "path_hit@80": r.get("path_hit@80"),
            "auto_tags": sub_tags(r),
            "manual_note": "",
        })
    summary = {
        "n": len(rows),
        "counts": dict(counts),
        "source": str(inp),
        "protocol": "bucket=correct|selection_gap|evidence_miss from path_hit@80 and is_correct",
    }
    payload = {"summary": summary, "annotations": out_rows}
    out = Path(args.output) if args.output else inp.parent / "failure_buckets_n500.json"
    if not out.is_absolute():
        out = ROOT / out
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
