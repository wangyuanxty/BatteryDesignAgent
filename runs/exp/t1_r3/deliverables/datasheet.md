# Technical Datasheet — V11 Cell (t1_r3)

**Document number**: VBF-EXPT1R3-DSH-01
**Date**: 2026-08-26
**Note**: virtual design datasheet; every value mechanically taken from the parameter set / simulation outputs (`runs/exp/t1_r3/cell/r5_v11_*.json`). This is a simulation-caliber datasheet, not a production release.

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 5.085 nominal; 5.0849 simulation-verified (1C, 25 °C) | `r5_v11_final.json` / `r5_v11_1c_spme.json:capacity_ah` |
| Nominal voltage / window (V) | 4.130 V midpoint; 2.5 – 4.2 V window | `r5_v11_energy.json:midpoint_voltage_v` / Chen2020 cut-offs |
| Rated energy (Wh) | 18.622 | `r5_v11_energy.json:energy_wh` |
| Energy density (Wh/kg) | 605.33 | `r5_v11_energy.json:energy_density_wh_kg` |
| Volumetric energy density (Wh/L) | 981.20 | `r5_v11_energy.json:energy_density_wh_l` |
| Maximum continuous discharge rate | 1C (5.085 A) verified by simulation; higher rates not simulated | `r5_v11_1c_spme.json` |
| Fast-charge capability | 4C (20.34 A): 92.0% of capacity in 13.8 min, anode potential min +0.0425 V (no plating), T_max 321.2 K at 45 °C ambient | `r5_v11_4c.json` |
| Operating temperature range | Verified 25 °C (1C discharge, 298.15 K ambient) and 45 °C ambient (4C charge, 318.15 K ambient); beyond this range not simulated | protocol conditions (runner PROTOCOLS) |
| Cycle life | **Not simulated (requires aging model) — not fabricated** | — |
| Safety determination | 4C plating: none (anode +0.0425 V); 4C T_max 321.2 K ≤ 333.15 K; overcharge 0.5C to 4.70 V: T_max 298.57 K, thermal-runaway triggered = false | `r5_v11_4c.json`, `r5_v11_oc.json`, `r5_v11_tr.json` |
| Dimensions and mass | single-layer stack: 65 mm × 1580 mm × 184.8 µm; 30.76 g (contract caliber, electrolyte excluded); 40.77 g incl. electrolyte; shell dims not parameterized | Chen2020 geometry + `r5_v11_energy.json` |
| Internal resistance (DCR) | 19.25 µΩ (from 1C curve) | `r5_v11_energy.json:dcr_ohm` |
