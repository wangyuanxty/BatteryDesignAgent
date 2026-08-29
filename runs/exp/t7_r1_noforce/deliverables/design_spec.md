# Cell Design Specification — VBF-T7R1NOFORCE-DS-01

**Case**: `t7_r1_noforce` — HEV battery (NMC811/graphite, Chen2020 baseline) · **Date**: 2026-08-25
All values mechanically taken from parameter-set dump / simulation output files / literature; source annotated per row. Numbers not in any tool output are written as "Not provided".

## 1. Basic Specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 (positive) / graphite (negative) | `--base Chen2020` parameter set (entry 0 meta) |
| Nominal capacity | 5.0 Ah | Chen2020 `Nominal cell capacity [A.h]` |
| Simulated 1C discharge capacity | 5.0065 Ah | `cell/r5_slim_1c_dfn.json` |
| Voltage window | 2.5 – 4.2 V | Chen2020 `Lower/Upper voltage cut-off [V]` |
| Discharge midpoint voltage | 3.826 V | `cell/r5_slim_energy.json` (calc-energy) |
| Electrode dimensions (unfolded) | 65 mm (height) × 1580 mm (width) | Chen2020 `Electrode height/width [m]`; area 0.1027 m² |
| Layer stack thickness | 186.8 µm (75.6 + 10 + 85.2 + 6 + 10) | Chen2020 + `params_r5_slim.json`; calc-energy `thickness_m` |
| Cell volume | 1.9184×10⁻⁵ m³ (19.18 cm³) | `cell/r5_slim_energy.json` (calc-energy `volume_m3`) |
| Shell / enclosure thickness | Not provided (no shell parameter in parameter set) | — |
| Electrolyte formulation | LiPF₆ in carbonate solvent, per Chen2020 parameterization; exact solvent composition Not provided (parameter set has no composition parameter). Design transport overrides: σ = 2.5 S/m, D = 5×10⁻¹⁰ m²/s, t⁺ = 0.5 | Chen2020 (baseline: t⁺ 0.2594; σ, D = Nyman2008 functions) + `params_r5_slim.json` (overrides, bridge estimates — flagged in propose R1) |
| Cation transference number | 0.5 (design) / 0.2594 (baseline) | `params_r5_slim.json` / Chen2020 |

## 2. Electrode, Separator, Current Collectors

| Layer | Thickness (µm) | Porosity | Active-material vol. frac. | Density (kg/m³) | Material / note | Source |
|---|---|---|---|---|---|---|
| Positive electrode (NMC811) | 75.6 | 0.335 | 0.665 | 3262 | unchanged from baseline | Chen2020 |
| Negative electrode (graphite) | 85.2 | 0.25 | 0.75 | 1657 | particle radius 4.0 µm (design), Al₂O₃ ALD coating → SEI k = 7.5×10⁻¹³ m/s | `params_r5_slim.json` |
| Separator | 10 (baseline 12) | 0.47 | — | 397 | design thinning | `params_r5_slim.json` / Chen2020 |
| Positive current collector (Al) | 10 (baseline 16) | — | — | 2700 | design thinning | `params_r5_slim.json` / Chen2020 |
| Negative current collector (Cu) | 6 (baseline 12) | — | — | 8960 | design thinning | `params_r5_slim.json` / Chen2020 |

**N/P ratio** (spec formula: negative capacity density × thickness ÷ positive capacity density × thickness; capacity density = c_max × (1−ε) × F/3600):

| Quantity | Value | Formula / source |
|---|---|---|
| Negative capacity density | 666,017 Ah/m³ | 33133 × 0.75 × 96485/3600 (Chen2020 `Maximum concentration in negative electrode`) |
| Positive capacity density | 1,124,723 Ah/m³ | 63104 × 0.665 × 96485/3600 (Chen2020 `Maximum concentration in positive electrode`) |
| **N/P** | **0.667** | (666,017 × 85.2×10⁻⁶) / (1,124,723 × 75.6×10⁻⁶) = 56.74 / 85.03 Ah/m² |

Note: in this parameterization the negative electrode is the limiting electrode (usable-window N/P = 1.00 by charge balance: 1C discharge 5.0065 Ah, negative stoich 0.901→0.042, positive 0.270→0.843 — Chen2020 initial concentrations).

## 3. Process Design Parameters

| Parameter | Formula | Value | Unit note / source |
|---|---|---|---|
| Positive areal density | thickness × (1−porosity) × density | 163.99 g/m² | calc-energy `layer_kg_m2.positive_electrode` |
| Negative areal density | thickness × (1−porosity) × density | 105.88 g/m² | calc-energy `layer_kg_m2.negative_electrode` |
| Separator areal weight | thickness × (1−porosity) × density | 2.10 g/m² | calc-energy `layer_kg_m2.separator` (tool caliber: solid fraction) |
| Positive compaction density | density × (1−porosity) ÷ **1000** | 2.169 g/cm³ | 3262 × 0.665 / 1000 (kg/m³ → g/cm³) |
| Negative compaction density | density × (1−porosity) ÷ **1000** | 1.243 g/cm³ | 1657 × 0.75 / 1000 |
| Electrolyte fill amount | pore volume × electrolyte density × fill factor | 5.27 cm³ / 6.33 g | pore volume = 0.1027 m² × (75.6µm×0.335 + 85.2µm×0.25 + 10µm×0.47) = 5.27 cm³; electrolyte density 1.2 g/cm³ (literature value, annotated); fill factor 1.0 (assumed) |
| Formation recommendation | — | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning |

## 4. Mass Breakdown (contract caliber: electrolyte excluded)

| Layer | kg/m² | Mass (g) | Source |
|---|---|---|---|
| Positive electrode coating | 0.163994 | 16.842 | calc-energy `layer_kg_m2` × 0.1027 m² |
| Negative electrode coating | 0.105882 | 10.874 | 〃 |
| Positive CC (Al, 10 µm) | 0.027000 | 2.773 | 〃 |
| Negative CC (Cu, 6 µm) | 0.053760 | 5.521 | 〃 |
| Separator | 0.002104 | 0.216 | 〃 |
| **Total (electrolyte excluded)** | 0.352740 | **36.226** | calc-energy `mass_kg` |
| Electrolyte (estimate, not in contract caliber) | — | 6.33 | §3 fill amount |
| **Total incl. electrolyte estimate** | — | **42.55** | — |

## 5. Performance Verification (vs entry-0 criteria)

| Item | Result | Threshold | Verdict | Source |
|---|---|---|---|---|
| 1C discharge capacity | 5.0065 Ah | nominal 5.0 (informational) | ✓ | `cell/r5_slim_1c_dfn.json` |
| Energy density | 491.471 Wh/kg (928.06 Wh/L) | ≥ 327.18 Wh/kg | ✓ (+164.3) | `cell/r5_slim_energy.json` |
| 4C fast charge @45 °C — lithium plating | anode surface potential min = +0.0153 V → plated = false | plated = false | ✓ | `cell/r5_slim_4c45.json` (`anode_potential_v`); log-evaluate R5 mechanical derivation |
| 4C fast charge @45 °C — temperature | T_max = 325.54 K (+7.39 K over 318.15 K ambient) | 573 K red line (informational) | ✓ | `cell/r5_slim_4c45.json` |
| SEI after 100 cyc @45 °C | 510.51 nm | ≤ 550 nm | ✓ (+39.5 nm) | `cell/r5_slim_aging45.json` |
| Nail penetration (10 W) thermal runaway | triggered = false; T_final = 317.0 K (equilibrium T_amb 298.15 K + 10 W / 0.531 W/K) | triggered = false | ✓ | `validation/r5_slim_nail.json` |
| DC internal resistance | 2.6415 mΩ | informational | — | `cell/r5_slim_energy.json` |
| Power density | 43.24 kW/kg | informational (HEV context) | — | `cell/r5_slim_energy.json` |

## 6. Design Notes (parameters changed vs Chen2020 baseline, with reasoning trace)

| Parameter | Baseline | Design | Why (reasoning trace) |
|---|---|---|---|
| Negative particle radius | 5.86 µm | 4.0 µm | 4C plating margin driver (~−17 mV/µm, empirical R2→R3); raised anode min from +12.6 mV (R3) / +11.2 mV (R4) to +15.3 mV (R5) |
| Negative electrode thickness | 85.2 µm | 85.2 µm (reverted after R3 92 µm / R4 95.2 µm) | SEI driver at 45 °C (+~7 nm/µm, empirical R2→R3→R4); R4 95.2 µm failed SEI 551.97 nm → revert |
| SEI kinetic rate constant | 1×10⁻¹² m/s | 7.5×10⁻¹³ m/s (Al₂O₃ ALD coating) | modest ~−18 nm SEI benefit (solvent-diffusion-limited regime at ~500 nm, L·k/D_ec ≈ 1×10⁹ ≫ 1 — plan-update entry); monotone, retained |
| Separator thickness | 12 µm | 10 µm | electrolyte-phase transport + mass (propose R1) |
| Positive CC (Al) | 16 µm | 10 µm | mass reduction, ED lever (propose R1) |
| Negative CC (Cu) | 12 µm | 6 µm | mass reduction, ED lever (propose R1) |
| Electrolyte σ / D / t⁺ | Nyman2008 functions / 0.2594 | 2.5 S/m / 5×10⁻¹⁰ m²/s / 0.5 | transport overrides (bridge estimates, flagged) — 4C plating margin (propose R1) |
| Total heat transfer coefficient | 10 W/m²/K | 100 W/m²/K (liquid cooling) | nail criterion load-bearing: without cooling (near-adiabatic hA ≈ 0.05 W/K) nail triggers (R1); with h = 100, hA = 0.531 W/K → triggered = false (R2–R5) |

Design evolution summary (audit: log.jsonl rounds R1–R5): R1 baseline FAIL (plating, anode −0.192 V; nail triggered) → R1b ceiling probe (ED 486 Wh/kg, no stage-2 escalation needed) → R2 cooling FAIL (plating −0.008 V) → R3 rate-ready anode PASS (margins thin) → R4 margin attempt FAIL (SEI 551.97 nm) → **R5 final PASS all four criteria**.
