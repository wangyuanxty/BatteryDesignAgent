# Technical Datasheet — t1_r1_noforce (C7 plating-margin-robust)

VBF-T1R1NOFORCE-DSH-01 · Generation date: 2026-08-25 · Virtual design values (simulation)

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah nominal (parameter set); 5.654 Ah verified (1C CC, 25 °C, to 2.5 V) | Chen2020 dump `Nominal cell capacity [A.h]`; `cell/r6_c7_1c_spme.json:capacity_ah` |
| Nominal voltage / window | 2.5 – 4.2 V; discharge midpoint 4.1146 V | Chen2020 dump; `cell/r6_c7_energy.json:midpoint_voltage_v` |
| Rated energy | 20.472 Wh (∫V·I dt of 1C discharge) | `cell/r6_c7_energy.json:energy_wh` |
| Energy density | 457.93 Wh/kg; 946.52 Wh/L (contract formula; electrolyte excluded from mass/volume) | `cell/r6_c7_energy.json` |
| Maximum continuous discharge rate | 1C verified (5.654 Ah); 5C not simulated | `cell/r6_c7_1c_spme.json` |
| Fast-charge capability | 4C CC at 45 °C: 4.63 Ah (81.9 % SOC) in ≈836 s (13.9 min); T_max 318.79 K; **no lithium plating** (anode potential min +0.00824 V SPMe / +0.00515 V DFN) | `cell/r6_c7_4c.json`, `cell/r6_c7_4c_dfn.json` |
| DC resistance | 4.029e-5 Ω (contract caliber, from 1C curve); power density 2.376 MW/kg (contract formula V_OC²/(4·DCR)/mass — idealized figure) | `cell/r6_c7_energy.json:dcr_ohm` |
| Operating temperature range | Simulated conditions: 25 °C (1C, overcharge) and 45 °C (4C charge). Low temperature: Not simulated (−20 °C protocol available) | honest scope statement |
| Cycle life | Not simulated (aging model available on Chen2020 but not in task scope; must not fabricate) | honest scope statement |
| Safety determination | Overcharge to 4.7 V: thermal runaway **not triggered** (three-side-reaction ODE, T_max 298.22 K, dT/dt max −8.6e-7 K/s). 4C temperature rise 0.64 K above 45 °C ambient (318.79 K), well below 60 °C limit | `cell/r6_c7_oc.json`, `validation/r6_c7_tr.json`, `cell/r6_c7_4c.json` |
| Dimensions and mass | Electrode 65 mm × 1580 mm (unwound); stack thickness 210.6 µm; shell dimensions Not provided. Mass 44.705 g (contract, electrolyte excluded); 51.448 g incl. electrolyte estimate (1.2 g/cm³ literature density) | Chen2020 dump; `cell/r6_c7_energy.json` |
| System | NMC811 / graphite, single-crystal cathode 1.2 µm, fine graphite anode 0.8 µm, EC/EMC + LiPF6 (σ 1.8 S/m, D 5e-10 m²/s, t⁺ 0.5) | `cell/r6_c7_params.json` |
