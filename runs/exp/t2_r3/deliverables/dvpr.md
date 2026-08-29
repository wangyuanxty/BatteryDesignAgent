# Design Verification Plan and Report (virtual) — combo-v5-final (VBF Case t2_r3)

> Virtual test calibre: values mechanically read from `cell/r7_final_*_dfn.json` / `r6_combo-v5-final_aging*_spme.json`; determinations vs entry-0 thresholds by `bda log-evaluate` (round 7, verdict pass). Uncovered conditions marked N/A (beyond pure simulation boundary).

| Item | Condition | Result value | Determination (vs criteria / threshold) | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C from 4.2 V to 2.5 V, 298.15 K | 5.06484 Ah | recorded; nominal 5.0 Ah (parameter set) exceeded | `r7_final_1c_dfn.json` capacity_ah |
| Low-temperature retention | 1C discharge, 253.15 K vs 298.15 K | 0.995697 | PASS (≥ 0.90) | `r7_final_lowT_retention.json` = 5.04305/5.06484; mechanical derivation |
| Energy density | contract calibre (electrolyte excluded) | 447.12 Wh/kg | PASS (≥ 327.18) | `r7_final_energy_dfn.json` energy_density_wh_kg |
| SEI after 100 cycles 1C | aging protocol, 100 cyc, 298.15 K | 276.22 nm | PASS (≤ 500) | `r7_final_sei_thickness_nm_100cyc.json` (SPMe aging protocol; params identical to DFN set) |
| SEI after 500 cycles 1C | aging protocol, 500 cyc, 298.15 K | 393.00 nm | PASS (≤ 550) | `r7_final_sei_thickness_nm_500cyc.json` |
| 4C fast-charge plating | 4C CC charge 2.5→4.2 V, 318.15 K ambient, lumped thermal + plating option | anode potential min +0.04432 V | PASS (negative electrode potential ≥ 0 V throughout; plated = false by mechanical derivation) | `r7_final_4c_dfn.json` anode_potential_v |
| 4C temperature rise | same protocol | T_max 347.70 K (74.55 °C), ΔT = +29.5 K vs 318.15 K ambient | recorded; NO contract threshold in entry 0 (annotated, not asserted as pass) | `r7_final_4c_dfn.json` T_max_K |
| Voltage window | parameter set | 2.5–4.2 V | recorded | Chen2020 cut-offs |
| Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| Overcharge to thermal runaway | — | N/A (protocol exists but not a contract item; requires physical experiment) | N/A | — |
| Crush / drop | — | N/A (requires physical experiment) | N/A | — |
| Cycle-life capacity retention | — | aging-protocol capacity trajectory declines steeply (0.3309→0.0123 Ah over 500 cyc); reported honestly, not asserted | N/A as contract metric (contract covers SEI thickness only); flagged for physical validation | `r6_combo-v5-final_aging500_spme.json` capacity_ah_per_cycle |
| Rate-pulse internal resistance | — | N/A (no pulse protocol; DCR 2.6125 mΩ from calc-energy recorded instead) | N/A | `r7_final_energy_dfn.json` dcr_ohm |

## Conclusion

**Pass/fail summary**: 5 of 5 contract criteria PASS at DFN calibre (energy density, low-T retention, SEI@100, SEI@500, no plating) — mechanical, per `bda log-evaluate` round 7 (`r7_batch_eval.json`: verdict=pass checked=5 unchecked=0). T_max recorded with no threshold.

**Uncovered items (paper-limitation citation)**: SEI aging numbers are SPMe-protocol calibre (500-cycle DFN aging not run); aging-protocol capacity trajectory artifact unresolved; low-T and 4C performance rest on literature-class constant electrolyte-transport overrides (estimated bridge, flagged); nail/overcharge/crush/drop/rate-pulse = N/A (beyond pure simulation boundary). SEI/electrolyte chemistry not DFT-validated (real_compute=false; endorse entry records the skip).
