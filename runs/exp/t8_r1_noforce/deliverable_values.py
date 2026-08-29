import json
base = 'runs/exp/t8_r1_noforce/cell/'
out = {}
for tag, f in [('energy', 'r6_v9_energy.json'), ('d1c', 'r6_v9_1c_dfn.json'),
               ('d5c', 'r6_v9_5c_dfn.json'), ('c4', 'r6_v9_4c_charge45_plating.json'),
               ('ret', 'r6_v9_retention.json')]:
    d = json.load(open(base + f, encoding='utf-8-sig'))
    keep = {k: v for k, v in d.items() if isinstance(v, (int, float, bool, str))}
    out[tag] = keep
    if 'layer_kg_m2' in d:
        out[tag]['layer_kg_m2'] = d['layer_kg_m2']
    if 'anode_potential_v' in d:
        out[tag]['anode_potential_min_v'] = min(d['anode_potential_v'])
    if 'time_s' in d:
        out[tag]['t_end_s'] = d['time_s'][-1]
print(json.dumps(out, indent=1))
