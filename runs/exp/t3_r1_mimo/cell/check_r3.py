import json
import os

ws = r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_mimo\cell'
variants = [('v5', 'E'), ('v6', 'F'), ('v7', 'G')]
labels = ['Arch E (58% thin, 0.43/0.33)', 'Arch F (63% thin, 0.44/0.34)', 'Arch G (54% thin, 0.42/0.32)']

# Also include R2 best for comparison
all_variants = [('v1', 'A'), ('v2', 'B'), ('v5', 'E'), ('v6', 'F'), ('v7', 'G')]
all_labels = ['A (50% thin)', 'B (65% thin)', 'E (58% thin)', 'F (63% thin)', 'G (54% thin)']

prefix_map = {
    'v1': 'r2', 'v2': 'r2',
    'v5': 'r3', 'v6': 'r3', 'v7': 'r3'
}

print(f'{"Variant":<35} {"1C Cap(Ah)":<12} {"5C Cap(Ah)":<12} {"5C Ret%":<10} {"T_max 5C":<10} {"Cap>=2?":<8} {"Ret>=95?":<8}')
print('-' * 105)

for (v, letter), label in zip(all_variants, all_labels):
    prefix = prefix_map[v]
    c1c_file = os.path.join(ws, f'{prefix}_{v}_1c.json')
    c5c_file = os.path.join(ws, f'{prefix}_{v}_5c.json')

    with open(c1c_file, encoding='utf-8') as f:
        c1c = json.load(f)
    with open(c5c_file, encoding='utf-8') as f:
        c5c = json.load(f)

    cap1c = c1c.get('capacity_ah', 0)
    cap5c = c5c.get('capacity_ah', 0)
    ret = (cap5c / cap1c * 100) if cap1c > 0 else 0
    t5c = c5c.get('T_max_K', 'N/A')
    cap_ok = 'YES' if cap1c >= 2.0 else 'NO'
    ret_ok = 'YES' if ret >= 95.0 else 'NO'

    print(f'{label:<35} {cap1c:<12.4f} {cap5c:<12.4f} {ret:<10.2f} {t5c:<10.2f} {cap_ok:<8} {ret_ok:<8}')
