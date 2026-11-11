"""Static cross-ref and float-order check for FaithPath_IEEEtran.tex"""
import re
from pathlib import Path

TEX = Path(__file__).parent / "FaithPath_IEEEtran.tex"
text = TEX.read_text(encoding="utf-8")
lines = text.splitlines()

labels: dict[str, int] = {}
for i, line in enumerate(lines, 1):
    for m in re.finditer(r"\\label\{([^}]+)\}", line):
        key = m.group(1)
        if key in labels:
            print(f"DUPLICATE label {key!r}: L{labels[key]} and L{i}")
        labels[key] = i

refs: list[tuple[int, str]] = []
for i, line in enumerate(lines, 1):
    for m in re.finditer(r"\\(?:ref|eqref|pageref)\{([^}]+)\}", line):
        refs.append((i, m.group(1)))

missing = sorted({k for _, k in refs if k not in labels})
print(f"Labels: {len(labels)}  Refs: {len(refs)}  Unique refs: {len(set(k for _, k in refs))}")
if missing:
    print("Missing labels:")
    for k in missing:
        first = next(i for i, kk in refs if kk == k)
        print(f"  {k} (first ref L{first})")
else:
    print("OK: all \\ref keys have \\label")

appendix_line = next((i for i, L in enumerate(lines, 1) if r"\appendix" in L), None)
main_refs_appendix_tables = [
    (i, k)
    for i, k in refs
    if k in ("tab:lit_mt", "tab:lit_tq", "tab:llm_pilot")
    and (appendix_line is None or i < appendix_line)
]
if main_refs_appendix_tables:
    print("Main-body refs to appendix-only floats:")
    for i, k in main_refs_appendix_tables:
        print(f"  L{i} \\ref{{{k}}}")

for key in ("tab:lit_mt", "tab:lit_tq", "tab:llm_pilot", "eq:pathhit", "app:lit_context", "app:llm_pilot"):
  def_ln = labels.get(key)
  if def_ln:
      first_ref = min((i for i, k in refs if k == key), default=None)
      print(f"{key}: label L{def_ln}, first ref L{first_ref}")

bad = [i for i, line in enumerate(lines, 1) if "sec:llm_pilot" in line]
if bad:
    print("sec:llm_pilot still present at lines:", bad)

# Figure assets
figs = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)
missing_figs = [f for f in set(figs) if not (TEX.parent / f).exists() and not (TEX.parent.parent / f).exists()]
if missing_figs:
    print("Missing includegraphics files:")
    for f in sorted(missing_figs):
        print(f"  {f}")
else:
    print(f"OK: all {len(set(figs))} figure paths exist")

# Main-text float order (before \\appendix)
main_end = appendix_line or len(lines)
key_floats = ("tab:reliability_gates", "tab:t4", "tab:oracle_gap", "fig:pathhit_k", "tab:diag")
print("\nMain-body first ref vs label (appendix floats may forward-ref):")
for key in key_floats:
    def_ln = labels.get(key)
    main_refs = [i for i, k in refs if k == key and i < main_end]
    if not def_ln and not main_refs:
        continue
    first_ref = min(main_refs) if main_refs else None
    loc = "appendix" if def_ln and def_ln > main_end else "main"
    warn = ""
    if def_ln and first_ref and first_ref < def_ln and def_ln <= main_end:
        warn = " [WARN: ref before label in main]"
    print(f"  {key}: label L{def_ln} ({loc}), first main ref L{first_ref}{warn}")
