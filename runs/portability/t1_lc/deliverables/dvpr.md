# Design Verification Plan & Report (virtual test) — VBF-T1LC-DVPR-01

One row per verification item; result values mechanically taken from simulation outputs.

| Item | Condition | Result | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C CC discharge to 2.5 V, 25 °C | 5.030 Ah | ✓ (vs 5.0 Ah nominal) | cell/r3_V3_1c_dfn.json:capacity_ah |
| Energy density | 1C discharge energy ÷ contract mass | 413.02 Wh/kg | ✓ (≥ 392.61 Wh/kg) | cell/r3_V3_energy.json:energy_density_wh_kg |
| 4C fast-charge temperature rise | 4C charge @45 °C, lumped thermal | 328.56 K (55.4 °C) | ✓ (≤ 333.15 K) | cell/r3_V3_4c_dfn.json:T_max_K |
| 4C fast-charge plating | 4C charge @45 °C + plating module | anode_potential_v min +0.0368 V | ✓ (no value < 0 V) | cell/r3_V3_4c_dfn.json:anode_potential_v |
| Overcharge to 4.7 V thermal runaway | 0.5C charge to 4.7 V → run-tr | triggered = false | ✓ (no TR) | cell/r3_V3_tr.json:triggered |
| Voltage window | upper/lower cut-off | 4.2 V / 2.5 V | ✓ (per design) | parameter set |
| Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| Crush / drop / external short | — | N/A (requires physical experiment) | N/A | — |
| Cycle life (aging) | — | N/A (aging model not run for this case) | N/A | — |
| Rate-pulse internal resistance | — | N/A (not in simulation protocol set) | N/A | — |

## Conclusion

- Passed virtual verification: 1C capacity, energy density, 4C temperature rise, 4C plating, overcharge-to-4.7 V thermal runaway, voltage window.
- Uncovered (paper limitations): nail penetration, crush/drop, cycle-life aging, rate-pulse DCR — require physical experiment or aging simulation.
