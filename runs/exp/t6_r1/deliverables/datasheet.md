# Technical Datasheet — VBF-T6R1-DSH-01

LNMO/graphite high-voltage smartphone cell — virtual design (DFN simulation fidelity)

| Field | Value | Source |
|---|---|---|
| Rated capacity | 6.20 Ah (1C, simulation-verified); parameter-set nominal 4.5 Ah | cell/r8_d6_1c_dfn.json:capacity_ah; parameter set |
| Nominal voltage / window | 4.11 V plateau midpoint; window 2.5 – 4.7 V | cell/r8_d6_energy_dfn.json:midpoint_voltage_v; parameter set |
| Rated energy | 25.41 Wh | cell/r8_d6_energy_dfn.json:energy_wh |
| Volumetric energy density | 1135.8 Wh/L | cell/r8_d6_energy_dfn.json:energy_density_wh_l |
| Gravimetric energy density | 493.3 Wh/kg (electrolyte excluded — parameter set lacks density) | cell/r8_d6_energy_dfn.json:energy_density_wh_kg |
| Maximum continuous discharge rate | 1C verified (6.198 Ah); 5C / low-temperature retention: not provided (outside contract; protocol exists, not run) | cell/r8_d6_1c_dfn.json |
| Fast-charge capability | 4C CC-CV charge at 45 °C ambient: T_max = 321.42 K (48.27 °C) ≤ 50 °C; no lithium plating (min anode potential +10.96 mV) | cell/r8_d6_4c_dfn.json |
| DC internal resistance | 6.38 mΩ (calc-energy midpoint DCR) | cell/r8_d6_energy_dfn.json:dcr_ohm |
| Power density | 13.52 kW/kg | cell/r8_d6_energy_dfn.json:power_density_w_kg |
| Operating temperature range | verified at 25 °C (1C discharge/aging) and 45 °C (4C charge); wider range not simulated | protocol definitions |
| Cycle life | 100 × 1C cycles simulated: SEI thickness 385.3 nm ≤ 500 nm target ✓. Cycle count to end-of-life: Not simulated (no capacity-fade EOL criterion in contract) | cell/r8_d6_aging_dfn.json:sei_thickness_nm_end |
| Safety determination | No plating at 4C (margin 11.0 mV); T_max margin 1.73 K below 50 °C red line; cooling requirement h = 400 W/m²K (active cooling design) | cell/r8_d6_4c_dfn.json; params_final.json |
| Dimensions | 65 mm × 1580 mm × 217.8 µm electrode stack; pouch shell thickness Not provided (not modeled) | parameter set; cell/r8_d6_energy_dfn.json |
| Mass | 51.50 g (electrolyte excluded); ≈ 57.8 g with electrolyte design estimate | cell/r8_d6_energy_dfn.json:mass_kg; design_spec §3 |

**Formulation notes (honesty):** electrolyte diffusivity 6.0e-10 m²/s is a constant override at the upper bound of reported low-viscosity fast-charge carbonate formulations (Nyman2008 baseline ≈ 2.9e-10 at 1000 mol/m³); materializing the design requires a real low-viscosity electrolyte with measured D_e in this range. EC-lean electrolyte (EC 2270.5 mol/m³) plus EC diffusivity 1.0e-18 m²/s are the SEI-control levers — an additive/solvent package must reproduce these effective values. All values are tool-output; this datasheet is a virtual-design document, not a production datasheet.
