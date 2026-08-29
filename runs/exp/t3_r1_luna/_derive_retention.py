import json
from pathlib import Path
root=Path('runs/exp/t3_r1_luna/cell')
for tag in ['r0_baseline','r1_v1','r2_v2']:
 a=json.load(open(root/(tag+'_1c.json'),encoding='utf-8')); b=json.load(open(root/(tag+'_5c.json'),encoding='utf-8'))
 out={'capacity_1c_ah':a['capacity_ah'],'capacity_5c_ah':b['capacity_ah'],'rate_retention_5C':b['capacity_ah']/a['capacity_ah'],'source_1c':tag+'_1c.json:capacity_ah','source_5c':tag+'_5c.json:capacity_ah'}
 json.dump(out,open(root/(tag+'_retention.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=2)
