"""Fine-tune near-miss candidates V_G and V_H."""
import os, sys, json, subprocess

os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
PYTHON = "D:/research/degradation_prognostics/Battery_Design_Agent/.venv/Scripts/python.exe"
CELL_DIR = "cell"

# Fine-tune variants
variants = {
    "V_I_h_porosity_thinnest_sep": {
        "Positive electrode porosity": 0.42,
        "Negative electrode porosity": 0.42,
        "Separator thickness [m]": 8e-6,
        "Separator porosity": 0.62
    },
    "V_J_thin_electrode_h_porosity": {
        "Positive electrode thickness [m]": 75e-6,
        "Negative electrode thickness [m]": 80e-6,
        "Positive electrode porosity": 0.38,
        "Negative electrode porosity": 0.38,
        "Positive particle radius [m]": 3e-6,
        "Negative particle radius [m]": 3e-6
    },
    "V_K_extreme_transport": {
        "Positive electrode porosity": 0.45,
        "Negative electrode porosity": 0.45,
        "Separator thickness [m]": 8e-6,
        "Separator porosity": 0.65,
        "Positive particle radius [m]": 3e-6,
        "Negative particle radius [m]": 3e-6
    },
    "V_L_optimized_for_plating": {
        "Positive electrode thickness [m]": 70e-6,
        "Negative electrode thickness [m]": 75e-6,
        "Positive electrode porosity": 0.4,
        "Negative electrode porosity": 0.4,
        "Separator thickness [m]": 10e-6,
        "Separator porosity": 0.6,
        "Positive particle radius [m]": 3e-6,
        "Negative particle radius [m]": 3e-6
    }
}

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
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"{name}: 1C ERROR: {r.stderr[:200]}")
        continue

    # calc-energy
    energy_file = f"{CELL_DIR}/{name}_energy.json"
    cmd_e = [PYTHON, "-m", "bda", "calc-energy",
             "--sim", sim_file, "--base", "Chen2020",
             "--out", energy_file]
    r_e = subprocess.run(cmd_e, capture_output=True, text=True, timeout=120)
    ed = 0
    if r_e.returncode == 0:
        with open(energy_file, encoding="utf-8") as ef:
            e_data = json.load(ef)
        ed = e_data['energy_density_wh_kg']
        print(f"{name}: ED = {ed:.2f} Wh/kg")

    # 4C charge DFN
    out_file = f"{CELL_DIR}/{name}_4c_dfn.json"
    cmd_4c = [PYTHON, "-m", "bda", "run-pyamm",
              "--params", params_file,
              "--protocol", "4C_charge_45C",
              "--base", "Chen2020", "--mode", "dfn",
              "--thermal", "lumped", "--plating",
              "--out", out_file]
    r_4c = subprocess.run(cmd_4c, capture_output=True, text=True, timeout=300)
    if r_4c.returncode != 0:
        print(f"  DFN failed, trying SPMe...")
        out_file_spme = f"{CELL_DIR}/{name}_4c_spme.json"
        cmd_spme = [PYTHON, "-m", "bda", "run-pyamm",
                    "--params", params_file,
                    "--protocol", "4C_charge_45C",
                    "--base", "Chen2020", "--mode", "spme",
                    "--thermal", "lumped", "--plating",
                    "--out", out_file_spme]
        r_spme = subprocess.run(cmd_spme, capture_output=True, text=True, timeout=180)
        if r_spme.returncode == 0:
            with open(out_file_spme, encoding="utf-8") as f:
                data = json.load(f)
            min_ap = min(data.get("anode_potential_v", [1.0]))
            print(f"  SPMe: anode_min={min_ap:.4f}V, plated={'YES' if min_ap < 0 else 'NO'}")
    else:
        with open(out_file, encoding="utf-8") as f:
            data = json.load(f)
        min_ap = min(data.get("anode_potential_v", [1.0]))
        print(f"  DFN: anode_min={min_ap:.4f}V, plated={'YES' if min_ap < 0 else 'NO'}")

print("\n=== Fine-tuning done ===")
