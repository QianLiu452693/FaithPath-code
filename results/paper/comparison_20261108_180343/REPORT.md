# Diagnostic ablations — MultiTQ n=500 (2026-11-08)

Variants: FULL, B2, F_notf, F_noprox, F_noprune, F_nomem, SN10/20/30

| Variant | Hits@1 | Path@80 | sec |
|---------|--------|---------|-----|
| B2 | **26.2** | 57.2 | 13 |
| F_noprox | 25.6 | 58.4 | 220 |
| F_notf | 25.0 | 58.8 | 4 |
| F_noprune | 25.0 | 58.8 | 4 |
| FULL | 24.8 | 58.4 | 322 |
| F_nomem | 24.8 | 58.4 | 218 |
| SN20 | 21.2 | 59.6 | 223 |
| SN10 | 20.6 | 59.4 | 214 |
| SN30 | 19.8 | 58.8 | 216 |

**Takeaways**
- Proximity term hurts Hits@1 more than temporal-first prune on this prefix.
- Seed noise drops Hits@1 ~4–5pp while PathHit stays flat → selection fragility.
- EGOR memory off does not change Hits@1 when gold type priors exist.
- B2 remains best and fastest.