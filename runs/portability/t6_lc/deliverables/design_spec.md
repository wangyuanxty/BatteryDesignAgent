# Cell Design Specification — VBF-T6LC-DS-01

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | LNMO (LiNi0.5Mn1.5O4, 4.7 V spinel) positive / graphite negative | `data/LNMO.json` (Chen2020 base + LNMO overrides) |
| Nominal capacity | 4.5 Ah | `data/LNMO.json` `Nominal cell capacity [A.h]` |
| Simulation-verified 1C capacity | 4.804 Ah | `cell/final_1c_dfn_h45.json:capacity_ah` |
| Voltage window | 2.5 – 4.7 V | `data/LNMO.json` lower/upper cut-off |
| Cell dimensions (electrode strip, unwound) | height 65 mm × width 1580 mm; total layer thickness 0.193 mm | `Electrode height [m]`, `Electrode width [m]`, `calc-energy thickness_m` |
| Pouch outer dimensions / shell thickness | Not provided (no shell/casing parameter) | parameter set |
| Electrolyte formulation | EC/EMC + LiPF6 (Nyman2008 transport) | Chen2020 baseline (default) |
| Cation transference number | 0.2594 | Chen2020 `Cation transference number` |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | Active-material volume fraction | Density (kg/m³) | Current collector |
|---|---|---|---|---|---|
| Positive (LNMO) | 57 | 0.335 | 0.665 | 4400 | Al 10 µm |
| Negative (graphite) | 110 | 0.25 | 0.75 | 1657 | Cu 8 µm |
| Separator | 8 | 0.47 | — | 1548 | — |

- N/P ratio = (110 µm × 0.75 × 33133) / (57 µm × 0.665 × 43000) = **1.68** (full-stoichiometry areal capacity ratio; negative capacity density × thickness ÷ positive capacity density × thickness).
- Positive particle radius 5.22 µm, negative particle radius 5.86 µm (Chen2020 baseline, unchanged).

## 3. Process design parameters

| Parameter | Value | Formula / source |
|---|---|---|
| Positive areal density | 166.8 g/m² | 57 µm × (1−0.335) × 4400 kg/m³ |
| Negative areal density | 136.7 g/m² | 110 µm × (1−0.25) × 1657 kg/m³ |
| Positive compaction density | 2.926 g/cm³ | 4400 × (1−0.335) / 1000 |
| Negative compaction density | 1.243 g/cm³ | 1657 × (1−0.25) / 1000 |
| Electrolyte fill amount | 6.2 g | pore volume (5.17 cm³) × 1.2 g/cm³ (literature electrolyte density) × fill factor 1.0 |
| Formation recommendation | 0.1C CC to 4.2 V, 25 ℃, 2 cycles | design recommended value; production value requires tuning |

## 4. Mass breakdown (contract-caliber, electrolyte & casing excluded)

| Layer | Mass (g) | Source |
|---|---|---|
| Positive electrode | 17.13 | `final_1c_energy_dfn_h45.json:layer_kg_m2.positive_electrode` × area |
| Negative electrode | 14.04 | same, `negative_electrode` |
| Positive current collector (Al) | 2.77 | same, `positive_cc` |
| Negative current collector (Cu) | 7.36 | same, `negative_cc` |
| Separator | 0.17 | same, `separator` |
| **Total (calc-energy mass_kg)** | **41.48** | `final_1c_energy_dfn_h45.json:mass_kg` |
| Electrolyte (not in mass_kg) | 6.2 | pore volume × 1.2 g/cm³ (annotated) |

## 5. Performance verification (vs entry-0 criteria)

| Item | Value | Threshold | Determination | Source |
|---|---|---|---|---|
| Volumetric energy density | 1005.8 Wh/L | ≥ 950 Wh/L | ✓ PASS | `final_1c_energy_dfn_h45.json:energy_density_wh_l` |
| Voltage plateau (discharge midpoint) | 4.115 V | ≥ 4.1 V | ✓ PASS | `final_1c_energy_dfn_h45.json:midpoint_voltage_v` |
| 4C fast-charge temperature | 322.59 K (49.44 ℃) | ≤ 323.15 K (50 ℃) | ✓ PASS | `final_4c_safety_h45_dfn.json:T_max_K` |
| 4C fast-charge lithium plating | anode potential min +0.0894 V | ≥ 0 V (no plating) | ✓ PASS | `final_4c_safety_h45_dfn.json:anode_potential_v` |
| Anode SEI thickness after 100 cycles | 9.5 nm (DFN) / 233 nm (SPMe) | ≤ 500 nm | ✓ PASS | `final_aging_dfn_h45.json` / `cell/R5A_aging_k1e-15.json` |

## 6. Design notes

- Voltage plateau ≥ 4.1 V is a cathode-OCP material property; Chen2020 NMC811 baseline midpoint 3.935 V cannot reach it → switched to high-voltage LNMO system (`data/LNMO.json`).
- 4C plating was fixed by raising N/P to 1.68 (negative electrode 85.2 → 110 µm); anode potential moved from −0.176 V (baseline) to +0.0894 V.
- Volumetric ED was preserved despite thicker anode by thinning separator (12 → 8 µm) and current collectors (Al 16 → 10 µm, Cu 12 → 8 µm) and thinning positive electrode (75.6 → 57 µm), which also shortens 1C cycles (less SEI) and reduces 4C heat.
- T_max ≤ 50 ℃ was closed by thermal management `Total heat transfer coefficient` = 45 W/m²/K (aggressive vapor-chamber-class cooling).
- SEI ≤ 500 nm was closed by anode surface coating `SEI kinetic rate constant` = 1×10⁻¹⁵ m/s (1000× slower than Chen2020 baseline 1×10⁻¹² m/s; DFN 9.5 nm, SPMe 233 nm — both pass).
