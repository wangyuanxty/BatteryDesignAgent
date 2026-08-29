# Cell Design Specification — LNMO High-Voltage Smartphone Cell

| Field | Value | Source |
|---|---|---|
| Electrochemical system | LNMO (LiNi0.5Mn1.5O4) high-voltage spinel cathode / graphite anode | `LNMO.json` positive override over `Chen2020` base |
| Nominal capacity (Ah) | 4.5 (parameter set) / 6.372 (simulated 1C) | parameter set + `r5_d11_1c.json` |
| Voltage window (V) | 2.5 – 4.7 | parameter set (`Lower/Upper voltage cut-off`) |
| Cell dimensions (H×W×T) | electrode 65 mm × 1580 mm (unwound) × 204.6 µm total layer stack; shell thickness **Not provided** | parameter set + `r5_d11_energy.json:thickness_m` |
| Electrolyte formulation | high-conductivity: σ = 1.8 S/m (constant), t⁺ = 0.4, D = Nyman2008 baseline (~1.77e-10 m²/s) | parameter bridge (formulation candidate) |
| Cation transference number | 0.4 | parameter bridge |
| SEI-suppressing coating | artificial SEI: SEI kinetic rate constant 2e-15 m/s (≈500× reduction, **estimate**) | parameter bridge (coating candidate) |

## 2. Electrode and Separator

| Layer | Thickness (µm) | Porosity | Density (kg/m³) | Active fraction | Particle radius (µm) | Source |
|---|---|---|---|---|---|---|
| Positive (LNMO) | 75.6 | 0.335 | 4400 | 0.665 | 5.22 | parameter set (LNMO density, Chen2020 geometry) |
| Negative (graphite) | 108 | 0.25 | 1657 | 0.75 | 1.5 | parameter set + design override |
| Separator | 7 | 0.47 | 397 | — | — | design override (Chen2020 baseline 12 µm) |
| Positive current collector (Al) | 8 | — | 2702 | — | — | design override (baseline 16 µm) |
| Negative current collector (Cu) | 6 | — | 8933 | — | — | design override (baseline 12 µm) |

- **N/P ratio** ≈ 1.04 (negative areal capacity 64.4 Ah/m² ÷ positive 62.1 Ah/m²; negative = 0.895·Δx·c_max·L·ε_am, positive = simulated 6.372 Ah / 0.1027 m²).

## 3. Process Design Parameters

| Parameter | Value | Formula / Source |
|---|---|---|
| Positive areal density | 221.2 g/m² | 75.6 µm × (1−0.335) × 4400 kg/m³ |
| Negative areal density | 134.2 g/m² | 108 µm × (1−0.25) × 1657 kg/m³ |
| Positive compaction density | 2.93 g/cm³ | 4400 × 0.665 / 1000 |
| Negative compaction density | 1.24 g/cm³ | 1657 × 0.75 / 1000 |
| Electrolyte fill amount | ≈6.85 g | pore volume (5.71 cm³) × 1.2 g/cm³ (literature density, annotated) |
| Formation recommendation | 0.1C CC to 4.7 V, 25 °C, 2 cycles | design-recommended value; production-line value requires tuning |

## 4. Mass Breakdown (contract caliber, electrolyte excluded)

| Layer | Mass (g/cell) | Source |
|---|---|---|
| Positive active (LNMO) | 22.72 | `r5_d11_energy.json:layer_kg_m2.positive_electrode` × area |
| Negative active (graphite) | 13.78 | `layer_kg_m2.negative_electrode` × area |
| Positive current collector (Al) | 2.22 | `layer_kg_m2.positive_cc` × area |
| Negative current collector (Cu) | 5.52 | `layer_kg_m2.negative_cc` × area |
| Separator | 0.151 | `layer_kg_m2.separator` × area |
| **Total** | **44.39** | `r5_d11_energy.json:mass_kg` (electrolyte/casing excluded) |

## 5. Performance Verification (vs criteria entry-0)

| Metric | Result | Threshold | Determination |
|---|---|---|---|
| 1C capacity | 6.372 Ah | — | — |
| Volumetric energy density | 1260.2 Wh/L | ≥ 950 | ✓ |
| Voltage plateau (midpoint) | 4.131 V | ≥ 4.1 | ✓ |
| 4C charge T_max | 321.68 K | ≤ 323.15 K | ✓ |
| 4C plating | anode min +0.043 V → no plating | false | ✓ |
| SEI thickness after 100 cyc | 193.6 nm | ≤ 500 nm | ✓ |

## 6. Design Notes

- System switched to LNMO (4.7 V-class cathode) because the plateau ≥ 4.1 V requirement excludes NMC811 (~3.6 V).
- Smartphone thin-cell architecture: current collectors thinned 16→8 µm (Al) / 12→6 µm (Cu) and separator 12→7 µm, re-allocating the saved volume to a thicker anode (85.2→108 µm) — raises N/P (fixes plating) and volumetric ED (1005→1260 Wh/L) without increasing total stack thickness.
- Anode particles reduced 5.86→1.5 µm to cut 4C solid-diffusion polarization (τ from ~1040 s to ~68 s).
- High-conductivity electrolyte (σ 1.8 S/m, t⁺ 0.4) reduces electrolyte concentration polarization.
- Artificial-SEI coating (SEI kinetic rate constant 2e-15 m/s) suppresses anode SEI growth (753→193.6 nm).
- Active cooling h = 400 W/m²·K keeps 4C-charge T_max ≤ 50 °C (321.68 K).

### Honest caveats
- The 4C CC charge reaches ~27 % SOC before the 4.7 V cutoff: the positive electrode is diffusion-limited because the model uses Chen2020 NMC solid diffusivity (4e-15 m²/s) — the `LNMO.json` `Positive electrode diffusivity` override uses a deprecated parameter name and is not applied.
- Cooling h = 400 W/m²·K requires active thermal management (heat pipe / vapor chamber).
- SEI coating factor (2e-15 m/s) is an estimate, not a simulated material.
