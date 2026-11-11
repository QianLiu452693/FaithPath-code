#!/usr/bin/env python3
"""ELDB bucket shares vs k_ref from per-question path_hit@k flags."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent


def bucket_at_k(row: dict, k: int) -> str:
    if row.get("is_correct"):
        return "correct"
    key = f"path_hit@{k}"
    if not row.get(key, False):
        return "evidence_miss"
    return "selection_gap"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="results/paper/comparison_20261108_195018/FULL.json")
    ap.add_argument("--ks", default="1,5,10,20,40,80,120,160")
    ap.add_argument("--out-json", default="results/paper/bucket_kref_sweep_n500.json")
    ap.add_argument("--out-pdf", default="paper/figures/fig_bucket_kref.png")
    args = ap.parse_args()
    inp = ROOT / args.input if not Path(args.input).is_absolute() else Path(args.input)
    data = json.loads(inp.read_text(encoding="utf-8"))
    rows = data["results"]
    n = len(rows)
    ks = [int(x) for x in args.ks.split(",")]
    series = []
    for k in ks:
        counts = {"correct": 0, "evidence_miss": 0, "selection_gap": 0}
        for r in rows:
            counts[bucket_at_k(r, k)] += 1
        wrong = counts["evidence_miss"] + counts["selection_gap"]
        series.append(
            {
                "k_ref": k,
                "counts": counts,
                "pct_of_all": {b: 100.0 * counts[b] / n for b in counts},
                "pct_of_errors": {
                    "evidence_miss": 100.0 * counts["evidence_miss"] / wrong if wrong else 0.0,
                    "selection_gap": 100.0 * counts["selection_gap"] / wrong if wrong else 0.0,
                },
            }
        )
    payload = {"n": n, "variant": "FULL", "source": str(inp), "series": series}
    out_json = ROOT / args.out_json
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(5.0, 3.5))
    x = [s["k_ref"] for s in series]
    em = [s["pct_of_errors"]["evidence_miss"] for s in series]
    sg = [s["pct_of_errors"]["selection_gap"] for s in series]
    ax.plot(x, em, "o-", color="#c0392b", label="evidence\\_miss (% of errors)")
    ax.plot(x, sg, "s-", color="#2980b9", label="selection\\_gap (% of errors)")
    ax.axvline(80, color="0.65", linestyle=":", linewidth=1, label="default $k_{\\mathrm{ref}}{=}80$")
    ax.set_xlabel("$k_{\\mathrm{ref}}$ (PathHit cutoff)")
    ax.set_ylabel("Share of incorrect items (%)")
    ax.set_xscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([str(k) for k in x])
    ax.legend(fontsize=8, loc="center right")
    ax.grid(True, alpha=0.3)
    ax.set_title(r"ELDB buckets vs $k_{\mathrm{ref}}$ (FULL, $n=500$)")
    out_pdf = ROOT / args.out_pdf
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_pdf)
    # Also write PDF next to PNG for Overleaf / pdflatex
    pdf_path = out_pdf.with_suffix(".pdf")
    try:
        fig.savefig(pdf_path)
    except Exception as e:
        print(f"PDF save skipped: {e}")
    print(f"Wrote {out_json}, {out_pdf}, {pdf_path}")


if __name__ == "__main__":
    main()
