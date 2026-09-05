"""Run nail penetration test from room temperature and with different hA values."""
import os, sys, json, subprocess

os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
PYTHON = "D:/research/degradation_prognostics/Battery_Design_Agent/.venv/Scripts/python.exe"
CELL_DIR = "cell"

mass_kg = 0.0434545275216  # from calc-energy

# Test 1: Nail from room temperature (298.15K) - most standard test condition
print("=== Test 1: Nail from room temperature (298.15K) ===")
cmd1 = [PYTHON, "-m", "bda", "run-tr",
        "--mass-kg", str(mass_kg),
        "--t-init", "298.15",
        "--q-nail", "10",
        "--out", f"{CELL_DIR}/V_K_nail_roomtemp.json"]
r1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=120)
if r1.returncode != 0:
    print(f"  ERROR: {r1.stderr[:500]}")
else:
    with open(f"{CELL_DIR}/V_K_nail_roomtemp.json", encoding="utf-8") as f:
        d = json.load(f)
    print(f"  triggered: {d['triggered']}")
    print(f"  T_max_K: {d['T_max_K']:.2f}")
    print(f"  T_final_K: {d['T_final_K']:.2f}")
    print(f"  mcp: {d['params']['mcp_J_K']:.2f} J/K")
    print(f"  hA: {d['params']['hA_W_K']} W/K")
    # Print first few T_series values
    for i, (t, T) in enumerate(zip(d['t_series_s'][:10], d['T_series_K'][:10])):
        print(f"    t={t:.0f}s: T={T:.2f}K")

# Test 2: With hA=1 (higher cooling, more realistic for larger cell surface)
print("\n=== Test 2: Nail from 298.15K, hA=1 W/K ===")
cmd2 = [PYTHON, "-m", "bda", "run-tr",
        "--mass-kg", str(mass_kg),
        "--t-init", "298.15",
        "--q-nail", "10",
        "--hA", "1.0",
        "--out", f"{CELL_DIR}/V_K_nail_hA1.json"]
r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=120)
if r2.returncode != 0:
    print(f"  ERROR: {r2.stderr[:500]}")
else:
    with open(f"{CELL_DIR}/V_K_nail_hA1.json", encoding="utf-8") as f:
        d = json.load(f)
    print(f"  triggered: {d['triggered']}")
    print(f"  T_max_K: {d['T_max_K']:.2f}")
    print(f"  T_final_K: {d['T_final_K']:.2f}")

# Test 3: With hA=0.5
print("\n=== Test 3: Nail from 298.15K, hA=0.5 W/K ===")
cmd3 = [PYTHON, "-m", "bda", "run-tr",
        "--mass-kg", str(mass_kg),
        "--t-init", "298.15",
        "--q-nail", "10",
        "--hA", "0.5",
        "--out", f"{CELL_DIR}/V_K_nail_hA05.json"]
r3 = subprocess.run(cmd3, capture_output=True, text=True, timeout=120)
if r3.returncode != 0:
    print(f"  ERROR: {r3.stderr[:500]}")
else:
    with open(f"{CELL_DIR}/V_K_nail_hA05.json", encoding="utf-8") as f:
        d = json.load(f)
    print(f"  triggered: {d['triggered']}")
    print(f"  T_max_K: {d['T_max_K']:.2f}")
    print(f"  T_final_K: {d['T_final_K']:.2f}")

print("\n=== Done ===")
