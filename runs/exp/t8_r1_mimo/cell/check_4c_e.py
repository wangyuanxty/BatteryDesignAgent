import json
d = json.load(open('runs/exp/t8_r1_mimo/cell/r3_archE_4c_charge.json', encoding='utf-8'))
tmax = d.get("T_max_K", "N/A")
anode = d.get("anode_potential_v", [])
anode_min = min(anode) if anode else "N/A"
cap = d.get("capacity_ah", "N/A")
print(f"ArchE 4C charge: T_max={tmax:.2f}K, anode_min={anode_min:.4f}V, cap={cap:.4f}Ah")
print(f"  Plating: {'YES' if anode_min < 0 else 'NO'}")
print(f"  Safety T: {'PASS' if tmax < 358.15 else 'FAIL'} (limit 358.15K)")
