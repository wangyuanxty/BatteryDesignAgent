import json

# 1C energy
d = json.load(open('runs/exp/t8_r1_mimo/cell/r3_archF_1c.json', encoding='utf-8'))
cap1c = d['capacity_ah']
tmax1c = d.get('T_max_K', 'N/A')

# 5C
d5 = json.load(open('runs/exp/t8_r1_mimo/cell/r3_archF_5c.json', encoding='utf-8'))
cap5c = d5['capacity_ah']
tmax5c = d5.get('T_max_K', 'N/A')

# 4C charge
d4 = json.load(open('runs/exp/t8_r1_mimo/cell/r3_archF_4c_charge.json', encoding='utf-8'))
tmax4c = d4.get('T_max_K', 'N/A')
anode = d4.get('anode_potential_v', [])
anode_min = min(anode) if anode else 'N/A'
plated = anode_min < 0 if isinstance(anode_min, float) else 'N/A'

retention = cap5c / cap1c * 100

print(f"ArchF Results:")
print(f"  1C: cap={cap1c:.4f}Ah, T_max={tmax1c:.2f}K")
print(f"  5C: cap={cap5c:.4f}Ah, T_max={tmax5c:.2f}K")
print(f"  5C retention: {retention:.1f}%")
print(f"  4C charge: T_max={tmax4c:.2f}K, anode_min={anode_min:.4f}V, plated={plated}")
print(f"  Safety T: {'PASS' if isinstance(tmax4c, float) and tmax4c < 358.15 else 'FAIL'}")
print(f"  Plating: {'PASS (no)' if not plated else 'FAIL (yes)'}")
