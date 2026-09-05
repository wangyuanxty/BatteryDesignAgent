import json, subprocess, os

os.chdir("D:\\research\\degradation_prognostics\\Battery_Design_Agent")

variants = {
    "J": "J_high_transport",
    "K": "K_mid_transport",
    "L": "L_transport_highNP",
}

print("=== Variants J/K/L Results ===")
print(f"{'Var':<4} {'ED':>8} {'Cap':>7} {'Plated':>7} {'minV':>8} {'Tmax':>7}")
print("-" * 50)

for v, name in variants.items():
    with open(f"runs/exp/t2_r1_mimo/cell/r4_{v}_1c.json") as f:
        d1c = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r4_{v}_4c.json") as f:
        d4c = json.load(f)

    ap = d4c.get("anode_potential_v", [])
    min_ap = min(ap) if ap else 999
    plated = min_ap < 0

    out_path = f"runs/exp/t2_r1_mimo/cell/r4_{v}_energy.json"
    params_path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    sim_path = f"runs/exp/t2_r1_mimo/cell/r4_{v}_1c.json"
    cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "calc-energy",
           "--sim", sim_path, "--params", params_path, "--base", "Chen2020", "--out", out_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    ed = "FAIL"
    if result.returncode == 0:
        with open(out_path, encoding="utf-8") as f:
            energy = json.load(f)
        ed = f"{energy['energy_density_wh_kg']:.1f}"

    print(f"{v:<4} {ed:>8} {d1c['capacity_ah']:>7.3f} {str(plated):>7} {min_ap:>8.4f} {d4c['T_max_K']:>7.1f}")
