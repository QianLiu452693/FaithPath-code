# MultiTQ Full Test — retrieval-only
- Source: `../comparison_20261108_002112`
- n = **54584** (official MultiTQ test)
- Variants: B0, B1, B2, FULL
- Wall: expand + eval ≈ 8.1h (FULL alone ≈ 7.65h)

| Variant | Hits@1 | Path@80 | vs B0 | vs FULL |
|---------|--------|---------|-------|---------|
| B0 | 10.78 | 0.00 | — | −13.53 sig |
| B1 | 20.03 | 70.52 | +9.25 sig | −4.28 sig |
| **B2 EmbedMHOP** | **25.11** | 60.13 | +14.33 sig | **+0.80 sig** CI[+0.58,+1.01] |
| FULL | 24.31 | 60.88 | +13.53 sig | — |

**Takeaway:** On the full MultiTQ test, B2 significantly exceeds FaithPath FULL under retrieval-only Hits@1; FULL remains far above weak priors.
