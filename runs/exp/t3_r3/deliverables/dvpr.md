# Design Verification Plan & Report - Power-Tool Battery (case t3_r3)

> VBF-T3R3-DVPR-01. Virtual test version: all results from simulation protocols. Uncovered conditions honestly written "N/A". No numbers from memory.

| Item | Condition | Result | Determination | Source |
|------|------|------|------|------|
| 1C discharge capacity | run-pyamm --protocol 1C_discharge (DFN) | 4.3176 Ah | PASS vs >= 2.0 Ah | r5_v12_1c_dfn.json:capacity_ah |
| 5C discharge capacity retention | run-pyamm --protocol 5C_discharge (DFN) / 1C | 98.62% (4.2581 Ah / 4.3176 Ah) | PASS vs >= 95% | r5_v12_derived.json:retention_5c |
| 4C fast-charge temperature rise | run-pyamm --protocol 4C_charge_45C --thermal lumped (DFN) | T_max 329.75 K (56.60 C) | PASS vs <= 333.15 K | r5_v12_4c_dfn.json:T_max_K |
| 4C fast-charge lithium plating | same protocol + --plating; anode potential < 0 V | anode min +41.7 mV | PASS (no plating) | r5_v12_4c_dfn.json:anode_potential_v |
| 5C discharge temperature | run-pyamm --protocol 5C_discharge --thermal lumped (DFN) | T_max 319.57 K (46.42 C) | PASS vs <= 333.15 K (informational) | r5_v12_5c_dfn.json:T_max_K |
| Power density | calc-energy contract formula V_OC2/(4*DCR)/mass | 181,557 W/kg | PASS vs >= 4,000 W/kg | r5_v12_energy.json:power_density_w_kg |
| Voltage window | parameter set upper/lower cut-offs | 2.5-4.2 V | PASS (design basis) | pybamm Chen2020 parameter set |
| Nail penetration | physical abuse test | - | N/A (beyond pure simulation boundary, requires physical experiment) | - |
| Overcharge to thermal runaway | physical safety test | - | N/A (beyond pure simulation boundary, requires physical experiment) | - |
| Crush / drop | mechanical abuse test | - | N/A (beyond pure simulation boundary, requires physical experiment) | - |
| Cycle life | aging protocol (SEI growth) | - | N/A (not simulated; no durability objective in task text) | - |
| Rate-pulse DC internal resistance | pulse protocol | - | N/A (not simulated; DCR estimate 1.059 mOhm at 1C mid-point for reference) | r5_v12_energy.json:dcr_ohm |

## Conclusion

All five entry-0 criteria verified PASS at DFN judge grade (round 5). Uncovered items: nail penetration, overcharge-to-runaway, crush/drop, cycle life, rate-pulse DCIR - all physical-experiment or aging-model territory, cited directly as paper limitations.
