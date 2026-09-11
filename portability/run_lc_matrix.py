"""run_lc_matrix.py — cross-harness portability driver (LangChain leg).

Same §4.6 design as the other legs: identical protocol, identical task texts
(T1 structural bottleneck, T6 material bottleneck), identical model and budget,
under the LangChain harness (on-demand skill idiom). Workspaces:
runs/portability/{t1,t6}_lc. Verdicts are judged afterwards by the same bda
adjudication layer.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = REPO_ROOT / "paper" / "portability" / "langchain" / "run_lc.py"
PY = Path('D:/anaconda/envs/py312/python.exe')  # migrated from the retired .venv

TASKS = [
    (
        "t1",
        "Design a battery for a next-generation pure electric sedan: energy density ≥ 392.61 Wh/kg, "
        "support 4C fast charge (no lithium plating), maximum temperature ≤ 60°C, "
        "overcharge to 4.7 V without triggering thermal runaway.",
    ),
    (
        "t6",
        "Design a battery for a smartphone: volumetric energy density ≥ 950 Wh/L, "
        "support 4C fast charge (no lithium plating), maximum temperature ≤ 50°C, "
        "anode SEI thickness ≤ 500 nm after 100 cycles, voltage plateau ≥ 4.1 V.",
    ),
]

MODEL = "deepseek-v4-pro"
MAX_TURNS = 300


def main() -> int:
    for task_id, text in TASKS:
        ws = REPO_ROOT / "runs" / "portability" / f"{task_id}_lc"
        print(f"=== starting {task_id}_lc (model={MODEL}, max_turns={MAX_TURNS}) ===", flush=True)
        r = subprocess.run(
            [str(PY), str(RUNNER), text, "--workspace", str(ws), "--max-turns", str(MAX_TURNS), "--model", MODEL],
            cwd=str(REPO_ROOT),
        )
        print(f"=== {task_id}_lc exit {r.returncode} ===", flush=True)
        if r.returncode != 0:
            print(f"{task_id}_lc FAILED", file=sys.stderr)
            return r.returncode
    print("run_lc_matrix complete: t1_lc + t6_lc done")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
