# Design Verification Plan and Report (virtual test version) — VBF-T6R1NOCEILING-DVPR-01

Design under verification: ED-Compact B-p (Chen2020 NMC811/graphite; compaction + dead-layer thinning + 4 µm negative particles; nominal 5.6 Ah). All results from simulation output files (mechanical values); uncovered conditions honestly N/A.

| # | Verification item | Condition | Result value | Determination (vs entry-0 criteria) | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | `1C_discharge`, SPMe, 25 °C | 5.3222 Ah (nominal 5.6 Ah, −5%) | reporting item; nominal reconciliation noted | `cell/r2_bp_1c.json:capacity_ah` |
| 2 | Volumetric energy density | contract caliber (electrolyte excluded) | 964.44 Wh/L | **PASS** (≥ 950) | `cell/r2_bp_energy.json:energy_density_wh_l` |
| 3 | Gravimetric energy density | contract caliber | 469.06 Wh/kg | reporting item | `cell/r2_bp_energy.json:energy_density_wh_kg` |
| 4 | Voltage plateau | discharge-time midpoint | 3.9214 V | **FAIL** (< 4.1) | `cell/r2_bp_energy.json:midpoint_voltage_v` |
| 5 | 4C fast-charge temperature rise | `4C_charge_45C`, DFN, lumped thermal, 45 °C ambient, h = 10 | T_max = 351.004 K (77.9 °C) | **FAIL** (> 323.15 K); family datum at h = 25: B 338.7 K — still FAIL | `cell/r2_bp_4c.json:T_max_K`; `cell/r3_bh25_4c.json:T_max_K` |
| 6 | 4C fast-charge plating | same, with plating module | anode potential min = −0.2566 V → plated = true | **FAIL** (must be false) | `cell/r2_bp_4c.json:anode_potential_v` |
| 7 | 4C charge acceptance | same | 0.096 Ah charged at 4C before 4.2 V limit | reporting item (poor fast-charge support, honestly recorded) | `cell/r2_bp_4c.json:capacity_ah` |
| 8 | Anode SEI after 100 cycles | `aging_1C_100cyc`, SPMe, isothermal, 25 °C | 417.74 nm | **PASS** (≤ 500) | `cell/r4_bp_aging.json:sei_thickness_nm_end` |
| 9 | Voltage window | parameter set | 2.5 – 4.2 V | reporting item | Chen2020 parameter set |
| 10 | DC resistance | 10%-discharge definition | 0.364 mΩ | reporting item | `cell/r2_bp_energy.json:dcr_ohm` |
| 11 | Nail penetration | — | N/A | N/A (beyond pure-simulation boundary, requires physical experiment) | — |
| 12 | Overcharge to thermal runaway | — | N/A | N/A (beyond pure-simulation boundary) | — |
| 13 | Crush / drop / vibration | — | N/A | N/A (requires physical experiment) | — |
| 14 | Cycle life to 80% capacity | — | Not simulated (aging protocol = 100 cycles; capacity trajectory shows climb-then-saturate artifact — annotated, not treated as normal degradation) | N/A | `cell/r4_bp_aging.json:capacity_ah_per_cycle` |

## Conclusion

- PASS items: 2 of 5 acceptance metrics (volumetric ED ≥ 950 Wh/L; SEI ≤ 500 nm after 100 cycles) plus reporting items 1, 3, 9, 10.
- FAIL items: voltage plateau (3.9214 V < 4.1 V), 4C plating (plated = true), 4C/45 °C T_max (351.0 K > 323.15 K at h = 10; 338.7 K at h = 25).
- Uncovered items: 11–14 (physical-experiment territory), 4C acceptance beyond 0.096 Ah (voltage-limited), B-p SEI at elevated temperature (45 °C aging protocol not run for this candidate).
- Overall: design does not satisfy the full acceptance contract (consistent with log `final` verdict "not achieved"); the in-boundary achievements and the per-metric relaxation mapping are documented in log entry `final.escalation`.
