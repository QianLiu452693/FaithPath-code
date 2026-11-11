# Overleaf upload checklist

Upload the **main `.tex`** and the entire **`figures/`** folder (same relative paths as in the repo).

## Required with `FaithPath_IEEEtran.tex` in project root

- All files under `figures/` used by `\includegraphics` (including **`fig_bucket_kref.pdf`** or `.png`)
- `algo_main_deferred.tex` is **no longer required** (pseudocode is inlined in the appendix)

## If the main file lives under `paper/`

Set Overleaf **Main document** to `paper/FaithPath_IEEEtran.tex`, or upload `figures/` as `paper/figures/`.

## Regenerate `fig_bucket_kref`

```bash
python paper/plot_bucket_kref.py
```

Outputs: `paper/figures/fig_bucket_kref.png`, `fig_bucket_kref.pdf`, `results/paper/bucket_kref_sweep_n500.json`.
