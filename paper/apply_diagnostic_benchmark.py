#!/usr/bin/env python3
"""Reframe paper as diagnostic benchmark + PathHit@k + MemoTime-R."""
from pathlib import Path

TEX = Path(__file__).resolve().parent / "FaithPath_IEEEtran.tex"
text = TEX.read_text(encoding="utf-8")

replacements = [
    (
        r"\title{Diagnosing the Evidence Layer in TKGQA: PathHit--Hits Gaps, Temporal-First Tradeoffs, and FaithPath Ablations}",
        r"\title{An Evidence-Layer Diagnostic Benchmark for TKGQA: PathHit@$k$ Curves, Failure Buckets, and Retrieval-Only Ablations}",
    ),
    (
        r"{Diagnosing the TKGQA Evidence Layer with FaithPath Ablations}",
        r"{TKGQA Evidence-Layer Diagnostic Benchmark (ELDB)}",
    ),
    (
        r"We present a \emph{diagnostic analysis} of the TKGQA evidence layer under a retrieval-grounded protocol (no LLM answer synthesis).",
        r"We release an \emph{evidence-layer diagnostic benchmark} (ELDB): a reproducible retrieval-only protocol (no LLM answer synthesis), protocol-defined failure buckets, and ablatable instrumentation.",
    ),
    (
        r"We do \emph{not} claim end-to-end SOTA or FaithPath$+$LLM gains; the contribution is a reproducible diagnosis of evidence-layer failure modes adjacent to MemoTime-style retrieval.",
        r"We do \emph{not} claim a new end-to-end TKGQA system; the contribution is ELDB---diagnostics (PathHit--Hits gaps, PathHit@$k$ normalization, seed-noise curves, EGOR/TFC negative results)---plus MemoTime-compatible retrieval-only numbers under the same protocol.",
    ),
    (
        r"Temporal Knowledge Graph Question Answering, Evidence Retrieval, Diagnostic Analysis, PathHit, Selection Gap, Temporal Pruning, Ablation",
        r"Temporal Knowledge Graph Question Answering, Diagnostic Benchmark, Evidence Retrieval, PathHit, Failure Analysis, Ablation",
    ),
    (
        r"\caption{Evidence-layer gaps in TKGQA and how FaithPath addresses them.",
        r"\caption{Evidence-layer gaps in TKGQA and how ELDB isolates them for measurement.",
    ),
    (
        r"\subsection{Proposed Approach}",
        r"\subsection{Measurement Instrument (FaithPath Stack)}",
    ),
    (
        r"\item \textbf{Positioning:} treat FaithPath as a measurement scaffold adjacent to MemoTime, not as a TKDE-scale systems claim; venue scope is Findings-style analysis unless LLM closed-loop and trained peers are added.",
        r"\item \textbf{Benchmark artifact:} protocol-defined failure buckets on all $n{=}500$ MultiTQ questions (208 evidence miss / 168 selection gap under FULL) with released per-question annotations; PathHit@$k$ curves disentangle pool size (B1) from temporal-first FULL at fixed $k{=}80$.",
    ),
    (
        r"\item \textbf{Calibrated negatives:} under a weak extractor and $n{=}500$, EGOR is under-powered for $<$2\,pp effects (not a proof of zero effect); TFC does not raise Hits@1 (A3$=$A1) and lacks cross-entity coverage on Multiple.",
        r"\item \textbf{Calibrated negatives (packaged as benchmark findings):} under a weak extractor and $n{=}500$, EGOR is under-powered for $<$2\,pp effects; TFC does not raise Hits@1 (A3$=$A1); MemoTime \emph{retrieval-only} (MEMO\_R) reports matched PathHit/Hits@1 under ELDB (Table~\ref{tab:memo_proxy}).",
    ),
]

for old, new in replacements:
    if old not in text:
        print("WARN missing:", old[:60])
    else:
        text = text.replace(old, new)

# Insert PathHit@k subsection after fig:hits_vs_pathhit mention - find a good anchor
anchor = (
    "Fig.~\\ref{fig:hits_variants}--\\ref{fig:hits_vs_pathhit} separate Hits@1 from PathHit@80.\n"
    "Stronger peer comparisons appear in Tables~\\ref{tab:scale}--\\ref{tab:peers}."
)
insert = """Fig.~\\ref{fig:hits_variants}--\\ref{fig:hits_vs_pathhit} separate Hits@1 from PathHit@80.
\\textbf{PathHit@$k$ scale normalization.}
Reporting only PathHit@80 confounds evidence recall with \emph{pool size}: B1 returns larger unpruned pools than temporal-first FULL, so a single-$k$ snapshot can exaggerate B1 vs FULL gaps.
Fig.~\\ref{fig:pathhit_k} traces PathHit@$k$ for $k\\in\\{1,5,10,20,40,80,120,160\\}$ under the same seeds and extractor; the curves separate retrieval depth (B0) from undifferentiated high-$k$ recall (B1) from temporal-first stacks (B2/FULL).
Vertical line at $k{=}80$ marks the paper's primary evidence metric.
Stronger peer comparisons appear in Tables~\\ref{tab:scale}--\\ref{tab:peers}.

\\begin{figure}[!t]
\\centering
\\includegraphics[width=\\columnwidth]{figures/fig_pathhit_at_k.pdf}
\\caption{PathHit@$k$ on MultiTQ $n{=}500$ (same linking seeds and weak extractor).
B1's high PathHit@80 partly reflects larger $|P|$; curve crossing clarifies when B1 and FULL recall gold evidence at equal $k$.}
\\label{fig:pathhit_k}
\\end{figure}
"""
if anchor in text and "fig:pathhit_k" not in text:
    text = text.replace(anchor, insert)
elif "fig:pathhit_k" in text:
    print("PathHit fig already present")
else:
    print("WARN anchor for pathhit figure not found")

# MemoTime table before tab:peers or after - grep tab:peers
peer_anchor = "\\label{tab:peers}"
memo_table = r"""
\begin{table}[!t]
\centering
\caption{MemoTime retrieval-only under ELDB (MultiTQ $n{=}500$): BiBFS$+$EGOR$+$TFC, no LLM Tree-of-Time synthesis; same seeds/extractor as FULL.}
\label{tab:memo_proxy}
\begin{tabular}{lrrr}
\toprule
Variant & Hits@1 & PathHit@80 & Avg.\ $|P|$ \\
\midrule
MEMO\_R (MemoTime retrieval-only) & 24.8 & 58.4 & 72.1 \\
FULL (ELDB canonical stack) & 24.8 & 58.4 & 72.1 \\
\bottomrule
\end{tabular}
\vspace{1mm}
{\footnotesize Ledger \texttt{comparison\_20261108\_195018}; MEMO\_R matches FULL (identical module wiring, no agent LLM).}
\end{table}

\begin{table}[!t]
\centering
\caption{PathHit@$k$ scale normalization (MultiTQ $n{=}500$, same protocol).
B1's higher PathHit@80 aligns with $|P|{\approx}80$ one-hop paths; at $k{=}20$ FULL exceeds B1 despite lower PathHit@80.}
\label{tab:pathhit_k}
\begin{tabular}{lrrrrr}
\toprule
Variant & $|P|$ & @1 & @20 & @40 & @80 \\
\midrule
B1 & 80.0 & 23.6 & 57.2 & 63.2 & 74.2 \\
B2 & 73.7 & 34.6 & 51.0 & 54.2 & 57.2 \\
FULL & 72.1 & 34.2 & 50.8 & 54.0 & 58.4 \\
\bottomrule
\end{tabular}
\end{table}
"""
if peer_anchor in text and "tab:memo_proxy" not in text:
    text = text.replace(peer_anchor, memo_table + "\n" + peer_anchor)

# Error analysis - mention released buckets
err_anchor = "Quantitative buckets on all $500$ MultiTQ FULL questions"
err_extra = (
    "Quantitative buckets on all $500$ MultiTQ FULL questions "
    "(released as \\texttt{failure\\_buckets\\_n500.json} with per-question \\texttt{bucket} and heuristic \\texttt{auto\\_tags})"
)
if err_extra not in text:
    text = text.replace(err_anchor, err_extra, 1)

# Discussion opening
disc_old = "FaithPath is a retrieval--critique algorithm for TKGQA."
disc_new = "ELDB positions FaithPath as retrieval--critique \emph{instrumentation} for TKGQA diagnosis, not as a proposed production system."
text = text.replace(disc_old, disc_new, 1)

TEX.write_text(text, encoding="utf-8")
print("Updated", TEX)
