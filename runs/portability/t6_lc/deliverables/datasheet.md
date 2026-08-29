# Technical Datasheet — VBF-T6LC-DSH-01

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 4.5 (nominal); 4.804 verified | `data/LNMO.json`; `final_1c_dfn_h45.json:capacity_ah` |
| Nominal voltage / voltage window (V) | 2.5 – 4.7 | `data/LNMO.json` |
| Rated energy (Wh) | 19.94 | `final_1c_energy_dfn_h45.json:energy_wh` |
| Volumetric energy density (Wh/L) | 1005.8 | `final_1c_energy_dfn_h45.json:energy_density_wh_l` |
| Gravimetric energy density (Wh/kg) | 480.7 (electrolyte/casing excluded) | `final_1c_energy_dfn_h45.json:energy_density_wh_kg` |
| Voltage plateau (discharge midpoint, V) | 4.115 | `final_1c_energy_dfn_h45.json:midpoint_voltage_v` |
| Maximum continuous discharge rate | 1C (verified 4.804 Ah) | 1C_discharge simulation |
| Fast-charge capability | 4C at 45 ℃: T_max 322.59 K, no lithium plating (anode potential min +0.0894 V) | `final_4c_safety_h45_dfn.json` |
| Cycle life (SEI) | 100 cycles: SEI 9.5 nm (DFN) / 233 nm (SPMe); ≤ 500 nm | `final_aging_dfn_h45.json`; `R5A_aging_k1e-15.json` |
| Operating temperature range | simulated at 25 ℃ (discharge), 45 ℃ (4C charge); broader range N/A | simulation protocols |
| Safety determination | no plating at 4C; T_max 322.59 K ≤ 50 ℃ | `final_4c_safety_h45_dfn.json` |
| Dimensions | electrode strip 65 mm × 1580 mm × 0.193 mm (unwound); pouch shell Not provided | parameter set |
| Mass | 41.48 g (excl. electrolyte/casing); +6.2 g electrolyte (literature density) | `final_1c_energy_dfn_h45.json:mass_kg` |
| DC resistance (10% discharge) | 7.0 mΩ | `final_1c_energy_dfn_h45.json:dcr_ohm` |
| Chemistry | LNMO spinel / graphite | `data/LNMO.json` |
