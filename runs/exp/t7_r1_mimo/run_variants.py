"""Run 4C charge simulations for all architecture variants."""
import os, sys, json, subprocess

os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
PYTHON = "D:/research/degradation_prognostics/Battery_Design_Agent/.venv/Scripts/python.exe"
CELL_DIR = "cell"

# Architecture variants (from propose entry)
variants = {
    "V_B_thin_electrode": {
        "Positive electrode thickness [m]": 70e-6,
        "Negative electrode thickness [m]": 75e-6
    },
    "V_C_high_porosity": {
        "Positive electrode porosity": 0.35,
        "Negative electrode porosity": 0.35,
        "Separator porosity": 0.55
    },
    "V_D_thin_sep_small_particles": {
        "Separator thickness [m]": 12e-6,
        "Positive particle radius [m]": 3.5e-6,
        "Negative particle radius [m]": 3.5e-6
    },
    "V_E_balanced": {
        "Positive electrode thickness [m]": 80e-6,
        "Negative electrode thickness [m]": 85e-6,
        "Positive electrode porosity": 0.33,
        "Negative electrode porosity": 0.33,
        "Positive particle radius [m]": 3.5e-6,
        "Negative particle radius [m]": 5e-6
    }
}

# First, run 1C discharge for each variant (for calc-energy)
print("=== Running 1C discharge for each variant ===")
for name, params in variants.items():
    params_file = f"{CELL_DIR}/{name}_params.json"
    with open(params_file, "w") as f:
        json.dump(params, f)

    # 1C discharge
    sim_file = f"{CELL_DIR}/{name}_1c.json"
    cmd = [PYTHON, "-m", "bda", "run-pyamm",
           "--params", params_file,
           "--protocol", "1C_discharge",
           "--base", "Chen2020", "--mode", "spme",
           "--out", sim_file]
    print(f"  Running 1C discharge for {name}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"    ERROR: {result.stderr[:500]}")
    else:
        print(f"    OK")

    # calc-energy
    energy_file = f"{CELL_DIR}/{name}_energy.json"
    cmd_e = [PYTHON, "-m", "bda", "calc-energy",
             "--sim", sim_file,
             "--base", "Chen2020",
             "--out", energy_file]
    result_e = subprocess.run(cmd_e, capture_output=True, text=True, timeout=120)
    if result_e.returncode != 0:
        print(f"    calc-energy ERROR: {result_e.stderr[:500]}")
    else:
        with open(energy_file, encoding="utf-8") as ef:
            e_data = json.load(ef)
        print(f"    ED = {e_data['energy_density_wh_kg']:.2f} Wh/kg")

# Then, run 4C charge for each variant
print("\n=== Running 4C charge at 45C for each variant ===")
for name, params in variants.items():
    params_file = f"{CELL_DIR}/{name}_params.json"
    out_file = f"{CELL_DIR}/{name}_4c.json"
    cmd = [PYTHON, "-m", "bda", "run-pyamm",
           "--params", params_file,
           "--protocol", "4C_charge_45C",
           "--base", "Chen2020", "--mode", "spme",
           "--thermal", "lumped", "--plating",
           "--out", out_file]
    print(f"  Running 4C charge for {name}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        print(f"    ERROR: {result.stderr[:500]}")
    else:
        with open(out_file, encoding="utf-8") as f:
            data = json.load(f)
        min_ap = min(data.get("anode_potential_v", [1.0]))
        print(f"    T_max={data.get('T_max_K', 'N/A'):.1f}K, anode_min={min_ap:.4f}V, plated={'YES' if min_ap < 0 else 'NO'}")

print("\n=== Done ===")
