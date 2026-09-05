import json, subprocess, os

os.chdir("D:\\research\\degradation_prognostics\\Battery_Design_Agent")

variants = {
    "F": "F_transport_only",
    "G": "G_sei_only",
    "H": "H_combined",
    "I": "I_moderate_combined",
}

print("=== Electrolyte Variant Results ===")
print(f"{'Variant':<12} {'ED Wh/kg':>10} {'Cap Ah':>8} {'Plated':>8} {'min V':>8} {'T_max K':>8}")
print("-" * 60)

for v, name in variants.items():
    with open(f"runs/exp/t2_r1_mimo/cell/r3_{v}_1c.json") as f:
        d1c = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r3_{v}_4c.json") as f:
        d4c = json.load(f)

    ap = d4c.get("anode_potential_v", [])
    min_ap = min(ap) if ap else 999
    plated = min_ap < 0

    # Compute ED
    out_path = f"runs/exp/t2_r1_mimo/cell/r3_{v}_energy.json"
    params_path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    sim_path = f"runs/exp/t2_r1_mimo/cell/r3_{v}_1c.json"
    cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "calc-energy",
           "--sim", sim_path, "--params", params_path, "--base", "Chen2020", "--out", out_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        with open(out_path, encoding="utf-8") as f:
            energy = json.load(f)
        ed = energy["energy_density_wh_kg"]
    else:
        ed = "FAILED"

    print(f"{v:<12} {ed if isinstance(ed,str) else f'{ed:.2f}':>10} {d1c['capacity_ah']:>8.4f} {str(plated):>8} {min_ap:>8.4f} {d4c['T_max_K']:>8.2f}")

# Also check lowT for variant H (the combined best candidate)
print("\n--- Low-T check for variant H ---")
cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "run-pyamm",
       "--params", "runs/exp/t2_r1_mimo/cell/params_H_combined.json",
       "--base", "Chen2020", "--protocol", "lowT_discharge", "--mode", "spme",
       "--out", "runs/exp/t2_r1_mimo/cell/r3_H_lowT.json"]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    with open("runs/exp/t2_r1_mimo/cell/r3_H_lowT.json") as f:
        dlt = json.load(f)
    with open("runs/exp/t2_r1_mimo/cell/r3_H_1c.json") as f:
        d1c = json.load(f)
    retention = dlt["capacity_ah"] / d1c["capacity_ah"] * 100
    print(f"H lowT: cap={dlt['capacity_ah']:.4f} Ah, retention={retention:.2f}%")
else:
    print(f"LowT FAILED: {result.stderr}")
