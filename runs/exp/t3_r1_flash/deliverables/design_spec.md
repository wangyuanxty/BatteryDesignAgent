# Cell Design Specification — VBF Power-Tool Cell (V4 Margin-fix)

Case: t3_r1_flash | Generation date: 2026-08-25 | Doc: VBF-T3R1FLASH-DS-01

## 1. Basic Specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC-type positive / graphite negative (Chen2020 parameterization) | base_params=Chen2020 (entry 0 meta) |
| Nominal capacity | 3.44 Ah | 1C DFN sim: cell/r2_v4_1c_dfn.json:capacity_ah=3.4376 |
| Voltage window | 2.5 – 4.2 V | parameter set (Lower/Upper voltage cut-off) |
| Cell dimensions | height 65 mm × width 1580 mm (wound strip) × stack 0.14 mm | parameter set (Electrode height/width), calc-energy thickness_m=1.4e-4 |
| Shell / casing thickness | Not provided (no casing parameter in set) | — |
| Electrolyte formulation | high-transport LiPF6-class formulation: σ_e=2.4 S/m, D_e=3.5e-10 m²/s, t⁺=0.5 (design overrides, estimate) | params_r2_v4.json (estimate, literature-adjacent) |
| Electrode area | 0.1027 m² | calc-energy area_m2 |

## 2. Electrode and Separator

| Layer | Thickness (µm) | Porosity | Particle radius (µm) | Material / note |
|---|---|---|---|---|
| Positive electrode | 42 | 0.40 | 0.8 | NMC-type; design value (baseline 75.6 µm / 0.335 / 5.22 µm) |
| Negative electrode | 58 | 0.38 | 1.0 | graphite; design value (baseline 85.2 µm / 0.25 / 5.86 µm) |
| Separator | 12 | 0.47 | — | parameter set |
| Positive current collector | 16 | — | — | Al (2700 kg/m³), parameter set |
| Negative current collector | 12 | — | — | Cu (8960 kg/m³), parameter set |

N/P ratio = negative capacity density × thickness ÷ positive capacity density × thickness
= (0.62×33133×58)/(0.60×63104×42) = **0.75** (full-range capacity-density definition; usable-window N/P is higher — cell is cathode-limited in simulation, anode margin +12% vs baseline).

## 3. Process Design Parameters

| Parameter | Formula | Value | Unit |
|---|---|---|---|
| Positive areal density | thickness × (1−porosity) × density | 42e-6×0.60×3262 = 82.2 g/m² | g/m² |
| Negative areal density | thickness × (1−porosity) × density | 58e-6×0.62×1657 = 59.6 g/m² | g/m² |
| Positive compaction density | density × (1−porosity) | 3262×0.60 = 1957 kg/m³ = 1.96 g/cm³ | g/cm³ |
| Negative compaction density | density × (1−porosity) | 1657×0.62 = 1027 kg/m³ = 1.03 g/cm³ | g/cm³ |
| Electrolyte fill amount | pore volume × electrolyte density × fill factor | 4.57 mL × 1.2 g/cm³ × 1.0 = 5.5 g | g (literature density 1.2 g/cm³, annotated) |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning | — |

## 4. Mass Breakdown (contract caliber; electrolyte excluded)

| Layer | kg/m² | Mass (g) |
|---|---|---|
| Positive electrode | 0.08220 | 8.44 |
| Negative electrode | 0.05959 | 6.12 |
| Positive CC (Al) | 0.04320 | 4.44 |
| Negative CC (Cu) | 0.10752 | 11.04 |
| Separator | 0.00253 | 0.26 |
| **Total (cell mass for energy density)** | | **30.30** |
| Electrolyte (informational) | | 5.48 (estimate) |

Source: calc-energy cell/r2_v4_energy.json (layer_kg_m2 × area 0.1027 m²); electrolyte excluded from contract mass (parameter set lacks density) — annotated.

## 5. Performance Verification (vs entry-0 criteria)

| Metric | Threshold | Value | Verdict | Source |
|---|---|---|---|---|
| capacity_ah | ≥ 2.0 Ah | 3.438 Ah | ✓ | r2_v4_1c_dfn.json:capacity_ah |
| retention_5c | ≥ 0.95 | 0.987 | ✓ | r2_v4_derived.json:retention_5c (3.393/3.438) |
| power_density_w_kg | ≥ 4000 W/kg | 111,807 W/kg | ✓ | r2_v4_energy.json:power_density_w_kg |
| T_max_K (4C charge @45 °C) | ≤ 333.15 K (60 °C) | 321.94 K (48.8 °C) | ✓ | r2_v4_4c_dfn.json:T_max_K |
| plated (4C charge) | false | false (anode min +22.6 mV) | ✓ | r2_v4_4c_dfn.json:anode_potential_v |

## 6. Design Notes (rationale from evaluate log)

- R0 baseline (Chen2020 unmodified): capacity 4.95 Ah ✓, power density 22,383 W/kg ✓, but retention_5c 0.087 ✗, plated=true ✗, T_max 354.3 K ✗. Root cause: positive solid diffusivity 4e-15 m²/s → particle diffusion time constant ~6.8 ks at r=5.22 µm vs 720 s 5C window (excluded lever: solid diffusivity; allowed lever: particle radius).
- R1: thin electrodes (42/52 µm), porosity 0.40/0.35, particles 1.0/1.5 µm, σ_e 2.0 S/m, t⁺ 0.4, h=100: retention 0.983 ✓, T_max 323.3 K ✓, power ✓, capacity 3.08 ✓; plated=true marginal (−3.9 mV at final charge instant only).
- R2 (final, V4): thicker negative (58 µm, ε 0.38, r 1.0 µm) raises end-of-charge anode potential floor; r_pos 0.8 µm improves charge acceptance; σ_e 2.4 S/m, t⁺ 0.5, D_e 3.5e-10: plated=false (anode min +22.6 mV), retention 0.987, T_max 321.9 K — all criteria pass.
- Conservative alternative V5 (anode-geometry fix only, V1-level transport) also passes all criteria (plated false, +16.0 mV).
