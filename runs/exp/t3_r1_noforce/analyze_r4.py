import json

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

def discharge_dur(d):
    tv = list(zip(d['time_s'], d['voltage_v']))
    for i in range(len(tv) - 1, -1, -1):
        if tv[i][1] > 2.6:
            return tv[i][0]
    return None

def charge_len(d):
    tv = list(zip(d['time_s'], d.get('voltage_v', [])))
    imin = next((i for i, (t, vol) in enumerate(tv) if vol < 2.6), None)
    iend = next((i for i in range(len(tv) - 1, -1, -1) if tv[i][1] > 4.1), None)
    if imin is None or iend is None or iend <= imin:
        return None
    return tv[iend][0] - tv[imin][0]

for v in ['v6', 'v7', 'v8']:
    base = 'runs/exp/t3_r1_noforce/cell'
    d1 = load(f'{base}/r4_{v}_1c_dfn.json')
    d5 = load(f'{base}/r4_{v}_5c_dfn.json')
    d4 = load(f'{base}/r4_{v}_4c45_dfn.json')
    e = load(f'{base}/r4_{v}_energy.json')
    cap1, cap5 = d1['capacity_ah'], d5['capacity_ah']
    ret = cap5 / cap1
    with open(f'{base}/r4_{v}_derived.json', 'w', encoding='utf-8') as f:
        json.dump({'capacity_ah': cap1, 'rate_retention_5c': ret}, f, indent=2)
    ap = d4.get('anode_potential_v', [])
    ap_min = min(ap) if ap else None
    tmax1, tmax5, tmax4 = d1['T_max_K'], d5['T_max_K'], d4['T_max_K']
    dur1, clen = discharge_dur(d1), charge_len(d4)
    print(f"{v}: 1C cap {cap1:.4f} Ah (dur {dur1:.0f} s, Tmax {tmax1:.2f} K) | 5C cap {cap5:.4f} ret {ret:.4f} Tmax {tmax5:.2f} K | 4C Tmax {tmax4:.2f} K charge {clen:.0f} s ap_min {ap_min:.4f} plated {d4.get('plated')} | PD {e['power_density_w_kg']:.0f} W/kg mass {e['mass_kg']:.4f} kg")
