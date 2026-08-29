# Technical Datasheet — V4b "h60 + anode margin" (VBF-T1R2-DSH-01)

Next-generation pure electric sedan cell — NMC811 / graphite (Chen2020 parameter set).

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah (nominal); 5.6997 Ah (simulation-verified 1C discharge) | parameter set `Nominal cell capacity [A.h]`; `cell/r4_v4b_1c_spme.json:capacity_ah` |
| Nominal voltage | 4.086 V (1C midpoint) | `cell/r4_v4b_energy.json:midpoint_voltage_v` |
| Voltage window | 2.5 – 4.2 V | parameter set `Lower/Upper voltage cut-off [V]` |
| Rated energy | 20.55 Wh | `cell/r4_v4b_energy.json:energy_wh` |
| Energy density | 583.2 Wh/kg (contract caliber, electrolyte excluded); 478.7 Wh/kg incl. electrolyte estimate | `cell/r4_v4b_energy.json:energy_density_wh_kg`; electrolyte-incl. `inferred` (20.553 Wh / 0.04293 kg, electrolyte density 1.2 g/cm³ literature `estimate`) |
| Volumetric energy density | 1028.4 Wh/L | `cell/r4_v4b_energy.json:energy_density_wh_l` |
| DCR | 80.4 µΩ | `cell/r4_v4b_energy.json:dcr_ohm` (1C-point estimate) |
| Power density | 1498.5 kW/kg | `cell/r4_v4b_energy.json:power_density_w_kg` (contract-caliber formula) |
| Maximum continuous discharge rate | 1C (5 A) — simulated | `cell/r4_v4b_1c_spme.json` |
| Fast-charge capability | 4C CC charge: T_max 326.5 K, no lithium plating (anode potential min +0.0215 V), CC acceptance 4.53 Ah (79% SOC) | `cell/r4_v4b_4c_dfn.json` (`T_max_K`, `anode_potential_v` min); acceptance `inferred`: 815 s × 20 A / 3600 |
| Operating temperature range | Simulated at 298.15 K ambient (25 °C); 4C fast charge verified to cell T_max 326.5 K with h = 60 W/m²·K cooling. Low-temperature performance: not simulated in this case | protocol `T_amb_K`; sim outputs; honest scope statement |
| Cycle life | Not simulated (durability not in this case's criteria; the Chen2020 set is aging-capable — SEI kinetic rate constant 1e-12 m/s — and the aging protocol is available for a follow-up round). Must not be read as a cycle-life claim | — |
| Safety | 4C: plated = false, T_max ≤ 333.15 K pass. Overcharge to 4.7 V (0.5C): T_max 299.4 K, thermal-runaway trigger = false (lumped 0-D model). Nail/crush/drop: N/A (beyond pure simulation boundary, requires physical experiment) | `cell/r4_v4b_4c_dfn.json`, `cell/r4_v4b_overcharge.json`, `cell/r4_v4b_tr.json` |
| Dimensions | Electrode area 0.1027 m²; electrode stack thickness 194.6 µm; design cell volume 2.514e-5 m³ (thermal sim). Height × width: Not provided (cell can not modeled) | `cell/r4_v4b_energy.json`; `cell/params_v4b.json` |
| Mass | 35.24 g (contract caliber, electrolyte excluded); 42.93 g incl. electrolyte estimate | `cell/r4_v4b_energy.json:mass_kg`; §3/§4 of design_spec.md |

Evidence: all safety/performance determinations above are mechanical `bda log-evaluate` round-4 verdicts (pass), recorded in `log.jsonl`.
