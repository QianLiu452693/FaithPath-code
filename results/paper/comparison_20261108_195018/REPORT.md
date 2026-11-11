# PathHit@k + MEMO_R diagnostic run (MultiTQ n=500)

**Command:** `comparison_experiment.py -q 500 --variants B0,B1,B2,FULL,MEMO_R`

## Leaderboard (Hits@1 / PathHit@80 / avg |P| / sec)

| Variant | Hits@1 | Path@80 | avg |P| | sec |
|---------|--------|---------|---------|-----|
| B2 | 26.2% | 57.2% | 73.7 | 72.3 |
| FULL | 24.8% | 58.4% | 72.1 | 246.7 |
| MEMO_R | 24.8% | 58.4% | 72.1 | 215.0 |
| B1 | 20.0% | 74.2% | 80.0 | 1.4 |
| B0 | 10.8% | 0.0% | 0.0 | 0.0 |

## PathHit@k (key points)

- B1 @80 = 74.2% but @1 = 23.6%; FULL @1 = 34.2%, @20 = 50.8% (beats B1 top-k ranking at small k).
- See `leaderboard.json` → `path_hit_at_k` per variant.

## Artifacts

- `failure_buckets_n500.json` — 500-row protocol buckets (124 correct / 208 evidence miss / 168 selection gap)
- Figure: `paper/figures/fig_pathhit_at_k.pdf`
