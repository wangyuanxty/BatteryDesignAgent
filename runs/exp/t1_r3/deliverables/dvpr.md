# Design Verification Plan & Report (virtual-test version) — V11 (t1_r3)

**Document number**: VBF-EXPT1R3-DVPR-01
**Date**: 2026-08-26
**Note**: virtual verification only; values mechanically taken from simulation outputs. Items beyond the pure-simulation boundary are honestly marked N/A.

| # | Verification item | Condition | Result value | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC to 2.5 V, 25 °C (SPMe) | 5.0849 Ah | informational (no capacity threshold registered in entry 0) | `r5_v11_1c_spme.json:capacity_ah` |
| 2 | Energy density | 1C discharge energy ÷ contract mass | 605.33 Wh/kg | ✓ PASS (≥ 392.61) | `r5_v11_energy.json:energy_density_wh_kg` |
| 3 | 4C fast-charge temperature rise | 4C CC charge, 45 °C ambient, lumped thermal | T_max 321.2 K (48.0 °C) | ✓ PASS (≤ 333.15 K) | `r5_v11_4c.json:T_max_K` |
| 4 | 4C fast-charge plating | same run, anode surface potential | min +0.0425 V → plated = false | ✓ PASS (no plating) | `r5_v11_4c.json:anode_potential_v` |
| 5 | 4C charge acceptance | 4C (20.34 A) to 4.2 V event | 4.677 Ah = 92.0% of 1C capacity in 13.8 min | ✓ task "support 4C fast charge" demonstrated | `r5_v11_4c.json:capacity_ah` × nominal 5.085 |
| 6 | Voltage window | parameter set | 2.5 – 4.2 V | ✓ PASS | Chen2020 cut-offs |
| 7 | Overcharge abuse to 4.7 V | 0.5C CC to 4.7 V (DFN) → coupled thermal-runaway ODE (mass 0.03076 kg) | v_end 4.700 V; T_max 298.57 K; triggered = false | ✓ PASS (no thermal runaway) | `r5_v11_oc.json`, `r5_v11_tr.json` |
| 8 | Nail penetration | — | — | N/A (beyond pure simulation boundary, requires physical experiment) | — |
| 9 | Crush / drop | — | — | N/A (requires physical experiment) | — |
| 10 | Cycle life | — | — | N/A (no aging model run in this case) | — |
| 11 | Rate-pulse internal resistance (HPPC) | — | — | N/A (protocol not run) | — |

## Conclusion

All six registered verification items pass; item 1 is informational (no threshold registered). Uncovered items (8–11) are outside the pure-simulation boundary and are listed as paper limitations.
