#!/usr/bin/env python3
"""Reliability gates: TFC score, PathHit evidence, and combined abstention (ELDB n=500)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent


def _gate_metrics(rows: list[dict], accept_fn) -> dict:
    n = len(rows)
    acc = [r for r in rows if accept_fn(r)]
    if not acc:
        return {"coverage": 0.0, "risk": 100.0, "hits@1_on_answered": 0.0, "n_answered": 0}
    correct = sum(1 for r in acc if r["is_correct"])
    return {
        "coverage": 100.0 * len(acc) / n,
        "risk": 100.0 * (1.0 - correct / len(acc)),
        "hits@1_on_answered": 100.0 * correct / len(acc),
        "n_answered": len(acc),
    }


def score_risk_coverage(rows: list[dict]) -> tuple[list[float], list[float]]:
    scores = np.array([float(r["tfc_score"]) for r in rows if r.get("tfc_score") is not None])
    correct = np.array([1 if r["is_correct"] else 0 for r in rows if r.get("tfc_score") is not None])
    if len(scores) == 0:
        scores = np.array([0.5] * len(rows))
        correct = np.array([1 if r["is_correct"] else 0 for r in rows])
    order = np.argsort(-scores)
    scores = scores[order]
    correct = correct[order]
    n = len(correct)
    covs, risks = [], []
    for k in range(5, n + 1, max(1, n // 40)):
        sub = correct[:k]
        covs.append(100.0 * k / n)
        risks.append(100.0 * (1.0 - sub.mean()))
    return covs, risks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-json", default=None)
    ap.add_argument("--out-fig", default="paper/figures/fig_tfc_risk_coverage.pdf")
    args = ap.parse_args()
    inp = Path(args.input)
    if not inp.is_absolute():
        inp = ROOT / inp
    rows = json.loads(inp.read_text(encoding="utf-8")).get("results") or []
    if not rows[0].get("tfc_score"):
        raise SystemExit("Re-run FULL with faithful/tfc_score fields")

    baseline = 100.0 * sum(1 for r in rows if not r["is_correct"]) / len(rows)

    gates = {
        "always_answer": _gate_metrics(rows, lambda r: True),
        "pathhit_evidence_gate": _gate_metrics(rows, lambda r: r.get("path_hit@80")),
        "tfc_score_ge_0.93": _gate_metrics(rows, lambda r: (r.get("tfc_score") or 0) >= 0.93),
        "combined_pathhit_and_tfc093": _gate_metrics(
            rows, lambda r: r.get("path_hit@80") and (r.get("tfc_score") or 0) >= 0.93
        ),
    }
    # strict bit (calibrated operating point; global Faithful is permissive at default theta_f)
    acc_hi = _gate_metrics(rows, lambda r: (r.get("tfc_score") or 0) >= 0.935)
    acc_lo = _gate_metrics(rows, lambda r: (r.get("tfc_score") or 0) < 0.92)

    payload = {
        "n": len(rows),
        "baseline_error_pct": baseline,
        "gates": gates,
        "tfc_score_high_band_ge_0.935": acc_hi,
        "tfc_score_low_band_lt_0.92": acc_lo,
        "note": (
            "Default Faithful bit is permissive on this prefix (all True); "
            "report score- and PathHit-gated operating points for KBS reliability narrative."
        ),
    }
    print(json.dumps(payload, indent=2))
    outj = Path(args.out_json) if args.out_json else inp.parent / "tfc_abstention.json"
    if not outj.is_absolute():
        outj = ROOT / outj
    outj.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    covs, risks = score_risk_coverage(rows)
    fig, ax = plt.subplots(figsize=(4.5, 3.3))
    ax.plot(covs, risks, color="#4361ee", linewidth=1.6, label="TFC score rank")
    ph = gates["pathhit_evidence_gate"]
    ax.scatter([ph["coverage"]], [ph["risk"]], c="#e76f51", s=60, zorder=5, label="PathHit@80 gate")
    ax.axhline(baseline, color="0.6", linestyle=":", linewidth=1, label=f"Always answer ({baseline:.0f}\\% err)")
    ax.set_xlabel(r"Coverage (\%)")
    ax.set_ylabel(r"Risk / error rate (\%)")
    ax.set_title("FaithPath reliability: risk--coverage (MultiTQ $n{=}500$)")
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out_fig = Path(args.out_fig)
    if not out_fig.is_absolute():
        out_fig = ROOT / out_fig
    out_fig.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_fig, bbox_inches="tight")
    print("saved", out_fig)


if __name__ == "__main__":
    main()
