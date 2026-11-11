# Scale Experiments Report — 20261107_191938
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU
- Wall: 2618.6s
- Variants: `B0,B1,B2,A1,A2,A3,FULL`

> No cloud API key detected for FaithPath+LLM closed-loop; EXAQT not reimplemented (mark as unmatched strong baseline).

## MultiTQ (n=2000)

| Variant | Hits@1 | Path@80 | sec |
|---------|--------|---------|-----|
| B0 | 10.15 | 0 | 0.0 |
| B1 | 19.7 | 71.65 | 3.7 |
| B2 | 24.7 | 58.8 | 172.5 |
| A1 | 22.2 | 58.3 | 33.0 |
| A2 | 23.35 | 59.4 | 960.8 |
| A3 | 22.15 | 58.3 | 20.8 |
| FULL | 23.3 | 59.4 | 930.3 |

### Paired bootstrap Hits@1 vs B0 / FULL

- **B0** vs B0 Δ=+0.00 CI[+0.00,+0.00] (ns); vs FULL Δ=-13.15 CI[-15.30,-10.95] (sig)
- **B1** vs B0 Δ=+9.55 CI[+7.55,+11.40] (sig); vs FULL Δ=-3.60 CI[-5.70,-1.65] (sig)
- **B2** vs B0 Δ=+14.55 CI[+12.40,+16.75] (sig); vs FULL Δ=+1.40 CI[+0.20,+2.65] (sig)
- **A1** vs B0 Δ=+12.05 CI[+10.00,+14.20] (sig); vs FULL Δ=-1.10 CI[-2.15,+0.00] (ns)
- **A2** vs B0 Δ=+13.20 CI[+11.00,+15.35] (sig); vs FULL Δ=+0.05 CI[+0.00,+0.15] (ns)
- **A3** vs B0 Δ=+12.00 CI[+9.95,+14.15] (sig); vs FULL Δ=-1.15 CI[-2.25,-0.05] (sig)
- **FULL** vs B0 Δ=+13.15 CI[+10.95,+15.30] (sig)

## TimeQuestions (n=1000)

| Variant | Hits@1 | Path@80 | sec |
|---------|--------|---------|-----|
| B0 | 4.1 | 0 | 0.0 |
| B1 | 24.9 | 58.5 | 1.9 |
| B2 | 23.4 | 61.5 | 256.3 |
| A1 | 23.4 | 61.6 | 45.8 |
| A2 | 24.1 | 59.4 | 3.0 |
| A3 | 23.4 | 61.6 | 4.8 |
| FULL | 24.1 | 59.4 | 1.4 |

### Paired bootstrap Hits@1 vs B0 / FULL

- **B0** vs B0 Δ=+0.00 CI[+0.00,+0.00] (ns); vs FULL Δ=-20.00 CI[-23.10,-17.20] (sig)
- **B1** vs B0 Δ=+20.80 CI[+17.80,+23.70] (sig); vs FULL Δ=+0.80 CI[-1.30,+2.90] (ns)
- **B2** vs B0 Δ=+19.30 CI[+16.50,+22.30] (sig); vs FULL Δ=-0.70 CI[-2.10,+0.60] (ns)
- **A1** vs B0 Δ=+19.30 CI[+16.50,+22.30] (sig); vs FULL Δ=-0.70 CI[-2.00,+0.50] (ns)
- **A2** vs B0 Δ=+20.00 CI[+17.20,+23.10] (sig); vs FULL Δ=+0.00 CI[+0.00,+0.00] (ns)
- **A3** vs B0 Δ=+19.30 CI[+16.50,+22.30] (sig); vs FULL Δ=-0.70 CI[-2.00,+0.50] (ns)
- **FULL** vs B0 Δ=+20.00 CI[+17.20,+23.10] (sig)
