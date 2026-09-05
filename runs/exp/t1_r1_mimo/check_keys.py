import json
with open(r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_mimo\run3_4c.json', encoding='utf-8') as f:
    data = json.load(f)
print("Keys:", list(data.keys()))
print("T_max_K:", data.get('T_max_K'))
print("plated:", data.get('plated'))
