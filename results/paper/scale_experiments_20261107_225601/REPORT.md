# Scale Experiments Report — 20261107_225601
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU
- Wall: 3734.1s
- Variants: `B0,B1,B2,A1,FULL`

> No cloud API key detected for FaithPath+LLM closed-loop; EXAQT not reimplemented (mark as unmatched strong baseline).

## MultiTQ (n=5000)

| Variant | Hits@1 | Path@80 | sec |
|---------|--------|---------|-----|
| B0 | 10.9 | 0 | 0.0 |
| B1 | 19.84 | 70.62 | 9.0 |
| B2 | 24.66 | 59.98 | 282.3 |
| A1 | 22.84 | 59.66 | 71.6 |
| FULL | 23.72 | 60.48 | 2480.3 |

### Paired bootstrap Hits@1 vs B0 / FULL

- **B0** vs B0 Δ=+0.00 CI[+0.00,+0.00] (ns); vs FULL Δ=-12.82 CI[-14.24,-11.34] (sig)
- **B1** vs B0 Δ=+8.94 CI[+7.72,+10.16] (sig); vs FULL Δ=-3.88 CI[-5.14,-2.66] (sig)
- **B2** vs B0 Δ=+13.76 CI[+12.28,+15.12] (sig); vs FULL Δ=+0.94 CI[+0.24,+1.62] (sig)
- **A1** vs B0 Δ=+11.94 CI[+10.52,+13.32] (sig); vs FULL Δ=-0.88 CI[-1.56,-0.22] (sig)
- **FULL** vs B0 Δ=+12.82 CI[+11.34,+14.24] (sig)

## TimeQuestions (n=3237)

| Variant | Hits@1 | Path@80 | sec |
|---------|--------|---------|-----|
| B0 | 4.7 | 0 | 0.0 |
| B1 | 24.16 | 57.65 | 5.3 |
| B2 | 23.23 | 60.89 | 542.4 |
| A1 | 23.14 | 60.92 | 113.2 |
| FULL | 22.98 | 58.48 | 13.3 |

### Paired bootstrap Hits@1 vs B0 / FULL

- **B0** vs B0 Δ=+0.00 CI[+0.00,+0.00] (ns); vs FULL Δ=-18.29 CI[-19.99,-16.56] (sig)
- **B1** vs B0 Δ=+19.46 CI[+17.82,+21.10] (sig); vs FULL Δ=+1.17 CI[+0.00,+2.32] (ns)
- **B2** vs B0 Δ=+18.54 CI[+16.81,+20.11] (sig); vs FULL Δ=+0.25 CI[-0.53,+0.99] (ns)
- **A1** vs B0 Δ=+18.44 CI[+16.74,+20.05] (sig); vs FULL Δ=+0.15 CI[-0.56,+0.83] (ns)
- **FULL** vs B0 Δ=+18.29 CI[+16.56,+19.99] (sig)
