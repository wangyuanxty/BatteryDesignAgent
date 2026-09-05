import json, subprocess, os

os.chdir("D:\\research\\degradation_prognostics\\Battery_Design_Agent")

variants = {
    "A": "A_thin_electrodes",
    "B": "B_thin_high_porosity",
    "C": "C_thin_optimal",
}

for v, name in variants.items():
    out_path = f"runs/exp/t2_r1_mimo/cell/r2_{v}_energy.json"
    params_path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    sim_path = f"runs/exp/t2_r1_mimo/cell/r2_{v}_1c.json"
    cmd = [
        ".venv\\Scripts\\python.exe", "-m", "bda", "calc-energy",
        "--sim", sim_path,
        "--params", params_path,
        "--base", "Chen2020",
        "--out", out_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Variant {v} calc-energy FAILED: {result.stderr}")
        continue
    with open(out_path, encoding="utf-8") as f:
        energy = json.load(f)
    print(f"Variant {v}: ED={energy['energy_density_wh_kg']:.2f} Wh/kg, mass={energy['mass_kg']*1000:.1f} g, cap={energy['capacity_ah']:.4f} Ah")
