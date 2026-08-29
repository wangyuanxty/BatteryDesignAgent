import json
pairs = [['v4', 'runs/exp/t8_r1_noforce/cell/r3_v4_1c_dfn.json', 'runs/exp/t8_r1_noforce/cell/r3_v4_5c_dfn.json'],
         ['v5', 'runs/exp/t8_r1_noforce/cell/r3_v5_1c_dfn.json', 'runs/exp/t8_r1_noforce/cell/r3_v5_5c_dfn.json'],
         ['v6', 'runs/exp/t8_r1_noforce/cell/r3_v6_1c_dfn.json', 'runs/exp/t8_r1_noforce/cell/r3_v6_5c_dfn.json']]
for tag, f1, f5 in pairs:
    q1 = json.load(open(f1, encoding='utf-8-sig'))['capacity_ah']
    q5 = json.load(open(f5, encoding='utf-8-sig'))['capacity_ah']
    json.dump({'capacity_retention_5c': q5/q1, 'q_1c_ah': q1, 'q_5c_ah': q5},
              open(f'runs/exp/t8_r1_noforce/cell/r3_{tag}_retention.json', 'w', encoding='utf-8'), indent=1)
    print(tag, 'retention', round(q5/q1, 4), 'q1', round(q1, 3), 'q5', round(q5, 3))
