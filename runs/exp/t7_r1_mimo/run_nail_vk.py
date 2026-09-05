"""Get V_K mass and run nail penetration test."""
import os, sys, json, subprocess

os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
PYTHON = "D:/research/degradation_prognostics/Battery_Design_Agent/.venv/Scripts/python.exe"
CELL_DIR = "cell"

# Get mass from calc-energy
with open(f"{CELL_DIR}/V_K_extreme_transport_energy.json", encoding="utf-8") as f:
    energy_data = json.load(f)
mass_kg = energy_data["mass_kg"]
print(f"V_K mass: {mass_kg*1000:.2f} g")

# Run nail penetration thermal runaway
cmd = [PYTHON, "-m", "bda", "run-tr",
       "--sim", f"{CELL_DIR}/V_K_overcharge.json",
       "--mass-kg", str(mass_kg),
       "--q-nail", "10",
       "--out", f"{CELL_DIR}/V_K_nail_tr.json"]
print("Running nail penetration test...")
r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
if r.returncode != 0:
    print(f"ERROR: {r.stderr[:500]}")
else:
    with open(f"{CELL_DIR}/V_K_nail_tr.json", encoding="utf-8") as f:
        data = json.load(f)
    print(f"  triggered: {data['triggered']}")
    print(f"  trigger_time_s: {data.get('trigger_time_s', 'N/A')}")
    print(f"  T_max_K: {data['T_max_K']:.2f}")
    print(f"  dTdt_max: {data['dTdt_max_K_s']:.2f} K/s")
    print(f"  mcp_J_K: {data['params']['mcp_J_K']:.2f}")
    print(f"  hA_W_K: {data['params']['hA_W_K']}")
    print(f"  q_nail_W: {data['params']['q_nail_W']}")
