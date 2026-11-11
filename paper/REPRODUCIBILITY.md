# Reproducibility notes (FaithPath evidence-layer runs)

## Code entrypoints
- Comparison / ablation suite: `memotime/comparison_experiment.py`
- Scale / full-test drivers: `memotime/run_scale_experiments.py` (if present), results under `results/paper/`
- Config / DB paths: `memotime/config.py` → MultiTQ / TimeQuestions SQLite + candidate JSON

## Data splits (deterministic prefixes)
- MultiTQ test file: `Data/MultiTQ/questions_with_candidates_multitq.json`
- TimeQuestions test file: via `TPKGConfig.get_test_data_path()` after `dataset=TimeQuestions`
- Prefix protocol: contiguous slice `[skip : skip+n]` with default `--skip 0`
  - typed ablations: MultiTQ `n=500`, TimeQuestions `n=200`
  - diagnostic B2/noise ledger: MultiTQ `n=500` → `results/paper/comparison_20261108_180343/`
  - PathHit@k + MEMO_R: `results/paper/comparison_20261108_195018/` (`failure_buckets_n500.json`, `leaderboard.json`)
  - Regenerate figures: `python paper/gen_all_figures.py`; `python paper/plot_pathhit_k.py --dir results/paper/comparison_20261108_195018`
  - ELDB bucket vs k_ref: `python paper/plot_bucket_kref.py` → `bucket_kref_sweep_n500.json`, `figures/fig_bucket_kref.png`
  - Proximity by type: `python paper/analyze_proximity_breakdown.py` → `proximity_breakdown_n500.json`
  - KBS reliability gates: `comparison_20261108_203409/` (re-run FULL with `faithful` fields); `python paper/analyze_tfc_abstention.py`; `python paper/faithful_llm_gate.py --n 200`
  - Full-test EGOR (A1 vs FULL): A1 `comparison_20261108_203409/A1.json`, FULL `comparison_20261108_002112/FULL.json`; paired CI `results/paper/egor_fulltest_a1_vs_full.json`
  - Selection-gap oracle: `python paper/analyze_selection_gap_oracle.py` → `selection_gap_oracle_n500.json`
  - Oracle module gap (n=500): `python paper/analyze_oracle_module_gap.py` → `oracle_module_gap_n500.json`
  - Full-test selection-gap oracle sample: `python paper/analyze_oracle_full_sample.py 180` → `oracle_full_selection_gap_sample.json`
  - EGOR blind-type pilot: `python paper/run_egor_unlabeled_pilot.py` → `egor_unlabeled_pilot_n200.json`
  - LLM closed-loop (Ollama): ensure `.env` has `LLM_BACKEND=ollama`, `LLM_MODEL=qwen2.5:3b`; run `python paper/run_llm_selection_experiment.py --n 200 --top-paths 5` → `llm_selection_n200.json` (~5 min retrieval + ~40 min LLM on 200q)
  - 7B repeat: `python paper/run_llm_selection_experiment.py --n 200 --model qwen2.5:7b --out results/paper/llm_selection_n200_7b.json`
  - EGOR LLM-Select probe: `python paper/run_egor_llm_select_pilot.py --n 200 --compact` → `egor_llm_select_pilot_n200.json`
  - Artifact index: Table `tab:artifacts` in tex; this file lists run commands
  - full MultiTQ: `n=54584` → `results/paper/fulltest_multitq_20261108/`
  - full TimeQuestions: `n=3237` → scale report `results/paper/scale_experiments_20261107_225601/`

## Seeds / determinism
- Encoder: `sentence-transformers/all-MiniLM-L6-v2` on CUDA
- Paired bootstrap: `n_boot=2000`, `seed=0` in `paired_bootstrap_ci`
- Seed-noise: per-question MD5(`qid:eta`) → NumPy Generator; replaces `ceil(eta*|S|)` seeds
- BiBFS greedy Top-$k$ (no stochastic sampling) → Hits@1 deterministic for fixed encoder build

## Canonical timing (L3)
| Ledger | FULL wall | FULL s/q | B2 wall | Use |
|--------|-----------|----------|---------|-----|
| Diagnostic `comparison_20261108_180343` | **322 s** | **0.64** | 13 s | Table `tab:diag` (canonical absolutes) |
| Earlier ablation fig4 ledger | ≈211 s | ≈0.42 | — | Fig. runtime relative bars only |
| MultiTQ full test | ≈27533 s | ≈0.50 | ≈1220 s | full-test text |

## Reproduce diagnostic table
```bash
cd MemoTime-main
python memotime/comparison_experiment.py --dataset MultiTQ --questions 500 \
  --variants "FULL,B2,F_notf,F_noprox,F_noprune,F_nomem,SN10,SN20,SN30" --gpu 0
```

## Not reproduced under our protocol (L4)
Trained EXAQT, ConTExT, TECQA retrieval stages, MemoTime full LLM agent, RTQA/Temp-R1.
