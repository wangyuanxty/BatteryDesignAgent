# Design Verification Plan and Report (Virtual Test) — Case t7_r1

Document: VBF-T7R1-DVPR-01 · Prepared 2026-08-25 · Signature: Prepared ______ / Reviewed ______ / Approved ______

| # | Item | Condition | Result | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C (6.0313 A nominal) discharge, 298.15 K, DFN | 6.032209 Ah | PASS (matches nominal 6.0313 Ah within 0.02 %) | cell/r5_v11_1c_dfn.json:capacity_ah |
| 2 | Energy density | contract formula: ∫V·I dt ÷ Σ layer thickness×(1−ε)×ρ×area (electrolyte excluded) | 483.247 Wh/kg | PASS vs threshold ≥ 327.18 Wh/kg | cell/r5_v11_energy.json:energy_density_wh_kg |
| 3 | 4C fast-charge plating | 4C charge at 45 °C ambient, lumped thermal + plating model, DFN | anode surface potential min +0.047604 V → plated = false | PASS (no potential < 0 V) | cell/r5_v11_4c45.json:anode_potential_v |
| 4 | 4C fast-charge temperature | same run | T_max = 330.130 K (56.98 °C) | informational — no T_max threshold in task (entry 0 "not_adjudicated") | cell/r5_v11_4c45.json:T_max_K |
| 5 | SEI thickness after 100 cycles @ 45 °C | aging_1C_100cyc_45C protocol, isothermal + SEI (ec reaction limited) | 465.473 nm | PASS vs threshold ≤ 550 nm | cell/r5_v11_aging45.json:sei_thickness_nm_end |
| 6 | Nail penetration → thermal runaway (virtual) | run-tr ODE, q_nail = 10 W, hA = 0.2655 W/K (= h 50 × 0.00531 m²), mass 45.105 g | triggered = false; T_max 336.320 K; dT/dt max 0.244883 K/s | PASS (no TR) | cell/r5_v11_nail.json |
| 6a | Nail cooling-margin sensitivity | h=40 (hA 0.2124): not triggered, T_max 348.69 K; h=30 (hA 0.1593): TRIGGERED at 666.0 s; h=25 (hA 0.1328): TRIGGERED at 518.4 s | design cooling floor ≈ 40 W/(m²·K) | margin evidence for h = 50 design point | cell/r4_v8_nail.json; cell/r5_v8_nail_h30.json; cell/r5_v8_nail_h25.json |
| 7 | Voltage window | parameter set upper/lower cut-off | 2.5 – 4.2 V | PASS (as configured) | Chen2020 parameter set |
| 8 | Baseline reference (R1) | Chen2020 unmodified, same protocols | ED 400.75 Wh/kg PASS; SEI 476.1 nm PASS; 4C plated = true (min −0.1918 V) FAIL; nail triggered at 322.2 s FAIL | baseline failures localized to plating + nail — both fixed by design | log.jsonl evaluate R1 evidence |

## N/A Items (beyond pure-simulation boundary — require physical experiment)

| Item | Status |
|---|---|
| Physical nail penetration / crush / drop | N/A (virtual TR ODE only; mechanical abuse requires hardware test) |
| Overcharge → thermal runaway | N/A (overcharge protocol not run — overcharge not part of task criteria) |
| Cycle life to failure (capacity-based EOL) | N/A beyond 100 simulated cycles |
| Rate-pulse internal resistance (HPPC) | N/A (DCR reported from discharge calc instead: 2.882 mΩ) |

## Conclusion

**PASS — 4/4 adjudicable criteria met at DFN precision** (energy density, plating-free 4C, SEI ≤ 550 nm, no nail TR). Note on aging trajectory: per-cycle capacities in the aging protocol are distorted by the thick-SEI-film model artifact at µm-scale films (baseline and all variants affected); the adjudicable metric per entry 0 is sei_thickness_nm_end (465.47 nm ≤ 550 nm), and the trajectory is labeled honestly in evaluate R3–R5 notes rather than interpreted as capacity behavior.
