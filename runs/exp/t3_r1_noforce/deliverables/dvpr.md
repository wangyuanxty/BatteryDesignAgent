# Design Verification Plan and Report (virtual-test version) — final design V8

**Document no.: VBF-T3R1NOFORCE-DVPR-01** · Case `exp/t3_r1_noforce` · 2026-08-25
All result values mechanically taken from simulation output files; uncovered conditions honestly written "N/A".

| # | Verification item | Condition | Result value | Determination (vs entry-0 criteria) | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C discharge, 298.15 K ambient, DFN + lumped thermal | 2.6683 Ah | PASS (≥ 2.0 Ah) | cell/r4_v8_1c_dfn.json:capacity_ah |
| 2 | 5C discharge capacity retention | 5C discharge, 298.15 K ambient, DFN | 2.6261 Ah; retention 0.9842 | PASS (≥ 0.95) | cell/r4_v8_5c_dfn.json:capacity_ah ÷ cell/r4_v8_1c_dfn.json:capacity_ah (cell/r4_v8_derived.json) |
| 3 | Power density | contract formula V_OC²/(4·DCR)/mass on 1C discharge | 73121.8 W/kg | PASS (≥ 4000 W/kg) | cell/r4_v8_energy.json:power_density_w_kg |
| 4 | 4C fast-charge temperature rise | 4C charge at 45 °C ambient, DFN + lumped thermal | T_max 323.57 K (50.4 °C) | PASS (≤ 333.15 K) | cell/r4_v8_4c45_dfn.json:T_max_K |
| 5 | 4C fast-charge plating | same as #4 + plating module; negative surface potential < 0 V → plated | anode potential min +0.0119 V → plated = false | PASS (plated = false) | cell/r4_v8_4c45_dfn.json:anode_potential_v |
| 6 | Voltage window | parameter set cut-offs | 2.5 – 4.2 V | PASS (upper bound never exceeded in protocols) | base parameter set |
| 7 | Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| 8 | Overcharge to thermal runaway | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| 9 | Crush / drop | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| 10 | Cycle life | — | N/A (requires aging model; not simulated in this case) | N/A | — |
| 11 | Rate-pulse internal resistance | — | N/A (requires physical experiment) | N/A | — |

## Conclusion

All 6 simulation-verifiable items PASS against the entry-0 criteria (mechanical `bda log-evaluate` evidence, round 4). Uncovered items (#7–#11) are beyond the pure-simulation boundary and are cited directly as paper limitations. Verification notes: the C-rate protocols run at the cell's own rated C-rates (Nominal cell capacity override, probe-verified cell/probe_nominal_1c_dfn.json); the plating margin is +11.9 mV — thin but positive, flagged in the DFMEA for production-tolerance control.
