import json
with open('D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run6_4c.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(min(data['anode_potential_v']))
