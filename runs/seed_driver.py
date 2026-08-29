"""seed_driver.py — 3-seed replication for the remaining six tasks (pro model).

Completes the 3x8 seed replication: T1/T6 already have r1-r3; this driver
adds r2/r3 for T2, T3, T4, T5, T7, T8 under deepseek-v4-pro, same harness,
same task texts (verbatim entry-0 texts of the r1 runs), same budget.
Resume-safe: skips workspaces whose log.jsonl already has a final entry.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BATCH_LOG = Path(__file__).resolve().parent / "exp" / "seed_batch.log"
TASKS = ["t2", "t3", "t4", "t5", "t7", "t8"]
SEEDS = ["r2", "r3"]
TASK_KEY_FALLBACK = ("task_verbatim", "task_text", "task")


def task_text(task: str) -> str:
    e0 = json.loads(
        (REPO / "runs" / "exp" / f"{task}_r1" / "log.jsonl")
        .read_text(encoding="utf-8").splitlines()[0]
    )
    meta = e0.get("criteria", {}).get("meta", {})
    for key in TASK_KEY_FALLBACK:
        if meta.get(key):
            return str(meta[key])
    raise KeyError(f"no task text key in {task}_r1 entry 0")


def finished(ws: Path) -> bool:
    log = ws / "log.jsonl"
    if not log.exists():
        return False
    return any(
        json.loads(line).get("action") == "final"
        for line in log.read_text(encoding="utf-8").splitlines() if line.strip()
    )


def run_one(task: str, seed: str) -> int:
    ws = REPO / "runs" / "exp" / f"{task}_{seed}"
    ws.mkdir(parents=True, exist_ok=True)
    if finished(ws):
        return 0
    cmd = [
        sys.executable, "run.py", task_text(task),
        "--workspace", str(ws),
        "--model", "deepseek-v4-pro",
        "--max-turns", "300",
    ]
    with open(BATCH_LOG, "a", encoding="utf-8") as out:
        out.write(f"[{task}_{seed}] start {time.strftime('%H:%M:%S')}\n")
        out.flush()
        proc = subprocess.run(cmd, cwd=REPO, stdout=out, stderr=subprocess.STDOUT)
        out.write(f"[{task}_{seed}] exit={proc.returncode} {time.strftime('%H:%M:%S')}\n")
        out.flush()
    return proc.returncode


def main() -> int:
    fails = 0
    for task in TASKS:
        for seed in SEEDS:
            try:
                fails += 1 if run_one(task, seed) != 0 else 0
            except Exception as exc:  # noqa: BLE001 - batch driver: log and continue
                with open(BATCH_LOG, "a", encoding="utf-8") as out:
                    out.write(f"[{task}_{seed}] driver error: {exc}\n")
                fails += 1
    with open(BATCH_LOG, "a", encoding="utf-8") as out:
        out.write(f"SEED BATCH DONE fails={fails}/12 {time.strftime('%H:%M:%S')}\n")
    return fails


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())