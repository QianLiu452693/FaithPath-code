# Paper Experiments Report — 20261106_214256
- Paper: arXiv:2510.13614v3
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU
- Code: MemoTime + Inv1 BiBFS/D_pred + Inv2 EGOR + Inv3 TFC
- Wall: 1578.0s

> Cloud-LLM Table1/2/3 numbers need API keys. Here we run retrieval-grounded improved MemoTime on GPU with paper metrics/breakdowns.

## Table 1 / 4 / Hyper / Innovations — MultiTQ
n=500

| Variant | Paper-map | Hits@1 | Multiple | Single | Entity | Time | Path@80 | sec |
|---------|-----------|--------|----------|--------|--------|------|---------|-----|
| B0 | ≈ w/o Temporal Evidence Retrieval (candi | 10.8 | 5.19 | 12.88 | 15.65 | None | 0 | 0.0 |
| B1 | ≈ weak graph (OneHop lexical) | 20.0 | 11.11 | 23.29 | 24.93 | 9.03 | 74.2 | 1.0 |
| A1 | ≈ w/o EGOR (BiBFS only) | 23.4 | 16.3 | 26.03 | 25.51 | 18.71 | 56.6 | 82.5 |
| A2 | BiBFS+EGOR | 24.8 | 10.37 | 30.14 | 27.83 | 18.06 | 58.4 | 235.8 |
| A3 | BiBFS+TFC | 23.4 | 16.3 | 26.03 | 25.51 | 18.71 | 56.6 | 5.2 |
| FULL | MemoTime-Improved (BiBFS+EGOR+TFC) ≈ Ful | 24.8 | 10.37 | 30.14 | 27.83 | 18.06 | 58.4 | 210.6 |
| H1 | Full D_max=1 | 24.2 | 8.15 | 30.14 | 26.96 | 18.06 | 60.2 | 15.5 |
| H2 | Full D_max=2 | 24.8 | 10.37 | 30.14 | 27.83 | 18.06 | 58.4 | 211.4 |
| H3 | Full D_max=3 (paper) | 24.8 | 10.37 | 30.14 | 27.83 | 18.06 | 58.4 | 212.4 |
| S1 | ≈ w/o Embedding Retrieval (lexical Score | 23.4 | 7.41 | 29.32 | 26.67 | 16.13 | 57.4 | 211.4 |
| S2 | Full + GPU embedding Score | 24.8 | 10.37 | 30.14 | 27.83 | 18.06 | 58.4 | 212.2 |

### Paper reference (GPT-4o-mini Full)
`{'overall': 64.2, 'Multiple': 40.3, 'Single': 73.0, 'entity': 61.5, 'time': 70.8}`

## Table 2 — TimeQuestions
n=200

| Variant | Hits@1 | Explicit | Implicit | Temporal | Ordinal | Path@80 | sec |
|---------|--------|----------|----------|----------|---------|---------|-----|
| B0 | 3.5 | 3.45 | 5.26 | 1.59 | 6.45 | 0 | 0.0 |
| B1 | 21.0 | 10.34 | None | 50.79 | 3.23 | 55.5 | 0.3 |
| A1 | 23.0 | 4.6 | 5.26 | 61.9 | 6.45 | 59.5 | 91.9 |
| A2 | 23.0 | 6.9 | None | 61.9 | 3.23 | 57.0 | 5.5 |
| FULL | 23.0 | 6.9 | None | 61.9 | 3.23 | 57.0 | 0.3 |
| S1 | 19.5 | 8.05 | None | 49.21 | 3.23 | 56.0 | 0.5 |
| S2 | 23.0 | 6.9 | None | 61.9 | 3.23 | 57.0 | 0.3 |

### Paper reference (GPT-4o-mini)
`{'overall': 60.9, 'Explicit': 60.0, 'Implicit': 50.0, 'Temporal': 69.4, 'Ordinal': 52.8}`

## Table 3 — LLM backbones
```json
{
  "status": "skipped_no_api_key",
  "message": "Set OPENAI_API_KEY or DASHSCOPE_API_KEY to run Table1/3 LLM backbone experiments",
  "paper_table3_note": "IO vs MemoTime on Qwen3-4B/8B/32B/80B, DeepSeek-V3, GPT-4-Turbo"
}
```
