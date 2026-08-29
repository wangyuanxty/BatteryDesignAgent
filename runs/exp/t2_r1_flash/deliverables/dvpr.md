# Design Verification Plan and Report (virtual test) — VBF-T2R1FLASH-DVPR-01

**Case**: t2_r1_flash · Verdict: **ALL PASS** (6/6 criteria)

| # | Verification item | Condition | Result | Determination (vs criteria) | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC discharge 25C to 2.5 V, DFN | 5.0469 Ah / 18.178 Wh | PASS (ED >= 327.18: 425.4 Wh/kg) | cell/r2_fcc_1c_dfn.json, r2_fcc_energy.json |
| 2 | 4C fast-charge temperature rise | 4C CC charge 45C amb, lumped thermal | T_max 329.2 K (red line 333.15 K) | PASS | cell/r2_fcc_4c.json |
| 3 | 4C fast-charge plating | 4C charge + plating module | anode min 12.3 mV >= 0 V | PASS (no plating) | cell/r2_fcc_4c.json anode_potential_v |
| 4 | SEI growth @100 cyc 1C | 1C CC cycling 100 cyc, SPMe aging | 78.2 nm | PASS (<= 500 nm) | cell/r2_fcc_aging100.json |
| 5 | SEI growth @500 cyc 1C | 1C CC cycling 500 cyc, SPMe aging | 262.0 nm | PASS (<= 550 nm) | cell/r2_fcc_derived.json |
| 6 | Low-temperature discharge | 1C discharge -20C | 99.4 % of 25C capacity | PASS (>= 90 %) | cell/r2_fcc_derived.json |
| 7 | Voltage window | parameter set | 2.5 – 4.2 V | PASS (contract window) | parameter set |

**Items marked N/A (beyond pure simulation boundary, requires physical experiment)**: nail penetration, overcharge-to-thermal-runaway, crush, drop, rate-pulse internal resistance, cycle life to 80% SOH (capacity-based), cell-can/tab mechanicals, formation optimization, manufacturing tolerances.

**Known artifact (honest note)**: under the standard SEI model the aging capacity trajectory shows a climb-then-saturate non-monotonic shape (lithium-loss shifts the voltage window); it is NOT treated as normal degradation — the reliable aging indicator is sei_thickness_nm_end (used for verdicts 4/5).
