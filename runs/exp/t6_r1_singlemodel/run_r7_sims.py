"""Driver: full E3/E4 sim sets (1C, energy, 4C, aging). Sequential, prints per step."""
import subprocess
import sys
from pathlib import Path

PY = r"D:\research\degradation_prognostics\Battery_Design_Agent\.venv\Scripts\python.exe"
BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"
CELL = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_singlemodel\cell")


def run(args, label):
    print(f"[{label}] START", flush=True)
    r = subprocess.run([PY, "-m", "bda", *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[{label}] FAILED rc={r.returncode}", flush=True)
        print("STDOUT:", r.stdout[-2000:], flush=True)
        print("STDERR:", r.stderr[-2000:], flush=True)
    else:
        print(f"[{label}] OK", flush=True)
    return r.returncode


steps = []
for tag in ("E3", "E4"):
    params = str(CELL / f"r7_{tag}_params.json")
    steps.append((["run-pyamm", "--params", params, "--protocol", "1C_discharge",
                   "--base", BASE, "--mode", "spme", "--thermal", "lumped",
                   "--out", str(CELL / f"r7_{tag}_1c_spme.json")], f"r7_{tag}_1c"))
    steps.append((["calc-energy", "--sim", str(CELL / f"r7_{tag}_1c_spme.json"), "--params", params,
                   "--base", BASE, "--out", str(CELL / f"r7_{tag}_energy.json")], f"r7_{tag}_energy"))
    steps.append((["run-pyamm", "--params", params, "--protocol", "4C_charge_45C",
                   "--base", BASE, "--mode", "spme", "--thermal", "lumped", "--plating",
                   "--out", str(CELL / f"r7_{tag}_4c_spme.json")], f"r7_{tag}_4c"))
    steps.append((["run-pyamm", "--params", params, "--protocol", "aging_1C_100cyc",
                   "--base", BASE, "--mode", "spme", "--thermal", "lumped", "--cycles", "100",
                   "--out", str(CELL / f"r7_{tag}_aging_spme.json")], f"r7_{tag}_aging"))

failures = []
for args, label in steps:
    if run(args, label) != 0:
        failures.append(label)
print("ALL STEPS DONE. failures:", failures, flush=True)
sys.exit(1 if failures else 0)
