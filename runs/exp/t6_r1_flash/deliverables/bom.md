# Bill of Materials — Smartphone Battery finN-2e19

**Document**: VBF-T6R1F-BOM-01 | **Case**: t6_r1_flash | **Date**: 2026-08-25 | **Source**: cell/r5_finN_dfn_1c_calc.json (layer_kg_m2), LNMO.json

## 1. Layer Stack (single cell, area 0.1027 m²)

| # | Layer | Material | Thickness (µm) | Porosity/loading | Density basis | kg/m² | Mass (g) |
|---|---|---|---|---|---|---|---|
| 1 | Positive current collector | Al foil | 8 | — | 2700 kg/m³ | 0.02160 | 2.22 |
| 2 | Positive electrode | LNMO spinel (LiNi₀.₅Mn₁.₅O₄) | 74 | ε_act 0.665 | 4120 kg/m³ (calc) | 0.22121 | 22.72 |
| 3 | Separator | PE/ceramic-coated | 8 | — | — | 0.00168 | 0.17 |
| 4 | Negative electrode | Graphite (dense-calendered) | 120 | ε_act **0.65** | 2260 kg/m³ (calc) | 0.14913 | 15.32 |
| 5 | Negative current collector | Cu foil | 6 | — | 8960 kg/m³ | 0.05376 | 5.52 |
| | **Stack total** | | **217.6** | | | **0.44739** | **45.95** |

Masses from calc-energy layer_kg_m2 × area. Electrolyte excluded from mass/volume (parameter set lacks density — contract caliber, `electrolyte_included: false`).

## 2. Electrolyte (formulation estimate)

| Component | Role | Parameter value |
|---|---|---|
| Base solvent | EC/EMC (3:7) + 1.2 M LiPF₆ (LNMO base) | — |
| High-transference additive | anion-immobilizing / single-ion-like additive | t⁺ = 0.9 |
| Conductivity enhancer | fluorinated solvent + conductive additive | σ = 20 S/m |
| Diffusivity | Li⁺ transport | D = 1e-9 m²/s |
| SEI modifier | LiF-rich SEI former (EC permeation block) | D_ec = 2e-19 m²/s |

Transport/SEI values are design estimates (log `props_source`: "estimate"); no electrolyte mass statement (parameter set lacks density).

## 3. Cell Totals (contract caliber, electrolyte/casing excluded)

| Quantity | Value |
|---|---|
| Capacity (1C) | 6.324 Ah |
| Energy | 26.18 Wh |
| Mass | 45.95 g |
| Volume (layer stack) | 22.35 cm³ |
| ED volumetric | 1171.7 Wh/L |
| ED gravimetric | 569.9 Wh/kg |
| Thickness (stack) | 217.6 µm |

## 4. Thermal Management BOM (per cell)

| Item | Specification | Effective h |
|---|---|---|
| Vapor chamber | 0.4 mm Cu, in-plane K > 5000 W/mK | — |
| Graphite spreader | 25 µm, in-plane K ~1500 W/mK | — |
| Aluminum frame contact | full-area, gap filler 1 W/mK | — |
| **Total effective** | | **300 W/m²K** (h=250 verified minimum for M5) |

## 5. Notes

- N/P ratio ≈ 1.15 (anode-to-cathode capacity incl. ε_act 0.65); chosen to keep the 4C charge real (~7 Ah) while minimizing the electrolyte-potential penalty that drives plating (see design_spec §4).
- All thickness/loading values are the `--params` file values of the final design (`_params_finN.json` + `EC diffusivity 2e-19`), simulation-verified.
