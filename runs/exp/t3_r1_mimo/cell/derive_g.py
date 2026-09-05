import json
import os

ws = r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_mimo\cell'

# Architecture G = v7
with open(os.path.join(ws, 'r3_v7_1c.json'), encoding='utf-8') as f:
    c1c = json.load(f)
with open(os.path.join(ws, 'r3_v7_5c.json'), encoding='utf-8') as f:
    c5c = json.load(f)

retention_5c = c5c['capacity_ah'] / c1c['capacity_ah']

combined = {
    'capacity_ah': c1c['capacity_ah'],
    'five_c_retention': retention_5c,
    'five_c_capacity_ah': c5c['capacity_ah'],
    'one_c_capacity_ah': c1c['capacity_ah'],
    'model_used_1c': c1c['model_used'],
    'model_used_5c': c5c['model_used'],
    'T_max_K_1c': c1c.get('T_max_K'),
    'T_max_K_5c': c5c.get('T_max_K'),
}

with open(os.path.join(ws, 'r3_g_combined.json'), 'w', encoding='utf-8') as f:
    json.dump(combined, f, indent=2)

print(f"Arch G (v7): 1C={c1c['capacity_ah']:.4f} Ah, 5C={c5c['capacity_ah']:.4f} Ah, retention={retention_5c*100:.2f}%")
print(f"T_max 1C={c1c.get('T_max_K')}, T_max 5C={c5c.get('T_max_K')}")
