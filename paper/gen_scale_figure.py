#!/usr/bin/env python3
"""Generate scale-up Hits@1 bar chart (vector PDF + PNG)."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)

# MultiTQ full n=54584 / TQ full n=3237
variants = ["B0", "B1", "B2", "FULL"]
mt = [10.8, 20.0, 25.1, 24.3]
tq = [4.7, 24.2, 23.2, 23.0]

x = np.arange(len(variants))
w = 0.38
fig, ax = plt.subplots(figsize=(6.2, 3.4))
b1 = ax.bar(x - w / 2, mt, w, label="MultiTQ full $n{=}54584$", color="#2c7fb8", hatch="//", edgecolor="black", linewidth=0.6)
b2 = ax.bar(x + w / 2, tq, w, label="TQ full $n{=}3237$", color="#fdd49e", hatch="\\\\", edgecolor="black", linewidth=0.6)
ax.set_xticks(x)
ax.set_xticklabels(variants)
ax.set_ylabel("Hits@1 (%)")
ax.set_ylim(0, 32)
ax.legend(frameon=False, loc="upper left")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
for bars in (b1, b2):
    for r in bars:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width() / 2, h + 0.4, f"{h:.1f}", ha="center", va="bottom", fontsize=7)
ax.set_title("Full-test retrieval-only Hits@1: B0/B1 vs B2 vs FaithPath FULL")
fig.tight_layout()
fig.savefig(OUT / "fig9_scale_hits.pdf")
fig.savefig(OUT / "fig9_scale_hits.png", dpi=200)
print("saved", OUT / "fig9_scale_hits.pdf")
