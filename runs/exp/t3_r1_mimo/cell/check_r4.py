import json
import os

ws = r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_mimo\cell'

files = {
    '1C': 'r4_enhanced_1c.json',
    '5C': 'r4_enhanced_5c.json',
    '4C charge': 'r4_enhanced_4c.json',
}

for label, fname in files.items():
    fpath = os.path.join(ws, fname)
    with open(fpath, encoding='utf-8') as f:
        data = json.load(f)
    print(f"\n=== {label} ({fname}) ===")
    print(f"  model_used: {data.get('model_used')}")
    print(f"  capacity_ah: {data.get('capacity_ah')}")
    print(f"  T_max_K: {data.get('T_max_K')}")
    ap = data.get('anode_potential_v')
    if ap:
        print(f"  anode_potential_v min: {min(ap):.4f}, max: {max(ap):.4f}")
        print(f"  plated: {min(ap) < 0}")
    print(f"  time_s (last): {data.get('time_s', [0])[-1]:.1f}")

# Compute retention
with open(os.path.join(ws, 'r4_enhanced_1c.json'), encoding='utf-8') as f:
    c1c = json.load(f)
with open(os.path.join(ws, 'r4_enhanced_5c.json'), encoding='utf-8') as f:
    c5c = json.load(f)

ret = c5c['capacity_ah'] / c1c['capacity_ah'] * 100
print(f"\n=== Summary ===")
print(f"  5C retention: {ret:.2f}%")
print(f"  1C capacity: {c1c['capacity_ah']:.4f} Ah")
print(f"  5C capacity: {c5c['capacity_ah']:.4f} Ah")
