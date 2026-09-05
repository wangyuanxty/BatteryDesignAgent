"""Run DFN 4C charge and additional architecture variants."""
import os, sys, json, subprocess

os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
PYTHON = "D:/research/degradation_prognostics/Battery_Design_Agent/.venv/Scripts/python.exe"
CELL_DIR = "cell"

# Additional aggressive variants
variants = {
    "V_F_small_anode_particle": {
        "Negative particle radius [m]": 2.5e-6
    },
    "V_G_thin_both_small_particles": {
        "Positive electrode thickness [m]": 60e-6,
        "Negative electrode thickness [m]": 65e-6,
        "Positive particle radius [m]": 3e-6,
        "Negative particle radius [m]": 3e-6,
        "Positive electrode porosity": 0.35,
        "Negative electrode porosity": 0.35
    },
    "V_H_high_porosity_thin_sep": {
        "Positive electrode porosity": 0.4,
        "Negative electrode porosity": 0.4,
        "Separator thickness [m]": 10e-6,
        "Separator porosity": 0.6
    }
}

# Run 1C discharge + calc-energy + 4C charge DFN for each
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
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"    ERROR: {r.stderr[:300]}")
        continue

    # calc-energy
    energy_file = f"{CELL_DIR}/{name}_energy.json"
    cmd_e = [PYTHON, "-m", "bda", "calc-energy",
             "--sim", sim_file, "--base", "Chen2020",
             "--out", energy_file]
    r_e = subprocess.run(cmd_e, capture_output=True, text=True, timeout=120)
    if r_e.returncode == 0:
        with open(energy_file, encoding="utf-8") as ef:
            e_data = json.load(ef)
        print(f"    ED = {e_data['energy_density_wh_kg']:.2f} Wh/kg")

    # 4C charge DFN
    out_file = f"{CELL_DIR}/{name}_4c_dfn.json"
    cmd_4c = [PYTHON, "-m", "bda", "run-pyamm",
              "--params", params_file,
              "--protocol", "4C_charge_45C",
              "--base", "Chen2020", "--mode", "dfn",
              "--thermal", "lumped", "--plating",
              "--out", out_file]
    print(f"    Running 4C charge DFN for {name}...")
    r_4c = subprocess.run(cmd_4c, capture_output=True, text=True, timeout=300)
    if r_4c.returncode != 0:
        print(f"      ERROR: {r_4c.stderr[:300]}")
        # Try SPMe fallback
        out_file_spme = f"{CELL_DIR}/{name}_4c_spme.json"
        cmd_4c_spme = [PYTHON, "-m", "bda", "run-pyamm",
                       "--params", params_file,
                       "--protocol", "4C_charge_45C",
                       "--base", "Chen2020", "--mode", "spme",
                       "--thermal", "lumped", "--plating",
                       "--out", out_file_spme]
        r_spme = subprocess.run(cmd_4c_spme, capture_output=True, text=True, timeout=180)
        if r_spme.returncode == 0:
            with open(out_file_spme, encoding="utf-8") as f:
                data = json.load(f)
            min_ap = min(data.get("anode_potential_v", [1.0]))
            print(f"      SPMe fallback: T_max={data.get('T_max_K', 'N/A'):.1f}K, anode_min={min_ap:.4f}V")
    else:
        with open(out_file, encoding="utf-8") as f:
            data = json.load(f)
        min_ap = min(data.get("anode_potential_v", [1.0]))
        model = data.get("model_used", "?")
        print(f"      {model}: T_max={data.get('T_max_K', 'N/A'):.1f}K, anode_min={min_ap:.4f}V, plated={'YES' if min_ap < 0 else 'NO'}")

# Also run baseline with DFN for comparison
print("\n=== Running baseline 4C charge DFN ===")
cmd_base = [PYTHON, "-m", "bda", "run-pyamm",
            "--params", f"{CELL_DIR}/baseline_params.json",
            "--protocol", "4C_charge_45C",
            "--base", "Chen2020", "--mode", "dfn",
            "--thermal", "lumped", "--plating",
            "--out", f"{CELL_DIR}/baseline_4c_dfn.json"]
r_base = subprocess.run(cmd_base, capture_output=True, text=True, timeout=300)
if r_base.returncode != 0:
    print(f"  DFN ERROR: {r_base.stderr[:300]}")
else:
    with open(f"{CELL_DIR}/baseline_4c_dfn.json", encoding="utf-8") as f:
        data = json.load(f)
    min_ap = min(data.get("anode_potential_v", [1.0]))
    model = data.get("model_used", "?")
    print(f"  Baseline DFN: T_max={data.get('T_max_K', 'N/A'):.1f}K, anode_min={min_ap:.4f}V, model={model}")

print("\n=== All done ===")
