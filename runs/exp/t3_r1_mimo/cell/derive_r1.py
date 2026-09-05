import json

ws = r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_mimo\cell'

# Load all outputs
with open(f'{ws}/r1_baseline_1c.json', encoding='utf-8') as f:
    c1c = json.load(f)
with open(f'{ws}/r1_baseline_5c.json', encoding='utf-8') as f:
    c5c = json.load(f)
with open(f'{ws}/r1_energy.json', encoding='utf-8') as f:
    energy = json.load(f)
with open(f'{ws}/r1_4c_charge.json', encoding='utf-8') as f:
    c4c = json.load(f)

# Derive 5C retention
retention_5c = c5c['capacity_ah'] / c1c['capacity_ah']

ap_min = min(c4c.get('anode_potential_v', [1])) if c4c.get('anode_potential_v') else None
plated = ap_min is not None and ap_min < 0

# Combined derived metrics
derived = {
    'capacity_ah': c1c['capacity_ah'],
    'energy_wh': energy['energy_wh'],
    'mass_kg': energy['mass_kg'],
    'energy_density_wh_kg': energy['energy_density_wh_kg'],
    'volume_m3': energy['volume_m3'],
    'energy_density_wh_l': energy['energy_density_wh_l'],
    'thickness_m': energy['thickness_m'],
    'midpoint_voltage_v': energy['midpoint_voltage_v'],
    'dcr_ohm': energy['dcr_ohm'],
    'power_density_w_kg': energy['power_density_w_kg'],
    'area_m2': energy['area_m2'],
    'five_c_retention': retention_5c,
    'five_c_capacity_ah': c5c['capacity_ah'],
    'one_c_capacity_ah': c1c['capacity_ah'],
    'T_max_K': c4c['T_max_K'],
    'plated': plated,
    'anode_potential_v_min': ap_min,
    'electrolyte_included': False,
    'model_used_1c': c1c['model_used'],
    'model_used_5c': c5c['model_used'],
    'model_used_4c': c4c['model_used']
}

with open(f'{ws}/r1_derived.json', 'w', encoding='utf-8') as f:
    json.dump(derived, f, indent=2)

print('5C retention:', f'{retention_5c:.4f} ({retention_5c*100:.2f}%)')
print('Capacity:', derived['capacity_ah'], 'Ah')
print('Power density:', derived['power_density_w_kg'], 'W/kg')
print('T_max:', derived['T_max_K'], 'K')
print('Plated:', derived['plated'])
print('Anode V min:', derived['anode_potential_v_min'])
