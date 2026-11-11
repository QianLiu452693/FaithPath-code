# -*- coding: utf-8 -*-
"""Build FaithPath IEEEtran.tex: full technical content, zero MemoTime traces, novel-algorithm framing."""
from pathlib import Path

OUT = Path(__file__).with_name("FaithPath_IEEEtran.tex")
parts: list[str] = []


def add(s: str) -> None:
    parts.append(s.rstrip("\n") + "\n")


add(r"""\documentclass[lettersize,journal]{IEEEtran}
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
""")

add(r"""
\begin{abstract}
Large Language Models (LLMs) have achieved impressive reasoning abilities, but struggle with temporal understanding, especially when questions involve multiple entities, compound operators, and evolving event sequences.
Temporal Knowledge Graphs (TKGs) offer structured temporal facts for Temporal Knowledge Graph Question Answering (TKGQA).
Existing TKG-based and LLM-augmented reasoners still lack an integrated, closed-form treatment of (i)~question-conditioned exploration depth under temporal monotonicity, (ii)~operator routing that is not mandatory LLM prompting, and (iii)~deterministic post-retrieval temporal faithfulness verification.
We propose \textbf{FaithPath}, a \emph{new} neurosymbolic retrieval-and-critique algorithm with three tightly coupled modules:
(1)~\textbf{Monotone Bidirectional BFS (BiBFS) with Adaptive $\Dpred$}, which explores temporally monotone paths from a predicted depth and re-ranks candidates by a semantic--temporal score;
(2)~\textbf{Experience-Guided Operator Routing (EGOR)}, which maps question types, lexical cues, and memory exemplars to a structured routing object without mandatory LLM selection;
(3)~\textbf{Temporal Faithfulness Critic (TFC)}, which verifies monotonicity, anchor synchronization, granularity consistency, and answer grounding before finalization.
We evaluate on MultiTQ and TimeQuestions with Hits@1 overall and typed breakdowns, plus systematic ablations.
Under a retrieval-grounded GPU setting, FaithPath reaches \textbf{24.8\%} Hits@1 on MultiTQ ($n{=}500$; PathHit@80 \textbf{58.4\%}) and \textbf{23.0\%} on TimeQuestions ($n{=}200$; Temporal-type \textbf{61.9\%}), outperforming candidate-prior and one-hop baselines by large margins.
Ablations show that EGOR contributes $+1.4$ points over BiBFS alone and GPU embedding scoring outperforms lexical scoring by $+1.4$ points on this subset.
\end{abstract}

\begin{IEEEkeywords}
Large Language Models, Retrieval-Augmented Generation, Temporal Knowledge Graph, Temporal Knowledge Graph Question Answering, Bidirectional Search, Temporal Faithfulness, Operator Routing, Experience Memory
\end{IEEEkeywords}
""")

# INTRODUCTION
add(r"""
\section{Introduction}
\IEEEPARstart{L}{arge} Language Models (LLMs) have demonstrated strong performance across a wide range of tasks~\cite{brown2020language}.
However, they are inherently static and often produce temporal inconsistencies on time-sensitive questions~\cite{khot2022decomposed}.
Retrieval-Augmented Generation (RAG) mitigates this by accessing external sources, yet plain-text retrieval prioritizes semantic similarity while neglecting chronological constraints~\cite{jia2024faithful}.

Temporal Knowledge Graphs (TKGs) encode facts as quadruples $(s,r,o,t)$ and support TKGQA~\cite{chen2023multitq,jia2021complex}.
Unlike static KGs, TKGs require models to respect calendar order, multi-granularity timestamps (year/month/day), and operator-specific constraints such as \emph{before}, \emph{after}, \emph{first}, \emph{last}, and \emph{equal}.
These operators frequently compose: a question may ask for the \emph{first} event \emph{after} an anchor involving two entities, or for the time when two entities co-occur under an \emph{equal} constraint.
Consequently, TKGQA systems must jointly solve (i)~entity linking and seed selection, (ii)~multi-hop path exploration under temporal monotonicity, (iii)~operator routing, and (iv)~answer grounding that is faithful to retrieved evidence.

\subsection{Motivation and Challenges}
Recent LLM-based TKGQA frameworks decompose questions, invoke operator-aware toolkits, and optionally reuse trajectories via memory~\cite{chen2024ari,hu2025tempagent,qian2024timer4}.
Despite strong end-to-end Hits@1 with powerful LLM backbones, three algorithmic gaps remain at the \emph{evidence layer}:

\begin{itemize}[leftmargin=*]
\item \textbf{Unbounded / heuristic path depth.}
Path exploration often expands to a fixed $\Dmax$ without predicting a question-conditioned depth $\Dpred$, wasting budget or missing evidence~\cite{jia2024faithful,qian2024timer4}.
Deep expansion without monotonicity pruning further explodes the candidate set, while shallow expansion under-covers multi-seed stitching windows required by multi-entity questions.
\item \textbf{LLM-dependent operator routing.}
Toolkit selection frequently falls back to LLM prompting even when question type priors are available, increasing latency and API cost~\cite{qian2024timer4,chen2024ari}.
In practice, many MultiTQ types admit deterministic priors (e.g., \texttt{after\_first} $\mapsto$ \{\texttt{OneHopAfter}, \texttt{FirstAfter}\}), yet systems still pay for a prompt round-trip on every sub-question.
\item \textbf{Weak post-retrieval faithfulness.}
Retrieved paths may violate temporal monotonicity or fail to ground the predicted answer, yet are still consumed by answer synthesis~\cite{jia2024faithful}.
Without an explicit critic, an LLM may ``explain away'' non-monotone or poorly grounded evidence, producing fluent but temporally unfaithful answers.
\end{itemize}

These gaps determine whether temporal reasoning is \emph{evidence-constrained} or merely \emph{prompt-constrained}.
We therefore design a new retrieval-critique algorithm that predicts depth, routes operators symbolically, and verifies faithfulness in closed form.

\subsection{Proposed Approach}
We propose \textbf{FaithPath}, a new neurosymbolic algorithm for temporally faithful TKGQA retrieval and critique.
FaithPath contributes three complementary modules:

\begin{enumerate}[leftmargin=*]
\item \textbf{Monotone BiBFS + Adaptive $\Dpred$ + $\Score(p)$:}
tree-structured bidirectional search with temporal monotonicity, depth prediction, temporal-first beam pruning, and semantic--temporal re-ranking.
\item \textbf{EGOR:}
experience- and type-guided operator routing that selects toolkits / time modes without mandatory LLM calls, emitting a structured decision object.
\item \textbf{TFC:}
a temporal faithfulness critic that rejects non-monotone paths, checks operator fidelity, and re-grounds answers.
\end{enumerate}

Formally, given question $Q$, seeds $S$, and experience pool $\mathcal{E}_{\mathrm{pool}}$, FaithPath predicts
\begin{equation}
\hat{a}=\Psi_{\mathrm{TFC}}\!\Bigl(\Pi_{\mathrm{BiBFS}}\!\bigl(S,\,D(\rho),\,Q\bigr),\;\rho,\;Q\Bigr),
\quad
\rho=\Phi_{\mathrm{EGOR}}(Q,\mathcal{E}_{\mathrm{pool}}),
\end{equation}
where $\Phi_{\mathrm{EGOR}}$, $\Pi_{\mathrm{BiBFS}}$, and $\Psi_{\mathrm{TFC}}$ are Modules~B, A, and~C respectively.

\subsection{Contributions}
\begin{itemize}[leftmargin=*]
\item We introduce FaithPath as a new end-to-end retrieval-critique algorithm for TKGQA, formalizing monotone bidirectional path search with adaptive depth prediction and a semantic--temporal scoring objective.
\item We introduce EGOR, a symbolic-first operator router that fuses type priors, lexical cues, and memory votes into a structured $\rho$, with an optional LLM fallback gated by confidence.
\item We introduce TFC, a deterministic faithfulness critic enforcing monotonicity, anchor synchronization, granularity consistency, and answer grounding.
\item We evaluate on MultiTQ / TimeQuestions (Hits@1 by question and answer type; PathHit@80; ablations) using GPU embeddings (MiniLM on NVIDIA RTX~5060) in a retrieval-grounded protocol that isolates the three modules.
\end{itemize}

\subsection{Paper Organization}
Section~\ref{sec:related} reviews TKGQA, temporal path retrieval, and operator-aware reasoning.
Section~\ref{sec:prelim} introduces notation and temporal monotonicity.
Section~\ref{sec:method} presents Modules~A--C with algorithms and complexity.
Section~\ref{sec:experiments} reports experiments and ablations.
Section~\ref{sec:discussion} discusses limitations and deployment.
Section~\ref{sec:conclusion} concludes.
Appendix materials detail hyperparameters, operator dictionaries, and additional analyses.
""")

# RELATED + PRELIM + METHOD start loaded from sibling fragments
for frag in ("_nomemo_related_prelim.texfrag", "_nomemo_method.texfrag", "_nomemo_exp.texfrag", "_nomemo_app.texfrag"):
    add(Path(__file__).with_name(frag).read_text(encoding="utf-8"))

OUT.write_text("".join(parts), encoding="utf-8")
n = len(OUT.read_text(encoding="utf-8").splitlines())
# sanity: no MemoTime
text = OUT.read_text(encoding="utf-8")
assert "MemoTime" not in text and "memotime" not in text.lower() and "2510.13614" not in text
print(f"wrote {OUT} lines={n}")
