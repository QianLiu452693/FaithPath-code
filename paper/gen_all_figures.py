#!/usr/bin/env python3
"""Regenerate paper figures 1--9 + pathhit (FaithPath / ELDB branding)."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PAPER = Path(__file__).resolve().parent
OUT = PAPER / "figures"
PREFIX_RUN = ROOT / "results" / "paper" / "comparison_20261106_214356"
PATHHIT_RUN = ROOT / "results" / "paper" / "comparison_20261108_195018"

BRAND = "FaithPath"
SUB = "ELDB protocol, MultiTQ $n{=}500$"  # for suptitles


def load_summary(run: Path, variant: str) -> dict:
    p = run / f"{variant}.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    return data["summary"]


def save(fig, name: str):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=200, bbox_inches="tight")
    print("wrote", OUT / f"{name}.pdf")


def fig1():
    ids = ["B0", "B1", "A1", "A3", "S1", "H1", "FULL"]
    labels = ["B0", "B1", "A1", "A3", "S1", "H1", f"{BRAND}\nFULL"]
    hits = [load_summary(PREFIX_RUN, v)["overall_hits@1"] for v in ids]
    colors = ["#9e9e9e", "#bdbdbd", "#8ecae6", "#219ebc", "#ffb703", "#fb8500", "#023047"]
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    x = np.arange(len(labels))
    bars = ax.bar(x, hits, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Hits@1 (%)")
    ax.set_ylim(0, 30)
    ax.set_title(f"{BRAND} retrieval-only variants ({SUB})")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.3, f"{b.get_height():.1f}",
                ha="center", va="bottom", fontsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    save(fig, "fig1_hits_variants")


def fig2_3():
    b1 = load_summary(PREFIX_RUN, "B1")
    full = load_summary(PREFIX_RUN, "FULL")
    labels = ["B1 OneHop", f"{BRAND} FULL"]
    ph = [b1["path_hit@80"], full["path_hit@80"]]
    h1 = [b1["overall_hits@1"], full["overall_hits@1"]]

    fig, ax = plt.subplots(figsize=(4.2, 3.4))
    x = np.arange(2)
    ax.bar(x, ph, color=["#90be6d", "#577590"], edgecolor="k", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("PathHit@80 (%)")
    ax.set_title(f"Evidence recall ({SUB})")
    for i, v in enumerate(ph):
        ax.text(i, v + 1, f"{v:.1f}", ha="center", fontsize=8)
    fig.tight_layout()
    save(fig, "fig2_pathhit")

    fig, ax = plt.subplots(figsize=(4.5, 3.4))
    w = 0.35
    ax.bar(x - w / 2, ph, w, label="PathHit@80", color="#577590")
    ax.bar(x + w / 2, h1, w, label="Hits@1", color="#f94144")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("(%)")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title(f"{BRAND} FULL: evidence vs answer hit")
    fig.tight_layout()
    save(fig, "fig3_hits_vs_pathhit")


def fig4():
    # earlier ablation ledger (relative); canonical in tab:diag
    names = ["B0", "B1", "A1", "H1", "FULL"]
    sec = [0.0, 1.4, 180.0, 15.0, 211.0]  # documented relative ledger
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    y = np.arange(len(names))
    ax.barh(y, sec, color="#457b9d", edgecolor="k", linewidth=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{BRAND} {n}" if n == "FULL" else n for n in names])
    ax.set_xlabel("Wall time (s), $n{=}500$ prefix")
    ax.set_xscale("symlog", linthresh=5)
    ax.set_title(f"{BRAND} latency (relative ablation ledger)")
    fig.tight_layout()
    save(fig, "fig4_runtime")


def fig5():
    full = load_summary(PREFIX_RUN, "FULL")["overall_hits@1"]
    deltas = []
    labs = []
    mapping = [
        ("B1", "w/o BiBFS (B1)"),
        ("A1", "w/o EGOR (A1)"),
        ("S1", "w/o DRM (S1)"),
        ("H1", "w/o depth (H1)"),
        ("A3", "w/o EGOR stack (A3)"),
        ("B0", "w/o KG (B0)"),
    ]
    for vid, lab in mapping:
        h = load_summary(PREFIX_RUN, vid)["overall_hits@1"]
        deltas.append(h - full)
        labs.append(lab)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    y = np.arange(len(labs))
    colors = ["#d62828" if d < 0 else "#2a9d8f" for d in deltas]
    ax.barh(y, deltas, color=colors, edgecolor="k", linewidth=0.4)
    ax.axvline(0, color="0.3", linewidth=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(labs, fontsize=8)
    ax.set_xlabel(r"$\Delta$ Hits@1 vs FaithPath FULL (pp)")
    ax.set_title(f"{BRAND} ablation deltas ({SUB})")
    fig.tight_layout()
    save(fig, "fig5_ablation_delta")


def fig6():
    s = load_summary(PREFIX_RUN, "FULL")
    ql = s["by_qlabel"]
    at = s["by_answer_type"]
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    cats = ["Multiple", "Single", "Entity", "Time"]
    vals = [ql["Multiple"]["hits@1"], ql["Single"]["hits@1"],
            at["entity"]["hits@1"], at["time"]["hits@1"]]
    ax.bar(cats, vals, color=["#e76f51", "#2a9d8f", "#264653", "#e9c46a"], edgecolor="k", linewidth=0.5)
    ax.set_ylabel("Hits@1 (%)")
    ax.set_title(f"{BRAND} FULL typed Hits@1 ({SUB})")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.5, f"{v:.1f}", ha="center", fontsize=8)
    fig.tight_layout()
    save(fig, "fig6_typed_multitq")


def fig7():
    s = load_summary(PREFIX_RUN, "FULL")
    qtypes = sorted(s["by_qtype"].keys())
    vals = [s["by_qtype"][q]["hits@1"] for q in qtypes]
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    x = np.arange(len(qtypes))
    ax.bar(x, vals, color="#4361ee", edgecolor="k", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(qtypes, rotation=35, ha="right", fontsize=7)
    ax.set_ylabel("Hits@1 (%)")
    ax.set_title(f"{BRAND} FULL by operator type ({SUB})")
    fig.tight_layout()
    save(fig, "fig7_operator_type")


def fig8():
    data = json.loads((PREFIX_RUN / "FULL.json").read_text(encoding="utf-8"))
    correct = sum(1 for r in data["results"] if r["is_correct"])
    miss = sum(1 for r in data["results"] if not r["is_correct"] and not r.get("path_hit@80"))
    gap = sum(1 for r in data["results"] if not r["is_correct"] and r.get("path_hit@80"))
    tq = load_summary(ROOT / "results" / "paper" / "comparison_20261106_214356", "FULL")
    # TQ n=200 from tab:t2 style - use B0 B1 FULL from another run if exists
    tq_run = ROOT / "results" / "paper"
    tq_hits = {"B0": 3.5, "B1": 21.0, "FULL": 23.0}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2))
    ax1.bar(["B0", "B1", f"{BRAND}\nFULL"], [tq_hits["B0"], tq_hits["B1"], tq_hits["FULL"]],
            color=["#adb5bd", "#6c757d", "#023047"], edgecolor="k", linewidth=0.5)
    ax1.set_ylabel("Hits@1 (%)")
    ax1.set_title("TimeQuestions $n{=}200$")

    sizes = [correct, gap, miss]
    labs = ["Correct", "Selection gap", "Evidence miss"]
    cols = ["#2a9d8f", "#f4a261", "#e76f51"]
    ax2.pie(sizes, labels=labs, autopct="%1.1f%%", colors=cols, startangle=90, textprops={"fontsize": 8})
    ax2.set_title(f"{BRAND} FULL outcome mix (ELDB buckets)")
    fig.suptitle(f"{BRAND} / ELDB error taxonomy", fontsize=10, y=1.02)
    fig.tight_layout()
    save(fig, "fig8_tq_and_errors")


def fig9():
    variants = ["B0", "B1", "B2", f"{BRAND}\nFULL"]
    mt = [10.8, 20.0, 25.1, 24.3]
    tq = [4.7, 24.2, 23.2, 23.0]
    x = np.arange(len(variants))
    w = 0.38
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    b1 = ax.bar(x - w / 2, mt, w, label="MultiTQ full", color="#2c7fb8", hatch="//", edgecolor="black", linewidth=0.6)
    b2 = ax.bar(x + w / 2, tq, w, label="TimeQuestions full", color="#fdd49e", hatch="\\\\", edgecolor="black", linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(variants)
    ax.set_ylabel("Hits@1 (%)")
    ax.set_ylim(0, 32)
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    ax.set_title(f"{BRAND} retrieval-only full-test Hits@1 (ELDB variants)")
    for bars in (b1, b2):
        for r in bars:
            h = r.get_height()
            ax.text(r.get_x() + r.get_width() / 2, h + 0.4, f"{h:.1f}", ha="center", va="bottom", fontsize=7)
    fig.tight_layout()
    save(fig, "fig9_scale_hits")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig1()
    fig2_3()
    fig4()
    fig5()
    fig6()
    fig7()
    fig8()
    fig9()
    print("Done. Run plot_pathhit_k.py for fig_pathhit_at_k.")


if __name__ == "__main__":
    main()
