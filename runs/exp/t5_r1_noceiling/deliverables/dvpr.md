# Design Verification Plan and Report (virtual-test version) — VBF-T5R1NOCEILING-DVPR-01

Cell: R4A MarginAnode1p0. One row per verification item; determinations are mechanical vs the log.jsonl entry-0 contract criteria; uncovered conditions honestly marked N/A.

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | run-pyamm 1C_discharge, DFN, 298.15 K ambient | 9.6251 Ah; terminates cleanly at 2.5000 V in 6930 s (no 7200-s truncation) | reported (no capacity threshold in contract) | cell/r4_A_1c_dfn.json; cell/r4_A_calc_dfn.json:capacity_ah |
| Energy density | calc-energy contract formula (energy Wh / mass kg; mass = sum layer thickness x (1-porosity) x density x area, electrolyte excluded) | 583.93 Wh/kg (SPMe cross-check 583.46) | PASS (>= 500.94) | cell/r4_A_calc_dfn.json:energy_density_wh_kg |
| 4C fast-charge temperature rise | run-pyamm 4C_charge_45C, DFN, lumped thermal, 318.15 K ambient | T_max 320.36 K (47.2 degC) | PASS (<= 333.15 K / 60 degC) | cell/r4_A_4c_dfn.json:T_max_K |
| 4C fast-charge plating | run-pyamm 4C_charge_45C + --plating, DFN | anode surface potential min +0.0212 V (charge ends at 4.2 V ceiling, 84.3% SOC) | PASS (no plating; min > 0 V) | cell/r4_A_4c_dfn.json:anode_potential_v |
| Voltage window | parameter set lower/upper cut-offs | 2.5 - 4.2 V | consistent with protocol termination conditions | parameter set |
| Nail penetration | - | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | - |
| Overcharge to thermal runaway | - | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | - |
| Crush / drop | - | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | - |
| Cycle life | - | N/A (no aging model; aging protocol not part of this contract) | N/A | - |
| Rate-pulse (HPPC) internal resistance | - | N/A (beyond pure simulation boundary); note calc-energy reports quasi-static DCR 0.00109 Ohm | N/A | cell/r4_A_calc_dfn.json:dcr_ohm |

## Conclusion

3/3 contract criteria PASS at DFN, with SPMe cross-check agreeing on all three (ED 583.46; anode min +0.0270 V; T_max 320.44 K). Safety margins: anode surface +21 mV above plating onset; temperature 12.8 K below the 60 degC limit; ED 16.6% above the 500.94 Wh/kg floor. Uncovered items (nail, overcharge-to-thermal-runaway, crush, drop, cycle life, HPPC) are outside the pure-simulation boundary and are cited as limitations.

