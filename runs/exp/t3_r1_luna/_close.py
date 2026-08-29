from bda.store import CaseWorkspace, append_entry
ws=CaseWorkspace('exp/t3_r1_luna',root='runs')
append_entry(ws,{'action':'endorse','skipped':True,'reason':'real_compute=false; no ORCA/MD values generated'})
append_entry(ws,{'action':'final','recommendation':'V2_high_rate Chen2020 design: 5.066 Ah nominal 1C capacity, 98.35% 5C retention, 3.18e6 W/kg contract power density, 328.63 K (55.48 C) maximum temperature during coupled 4C/45C charge, and no plating (minimum anode potential 0.02563 V). Values are tool outputs or mechanically derived files; electrolyte mass is excluded by calc-energy contract.','verdict':'achieved'})
