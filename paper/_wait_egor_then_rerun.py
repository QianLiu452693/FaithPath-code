"""After first egor pilot finishes, rerun n=200 with fixed prompts (--compact)."""
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = ROOT / "results/paper/.egor_pilot_v2_done"


def main():
    time.sleep(120)
    for _ in range(120):
        src = ROOT / "results/paper/egor_llm_select_pilot_n200.json"
        if src.is_file():
            data = json.loads(src.read_text(encoding="utf-8"))
            if data.get("wall_sec", 0) > 60 and data.get("n_fail", 200) < 200:
                break
        time.sleep(30)
    subprocess.check_call(
        ["python", str(ROOT / "paper/run_egor_llm_select_pilot.py"), "--n", "200", "--compact"],
        cwd=str(ROOT),
    )
    MARKER.write_text("ok", encoding="utf-8")


if __name__ == "__main__":
    main()
