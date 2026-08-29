"""bo_seed_driver.py — BO 3-seed robustness: seeds 5678 and 9012 (1234 exists).

Same per-task configuration as the main BO runs (bases recovered by
trial-0 fingerprints: t1=ORegan2022, t2-t7=Chen2020, t8=OKane2022).
50 evaluations each, same evaluator/objective as the published-standard
replication. Skip-if-exists on bo_trajectory.json (resume-safe).
"""

import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BATCH_LOG = Path(__file__).resolve().parent / "c2" / "bo_seed_batch.log"
PY = str(REPO / ".venv" / "Scripts" / "python.exe")

CONFIG = {
    "t1": "ORegan2022", "t2": "Chen2020", "t3": "Chen2020", "t4": "Chen2020",
    "t5": "Chen2020", "t6": "Chen2020", "t7": "Chen2020", "t8": "OKane2022",
}
SEEDS = ["5678", "9012"]


def run_one(t: str, seed: str) -> int:
    ws = REPO / "runs" / "c2" / f"{t}_seed{seed}"
    ws.mkdir(parents=True, exist_ok=True)
    if (ws / "bo_trajectory.json").exists():
        return 0
    cmd = [
        PY, "bo_baseline.py",
        "--task", t, "--base", CONFIG[t],
        "--budget", "50", "--seed", seed,
        "--workspace", str(ws),
    ]
    with open(BATCH_LOG, "a", encoding="utf-8") as out:
        out.write(f"[{t}_seed{seed}] start {time.strftime('%H:%M:%S')}\n")
        out.flush()
        proc = subprocess.run(cmd, cwd=REPO, stdout=out, stderr=subprocess.STDOUT)
        out.write(f"[{t}_seed{seed}] exit={proc.returncode} {time.strftime('%H:%M:%S')}\n")
        out.flush()
    return proc.returncode


def main() -> int:
    fails = 0
    for t in ("t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"):
        for seed in SEEDS:
            try:
                fails += 1 if run_one(t, seed) != 0 else 0
            except Exception as exc:  # noqa: BLE001 - batch driver: log and continue
                with open(BATCH_LOG, "a", encoding="utf-8") as out:
                    out.write(f"[{t}_seed{seed}] driver error: {exc}\n")
                fails += 1
    with open(BATCH_LOG, "a", encoding="utf-8") as out:
        out.write(f"BO SEED BATCH DONE fails={fails}/16 {time.strftime('%H:%M:%S')}\n")
    return fails


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())