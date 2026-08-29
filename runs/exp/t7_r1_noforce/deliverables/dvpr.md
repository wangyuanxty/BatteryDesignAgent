# Design Verification Plan and Report — VBF-T7R1NOFORCE-DVPR-01

**Case**: `t7_r1_noforce` — HEV battery · **Date**: 2026-08-25 · **Virtual test version** — all results from simulation outputs; uncovered conditions marked N/A (requires physical experiment). No numbers from memory.

## Verification Items

| # | Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC discharge, 25 °C ambient | 5.0065 Ah | ✓ vs nominal 5.0 Ah (entry-0 informational) | `cell/r5_slim_1c_dfn.json` |
| 2 | 4C fast-charge temperature rise | 4C charge @45 °C, lumped thermal, h = 100 W/m²/K | T_max = 325.54 K (+7.39 K vs 318.15 K ambient) | ✓ below 573 K red line | `cell/r5_slim_4c45.json` |
| 3 | 4C fast-charge lithium plating | same run, anode surface potential vs Li/Li⁺ | min = +0.0153 V (≥ 0) → plated = false | ✓ (criterion `plated: false`) | `cell/r5_slim_4c45.json`; log-evaluate R5 mechanical derivation |
| 4 | Voltage window | parameter set limits | 2.5 – 4.2 V | informational | Chen2020 dump |
| 5 | Energy density | calc-energy (discharge energy ÷ layer mass, electrolyte excluded) | 491.47 Wh/kg | ✓ ≥ 327.18 Wh/kg | `cell/r5_slim_energy.json` |
| 6 | SEI growth @45 °C | 100 × 1C cycles, ec-reaction-limited SEI, 318.15 K | 510.51 nm at cycle 100 | ✓ ≤ 550 nm | `cell/r5_slim_aging45.json` |
| 7 | Nail penetration (10 W) thermal runaway | t_init = 325.54 K (4C T_max), T_amb = 298.15 K, q = 10 W, hA = 0.531 W/K, Kim/Coman ODE | triggered = false; T_final = 317.0 K; dT/dt max = −1.1×10⁻⁹ K/s | ✓ (criterion `triggered: false`) | `validation/r5_slim_nail.json` |
| 8 | DC internal resistance | calc-energy rate-pulse caliber | 2.6415 mΩ | informational | `cell/r5_slim_energy.json` |

**Item 3 protocol detail** (honesty): the 4C charge is an experiment [1C discharge to 2.5 V → 4C CC to 4.2 V → CV hold to 900 s charge step]. CC phase lasted 379.7 s (~2.11 Ah at 20 A) before hitting 4.2 V; the anode potential continued to fall during the CV hold, reaching its minimum +0.0153 V at protocol end — the plating criterion is judged at this worst point.

**Item 7 condition detail** (honesty): ambient = 298.15 K (thermal-runaway module default, pre-registered in entry 0 meta); the design's own cooling (hA = 0.531 W/K) is used. Equilibrium T_final = 298.15 + 10/0.531 = 316.98 K (matches output 317.0 K). Sensitivity remark: at a 318.15 K ambient the equilibrium would be ≈ 337 K — still far below the 573 K trigger; the verdict is robust to this condition choice, and the condition is stated rather than varied.

## N/A Items (beyond pure simulation boundary — requires physical experiment)

| Item | Note |
|---|---|
| Nail penetration (physical) | Virtual thermal-runaway ODE only; no structural/mechanical model |
| Overcharge to thermal runaway | Protocol exists in tool but not part of this case's contract; not simulated |
| Crush / drop | No mechanical abuse model |
| Cycle life (cycles to end-of-life) | Only SEI thickness is modeled (ec-reaction-limited); capacity-fade chain beyond SEI absent; per-cycle capacity trajectory artifact (climb 0.84→1.39 Ah) annotated in evaluate entries — `sei_thickness_nm_end` is the reliable indicator |
| Rate-pulse internal resistance (physical) | DCR is simulation-caliber (calc-energy) |

## Conclusion

**All four contract criteria PASS** (mechanical log-evaluate verdict R5: pass, checked 4): energy density 491.47 ≥ 327.18 Wh/kg; 4C @45 °C plated = false (anode min +0.0153 V); SEI 510.51 ≤ 550 nm; nail triggered = false. Uncovered items listed above are the paper's honest limitations: physical abuse tests, cycle life, and true DFT/MD material endorsement (endorse entry: skipped, real_compute = false) remain for physical/first-principles follow-up.
