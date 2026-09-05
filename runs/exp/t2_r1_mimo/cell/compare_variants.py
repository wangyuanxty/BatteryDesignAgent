import json

variants = ["A", "B", "C"]
results = {}

for v in variants:
    # Read 1C discharge
    with open(f"runs/exp/t2_r1_mimo/cell/r2_{v}_1c.json") as f:
        d1c = json.load(f)
    # Read 4C charge
    with open(f"runs/exp/t2_r1_mimo/cell/r2_{v}_4c.json") as f:
        d4c = json.load(f)

    cap_1c = d1c["capacity_ah"]
    ap = d4c.get("anode_potential_v", [])
    min_ap = min(ap) if ap else 999
    plated = min_ap < 0

    results[v] = {
        "capacity_1c": cap_1c,
        "T_max_4c": d4c["T_max_K"],
        "min_anode_v": min_ap,
        "plated": plated,
    }
    print(f"Variant {v}: cap_1c={cap_1c:.4f} Ah, T_max_4C={d4c['T_max_K']:.2f} K, min_anode_V={min_ap:.4f}, plated={plated}")

# Now compute energy density for each
print("\n--- Energy density ---")
for v in variants:
    import subprocess, os
    os.chdir("D:\\research\\degradation_prognostics\\Battery_Design_Agent")
    out_path = f"runs/exp/t2_r1_mimo/cell/r2_{v}_energy.json"
    params_path = f"runs/exp/t2_r1_mimo/cell/params_{ {'A':'A_thin_electrodes','B':'B_thin_high_porosity','C':'C_thin_optimal'}[v] }.json"
    sim_path = f"runs/exp/t2_r1_mimo/cell/r2_{v}_1c.json"
    cmd = f'.venv\\Scripts\\python.exe -m bda calc-energy --sim "{sim_path}" --params "{params_path}" --base Chen2020 --out "{out_path}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Variant {v} calc-energy FAILED: {result.stderr}")
        continue
    with open(out_path) as f:
        energy = json.load(f)
    print(f"Variant {v}: ED={energy['energy_density_wh_kg']:.2f} Wh/kg, mass={energy['mass_kg']*1000:.1f} g")
    results[v]["ed"] = energy["energy_density_wh_kg"]
    results[v]["mass_g"] = energy["mass_kg"] * 1000

print("\n--- Summary ---")
print(f"{'Variant':<10} {'ED Wh/kg':>10} {'Cap Ah':>8} {'Plated':>8} {'T_max K':>8} {'min V':>8}")
for v in variants:
    r = results[v]
    print(f"{v:<10} {r.get('ed','?'):>10.2f} {r['capacity_1c']:>8.4f} {str(r['plated']):>8} {r['T_max_4c']:>8.2f} {r['min_anode_v']:>8.4f}")
