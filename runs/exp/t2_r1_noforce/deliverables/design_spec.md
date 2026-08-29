# Cell Design Specification — F1 (Grid Energy Storage Cell)

**VBF-T2R1NOFORCE-DS-001** | Case: t2_r1_noforce | Date: 2026-08-25 | Base parameter set: Chen2020 (PyBaMM)

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Chen2020 teaching parameterization) | entry-0 meta, base Chen2020 |
| Nominal capacity | 5.0 Ah | parameter set `Nominal cell capacity [A.h]` |
| Verified 1C capacity (25 °C) | 5.0282 Ah | `cell/r5_f1_1c_spme.json:capacity_ah` |
| Voltage window | 2.5 – 4.2 V | parameter set `Upper/Lower voltage cut-off [V]` |
| Dimensions (H × W × T) | 65 × 158 × 0.2008 mm | parameter set `Electrode height/width [m]`; `cell/r5_f1_energy.json:thickness_m` |
| Shell thickness | Not provided (no parameter) | — |
| Electrolyte formulation | EC/EMC + LiPF6 (task default); bulk solvent concentration 2636 mol/m³; EC initial concentration 4541 mol/m³; no additive applied (anode-side ceramic coating used instead) | parameter set `Bulk solvent concentration [mol.m-3]`, `EC initial concentration in electrolyte [mol.m-3]` |
| Cation transference number | 0.2594 | parameter set `Cation transference number` |

## 2. Electrode and separator

| Layer | Material | Thickness (µm) | Porosity | Active vol. fraction | Particle radius (µm) | Density (kg/m³) |
|---|---|---|---|---|---|---|
| Positive electrode | NMC811 | 75.6 | 0.335 | 0.665 | 5.22 | 3262 |
| Negative electrode | Graphite, ceramic-coated (ALD Al2O3/TiO2 class; k_SEI 4e-13 = ×0.4) | 85.2 | **0.42 (design change)** | 0.75 | **3 (design change)** | 1657 |
| Separator | — | 12 | 0.47 | — | — | 397 |
| Positive current collector | Al | 16 | — | — | — | 2700 |
| Negative current collector | Cu | 12 | — | — | — | 8960 |

- **N/P ratio (theoretical full-window areal-capacity ratio, deliverable formula: capacity density × thickness)**: 0.582 for F1 (baseline 0.753). Capacity density = c_max × F/3600 × active vol. fraction × (1−porosity) × thickness → negative 32.91 Ah/m², positive 56.54 Ah/m² (computed from parameter set values above).
- **Practical (reversible) N/P**: ≈ 0.88 — the design is deliberately anode-limited (measured cell capacity 5.0282 Ah below cathode practical capacity ~5.74 Ah from R1); the anode-limiting strategy, combined with porosity 0.42 + 3 µm particles, is what clears the 4C plating criterion.

## 3. Process design parameters

| Parameter | Value | Formula / note |
|---|---|---|
| Positive areal density | 164.0 g/m² | 75.6 µm × (1−0.335) × 3262 kg/m³ (matches `r5_f1_energy.json:layer_kg_m2.positive_electrode`) |
| Negative areal density | 81.9 g/m² | 85.2 µm × (1−0.42) × 1657 kg/m³ (matches `r5_f1_energy.json:layer_kg_m2.negative_electrode`) |
| Positive compaction density | 2.169 g/cm³ | 3262 × 0.665 ÷ 1000 |
| Negative compaction density | 0.961 g/cm³ | 1657 × 0.58 ÷ 1000 |
| Electrolyte fill amount | 8.23 g | pore volume 6.855 cm³ × 1.2 g/cm³ (literature value, annotated) |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning |

## 4. Mass breakdown

| Layer | Mass (g) | Source |
|---|---|---|
| Positive electrode (NMC811) | 16.842 | `r5_f1_energy.json:layer_kg_m2` × 0.1027 m² |
| Negative electrode (coated graphite) | 8.409 | same |
| Positive current collector (Al) | 4.437 | same |
| Negative current collector (Cu) | 11.042 | same |
| Separator | 0.259 | same |
| **Total (contract caliber, electrolyte excluded)** | **40.990** | `r5_f1_energy.json:mass_kg` |
| Electrolyte (annotated, 1.2 g/cm³ literature) | +8.23 | §3 |

## 5. Performance verification

| Metric | Criterion (entry 0) | Measured | Verdict |
|---|---|---|---|
| Energy density | ≥ 327.18 Wh/kg | 435.44 Wh/kg | ✓ PASS |
| SEI thickness @100 cyc | ≤ 500 nm | 439.52 nm | ✓ PASS |
| SEI thickness @500 cyc | ≤ 550 nm | 738.43 nm | ✗ FAIL (documented unreachable — see final entry escalation) |
| −20 °C retention | ≥ 90 % | 99.45 % | ✓ PASS |
| 4C charge plating | none (anode φ ≥ 0 V) | min anode potential +0.0071 V | ✓ PASS |
| 4C max temperature (informational) | — | 359.92 K (86.8 °C, +41.8 K from 45 °C) | reported |

## 6. Design notes (changes vs baseline and why)

1. **Negative particle radius 5.86 → 3 µm** (R2 V1): raises active surface area, drops anode overpotential at 4C — min anode potential −0.192 → −0.138 V.
2. **Negative porosity 0.25 → 0.42** (R3 V3/V6 → R5 F1): the strongest single plating lever (0.35 → −0.074 V; 0.40 → −0.0017 V; 0.42 → **+0.0071 V**).
3. **Ceramic-coated graphite, SEI kinetic rate constant 1e-12 → 4e-13** (R3 C1, ALD Al2O3/TiO2 class): only lever that reduces SEI (−5.6 % @100 cyc, −4.2 % @500 cyc), bringing SEI@100 inside contract (439.5 ≤ 500).
4. Rejected directions (with evidence): N/P rebalance via thicker anode (R4 V7/V8 — SEI scales with anode thickness, both SEI contracts fail); electrolyte scalar overrides (would destroy Nyman2008 T-dependent transport); k_SEI beyond ×0.4 (R5 F2 ×0.1 → 701.4 nm @500 cyc — saturating lever); system switch to OKane2022 (R5 S1 — graphite-only, z_sei=1, SEI worse: 626.8/1067.7 nm).
