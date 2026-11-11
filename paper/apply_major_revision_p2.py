#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "FaithPath_IEEEtran.tex"


def repl(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"MISSING: {label}\n---\n{old[:200]}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")

    text = repl(
        text,
        r"""\paragraph{Evaluation protocol (important).}
This paper is an \emph{evidence-layer retrieval ablation study}.
Unless noted, all FaithPath numbers are \emph{retrieval-grounded}: answers are extracted from ranked monotone paths by Modules~A--C \textbf{without} LLM answer synthesis.
We separately report \textbf{PathHit@80} (gold appears on a top-$80$ path: evidence recall) and \textbf{Hits@1} (extracted answer matches gold).
Path-level TFC Accept/Faithful does \emph{not} equal answer correctness.
Literature Full-train / Full-LLM rows (including MemoTime-style agents) are contextual only and are \textbf{not} comparable to our retrieval-only results.
We report full-test MultiTQ / TimeQuestions sweeps under the same retrieval-grounded protocol; FaithPath$+$LLM closed-loop Hits@1 is \emph{not} claimed.""",
        r"""\paragraph{Evaluation protocol (important).}
This paper is an \emph{evidence-layer retrieval ablation and measurement study}.
Unless noted, all FaithPath numbers are \emph{retrieval-grounded}: answers are extracted from ranked monotone paths by a weak closed-form extractor (path tail / end time; Eq.~\eqref{eq:extract}) \textbf{without} LLM answer synthesis.
We separately report \textbf{PathHit@80} (evidence recall) and \textbf{Hits@1} (extractor answer hit).
Path-level TFC Accept/Faithful does \emph{not} equal answer correctness.
\textbf{Extractor confound.}
The PathHit--Hits@1 gap implies selection headroom; the same weak extractor may also attenuate module-level Hits@1 effects (e.g., EGOR), so ``not significant under retrieval-only extraction'' must not be read as ``module is useless under a stronger selector.''
FaithPath$+$LLM closed-loop evaluation is a required follow-up, not claimed here.
Literature Full-train / Full-LLM numbers are cited only in a separate contextual table and are \textbf{not} comparable to our retrieval-only rows.""",
        "protocol",
    )

    # Split MultiTQ table into lit + retrieval
    old_t1 = r"""\begin{table*}[!t]
\centering
\caption{Performance comparison on MultiTQ (Hits@1, \%).
\textbf{Setting} separates Full-train/Full-LLM literature from Retrieval-only FaithPath ($n{=}500$).
PathHit@80 of FaithPath FULL is $58.4\%$.}
\label{tab:t1}
\begin{tabular}{llccccc}
\toprule
\textbf{Model} & \textbf{Setting} & \textbf{Overall} & \textbf{Mult.} & \textbf{Single} & \textbf{Ent.} & \textbf{Time} \\
\midrule
BERT~\cite{devlin2019bert} & Full train & 8.3 & 6.1 & 9.2 & 10.1 & 4.0 \\
ALBERT~\cite{lan2019albert} & Full train & 10.8 & 8.6 & 11.6 & 13.9 & 3.2 \\
EmbedKGQA & Full train & 20.6 & 13.4 & 23.5 & 29.0 & 0.1 \\
CronKGQA~\cite{saxena2021cronkgqa} & Full train & 27.9 & 13.4 & 33.7 & 32.8 & 15.6 \\
MultiQA~\cite{chen2023multitq} & Full train & 29.3 & 15.9 & 34.7 & 34.9 & 15.7 \\
ChatGPT & Full LLM & 10.2 & 7.7 & 14.7 & 13.7 & 2.0 \\
KG-RAG~\cite{chen2024ari} & Full LLM & 18.5 & 16.0 & 20.0 & 23.0 & 7.0 \\
ReAct KB~\cite{chen2024ari} & Full LLM & 21.0 & 13.6 & 63.5 & 31.3 & 30.0 \\
ARI~\cite{chen2024ari} & Full LLM & 38.0 & 68.0 & 21.0 & 39.4 & 34.4 \\
TempAgent~\cite{hu2025tempagent} & Full LLM & 53.9 & 16.8 & 68.4 & 47.8 & 66.1 \\
\midrule
CandidatePrior (B0) & Retrieval-only & 10.8 & 5.2 & 12.9 & 15.7 & 0.0 \\
OneHopLexical (B1) & Retrieval-only & 20.0 & 11.1 & 23.3 & 24.9 & 9.0 \\
BiBFS only (A1) & Retrieval-only & 23.4 & \underline{16.3} & 26.0 & 25.5 & \underline{18.7} \\
\textbf{FaithPath (FULL)} & Retrieval-only & \underline{24.8} & 10.4 & \underline{30.1} & \underline{27.8} & 18.1 \\
\bottomrule
\end{tabular}
\end{table*}

Literature Full-train/Full-LLM rows are contextual only.
Under our retrieval-grounded prefix protocol, \textbf{FaithPath FULL achieves 24.8\%} Hits@1 ($+14.0$ vs.\ weak prior B0, $+4.8$ vs.\ B1) with PathHit@80 $=58.4\%$.
These primary deltas are relative to weak priors B0/B1 only, not EXAQT, B2, or MemoTime agents (see Table~\ref{tab:scale} for B2).
Bootstrap 95\% CIs on the $n{=}500$ prefix: Hits@1 $[20.8,28.6]$; paired FULL$-$B0 and FULL$-$B1 exclude $0$; paired FULL$-$A1 (EGOR) includes $0$.
Fig.~\ref{fig:hits_variants}--\ref{fig:hits_vs_pathhit} separate Hits@1 (answer hit) from PathHit@80 (evidence recall)."""

    new_t1 = r"""\begin{table}[!t]
\centering
\caption{Contextual MultiTQ literature numbers (Hits@1, \%) under published Full-train/Full-LLM protocols.
\textbf{Not comparable} to our retrieval-only tables.}
\label{tab:lit_mt}
\begin{tabular}{lccccc}
\toprule
\textbf{Model} & \textbf{Overall} & \textbf{Mult.} & \textbf{Single} & \textbf{Ent.} & \textbf{Time} \\
\midrule
BERT~\cite{devlin2019bert} & 8.3 & 6.1 & 9.2 & 10.1 & 4.0 \\
CronKGQA~\cite{saxena2021cronkgqa} & 27.9 & 13.4 & 33.7 & 32.8 & 15.6 \\
MultiQA~\cite{chen2023multitq} & 29.3 & 15.9 & 34.7 & 34.9 & 15.7 \\
ARI~\cite{chen2024ari} & 38.0 & 68.0 & 21.0 & 39.4 & 34.4 \\
TempAgent~\cite{hu2025tempagent} & 53.9 & 16.8 & 68.4 & 47.8 & 66.1 \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[!t]
\centering
\caption{Retrieval-only MultiTQ prefix ($n{=}500$, Hits@1, \%).
PathHit@80 of FULL is $58.4\%$.
Lifts vs.\ B0/B1 are not claims vs.\ B2 or Full-LLM agents.}
\label{tab:t1}
\begin{tabular}{lcccc}
\toprule
\textbf{Variant} & \textbf{Overall} & \textbf{Mult.} & \textbf{Single} & \textbf{Ent.} / Time \\
\midrule
B0 CandidatePrior & 10.8 & 5.2 & 12.9 & 15.7 / 0.0 \\
B1 OneHopLexical & 20.0 & 11.1 & 23.3 & 24.9 / 9.0 \\
A1 BiBFS only & 23.4 & \underline{16.3} & 26.0 & 25.5 / \underline{18.7} \\
\textbf{FULL} & \underline{24.8} & 10.4 & \underline{30.1} & \underline{27.8} / 18.1 \\
\bottomrule
\end{tabular}
\end{table}

Under the retrieval-grounded prefix protocol, FULL reaches $24.8\%$ Hits@1 vs.\ weak priors B0/B1 (paired FULL$-$B0 $\Delta{+}14.0$\,pp, 95\% CI $[+9.8,+18.2]$; FULL$-$B1 $\Delta{+}4.8$\,pp, CI $[-8.6,-0.8]$ for B1$-$FULL, i.e., FULL above B1).
Marginal FULL Hits@1 CI on $n{=}500$: $[20.8,28.6]$.
Paired FULL$-$A1 (EGOR effect) $\Delta{+}1.4$\,pp, 95\% CI $[-0.6,+3.6]$ \emph{includes $0$}.
\textbf{Power note:} at $n{=}500$, a $\sim$1.4\,pp paired effect is under-powered (rough SE $\approx$2--3\,pp); ``not significant'' $\neq$ ``proven null.''
Fig.~\ref{fig:hits_variants}--\ref{fig:hits_vs_pathhit} separate Hits@1 from PathHit@80.
Stronger peer comparisons are deferred to Tables~\ref{tab:scale}--\ref{tab:peers}."""
    text = repl(text, old_t1, new_t1, "split_t1")

    text = repl(
        text,
        r"""\caption{Full-test / large retrieval-only sweeps (Hits@1 / PathHit@80, \%).
B2$=$embedding multi-hop without temporal-first pruning.
MultiTQ \emph{full} $n{=}54{,}584$: B2 \emph{significantly} exceeds FULL (paired $\Delta{+}0.80$\,pp, 95\% CI $[+0.58,+1.01]$).
TimeQuestions \emph{full} $n{=}3237$: B1/B2/FULL tied (paired CIs vs.\ FULL include $0$).}
\label{tab:scale}""",
        r"""\caption{Full-test retrieval-only sweeps (Hits@1 / PathHit@80, \%; $n_{\mathrm{MT}}{=}54{,}584$, $n_{\mathrm{TQ}}{=}3237$).
B2$=$embedding multi-hop without temporal-first prune/proximity.
MultiTQ: paired B2$-$FULL $\Delta{+}0.80$\,pp, 95\% CI $[+0.58,+1.01]$ (excludes $0$; $n_{\mathrm{boot}}{=}2000$).
TQ: B1/B2/FULL tied (paired CIs vs.\ FULL include $0$).}
\label{tab:scale}""",
        "tab_scale_cap",
    )

    text = repl(
        text,
        r"""\caption{Finding: on MultiTQ full test ($n{=}54{,}584$), B2 EmbedMHOP exceeds FULL Hits@1; on full TimeQuestions, B1/B2/FULL are near-tied.
Bars use color plus hatch for colorblind-safe encoding.}
\label{fig:scale_hits}""",
        r"""\caption{Full-test Hits@1 ($n_{\mathrm{MT}}{=}54{,}584$, $n_{\mathrm{TQ}}{=}3237$).
B2 exceeds FULL on MultiTQ; B1/B2/FULL near-tied on TimeQuestions.
Color plus hatch encoding.}
\label{fig:scale_hits}""",
        "fig9_cap",
    )

    # Insert B2 analysis after reading peer paragraph
    old_peer = r"""\paragraph{Reading peer and full-test results.}
Under retrieval-only extraction, B2 can exceed FULL Hits@1 (esp.\ MultiTQ full test, Table~\ref{tab:scale}), and B3 shows that high PathHit (evidence recall) need not yield best Hits@1 (Table~\ref{tab:peers}).
FULL still significantly beats weak priors B0/B1 and beats the EXAQT-proxy on Hits@1 under our extractor.
FaithPath's distinctive value is therefore (i)~monotone evidence with PathHit diagnostics, (ii)~structured EGOR control without LLM toolkit calls, and (iii)~TFC as a faithfulness \emph{filter}, not an automatic Hits@1 booster.
FaithPath$+$LLM and \emph{trained} EXAQT re-runs remain out of scope / unmatched."""

    new_peer = r"""\paragraph{Reading peer and full-test results.}
On MultiTQ full test, B2 exceeds FULL (Table~\ref{tab:scale}): this is a primary finding of the ablation study, not a footnote.
B3 further shows PathHit $\neq$ Hits@1 (Table~\ref{tab:peers}).
FULL still beats weak priors B0/B1 under the same extractor; EGOR/TFC should not be marketed as independent Hits@1 modules here.
FaithPath$+$LLM selection and \emph{trained} EXAQT / RTQA retrieval re-runs remain unmatched follow-ups.

\paragraph{Why can B2 beat FULL on MultiTQ full test?}
\label{sec:b2_analysis}
B2 disables temporal-first beam pruning and the proximity term while keeping embedding multi-hop retrieval ($D_{\max}{=}2$).
Typed Hits@1 on the full MultiTQ test localize the gap:
Multiple $13.2\%$ (B2) vs.\ $10.0\%$ (FULL);
\texttt{before\_last} $11.1\%$ vs.\ $4.7\%$;
Single nearly tied ($29.9\%$ vs.\ $30.1\%$);
\texttt{before\_after}/\texttt{equal} are close or favor FULL slightly.
A plausible mechanism is that temporal-first pruning and proximity bias discard gold neighbors on long-tail / multi-constraint items (especially Multiple and \texttt{before\_last}), while pure embedding ranking retains them.
Latency reinforces the point: on the same full MultiTQ sweep, B2 wall time is $\approx$0.022\,s/q vs.\ FULL $\approx$0.50\,s/q (BiBFS$+$Score dominate).
Thus, under retrieval-only Hits@1, monotone temporal-first retrieval is \emph{not} uniformly beneficial; diagnosing prune/proximity false negatives is the central open scientific question raised by Table~\ref{tab:scale}.

\paragraph{PathHit@80 caveat.}
B1 PathHit@80 ($74.2\%$ on $n{=}500$) exceeds FULL ($58.4\%$) partly because one-hop neighbor sets are larger; comparing PathHit@$k$ at fixed $k{=}80$ across unequal candidate generators is imperfect.
We therefore treat PathHit as a diagnostic of evidence presence under each method's own top-$80$ list, not as a size-matched recall curve (PathHit@$k$ sweeps are deferred)."""
    text = repl(text, old_peer, new_peer, "b2_analysis")

    # Efficiency: add B2
    text = repl(
        text,
        r"""\paragraph{Efficiency.}
FULL on MultiTQ ($n{=}500$) takes $\sim$211\,s wall ($\approx$0.42\,s/q); peak MiniLM memory $\approx$0.28\,GB.
Approximate per-question split: EGOR/TFC $<5$\,ms; MiniLM $\sim$50--80\,ms; BiBFS $\sim$300--350\,ms.
Fig.~\ref{fig:runtime} compares wall-clock latency (log scale): BiBFS dominates; $D_{\max}{=}1$ (H1) is substantially cheaper.""",
        r"""\paragraph{Efficiency.}
FULL on MultiTQ ($n{=}500$) takes $\sim$211\,s wall ($\approx$0.42\,s/q); peak MiniLM memory $\approx$0.28\,GB.
Approximate per-question split: EGOR/TFC $<5$\,ms; MiniLM $\sim$50--80\,ms; BiBFS $\sim$300--350\,ms.
On MultiTQ \emph{full} test, B2 is far cheaper than FULL ($\approx$0.022 vs.\ $\approx$0.50\,s/q) while attaining higher Hits@1: efficiency does not favor FULL under this protocol.
Fig.~\ref{fig:runtime} compares wall-clock latency on the $n{=}500$ ledger (log scale): BiBFS dominates; $D_{\max}{=}1$ (H1) is substantially cheaper.""",
        "efficiency",
    )

    # Error analysis / TFC abstention note
    text = repl(
        text,
        r"""\textbf{Mechanism boundary.}
TFC predicates $C_2$/$C_3$ check end-time vs.\ anchors and granularity on a \emph{single} path; they do \emph{not} fully encode cross-entity temporal alignment across parallel branches.
Hard Multiple cases therefore expose a PathHit--Hits@1 selection gap that retrieval-only path-tail extraction cannot close without an outer multi-constraint selector (e.g., LLM).""",
        r"""\textbf{Mechanism boundary.}
TFC predicates $C_2$/$C_3$ check end-time vs.\ anchors and granularity on a \emph{single} path; they do \emph{not} fully encode cross-entity temporal alignment across parallel branches.
Hard Multiple / \texttt{before\_last}/\texttt{after\_first} cases therefore expose both a selection gap and a TFC coverage gap: the faithfulness filter is weakest precisely where faithfulness is most needed.
\textbf{Abstention evaluation (missing).}
If TFC's value is primarily as an abstention gate, one must report Faithful$=$0 precision/recall or risk--coverage curves against Hits@1 errors.
We do not yet provide Accept/Hits@1 confusion matrices or EGOR type-accuracy breakdowns; these analyses are required before claiming filter utility beyond the A3$=$A1 Hits@1 result.""",
        "tfc_abstention",
    )

    # Discussion limitations rewrite
    old_disc_lim = r"""\paragraph{Limitations.}
(1)~Full-test retrieval sweeps are reported for MultiTQ ($n{=}54{,}584$) and TimeQuestions ($n{=}3237$); typed ablations remain on prefixes $n{=}500/200$.
(2)~This paper intentionally evaluates the \emph{evidence layer only}; FaithPath$+$LLM end-to-end QA is out of scope.
(3)~Trained EXAQT is not re-run; we instead report an untrained EXAQT-proxy (B3) under our protocol. B2 EmbedMHOP exceeds FULL Hits@1 on MultiTQ full test.
(4)~Seeds assume candidate lists; entity-linking noise is a first-order risk (Section~\ref{sec:robust}).
(5)~EGOR dictionaries and thresholds are dataset-specific; independent EGOR Hits@1 gain is not significant on the $n{=}500$ prefix.
(6)~TFC does not raise retrieval-only Hits@1.
(7)~ICEWS geopolitical bias; high-stakes use needs human oversight.
Optional future work: trained EXAQT re-run, noise/$\theta_r$ studies."""

    new_disc_lim = r"""\paragraph{Limitations (aligned with review priorities).}
(1)~Contribution mismatch risk: EGOR/TFC are formalized modules, but under retrieval-only Hits@1 they lack significant independent accuracy gains; the paper must be read as ablation/measurement.
(2)~Weak extractor may confound module comparisons; FaithPath$+$LLM selection on at least one subset is required follow-up.
(3)~B2 $>$ FULL on MultiTQ full test is explained only via typed aggregates; controlled prune/proximity ablations and PathHit@$k$ curves remain incomplete.
(4)~TFC abstention utility (Accept vs.\ error confusion; risk--coverage) is not quantified.
(5)~EGOR type-prediction accuracy and conditional Hits@1 on correct-$\tau$ subsets are not reported.
(6)~Seed-noise injection ($\eta\in\{0.1,0.2,0.3\}$) remains deferred despite being first-order.
(7)~RTQA/Temp-R1 retrieval components and trained EXAQT are not re-run under our protocol.
(8)~ICEWS bias; high-stakes use needs oversight."""
    text = repl(text, old_disc_lim, new_disc_lim, "discussion_lim")

    old_conc = r"""\section{Conclusion}
\label{sec:conclusion}

We presented \textbf{FaithPath} as an \emph{evidence-layer} retrieval--critique stack (adaptive-$\Dpred$ BiBFS, LLM-optional EGOR, path-level TFC filter) for TKGQA.
Under a retrieval-grounded protocol with no end-to-end LLM synthesis (by design), FULL improves over weak priors B0/B1 on both full tests, while on MultiTQ full test the embedding multi-hop peer B2 significantly exceeds FULL Hits@1; on full TimeQuestions, B1/B2/FULL are tied.
Ablations show BiBFS as the main internal driver vs.\ one-hop; EGOR and TFC do not deliver significant independent Hits@1 gains under retrieval-only extraction.
We recommend framing subsequent claims around evidence recall, faithfulness filtering, and modular plug-in use, rather than end-to-end TKGQA SOTA."""

    new_conc = r"""\section{Conclusion}
\label{sec:conclusion}

We presented \textbf{FaithPath} as an evidence-layer \emph{ablation and measurement} stack for TKGQA retrieval (Adaptive-$\Dpred$ BiBFS, EGOR, TFC).
Under a retrieval-grounded weak-extractor protocol, BiBFS drives gains vs.\ weak one-hop priors, while EGOR and TFC do not deliver significant independent Hits@1 gains.
On MultiTQ full test, B2 exceeds FULL (paired CI $[+0.58,+1.01]$), with the margin concentrated on Multiple and \texttt{before\_last}---showing that temporal-first retrieval is not uniformly best and that weak-prior comparisons alone are insufficient.
We recommend reading this work as a modular negative-result / measurement paper adjacent to MemoTime-style agents, and treating FaithPath$+$LLM selection, TFC abstention curves, and prune-error analyses as the next required experiments---not as optional extras."""
    text = repl(text, old_conc, new_conc, "conclusion")

    # FAQ soften
    text = repl(
        text,
        r"""\paragraph{Is FaithPath only a search heuristic?}
No. It integrates Adaptive-$\Dpred$ BiBFS, structured EGOR, and TFC into one new algorithm with closed-form objectives.""",
        r"""\paragraph{Is FaithPath a new SOTA algorithm?}
No. It is a closed-form, ablatable evidence-layer stack for measurement; EGOR/TFC are not independent Hits@1 winners under our protocol.""",
        "faq",
    )

    # Bib status
    text = repl(
        text,
        r"""\bibitem{tan2025memotime}
X.~Tan, X.~Wang, Q.~Liu, X.~Xu, X.~Yuan, L.~Zhu, and W.~Zhang, ``MemoTime: Memory-augmented temporal knowledge graph enhanced large language model reasoning,'' in \emph{Proc.\ ACM Web Conf.\ (WWW)}, 2026, arXiv:2510.13614.""",
        r"""\bibitem{tan2025memotime}
X.~Tan, X.~Wang, Q.~Liu, X.~Xu, X.~Yuan, L.~Zhu, and W.~Zhang, ``MemoTime: Memory-augmented temporal knowledge graph enhanced large language model reasoning,'' arXiv:2510.13614, 2025, preprint.""",
        "bib_memo",
    )
    text = repl(
        text,
        r"""\bibitem{gong2026tempr1}
Z.~Gong, Z.~Liu, S.~Li, \emph{et~al.}, ``Temp-R1: A unified autonomous agent for complex temporal KGQA via reverse curriculum reinforcement learning,'' in \emph{ACL}, 2026, arXiv:2601.18296.""",
        r"""\bibitem{gong2026tempr1}
Z.~Gong, Z.~Liu, S.~Li, \emph{et~al.}, ``Temp-R1: A unified autonomous agent for complex temporal KGQA via reverse curriculum reinforcement learning,'' arXiv:2601.18296, 2026, preprint.""",
        "bib_tempr1",
    )

    # Robustness: acknowledge deferred seed noise more strongly
    text = repl(
        text,
        r"""Controlled noise injection experiments to quantify performance degradation under real-world entity-linking errors are left for future work.""",
        r"""Controlled noise injection ($\eta\in\{0.1,0.2,0.3\}$) is \textbf{not} reported in this revision and remains a first-order missing experiment.""",
        "seed_noise",
    )

    # Closing appendix remark
    text = repl(
        text,
        r"""Together with Sections~\ref{sec:method}--\ref{sec:experiments}, they fully specify FaithPath as a new temporally faithful retrieval-critique algorithm for TKGQA.""",
        r"""Together with Sections~\ref{sec:method}--\ref{sec:experiments}, they specify FaithPath as an ablatable evidence-layer retrieval--critique stack for TKGQA measurement.""",
        "app_closing",
    )

    TEX.write_text(text, encoding="utf-8")
    print("Phase2 OK")


if __name__ == "__main__":
    main()
