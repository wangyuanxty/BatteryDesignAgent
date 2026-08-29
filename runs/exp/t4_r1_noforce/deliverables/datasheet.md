# Technical Datasheet — V10a_final_h45 (extreme-cold equipment battery)

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah nominal (parameter set); 5.0618 Ah simulation-verified at 1C | Chen2020 set; r6_final_1c_dfn.json:capacity_ah |
| Nominal voltage / window | 3.89 V discharge midpoint; 2.5 – 4.2 V | r6_final_energy_dfn.json:midpoint_voltage_v; Chen2020 cut-offs |
| Rated energy | 18.400 Wh (V·I time integration of 1C discharge) | r6_final_energy_dfn.json:energy_wh |
| Energy density | 564.84 Wh/kg (contract caliber, electrolyte excluded from mass) | r6_final_energy_dfn.json:energy_density_wh_kg |
| Volumetric energy density | 969.50 Wh/L (layer-stack volume, electrolyte/casing excluded) | r6_final_energy_dfn.json:energy_density_wh_l |
| DC resistance | 3.367 mOhm (OCV − V@10% discharge over I_1C) | r6_final_energy_dfn.json:dcr_ohm |
| Maximum continuous discharge rate | 1C (simulation protocol; higher rates not simulated) | r6_final_1c_dfn.json |
| Fast-charge capability | 4C at 45 C: T_max 329.33 K (limit 333.15 K), no lithium plating (anode min +28.96 mV) | r6_final_4C45_safety_dfn.json |
| Low-temperature performance | -20 C 1C retention 0.9944 (5.0337 Ah) | derived_r6_final_dfn.json |
| Operating temperature range | simulated at -20 C and 45 C ambient; intermediate temperatures not simulated | lowT_discharge / 4C_charge_45C protocols |
| Cycle life | Not simulated (requires aging model) — not fabricated | |
| Safety determination | no plating at 4C/45C; max temperature below 333.15 K red line | r6_final_4C45_safety_dfn.json |
| Dimensions and mass | electrode sheet 65 mm x 1580 mm; stack thickness 184.8 um; mass 32.58 g (contract caliber, electrolyte excluded; +7.98 g electrolyte estimate) | Chen2020 set; r6_final_energy_dfn.json |
| Cooling requirement | total heat transfer coefficient 45 W/m2K (design value) | params_r6_v10a_h45.json |
