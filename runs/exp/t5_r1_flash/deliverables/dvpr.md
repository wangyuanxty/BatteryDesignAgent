# Design Verification Plan & Report (virtual test) — t5_r1_flash

**Doc No. VBF-T5R1FLASH-DVPR-01** · Rev A (2026-08-25) · Virtual-test version; all results from simulation (run-pyamm / calc-energy), conclusion-grade values DFN.

| # | Verification item | Condition | Result | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC discharge 4.7→2.5 V, 25 °C | 8.26 Ah | informational (no contract threshold) | cell/r9_lnmo_r6_1c_dfn.json:capacity_ah |
| 2 | Energy density | 1C discharge energy ÷ contract mass | 597.9 Wh/kg | ✓ PASS vs ≥500.94 | cell/r9_lnmo_r6_energy_dfn.json:energy_density_wh_kg |
| 3 | 4C fast-charge temperature | 4C charge, 45 °C ambient, lumped thermal, DFN | T_max 327.55 K (54.4 °C) | ✓ PASS vs ≤333.15 K | cell/r9_lnmo_r6_4c45_dfn.json:T_max_K |
| 4 | 4C fast-charge plating | same, anode potential series | min +14.7 mV (>0) | ✓ PASS (plated=false) | cell/r9_lnmo_r6_4c45_dfn.json:anode_potential_v |
| 5 | Voltage window | parameter set limits | 2.5–4.7 V | — | LNMO.json |
| 6 | 4C charge acceptance | protocol cap | 2.0 Ah accepted | informational | cell/r9_lnmo_r6_4c45_dfn.json:capacity_ah |
| 7 | DC resistance (formula) | calc-energy V²/4P formula | 8.0 mΩ | informational | cell/r9_lnmo_r6_energy_dfn.json:dcr_ohm |
| 8 | Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | — | — |
| 9 | Overcharge to thermal runaway | — | N/A (same) | — | — |
| 10 | Crush / drop / mechanical | — | N/A (same) | — | — |
| 11 | Cycle life | — | N/A (aging model not in scope of this case; no SEI aging protocol run) | — | — |
| 12 | Rate-pulse internal resistance | — | N/A (same) | — | — |

**Conclusion:** contract requirements **ACHIEVED** — energy density 597.9 ≥ 500.94 Wh/kg ✓, 4C no-plating ✓ (anode min +14.7 mV), T_max 327.6 °C ≤ 60 °C ✓.
**Not covered (paper limitations):** mechanical abuse, overcharge, cycle life, low temperature, rate pulse — require physical experiments; electrolyte transport values are estimates pending true MD endorsement (real_compute=false).
