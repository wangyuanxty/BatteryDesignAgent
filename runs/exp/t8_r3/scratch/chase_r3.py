"""Run the 4-sim chain for one round-3 candidate (subprocess, absolute paths)."""
import subprocess
import sys
from pathlib import Path

REPO = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent")
PY = REPO / ".venv" / "Scripts" / "python.exe"
CELL = REPO / "runs" / "exp" / "t8_r3" / "cell"

name = sys.argv[1]
tag = name.replace(" ", "_")
params = CELL / f"params_r3_{tag}.json"

steps = [
    (["run-pyamm", "--params", str(params), "--protocol", "5C_discharge", "--mode", "dfn",
      "--thermal", "lumped", "--plating", "--out", str(CELL / f"r3_{tag}_5c_dfn.json")],
     "5c"),
    (["run-pyamm", "--params", str(params), "--protocol", "4C_charge_45C", "--mode", "dfn",
      "--thermal", "lumped", "--plating", "--out", str(CELL / f"r3_{tag}_4c_safety.json")],
     "4c"),
    (["run-pyamm", "--params", str(params), "--protocol", "1C_discharge", "--mode", "dfn",
      "--thermal", "lumped", "--plating", "--out", str(CELL / f"r3_{tag}_1c_dfn.json")],
     "1c"),
    (["calc-energy", "--sim", str(CELL / f"r3_{tag}_1c_dfn.json"), "--params", str(params),
      "--out", str(CELL / f"r3_{tag}_energy.json")],
     "energy"),
]
for args, label in steps:
    print(f"[{name}] {label} start", flush=True)
    r = subprocess.run([str(PY), "-m", "bda"] + args, cwd=str(REPO), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    print(f"[{name}] {label} exit={r.returncode}", flush=True)
    if r.stdout.strip():
        print(r.stdout[-600:], flush=True)
    if r.returncode != 0:
        print("STDERR:", r.stderr[-1800:], flush=True)
        sys.exit(f"[{name}] {label} failed rc={r.returncode}")
print(f"[{name}] ALL 4 STEPS DONE", flush=True)