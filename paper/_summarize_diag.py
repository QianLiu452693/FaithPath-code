import json
from pathlib import Path

d = Path(r"E:/cursor-code/TKG1/MemoTime-main/MemoTime-main/results/paper/comparison_20261108_180343")
rows = []
for p in sorted(d.glob("*.json")):
    if p.name == "leaderboard.json":
        continue
    data = json.loads(p.read_text(encoding="utf-8"))
    s = data["summary"]
    rows.append(s)
    print(f"{s['variant']:<10} Hits={s['overall_hits@1']:.2f} Path={s['path_hit@80']:.2f} sec={s['wall_sec']:.1f}")

lb = d / "leaderboard.json"
if lb.exists():
    L = json.loads(lb.read_text(encoding="utf-8"))
    print("\nPaired vs FULL:")
    for k, v in (L.get("paired_bootstrap_hits@1") or {}).items():
        vf = v.get("vs_FULL")
        if vf:
            print(k, vf)
