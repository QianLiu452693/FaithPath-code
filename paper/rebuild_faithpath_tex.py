#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild FaithPath_IEEEtran.tex as a coherent manuscript after pre-submission revisions.

Keeps: Preliminaries + Method (equations / algorithms / TikZ).
Rewrites: preamble packaging, Abstract, Intro, Related Work, Experiments,
          Discussion, Conclusion, lean appendix, bibliography.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "FaithPath_IEEEtran.tex"
OUT = ROOT / "FaithPath_IEEEtran.tex"
BACKUP = ROOT / "FaithPath_IEEEtran.tex.bak_before_rebuild"


def extract_between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j].rstrip() + "\n"


def main() -> None:
    old = SRC.read_text(encoding="utf-8")
    BACKUP.write_text(old, encoding="utf-8")

    method_core = extract_between(
        old,
        r"\section{Preliminaries}",
        r"\section{Experiments}",
    )
    # Drop duplicated trailing blank lines
    method_core = method_core.rstrip() + "\n\n"

    preamble = r"""\documentclass[lettersize,journal]{IEEEtran}
\usepackage{caption}
\usepackage{pgfplots}
\pgfplotsset{compat=1.17}
\usepackage{amsmath,amsfonts}
\usepackage{algorithmic}
\usepackage{algorithm}
\usepackage{array}
\usepackage[caption=false,font=normalsize,labelfont=sf,textfont=sf]{subfig}
\usepackage{textcomp}
\usepackage{stfloats}
\usepackage{url}
\usepackage{verbatim}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{tabularx}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{float}
\usepackage{amsthm}
\usepackage{enumitem}
\usepackage{multirow}
\usepackage{tikz}
\usepackage{xcolor}
\usepackage{bm}
\usepackage{mathtools}
\usetikzlibrary{positioning,arrows.meta,fit,calc,shapes.geometric}
\hyphenation{op-tical net-works semi-conduc-tor IEEE-Xplore}

\usepackage[%
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=magenta,
    pdfborder={0 0 0},
    bookmarks=true,
    pdfencoding=auto
]{hyperref}

\newtheorem{theorem}{Theorem}
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\newtheorem{remark}{Remark}
\newtheorem{assumption}{Assumption}

\newcommand{\FaithPath}{\textsc{FaithPath}}
\newcommand{\EGOR}{\textsc{EGOR}}
\newcommand{\TFC}{\textsc{TFC}}
\newcommand{\BiBFS}{\textsc{BiBFS}}
\newcommand{\Dpred}{D_{\mathrm{pred}}}
\newcommand{\Dmax}{D_{\max}}
\newcommand{\Score}{\mathrm{Score}}
\newcommand{\ind}{\mathbf{1}}

\begin{document}

\title{FaithPath: Temporally Faithful Bidirectional Path Reasoning with Experience-Guided Operator Routing for Temporal Knowledge Graph Question Answering}

\author{
Anonymous Authors
\thanks{Manuscript received ; revised . Corresponding author: Anonymous.}
}

\markboth{IEEE Transactions on Knowledge and Data Engineering}%
{FaithPath: Temporally Faithful Path Reasoning for TKGQA}

\maketitle
"""

    front = r"""
\begin{abstract}
Large Language Models (LLMs) struggle with temporal understanding on multi-entity, operator-compound temporal knowledge graph question answering (TKGQA).
We study the \emph{evidence layer}: closed-form path retrieval and path-level temporal verification \emph{without} end-to-end LLM answer synthesis.
We propose \textbf{FaithPath}, a retrieval--critique stack with three modules:
(1)~\textbf{Monotone BiBFS with Adaptive $\Dpred$}, the primary Hits@1 driver under our protocol;
(2)~\textbf{EGOR}, an LLM-optional symbolic router emitting structured $\rho$ (independent Hits@1 gain \emph{not} significant on our MultiTQ prefix);
(3)~\textbf{TFC}, a path-level faithfulness \emph{filter} (not a Hits@1 booster under retrieval-only extraction).
\textbf{Scope:} retrieval-grounded evaluation only; primary ablations use prefixes $n{=}500/200$, with \emph{full-test} MultiTQ ($n{=}54{,}584$) and TimeQuestions ($n{=}3237$).
Here \emph{faithfulness} means path--operator/anchor consistency, distinct from answer factual correctness; PathHit@80 measures evidence recall and Hits@1 measures answer hit.
On the MultiTQ prefix, FULL reaches \textbf{24.8\%} Hits@1 vs.\ weak priors B0/B1; on the MultiTQ full test, embedding multi-hop \textbf{B2} (\textbf{25.1\%}) significantly exceeds FULL ($24.3\%$).
On full TimeQuestions, B1/B2/FULL are statistically tied near $23$--$24\%$.
An untrained EXAQT-inspired proxy (B3) attains high PathHit but lower Hits@1 than FULL under our extractor.
\end{abstract}

\begin{IEEEkeywords}
Temporal Knowledge Graph Question Answering, Bidirectional Search, Temporal Faithfulness, Operator Routing, Evidence Retrieval, Experience Memory
\end{IEEEkeywords}

\section{Introduction}
\IEEEPARstart{L}{arge} Language Models (LLMs) are strong general reasoners but remain brittle on time-sensitive factual questions~\cite{brown2020language,khot2022decomposed}.
Retrieval-Augmented Generation (RAG) helps, yet text-only retrieval often ignores chronological constraints~\cite{jia2024faithful}.
Temporal Knowledge Graphs (TKGs) store facts as $(s,r,o,t)$ and enable TKGQA~\cite{chen2023multitq,jia2021complex}, where answers must obey operators such as \emph{before}, \emph{after}, \emph{first}, \emph{last}, and \emph{equal}, including compositions over multiple entities.

\subsection{Motivation and Challenges}
Recent LLM-agent TKGQA systems decompose questions, call toolkits, and optionally reuse memory~\cite{chen2024ari,hu2025tempagent,qian2024timer4,tan2025memotime}.
Their end-to-end Hits@1 can be high, but three evidence-layer gaps remain:
\begin{itemize}[leftmargin=*]
\item \textbf{Heuristic path depth.} Fixed $\Dmax$ exploration either wastes budget or under-covers multi-seed stitching windows.
\item \textbf{LLM-dependent operator routing.} Many MultiTQ types admit deterministic priors, yet systems still pay an LLM round-trip per sub-question.
\item \textbf{Weak post-retrieval faithfulness.} Non-monotone or poorly grounded paths may still enter answer synthesis.
\end{itemize}
We therefore isolate a closed-form retrieval--critique substrate that can sit beneath agents or be evaluated alone.

\subsection{Proposed Approach}
\textbf{FaithPath} couples three modules:
\textbf{Module~A} monotone BiBFS with Adaptive $\Dpred$ and semantic--temporal re-ranking;
\textbf{Module~B} EGOR, which emits structured $\rho=(\tau,\mathcal{O},d_\rho,m_{\mathrm{time}},\mathrm{sel},c)$ without mandatory LLM calls;
\textbf{Module~C} TFC, which checks monotonicity, anchors, and grounding at the path level.
Formally,
\begin{align}
\hat{a}&=\Psi_{\mathrm{TFC}}\!\Bigl(
\Pi_{\mathrm{BiBFS}}(Q,S;\rho)\Bigr),\\
\rho&=\Phi_{\mathrm{EGOR}}(Q,\mathcal{E}_{\mathrm{pool}}).
\end{align}

\subsection{Contributions}
\begin{itemize}[leftmargin=*]
\item We formalize FaithPath as an \emph{evidence-layer} retrieval--critique stack for TKGQA, evaluated under a retrieval-grounded protocol that separates PathHit (evidence recall) from Hits@1 (answer hit).
\item We present EGOR as an LLM-optional symbolic router; on our MultiTQ prefix its independent Hits@1 lift is \textbf{not} statistically significant.
\item We present TFC as a deterministic path-level faithfulness filter; under retrieval-only extraction it does not raise Hits@1 (A3$=$A1).
\item We report prefix ablations ($n{=}500/200$), full-test MultiTQ / TimeQuestions, stronger peers B2 (EmbedMHOP) and B3 (EXAQT-proxy), paired bootstrap CIs, and an explicit MemoTime differentiation (Section~\ref{sec:memotime}).
\end{itemize}

\subsection{Paper Organization}
Section~\ref{sec:related} reviews related work.
Section~\ref{sec:prelim}--\ref{sec:method} give preliminaries and FaithPath.
Section~\ref{sec:experiments} reports experiments.
Section~\ref{sec:discussion} discusses limitations; Section~\ref{sec:conclusion} concludes.

\section{Related Work}
\label{sec:related}

\subsection{Temporal Knowledge Graph Question Answering}
Early TKGQA methods embed temporal signals (CronKGQA~\cite{saxena2021cronkgqa}, TempoQR~\cite{mavromatis2022tempoqr}, TFLEX~\cite{lin2023tflex}) or retrieve subgraphs (EXAQT~\cite{jia2021complex}, TwiRGCN~\cite{sharma2022twirgcn}).
MultiTQ~\cite{chen2023multitq} and TimeQuestions~\cite{jia2021complex} remain standard; Mul$^2$Questions~\cite{liu2024mul2} further stresses dense multi-hop patterns.
We group recent lines as:
\emph{Embedding / PLM} (CronKGQA, TempoQR, TFLEX, MultiQA);
\emph{LLM agents} (ARI~\cite{chen2024ari}, TimeR$^4$~\cite{qian2024timer4}, TempAgent~\cite{hu2025tempagent}, RTQA~\cite{gong2025rtqa}, Temp-R1~\cite{gong2026tempr1});
\emph{Temporal complex-query embedding} (TFLEX).
FaithPath does not compete as another full LLM agent or trained query embedder; it isolates a training-free evidence retrieval and critique substrate.

\subsection{Closest Prior System: MemoTime}
\label{sec:memotime}
MemoTime~\cite{tan2025memotime} is the closest contemporaneous system on MultiTQ / TimeQuestions.
It couples Tree-of-Time LLM decomposition, operator-aware toolkit selection, temporally monotone pruning, experience-memory reuse, and semantic--temporal re-ranking of the form
$\mathrm{Score}=\lambda_{\mathrm{sem}}\mathrm{DRM}+\lambda_{\mathrm{prox}}\exp(-\delta/\sigma)$.
\textbf{Shared substrate.}
FaithPath reuses that retrieval-layer scoring form (Section~\ref{sec:bibfs}) and likewise uses experience exemplars.
\textbf{Differentiation.}
(i)~\emph{Loop:} MemoTime is an LLM-closed end-to-end agent; FaithPath is retrieval-only and does not claim MemoTime-style end-to-end Hits@1.
(ii)~\emph{Routing:} MemoTime selects toolkits inside an LLM loop; EGOR emits structured $\rho$ consumed symbolically (LLM-Select unused in our runs).
(iii)~\emph{Faithfulness:} MemoTime enforces temporal validity during agent search; TFC is a post-retrieval Accept/Faithful \emph{filter} that does not raise retrieval-only Hits@1 here.
(iv)~\emph{Depth:} FaithPath exposes Adaptive $\Dpred$ and multi-seed windows as first-class, ablatable equations.
We position FaithPath as a modularization of the evidence layer adjacent to MemoTime, not as a substitute for its LLM results.

\subsection{Temporal Path Retrieval and Faithfulness}
Bidirectional search and temporal pruning appear in TKG forecasting (TLogic~\cite{liu2022tlogic}, xERTE~\cite{han2021xerte}).
Faithful temporal QA~\cite{jia2024faithful} emphasizes evidence-supported timelines.
TFC uses a narrower contract: deterministic $C_1$--$C_3$ and grounding $g$ over retrieved paths; Accept $\neq$ answer correctness.

\subsection{Positioning}
\label{sec:positioning}
This paper is an \emph{evidence-layer retrieval ablation study}.
Primary lifts vs.\ weak priors B0/B1 are not SOTA claims vs.\ trained EXAQT or MemoTime full-LLM.
We additionally report B2/B3 under a matched retrieval-only protocol and full-test MultiTQ / TimeQuestions.
\textbf{Venue note.}
Without end-to-end LLM QA, the empirical scope is closer to a TKGQA Findings-style ablation than to a large-scale TKDE systems claim; we keep the TKDE template for formatting while stating this scope.

"""

    experiments = r"""
\section{Experiments}
\label{sec:experiments}

\subsection{Protocol}
\label{sec:protocol}
This paper is an \emph{evidence-layer retrieval ablation study}.
We answer by closed-form extraction from retrieved paths (no cloud LLM synthesis).
We separately report \textbf{PathHit@80} (gold on a top-$80$ path) and \textbf{Hits@1} (extracted answer matches gold).
Path-level TFC Accept/Faithful does \emph{not} equal answer correctness.
Literature Full-train / Full-LLM rows (including MemoTime-style agents and trained EXAQT) are contextual only.

\subsection{Datasets}
We evaluate on MultiTQ~\cite{chen2023multitq} and TimeQuestions~\cite{jia2021complex}.
Primary ablations use contiguous candidate-expanded prefixes: MultiTQ $n{=}500$ and TimeQuestions $n{=}200$ ($\sim$30 candidates/question).
Under the same protocol we also report the \emph{full} MultiTQ test ($n{=}54{,}584$) and the \emph{full} TimeQuestions test ($n{=}3237$).

\subsection{Baselines and Variants}
Literature embedding / PLM / LLM numbers are cited under their published settings.
FaithPath-internal variants:
\begin{itemize}[leftmargin=*]
\item \textbf{B0} CandidatePrior (top-1 seed; no walk).
\item \textbf{B1} OneHopLexical.
\item \textbf{B2} EmbedMHOP: embedding multi-hop without temporal-first prune / proximity.
\item \textbf{B3} EXAQT-proxy: untrained compact seed subgraph $+$ MiniLM fact--question filter (not trained GST/R-GCN EXAQT).
\item \textbf{A1} BiBFS only; \textbf{A2} BiBFS+EGOR; \textbf{A3} BiBFS+TFC; \textbf{FULL} BiBFS+EGOR+TFC.
\item \textbf{H1/H2/H3} FULL with $D_{\max}\in\{1,2,3\}$; \textbf{S1/S2} lexical vs.\ embedding Score.
\end{itemize}

\subsection{Main Results}
\label{sec:main}

\begin{table*}[!t]
\centering
\caption{MultiTQ Hits@1 (\%). Setting separates Full-train/Full-LLM literature from Retrieval-only FaithPath ($n{=}500$).
PathHit@80 of FULL is $58.4\%$.}
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

On the MultiTQ prefix, FULL reaches $24.8\%$ Hits@1 ($+14.0$ vs.\ B0, $+4.8$ vs.\ B1; paired CIs exclude $0$).
These deltas are relative to weak priors only, not trained EXAQT or MemoTime agents.
Paired FULL$-$A1 (EGOR) includes $0$.
Fig.~\ref{fig:hits_variants}--\ref{fig:hits_vs_pathhit} separate Hits@1 from PathHit@80.

\begin{table}[!t]
\centering
\caption{TimeQuestions Hits@1 (\%). FaithPath: Retrieval-only, $n{=}200$.}
\label{tab:t2}
\begin{tabular}{llcccc}
\toprule
\textbf{Model} & \textbf{Setting} & \textbf{Overall} & \textbf{Expl.} & \textbf{Temp.} & \textbf{Ord.} \\
\midrule
EXAQT~\cite{jia2021complex} & Full train & 57.2 & 56.8 & 64.2 & 42.0 \\
CronKGQA~\cite{saxena2021cronkgqa} & Full train & 46.3 & 46.4 & 52.7 & 31.8 \\
\midrule
CandidatePrior (B0) & Retrieval-only & 3.5 & 3.5 & 1.6 & 6.5 \\
OneHopLexical (B1) & Retrieval-only & 21.0 & 10.3 & 50.8 & 3.2 \\
\textbf{FaithPath (FULL)} & Retrieval-only & 23.0 & 6.9 & \textbf{61.9} & 3.2 \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[!t]
\centering
\caption{Full-test retrieval-only sweeps (Hits@1 / PathHit@80, \%).
MultiTQ full: B2 significantly exceeds FULL ($\Delta{+}0.80$, 95\% CI $[+0.58,+1.01]$).
TQ full: B1/B2/FULL tied.}
\label{tab:scale}
\begin{tabular}{lcccc}
\toprule
\textbf{Variant} & \textbf{MT full} & Path@80 & \textbf{TQ full} & Path@80 \\
\midrule
B0 CandidatePrior & 10.8 & 0.0 & 4.7 & 0.0 \\
B1 OneHopLexical & 20.0 & 70.5 & \textbf{24.2} & 57.7 \\
B2 EmbedMHOP & \textbf{25.1} & 60.1 & 23.2 & 60.9 \\
FULL & 24.3 & 60.9 & 23.0 & 58.5 \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[!t]
\centering
\caption{Matched retrieval-only peers on prefixes (Hits@1 / PathHit@80, \%).
B3$=$untrained EXAQT-proxy.
B3 can win PathHit while losing Hits@1 under closed-form extraction.}
\label{tab:peers}
\begin{tabular}{lcccc}
\toprule
\textbf{Variant} & \textbf{MT $n{=}500$} & Path@80 & \textbf{TQ $n{=}500$} & Path@80 \\
\midrule
B0 & 10.8 & 0.0 & 4.6 & 0.0 \\
B1 & 20.0 & 74.2 & 25.0 & 58.6 \\
B2 EmbedMHOP & \textbf{26.2} & 57.2 & 24.0 & 61.6 \\
B3 EXAQT-proxy & 22.2 & \textbf{76.8} & 18.8 & 65.2 \\
A1 BiBFS & 23.4 & 56.6 & --- & --- \\
FULL & 24.8 & 58.4 & \textbf{25.4} & 59.6 \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[!t]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig1_hits_variants.pdf}
\caption{Finding: FULL reaches $24.8\%$ Hits@1 vs.\ weak priors B0/B1; A3$=$A1 shows TFC alone does not lift retrieval-only Hits@1.}
\label{fig:hits_variants}
\end{figure}

\begin{figure}[!t]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig2_pathhit.pdf}
\caption{Finding: B1 PathHit@80 ($74.2\%$) exceeds FULL ($58.4\%$); high evidence recall alone does not yield best Hits@1.}
\label{fig:pathhit}
\end{figure}

\begin{figure}[!t]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig3_hits_vs_pathhit.pdf}
\caption{Finding: FULL PathHit@80 ($58.4\%$) far exceeds Hits@1 ($24.8\%$); evidence recall $\neq$ answer hit.}
\label{fig:hits_vs_pathhit}
\end{figure}

\begin{figure}[!t]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig9_scale_hits.pdf}
\caption{Finding: on MultiTQ full test, B2 exceeds FULL Hits@1; on full TimeQuestions, B1/B2/FULL are near-tied.
Color plus hatch encoding for colorblind-safe reading.}
\label{fig:scale_hits}
\end{figure}

\begin{table}[!t]
\centering
\caption{Weak-prior B0 vs.\ FaithPath (Hits@1, \%). Not a matched EXAQT/MemoTime comparison.}
\label{tab:t3}
\begin{tabular}{lcccc}
\toprule
\textbf{Dataset} & \textbf{B0} & \textbf{FaithPath} & $\uparrow$ vs B0 & $\times$ vs B0 \\
\midrule
MultiTQ ($n{=}500$) & 10.8 & \textbf{24.8} & $+14.0$ & $2.3\times$ \\
TimeQuestions ($n{=}200$) & 3.5 & \textbf{23.0} & $+19.5$ & $6.6\times$ \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Peer reading.}
B2 can exceed FULL on MultiTQ (Table~\ref{tab:scale}); B3 shows PathHit $\neq$ Hits@1 (Table~\ref{tab:peers}).
FULL still beats weak priors and beats B3 on Hits@1 under our extractor.
Trained EXAQT is not re-run; B3 is an unsupervised stage-1 proxy only.

\subsection{Ablation Study}
\label{sec:ablation}

\begin{table}[!t]
\centering
\caption{Ablation on MultiTQ (Hits@1 \%, $n{=}500$, Retrieval-only).}
\label{tab:t4}
\begin{tabular}{lccccc}
\toprule
\textbf{Model Variant} & \textbf{Overall} & \textbf{Mult.} & \textbf{Single} & \textbf{Ent.} & \textbf{Time} \\
\midrule
FaithPath (Full) & \textbf{24.8} & 10.4 & \textbf{30.1} & \textbf{27.8} & 18.1 \\
w/o Graph-based Retrieval (OneHop) & 20.0 & 11.1 & 23.3 & 24.9 & 9.0 \\
w/o Embedding Retrieval (lexical Score) & 23.4 & 7.4 & 29.3 & 26.7 & 16.1 \\
w/o Temporal Evidence Retrieval (B0) & 10.8 & 5.2 & 12.9 & 15.7 & 0.0 \\
w/o EGOR / type routing (BiBFS only) & 23.4 & \textbf{16.3} & 26.0 & 25.5 & \textbf{18.7} \\
w/o Adaptive depth ($D_{\max}{=}1$) & 24.2 & 8.2 & 30.1 & 27.0 & 18.1 \\
BiBFS+TFC only (A3) & 23.4 & 16.3 & 26.0 & 25.5 & 18.7 \\
\bottomrule
\end{tabular}
\end{table}

\textbf{Paired CIs ($n{=}500$).}
BiBFS vs.\ OneHop is the primary significant driver ($+3.4$ to $+4.8$\,pp).
EGOR (FULL$-$A1): observed $-1.4$\,pp; 95\% CI includes $0$ (no significant independent Hits@1 gain).
TFC: A3$=$A1; no Hits@1 lift under retrieval-only extraction.
Fig.~\ref{fig:ablation_delta} summarizes deltas vs.\ FULL.

\begin{figure}[!t]
\centering
\includegraphics[width=0.98\columnwidth]{figures/fig5_ablation_delta.pdf}
\caption{Ablation $\Delta$Hits@1 vs.\ FULL on MultiTQ ($n{=}500$).
Removing graph retrieval or all temporal evidence hurts most; EGOR/embedding lifts are small/non-significant.}
\label{fig:ablation_delta}
\end{figure}

\begin{figure}[!t]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig4_runtime.pdf}
\caption{Finding: BiBFS dominates latency (FULL $\approx$211\,s wall / $\approx$0.42\,s/q); H1 is much cheaper.
\textbf{Log-scale y-axis:} numeric labels give absolute seconds.}
\label{fig:runtime}
\end{figure}

\begin{figure}[!t]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig6_typed_multitq.pdf}
\caption{Finding: Single ($30.1\%$) far exceeds Multiple ($10.4\%$) under retrieval-only extraction.}
\label{fig:typed}
\end{figure}

\begin{figure}[!t]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig7_operator_type.pdf}
\caption{Finding: \texttt{before\_after}/\texttt{equal} are strongest; \texttt{before\_last}/\texttt{after\_first} remain hard.}
\label{fig:operator}
\end{figure}

\begin{figure}[!t]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig8_tq_and_errors.pdf}
\caption{Finding: TimeQuestions Temporal-type drives most gains; error mix shows evidence miss vs.\ selection gap.}
\label{fig:tq_errors}
\end{figure}

\subsection{Error Analysis}
Multiple questions ($10.4\%$ Hits@1) and compound operators (\texttt{before\_last}/\texttt{after\_first}) remain hard.
TFC $C_2$/$C_3$ check a single path against anchors; they do not fully encode cross-entity co-constraints (Section~\ref{sec:tfc}).
This is a mechanism gap, not only seed noise.

\section{Discussion}
\label{sec:discussion}
The PathHit--Hits@1 gap ($58.4\%$ vs.\ $24.8\%$ on the MultiTQ prefix) shows evidence can be present while ranked-path extraction fails, especially on Multiple questions.
\paragraph{Limitations.}
(1)~Typed ablations use prefixes; full-test Hits@1 are reported for MultiTQ ($54$k) and TimeQuestions ($3237$).
(2)~Evidence-layer only; FaithPath$+$LLM end-to-end QA is out of scope.
(3)~Trained EXAQT is not re-run; B3 is an untrained proxy.
(4)~Seed linking noise is first-order.
(5)~EGOR independent Hits@1 gain is not significant on the $n{=}500$ prefix; TFC does not raise retrieval-only Hits@1.
(6)~ICEWS geopolitical bias.
\paragraph{Optional future work.}
Trained EXAQT under our PathHit protocol; noise/$\theta_r$ sweeps; optional FaithPath$+$LLM gating studies.

\section{Conclusion}
\label{sec:conclusion}
We presented FaithPath as an evidence-layer retrieval--critique stack for TKGQA.
Under retrieval-grounded evaluation, FULL improves over weak priors B0/B1, while B2 can exceed FULL on MultiTQ full test and B3 shows PathHit $\neq$ Hits@1.
BiBFS is the main internal Hits@1 driver; EGOR and TFC should be described as routing control and faithfulness filtering, not as proven independent accuracy modules under our protocol.
"""

    appendix = r"""
\appendix

\section{Notation Summary}
\label{app:notation}
\begin{table}[!t]
\centering
\caption{Notation summary.}
\label{tab:notation}
\begin{tabular}{ll}
\toprule
\textbf{Symbol} & \textbf{Meaning} \\
\midrule
$\mathcal{G}=(\mathcal{E},\mathcal{R},\mathcal{T},\mathcal{F})$ & temporal knowledge graph \\
$Q$, $I$ & question / indicator text \\
$S$ & seed entities \\
$p$, $|p|$ & temporal path and length \\
$\Dpred$, $\Dmax$, $D$ & predicted / max / effective depth \\
$\rho$ & EGOR routing decision \\
$k_{\max}$ & max operators in EGOR bundle ($\neq\Dmax$) \\
$\mathcal{P}^\star$, $\mathcal{P}_{\mathrm{beam}}$ & ranked / beamed paths \\
$\Phi_{\mathrm{TFC}}$, Faithful & critic score / acceptance bit \\
\bottomrule
\end{tabular}
\end{table}

\section{Threats to Validity}
\label{app:threats}
\begin{itemize}[leftmargin=*]
\item \textbf{Internal:} full-test Hits@1 reported; typed ablations use prefixes $n{=}500/200$.
\item \textbf{Construct:} retrieval-grounded Hits@1 $\neq$ LLM Hits@1; PathHit $\neq$ correctness.
\item \textbf{External:} trained EXAQT unmatched (B3 is unsupervised proxy); ICEWS bias.
\item \textbf{Statistical:} EGOR $+1.4$ CI includes $0$ on the $n{=}500$ prefix.
\end{itemize}

\section{Reproducibility Notes}
\label{app:repro}
Hardware: NVIDIA RTX~5060 Laptop GPU; encoder: MiniLM (\texttt{all-MiniLM-L6-v2}).
Defaults: $D_{\max}{=}3$, $W_1{=}80$, $(\lambda_{\mathrm{sem}},\lambda_{\mathrm{prox}}){=}(0.6,0.4)$, $\theta_r{=}0.5$, $k_{\max}{=}3$.
Code path: comparison variants B0--B3/A1--A3/FULL with paired bootstrap Hits@1.
"""

    bib = r"""
\begin{thebibliography}{99}

\bibitem{brown2020language}
T.~B.~Brown \emph{et~al.}, ``Language models are few-shot learners,'' arXiv:2005.14165, 2020.

\bibitem{chen2023multitq}
Z.~Chen, J.~Liao, and X.~Zhao, ``Multi-granularity temporal question answering over knowledge graphs,'' in \emph{ACL}, 2023.

\bibitem{chen2024ari}
Z.~Chen, D.~Li, X.~Zhao, \emph{et~al.}, ``Temporal knowledge question answering via abstract reasoning induction,'' in \emph{ACL}, 2024.

\bibitem{devlin2019bert}
J.~Devlin \emph{et~al.}, ``BERT: Pre-training of deep bidirectional transformers for language understanding,'' in \emph{NAACL}, 2019.

\bibitem{han2021xerte}
Z.~Han, P.~Chen, Y.~Ma, and V.~Tresp, ``Explainable subgraph reasoning for forecasting on temporal knowledge graphs,'' in \emph{ICLR}, 2021.

\bibitem{hu2025tempagent}
Q.~Hu, X.~Tu, \emph{et~al.}, ``Time-aware ReAct agent for temporal knowledge graph question answering,'' in \emph{Findings of NAACL}, 2025.

\bibitem{jia2021complex}
Z.~Jia, S.~Pramanik, R.~Saha~Roy, and G.~Weikum, ``Complex temporal question answering on knowledge graphs,'' in \emph{CIKM}, 2021.

\bibitem{jia2024faithful}
Z.~Jia, P.~Christmann, and G.~Weikum, ``Faithful temporal question answering over heterogeneous sources,'' in \emph{WWW}, 2024.

\bibitem{khot2022decomposed}
T.~Khot \emph{et~al.}, ``Decomposed prompting: A modular approach for solving complex tasks,'' arXiv:2210.02406, 2022.

\bibitem{lan2019albert}
Z.~Lan \emph{et~al.}, ``ALBERT: A lite BERT for self-supervised learning of language representations,'' arXiv:1909.11942, 2019.

\bibitem{liu2022tlogic}
Y.~Liu, Y.~Ma, M.~Hildebrandt, M.~Joblin, and V.~Tresp, ``TLogic: Temporal logical rules for explainable link forecasting on temporal knowledge graphs,'' in \emph{AAAI}, 2022.

\bibitem{mavromatis2022tempoqr}
C.~Mavromatis \emph{et~al.}, ``TempoQR: Temporal question reasoning over knowledge graphs,'' in \emph{AAAI}, 2022.

\bibitem{qian2024timer4}
X.~Qian \emph{et~al.}, ``TimeR$^4$: Time-aware retrieve-rewrite-reason-refine for TKGQA,'' in \emph{EMNLP}, 2024.

\bibitem{saxena2021cronkgqa}
A.~Saxena, S.~Chakrabarti, and P.~Talukdar, ``Question answering over temporal knowledge graphs,'' in \emph{ACL}, 2021.

\bibitem{sharma2022twirgcn}
A.~Sharma, A.~Saxena, \emph{et~al.}, ``TwiRGCN: Temporally weighted graph convolution for question answering over temporal knowledge graphs,'' 2022.

\bibitem{tan2025memotime}
X.~Tan, X.~Wang, Q.~Liu, X.~Xu, X.~Yuan, L.~Zhu, and W.~Zhang, ``MemoTime: Memory-augmented temporal knowledge graph enhanced large language model reasoning,'' in \emph{Proc.\ ACM Web Conf.\ (WWW)}, 2026, arXiv:2510.13614.

\bibitem{gong2025rtqa}
Z.~Gong, J.~Li, Z.~Liu, L.~Liang, H.~Chen, and W.~Zhang, ``RTQA: Recursive thinking for complex temporal knowledge graph question answering with large language models,'' in \emph{EMNLP}, 2025.

\bibitem{gong2026tempr1}
Z.~Gong, Z.~Liu, S.~Li, \emph{et~al.}, ``Temp-R1: A unified autonomous agent for complex temporal KGQA via reverse curriculum reinforcement learning,'' in \emph{ACL}, 2026, arXiv:2601.18296.

\bibitem{lin2023tflex}
X.~Lin, Haihong~E, C.~Xu, \emph{et~al.}, ``TFLEX: Temporal feature-logic embedding framework for complex reasoning over temporal knowledge graphs,'' in \emph{NeurIPS}, 2023.

\bibitem{liu2024mul2}
J.~Liu, Z.~Liu, X.~Lyu, P.~Jin, and J.~Xu, ``Towards multi-relational multi-hop reasoning over dense temporal knowledge graphs,'' in \emph{Findings of ACL}, 2024.

\end{thebibliography}

\end{document}
"""

    # Ensure method labels referenced in rewritten front exist
    if r"\label{sec:bibfs}" not in method_core:
        method_core = method_core.replace(
            r"\subsection{Module A: Monotone BiBFS with Adaptive $D_{\mathrm{pred}}$}",
            r"\subsection{Module A: Monotone BiBFS with Adaptive $D_{\mathrm{pred}}$}"
            + "\n"
            + r"\label{sec:bibfs}",
            1,
        )

    doc = preamble + front + method_core + experiments + appendix + bib
    # Strip em dashes if any slipped in
    doc = doc.replace("\u2014", ", ").replace("---", ", ")
    OUT.write_text(doc, encoding="utf-8")
    print(f"backup -> {BACKUP}")
    print(f"wrote  -> {OUT}")
    print(f"lines  -> {doc.count(chr(10))+1}")


if __name__ == "__main__":
    main()
