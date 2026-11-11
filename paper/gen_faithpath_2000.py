# -*- coding: utf-8 -*-
"""Generate FaithPath_IEEEtran.tex expanded to ~2000 lines."""
from pathlib import Path

OUT = Path(__file__).with_name("FaithPath_IEEEtran.tex")
parts: list[str] = []


def add(s: str) -> None:
    parts.append(s.rstrip("\n") + "\n")


def sec_comment(title: str) -> None:
    add("")
    add("% " + "=" * 60)
    add(f"% {title}")
    add("% " + "=" * 60)


# ---------------------------------------------------------------------------
# PREAMBLE
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# ABSTRACT
# ---------------------------------------------------------------------------
sec_comment("ABSTRACT")
add(r"""
\begin{abstract}
Large Language Models (LLMs) have achieved impressive reasoning abilities, but struggle with temporal understanding, especially when questions involve multiple entities, compound operators, and evolving event sequences.
Temporal Knowledge Graphs (TKGs) offer structured temporal facts for TKGQA, yet existing TKG-based LLM reasoning methods---including memory-augmented frameworks such as MemoTime---still under-specify predicted exploration depth under temporal monotonicity, experience-guided operator routing without mandatory LLM calls, and post-hoc temporal faithfulness verification.
We propose \textbf{FaithPath}, a retrieval-centric enhancement with three breakthrough modules:
(1)~\textbf{Monotone BiBFS with Adaptive $\Dpred$}, which explores temporally monotone paths from a predicted depth and re-ranks candidates by a semantic--temporal score;
(2)~\textbf{Experience-Guided Operator Routing (EGOR)}, which maps question types and lexical cues to operator bundles without mandatory LLM selection;
(3)~\textbf{Temporal Faithfulness Critic (TFC)}, which verifies monotonicity, anchor synchronization, and answer grounding before finalization.
Following the experimental protocol of MemoTime, we evaluate on MultiTQ and TimeQuestions with Hits@1 overall and typed breakdowns, plus ablations aligned with MemoTime's Table~4 design.
Under a retrieval-grounded GPU setting, FaithPath reaches \textbf{24.8\%} Hits@1 on MultiTQ ($n{=}500$; PathHit@80 \textbf{58.4\%}) and \textbf{23.0\%} on TimeQuestions ($n{=}200$; Temporal-type \textbf{61.9\%}), outperforming candidate-prior and one-hop baselines by large margins.
Ablations confirm that EGOR contributes $+1.4$ points over BiBFS alone, and GPU embedding scoring outperforms lexical scoring by $+1.4$ points.
\end{abstract}

\begin{IEEEkeywords}
Large Language Models, Retrieval-Augmented Generation, Temporal Knowledge Graph, Temporal Knowledge Graph Question Answering, Memory-Augmented Retrieval-Augmented Generation, Bidirectional Search, Temporal Faithfulness
\end{IEEEkeywords}
""")

# ---------------------------------------------------------------------------
# INTRODUCTION
# ---------------------------------------------------------------------------
sec_comment("INTRODUCTION")
add(r"""
\section{Introduction}
\IEEEPARstart{L}{arge} Language Models (LLMs) have demonstrated strong performance across a wide range of tasks~\cite{brown2020language}.
However, they are inherently static and often produce temporal inconsistencies on time-sensitive questions~\cite{khot2022decomposed}.
Retrieval-Augmented Generation (RAG) mitigates this by accessing external sources, yet plain-text retrieval prioritizes semantic similarity while neglecting chronological constraints~\cite{jia2024faithful}.

Temporal Knowledge Graphs (TKGs) encode facts as quadruples $(s,r,o,t)$ and support Temporal Knowledge Graph Question Answering (TKGQA)~\cite{chen2023multitq,jia2021complex}.
Unlike static KGs, TKGs require models to respect calendar order, multi-granularity timestamps (year/month/day), and operator-specific constraints such as \emph{before}, \emph{after}, \emph{first}, \emph{last}, and \emph{equal}.
These operators frequently compose: a question may ask for the \emph{first} event \emph{after} an anchor involving two entities, or for the time when two entities co-occur under an \emph{equal} constraint.
Consequently, TKGQA systems must jointly solve (i)~entity linking and seed selection, (ii)~multi-hop path exploration under temporal monotonicity, (iii)~operator routing, and (iv)~answer grounding that is faithful to retrieved evidence.

\subsection{Motivation and Challenges}
Recent LLM-based TKGQA frameworks---notably MemoTime~\cite{tan2025memotime}---decompose questions into a hierarchical Tree of Time, invoke operator-aware toolkits, and reuse verified trajectories via experience memory.
Despite strong end-to-end Hits@1 with powerful LLM backbones, three retrieval-layer gaps remain:

\begin{itemize}[leftmargin=*]
\item \textbf{Unbounded / heuristic path depth.}
Path exploration often expands to a fixed $\Dmax$ without predicting a question-conditioned depth $\Dpred$, wasting budget or missing evidence~\cite{tan2025memotime,jia2024faithful}.
Deep expansion without monotonicity pruning further explodes the candidate set, while shallow expansion under-covers multi-seed stitching windows used by MemoTime-style retrieval.
\item \textbf{LLM-dependent operator routing.}
Toolkit selection frequently falls back to LLM prompting even when question type priors are available, increasing latency and API cost~\cite{qian2024timer4,chen2024ari}.
In practice, many MultiTQ types admit deterministic priors (e.g., \texttt{after\_first} $\mapsto$ \{\texttt{OneHopAfter}, \texttt{FirstAfter}\}), yet systems still pay for a prompt round-trip on every subtree.
\item \textbf{Weak post-retrieval faithfulness.}
Retrieved paths may violate temporal monotonicity or fail to ground the predicted answer, yet are still consumed by answer synthesis~\cite{jia2024faithful,tan2025memotime}.
Without an explicit critic, an LLM may ``explain away'' non-monotone or poorly grounded evidence, producing fluent but temporally unfaithful answers.
\end{itemize}

These gaps are not merely engineering details: they determine whether Tree-of-Time reasoning is \emph{evidence-constrained} or merely \emph{prompt-constrained}.
A retrieval stack that predicts depth, routes operators symbolically, and verifies faithfulness can reduce API cost, improve reproducibility, and provide a drop-in substrate for open-weight LLMs.

\subsection{Proposed Approach}
To address these issues, we propose \textbf{FaithPath}, a neurosymbolic retrieval stack that plugs into MemoTime-style Tree-of-Time pipelines~\cite{tan2025memotime}.
FaithPath contributes three complementary innovations:

\begin{enumerate}[leftmargin=*]
\item \textbf{Monotone BiBFS + Adaptive $\Dpred$ + $\Score(p)$:}
tree-structured bidirectional search with temporal monotonicity, depth prediction, temporal-first beam pruning, and semantic--temporal re-ranking.
\item \textbf{EGOR:}
experience- and type-guided operator routing that selects toolkits / time modes without mandatory LLM calls.
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
Our contributions are summarized as follows:
\begin{itemize}[leftmargin=*]
\item We formalize monotone bidirectional path search with adaptive depth prediction and a semantic--temporal scoring objective aligned with MemoTime's Score formula.
\item We introduce EGOR, a symbolic-first operator router that fuses type priors, lexical cues, and memory votes, with an optional LLM fallback gated by confidence.
\item We introduce TFC, a deterministic faithfulness critic enforcing monotonicity, anchor synchronization, and answer grounding.
\item We evaluate under the \emph{same datasets, metrics, and ablation taxonomy} as MemoTime~\cite{tan2025memotime} (MultiTQ / TimeQuestions; Hits@1 by question and answer type; Table~4-style ablations), using GPU embeddings (MiniLM on NVIDIA RTX~5060) in a retrieval-grounded protocol that isolates the three modules.
\end{itemize}

\subsection{Paper Organization}
Section~\ref{sec:related} reviews TKGQA, temporal path retrieval, and memory-augmented reasoning.
Section~\ref{sec:prelim} introduces notation and temporal monotonicity.
Section~\ref{sec:method} presents Modules~A--C with algorithms and complexity.
Section~\ref{sec:experiments} reports MemoTime-aligned experiments.
Section~\ref{sec:discussion} discusses limitations and deployment notes.
Section~\ref{sec:conclusion} concludes.
Appendix materials detail hyperparameters, operator dictionaries, and additional analyses.
""")

# ---------------------------------------------------------------------------
# RELATED WORK
# ---------------------------------------------------------------------------
sec_comment("RELATED WORK")
add(r"""
\section{Related Work}
\label{sec:related}

\subsection{Temporal Knowledge Graph Question Answering}
Early TKGQA methods embed entities/relations with temporal signals (e.g., CronKGQA~\cite{saxena2021cronkgqa}, TempoQR~\cite{mavromatis2022tempoqr}) or retrieve subgraphs (EXAQT~\cite{jia2021complex}, TwiRGCN~\cite{sharma2022twirgcn}).
MultiTQ~\cite{chen2023multitq} and TimeQuestions~\cite{jia2021complex} remain standard benchmarks; CronQuestions is often avoided due to spurious correlations~\cite{sharma2022twirgcn,qian2024timer4}.
Embedding-based systems excel on shallow patterns but struggle with compound operators and multi-entity synchronization.
LLM-augmented systems such as ARI~\cite{chen2024ari}, TempAgent~\cite{hu2025tempagent}, TimeR$^4$~\cite{qian2024timer4}, and MemoTime~\cite{tan2025memotime} improve multi-hop temporal reasoning via decomposition and tool use.
FaithPath focuses on the \emph{evidence retrieval and pruning} layer shared by these systems (MemoTime §4.3), treating LLM synthesis as an optional outer loop.

\subsection{Temporal Path Retrieval and Faithfulness}
Bidirectional search and temporal pruning appear in TKG reasoning~\cite{han2021xerte,liu2022tlogic}.
Path-based forecasting methods emphasize explainability through explicit edges and timestamps.
Faithfulness---ensuring answers are supported by temporally consistent evidence---has been emphasized in temporal QA over heterogeneous sources~\cite{jia2024faithful}.
Our TFC operationalizes faithfulness as verifiable constraints (monotonicity, anchors, grounding) before answer selection, rather than relying solely on LLM self-consistency.

\subsection{Memory-Augmented and Operator-Aware Reasoning}
Experience memory and exemplar retrieval improve stability in MemoTime~\cite{tan2025memotime}.
Related memory-RAG systems store successful trajectories and retrieve them as soft prompts.
EGOR specializes this idea for \emph{operator routing}: type priors, lexical cues, and memory exemplars jointly decide toolkits and $\Dpred$ bias, reducing LLM dependency.
Unlike generic memory that only conditions prompts, EGOR emits a structured decision $\rho$ consumed by BiBFS and TFC.

\subsection{Retrieval-Augmented Generation under Temporal Constraints}
Standard RAG ranks passages by dense similarity~\cite{brown2020language}.
Temporal RAG additionally requires calendar order and operator fidelity~\cite{jia2024faithful}.
FaithPath can be viewed as a structured temporal RAG front-end: instead of free-text chunks, it retrieves monotone TKG paths scored by DRM and proximity, then criticizes them before generation.
This design is complementary to Tree-of-Time: FaithPath supplies the grounded evidence that hierarchical LLM reasoners consume.

\subsection{Positioning Relative to MemoTime}
MemoTime provides hierarchical decomposition, toolkit invocation, and experience write-back~\cite{tan2025memotime}.
FaithPath does not replace Tree-of-Time; it hardens three under-specified retrieval behaviors into testable modules with closed-form equations, algorithms, and ablations.
When an LLM is available, FaithPath can sit beneath MemoTime as a drop-in retrieval substrate; when APIs are unavailable, FaithPath still yields retrieval-grounded Hits@1 and PathHit@$k$ for offline evaluation.
""")

# ---------------------------------------------------------------------------
# PRELIMINARIES
# ---------------------------------------------------------------------------
sec_comment("PRELIMINARIES")
add(r"""
\section{Preliminaries}
\label{sec:prelim}

\begin{definition}[Temporal Knowledge Graph]
A TKG is a tuple $\mathcal{G}=(\mathcal{E},\mathcal{R},\mathcal{T},\mathcal{F})$ where
\begin{equation}
\label{eq:tkg}
\mathcal{F}\subseteq\mathcal{E}\times\mathcal{R}\times\mathcal{E}\times\mathcal{T},\qquad
(s,r,o,t)\in\mathcal{F}.
\end{equation}
Entities $\mathcal{E}$ and relations $\mathcal{R}$ may be typed; timestamps $\mathcal{T}$ may be strings at year/month/day granularity.
\end{definition}

\begin{definition}[TKGQA]
Given question $Q$ and topic entities $Topics\subseteq\mathcal{E}$, predict answer $a^\star$ such that
\begin{equation}
\label{eq:tkgqa}
a^\star=\arg\max_{a\in\mathcal{A}(Q)}\,P\!\left(a\mid Q,\mathcal{G},Topics\right),
\end{equation}
where $\mathcal{A}(Q)$ is the answer space (entities and/or timestamps), consistent with prior TKGQA settings~\cite{tan2025memotime,chen2023multitq}.
\end{definition}

\begin{definition}[Temporal Path~\cite{tan2025memotime}]
A length-$\ell$ path is
\begin{equation}
\label{eq:path}
p=\bigl(e_0\xrightarrow{r_1,t_1}e_1\xrightarrow{r_2,t_2}\cdots\xrightarrow{r_\ell,t_\ell}e_\ell\bigr),
\end{equation}
with $(e_{i-1},r_i,e_i,t_i)\in\mathcal{F}$ for all $i\in\{1,\ldots,\ell\}$, satisfying connectivity and temporal monotonicity.
\end{definition}

\begin{definition}[Calendar Normalization]
Let $\kappa:\mathcal{T}\cup\{\varepsilon\}\!\to\!\mathbb{Z}_{\ge 0}\cup\{\infty\}$ map a timestamp string to an epoch key (missing $\varepsilon\mapsto\infty$).
The order on times is
\begin{equation}
\label{eq:time_le}
t\preceq t'\;\Longleftrightarrow\;\kappa(t)\le\kappa(t').
\end{equation}
We write $t\prec t'$ when $\kappa(t)<\kappa(t')$.
\end{definition}

\begin{definition}[Temporally Monotone Path]
Path $p$ in \eqref{eq:path} is monotone iff
\begin{equation}
\label{eq:mono}
\mathbb{I}_{\mathrm{mono}}(p)=\prod_{i=1}^{\ell-1}\ind\!\left[t_i\preceq t_{i+1}\right]=1.
\end{equation}
\end{definition}

\begin{definition}[Path Textualization]
Let $\mathrm{txt}(p)$ serialize edges of $p$ into a space-separated string of entities, relations, and timestamps for embedding and lexical matching.
\end{definition}

\begin{definition}[Operator Bundle]
An operator bundle $\mathcal{O}=\{o_1,\ldots,o_k\}$ is an ordered list of toolkit primitives (e.g., \texttt{OneHopAfter}, \texttt{FirstAfter}) associated with a temporal type $\tau$.
\end{definition}

\begin{assumption}[Seed Availability]
Topic entities / candidates yield a non-empty seed set $S\subseteq\mathcal{E}$ with $|S|\ge 1$.
If $|S|=1$, stitching degenerates to single-seed expansion.
\end{assumption}

\begin{proposition}[Monotonicity is Prefix-Closed]
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
\end{proof}

\begin{remark}
Temporal monotonicity is a necessary but not sufficient condition for operator faithfulness.
TFC further checks anchors and grounding (Section~\ref{sec:tfc}).
\end{remark}
""")

# ---------------------------------------------------------------------------
# METHOD OVERVIEW
# ---------------------------------------------------------------------------
sec_comment("THE PROPOSED FAITHPATH APPROACH")
add(r"""
\section{The Proposed FaithPath Approach}
\label{sec:method}

FaithPath augments MemoTime-style Tree-of-Time reasoning~\cite{tan2025memotime} with three mathematically specified modules (Fig.~\ref{fig:framework}):
\textbf{Module~A} Monotone BiBFS with Adaptive $\Dpred$;
\textbf{Module~B} EGOR;
\textbf{Module~C} TFC.
The end-to-end predictor is
\begin{equation}
\label{eq:pipeline}
\hat{a}=\Psi_{\mathrm{TFC}}\!\Bigl(\Pi_{\mathrm{BiBFS}}\!\bigl(S,\,D(\rho),\,Q\bigr),\;\rho,\;Q\Bigr),
\end{equation}
where $\rho=\Phi_{\mathrm{EGOR}}(Q,\mathcal{E}_{\mathrm{pool}})$ is the routing decision and $S$ are retrieval seeds.

\begin{figure*}[!t]
\centering
\begin{tikzpicture}[
  font=\small,
  box/.style={draw, rounded corners, align=center, inner sep=6pt, minimum height=1.1cm},
  arrow/.style={-{Latex}, thick}
]
\node[box, fill=blue!12, minimum width=2.6cm] (q) {Question $Q$\\+ Seeds $S$};
\node[box, fill=orange!18, minimum width=3.2cm, right=0.7cm of q] (egor) {\textbf{Module B: EGOR}\\$\Phi_{\mathrm{EGOR}}$};
\node[box, fill=green!15, minimum width=3.4cm, right=0.7cm of egor] (bibfs) {\textbf{Module A: BiBFS}\\$\Pi_{\mathrm{BiBFS}}$};
\node[box, fill=red!12, minimum width=3.0cm, right=0.7cm of bibfs] (tfc) {\textbf{Module C: TFC}\\$\Psi_{\mathrm{TFC}}$};
\node[box, fill=gray!15, minimum width=2.4cm, right=0.7cm of tfc] (ans) {Answer $\hat{a}$};
\draw[arrow] (q) -- (egor);
\draw[arrow] (egor) -- (bibfs);
\draw[arrow] (bibfs) -- (tfc);
\draw[arrow] (tfc) -- (ans);
\end{tikzpicture}
\caption{FaithPath pipeline composed of three innovation modules with operators $\Phi_{\mathrm{EGOR}}$, $\Pi_{\mathrm{BiBFS}}$, and $\Psi_{\mathrm{TFC}}$, compatible with MemoTime temporal grounding and experience memory~\cite{tan2025memotime}.}
\label{fig:framework}
\end{figure*}

\subsection{Design Principles}
We follow four design principles:
\begin{enumerate}[leftmargin=*]
\item \textbf{Temporal first.} Monotonicity and proximity prune before semantic scoring.
\item \textbf{Symbolic when possible.} Operator routing and faithfulness checks are deterministic when confidence is high.
\item \textbf{MemoTime-compatible.} Candidate length windows, $W_1{=}80$, and Score defaults match MemoTime~\cite{tan2025memotime}.
\item \textbf{API-light evaluation.} Retrieval-grounded Hits@1 isolates Modules~A--C without cloud LLMs.
\end{enumerate}
""")

print("lines so far approx", sum(p.count("\n") for p in parts))
OUT_PARTS = Path(__file__).with_name("_parts")
OUT_PARTS.mkdir(exist_ok=True)
(OUT_PARTS / "p1.texfrag").write_text("".join(parts), encoding="utf-8")
print("saved p1", sum(1 for _ in "".join(parts).splitlines()))
