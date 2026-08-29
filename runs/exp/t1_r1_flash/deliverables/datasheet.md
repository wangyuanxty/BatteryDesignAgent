# Technical Datasheet — VBF-T1R1FLASH-DSH-01

Next-generation BEV sedan cell · NMC811 / graphite+SiOx · Generation date: 2026-08-25

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 5.0 nominal (parameter set) / 4.936 verified (1C DFN) | OKane2022 params; cell/final_1c_dfn.json:capacity_ah |
| Nominal voltage / window (V) | 3.56 midpoint / 2.5–4.2 | cell/final_energy.json:midpoint_voltage_v; parameter set |
| Rated energy (Wh) | 17.51 (1C discharge integration) | cell/final_energy.json:energy_wh |
| Energy density (Wh/kg) | 459.4 (contract caliber, electrolyte excluded) / 893.5 Wh/L | cell/final_energy.json |
| Maximum continuous discharge rate | 1C verified (4.936 Ah delivered at 1C) | cell/final_1c_dfn.json |
| Fast-charge capability | 4C @45 °C ambient: T_max 50.2 °C (≤60 °C), no plating (anode min +0.0114 V) | cell/archA_h150_f4b_4c.json |
| Required cooling | liquid cooling h ≥ 120 W/m²·K (design point 150); without it T_max 94 °C at h=10 | baseline_4c vs final_4c |
| Operating temperature range | Simulation conditions only: 25 °C (1C), 45 °C (4C); wider range not simulated | — |
| Cycle life | Not simulated (aging protocol not in task scope); no fabricated value | — |
| Safety determination | Overcharge to 4.7 V: thermal runaway NOT triggered (ODE verdict false); plating: none at 4C | cell/final_tr.json:triggered; final_4c |
| Dimensions & mass | 1580 × 65 mm strip, stack 0.1908 mm; 38.11 g (electrolyte-excluded caliber) | parameter set; cell/final_energy.json |
| DC resistance | 20.3 mΩ (10% discharge DCR) | cell/final_energy.json:dcr_ohm |
| Power density | 5314 W/kg (V_OC²/4R ÷ mass) | cell/final_energy.json:power_density_w_kg |
