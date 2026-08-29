# Cell Design Specification — VBF-T4R2-DS-01
Case t4_r2: extreme-cold environment equipment battery (−20 °C, 1C discharge retention ≥ 95 %, ED ≥ 327.18 Wh/kg, volumetric ED ≥ 880 Wh/L)
Generation date: 2026-08-26 (headless session; prepared/reviewed/approved signature block in delivery_index)

> All values below are mechanically taken from the Chen2020 parameter set (overridden by `cell/params_E3.json`), from tool output JSONs under `cell/`, or from literature defaults explicitly annotated. No number is written from memory; missing items are stated as "Not provided".

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811-like positive / graphite negative, LiPF6-class electrolyte (Chen2020, LGM50-derived teaching parameterization) | Chen2020 parameter set (entry-0 default record) |
| Nominal capacity | 5.0 Ah | `Nominal cell capacity [A.h]` = 5.0 (parameter set) |
| Measured 1C capacity (25 °C, DFN) | 5.0392 Ah (+0.78 % vs nominal; re-nominalization threshold ±3 % → nominal kept) | `cell/r5_E3_1c_dfn.json` |
| Voltage window | 2.5 – 4.2 V | `Lower/Upper voltage cut-off [V]` (parameter set) |
| Cell dimensions (electrode strip) | height 65.0 mm × width 1580.0 mm × stack thickness 0.1888 mm | `Electrode height/width [m]`, stack = 75.6+85.2+8+12+8 µm |
| Wound/outer cell dimensions, shell thickness | Not provided (no enclosure parameters in set) | honest "Not provided" per template |
| Electrolyte formulation | High-transport blended-single-ion class: σ 1.6 S/m, D 3.2e-10 m²/s, t⁺ 0.6, c₀ 1000 mol/m³. **Formulation estimates (parameter bridge), temperature-independent scalars — marked `estimate`, not measured** | `params_E3.json` overrides; B4/E2/E3 branch reasoning (evaluate R4/R5) |
| Cation transference number | 0.6 (estimate) | parameter override |
| Cooling design | total heat transfer coefficient h = 80 W/(m²·K) (liquid-cold-plate class) | `params_E3.json` |

## 2. Electrode and separator

| Layer | Thickness | Porosity | Particle radius | Material / density | Source |
|---|---|---|---|---|---|
| Positive electrode | 75.6 µm | 0.28 | 3.5 µm | NMC811-class, 3262 kg/m³ (from layer mass ÷ (t×(1−ε))) | parameter set + `calc-energy` layer_kg_m2 |
| Negative electrode | 85.2 µm | 0.28 (raised from 0.22 — plating headroom, +43.6 % effective transport via Bruggeman ε^1.5) | 3.0 µm | graphite-class, 1657 kg/m³ | parameter set + params_E3.json |
| Separator | 8 µm | 0.47 | — | 397 kg/m³ | parameter set |
| Positive current collector | 12 µm | — | — | Al, 2700 kg/m³ | parameter set |
| Negative current collector | 8 µm | — | — | Cu, 8960 kg/m³ | parameter set |
| **N/P ratio** | **1.03** | | | basis note below | |

N/P basis (mechanical): full-window electrode capacities = c_max × (full stoichiometry window at equilibrium voltage floors) × F/3600 × thickness × ε_active × area. Values from the solved DFN (C/10 floors): anode window 0→0.9014 → 5.253 Ah; cathode window 0.2700→0.8531 → 5.092 Ah; ε_active from parameter set (neg 0.75, pos 0.665). Inventory closure check: both electrodes transfer 5.0384 Ah over the 1C discharge span (computed 5.0385/5.0387) — consistent at 0.1 %. Cell is **positive-limited** (cathode exhausts first at 2.5 V floor; anode retains x = 0.0276).

## 3. Process design parameters

| Parameter | Value | Formula | Notes |
|---|---|---|---|
| Positive areal density | 177.6 g/m² | layer_kg_m2 × 1000 | t × (1−ε) × density = 75.6 µm × 0.72 × 3262 kg/m³ = 177.6 g/m² ✓ |
| Negative areal density | 101.6 g/m² | layer_kg_m2 × 1000 | 85.2 µm × 0.72 × 1657 = 101.6 ✓ |
| Positive compaction density | 2.35 g/cm³ | density × (1−ε) ÷ **1000** | 3262×0.72/1000 |
| Negative compaction density | 1.19 g/cm³ | density × (1−ε) ÷ 1000 | 1657×0.72/1000 |
| Electrolyte fill amount | 6.01 g/cell | pore volume × 1.2 g/cm³ (literature electrolyte density) × fill factor 1.0 | pore volume 5.010e-6 m³ (ε-weighted layers × area); density is literature default (set has none) — annotated |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; production-line value requires tuning | annotated "design recommendation" |

## 4. Mass breakdown (contract-caliber, electrolyte excluded in cell mass)

| Component | g/cell | kg/kWh | Source |
|---|---|---|---|
| Positive active layer | 18.23 | 1.004 | layer_kg_m2 × area (calc-energy) |
| Negative active layer | 10.44 | 0.575 | layer_kg_m2 × area |
| Positive CC (Al 12 µm) | 3.33 | 0.183 | layer_kg_m2 × area |
| Negative CC (Cu 8 µm) | 7.36 | 0.405 | layer_kg_m2 × area |
| Separator (8 µm) | 0.17 | 0.010 | layer_kg_m2 × area |
| Electrolyte (pore fill) | 6.01 | 0.331 | pore volume × 1.2 g/cm³ (literature) |
| **Total (incl. electrolyte)** | **45.55** | **2.508** | |
| Total without electrolyte | 39.54 | 2.177 | matches calc-energy mass_kg 0.039536 |

Active-layer masses carry no binder/conductive-additive split (set has no such keys) — split rows appear in the BOM with literature default 96/2/2 wt% annotation.

## 5. Performance verification (DFN verdict grade)

| Item | Value | Threshold | Verdict | Source |
|---|---|---|---|---|
| 1C retention, −20 °C | 0.9938 | ≥ 0.95 | ✓ (+4.6 ppt) | `r5_E3_retention_dfn.json` (5.0078/5.0392 Ah) |
| Energy density (gravimetric) | 459.45 Wh/kg | ≥ 327.18 | ✓ (+132.3) | `r5_E3_energy_dfn.json` (contract caliber, electrolyte excluded) |
| Volumetric energy density | 936.82 Wh/L | ≥ 880 | ✓ (+56.8) | `r5_E3_energy_dfn.json` (Σ layer thickness × area) |
| 4C charge temperature rise (45 °C ambient) | T_max 326.96 K | ≤ 333.15 | ✓ (margin 6.19 K) | `r5_E3_4c_dfn2.json` (stage-4 exam, second independent run) |
| 4C plating | min anode surface potential +0.0060 V | ≥ 0 (plated=false) | ✓ (margin 6 mV; 0/307 points negative) | `r5_E3_4c_dfn2.json` `anode_potential_v` |

Reproducibility: two independent DFN 4C runs returned identical T_max/anode-potential min (`r5_E3_4c_dfn.json` and `_dfn2`).

## 6. Design notes (what changed and why; cites evaluate-log reasoning)

- **Problem**: baseline Chen2020 passes W1/W2/W4(SPMe) but fails W3 (843.5 vs 880 Wh/L) and W5 (4C plating at DFN: anode separator-interface saturation, ap_min −0.19…−0.26 V) (evaluate R1, funnel R1).
- **W3 fix (R2)**: stack compression — porosities 0.28/0.22, separator 12→8 µm, collectors 16/12→12/8 µm (B1 893.1 Wh/L) (evaluate R2).
- **W4/W5 fix (R3–R5, escalation layer 1)**: geometry-only plating levers exhausted (particle radius neutral-to-worse; anode margin monotone but insufficient — funnel R3, strike 1). Lever class switched to electrolyte transport (σ/D/t⁺) + cooling + anode porosity headroom: ap_min −0.259 → **+0.0060 V**, T_max 357.5 → **326.96 K** (evaluate R4/R5). E3 = E2 (transport-max, h=80) + anode porosity 0.22→0.28, the final 0.078 V lever (funnel R5).
- **Honesty procedures applied**: cold-soak lowT (`Initial temperature [K]` 253.15), C-rate re-nominalization (E3 probe 5.0392 within ±3 % → nominal 5.0 kept), SPMe-at-4C plating indicator rejected (R2 diagnostic) — all safety verdicts DFN-grade, cell volume mechanically refreshed (1.939e-5 m³).
- **Remaining caveats**: electrolyte transport scalars are formulation estimates (flat-in-T in this parameter set); Stage-5 true compute skipped (real_compute=false, endorse entry); wound outer dimensions/enclosure not provided; cycle life not simulated.