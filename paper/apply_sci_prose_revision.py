#!/usr/bin/env python3
"""SCI-style prose: experiment rationale, where-clauses, fewer itemize."""
from pathlib import Path

TEX = Path(__file__).resolve().parent / "FaithPath_IEEEtran.tex"
t = TEX.read_text(encoding="utf-8")

# --- fixes ---
t = t.replace("a 	extbf{conditional", "a \\textbf{conditional")
t = t.replace(
    "On MultiTQ full test, B2 exceeds FULL; we treat this as a central empirical finding, not a footnote.",
    "Full-test comparisons (Table~\\ref{tab:scale}) are used to stress-test ranking and proximity choices under matched PathHit, not to declare a single ``winning'' variant.",
)

# --- Introduction challenges: itemize -> prose ---
old_ch = r"""\begin{itemize}[leftmargin=*]
\item \textbf{Unbounded / heuristic path depth.}
Path exploration often expands to a fixed $\Dmax$ without predicting a question-conditioned depth $\Dpred$, wasting budget or missing evidence~\cite{jia2024faithful,qian2024timer4}.
Deep expansion without monotonicity pruning further explodes the candidate set, while shallow expansion under-covers multi-seed stitching windows required by multi-entity questions.
\item \textbf{LLM-dependent operator routing.}
Toolkit selection frequently falls back to LLM prompting even when question type priors are available, increasing latency and API cost~\cite{qian2024timer4,chen2024ari}.
In practice, many MultiTQ types admit deterministic priors (e.g., \texttt{after\_first} $\mapsto$ \{\texttt{OneHopAfter}, \texttt{FirstAfter}\}), yet systems still pay for a prompt round-trip on every sub-question.
\item \textbf{Weak post-retrieval faithfulness.}
Retrieved paths may violate temporal monotonicity or fail to ground the predicted answer, yet are still consumed by answer synthesis~\cite{jia2024faithful}.
Without an explicit critic, an LLM may ``explain away'' non-monotone or poorly grounded evidence, producing fluent but temporally unfaithful answers.
\end{itemize}"""
new_ch = r"""First, path depth is often fixed at $\Dmax$ rather than conditioned on the question, which either wastes expansion budget or misses multi-seed stitches~\cite{jia2024faithful,qian2024timer4}.
Second, operator routing still defaults to LLM toolkits although MultiTQ types admit stable priors (e.g., \texttt{after\_first} $\mapsto$ \{\texttt{OneHopAfter}, \texttt{FirstAfter}\}), incurring latency without guaranteed gain~\cite{qian2024timer4,chen2024ari}.
Third, retrieved paths can violate monotonicity or fail to ground the emitted answer, yet downstream synthesis may still consume them~\cite{jia2024faithful}; without an explicit verifier, fluent but temporally inconsistent answers are difficult to detect."""
if old_ch in t:
    t = t.replace(old_ch, new_ch)

# --- Contributions ---
old_c = r"""\subsection{Contributions}
\begin{itemize}[leftmargin=*]
\item \textbf{\FaithPath{} method:} monotone BiBFS with adaptive $\Dpred$, EGOR symbolic routing, and TFC path-level critique as a named, ablatable retrieval--critique stack for TKGQA.
\item \textbf{\ELDB{} diagnosis:} quantify that retrieval often recalls gold evidence (PathHit) while weak extraction fails (Hits@1), making selection---not only retrieval---the dominant failure mode.
\item \textbf{Counterintuitive tradeoff:} show B2 $>$ FULL on MultiTQ full test and localize the gap; controlled ablations separate temporal-first pruning from proximity scoring.
\item \textbf{Robustness:} report seed-noise degradation curves ($\eta\in\{0.1,0.2,0.3\}$) under the same protocol.
\item \textbf{Reliability gates:} PathHit and TFC score define abstention policies that improve answered accuracy under coverage constraints (Table~\ref{tab:reliability_gates}); MEMO\_R aligns MemoTime retrieval with \ELDB{} (Table~\ref{tab:memo_proxy}).
\item \textbf{Benchmark artifact:} protocol-defined failure buckets on all $n{=}500$ MultiTQ questions (208 evidence miss / 168 selection gap under FULL) with released per-question annotations; PathHit@$k$ curves disentangle pool size (B1) from temporal-first FULL at fixed $k{=}80$.
\end{itemize}"""
new_c = r"""\subsection{Contributions}
We present \FaithPath{}, a retrieval--critique stack for TKGQA in which monotone BiBFS, symbolic EGOR routing, and TFC verification can be switched on or off without changing the evaluation harness.
We release \ELDB{}, a protocol that reports PathHit and Hits@1 jointly, tags each question into evidence-miss versus selection-gap buckets, and supports PathHit@$k$ sweeps so that recall numbers are not confounded by pool size.
Empirically, we characterize when temporal proximity scoring harms answer hit despite stable PathHit (controlled F\_noprox / B2 ablations and full-test comparisons in Tables~\ref{tab:diag}--\ref{tab:scale}), how seed noise degrades selection more than recall (Table~\ref{tab:diag}), and which abstention gates improve accuracy on the answered subset (Table~\ref{tab:reliability_gates}).
A MemoTime-aligned retrieval-only variant (MEMO\_R) is included to show that the protocol applies outside a single code path (Table~\ref{tab:memo_proxy})."""
if old_c in t:
    t = t.replace(old_c, new_c)

# --- Method intro enumerate ---
old_m = r"""\begin{enumerate}[leftmargin=*]
\item \textbf{Monotone BiBFS + Adaptive $\Dpred$ + $\Score(p)$:}
tree-structured bidirectional search with temporal monotonicity, depth prediction, temporal-first beam pruning, and semantic--temporal re-ranking.
\item \textbf{EGOR:}
LLM-optional symbolic routing to a structured $\rho$ (type, operators, depth prior, time mode, selection).
\item \textbf{TFC:}
a path-level faithfulness filter (monotonicity, anchors, grounding), not an answer-correctness oracle.
\end{enumerate}"""
new_m = r"""Module~A (BiBFS) performs monotone path expansion with adaptive depth $\Dpred$, temporal-first beam pruning, and semantic--temporal scoring $\Score(p)$.
Module~B (EGOR) maps the question to a routing record $\rho$ (type, operators, depth prior, time mode, selection) without requiring an LLM call when priors suffice.
Module~C (TFC) applies path-level predicates for monotonicity, anchors, and grounding; its output is a faithfulness signal rather than a guarantee of answer correctness."""
if old_m in t:
    t = t.replace(old_m, new_m)

# --- Design principles ---
old_dp = r"""\subsection{Design Principles}
\begin{enumerate}[leftmargin=*]
\item \textbf{Temporal first.} Monotonicity and proximity prune before semantic scoring.
\item \textbf{Symbolic when possible.} Operator routing and faithfulness checks are deterministic when confidence is high.
\item \textbf{Multi-seed aware.} Candidate length windows scale with $|S|$ and depth $D$; $W_1{=}80$ retains a broad evidence set for PathHit analysis.
\item \textbf{API-light evaluation.} Retrieval-grounded Hits@1 isolates Modules~A--C without cloud LLMs.
\end{enumerate}"""
new_dp = r"""\subsection{Design Principles}
Paths are pruned for temporal monotonicity and proximity before semantic re-ranking, so chronological constraints are not an afterthought.
Operator routing and faithfulness checks are symbolic whenever confidence from type priors or memory is high, reserving LLM fallbacks for low-confidence cases.
Length windows $\mathcal{C}_D(S)$ scale with the number of seeds and depth $D$, and the top-$W_1$ list ($W_1{=}80$) is kept wide enough to measure PathHit without collapsing the analysis to a single path.
All module ablations share a retrieval-grounded extractor so that cloud LLMs do not obscure the effect of retrieval and verification."""
if old_dp in t:
    t = t.replace(old_dp, new_dp)

# --- Experiments intro + objectives ---
old_exp = r"""\section{Experiments}
\label{sec:experiments}

We evaluate FaithPath on two challenging TKGQA datasets.
We report Hits@1 overall and typed breakdowns, plus ablations.
Defaults: $\Dmax{=}3$, $W_1{=}80$, hybrid DRM+proximity scoring, experience memory available.
GPU: NVIDIA GeForce RTX~5060; embeddings: MiniLM on CUDA.

\paragraph{Evaluation protocol (important).}"""
new_exp = r"""\section{Experiments}
\label{sec:experiments}

Experiments are designed to answer four questions that a knowledge-system paper must separate explicitly: whether gold evidence is retrieved (PathHit), whether a fixed extractor turns that evidence into a correct answer (Hits@1), which architectural knob moves each quantity, and whether verification signals support abstention before a downstream decision module fires.
We therefore hold the answer extractor constant (path tail or end time; Eq.~\eqref{eq:extract}) and change only retrieval, routing, and critique components.
MultiTQ and TimeQuestions are used because they expose complementary operator and granularity structure; a prefix of $n{=}500$ / $n{=}200$ supports controlled ablations, while official full tests check that prefix trends are not sampling artefacts.
All FaithPath variants use $\Dmax{=}3$, $W_1{=}80$, hybrid DRM+proximity scoring unless a row states otherwise; embeddings come from MiniLM on an NVIDIA RTX~5060 (CUDA).

\subsection{Experimental objectives and protocol}
The \emph{weak-prior block} (B0, B1) establishes how much signal lies in entity linking alone versus one-hop lexical recall, isolating whether KG traversal is necessary.
The \emph{module ladder} (A1$\rightarrow$FULL) tests whether EGOR routing and TFC verification change Hits@1 or PathHit when BiBFS is held fixed.
The \emph{peer block} (B2, B3) places FaithPath next to embedding multi-hop retrieval and an untrained EXAQT-style subgraph filter under identical seeds and metrics, clarifying whether gains are specific to temporal-first BiBFS or generic to strong retrieval.
The \emph{scale block} repeats selected variants on full MultiTQ ($n{=}54{,}584$) and TimeQuestions ($n{=}3237$) to obtain paired bootstrap intervals on Hits@1 where prefix $n{=}500$ would be under-powered (e.g., EGOR).
The \emph{reliability block} (Section~\ref{sec:reliability}) evaluates abstention policies because TFC is intended as a gate, not a Hits@1 booster under the weak extractor.
Finally, \emph{seed-noise injections} (SN$\eta$ in Table~\ref{tab:diag}) stress linking quality to separate evidence loss from selection loss.

\paragraph{Reporting convention.}"""
if old_exp in t:
    t = t.replace(old_exp, new_exp)
    t = t.replace(
        "\\paragraph{Evaluation protocol (important).}",
        "\\paragraph{Reporting convention.}",
        1,
    )

# --- datasets itemize ---
old_ds = r"""We avoid CronQuestions due to spurious correlations~\cite{sharma2022twirgcn,qian2024timer4} and evaluate on:
\begin{itemize}[leftmargin=*]
\item \textbf{MultiTQ}~\cite{chen2023multitq}: ICEWS05--15; year/month/day; operators before/after/equal/first/last; Multiple vs.\ Single; Entity vs.\ Time.
\item \textbf{TimeQuestions}~\cite{jia2021complex}: Explicit / Implicit / Temporal / Ordinal; yearly granularity.
\end{itemize}"""
new_ds = r"""Following prior critique of spurious temporal shortcuts on CronQuestions~\cite{sharma2022twirgcn,qian2024timer4}, we evaluate on MultiTQ~\cite{chen2023multitq} (ICEWS05--15, multi-granularity timestamps, compositional operators, Multiple/Single and Entity/Time splits) and TimeQuestions~\cite{jia2021complex} (Explicit/Implicit/Temporal/Ordinal categories at yearly granularity)."""
if old_ds in t:
    t = t.replace(old_ds, new_ds)

# --- baselines itemize -> prose ---
old_bl = r"""FaithPath-internal retrieval variants:
\begin{itemize}[leftmargin=*]
\item \textbf{B0 CandidatePrior:} top-1 entity candidate (no KG walk).
\item \textbf{B1 OneHopLexical:} 1-hop neighbors + lexical overlap.
\item \textbf{B2 EmbedMHOP:} embedding-scored multi-hop retrieval ($D_{\max}{=}2$) \emph{without} temporal-first beam prune or proximity term (stronger retrieval-only peer).
\item \textbf{B3 EXAQT-proxy:} untrained EXAQT-inspired compact seed subgraph $+$ MiniLM fact--question relevance filter (same seeds/extractor; \emph{not} trained GST/R-GCN EXAQT).
\item \textbf{A1:} BiBFS only.
\item \textbf{A2:} BiBFS+EGOR.
\item \textbf{A3:} BiBFS+TFC.
\item \textbf{FULL:} BiBFS+EGOR+TFC.
\item \textbf{H1/H2/H3:} FULL with $D_{\max}\in\{1,2,3\}$.
\item \textbf{S1/S2:} FULL with lexical vs.\ GPU embedding Score$(p)$.
\end{itemize}"""
new_bl = r"""Internal variants are named to match the experimental objectives above.
B0 takes the top candidate entity without walking the graph; B1 scores one-hop neighbors lexically.
B2 performs embedding-based multi-hop expansion ($D_{\max}{=}2$) without temporal-first pruning or proximity, serving as a strong non-FaithPath retrieval peer.
B3 builds a compact seed subgraph and filters facts with MiniLM, mimicking the retrieval stage of EXAQT~\cite{jia2021complex} without trained GST/R-GCN components.
A1--A3 add BiBFS, EGOR, and TFC in sequence; FULL is the complete stack.
H1--H3 vary $D_{\max}\in\{1,2,3\}$; S1/S2 swap lexical versus GPU semantic scoring in $\Score(p)$."""
if old_bl in t:
    t = t.replace(old_bl, new_bl)

# --- equation where clauses (after selected labels) ---
where_score = r"""
where $\mathrm{DRM}(I,p)\in[0,1]$ is dense relevance between question $I$ and path text $\mathrm{txt}(p)$ (Eq.~\eqref{eq:drm}), $\pi(p)\in(0,1]$ is a proximity factor with scale $\sigma$ in days, $\lambda_{\mathrm{sem}}$ and $\lambda_{\mathrm{prox}}$ are convex weights with $\lambda_{\mathrm{sem}}+\lambda_{\mathrm{prox}}=1$, and $\Score(p)$ ranks candidates for the top-$W_1$ cut.
Eq.~\eqref{eq:score} is used because TKGQA retrieval must trade semantic match against calendar closeness when questions anchor on a date or event."""

if "Eq.~\\eqref{eq:score} is used because" not in t:
    t = t.replace(
        "subject to $\\lambda_{\\mathrm{sem}}+\\lambda_{\\mathrm{prox}}=1$ (defaults $0.6/0.4$, $\\sigma=365$).\n"
        "When GPU embeddings are unavailable, replace DRM by Lex in \\eqref{eq:score}.",
        "subject to $\\lambda_{\\mathrm{sem}}+\\lambda_{\\mathrm{prox}}=1$ (defaults $0.6/0.4$, $\\sigma=365$)."
        + where_score
        + "\nWhen GPU embeddings are unavailable, replace DRM by Lex in \\eqref{eq:score}.",
    )

where_rho = r"""
where $\tau$ is the predicted question type, $\mathcal{O}$ the operator bundle consumed by the toolkit mapper, $d_\rho$ a depth prior fed into $\Dpred$, $m_{\mathrm{time}}$ the anchor mode (before/after/equal/range), $\mathrm{sel}$ the first/last policy for time answers, and $c\in[0,1]$ the fused routing confidence.
Eq.~\eqref{eq:rho} is introduced so that BiBFS and TFC read the same structured record rather than duplicating heuristic rules in each module."""

if "Eq.~\\eqref{eq:rho} is introduced so" not in t:
    t = t.replace(
        "where $\\tau$ is the temporal type, $\\mathcal{O}=\\{o_1,\\ldots,o_k\\}$ an ordered operator bundle,\n"
        "$d_\\rho$ a depth prior, $m_{\\mathrm{time}}$ a time mode, $\\mathrm{sel}$ a selection policy, and $c\\in[0,1]$ confidence.",
        where_rho.strip(),
    )

# prelim eq:tkg
if "where $(s,r,o,t)$ denotes" not in t:
    t = t.replace(
        "Entities $\\mathcal{E}$ and relations $\\mathcal{R}$ may be typed; timestamps $\\mathcal{T}$ may be strings at year/month/day granularity.",
        "where $(s,r,o,t)$ denotes subject, relation, object, and timestamp of an observed fact, "
        "$\\mathcal{E}$ and $\\mathcal{R}$ are entity and relation vocabularies, and $\\mathcal{T}$ stores time strings at year/month/day granularity.",
    )

# fix appendix verbatim
bad_verbatim = r"""    P_raw = monotone_bibfs(G, S, D
    , rho) # Module A"""
if bad_verbatim in t:
    t = t.replace(bad_verbatim, "    P_raw = monotone_bibfs(G, S, D, rho)  # Module A")
t = t.replace("    a_hat, faithful = tfc(P_star, \n    rho, Q)# Module C", "    a_hat, faithful = tfc(P_star, rho, Q)  # Module C")

TEX.write_text(t, encoding="utf-8")
print("Updated", TEX)
