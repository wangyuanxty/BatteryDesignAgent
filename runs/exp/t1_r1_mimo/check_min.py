import json
with open(r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_mimo\run1_4c.json') as f:
    data = json.load(f)
print(min(data['anode_potential_v']))
