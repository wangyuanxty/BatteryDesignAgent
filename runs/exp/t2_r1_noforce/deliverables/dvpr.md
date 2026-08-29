# Design Verification Plan and Report (Virtual Test Version) — F1

**VBF-T2R1NOFORCE-DVPR-001** | Case: t2_r1_noforce | Date: 2026-08-25 | All results from simulation outputs; uncovered conditions honestly marked N/A.

| # | Verification item | Condition | Result | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC discharge, 25 °C | 5.0282 Ah (nominal 5.0 Ah) | PASS (≥ nominal; no explicit capacity criterion in task) | `cell/r5_f1_1c_spme.json:capacity_ah` |
| 2 | Energy density | contract caliber (ED = ∫V·I dt / Σ layer mass, electrolyte excluded) | 435.44 Wh/kg | **PASS (≥ 327.18 Wh/kg)** | `cell/r5_f1_energy.json:energy_density_wh_kg` |
| 3 | 4C fast-charge plating | 4C charge from 45 °C, anode potential criterion | min anode potential +0.0071 V | **PASS (no plating, φ ≥ 0 V)** | `cell/r5_f1_4c_dfn.json:anode_potential_v` (min, tool-derived) |
| 4 | 4C fast-charge temperature rise | 4C charge, lumped thermal, h=10 | T_max 359.92 K (+41.8 K from 45 °C) | reported (no temperature threshold in task criteria) | `cell/r5_f1_4c_dfn.json:T_max_K` |
| 5 | −20 °C discharge retention | 1C discharge, 253.15 K ambient + initial temp (cold-start fix) | 99.45 % (5.0003 / 5.0282 Ah) | **PASS (≥ 90 %)** | `derived/r5_f1_retention.json` ← `cell/r5_f1_lowT_spme.json` |
| 6 | SEI thickness @100 cyc | 1C cycling, 100 cyc, 25 °C isothermal | 439.52 nm | **PASS (≤ 500 nm)** | `cell/r5_f1_aging100_spme.json:sei_thickness_nm_end` |
| 7 | SEI thickness @500 cyc | 1C cycling, 500 cyc, 25 °C isothermal | 738.43 nm | **FAIL (> 550 nm)** — documented unreachable (three-strike, final entry) | `cell/r5_f1_aging500_spme.json:sei_thickness_nm_end` |
| 8 | Voltage window | parameter set limits | 2.5 – 4.2 V | PASS (usage within limits) | parameter set cut-offs |

**Items explicitly N/A (beyond pure-simulation boundary, require physical experiment)**: nail penetration, overcharge-to-thermal-runaway, crush, drop, rate-pulse internal resistance (DCR is model-computed only), cycle-life capacity retention (aging simulated for SEI growth only; capacity trajectory shows the climb-then-saturate artifact and is not reported as degradation), electrode manufacturability tolerances.

**Conclusion**: 4 of 5 task criteria PASS (ED, SEI@100, −20 °C retention, 4C no-plating). 1 criterion FAIL (SEI@500 ≤ 550 nm) — not a design failure but a model-family limitation: the ec-reaction-limited SEI growth law cannot saturate; measured minimum growth ratio 100→500 cyc is ×1.68 and the k_SEI lever saturates (R5 F2). Uncovered items listed above are cited as paper limitations.
