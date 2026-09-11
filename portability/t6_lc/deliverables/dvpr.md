# Design Verification Plan & Report (virtual-test) — VBF-T6LC-DVPR-01

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C CC discharge, 298.15 K, DFN | 4.804 Ah | PASS (≥ nominal 4.5 Ah) | `cell/final_1c_dfn_h45.json:capacity_ah` |
| Volumetric energy density | contract-caliber stack formula | 1005.8 Wh/L | PASS (≥ 950 Wh/L) | `cell/final_1c_energy_dfn_h45.json:energy_density_wh_l` |
| Voltage plateau | discharge-time midpoint | 4.115 V | PASS (≥ 4.1 V) | `cell/final_1c_energy_dfn_h45.json:midpoint_voltage_v` |
| 4C fast-charge temperature rise | 4C charge, 45 ℃, lumped thermal, DFN | 322.59 K (49.44 ℃) | PASS (≤ 323.15 K / 50 ℃) | `cell/final_4c_safety_h45_dfn.json:T_max_K` |
| 4C fast-charge plating | `--plating`, anode surface potential | min +0.0894 V | PASS (≥ 0 V, no plating) | `cell/final_4c_safety_h45_dfn.json:anode_potential_v` |
| Anode SEI thickness after 100 cycles | 1C aging 100 cycles, DFN (and SPMe) | 9.5 nm (DFN) / 233 nm (SPMe) | PASS (≤ 500 nm) | `cell/final_aging_dfn_h45.json:sei_thickness_nm_end` |
| Voltage window | parameter set | 2.5 – 4.7 V | PASS (system definition) | `data/LNMO.json` |

Items explicitly N/A (beyond pure-simulation boundary, require physical experiment): nail penetration, overcharge-to-thermal-runaway, crush, drop, rate-pulse internal resistance, long-term calendar life.

## Conclusion

All six simulated verification items PASS against the entry-0 criteria. Uncovered physical-abuse items are listed above and are outside the virtual-test boundary.
