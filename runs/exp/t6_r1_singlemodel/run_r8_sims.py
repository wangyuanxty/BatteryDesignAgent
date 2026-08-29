"""Run all R8 sims: E5/E6 1C, energy, 4C plating, aging."""
import json
import subprocess
import sys
from pathlib import Path

CELL = Path("cell")
PY = r"D:\research\degradation_prognostics\Battery_Design_Agent\.venv\Scripts\python.exe"
BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

steps = []
for tag in ("E5", "E6"):
    p = CELL / f"r8_{tag}_params.json"
    steps += [
        (f"r8_{tag}_1c", ["run-pyamm", "--params", str(p), "--protocol", "1C_discharge",
                          "--base", BASE, "--mode", "spme", "--out", f"cell/r8_{tag}_1c_spme.json"]),
        (f"r8_{tag}_energy", ["calc-energy", "--sim", f"cell/r8_{tag}_1c_spme.json",
                              "--params", str(p), "--base", BASE, "--out", f"cell/r8_{tag}_energy.json"]),
        (f"r8_{tag}_4c", ["run-pyamm", "--params", str(p), "--protocol", "4C_charge_45C",
                          "--base", BASE, "--mode", "spme", "--thermal", "lumped", "--plating",
                          "--out", f"cell/r8_{tag}_4c_spme.json"]),
        (f"r8_{tag}_aging", ["run-pyamm", "--params", str(p), "--protocol", "aging_1C_100cyc",
                             "--base", BASE, "--mode", "spme", "--out", f"cell/r8_{tag}_aging_spme.json"]),
    ]

failures = []
for name, args in steps:
    print(f"[{name}] START", flush=True)
    try:
        r = subprocess.run([PY, "-m", "bda", *args], capture_output=True, text=True, timeout=1800)
        if r.returncode != 0:
            failures.append(name)
            print(f"[{name}] rc={r.returncode} stderr={r.stderr[-400:]}", flush=True)
        else:
            print(f"[{name}] OK", flush=True)
    except Exception as e:
        failures.append(name)
        print(f"[{name}] EXC {e}", flush=True)

print("ALL STEPS DONE. failures:", failures)
