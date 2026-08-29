# Cell Design Specification — VBF-T5R3-DS-01

**Case**: t5_r3 — next-generation flagship vehicle battery · **Generated**: 2026-08-26 · **Status**: DFN-verified concept (virtual test), true-compute endorsement skipped (`real_compute=false`)

## 1. Basic Specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Chen2020 baseline parameterization) | `param_dump.txt` Chen2020; base determined in funnel entry (start_stage=3) |
| Nominal capacity | 5.0 Ah (parameter set nominal) | `param_dump.txt`: Nominal cell capacity [A.h] |
| Verified 1C capacity | 5.0442 Ah (full-order DFN) | `cell/r6_y4_1c_dfn.json:capacity_ah` |
| Voltage window | 2.5 – 4.2 V | `param_dump.txt`: Upper/Lower voltage cut-off |
| Midpoint voltage | 3.832 V (1C discharge) | `cell/r6_y4_energy_dfn.json:midpoint_voltage_v` |
| Cell dimensions | Stack thickness 178.8 µm × electrode area 0.1027 m² (height 0.065 m × width 1.58 m) | `r6_y4_energy_dfn.json:thickness_m/area_m2`; geometry `param_dump.txt` |
| Shell / enclosure thickness | Not provided (no parameter) | — |
| Electrolyte formulation | Chen2020 baseline (LiPF6 EC/EMC-type) with transport upgrade: conductivity 5.0 S/m (constant), cation transference number **0.6**, diffusivity 9e-10 m²/s | `cell/params_y4.json` (design overrides); no additive candidates invented (case starts at Stage 3 — recorded in funnel entry) |
| Cation transference number | 0.6 (baseline default 0.2594) | `cell/params_y4.json` |

## 2. Electrode and Separator

| Layer | Thickness | Porosity | AM volume fraction | Density | Source |
|---|---|---|---|---|---|
| Positive electrode (NMC811) | 75.6 µm | 0.335 | 0.665 | 3262 kg/m³ | `param_dump.txt` Chen2020 (baseline, not overridden) |
| Negative electrode (graphite) | 85.2 µm | 0.25 | 0.75 | 1657 kg/m³ | `param_dump.txt` Chen2020 |
| Separator | **7 µm** (baseline 12 µm) | 0.47 | — | (mass ref 210 kg/m³ eq.) | `cell/params_y4.json` override + `param_dump.txt` |
| Positive current collector | **Al 6 µm** (baseline 16 µm) | — | — | 2700 kg/m³ | `cell/params_y4.json` + `param_dump.txt` |
| Negative current collector | **Cu 5 µm** (baseline 12 µm) | — | — | 8960 kg/m³ | `cell/params_y4.json` + `param_dump.txt` |
| Particle radii | Positive + negative both **3 µm** (baseline 5.22 / 5.86 µm) | — | — | — | `cell/params_y4.json` |

**N/P ratio ≈ 1.19** — areal capacities: negative = 8.52e-4 cm × 0.75 × 1.657 g/cm³ × 372 mAh/g = 3.94 mAh/cm²; positive = 7.56e-4 × 0.665 × 3.262 × 201 = 3.30 mAh/cm². *(Specific capacities 372 / 201 mAh/g are domain-standard literature defaults, annotated — Chen2020 parameter set does not expose per-electrode capacity-density keys.)*

## 3. Process Design Parameters

| Parameter | Value | Formula | Note |
|---|---|---|---|
| Positive areal density | 163.99 g/m² | thickness × (1−ε) × ρ = 16.842 g ÷ 0.1027 m² | mechanical |
| Negative areal density | 105.88 g/m² | 10.874 g ÷ 0.1027 m² | mechanical |
| Positive compaction density | 2.169 g/cm³ | 3262 × 0.665 ÷ 1000 | ÷1000 note per spec |
| Negative compaction density | 1.243 g/cm³ | 1657 × 0.75 ÷ 1000 | ÷1000 note per spec |
| Electrolyte fill amount | 6.15 g | pore volume 5.126 cm³ × 1.2 g/cm³ (fill factor 1.0) | electrolyte density = literature value 1.2 g/cm³, annotated |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | — | design recommended value; actual production-line value requires tuning |

## 4. Mass Breakdown (DFN-verified geometry)

| Layer | Mass (g) | Basis |
|---|---|---|
| Positive electrode (coating) | 16.842 | `r6_y4_energy_dfn.json:layer_kg_m2.positive_electrode` × 0.1027 m² |
| Negative electrode (coating) | 10.874 | same, negative_electrode |
| Positive current collector (Al) | 1.664 | layer_kg_m2.positive_cc |
| Negative current collector (Cu) | 4.601 | layer_kg_m2.negative_cc |
| Separator | 0.151 | layer_kg_m2.separator |
| **Total (contract caliber, electrolyte excluded)** | **34.132** | `r6_y4_energy_dfn.json:mass_kg` — matches Σ automatically |
| Electrolyte (est., annotated) | 6.15 | pore volume × 1.2 g/cm³ |
| Total incl. electrolyte | 40.28 | contract formula excludes electrolyte — noted |

## 5. Performance Verification (thresholds from task text, entry-0 contract)

| Item | Value | Threshold | Determination | Source |
|---|---|---|---|---|
| 1C capacity | 5.0442 Ah | no contractual threshold (info) | — | `r6_y4_1c_dfn.json:capacity_ah` |
| Energy density | **535.72 Wh/kg** | ≥ 500.94 Wh/kg | **✓ PASS** | `r6_y4_energy_dfn.json:energy_density_wh_kg` (contract formula, electrolyte excluded) |
| Volumetric energy density | 995.79 Wh/L | info | — | `r6_y4_energy_dfn.json:energy_density_wh_l` |
| 4C max temperature | **327.60 K (54.4 °C)** | ≤ 333.15 K (≤ 60 °C) | **✓ PASS** | `r6_y4_4c_dfn.json:T_max_K` |
| 4C lithium plating | min anode potential **+0.0200 V** (never < 0) | plated = false | **✓ PASS** | `r6_y4_4c_dfn.json:anode_potential_v` |
| 4C CC charge window | 0 → ≈69% SOC (3.48 Ah) in 626 s at 20 A, then 4.2 V cut-off | info (task = "support 4C fast charge (no plating)"; CV tail at decaying current, plating risk monotonic with current — domain reasoning, not simulated) | — | `r6_y4_4c_dfn.json:time_s/voltage_v` (charge step, 20 A) |
| DC resistance | 2.723 mΩ | info | — | `r6_y4_energy_dfn.json:dcr_ohm` |
| Power density | 45,030 W/kg | info | — | `r6_y4_energy_dfn.json:power_density_w_kg` |

Verified with full-order DFN (`model_used: DFN`, no solver fallback).

## 6. Design Notes

- **Why these changes**: baseline Chen2020 = ED 400.29 Wh/kg / 4C plated (min_ap −0.438 V, CC window ≈26 s) / T_max 332.35 K (round 1). Root cause of plating = electrolyte salt transport (4 isolation simulations, round 2). Levers: thin CC/sep/particles + transport upgrade (σ 5.0 S/m, t⁺ 0.6, D_e 9e-10) + double-sided cooling area 0.01062 m² + mild thermal tuning h=26 W/m²K (≈6.6 mV/K kinetic margin leverages self-heating; finalists warm→327.6–331.2 K, still ≥2.5 K below 333.15 K). Honest true-4C rebuild at 5 Ah actual (round 4 honesty probes caught an earlier 6.55 Ah nameplate artifact and it was rejected). Finalists Y4 (above) and Y3 (Al 8 µm / sep 9 µm, ED 526.24, min_ap +0.0162 V) both DFN-verified (round 6).
- 5 µm Cu / 6 µm Al foils are aggressive for winding — Y3 (8 µm Al / 9 µm sep) is the supply-friendly alternate with almost identical electrical performance.
- Full rationale per round: `log.jsonl` rounds 1–6 (propose/evaluate entries).