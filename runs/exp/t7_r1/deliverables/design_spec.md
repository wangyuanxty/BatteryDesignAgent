# Cell Design Specification — HEV Fast-Charge Battery (Case t7_r1)

Document: VBF-T7R1-DS-01 · Prepared 2026-08-25 · Signature: Prepared ______ / Reviewed ______ / Approved ______

## 1. Basic Specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (pouch, Chen2020 baseline parameterization) | entry 0 meta.base; anchor table |
| Nominal capacity | 6.0313 Ah | params_v11.json (mechanically = measured 1C capacity, rule per propose_r2b) |
| Measured 1C capacity (DFN) | 6.032209 Ah | cell/r5_v11_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V | Chen2020 parameter set (Lower/Upper voltage cut-off) |
| Nominal (midpoint) voltage | 3.7237 V | cell/r5_v11_energy.json:midpoint_voltage_v |
| Cell dimensions (electrode stack) | height 65 mm × width 1580 mm × thickness 230.6 µm | parameter set (Electrode height/width); thickness = calc-energy sum |
| Shell / enclosure thickness | Not provided | no parameter in set |
| Electrolyte formulation | EC/EMC + LiPF6 base; transport overrides σ = 2.5 S/m, t⁺ = 0.55, D_e = 6×10⁻¹⁰ m²/s | params_v11.json (design); base = Chen2020 |
| Electrolyte additive candidates | None (Stage 2 not entered; start_stage = 3, no new materials in task) | entry 0 meta |
| Cation transference number | 0.55 | params_v11.json |
| Cooling design | h = 50 W/(m²·K) on cell cooling surface 0.00531 m² → hA = 0.2655 W/K | params_v11.json; bridge (area = "Cell cooling surface area [m2]", Chen2020/injected default) |

## 2. Electrode and Separator

| Layer | Thickness | Porosity | Particle radius | AM volume fraction | Density (set) | Current collector |
|---|---|---|---|---|---|---|
| Positive (NMC811) | 75.6 µm | 0.335 | 3.5 µm (design) | 0.665 | 3262 kg/m³ | Al 16 µm (2700 kg/m³) |
| Separator | 12 µm | 0.47 | — | — | 397 kg/m³ | — |
| Negative (graphite) | 115 µm (design) | 0.36 (design) | 1.5 µm (design) | 0.75 | 1657 kg/m³ | Cu 12 µm (8960 kg/m³) |

- All values dumped from the Chen2020 parameter set with params_v11 overrides applied (mechanical dump, 2026-08-25).
- N/P ratio = negative theoretical areal capacity ÷ cell measured areal capacity (positive usable capacity):
  - Negative theoretical areal capacity = 115 µm × (1−0.36) × 33133 mol/m³ × F/3600 = 65.36 Ah/m²
  - Cell measured areal capacity = 6.032209 Ah ÷ 0.1027 m² = 58.74 Ah/m²
  - **Practical N/P = 1.113** (full-range theoretical N/P = 65.36/85.03 = 0.769, positive full-range 85.03 Ah/m² — NMC811 utilises ≈69 % of its theoretical range in the 2.5–4.2 V window; both values reproduced in calc.xlsx)
- Maximum concentrations: positive 63104 mol/m³, negative 33133 mol/m³ (parameter set).

## 3. Process Design Parameters

| Parameter | Formula | Value | Notes |
|---|---|---|---|
| Positive areal density | l × (1−ε) × ρ | 75.6e-6 × 0.665 × 3262 = 164.0 g/m² | parameter set |
| Negative areal density | l × (1−ε) × ρ | 115e-6 × 0.64 × 1657 = 122.0 g/m² | parameter set |
| Positive compaction density | ρ × (1−ε) / 1000 | 3262 × 0.665 / 1000 = 2.17 g/cm³ | set values |
| Negative compaction density | ρ × (1−ε) / 1000 | 1657 × 0.64 / 1000 = 1.06 g/cm³ | set values |
| Electrolyte fill amount | pore volume × ρ_elec × fill factor | 7.432 cm³ × 1.2 g/cm³ × 1.0 = 8.92 g | ρ_elec = 1.2 g/cm³ literature value; fill factor 1.0 assumption |
| Formation recommendation | 0.1C CC charge to 4.2 V, 25 °C, 2 cycles | — | design recommended value; production-line value requires tuning |

## 4. Mass Breakdown (formula caliber = calc-energy contract, electrolyte excluded)

| Layer | Mass (g) | Formula / source |
|---|---|---|
| Positive electrode coating | 16.842 | layer_kg_m2 0.163994 × 0.1027 m² (cell/r5_v11_energy.json) |
| Negative electrode coating | 12.525 | layer_kg_m2 0.121955 × 0.1027 m² |
| Positive current collector (Al) | 4.437 | 0.0432 × 0.1027 |
| Negative current collector (Cu) | 11.042 | 0.10752 × 0.1027 |
| Separator | 0.259 | 0.00252492 × 0.1027 |
| **Total (contract, electrolyte excluded)** | **45.105** | cell/r5_v11_energy.json:mass_kg |
| Electrolyte (additive, estimate) | 8.92 | pore-volume formula above, not in contract mass |

## 5. Performance Verification (vs entry 0 criteria)

| Metric | Threshold | Value | Verdict | Source |
|---|---|---|---|---|
| Energy density | ≥ 327.18 Wh/kg | 483.247 Wh/kg | ✓ PASS | cell/r5_v11_energy.json:energy_density_wh_kg |
| 4C fast charge plating | plated = false | anode surface min +0.0476 V → not plated | ✓ PASS | cell/r5_v11_4c45.json:anode_potential_v |
| 4C max temperature | not adjudicated (absent from task) | 330.130 K (56.98 °C) at 45 °C ambient | informational | cell/r5_v11_4c45.json:T_max_K |
| SEI after 100 cyc @45 °C | ≤ 550 nm | 465.473 nm | ✓ PASS | cell/r5_v11_aging45.json:sei_thickness_nm_end |
| Nail penetration (10 W) TR | triggered = false | triggered = false, T_max 336.320 K, dT/dt max 0.245 K/s | ✓ PASS | cell/r5_v11_nail.json |
| 1C capacity | — (not adjudicated) | 6.032209 Ah | informational | cell/r5_v11_1c_dfn.json:capacity_ah |

## 6. Design Notes (what changed vs baseline and why)

| Round | Change | Rationale (evaluate log) |
|---|---|---|
| R1 | Baseline Chen2020 | ED 400.75 ✓, SEI 476.1 ✓, but 4C plating (anode min −0.1918 V) and nail TR (triggered 322 s) FAIL |
| R2 | Transport set V1–V3 (σ/t⁺/D_e, h) | plating persists (−0.134 V best); V4 ceiling probe ED 464 Wh/kg → ED non-binding, no Stage-2 escalation |
| R3 | Isolations: porosity dominant (−0.134 → −0.0419 V); h=200 worsens plating | V5 combination (+0.0351 V, porosity 0.32, 1.5 µm graphite, D_e 5e-10, h 50) first full pass |
| R4 | Margin widening: V8 σ2.5/t⁺0.55/D_e6e-10/poro0.36 (+0.0494 V) | nail cooling floor mapped: h=40 passes (T_max 348.7 K), h=30 triggers at 666 s (r5_v8_nail_h30) |
| R5 | V11-final = V8 + h=50 (nominal mechanically 6.0313) | DFN-precision verification: all four criteria pass (this sheet, §5) |
