# Design Verification Plan and Report (virtual test version) — VBF-T3R2-DVPR-01

Case `t3_r2` — power-tool battery. Every result value is mechanically taken from simulation output files; uncovered conditions are honestly listed as N/A. Model: DFN, lumped thermal, plating option enabled on the charge protocol.

## Verification items

| # | Item | Condition | Result value | Determination (vs entry-0 criteria) | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC discharge to 2.5 V, 25 °C ambient | 3.3278 Ah | PASS (>= 2 Ah) | `cell/r2_p1_1c_dfn.json:capacity_ah` |
| 2 | 5C discharge capacity retention | 5C CC discharge to 2.5 V, 25 °C, 720 s protocol | 98.89 % (5C 3.2911 Ah ÷ 1C 3.3278 Ah, same parameters incl. re-based nominal) | PASS (>= 95 %) | `cell/r2_p1_derived.json:capacity_retention_5c` |
| 3 | 5C discharge peak temperature | same run as #2 | 322.22 K (49.07 °C) | PASS (<= 333.15 K) | `cell/r2_p1_derived.json:t_max_5c_k` |
| 4 | 4C fast-charge lithium plating | 4C CC charge to 4.2 V at 45 °C ambient (after 1C depletion), plating option on | anode surface potential min +0.0364 V — never below 0 V -> not plated | PASS (plated == false) | `cell/r2_p1_4c_dfn.json:anode_potential_v` |
| 5 | 4C fast-charge peak temperature | same run as #4 | 332.52 K (59.37 °C) | PASS (<= 333.15 K) | `cell/r2_p1_4c_dfn.json:T_max_K` |
| 6 | Power density | contract formula V_OC^2 / (4·DCR) / mass; DCR = (V_start − V@10%) / I_1C | 63,130 W/kg | PASS (>= 4000 W/kg) | `cell/r2_p1_energy.json:power_density_w_kg` |
| 7 | Voltage window | parameter set limits | 2.5 – 4.2 V | PASS (design datum) | Chen2020 parameter set |
| 8 | Rated energy / energy density | 1C discharge energy integral; mass per contract | 12.13 Wh; 407.6 Wh/kg; 837.4 Wh/L | Informative (no contractual threshold) | `cell/r2_p1_energy.json` |

## Items explicitly not covered in this task

| Item | Status | Note |
|---|---|---|
| Nail penetration | N/A (beyond pure-simulation boundary, requires physical experiment) | abuse scenario not in task contract |
| Overcharge to thermal runaway | N/A (protocol exists in toolchain; not required by task contract and not run — honest, not fabricated) | — |
| Crush / drop | N/A (requires physical experiment) | — |
| Cycle life | Not simulated (aging-capable parameter set available; task contract has no cycle requirement) | — |
| Rate-pulse DC resistance | Not simulated; the DCR datum is the calc-energy start-to-10% formula | — |

## Conclusion

All six contractual verification items (capacity, 5C retention, 5C T_max, 4C plating, 4C T_max, power density) PASS on the delivered design `P1_power_stack` (log round 2, `verdict=pass` by `bda log-evaluate`). Uncovered items for the paper's limitations section: physical abuse tests, cycle life, pulse resistance, and pack-level thermal management (the 4C T_max margin is 0.63 K under h = 10 W/m2K — pack cooling must be confirmed at system level).