# Cell Design Specification — archN_robust (VBF-T5R1SINGLEMODEL-DS-001)

> Case: t5_r1_singlemodel — next-generation flagship vehicle cell. All values mechanically taken from parameter set / simulation output / literature and source-annotated per line. Missing items are written "Not provided"; no numbers from memory.

## 1. Basic Specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (LG M50-class parameterization, no SiOx) | base parameter set OKane2022 (anchor-table default for task without named electrode system: Chen2020-class; recorded in entry 0) |
| Nominal capacity | 5.0 Ah (parameter set) / 5.0374 Ah (1C DFN discharge measured) | `OKane2022:Nominal cell capacity [A.h]` / `cell/r5_final_archN_1c_dfn.json:capacity_ah` |
| Voltage window | 2.5 – 4.2 V | `OKane2022:Lower/Upper voltage cut-off [V]` |
| Nominal (midpoint) voltage | 3.7106 V (1C DFN discharge, mid-time sample) | `cell/r5_final_archN_energy_dfn.json:midpoint_voltage_v` |
| Cell dimensions | 65 mm (height) × 1580 mm (width) × 0.1848 mm (layer-stack thickness); shell thickness Not provided (no parameter) | `OKane2022:Electrode height/width [m]`; thickness = Σ layer thickness from `calc-energy` |
| Electrolyte formulation | OKane2022 base electrolyte (LiPF6, EC/EMC-class; base transport parameters overridden) + additive candidates VC / FEC / DTD (qualitative recommendation, mace-screened pass) | `OKane2022` base; overrides `candidates/r4_archN_params.json`; `validation/r5_molecules_mace.json` |
| Electrolyte conductivity σ | 3.5 S·m⁻¹ (design override) | `candidates/r4_archN_params.json:"Electrolyte conductivity [S.m-1]"` |
| Electrolyte diffusivity D | 1.2×10⁻⁹ m²·s⁻¹ (design override) | `candidates/r4_archN_params.json:"Electrolyte diffusivity [m2.s-1]"` |
| Cation transference number t⁺ | 0.55 (design override) | `candidates/r4_archN_params.json:"Cation transference number"` |
| Cooling | h = 45.0 W·m⁻²·K⁻¹ (design override; within safe window — h>45 overcools the anode and risks plating, measured in R3) | `candidates/r4_archN_params.json:"Total heat transfer coefficient [W.m-2.K-1]"` |

## 2. Electrode and Separator

| Layer | Thickness (µm) | Porosity | Material / notes | Source |
|---|---|---|---|---|
| Positive electrode | 75.6 | 0.40 | NMC811; AM volume fraction 0.665 (base-set) | `OKane2022:Positive electrode thickness [m]` + override `Positive electrode porosity` |
| Negative electrode | 85.2 | 0.22 | graphite; AM volume fraction 0.75 (base-set) | `OKane2022:Negative electrode thickness [m]` + override `Negative electrode porosity` |
| Separator | 10.0 | 0.47 | base OKane2022 separator (397 kg·m⁻³) | override `Separator thickness [m]`; `OKane2022:Separator porosity/density` |
| Positive current collector | 8.0 | — | Al, 2700 kg·m⁻³ | override `Positive current collector thickness [m]`; `OKane2022:Positive current collector density` |
| Negative current collector | 6.0 | — | Cu, 8960 kg·m⁻³ | override `Negative current collector thickness [m]`; `OKane2022:Negative current collector density` |
| Particle size | pos r = 2.0 µm / neg r = 2.2 µm | — | reduced from base to boost 4C kinetics (plating margin +21.5 mV) | `candidates/r4_archN_params.json` |
| N/P ratio | 1.00 (voltage-cutoff equilibrium caliber) | — | inferred: OCP-endpoint solve at 2.5/4.2 V with lithium conservation; equilibrium capacity 5.097 Ah vs simulated 5.037 Ah (+1.2%, kinetic cutoffs). Stoich windows x_p 0.268–0.851, x_n 0.030–0.905. Cell is negative-limited in practice (measured R2: −8% neg thickness → −7.9% capacity); plating avoidance is secured by transport bridge + particle sizing rather than anode oversize | `_np_ratio.py` (mechanical, from OKane2022 OCP CSV + concentrations) |

## 3. Process Design Parameters

| Parameter | Formula | Value | Source |
|---|---|---|---|
| Positive areal density | thickness × (1−porosity) × density | 0.14796 kg·m⁻² = 147.96 g·m⁻² | `r5_final_archN_energy_dfn.json:layer_kg_m2.positive_electrode` |
| Negative areal density | thickness × (1−porosity) × density | 0.11012 kg·m⁻² = 110.12 g·m⁻² | `r5_final_archN_energy_dfn.json:layer_kg_m2.negative_electrode` |
| Positive compaction density | density × (1−porosity) ÷ 1000 | 3262 × 0.60 / 1000 = 1.957 g·cm⁻³ | `OKane2022:Positive electrode density` + override porosity |
| Negative compaction density | density × (1−porosity) ÷ 1000 | 1657 × 0.78 / 1000 = 1.293 g·cm⁻³ | `OKane2022:Negative electrode density` + override porosity |
| Electrolyte fill amount | pore volume × electrolyte density × fill factor | (75.6×0.40 + 85.2×0.22 + 10×0.47) µm × 0.1027 m² = 5.51 cm³ × 1.2 g·cm⁻³ × 1.0 = 6.62 g | pore volume from layer parameters; electrolyte density 1.2 g·cm⁻³ literature value (annotated); fill factor 1.0 assumed |
| Formation recommendation | design recommended value | 0.1C CC charge to 4.2 V, 25 °C, 2 cycles — design recommended value; actual production-line value requires tuning | annotated (design recommendation) |

## 4. Mass Breakdown (calc-energy contract caliber: electrolyte excluded)

| Layer | kg·m⁻² | g/cell (area 0.1027 m²) | Source |
|---|---|---|---|
| Positive electrode | 0.14796 | 15.20 | `r5_final_archN_energy_dfn.json:layer_kg_m2` |
| Negative electrode | 0.11012 | 11.31 | same |
| Positive current collector (Al) | 0.02160 | 2.22 | same |
| Negative current collector (Cu) | 0.05376 | 5.52 | same |
| Separator | 0.00210 | 0.22 | same |
| **Total (contract caliber)** | 0.33555 | **34.46** | `r5_final_archN_energy_dfn.json:mass_kg` |
| Electrolyte (BOM caliber only) | — | 6.62 (literature density 1.2 g·cm⁻³) | see process table |
| **Total with electrolyte** | — | **41.08** | inferred |

## 5. Performance Verification (vs entry-0 criteria)

| Item | Value | Criterion | Determination | Source |
|---|---|---|---|---|
| Gravimetric energy density | 533.18 Wh/kg (1C DFN) | ≥ 500.94 Wh/kg | ✓ PASS (+32.2) | `cell/r5_final_archN_energy_dfn.json:energy_density_wh_kg` (SPMe cross-check 531.85, +0.25%) |
| Volumetric energy density | 968.10 Wh/L | not a criteria metric | informational | `cell/r5_final_archN_energy_dfn.json:energy_density_wh_l` |
| Max temperature, 4C fast charge | 330.50 K = 57.35 °C | ≤ 333.15 K (60 °C) | ✓ PASS (2.65 K margin) | `cell/r4_archN_4c_dfn.json:T_max_K` (protocol 4C_charge_45C, T_amb 318.15 K) |
| Lithium plating, 4C fast charge | anode potential min +0.0215 V | plated = false | ✓ PASS (no plating, +21.5 mV margin) | `cell/r4_archN_4c_dfn.json:anode_potential_v` min |
| 1C discharge capacity | 5.0374 Ah | — | informational | `cell/r5_final_archN_1c_dfn.json:capacity_ah` |
| DC resistance (1C-derived) | 15.89 mΩ | — | informational | `cell/r5_final_archN_energy_dfn.json:dcr_ohm` |
| Power density (theoretical peak) | 7707 W·kg⁻¹ | — | informational | `cell/r5_final_archN_energy_dfn.json:power_density_w_kg` |

## 6. Design Notes

- **Mass levers (ED)**: current collectors thinned to 8/6 µm and separator to 10 µm; positive porosity raised 0.335→0.40 — the positive electrode has large capacity slack (measured R1: porosity 0.40 costs no capacity because the negative electrode binds capacity), so porosity became a free mass lever (+ED without capacity loss). Baseline ED 400.8 → final 533.2 Wh/kg (DFN).
- **Safety levers (4C plating + temperature)**: electrolyte transport bridge (σ 3.5 S·m⁻¹ / D 1.2×10⁻⁹ m²·s⁻¹ / t⁺ 0.55) + small particles (2.0/2.2 µm) + h = 45 W·m⁻²·K⁻¹. Cooling-vs-plating trade-off measured: h = 50/60 overcools the anode → potential dips below 0 V; h = 45 sits inside the safe window (R3/R4 evaluations, log.jsonl).
- **Negative-limited cell**: N/P ≈ 1.00 at the voltage-cutoff equilibrium caliber; the negative electrode binds cell capacity (R2 measurement). This is the honest consequence of the mass-first design; plating is instead suppressed kinetically (transport bridge) — anode margin +21.5 mV at 4C.
- **Additives**: VC / FEC / DTD screened under the funnel_voting OFF ablation (run-mlp(mace) only, hard lines converged=true and energy_ev ≤ 0.0 eV — all passed; no disputed). Recommended qualitatively for SEI film formation to support fast charge; cell-level additive effect is not simulatable in this library (no additive bridge parameter) — recorded honestly.
- **Not provided**: shell/enclosure thickness (no parameter), electrode binder/conductive-additive parameters (base set has AM + porosity only — BOM split uses literature defaults, annotated), cycle-life simulation (no aging run in this case; aging model available in library), mechanical/abuse tests (outside pure-simulation boundary).
