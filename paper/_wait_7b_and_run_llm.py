"""Wait for qwen2.5:7b in Ollama then run LLM answer-selection n=200."""
import json
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def has_7b() -> bool:
    tags = json.loads(urllib.request.urlopen("http://localhost:11434/api/tags", timeout=30).read())
    for m in tags.get("models", []):
        if "7b" in (m.get("name") or ""):
            return True
    return False


def main():
    for _ in range(240):
        if has_7b():
            break
        time.sleep(15)
    else:
        raise SystemExit("qwen2.5:7b not available after wait")
    subprocess.check_call(
        [
            "python",
            str(ROOT / "paper/run_llm_selection_experiment.py"),
            "--n",
            "200",
            "--model",
            "qwen2.5:7b",
            "--out",
            "results/paper/llm_selection_n200_7b.json",
        ],
        cwd=str(ROOT),
    )


if __name__ == "__main__":
    main()
