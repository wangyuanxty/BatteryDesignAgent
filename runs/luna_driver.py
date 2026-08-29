"""luna_driver.py — third-model robustness leg: 8 tasks on gpt-5.6-luna.

Sequential, same protocol/harness/budget as the pro/flash legs. Task texts
are the verbatim entry-0 texts of the governed runs (identical inputs).
Env (not committed, never printed): LUNA_BASE_URL, LUNA_KEY.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BATCH_LOG = Path(__file__).resolve().parent / "exp" / "luna_batch.log"

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


def _finished(ws: Path) -> bool:
    """Resume support: a workspace whose log.jsonl has a final entry is done."""
    log = ws / "log.jsonl"
    if not log.exists():
        return False
    return any(
        json.loads(line).get("action") == "final"
        for line in log.read_text(encoding="utf-8").splitlines() if line.strip()
    )


def run_one(task: str) -> int:
    ws = REPO / "runs" / "exp" / f"{task}_r1_luna"
    ws.mkdir(parents=True, exist_ok=True)
    if _finished(ws):
        with open(BATCH_LOG, "a", encoding="utf-8") as out:
            out.write(f"[{task}] skip (final entry exists) {time.strftime('%H:%M:%S')}\n")
        return 0
    text = task_text(task)
    env = dict(os.environ)
    env["ANTHROPIC_BASE_URL"] = os.environ["LUNA_BASE_URL"]
    env["ANTHROPIC_AUTH_TOKEN"] = os.environ["LUNA_KEY"]
    env["ANTHROPIC_API_KEY"] = os.environ["LUNA_KEY"]
    env.pop("ANTHROPIC_MODEL", None)
    cmd = [
        sys.executable, "run.py", text,
        "--workspace", str(ws),
        "--model", "gpt-5.6-luna",
        "--max-turns", "300",
    ]
    with open(BATCH_LOG, "a", encoding="utf-8") as out:
        out.write(f"[{task}] start {time.strftime('%H:%M:%S')} ws={ws}\n")
        out.flush()
        proc = subprocess.run(cmd, cwd=REPO, env=env, stdout=out, stderr=subprocess.STDOUT)
        out.write(f"[{task}] exit={proc.returncode} {time.strftime('%H:%M:%S')}\n")
        out.flush()
    return proc.returncode


def main() -> int:
    tasks = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"]
    fails = 0
    for t in tasks:
        try:
            code = run_one(t)
            fails += 1 if code != 0 else 0
        except Exception as exc:  # noqa: BLE001 - batch driver: log and continue
            with open(BATCH_LOG, "a", encoding="utf-8") as out:
                out.write(f"[{t}] driver error: {exc}\n")
            fails += 1
    with open(BATCH_LOG, "a", encoding="utf-8") as out:
        out.write(f"BATCH DONE fails={fails}/{len(tasks)} {time.strftime('%H:%M:%S')}\n")
    return fails


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
