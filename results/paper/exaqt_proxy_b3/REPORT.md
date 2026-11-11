# EXAQT-proxy (B3) matched-protocol comparison

**Definition:** untrained EXAQT-inspired baseline  
- compact seed-centered subgraph (≤2 hops)  
- MiniLM fact–question relevance scoring  
- same seeds + Hits@1/PathHit extractor as FaithPath  
- **Not** trained GST / R-GCN EXAQT

## MultiTQ $n{=}500$ (`comparison_20261108_133958`)
| Variant | Hits@1 | Path@80 | vs FULL |
|---------|--------|---------|---------|
| B0 | 10.8 | 0.0 | −14.0 sig |
| B1 | 20.0 | 74.2 | −4.8 sig |
| B2 | **26.2** | 57.2 | +1.4 ns |
| **B3** | 22.2 | **76.8** | −2.6 ns |
| A1 | 23.4 | 56.6 | −1.4 ns |
| FULL | 24.8 | 58.4 | — |

## TimeQuestions $n{=}500$ (`comparison_20261108_135003`)
| Variant | Hits@1 | Path@80 | vs FULL |
|---------|--------|---------|---------|
| B0 | 4.6 | 0.0 | −20.8 sig |
| B1 | 25.0 | 58.6 | −0.4 ns |
| B2 | 24.0 | 61.6 | −1.4 ns |
| **B3** | 18.8 | 65.2 | **−6.6 sig** |
| FULL | **25.4** | 59.6 | — |

**Takeaway:** B3 recovers more evidence (PathHit) but underperforms FULL on Hits@1 under closed-form extraction; trained EXAQT remains unreproduced.
