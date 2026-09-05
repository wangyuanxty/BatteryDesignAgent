import json
with open(r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_mimo\run3_4c.json') as f:
    data = json.load(f)
print("T_max_K:", data.get('T_max_K'))
print("plated:", data.get('plated'))
if 'anode_potential_v' in data:
    print("Anode min:", min(data['anode_potential_v']))
