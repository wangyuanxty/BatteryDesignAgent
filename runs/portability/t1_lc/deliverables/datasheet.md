# Technical Datasheet — VBF-T1LC-DSH-01

Next-generation pure-electric sedan cell (virtual design). Values mechanically taken from parameter set / simulation outputs.

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah (nominal); 5.03 Ah (simulation-verified) | parameter set / cell/r3_V3_1c_dfn.json |
| Nominal voltage (plateau) | 3.82 V | cell/r3_V3_energy.json:midpoint_voltage_v |
| Voltage window | 2.5 – 4.2 V | parameter set |
| Rated energy | 17.95 Wh | cell/r3_V3_energy.json:energy_wh |
| Energy density (gravimetric) | 413.02 Wh/kg | cell/r3_V3_energy.json:energy_density_wh_kg |
| Energy density (volumetric, contract) | 870.31 Wh/L | cell/r3_V3_energy.json:energy_density_wh_l |
| Maximum continuous discharge | 1C (5.03 A) | 1C discharge simulation |
| Fast-charge capability | 4C charge: T_max 55.4 °C, no lithium plating | cell/r3_V3_4c_dfn.json |
| DC resistance | 3.38 mΩ | cell/r3_V3_energy.json:dcr_ohm |
| Power density (theoretical peak) | 28.33 kW/kg | cell/r3_V3_energy.json:power_density_w_kg |
| Operating temperature range | discharge 25 °C; fast charge 45 °C ambient (simulated conditions) | simulation protocol |
| Cycle life | Not simulated (aging model not run for this case) | honest N/A |
| Safety determination | no plating at 4C; T_max ≤ 60 °C; overcharge 4.7 V no thermal runaway | cell/r3_V3_4c_dfn.json / cell/r3_V3_tr.json |
| Dimensions | electrode sheet 65 mm × 1580 mm; total layer thickness 200.8 µm; shell not provided | parameter set / energy output |
| Mass | 43.45 g (contract caliber, electrolyte excluded) | cell/r3_V3_energy.json:mass_kg |

Notes:
- Gravimetric energy density is contract caliber: discharge energy ÷ layer mass (electrode active + current collectors + separator), electrolyte and casing excluded.
- Cycle life and physical-abuse items require physical experiment / aging simulation not run here; reported honestly as not provided.
