import json

files = [
    'runs/exp/t8_r1_mimo/cell/r2_chen2020_archB_4c_charge.json',
]
for path in files:
    d = json.load(open(path))
    tmax = d.get("T_max_K", "N/A")
    anode = d.get("anode_potential_v", [])
    anode_min = min(anode) if anode else "N/A"
    cap = d.get("capacity_ah", "N/A")
    model = d["model_used"]
    print(f"4C charge: T_max={tmax:.2f}K, anode_min={anode_min:.4f}V, cap={cap:.4f}Ah, model={model}")
    print(f"  Plating: {'YES' if anode_min < 0 else 'NO'}")
    print(f"  Safety T: {'PASS' if tmax < 358.15 else 'FAIL'} (limit 358.15K)")
