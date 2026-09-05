import json
with open(r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_mimo\run3_4c.json', encoding='utf-8') as f:
    data = json.load(f)
with open(r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_mimo\run1_energy.json', encoding='utf-8') as f:
    energy = json.load(f)

with open(r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_mimo\sim.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)
