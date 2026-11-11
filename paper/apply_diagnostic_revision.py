#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reposition FaithPath as a diagnostic analysis paper + clean residual issues."""
from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "FaithPath_IEEEtran.tex"


def repl(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"MISSING: {label}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    Path(str(TEX) + ".bak_before_diagnostic").write_text(text, encoding="utf-8")

    text = repl(
        text,
        r"\title{FaithPath: An Evidence-Layer Ablation Study of Temporally Faithful Path Retrieval for TKGQA}",
        r"\title{Diagnosing the Evidence Layer in TKGQA: PathHit--Hits Gaps, Temporal-First Tradeoffs, and FaithPath Ablations}",
        "title",
    )
    text = repl(
        text,
        r"{FaithPath: Evidence-Layer Ablation for TKGQA Retrieval}",
        r"{Diagnosing the TKGQA Evidence Layer with FaithPath Ablations}",
        "markboth",
    )

    old_abs = r"""\begin{abstract}
This paper is an \emph{evidence-layer ablation and measurement study} for temporal knowledge graph question answering (TKGQA), not an end-to-end SOTA claim.
We formalize a closed-form retrieval--critique stack (\textbf{FaithPath}) whose modules can be ablated under a retrieval-grounded protocol (path-tail/time extraction; no LLM answer synthesis):
(1)~\textbf{Monotone BiBFS with Adaptive $\Dpred$} (primary Hits@1 driver vs.\ weak one-hop priors);
(2)~\textbf{EGOR}, a symbolic LLM-optional router emitting structured $\rho$ (independent Hits@1 gain \emph{not} significant on our MultiTQ prefix);
(3)~\textbf{TFC}, a path-level faithfulness \emph{filter} (A3$=$A1 under retrieval-only extraction).
Here \emph{faithfulness} means path--operator/anchor consistency, distinct from answer correctness; PathHit@80 $=$ evidence recall and Hits@1 $=$ answer hit under a deliberately weak extractor.
\textbf{Scope:} prefixes $n{=}500/200$ for typed ablations; full-test MultiTQ ($n{=}54{,}584$) and TimeQuestions ($n{=}3237$); no FaithPath$+$LLM closed-loop Hits@1.
On MultiTQ full test, stronger peer \textbf{B2} (embedding multi-hop \emph{without} temporal-first prune/proximity) reaches \textbf{25.1\%} vs.\ FULL \textbf{24.3\%} (paired $\Delta{+}0.80$\,pp, 95\% CI $[+0.58,+1.01]$, excludes $0$).
Typed breakdowns show B2's margin concentrates on Multiple and \texttt{before\_last}, consistent with temporal-first pruning harming some gold paths.
On full TimeQuestions, B1/B2/FULL are tied near $23$--$24\%$.
B3 (untrained EXAQT-proxy) can win PathHit while losing Hits@1.
We position FaithPath as a modularization and negative-result report adjacent to MemoTime-style retrieval, not as a substitute for Full-LLM agents.
\end{abstract}"""

    new_abs = r"""\begin{abstract}
We present a \emph{diagnostic analysis} of the TKGQA evidence layer under a retrieval-grounded protocol (no LLM answer synthesis).
Using an ablatable stack (\textbf{FaithPath}: monotone BiBFS, EGOR routing, TFC path filter) we separate \textbf{PathHit@80} (evidence recall) from \textbf{Hits@1} (weak path-tail/time extraction).
Three findings organize the paper:
(i)~\textbf{Selection is the bottleneck:} on MultiTQ $n{=}500$, FULL PathHit@80 is $58.4\%$ while Hits@1 is $24.8\%$ ($44.7\%$ of errors are selection gaps).
(ii)~\textbf{Temporal-first is not uniformly helpful:} on MultiTQ full test ($n{=}54{,}584$), embedding multi-hop \textbf{B2} (no temporal-first prune/proximity) reaches $25.1\%$ vs.\ FULL $24.3\%$ (paired $\Delta{+}0.80$\,pp, 95\% CI $[+0.58,+1.01]$); the margin concentrates on Multiple and \texttt{before\_last}.
Controlled ablations disentangle prune vs.\ proximity; seed-noise curves quantify linking fragility.
(iii)~\textbf{Module-level negative results under a weak extractor:} EGOR's $+1.4$\,pp lift is not significant at $n{=}500$ (under-powered for $<$2\,pp effects); TFC yields A3$=$A1 Hits@1 and is weakest on Multiple.
We do \emph{not} claim end-to-end SOTA or FaithPath$+$LLM gains; the contribution is a reproducible diagnosis of evidence-layer failure modes adjacent to MemoTime-style retrieval.
\end{abstract}"""
    text = repl(text, old_abs, new_abs, "abstract")

    text = repl(
        text,
        r"""\begin{IEEEkeywords}
Temporal Knowledge Graph Question Answering, Evidence Retrieval, Ablation Study, Bidirectional Search, Temporal Faithfulness, Operator Routing, PathHit
\end{IEEEkeywords}""",
        r"""\begin{IEEEkeywords}
Temporal Knowledge Graph Question Answering, Evidence Retrieval, Diagnostic Analysis, PathHit, Selection Gap, Temporal Pruning, Ablation
\end{IEEEkeywords}""",
        "keywords",
    )

    old_contrib = r"""\subsection{Contributions}
\begin{itemize}[leftmargin=*]
\item We formalize and \emph{ablate} an evidence-layer retrieval--critique stack (Adaptive-$\Dpred$ BiBFS, EGOR, TFC) under a retrieval-grounded protocol that separates PathHit (evidence recall) from Hits@1 (answer hit).
\item We report \textbf{negative / non-significant} module results under this protocol: EGOR's independent Hits@1 lift is not significant on the MultiTQ $n{=}500$ prefix (paired CI includes $0$); TFC does not change retrieval-only Hits@1 (A3$=$A1). These modules are retained as ablatable control surfaces, not as proven accuracy contributions.
\item We show that a stronger retrieval peer (\textbf{B2}) can exceed FULL on MultiTQ full test, and analyze where the gap arises (Multiple / \texttt{before\_last}), clarifying that lifts vs.\ weak priors B0/B1 alone are insufficient.
\item We differentiate FaithPath from MemoTime as modularization and measurement of a shared retrieval substrate (Section~\ref{sec:memotime}), not as an end-to-end LLM-agent replacement.
\end{itemize}"""

    new_contrib = r"""\subsection{Contributions}
\begin{itemize}[leftmargin=*]
\item \textbf{Diagnosis:} quantify that TKGQA retrieval often recalls gold evidence (PathHit) while weak extraction fails (Hits@1), making selection---not only retrieval---the dominant failure mode.
\item \textbf{Counterintuitive tradeoff:} show B2 $>$ FULL on MultiTQ full test and localize the gap; controlled ablations separate temporal-first pruning from proximity scoring.
\item \textbf{Robustness:} report seed-noise degradation curves ($\eta\in\{0.1,0.2,0.3\}$) under the same protocol.
\item \textbf{Calibrated negatives:} under a weak extractor and $n{=}500$, EGOR is under-powered for $<$2\,pp effects (not a proof of zero effect); TFC does not raise Hits@1 (A3$=$A1) and lacks cross-entity coverage on Multiple.
\item \textbf{Positioning:} treat FaithPath as a measurement scaffold adjacent to MemoTime, not as a TKDE-scale systems claim; venue scope is Findings-style analysis unless LLM closed-loop and trained peers are added.
\end{itemize}"""
    text = repl(text, old_contrib, new_contrib, "contrib")

    # Demote propositions
    text = repl(
        text,
        r"""\begin{proposition}[Monotonicity is Prefix-Closed]
If $p$ is monotone and $p'$ is a prefix of $p$, then $p'$ is monotone.
\end{proposition}
\begin{proof}
Any consecutive pair in $p'$ is also consecutive in $p$; the product in \eqref{eq:mono} remains $1$.
\end{proof}

\begin{proposition}[Stitching Preserves Monotonicity]
If segments $p^{(1)},\ldots,p^{(n-1)}$ are each monotone and satisfy
$t_{\mathrm{end}}(p^{(i)})\preceq t_{\mathrm{start}}(p^{(i+1)})$ for all $i$, then the stitched path is monotone.
\end{proposition}
\begin{proof}
Within-segment pairs obey monotonicity by assumption; cross-segment junctions obey the stitching inequalities; the global product is therefore $1$.
\end{proof}""",
        r"""\begin{remark}[Monotonicity is prefix-closed]
If $p$ is monotone and $p'$ is a prefix of $p$, then $p'$ is monotone, since every consecutive pair in $p'$ appears in $p$.
\end{remark}

\begin{remark}[Stitching preserves monotonicity]
If each segment is monotone and junction times satisfy
$t_{\mathrm{end}}(p^{(i)})\preceq t_{\mathrm{start}}(p^{(i+1)})$, the stitched path is monotone.
\end{remark}""",
        "props",
    )

    # Fix By Proposition~1 references if any
    text = text.replace("By Proposition~1,", "By the prefix-closed remark,")
    text = text.replace("Proposition~1", "the prefix-closed remark")
    text = text.replace("Proposition~2", "the stitching remark")

    # Remove Core labels appendix residue
    text = repl(
        text,
        r"""\section{Symbol Index by Equation}
\label{app:eqindex}
Core labels:
\eqref{eq:tkg}--\eqref{eq:mono},
\eqref{eq:pipeline},
\eqref{eq:nbr}--\eqref{eq:compA},
\eqref{eq:rho}--\eqref{eq:compB},
\eqref{eq:c1}--\eqref{eq:comp_all}.

""",
        "",
        "core_labels",
    )

    # Soften Score min redundancy note in appendix if present - add remark near path_faith
    text = repl(
        text,
        r"""\phi(p)&=w_1 C_1(p)+w_2 C_3(p;m,\mathcal{A})
+w_3\min\bigl(1,\mathrm{Score}(p)\bigr),\\""",
        r"""\phi(p)&=w_1 C_1(p)+w_2 C_3(p;m,\mathcal{A})
+w_3\,\mathrm{Score}(p),\\""",
        "phi_score",
    )

    # Unify Finding captions: strip "Finding:"
    text = text.replace(r"\caption{Finding: ", r"\caption{")

    # Venue positioning stronger
    text = repl(
        text,
        r"""\textbf{Venue note.}
The empirical scope matches a Findings-style ablation more than a large-scale TKDE systems claim; we keep the TKDE template for formatting while stating this scope explicitly.""",
        r"""\textbf{Venue note.}
Author self-assessment: absent FaithPath$+$LLM closed-loop Hits@1, trained EXAQT/MemoTime matched runs, and a systems-scale deployment study, the present contribution is a \emph{Findings-style diagnostic analysis}, not a TKDE systems claim.
We retain the TKDE template only for formatting while recommending Findings/short-paper venues unless those gaps are closed.""",
        "venue",
    )

    # Power analysis paragraph expansion
    text = repl(
        text,
        r"""\textbf{Power note:} at $n{=}500$, detecting a $\sim$1.4\,pp paired effect is under-powered (rough SE $\approx$2--3\,pp); ``not significant'' $\neq$ ``proven null.''""",
        r"""\textbf{Power analysis (EGOR).}
For paired Bernoulli outcomes near $p{\approx}0.24$, a rough SE for a difference is
$\sqrt{2p(1-p)/n}\approx 2.7$\,pp at $n{=}500$.
Detecting a $1.4$\,pp effect at $80\%$ power (two-sided $z{\approx}2.8$) would require on the order of $n{\sim}10^4$ questions.
Thus ``CI includes $0$ at $n{=}500$'' means \emph{under-powered}, not a proof that EGOR has zero effect under a stronger extractor.""",
        "power",
    )

    # Ordinal note after TQ table mention
    if "Ordinal remains hard" not in text:
        text = repl(
            text,
            r"""FULL reaches $23.0\%$ overall and $61.9\%$ on Temporal-type questions under retrieval-only extraction (Fig.~\ref{fig:tq_errors}, left); these numbers are not comparable to Table~\ref{tab:lit_tq}.""",
            r"""FULL reaches $23.0\%$ overall and $61.9\%$ on Temporal-type questions under retrieval-only extraction (Fig.~\ref{fig:tq_errors}, left); these numbers are not comparable to Table~\ref{tab:lit_tq}.
\textbf{Ordinal:} FULL Ordinal Hits@1 is only $3.2\%$ (tied with B1), indicating that EGOR/TFC provide no measurable help for ordinal ranking under path-tail extraction---consistent with TFC's single-path $C_2$/$C_3$ boundary.""",
            "ordinal",
        )

    # Conclusion rewrite
    old_c = r"""\section{Conclusion}
\label{sec:conclusion}

We presented \textbf{FaithPath} as an evidence-layer \emph{ablation and measurement} stack for TKGQA retrieval (Adaptive-$\Dpred$ BiBFS, EGOR, TFC).
Under a retrieval-grounded weak-extractor protocol, BiBFS drives gains vs.\ weak one-hop priors, while EGOR and TFC do not deliver significant independent Hits@1 gains.
On MultiTQ full test, B2 exceeds FULL (paired CI $[+0.58,+1.01]$), with the margin concentrated on Multiple and \texttt{before\_last}---showing that temporal-first retrieval is not uniformly best and that weak-prior comparisons alone are insufficient.
We recommend reading this work as a modular negative-result / measurement paper adjacent to MemoTime-style agents, and treating FaithPath$+$LLM selection, TFC abstention curves, and prune-error analyses as the next required experiments---not as optional extras."""

    new_c = r"""\section{Conclusion}
\label{sec:conclusion}

This paper diagnoses the TKGQA evidence layer rather than claiming a new end-to-end SOTA system.
Under retrieval-grounded extraction, PathHit far exceeds Hits@1 (selection bottleneck); temporal-first FULL can lose to simpler B2 on MultiTQ full test; EGOR/TFC lack significant independent Hits@1 gains under a weak extractor and limited $n$.
Controlled prune/proximity ablations and seed-noise curves make these failure modes measurable.
We recommend Findings-style venues for the present scope, and TKDE-scale resubmission only after adding FaithPath$+$LLM selection, matched MemoTime/trained-EXAQT retrieval comparisons, and complete abstention analyses."""
    text = repl(text, old_c, new_c, "conclusion")

    TEX.write_text(text, encoding="utf-8")
    print("diagnostic revision OK")


if __name__ == "__main__":
    main()
