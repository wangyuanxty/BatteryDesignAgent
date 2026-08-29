# Technical Datasheet — VBF Power-Tool Cell (V4 Margin-fix)

Case: t3_r1_flash | Generation date: 2026-08-25 | Doc: VBF-T3R1FLASH-DSH-01

| Field | Value | Source |
|---|---|---|
| Rated capacity | 3.44 Ah (nominal 3.438 Ah simulated at 1C, DFN) | r2_v4_1c_dfn.json:capacity_ah |
| Nominal voltage | midpoint 3.88 V | r2_v4_energy.json:midpoint_voltage_v |
| Voltage window | 2.5 – 4.2 V | parameter set |
| Rated energy | 12.42 Wh | r2_v4_energy.json:energy_wh (∫V·I dt) |
| Gravimetric energy density | 410 Wh/kg | r2_v4_energy.json (contract caliber; electrolyte/casing excluded) |
| Volumetric energy density | 864 Wh/L | r2_v4_energy.json |
| Power density (theoretical peak, P=V²/4R) | 111,807 W/kg | r2_v4_energy.json:power_density_w_kg |
| DC resistance (1C, first 10% time) | 1.26 mΩ | r2_v4_energy.json:dcr_ohm |
| Max continuous discharge rate | 5C with 98.7% capacity retention | r2_v4_5c_dfn.json + derived |
| Fast-charge capability (4C @45 °C) | CC-phase no lithium plating (anode min +22.6 mV); T_max 48.8 °C | r2_v4_4c_dfn.json |
| 4C CC-phase charge acceptance | 0.617 Ah before 4.2 V cutoff (CV would complete; honest note) | r2_v4_4c_dfn.json:capacity_ah |
| Operating temperature range | Per simulation: charge tested at 45 °C ambient; discharge at 25 °C | protocol conditions (honest: full range not characterized) |
| Cycle life | Not simulated (no aging criterion in task; requires aging model run) | honest annotation |
| Safety determination | Plating: NO (anode potential > 0 V throughout 4C charge); T_max 48.8 °C < 60 °C limit | r2_v4_4c_dfn.json |
| Dimensions | 65 mm × 1580 mm strip, stack 0.14 mm (shell not modeled) | parameter set + calc-energy |
| Mass | 30.30 g (contract layer mass; +5.5 g electrolyte estimate = 35.8 g) | r2_v4_energy.json:mass_kg |
| Chemistry | NMC-type cathode / graphite anode; high-transport LiPF6-class electrolyte (σ 2.4 S/m, t⁺ 0.5) | params_r2_v4.json |
