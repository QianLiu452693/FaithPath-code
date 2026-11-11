import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "results/paper/comparison_20261108_195018/failure_buckets_n500.json"
d = json.loads(p.read_text(encoding="utf-8"))
for bucket in ("selection_gap", "evidence_miss", "correct"):
    sub = [a for a in d["annotations"] if a["bucket"] == bucket]
    m = sum(1 for a in sub if a["qlabel"] == "Multiple")
    n = len(sub)
    print(bucket, n, "Multiple%", round(100 * m / n, 1) if n else 0)
