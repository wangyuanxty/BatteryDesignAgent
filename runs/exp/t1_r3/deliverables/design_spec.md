# Cell Design Specification — V11 (t1_r3)

**Document number**: VBF-EXPT1R3-DS-01
**Case**: t1_r3 — next-generation pure electric sedan battery (ED ≥ 392.61 Wh/kg, 4C fast charge without plating, T_max ≤ 60 °C, overcharge 4.7 V without thermal runaway)
**Date**: 2026-08-26
**Caliber note**: all values mechanically taken from the Chen2020 parameter set, the V11 parameter file, and simulation outputs (`runs/exp/t1_r3/cell/r5_v11_*.json`); per-line sources annotated. Cell-level virtual design; engineering manufacturing drawings (tolerances) and line process cards are outside the pure-simulation boundary.

## 1. Basic Specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 (LG M50 calibration) / graphite | Chen2020 parameter set (OCP functions nmc_LGM50_ocp_Chen2020 / graphite_LGM50_ocp_Chen2020) |
| Nominal capacity | 5.085 Ah (calibrated to measured 1C capacity, R5) | `runs/exp/t1_r3/cell/r5_v11_final.json` |
| Measured 1C capacity | 5.0849 Ah (1C CC discharge to 2.5 V, 25 °C) | `runs/exp/t1_r3/cell/r5_v11_1c_spme.json:capacity_ah` |
| Voltage window | 2.5 – 4.2 V | Chen2020: Lower/Upper voltage cut-off |
| Electrode dimensions | height 65 mm × width 1580 mm (single unwound layer, area 0.1027 m²) | Chen2020: Electrode height/width |
| Cell shell dimensions (H×W×T) | Not provided (no shell parameter in the set) | — |
| Layer stack thickness | 184.8 µm (75.6 + 85.2 + 8 + 10 + 6 µm) | `r5_v11_energy.json:thickness_m` |
| Electrolyte | 1 M LiPF6 base (Nyman2008 transport model); design transport targets σ=1.8 S/m, D=6.0e-10 m²/s, t⁺=0.55 (advanced-electrolyte estimate, flagged in plan) | Chen2020 functions + `r5_v11_final.json` |
| Additive candidates | None evaluated (no Stage-2 molecular funnel in this case; task is cell-design level) | — (honest omission) |
| Cation transference number | 0.55 | `r5_v11_final.json` |

## 2. Electrode and Separator

| Layer | Thickness | Porosity | Active volume fraction | Particle radius | Density | Source |
|---|---|---|---|---|---|---|
| Positive (NMC811) | 75.6 µm | 0.45 | 0.55 | 0.8 µm | 3262 kg/m³ | Chen2020 (thickness/density) + `r5_v11_final.json` (porosity/radius) |
| Negative (graphite) | 85.2 µm | 0.42 | 0.58 | 0.8 µm | 1657 kg/m³ | same |
| Separator | 8 µm | 0.60 | — | — | 397 kg/m³ | same |
| Positive current collector | 10 µm Al | — | — | — | 2700 kg/m³ | same |
| Negative current collector | 6 µm Cu | — | — | — | 8960 kg/m³ | same |

**N/P ratio**: 0.624 geometric = (ε_am·c_max·δ)neg ÷ (ε_am·c_max·δ)pos = (0.58 × 33133 × 85.2 µm) ÷ (0.55 × 63104 × 75.6 µm), per the template formula, from parameter-set keys (c_max values read from pybamm Chen2020 set; ε_am = 1 − porosity). **Caveat**: the Chen2020 negative OCP fit saturates above stoich 0.90 (OCP_neg(0.90) = OCP_neg(1.00) = 0.092 V, mechanically evaluated), so the practical negative window differs from the geometric window; the as-operated N/P is therefore verified by simulation instead: plating-free at true 4C with anode potential min +0.0425 V (`r5_v11_4c.json:anode_potential_v`).

## 3. Process Design Parameters

| Parameter | Value | Formula | Source |
|---|---|---|---|
| Positive areal density | 135.63 g/m² | δ × (1−ε) × ρ = 75.6e-6 × 0.55 × 3262 | `r5_v11_energy.json:layer_kg_m2.positive_electrode` |
| Negative areal density | 81.88 g/m² | δ × (1−ε) × ρ = 85.2e-6 × 0.58 × 1657 | `r5_v11_energy.json:layer_kg_m2.negative_electrode` |
| Positive compaction density | 1.79 g/cm³ | ρ × (1−ε) = 3262 × 0.55 / 1000 | derived from Chen2020 + porosity |
| Negative compaction density | 0.96 g/cm³ | ρ × (1−ε) = 1657 × 0.58 / 1000 | derived from Chen2020 + porosity |
| Electrolyte fill amount | 9.19 g | pore volume × 1.2 g/cm³ × 1.0 = 7.662 cm³ × 1.2 | pore volume = A×(δ_pos·ε_pos + δ_neg·ε_neg + δ_sep·ε_sep); electrolyte density 1.2 g/cm³ literature value, fill factor 1.0 idealized |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning | — |

## 4. Mass Breakdown

| Component | Mass (g) | Source |
|---|---|---|
| Positive electrode (active solids) | 13.930 | `r5_v11_energy.json:layer_kg_m2.positive_electrode` × 0.1027 m² × 1000 |
| Negative electrode (active solids) | 8.409 | `r5_v11_energy.json:layer_kg_m2.negative_electrode` × 0.1027 m² × 1000 |
| Positive current collector (Al) | 2.773 | `r5_v11_energy.json:layer_kg_m2.positive_cc` × 0.1027 m² × 1000 |
| Negative current collector (Cu) | 5.521 | `r5_v11_energy.json:layer_kg_m2.negative_cc` × 0.1027 m² × 1000 |
| Separator | 0.130 | `r5_v11_energy.json:layer_kg_m2.separator` × 0.1027 m² × 1000 |
| **Total (contract caliber, electrolyte excluded)** | **30.763** | `r5_v11_energy.json:mass_kg` (calc-energy contract: electrolyte density absent from parameter set → excluded) |
| Electrolyte (additive) | 9.19 | see §3 fill amount; NOT in contract mass |
| Total incl. electrolyte | 40.77 | sum |

## 5. Performance Verification

| Item | Result | Criterion (entry 0) | Verdict | Source |
|---|---|---|---|---|
| Energy density | 605.33 Wh/kg | ≥ 392.61 Wh/kg | ✓ PASS | `r5_v11_energy.json:energy_density_wh_kg` |
| Volumetric energy density | 981.20 Wh/L | (informational) | — | `r5_v11_energy.json:energy_density_wh_l` |
| 1C discharge capacity | 5.0849 Ah | (no capacity threshold registered) | informational | `r5_v11_1c_spme.json:capacity_ah` |
| 4C fast charge acceptance | 4.677 Ah = 92.0% of 1C capacity in 13.8 min at 20.34 A (true 4C) | task: "support 4C fast charge" | ✓ (no plating + full charge reachable) | `r5_v11_4c.json:capacity_ah` × nominal 5.085 |
| 4C plating determination | anode potential min +0.0425 V (≥ 0 V) | plated = false | ✓ PASS | `r5_v11_4c.json:anode_potential_v` |
| 4C maximum temperature | 321.2 K (48.0 °C) | T_max_K ≤ 333.15 K | ✓ PASS | `r5_v11_4c.json:T_max_K` |
| Overcharge to 4.7 V | v reached 4.700 V; T_max 298.57 K; thermal-runaway triggered = false | triggered = false; T_max ≤ 333.15 K | ✓ PASS | `r5_v11_oc.json` + `r5_v11_tr.json` |
| Rated energy | 18.622 Wh | — | — | `r5_v11_energy.json:energy_wh` |

## 6. Design Notes

Changes vs the Chen2020 baseline and why (reasoning cited from the evaluate log rounds R1–R6):

1. **Transport/kinetics pack** (R2 V1 → kept in all later variants): electrolyte conductivity 1.8 S/m (constant, replaces the Nyman2008 temperature function — advanced-electrolyte ceiling assumption, flagged in the Stage-1 plan), D 6.0e-10 m²/s, t⁺ 0.55, porosity 0.45/0.42. Effect: anode potential −0.19 V → +0.005 V (plating removed), T_max 354 K → 328 K (R2 evaluate).
2. **Particle size 0.8 µm** (R4 V9): 2× active surface vs 1.5 µm — widened the 4C anode margin to +0.0424 V (R4 evaluate).
3. **Current collectors 16/12 → 10/6 µm** (R4 V9): holds ED far above the 392.61 target despite added porosity mass.
4. **Thermal: h = 120 W/m²/K** (R4 V9): 4C T_max 321.0 K; overcharge T_max 298.57 K.
5. **Nominal capacity 5.085 Ah** (R5 V11): calibrated to the measured 1C capacity so the harness 4C protocol (4×nominal = 20.34 A) is a true 4C — units diagnosis of the earlier apparent "acceptance plateau" (charge capacity_ah is C-rate-normalized duration; true Ah = reported × nominal).
6. **N/P lever**: tested in R3 (V7) and found net-negative at 4C (thicker negative lengthens the diffusion path) — not used.
