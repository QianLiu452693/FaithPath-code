# Knowledge-Based Systems (KBS) submission notes

## Positioning
- **FaithPath**: proposed knowledge-system stack (BiBFS + EGOR + TFC) — retrieve → verify → decide.
- **ELDB**: exportable evaluation protocol (PathHit, failure buckets, gates), not only FaithPath-internal tables.
- Emphasize **reliability / evaluation knowledge**, not “modules fail” or leaderboard SOTA.

## Key new artifacts (this pass)
| Artifact | Path |
|----------|------|
| TFC + PathHit gates | `results/paper/comparison_20261108_203409/tfc_abstention.json` |
| Risk–coverage figure | `paper/figures/fig_tfc_risk_coverage.pdf` |
| Gate subset n=200 | `results/paper/comparison_20261108_203409/gate_subset_n200.json` |
| Full-test A1 vs FULL | running: `memotime/comparison_experiment.py -q 54584 --variants A1,FULL` |

## LaTeX
- Content revisions in `FaithPath_IEEEtran.tex` (IEEE class placeholder).
- **Before upload to Elsevier**: port to `elsarticle` template (`Knowledge-Based Systems` → “Submit your manuscript” → LaTeX instructions).

## Suggested cover letter bullets
1. Novel knowledge-system architecture for temporal KG QA with explicit verification layer (TFC).
2. ELDB protocol and failure taxonomy for community reuse.
3. Empirical demonstration that PathHit ≫ Hits@1 — actionable diagnosis for RAG/KG systems.
4. Abstention operating points that improve answered accuracy under coverage constraints.

## Still recommended before final submit
- Complete full-test **A1 vs FULL** run and insert paired Δ + CI into §Experiments.
- Optional: Ollama/Qwen gate-on LLM pilot on n=200 (`paper/faithful_llm_gate.py --ollama-model …`).
- Tighten `theta_f` so binary Faithful is not saturated (optional ablation row `F_tfc_strict`).
