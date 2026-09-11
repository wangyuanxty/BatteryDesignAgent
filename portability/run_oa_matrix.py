"""run_oa_matrix.py — cross-harness portability driver (OpenAI Agents SDK leg).

Executes the §4.6 design: the same protocol, the same task texts (T1 structural
bottleneck, T6 material bottleneck), the same model, and the same 300-turn
budget, under the OpenAI Agents SDK harness. Workspaces: runs/portability/{t1,t6}_oa.
Run after the primary-harness legs; verdicts are judged afterwards by the SAME
bda adjudication layer (log-evaluate / verify-deliverables) — the judgment
mechanics are CLI, hence harness-independent by construction.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = REPO_ROOT / "paper" / "portability" / "oa_sdk" / "run_oa.py"
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
        ws = REPO_ROOT / "runs" / "portability" / f"{task_id}_oa"
        print(f"=== starting {task_id}_oa (model={MODEL}, max_turns={MAX_TURNS}) ===", flush=True)
        r = subprocess.run(
            [str(PY), str(RUNNER), text, "--workspace", str(ws), "--max-turns", str(MAX_TURNS), "--model", MODEL],
            cwd=str(REPO_ROOT),
        )
        print(f"=== {task_id}_oa exit {r.returncode} ===", flush=True)
        if r.returncode != 0:
            print(f"{task_id}_oa FAILED", file=sys.stderr)
            return r.returncode
    print("run_oa_matrix complete: t1_oa + t6_oa done")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
