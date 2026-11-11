#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply pre-submit major revision narrative patches to FaithPath_IEEEtran.tex."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEX = ROOT / "FaithPath_IEEEtran.tex"
BACKUP = ROOT / "FaithPath_IEEEtran.tex.bak_before_major_rev"


def repl(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"MISSING BLOCK: {label}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    BACKUP.write_text(text, encoding="utf-8")

    text = repl(
        text,
        r"\title{FaithPath: Temporally Faithful Bidirectional Path Reasoning with Experience-Guided Operator Routing for Temporal Knowledge Graph Question Answering}",
        r"\title{FaithPath: An Evidence-Layer Ablation Study of Temporally Faithful Path Retrieval for TKGQA}",
        "title",
    )

    text = repl(
        text,
        r"{FaithPath: Temporally Faithful Path Reasoning for TKGQA}",
        r"{FaithPath: Evidence-Layer Ablation for TKGQA Retrieval}",
        "markboth",
    )

    old_abs = r"""\begin{abstract}
Large Language Models (LLMs) struggle with temporal understanding on multi-entity, operator-compound TKGQA.
We study the \emph{evidence layer} of temporally faithful retrieval: predicting exploration depth, routing operators without mandatory LLM prompting, and verifying path-level temporal constraints before answer extraction.
We propose \textbf{FaithPath}, a closed-form retrieval--critique stack with three modules:
(1)~\textbf{Monotone BiBFS with Adaptive $\Dpred$}, the primary accuracy driver under our protocol;
(2)~\textbf{EGOR}, a symbolic, LLM-optional structured router (independent Hits@1 gain \emph{not} significant on our prefix);
(3)~\textbf{TFC}, a path-level faithfulness \emph{filter} (not a Hits@1 booster under retrieval-only extraction).
\textbf{Scope:} retrieval-grounded evidence-layer evaluation (no FaithPath$+$LLM end-to-end Hits@1); primary ablations use prefixes $n{=}500/200$, with \emph{full-test} MultiTQ ($n{=}54{,}584$) and TimeQuestions ($n{=}3237$).
Here \emph{faithfulness} means path--operator/anchor consistency (TFC), not answer factual correctness; PathHit@80 measures evidence recall, Hits@1 measures answer hit.
On the MultiTQ prefix, FULL reaches \textbf{24.8\%} Hits@1 (PathHit@80 \textbf{58.4\%}) vs.\ weak priors B0/B1; on the MultiTQ \emph{full} test, embedding multi-hop \textbf{B2} (\textbf{25.1\%}) \emph{significantly} exceeds FULL ($24.3\%$; paired $\Delta{+}0.8$\,pp).
On full TimeQuestions, B1/B2/FULL are statistically tied near $23$--$24\%$.
An untrained EXAQT-inspired proxy (\textbf{B3}) attains higher PathHit but lower Hits@1 than FULL under our extractor (PathHit $\neq$ Hits@1).
Ablations: BiBFS drives the lift vs.\ one-hop; EGOR's independent Hits@1 gain is not significant; TFC does not change retrieval-only Hits@1 (A3$=$A1).
\end{abstract}"""

    new_abs = r"""\begin{abstract}
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
    text = repl(text, old_abs, new_abs, "abstract")

    text = repl(
        text,
        r"""\begin{IEEEkeywords}
Large Language Models, Retrieval-Augmented Generation, Temporal Knowledge Graph, Temporal Knowledge Graph Question Answering, Bidirectional Search, Temporal Faithfulness, Operator Routing, Experience Memory
\end{IEEEkeywords}""",
        r"""\begin{IEEEkeywords}
Temporal Knowledge Graph Question Answering, Evidence Retrieval, Ablation Study, Bidirectional Search, Temporal Faithfulness, Operator Routing, PathHit
\end{IEEEkeywords}""",
        "keywords",
    )

    # Contributions
    old_contrib = r"""\subsection{Contributions}
\begin{itemize}[leftmargin=*]
\item We formalize FaithPath as an \emph{evidence-layer} retrieval--critique stack for TKGQA: adaptive-$\Dpred$ monotone BiBFS with multi-seed stitching, evaluated under a retrieval-grounded protocol that isolates path evidence from LLM answer synthesis.
\item We present EGOR as an \emph{LLM-optional} symbolic router emitting structured $\rho$ for depth/mode/selection control; we report that its Hits@1 lift is \textbf{not} statistically significant on our prefix.
\item We present TFC as a deterministic \emph{path-level faithfulness filter} (not answer correctness); under retrieval-only extraction it does not raise Hits@1.
\item We report prefix ablations ($n{=}500/200$), full-test MultiTQ / TimeQuestions, matched peers B2 (EmbedMHOP) and B3 (EXAQT-proxy), paired bootstrap CIs, and an explicit MemoTime differentiation (Section~\ref{sec:memotime}).
\end{itemize}"""

    new_contrib = r"""\subsection{Contributions}
\begin{itemize}[leftmargin=*]
\item We formalize and \emph{ablate} an evidence-layer retrieval--critique stack (Adaptive-$\Dpred$ BiBFS, EGOR, TFC) under a retrieval-grounded protocol that separates PathHit (evidence recall) from Hits@1 (answer hit).
\item We report \textbf{negative / non-significant} module results under this protocol: EGOR's independent Hits@1 lift is not significant on the MultiTQ $n{=}500$ prefix (paired CI includes $0$); TFC does not change retrieval-only Hits@1 (A3$=$A1). These modules are retained as ablatable control surfaces, not as proven accuracy contributions.
\item We show that a stronger retrieval peer (\textbf{B2}) can exceed FULL on MultiTQ full test, and analyze where the gap arises (Multiple / \texttt{before\_last}), clarifying that lifts vs.\ weak priors B0/B1 alone are insufficient.
\item We differentiate FaithPath from MemoTime as modularization and measurement of a shared retrieval substrate (Section~\ref{sec:memotime}), not as an end-to-end LLM-agent replacement.
\end{itemize}"""
    text = repl(text, old_contrib, new_contrib, "contributions")

    text = repl(
        text,
        r"""\subsection{Proposed Approach}
We propose \textbf{FaithPath}, a new neurosymbolic algorithm for temporally faithful TKGQA retrieval and critique (overview in Fig.~\ref{fig:intro}; full pipeline in Fig.~\ref{fig:framework}).
FaithPath contributes three complementary modules:""",
        r"""\subsection{Proposed Approach}
We formalize \textbf{FaithPath} as a closed-form evidence-layer stack for measurement (overview in Fig.~\ref{fig:intro}; full pipeline in Fig.~\ref{fig:framework}).
Three ablatable modules are specified:""",
        "proposed",
    )

    # Soften method opening
    text = repl(
        text,
        r"""FaithPath is a new algorithm composed of three mathematically specified modules (Fig.~\ref{fig:framework}):
\textbf{Module~A} Monotone BiBFS with Adaptive $\Dpred$;
\textbf{Module~B} EGOR;
\textbf{Module~C} TFC.""",
        r"""FaithPath comprises three mathematically specified, ablatable modules (Fig.~\ref{fig:framework}):
\textbf{Module~A} Monotone BiBFS with Adaptive $\Dpred$;
\textbf{Module~B} EGOR (routing control surface);
\textbf{Module~C} TFC (path-level filter, not a Hits@1 booster under our extractor).""",
        "method_open",
    )

    # MemoTime differentiation honesty
    old_memo = r"""We therefore position FaithPath as a modularization and measurement of the evidence layer adjacent to MemoTime, not as a substitute for its LLM end-to-end results."""
    new_memo = r"""\textbf{Honest increment.}
The scientific increment relative to MemoTime is primarily \emph{modularization, ablatable equations, and negative-result reporting} under a retrieval-only protocol---not a new end-to-end reasoning paradigm.
Shared ingredients (monotone pruning, experience cues, semantic--temporal Score) are reused by design; Adaptive $\Dpred$, structured $\rho$, and post-hoc TFC are the measurement knobs.
We therefore position FaithPath as an evidence-layer ablation adjacent to MemoTime, not as a substitute for its LLM end-to-end results."""
    text = repl(text, old_memo, new_memo, "memotime")

    # Positioning
    old_pos = r"""\subsection{Positioning}
This paper is an \emph{evidence-layer retrieval ablation study}: Adaptive-$\Dpred$ BiBFS $+$ EGOR $+$ TFC under a retrieval-grounded protocol.
Primary lifts are relative to weak priors (B0/B1); Table~\ref{tab:scale} further compares a stronger embedding multi-hop peer (B2).
Matched EXAQT and MemoTime full-LLM numbers remain protocol-incomparable.
\textbf{Venue note.}
Without full-test MultiTQ and without end-to-end LLM QA, the empirical scope is closer to a TKGQA / NLP Findings-style ablation paper than to a large-scale TKDE systems claim; we keep the TKDE template for formatting while stating this scope explicitly."""
    new_pos = r"""\subsection{Positioning}
\label{sec:positioning}
This paper is an \emph{evidence-layer retrieval ablation and measurement study}.
Primary internal comparisons include weak priors (B0/B1), BiBFS-only (A1), and stronger retrieval peers (B2 EmbedMHOP; B3 EXAQT-proxy).
On MultiTQ full test, B2 exceeds FULL; we treat this as a central empirical finding, not a footnote.
Matched trained EXAQT, RTQA/Temp-R1 retrieval components, and MemoTime full-LLM numbers remain protocol-incomparable; we cite them contextually only.
\textbf{Extractor caveat.}
Our Hits@1 uses a weak path-tail/time extractor; module effects may be attenuated by extractor noise (PathHit $\gg$ Hits@1). FaithPath$+$LLM selection is left as required follow-up (Section~\ref{sec:discussion}).
\textbf{Venue note.}
The empirical scope matches a Findings-style ablation more than a large-scale TKDE systems claim; we keep the TKDE template for formatting while stating this scope explicitly."""
    text = repl(text, old_pos, new_pos, "positioning")

    TEX.write_text(text, encoding="utf-8")
    print("Phase1 OK:", TEX)
    print("bytes", TEX.stat().st_size)


if __name__ == "__main__":
    main()
