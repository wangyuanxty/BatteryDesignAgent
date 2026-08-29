# VBF Design Verification Plan & Report (virtual-test version) — dvpr

**Document number**: VBF-T7R3-DVPR-01 · **Case**: t7_r3 · **Date**: 2026-08-26
All result values are mechanically taken from bda simulation outputs. Prepared / Reviewed / Approved: ________

| # | Verification item | Condition | Result value | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 6.28 A CC to 2.5 V, 25 °C (SPMe) | 6.2569 Ah | ✓ vs nominal 6.28 Ah | `cell/r7_v19_final_1c.json:capacity_ah` |
| 2 | 1C discharge capacity (DFN cross-check) | 6.28 A CC to 2.5 V (DFN) | 6.28 Ah | ✓ consistent | `cell/r6_v19_1c_dfn.json:capacity_ah` |
| 3 | Energy density | contract formula ∫V·I₁C dt ÷ mass | 482.43 Wh/kg ≥ 327.18 | ✓ PASS | `cell/r7_v19_final_energy.json:energy_density_wh_kg` |
| 4 | 4C fast-charge temperature rise | 25.12 A charge from 2.5 V to 4.2 V, 45 °C, lumped thermal | T_max 363.2 K (90.1 °C) | ✓ no criterion on T; recorded | `cell/r7_v19_final_4c45c.json:T_max_K` |
| 5 | 4C fast-charge lithium plating | same run, `--plating`, DFN | anode surface potential min **+0.0171 V**; plated = false | ✓ PASS | `cell/r7_v19_final_4c45c.json:anode_potential_v` |
| 6 | SEI growth durability | aging 1C ×100 cyc @ 45 °C (SEI ec-reaction-limited, isothermal) | SEI end 512.92 nm ≤ 550 nm | ✓ PASS | `cell/r7_v19_final_aging45c.json:sei_thickness_nm_end` |
| 7 | Nail penetration thermal runaway (virtual ODE) | q_nail = 10 W, mcp = 41.94 J/K (46.62 g × 900), hA = 0.5 W/K, T₀ = 298.15 K | triggered = **false**, T_max = 318.2 K, dT/dt_max = 0.236 K/s | ✓ PASS | `cell/r7_v19_final_nail_hA05.json` |
| 8 | Nail sweep — cooling margin | hA = 0.05 / 0.2 / 0.3 / 0.4 / 0.5 W/K | triggers at 346 s / triggers at 2097 s (405 K) / pass 331.7 K / pass 323.2 K / pass 318.2 K | min required hA ≈ 0.3 W/K → design 0.5 W/K | `cell/r7_v19_final_nail_hA*.json` |
| 9 | Voltage window | parameter set cut-offs | 2.5 – 4.2 V | ✓ | Chen2020 set |

**Not covered (N/A — beyond pure simulation boundary, requires physical experiment)**: overcharge-to-thermal-runaway physical test, crush, drop, vibration, calendar life, EOL capacity retention, low-temperature (< 0 °C) performance, rate-pulse internal resistance, production tolerances. (Virtual overcharge protocol exists but was not in the task criteria.)

**Conclusion**: All six task criteria verified PASS in the virtual battery (ED 482.4 ≥ 327.18 Wh/kg; SEI 512.9 ≤ 550 nm; plated = false at 4C/25.12 A; triggered = false at 10 W nail with designed cooling). Uncovered items above are listed for release-book honesty; they require physical prototypes.