import json
import os

ws = r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_mimo\cell'
variants = ['v1', 'v2', 'v3', 'v4']
names = ['Architecture A (50% thin)', 'Architecture B (65% thin)', 'Architecture C (ultra-thin)', 'Architecture D (thin+thin CC)']

print(f'{"Variant":<30} {"1C Cap(Ah)":<12} {"5C Cap(Ah)":<12} {"5C Ret%":<10} {"T_max 1C":<10} {"T_max 5C":<10} {"model_1c":<10} {"model_5c":<10}')
print('-' * 110)

for v, name in zip(variants, names):
    c1c_file = os.path.join(ws, f'r2_{v}_1c.json')
    c5c_file = os.path.join(ws, f'r2_{v}_5c.json')

    with open(c1c_file, encoding='utf-8') as f:
        c1c = json.load(f)
    with open(c5c_file, encoding='utf-8') as f:
        c5c = json.load(f)

    cap1c = c1c.get('capacity_ah', 0)
    cap5c = c5c.get('capacity_ah', 0)
    ret = (cap5c / cap1c * 100) if cap1c > 0 else 0
    t1c = c1c.get('T_max_K', 'N/A')
    t5c = c5c.get('T_max_K', 'N/A')
    m1c = c1c.get('model_used', '?')
    m5c = c5c.get('model_used', '?')

    print(f'{name:<30} {cap1c:<12.4f} {cap5c:<12.4f} {ret:<10.2f} {t1c:<10.2f} {t5c:<10.2f} {m1c:<10} {m5c:<10}')
