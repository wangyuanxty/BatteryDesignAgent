import json
with open(r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_mimo\run3_4c.json', encoding='utf-8') as f:
    data = json.load(f)
with open(r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_mimo\run1_energy.json', encoding='utf-8') as f:
    energy = json.load(f)

print(json.dumps({
    "sim": data,
    "mass_kg": energy['mass_kg'],
    "t_init": data['T_max_K']
}, indent=2))
