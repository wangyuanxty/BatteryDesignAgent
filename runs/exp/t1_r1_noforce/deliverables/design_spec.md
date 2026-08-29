# Cell Design Specification — t1_r1_noforce (C7 plating-margin-robust)

VBF-T1R1NOFORCE-DS-01 · Generation date: 2026-08-25 · Virtual design (simulation-based; no physical build)

## 1. Basic Specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Chen2020 baseline parameter set, pure-graphite negative) | `--base Chen2020`, parameter dump (no SiOx keys) |
| Nominal capacity | 5.0 Ah (parameter set) / 5.654 Ah (simulated 1C, 25 °C) | `cell/r6_c7_1c_spme.json:capacity_ah` |
| Voltage window | 2.5 – 4.2 V (charge upper cut-off 4.2 V; overcharge protocol = +0.5 V → 4.7 V, matching task spec) | Chen2020 dump `Upper/Lower voltage cut-off [V]` |
| Electrode geometry | 0.065 m × 1.58 m = 0.1027 m² (unwound electrode, parameter-set geometry) | Chen2020 dump `Electrode height/width [m]` |
| Cell stack thickness | 210.6 µm (75.6 + 95 + 16 + 12 + 12 µm); shell thickness: Not provided | `cell/r6_c7_energy.json:thickness_m` |
| Electrolyte formulation | EC/EMC + LiPF6 (baseline) with transport overrides: conductivity 1.8 S/m, diffusivity 5e-10 m²/s (formulation-bridge **estimates**, not simulation output) | `cell/r6_c7_params.json` |
| Cation transference number | 0.5 (override; baseline 0.2594) | `cell/r6_c7_params.json`; Chen2020 dump |
| Cooling design | Liquid cold plate, both pouch faces: h = 25 W/m²K, A = 2 × 0.1027 = 0.2054 m² | `cell/r6_c7_params.json` |

## 2. Electrode and Separator

| Layer | Material | Thickness | Porosity | Active fraction | Particle radius (design) |
|---|---|---|---|---|---|
| Positive | NMC811 | 75.6 µm | 0.335 | 0.665 | 1.2 µm (single-crystal) |
| Separator | PP | 12 µm | 0.47 | — | — |
| Negative | Graphite | 95 µm (base 85.2 µm) | 0.25 | 0.75 | 0.8 µm (fine graphite) |
| Positive CC | Al | 16 µm | — | — | — |
| Negative CC | Cu | 12 µm | — | — | — |

N/P ratio (capacity basis) = (neg capacity density × thickness) ÷ (pos capacity density × thickness)
= (33133×0.75×96485/3600×95e-6) ÷ (63104×0.665×96485/3600×75.6e-6) = 63.280 ÷ 85.020 = **0.744**.
Source: Chen2020 dump (`Maximum concentration`, active fractions) + override thickness. Note: this baseline parameterization is anode-limited (capacity N/P < 1); the measured 1C capacity (5.654 Ah) tracks the anode inventory — verified in R4 (capacity grew linearly with anode thickness).

## 3. Process Design Parameters

| Parameter | Formula | Value | Unit |
|---|---|---|---|
| Positive areal density | thickness × (1−porosity) × density | 163.99 | g/m² |
| Negative areal density | thickness × (1−porosity) × density | 118.06 | g/m² |
| Positive compaction density | areal density ÷ thickness | 2.169 | g/cm³ |
| Negative compaction density | areal density ÷ thickness | 1.243 | g/cm³ |
| Electrolyte fill amount | pore volume × 1.2 g/cm³ (literature density) × fill factor 1.0 | 6.74 | g/cell |
| Formation recommendation | design value: 0.1C CC to 4.2 V, 25 °C, 2 cycles (production-line value requires tuning) | — | — |

Areal densities sourced from `cell/r6_c7_energy.json:layer_kg_m2` (contract caliber). Electrolyte density is a literature value (1.2 g/cm³), annotated as such.

## 4. Mass Breakdown

| Layer | kg/m² | g/cell | Source |
|---|---|---|---|
| Positive electrode | 0.163994 | 16.842 | `cell/r6_c7_energy.json:layer_kg_m2` × area |
| Negative electrode | 0.118061 | 12.125 | same |
| Positive CC (Al) | 0.043200 | 4.437 | same |
| Negative CC (Cu) | 0.107520 | 11.042 | same |
| Separator | 0.002525 | 0.259 | same |
| **Total (contract, electrolyte excluded)** | — | **44.705** | `cell/r6_c7_energy.json:mass_kg` |
| Electrolyte (estimate) | — | 6.743 | pore volume × 1.2 g/cm³ (literature) |
| **Total incl. electrolyte (estimate)** | — | **51.448** | mechanical sum |

## 5. Performance Verification (vs entry-0 criteria)

| Item | Result | Criterion | Verdict |
|---|---|---|---|
| Energy density | 457.93 Wh/kg | ≥ 392.61 Wh/kg | ✓ PASS (+65.3) |
| 4C charge @45 °C, max temperature | 318.79 K | ≤ 333.15 K (60 °C) | ✓ PASS (margin 14.4 K) |
| 4C charge lithium plating | anode potential min +0.00824 V (SPMe); +0.00515 V (DFN cross-check) | never < 0 V | ✓ PASS |
| Overcharge to 4.7 V thermal runaway | triggered = false, T_max 298.22 K | no thermal runaway | ✓ PASS |
| 1C discharge capacity | 5.654 Ah | (no task threshold — informational) | — |
| 4C CC charge acceptance | 4.63 Ah = 81.9 % SOC in ≈836 s at 20 A | (design-quality gate ~80 %) | ✓ met |

Sources: `cell/r6_c7_energy.json`, `cell/r6_c7_4c.json`, `cell/r6_c7_4c_dfn.json`, `cell/r6_c7_oc.json`, `validation/r6_c7_tr.json`.

## 6. Design Notes (what changed and why)

1. **Cooling**: parameter-set cooling area (0.00531 m²) is an edge-cooling artifact for a 0.1027 m² pouch; double-face cold-plate cooling (0.2054 m², h = 25 W/m²K) is the standard pack design. This solved T_max (354.3 → 318.8 K). (R2→C3)
2. **Electrolyte transport**: σ 1.8 S/m, D 5e-10 m²/s, t⁺ 0.5 (formulation-bridge estimates) cut charge-onset polarization. (R2→C2)
3. **Particle size balance**: cathode 1.2 µm single-crystal (τ_solid = R²/D = 360 s ≪ 900 s 4C window; commercial practice); anode 0.8 µm fine graphite — the anode kinetic cut was the decisive plating lever (+16 mV for 1.5→1.0 µm, +7 mV more for 1.0→0.8 µm). (R5→C7)
4. **Anode thickness 95 µm**: baseline is anode-limited (capacity N/P 0.744); thickening added capacity (+11.4 %) and energy without ED penalty (400.8 → 456–458 Wh/kg). (R4)
5. **Honest caveats**: plating margin is thin (+5 mV under DFN) — prototype 4C validation recommended before production; the 4C charge-side `capacity_ah` in runner outputs under-reports by the nominal-capacity factor (×5 for Chen2020) — true charge capacity derived mechanically (0.92596 × 5 = 4.63 Ah) and noted per round.
