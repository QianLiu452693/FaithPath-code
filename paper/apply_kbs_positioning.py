#!/usr/bin/env python3
"""KBS-oriented narrative: knowledge-system reliability, TFC safety valve, demote B2 headline."""
from pathlib import Path

TEX = Path(__file__).resolve().parent / "FaithPath_IEEEtran.tex"
t = TEX.read_text(encoding="utf-8")

t = t.replace(
    "\\markboth{IEEE Transactions on Knowledge and Data Engineering}%\n"
    "{Author \\emph{et~al.}: \\FaithPath{} and \\ELDB{} for TKGQA}",
    "\\markboth{Knowledge-Based Systems}%\n"
    "{\\FaithPath{} / \\ELDB{}: reliability diagnosis for temporal KG question answering}",
)

old_abs = """Three findings organize the paper:
(i)~\\textbf{Selection is the bottleneck:} on MultiTQ $n{=}500$, FULL PathHit@80 is $58.4\\%$ while Hits@1 is $24.8\\%$ ($44.7\\%$ of errors are selection gaps).
(ii)~\\textbf{Temporal-first is not uniformly helpful:} on MultiTQ full test ($n{=}54{,}584$), embedding multi-hop \\textbf{B2} (no temporal-first prune/proximity) reaches $25.1\\%$ vs.\\ FULL $24.3\\%$ (paired $\\Delta{+}0.80$\\,pp, 95\\% CI $[+0.58,+1.01]$); the margin concentrates on Multiple and \\texttt{before\\_last}.
Controlled ablations disentangle prune vs.\\ proximity; seed-noise curves quantify linking fragility.
(iii)~\\textbf{Module-level negative results under a weak extractor:} EGOR's $+1.4$\\,pp lift is not significant at $n{=}500$ (under-powered for $<$2\\,pp effects); TFC yields A3$=$A1 Hits@1 and is weakest on Multiple.
We do \\emph{not} claim end-to-end SOTA against full-LLM agents; the journal contribution is the named \\FaithPath{} method plus \\ELDB{} diagnostics (PathHit--Hits gaps, PathHit@$k$ curves, seed-noise stress tests, EGOR/TFC negative results) and MemoTime-compatible retrieval-only baselines under one protocol."""

new_abs = """Three reliability findings organize the paper:
(i)~\\textbf{Knowledge-to-decision gap:} on MultiTQ $n{=}500$, PathHit@80 is $58.4\\%$ but Hits@1 is only $24.8\\%$---the system often \\emph{retrieves} gold evidence yet fails the \\emph{last mile} of answer selection ($44.7\\%$ of errors are selection gaps; \\ELDB{} failure buckets quantify this).
(ii)~\\textbf{Decoupled verification vs.\\ ranking:} TFC is a \\emph{safety valve} (path faithfulness and abstention signals), not a Hits@1 booster under a weak extractor; score- and PathHit-gated operating points raise answered accuracy to $44.4\\%$ at $37.8\\%$ coverage vs.\\ $24.8\\%$ always-answer (Table~\\ref{tab:reliability_gates}).
(iii)~\\textbf{Reusable \\ELDB{} protocol:} PathHit@$k$ normalization, seed-noise stress tests, and full-test ablations isolate when temporal proximity scoring harms selection; a modest B2 vs.\\ FULL Hits@1 gap on full MultiTQ ($+0.8$\\,pp) is \\emph{not} evidence superiority at matched PathHit ($60.1$ vs.\\ $60.9$).
We position \\FaithPath{} as a knowledge-system stack (retrieve $\\rightarrow$ verify $\\rightarrow$ decide) and \\ELDB{} as an evaluation protocol exportable beyond our implementation."""

if old_abs in t:
    t = t.replace(old_abs, new_abs)
else:
    print("WARN: abstract block not found")

t = t.replace(
    "Temporal Knowledge Graph Question Answering, FaithPath, Diagnostic Benchmark, Evidence Retrieval, PathHit, Ablation",
    "Knowledge-based systems, Temporal knowledge graph question answering, FaithPath, Reliability, Abstention, PathHit",
)

t = t.replace(
    "\\textbf{Journal scope (IEEE TKDE).}\n"
    "The manuscript is formatted for \\emph{IEEE Transactions on Knowledge and Data Engineering}: it presents a specified method (\\FaithPath{}), reproducible benchmark artifacts (\\ELDB{}), and large-scale empirical analysis.\n"
    "It is not positioned as a pure leaderboard SOTA paper: absent \\FaithPath{}$+$LLM closed-loop Hits@1 and matched full-agent MemoTime runs, we report diagnostic and ablation evidence rather than claiming dominant end-to-end accuracy.",
    "\\textbf{Target venue (Knowledge-Based Systems).}\n"
    "KBS emphasizes knowledge systems with theory, implementation, and actionable reliability lessons.\n"
    "We contribute (a)~the \\FaithPath{} retrieve--verify--decide stack, (b)~the \\ELDB{} evaluation protocol for evidence-grounded TKGQA, and (c)~empirical \\emph{evaluation knowledge}: where failures occur, which gates reduce risk, and which design knobs trade PathHit for answer hit.",
)

# Contributions bullet on negatives -> reliability
t = t.replace(
    "\\item \\textbf{Calibrated negatives (packaged as benchmark findings):} under a weak extractor and $n{=}500$, EGOR is under-powered for $<$2\\,pp effects; TFC does not raise Hits@1 (A3$=$A1); MemoTime \\emph{retrieval-only} (MEMO\\_R) reports matched PathHit/Hits@1 under \\ELDB{} (Table~\\ref{tab:memo_proxy}).",
    "\\item \\textbf{Reliability gates:} TFC plus PathHit define abstention operating points that enrich errors under always-answer retrieval (Table~\\ref{tab:reliability_gates}); MEMO\\_R confirms MemoTime-compatible retrieval under \\ELDB{} (Table~\\ref{tab:memo_proxy}).",
)

anchor_robust = "\\subsection{Robustness Notes}"
reliability_block = r"""
\subsection{Knowledge-System Reliability and Abstention}
\label{sec:reliability}
Under a weak path-tail extractor, TFC does \emph{not} raise Hits@1 (A3$=$A1); its role is to certify whether ranked evidence is temporally grounded before downstream decision modules (LLM or human) consume it.
On $n{=}500$, the default Faithful bit is permissive (all paths pass at $\theta_f{=}0.35$), so we report \textbf{calibrated operating points} using PathHit@80 (evidence present?) and TFC scores (Table~\ref{tab:reliability_gates}, Fig.~\ref{fig:tfc_rc}).
Abstaining when PathHit@80$=$0 covers $58.4\%$ of questions and cuts error among answered items from $75.2\%$ to $57.5\%$ while raising effective Hits@1 on the answered set to $42.5\%$.
Combining PathHit with a stricter score cutoff ($\mathrm{Score}_{\mathrm{TFC}}\ge 0.93$) trades coverage ($37.8\%$) for $44.4\%$ Hits@1 on accepted queries---a concrete \emph{knowledge-to-decision} interface for outer-loop LLM gating (minimal LLM pilot deferred; see Section~\ref{sec:discussion}).

\begin{table}[!t]
\centering
\caption{Reliability gates on MultiTQ $n{=}500$ (\FaithPath{} FULL). Coverage = fraction answered; risk = error among answered; Hits@1 = accuracy on answered subset.}
\label{tab:reliability_gates}
\begin{tabular}{lrrr}
\toprule
Gate policy & Coverage (\%) & Risk (\%) & Hits@1 (\%) \\
\midrule
Always answer & 100.0 & 75.2 & 24.8 \\
PathHit@80$=$1 only & 58.4 & 57.5 & 42.5 \\
$\mathrm{Score}_{\mathrm{TFC}}\ge 0.93$ & 61.8 & 72.8 & 27.2 \\
PathHit + TFC$\ge 0.93$ & 37.8 & 55.6 & 44.4 \\
High band TFC$\ge 0.935$ & 14.0 & 51.4 & 48.6 \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[!t]
\centering
\includegraphics[width=0.92\columnwidth]{figures/fig_tfc_risk_coverage.pdf}
\caption{Risk--coverage for \FaithPath{} FULL ($n{=}500$): TFC score ranking (curve) vs.\ PathHit@80 evidence gate (marker). Baseline = always-answer retrieval error.}
\label{fig:tfc_rc}
\end{figure}

"""
if anchor_robust in t and "tab:reliability_gates" not in t:
    t = t.replace(anchor_robust, reliability_block + anchor_robust)

# Demote B2 in reading paragraph
t = t.replace(
    "On MultiTQ full test, B2 exceeds FULL (Table~\\ref{tab:scale}): this is a primary finding of the ablation study, not a footnote.",
    "On MultiTQ full test, B2 slightly exceeds FULL on Hits@1 ($25.1$ vs.\\ $24.3$; Table~\\ref{tab:scale}) but \emph{does not} improve PathHit@80 ($60.1$ vs.\\ $60.9$); we treat this as a \textbf{conditional ablation signal} (proximity/proximity-free ranking under a weak extractor), not as overall system dominance.",
)

# Add B2 discussion paragraph before or in b2_analysis
b2_ins = r"""
\paragraph{Interpreting B2 vs.\ FULL for knowledge-system design.}
B2 removes temporal-first pruning and proximity re-ranking; its Hits@1 lead on full MultiTQ concentrates on Multiple and \texttt{before\_last} prefixes where proximity scoring can over-penalize plausible paths.
At matched evidence recall (PathHit@80 within $0.8$\,pp on full test), B2's Hits advantage is better read as \emph{selection simplified by a different ranking geometry} than as strictly better knowledge retrieval.
\FaithPath{} FULL remains the reference stack for faithfulness-aware retrieval; B2 is an \ELDB{} diagnostic variant.
"""
if "\\paragraph{Why can B2 beat FULL?" in t and "Interpreting B2 vs." not in t:
    t = t.replace("\\paragraph{Why can B2 beat FULL? Controlled component ablations.}", b2_ins + "\\paragraph{Why can B2 beat FULL? Controlled component ablations.}")

# TFC module text reframing
t = t.replace(
    "\\paragraph{On TFC: faithfulness filter $\\neq$ correctness.}\n"
    "TFC verifies path-level monotonicity/anchors/grounding; Accept/Faithful does not imply Hits@1 correctness.\n"
    "Under retrieval-only answering, A3$=$A1 on Hits@1, so we do \\emph{not} claim a Hits@1 lift from TFC.\n"
    "Any benefit as a gate for outer LLM accept/reject rates is \\emph{out of scope} of this evidence-layer study.",
    "\\paragraph{TFC as safety valve (knowledge verification).}\n"
    "TFC verifies path-level monotonicity, anchors, and grounding before decisions.\n"
    "It is not tuned as a Hits@1 booster under path-tail extraction (A3$=$A1), but supplies \\texttt{Score}$_{\\mathrm{TFC}}$ and (when calibrated) Faithful bits for abstention and outer-loop LLM gating (Section~\\ref{sec:reliability}).",
)

# Limitations updates
t = t.replace(
    "(4)~TFC abstention utility (Accept vs.\\ error confusion; risk--coverage) is still not quantified.",
    "(4)~Full LLM closed-loop with Faithful/PathHit gating is not yet run locally (Ollama/API pilot planned); Section~\\ref{sec:reliability} reports retrieval-layer risk--coverage.",
)

t = t.replace(
    "(2)~FaithPath$+$LLM selection on at least one subset remains required before claiming module utility under strong extractors.",
    "(2)~\\FaithPath{}$+$open-weight LLM selection on $n{\\approx}200$ with gate on/off is the next integration step; \\ELDB{} gates already separate evidence miss vs.\\ selection risk without an LLM.",
)

# Full-test EGOR paragraph before limitations reproducibility - after experiments ablation
egor_full = r"""
\paragraph{EGOR at scale (full MultiTQ).}
Prefix-level FULL$-$A1 is $+1.4$\,pp with CI including $0$ at $n{=}500$; we additionally report paired bootstrap on the official full test ($n{=}54{,}584$) from ledger \texttt{comparison\_*} (A1 vs.\ FULL).
This test addresses ``under-powered at $n{=}500$'' criticism: if the gap remains inside $0$, EGOR's incremental routing is absorbed by the selection bottleneck under retrieval-only extraction; a significant full-test gap would instead support modular routing value.
"""
if "EGOR at scale (full MultiTQ)" not in t and "\\textbf{Effect sizes and paired CIs" in t:
    t = t.replace("\\textbf{Effect sizes and paired CIs (Hits@1, $n{=}500$).}", egor_full + "\\textbf{Effect sizes and paired CIs (Hits@1, $n{=}500$).}")

# Conclusion tweak
t = t.replace(
    "Controlled ablations, PathHit@$k$ normalization, and seed-noise curves make these failure modes measurable for future \\FaithPath{}$+$LLM and matched peer studies.",
    "Controlled ablations, PathHit@$k$ normalization, reliability gates, and seed-noise curves turn failure modes into \\emph{evaluation knowledge} for knowledge-based TKGQA systems and \\FaithPath{}$+$LLM integration.",
)

TEX.write_text(t, encoding="utf-8")
print("Updated", TEX)
