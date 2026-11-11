# Response to Reviewers (KBS Major Revision)

Manuscript: `paper/FaithPath_IEEEtran.tex`  
Cover letter: `paper/COVER_LETTER_KBS.md`

## Associate Editor (综合)

| AE must-fix | Response | Location |
|-------------|----------|----------|
| ELDB first; FaithPath reference; not SOTA; TFC abstention; MemoTime substrate | Unified messaging in abstract, intro, contributions, experiments reader guide, conclusion; BiBFS/Score cites MemoTime | Abstract; §Intro; §Contributions; §Experiments opener; §Method; §Conclusion |
| $k_{\mathrm{ref}}$ sweep & not a constant | Fig.~\ref{fig:bucket_kref}, Table~\ref{tab:bucket_kref}; choosing-$k_{\mathrm{ref}}$ paragraph | §ELDB; §Error analysis |
| Proximity negative effect by type | Table~\ref{tab:proximity_breakdown}; B2/FULL discussion | §B2; Table~\ref{tab:diag} |
| Gold-qtype / gold-seeds limits; blind $n{=}200$ in body | Table~\ref{tab:blind_qtype}, §\ref{sec:blind_qtype}; §Discussion | §\ref{sec:blind_qtype}; §Discussion |
| Pseudocode & boundary cases to appendix | Alg. in Appendix~\ref{app:algo_main}; Table~\ref{tab:boundary_cases} | Appendix |
| ELDB migration / agent / datasets future work | §Discussion ``When ELDB does and does not apply''; Appendix~\ref{app:future} | §Discussion; Appendix |
| LLM appendix only | Appendix~\ref{app:llm_pilot} flagged non-core; one line in experiments | Appendix; §Experiments |
| Reproducibility + cover letter | §\ref{sec:data_availability}; `REPRODUCIBILITY.md`; `COVER_LETTER_KBS.md` | §Data availability |

---

## Reviewer #1 (Minor)

| Comment | Response | Location |
|---------|----------|----------|
| W1 External ELDB validation limited | Validated: FaithPath + MEMO\_R; not validated: trained systems; engineering steps listed | §Discussion export + ``When ELDB does and does not apply'' |
| W2 Gold-qtype; blind routing small | Table~\ref{tab:blind_qtype} in **main** ($n{=}200$) | §\ref{sec:blind_qtype} |
| W3 Oracle headroom easy to miss | Footnotes on Tables~\ref{tab:t1}, \ref{tab:scale}, \ref{tab:t4}; Table~\ref{tab:oracle_gap} | §Main results; §Ablation |
| W4 Memory write-back risk | F\_nomem + future multi-epoch ablation design | §Discussion; §Robustness |
| W5 LLM not closed | Appendix negative probe; future work (iii)(v) | Appendix~\ref{app:llm_pilot}; Appendix~\ref{app:future} |
| S1 ELDB scope for black-box agents | Explicit non-fit + instrumentation checklist | §Discussion |
| S2 Blind routing to body | Done | §\ref{sec:blind_qtype} |
| S3 Oracle on key tables | Done | Table footnotes |
| S4 Memory ablation plan | Paragraph ``Future ablation'' | §Discussion |
| S5 LLM in appendix | Unchanged | Appendix |

**Recommendation addressed:** Minor revision items incorporated.

---

## Reviewer #2 (Major)

| Comment | Response | Location |
|---------|----------|----------|
| W1 Contribution blur / MemoTime inheritance | Experiments reader guide; MemoTime §II-B; Module A text | §Experiments; §Related MemoTime; §Method |
| W2 Proximity mechanism by operator | Table~\ref{tab:proximity_breakdown}; Multiple/B2 full-test | §B2; Table~\ref{tab:scale} |
| W3 TFC needs downstream head | A3$=$A1; gates; LLM appendix negative | §TFC; Table~\ref{tab:t4}; Appendix |
| W4 Only MultiTQ/TQ | CronQuestions in future work | Appendix~\ref{app:future} (iii) |
| W5 Long pseudocode | Moved to Appendix~\ref{app:algo_main} | Appendix |
| S1–S5 | Same as rows above | — |

**Recommendation addressed:** Major framing and analysis revisions.

---

## Reviewer #3 (Minor)

| Comment | Response | Location |
|---------|----------|----------|
| W1 $k_{\mathrm{ref}}$ discussion thin | ``Choosing $k_{\mathrm{ref}}$'' + main table/figure | §ELDB; §Error analysis |
| W2 Synthetic seed noise | Stated in §Robustness; real linker future (iv) | §Robustness; Appendix~\ref{app:future} |
| W3 LLM agent trajectories | Future (v) in Appendix~\ref{app:future} | Appendix |
| W4 Boundary cases only in appendix | Table~\ref{tab:boundary_cases}; forward ref from §Method | Appendix; §Method |
| S1–S4 | As above | — |

**Recommendation addressed:** Minor items incorporated.

---

## Second-round major/minor checklist (M1–M6)

| ID | Comment | Response | Location |
|----|---------|----------|----------|
| **M1** | ELDB generality / external stacks | Applicability **checklist** (data contract); softened “plug-in” to “adapt given ranked paths”; FaithPath + MEMO\_R only validated | §Discussion checklist; §Contributions; §ELDB |
| **M2** | $k_{\mathrm{ref}}$, $\tilde{a}(p)$ comparability | Intro + contributions qualify **48.3%**; error analysis labels protocol-specific statistic | §Intro; §Contributions; §Error analysis; Conclusion |
| **M3** | B2/B3 proxy misread as EXAQT | **Bold** proxy disclaimer; table captions/rows say *untrained EXAQT-style proxy* | §Baselines; Table~\ref{tab:peers} |
| **M4** | Global vs conditional Hits@1 | §Reliability defines both metrics; Table~\ref{tab:reliability_gates} caption; 44.4% = conditional only | §\ref{sec:reliability}; Conclusion |
| **M5** | SN$\eta$ realism | Synthetic stress-test upper bound; real linker future work | §Robustness; Appendix~\ref{app:future} (iv) |
| **M6** | Prefix under-powered ablations | Banner in §Ablation; full-test primary for EGOR CI | §\ref{sec:ablation}; §Main results power note |
| m2 | Fig. PathHit@$k$, bucket $k{=}80$ | Caption stresses $|P|$; `plot_bucket_kref.py` marks $k_{\mathrm{ref}}{=}80$ | Fig.~\ref{fig:pathhit_k}; `plot_bucket_kref.py` |
| m3 | MemoTime RW length | Compressed §MemoTime | §Related MemoTime |
| m4 | Artifact→table map | Expanded §Data availability sentence | §\ref{sec:data_availability} |
| m5 | ICEWS / gold seeds limits | Limitations paragraph in §Discussion | §Discussion limitations |
| Typo | Rank-1 gold but wrong | Table~\ref{tab:oracle_gap} caption | §Error analysis |
| m1 | $\ind$ symbol | Single `\mathbbm{1}` via `bbm` package | Preamble |

**Note:** Abstract left unchanged per author instruction (“摘要不动”).

---

## Artifacts (reproducibility)

- `bucket_kref_sweep_n500.json`, `proximity_breakdown_n500.json`
- `egor_unlabeled_pilot_n200.json`
- `paper/plot_bucket_kref.py`, `paper/analyze_proximity_breakdown.py`
- Index: Table~\ref{tab:artifacts}

## Overleaf

See `paper/OVERLEAF.md` (upload `figures/` including `fig_bucket_kref.pdf`).
