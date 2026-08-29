# Technical Datasheet — VBF-T1R1-DSH-01

Case: t1_r1 | Date: 2026-08-25 | Prepared: ____________ | Reviewed: ____________ | Approved: ____________

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah nominal (parameter); 5.6505 Ah simulated 1C discharge | Chen2020 "Nominal cell capacity [A.h]"; cell/r3_I_1c.json:capacity_ah |
| Nominal voltage | 4.0067 V (discharge midpoint) | cell/r3_I_energy.json:midpoint_voltage_v |
| Voltage window | 2.5 – 4.2 V | Chen2020 cut-off parameters |
| Rated energy | 19.967 Wh | cell/r3_I_energy.json:energy_wh (V·I time integration) |
| Energy density | 553.98 Wh/kg; 905.98 Wh/L | cell/r3_I_energy.json:energy_density_wh_kg / energy_density_wh_l (contract mass caliber: layer stack, electrolyte excluded) |
| Maximum continuous discharge | 1C (5.0 A); verified 5.6505 Ah at 1C, 298.15 K ambient, peak temperature 299.55 K | cell/r3_I_1c.json (protocol 1C_discharge) |
| Fast-charge capability | 4C (20 A) CC charge: peak cell temperature 325.65 K (52.51 °C, ambient 318.15 K, rise +7.50 K); no lithium plating (anode potential min +0.0249 V) | cell/r3_I_4c_dfn.json (DFN authoritative; SPMe corroborates min +0.0135 V) |
| DC internal resistance | 0.155 mΩ (mechanical derivation: (V[0] − V[10% t]) / I_1C) | cell/r3_I_energy.json:dcr_ohm |
| Peak power density | 748.3 kW/kg (P = V_OC2/(4·R_DC), per mass) | cell/r3_I_energy.json:power_density_w_kg |
| Operating temperature range | 298.15 K discharge / 318.15 K 4C charge simulated; wider range not simulated (honest statement) | protocol definitions (1C_discharge, 4C_charge_45C) |
| Cycle life | Not simulated (requires aging model) — must not be fabricated | — |
| Safety determination | Overcharge to 4.7000 V: no thermal runaway (triggered = false, peak 299.55 K); 4C charge below 60 °C red line | cell/r3_I_oc.json; cell/r3_I_tr.json; cell/r3_I_4c_dfn.json |
| Dimensions | Electrode sheet 65 mm × 1580 mm; stack thickness 214.6 µm; shell dimensions Not provided | Chen2020 geometry; cell/r3_I_energy.json:thickness_m |
| Mass | 36.044 g stack (contract caliber, electrolyte excluded); 45.43 g with electrolyte fill (1.2 g/cm3 literature density) | cell/r3_I_energy.json:mass_kg; pore-volume derivation (see design_spec section 3) |
| Chemistry | NMC811 / graphite; high-conductivity high-t+ electrolyte (σ = 1.8 S/m estimate, t+ = 0.55 estimate) | Chen2020 + params_r3_I.json |
