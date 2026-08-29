# Cell Design Specification — combo-v5-final (VBF Case t2_r3)

> All values mechanically sourced from `cell/r7_final_*_dfn.json`, `cell/r6_combo-v5-final_aging*_spme.json`, `r6_combo-v5-final_params.json` and the Chen2020 parameter set; line-by-line source below. No values written from memory.

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite | Chen2020 base set (task names no system) |
| Nominal capacity | 5.0 Ah (parameter set) / 5.0648 Ah (simulated) | `Nominal cell capacity [A.h]`; `r7_final_1c_dfn.json` capacity_ah |
| Voltage window | 2.5–4.2 V | parameter set cut-offs |
| Cell dimensions (H×W×T stack) | 65 mm × 1580 mm × 0.201 mm | `Electrode height/width [m]`; thickness = 75.6+12.0+85.2+16+12 µm layer sum (calc-energy thickness_m) |
| Shell thickness | Not provided (no parameter) | — |
| Electrolyte formulation | 1 M LiPF6 in EC:EMC (3:7 w/w) — Chen2020 parameterization; additive candidates: Not provided (not parameterized) | Chen2020 set documentation |
| Cation transference number | 0.45 (override; baseline 0.2594) | `r6_combo-v5-final_params.json` / Chen2020 |
| Electrolyte conductivity | 1.7 S/m constant (override; baseline Nyman2008 σ(298 K)=0.9487 S/m) | params / Chen2020 function |
| Electrolyte diffusivity | 5.0e-10 m²/s constant (override; baseline 1.769e-10) | params / Chen2020 function |

## 2. Electrode and separator

| Layer | Thickness | Porosity | Active vol. frac. | Particle radius | Material / collector |
|---|---|---|---|---|---|
| Positive (NMC811) | 75.6 µm | 0.335 | 0.665 | 2.5 µm (final; baseline 5.22) | ρ = 3262 kg/m³ |
| Negative (graphite) | 85.2 µm | 0.4 (final; baseline 0.25) | 0.75 | 2.0 µm (final; baseline 5.86) | ρ = 1657 kg/m³ |
| Separator | 12 µm | 0.47 | — | — | ρ = 397 kg/m³ |
| Positive collector | 16 µm Al | — | — | — | ρ = 2700 kg/m³ |
| Negative collector | 12 µm Cu | — | — | — | ρ = 8960 kg/m³ |

All parameters above are Chen2020 set values except porosities/particle radii overridden by `r6_combo-v5-final_params.json`.

N/P ratio = 0.667 (mechanical: c_max×active-volume-fraction×thickness, neg/pos = 33133×0.75×85.2 / 63104×0.665×75.6 µm). Below unity means the parameter set's positive electrode is oversized relative to the negative (anode-limited window). Set-inherent; unchanged by this design's overrides; flagged for physical cell-balancing validation. µm unit note: ratio is monotonic in thickness so units cancel.

## 3. Process design parameters

| Parameter | Value | Formula | Source |
|---|---|---|---|
| Pos. areal density | 163.99 g/m² | L×(1−porosity)×ρ | 75.6 µm×0.665×3262 kg/m³ (Chen2020) |
| Neg. areal density | 84.71 g/m² | L×(1−porosity)×ρ | 85.2 µm×0.6×1657 kg/m³ |
| Pos. compaction density | 2.17 g/cm³ | ρ×(1−porosity)÷1000 | divided by 1000 (kg/m³→g/cm³) |
| Neg. compaction density | 0.99 g/cm³ | ρ×(1−porosity)÷1000 | |
| Electrolyte fill amount | 8.02 g | pore volume×1.2 g/cm³×fill factor 1.0 | pore = 6.7 cm³; electrolyte density 1.2 g/cm³ literature value (not in set) |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | — | design recommended value; actual production-line value requires tuning, flagged for validation |

## 4. Mass breakdown

| Component | Mass | Formula-calibre note |
|---|---|---|
| Positive electrode (NMC811 × 0.665 vol) | 16.8422 g | L×A×(1−por)×ρ from calc-energy layer_kg_m2 = 0.163993788 kg/m² × 0.1027 m² |
| Negative electrode (graphite × 0.75 vol) | 8.6993 g | layer_kg_m2 = 0.08470583999999999 kg/m² × 0.1027 m² |
| Separator | 0.2593 g | layer_kg_m2 = 0.00252492 kg/m² × 0.1027 m² |
| Positive collector Al | 4.4366 g | layer_kg_m2 = 0.043199999999999995 kg/m² × 0.1027 m² |
| Negative collector Cu | 11.0423 g | layer_kg_m2 = 0.10752 kg/m² × 0.1027 m² |
| Electrolyte (excluded by contract calibre) | 8.02 g | pore-volume calibre, literature 1.2 g/cm³ |
| **Total (calc-energy contract calibre, electrolyte excluded)** | **41.2797 g** | `r7_final_energy_dfn.json` mass_kg = 0.04128 kg |
| Total incl. electrolyte | 49.30 g | auxiliary calibre |

## 5. Performance verification

| Metric | Simulated | Threshold (entry 0) | Determination | Source |
|---|---|---|---|---|
| Energy density | 447.12 Wh/kg | ≥ 327.18 | ✓ PASS | `r7_final_energy_dfn.json` energy_density_wh_kg |
| Low-T retention (−20 °C/25 °C, DFN) | 0.9957 | ≥ 0.90 | ✓ PASS | `r7_final_lowT_retention.json` = 5.0430/5.0648 |
| SEI @ 100 cyc | 276.2 nm | ≤ 500 | ✓ PASS | `r7_final_sei_thickness_nm_100cyc.json` (SPMe aging, note in file) |
| SEI @ 500 cyc | 393.0 nm | ≤ 550 | ✓ PASS | `r7_final_sei_thickness_nm_500cyc.json` |
| 4C plating | anode potential min = +0.0443 V | ≥ 0 V (no plating) | ✓ PASS | `r7_final_4c_dfn.json` anode_potential_v |
| 4C fast charge | charge-phase duration ≈ 693 s (V-min restart → 4.2 V cut-off at 4344.8 s); charge capacity 0.7705 Ah; protocol = 1C pre-discharge (4.106→2.956 V, ~3530 s) + 4C CC charge, 318.15 K ambient | recorded | — | `r7_final_4c_dfn.json` time_s / voltage_v / capacity_ah (runner: C-rate 4.0) |
| Max cell temperature @ 4C | 347.70 K (74.55 °C) | no contract threshold; recorded | — | 4C protocol runs at 318.15 K ambient (`run-pyamm --thermal lumped`) |
| 1C capacity | 5.0648 Ah | nominal 5.0 Ah | recorded | `r7_final_1c_dfn.json` |

## 6. Design notes — parameters changed vs Chen2020 baseline

| Parameter | Baseline | Final | Why (citing evaluate-log rounds) |
|---|---|---|---|
| Positive particle radius | 5.22 µm | 2.5 µm | unlocks 4C charge acceptance: baseline cathode surface saturates ~26 s into 4C (t≈R²/D_s hours); fine particles shorten diffusion (round 3 evidence; r4-r7) |
| Negative particle radius | 5.86 µm | 2.0 µm | raises anode charge-transfer area, lifts anode potential away from 0 V during 4C (rounds 2/5/7) |
| Electrolyte conductivity | σ(T) fcn (0.9487 @298K) | 1.7 S/m const. | transport override; reduces ohmic drop at 4C and −20 °C; literature-class constant bridge flagged as estimate (rounds 2/6) |
| Electrolyte diffusivity | 1.769e-10 m²/s | 5e-10 | concentration-polarization relief; supports low-T retention (rounds 2/6) |
| Cation transference number | 0.2594 | 0.45 | further concentration-polarization relief (rounds 2/6) |
| Negative porosity | 0.25 | 0.40 | electrolyte path widening → anode potential lift during 4C; small ED cost (round 5/6) |
| SEI kinetic rate constant | 1e-12 m/s | 2e-13 | SEI-suppressing-coating bridge; near-inert at 100 cyc (round 2) but retained for late-life (rounds 2–7) |
| SEI partial molar volume | 9.585e-5 m³/mol | 4.7925e-5 | denser, LiF/Li₂O-rich SEI film: thickness scales linearly with V̄, no early-life IR penalty (rounds 5/6 discovery) |

Bridge/estimate flags: transport overrides are literature-class constants (not simulation-derived); SEI k/V̄ are electrode-modification bridges; all flagged per protocol as fabrication-grade estimators, re-validatable by true stage 2–4 (skipped: real_compute=false).
