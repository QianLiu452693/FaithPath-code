#!/usr/bin/env python3
"""Plot PathHit@k curves from comparison_experiment summary JSONs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent


def load_curve(path: Path) -> tuple[list[int], list[float]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    s = data.get("summary") or data
    curve = s.get("path_hit_at_k")
    if not curve:
        k_list = [1, 5, 10, 20, 40, 80, 120, 160]
        curve = {str(k): s.get("path_hit@80", 0) if k == 80 else None for k in k_list}
        curve = {k: v for k, v in curve.items() if v is not None}
    ks = sorted(int(k) for k in curve.keys())
    ys = [float(curve[str(k)]) for k in ks]
    return ks, ys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="directory with B0.json, B1.json, ...")
    ap.add_argument("--variants", default="B0,B1,B2,FULL,MEMO_R")
    ap.add_argument("--out", default="paper/figures/fig_pathhit_at_k.pdf")
    args = ap.parse_args()
    d = Path(args.dir)
    if not d.is_absolute():
        d = ROOT / d
    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)

    styles = {
        "B0": ("--", "#888888"),
        "B1": ("-", "#1f77b4"),
        "B2": ("-", "#ff7f0e"),
        "FULL": ("-", "#2ca02c"),
        "MEMO_R": ("-.", "#9467bd"),
    }
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    for vid in args.variants.split(","):
        vid = vid.strip()
        f = d / f"{vid}.json"
        if not f.exists():
            print(f"skip missing {f}")
            continue
        ks, ys = load_curve(f)
        ls, col = styles.get(vid, ("-", "black"))
        avg_p = json.loads(f.read_text(encoding="utf-8"))["summary"].get("avg_paths", 0)
        ax.plot(ks, ys, linestyle=ls, color=col, marker="o", markersize=4,
                label=f"{vid} (avg $|P|={avg_p:.0f}$)")
    ax.axvline(80, color="0.7", linestyle=":", linewidth=1)
    ax.text(82, ax.get_ylim()[0] + 2, "$k{=}80$", fontsize=8, color="0.4")
    ax.set_xlabel("PathHit cutoff $k$ (top-$k$ paths)")
    ax.set_ylabel("PathHit@$k$ recall (\%)")
    ax.set_title("FaithPath / ELDB: PathHit@$k$ evidence recall ($n{=}500$)")
    ax.legend(fontsize=7, loc="lower right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
