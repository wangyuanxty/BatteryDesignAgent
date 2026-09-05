import json, subprocess, os

os.chdir("D:\\research\\degradation_prognostics\\Battery_Design_Agent")

variants = {
    "D": "D_thin_highNP",
    "E": "E_moderate_highNP",
}

for v, name in variants.items():
    with open(f"runs/exp/t2_r1_mimo/cell/r2_{v}_1c.json") as f:
        d1c = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r2_{v}_4c.json") as f:
        d4c = json.load(f)

    ap = d4c.get("anode_potential_v", [])
    min_ap = min(ap) if ap else 999
    plated = min_ap < 0

    # Compute ED
    out_path = f"runs/exp/t2_r1_mimo/cell/r2_{v}_energy.json"
    params_path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    sim_path = f"runs/exp/t2_r1_mimo/cell/r2_{v}_1c.json"
    cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "calc-energy",
           "--sim", sim_path, "--params", params_path, "--base", "Chen2020", "--out", out_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        with open(out_path, encoding="utf-8") as f:
            energy = json.load(f)
        ed = energy["energy_density_wh_kg"]
    else:
        ed = "FAILED"
        print(f"  calc-energy error: {result.stderr}")

    print(f"Variant {v}: ED={ed} Wh/kg, cap_1c={d1c['capacity_ah']:.4f} Ah, "
          f"min_anode_V={min_ap:.4f}, plated={plated}, T_max={d4c['T_max_K']:.2f} K")

# Summary table
print("\n=== ALL VARIANTS SUMMARY ===")
print(f"{'Variant':<12} {'ED Wh/kg':>10} {'Cap Ah':>8} {'Plated':>8} {'min V':>8} {'T_max K':>8}")
print("-" * 60)

all_vars = {
    "Baseline": {"ed": 400.29, "cap": 4.948, "plated": True, "min_v": -0.439, "tmax": 332.4},
    "A_thin": {"ed": 324.63, "cap": 3.155, "plated": True, "min_v": -0.422, "tmax": 330.5},
    "B_thin_HP": {"ed": 318.29, "cap": 2.603, "plated": True, "min_v": -0.049, "tmax": 350.2},
    "C_thin_opt": {"ed": 297.07, "cap": 2.351, "plated": True, "min_v": -0.039, "tmax": 349.5},
}

# Add D and E from fresh reads
for v, name in [("D", "D_thin_highNP"), ("E", "E_moderate_highNP")]:
    with open(f"runs/exp/t2_r1_mimo/cell/r2_{v}_1c.json") as f:
        d1c = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r2_{v}_4c.json") as f:
        d4c = json.load(f)
    ap = d4c.get("anode_potential_v", [])
    min_ap = min(ap) if ap else 999
    out_path = f"runs/exp/t2_r1_mimo/cell/r2_{v}_energy.json"
    with open(out_path, encoding="utf-8") as f:
        energy = json.load(f)
    all_vars[f"{v}_{name.split('_',1)[1]}"] = {
        "ed": energy["energy_density_wh_kg"],
        "cap": d1c["capacity_ah"],
        "plated": min_ap < 0,
        "min_v": min_ap,
        "tmax": d4c["T_max_K"],
    }

for name, r in all_vars.items():
    print(f"{name:<12} {r['ed']:>10.2f} {r['cap']:>8.4f} {str(r['plated']):>8} {r['min_v']:>8.4f} {r['tmax']:>8.2f}")
