"""bo_seed_parallel.py — parallel BO 3-seed workers with atomic job claims.

Spawns N worker processes; each worker claims remaining jobs via an
O_EXCL claim file, then runs bo_baseline.py (same config as the main
runs). Resume-safe: skips finished (trajectory exists) and claimed jobs.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = str(REPO / ".venv" / "Scripts" / "python.exe")
BATCH_LOG = REPO / "runs" / "c2" / "bo_seed_batch.log"

CONFIG = {
    "t1": "ORegan2022", "t2": "Chen2020", "t3": "Chen2020", "t4": "Chen2020",
    "t5": "Chen2020", "t6": "Chen2020", "t7": "Chen2020", "t8": "OKane2022",
}
JOBS = [f"{t}_{s}" for t in ("t5", "t6", "t7", "t8")
        for s in ("seed5678", "seed9012")]
N_WORKERS = 3


def claim(wid: int, job: str) -> bool:
    """Atomically claim a job; False if someone else got it."""
    t, seed = job.rsplit("_", 1)
    ws = REPO / "runs" / "c2" / f"{t}_{seed}"
    if (ws / "bo_trajectory.json").exists():
        return False
    try:
        fd = os.open(str(ws / f".claim_{wid}"), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
        return True
    except FileExistsError:
        return False


def run_job(job: str) -> int:
    t, seed = job.rsplit("_", 1)
    ws = REPO / "runs" / "c2" / f"{t}_{seed}"
    ws.mkdir(parents=True, exist_ok=True)
    cmd = [PY, "bo_baseline.py", "--task", t, "--base", CONFIG[t],
           "--budget", "50", "--seed", seed.replace("seed", ""),
           "--workspace", str(ws)]
    with open(BATCH_LOG, "a", encoding="utf-8") as out:
        out.write(f"[{job}@{os.getpid()}] start {time.strftime('%H:%M:%S')}\n")
        out.flush()
        proc = subprocess.run(cmd, cwd=REPO, stdout=out, stderr=subprocess.STDOUT)
        out.write(f"[{job}] exit={proc.returncode} {time.strftime('%H:%M:%S')}\n")
        out.flush()
    return proc.returncode


def worker(wid: int) -> int:
    fails = 0
    for job in JOBS:
        if not claim(wid, job):
            continue
        try:
            fails += 1 if run_job(job) != 0 else 0
        except Exception as exc:  # noqa: BLE001 - worker: log and continue
            with open(BATCH_LOG, "a", encoding="utf-8") as out:
                out.write(f"[{job}] worker error: {exc}\n")
            fails += 1
    return fails


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--worker" in sys.argv:
        wid = int(sys.argv[sys.argv.index("--worker") + 1])
        raise SystemExit(worker(wid))
    procs = []
    for wid in range(1, N_WORKERS + 1):
        procs.append(subprocess.Popen(
            [PY, str(Path(__file__).resolve()), "--worker", str(wid)],
            cwd=REPO, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)))
    for p in procs:
        p.wait()
    with open(BATCH_LOG, "a", encoding="utf-8") as out:
        out.write(f"BO PARALLEL DONE {time.strftime('%H:%M:%S')}\n")
    raise SystemExit(0)