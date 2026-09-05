import json

# Read energy density files
for label, path in [
    ('ArchD_1C_energy', 'runs/exp/t8_r1_mimo/cell/r3_archD_1c_energy.json'),
    ('ArchE_1C_energy', 'runs/exp/t8_r1_mimo/cell/r3_archE_1c_energy.json'),
]:
    d = json.load(open(path, encoding='utf-8'))
    print(f"{label}: ED={d['energy_density_wh_kg']:.1f} Wh/kg, mass={d['mass_kg']*1000:.1f}g, cap={d['capacity_ah']:.3f}Ah")

# Read 5C discharge
for label, path in [
    ('ArchD_5C', 'runs/exp/t8_r1_mimo/cell/r3_archD_5c.json'),
    ('ArchE_5C', 'runs/exp/t8_r1_mimo/cell/r3_archE_5c.json'),
]:
    d = json.load(open(path, encoding='utf-8'))
    print(f"{label}: cap={d['capacity_ah']:.4f}Ah, T_max={d.get('T_max_K','N/A')}")

# Read 1C discharge for capacity
for label, path in [
    ('ArchD_1C', 'runs/exp/t8_r1_mimo/cell/r3_chen2020_archD_1c.json'),
    ('ArchE_1C', 'runs/exp/t8_r1_mimo/cell/r3_chen2020_archE_1c.json'),
]:
    d = json.load(open(path, encoding='utf-8'))
    print(f"{label}: cap={d['capacity_ah']:.4f}Ah, T_max={d.get('T_max_K','N/A')}")
