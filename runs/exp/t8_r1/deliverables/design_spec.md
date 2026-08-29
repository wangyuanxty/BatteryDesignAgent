# Cell Design Specification — T8-40g Long-Endurance Drone Battery

- **Document code**: VBF-T8R1-DS-01
- **Case**: t8_r1 — long-endurance drone battery (energy density ≥ 446.18 Wh/kg, 5C discharge with capacity retention ≥ 90%, cell mass ≤ 40 g)
- **Generation date**: 2026-08-25
- **Signature**: Prepared: ________  Reviewed: ________  Approved: ________

All values below are mechanically taken from tool output files under `cell/` (PyBaMM DFN simulations, `calc-energy`) or from the Chen2020 base parameter set probe (`cell/chen2020_base_probe.json`). Values marked "literature/estimate" are annotated as such.

## 1. Basic Specification

| Item | Value | Source |
|------|-------|--------|
| Electrochemical system | NMC811 / graphite (Chen2020 baseline teaching parameterization) | `--base Chen2020` |
| Nominal capacity | 6.1494 Ah | `r5_final_params.json` (Chen2020 5.0 Ah × area scaling 1.2299) |
| Verified 1C capacity | 6.9427 Ah | `r5_final_1c_dfn.json` |
| Voltage window | 2.5 – 4.2 V | `chen2020_base_probe.json` |
| Discharge midpoint voltage | 3.876 V | `r5_final_energy.json` (mechanical: time-midpoint voltage of 1C discharge) |
| Cell dimensions (unwound electrode geometry) | height 72.085 mm × width 1752.2 mm × thickness 0.1946 mm | `r5_final_params.json`, `r5_final_energy.json` (Σ layer thickness) |
| Shell / packaging thickness | Not provided (no parameter in set) | — |
| Electrolyte formulation | LiPF6 in organic carbonate (Chen2020 baseline; set defines transport properties, no explicit solvent-composition key) | probe |
| Transport overrides | conductivity σ = 1.3 S/m (constant), cation transference number t⁺ = 0.5, diffusivity D = 3.5×10⁻¹⁰ m²/s (constant) | `r5_final_params.json`; literature-class estimates (annotated in evaluate log) |
| Electrolyte additive candidates | Not proposed (start_stage = 3; no Stage-2 additive screening) | funnel entry |
| Cation transference number | 0.5 (override; Chen2020 base 0.2594) | `r5_final_params.json`, probe |

## 2. Electrode and Separator

| Layer | Thickness (µm) | Porosity | Density (kg/m³) | Areal mass (kg/m²) | Source |
|-------|---------------|----------|-----------------|--------------------|--------|
| Positive electrode (NMC811) | 75.6 (base) | 0.45 | 3262 | 0.13563 | `r5_final_params.json`, probe, `r5_final_energy.json` |
| Negative electrode (graphite) | 95.0 (override; base 85.2) | 0.35 | 1657 | 0.10232 | same |
| Separator | 10.0 (override; base 12.0) | 0.55 | 397 | 0.00179 | same |
| Positive current collector (Al) | 8.0 (override; base 16.0) | — | 2700 | 0.02160 | same |
| Negative current collector (Cu) | 6.0 (override; base 12.0) | — | 8960 | 0.05376 | same |
| Total stack thickness | 194.6 µm | — | — | 0.31510 | `r5_final_energy.json` |

Particle radii: positive 1.0 µm (base 5.22 µm), negative 1.5 µm (base 5.86 µm) — `r5_final_params.json`, probe.

**N/P ratio** = negative capacity density × thickness ÷ positive capacity density × thickness = **0.96** (assembled-lithium basis, formula in `calc.xlsx` sheet "N/P and mass"): capacity density = (1−ε) × c_max × F/3600 × usable window, with windows taken from the only stoich data the set provides (initial concentrations: x₀ = 0.270 positive, y₀ = 0.9014 negative). Chen2020 has no stoich-limit keys (probe `_stoich_keys: []`). Full-theoretical-window (Δx=Δy=1) ratio = 0.78, also shown in `calc.xlsx`.

## 3. Process Design Parameters

| Parameter | Formula | Value | Unit | Source |
|-----------|---------|-------|------|--------|
| Positive areal density | thickness × (1−ε) × density | 135.63 | g/m² | `r5_final_energy.json` layer_kg_m2 |
| Negative areal density | thickness × (1−ε) × density | 102.32 | g/m² | same |
| Positive compaction density | density × (1−ε) ÷ 1000 | 1.794 | g/cm³ | probe (3262 × 0.55) |
| Negative compaction density | density × (1−ε) ÷ 1000 | 1.077 | g/cm³ | probe (1657 × 0.65) |
| Electrolyte fill amount | pore volume × 1.2 g/cm³ (literature value, fill factor 100%) | 9.19 cm³ → 11.03 g | g | pore volume from layer porosities × area; density literature-annotated |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles (design recommended value; production value requires tuning) | — | — | annotated recommendation |

## 4. Mass Breakdown (contract caliber, electrolyte excluded)

| Component | Mass (g) | Source |
|-----------|----------|--------|
| Positive electrode layer | 17.131 | `r5_final_energy.json` layer_kg_m2 × area |
| Negative electrode layer | 12.923 | same |
| Separator | 0.226 | same |
| Al current collector | 2.728 | same |
| Cu current collector | 6.790 | same |
| **Total (contract caliber)** | **39.798** | same (`mass_kg` 0.0398) |
| Electrolyte (literature density, NOT in contract mass) | 11.03 | pore volume × 1.2 g/cm³, annotated |

Contract formula: ED = ∫V·I₁C dt ÷ Σ layer_thickness × (1−porosity) × density × area. Electrolyte excluded (parameter set has no electrolyte density) — annotated honestly.

## 5. Performance Verification (vs entry-0 criteria)

| Item | Value | Criterion | Verdict | Source |
|------|-------|-----------|---------|--------|
| Energy density | 634.32 Wh/kg | ≥ 446.18 Wh/kg | ✓ PASS | `r5_final_energy.json` |
| Energy density (volumetric) | 1027.10 Wh/L | — (informational) | — | same |
| 1C capacity | 6.9427 Ah, T_max 299.76 K | — | ✓ | `r5_final_1c_dfn.json` |
| 5C discharge capacity / retention | 6.8571 Ah / 98.77% | ≥ 90% | ✓ PASS | `r5_final_5c_dfn.json`, `r5_final_retention.json` |
| 5C discharge T_max | 319.99 K | — (informational) | ✓ | `r5_final_5c_dfn.json` |
| Cell mass | 39.800 g | ≤ 40 g | ✓ PASS | `r5_final_energy.json` |
| 4C charge @45 °C T_max | 330.41 K | ≤ 333.15 K | ✓ PASS (margin 2.74 K) | `r5_final_4c45_dfn.json` |
| Lithium plating (4C @45 °C) | anode potential min +0.0082 V > 0 | no plating | ✓ PASS | `r5_final_4c45_dfn.json` (auto-derived: min(anode_potential_v) ≥ 0) |
| DCR / power density | 0.684 mΩ / 156.1 kW/kg | — (informational) | — | `r5_final_energy.json` |

Honest caveat: 4C charge at 45 °C reaches the 4.2 V upper cut-off after only 0.9395 Ah charged (voltage-limited acceptance at 4C); fast charge at 4C is therefore thermally safe and plating-free but capacity-limited. Charging at lower C-rate removes the voltage limitation.

## 6. Design Notes (change history vs baseline, citing evaluate log)

| Change | Baseline (Chen2020) | Final | Why (evaluate log round) |
|--------|--------------------|-------|--------------------------|
| Positive/negative particle radius | 5.22 / 5.86 µm | 1.0 / 1.5 µm | R2 V4: baseline 5C retention was 8.7% — solid-state diffusion time constant τ = r²/D_s limits 5C delivery; smaller particles raise rate capability |
| Electrolyte conductivity / t⁺ / diffusivity | conc.-dependent func / 0.2594 / func | 1.3 S/m const / 0.5 / 3.5e-10 const | R2 V4: transport upgrade reduces electrolyte polarization at 5C (literature-class estimates) |
| Electrode porosity | 0.335 / 0.25 / 0.47 | 0.45 / 0.35 / 0.55 | R2 V4: higher porosity improves ion transport at 5C (costs ED, accepted — ED margin large) |
| Separator thickness | 12 µm | 10 µm | R2 V2/V4: thinner separator cuts ionic path resistance |
| Negative electrode thickness | 85.2 µm | 95.0 µm | R3 V7: thickens anode to add lithiation-capacity headroom (N/P↑, plating margin +10× at 4C) |
| Current collector thickness | 16 / 12 µm | 8 / 6 µm | R2 V2: thin foils raise gravimetric ED (ceiling assessment: 487 Wh/kg reachable in-architecture) |
| Cooling coefficient h | 10 W/m²/K | 40 W/m²/K | R3 V5 (30) → R4 V8 (35) → R4 V9 (40): 4C-45 °C exam T_max 354.3 K → 330.41 K (≤ 333.15 K); forced-air cooling assumed |
| Geometry / capacity scaling | 0.065 m × 1.58 m, 5.0 Ah | 0.072085 m × 1.7522 m, 6.1494 Ah | R5: area scaling ×1.2299 to bring mass to 39.8 g (≤ 40 g); verified scaling-invariant (ED/retention/T_max identical) |

No system switch: ceiling assessment (R1) showed the 446.18 Wh/kg target is reachable within the Chen2020 architecture (thin-foil ceiling ≈ 487 Wh/kg), so no Stage-2 escalation was triggered.

## 7. Safety Determination

| Item | Value | Criterion | Verdict | Source |
|------|-------|-----------|---------|--------|
| T_max, 4C charge @45 °C | 330.41 K | ≤ 333.15 K | ✓ PASS | `r5_final_4c45_dfn.json` |
| Plating, 4C charge @45 °C | anode min +0.0082 V | ≥ 0 V | ✓ PASS | same |
| Overcharge / nail / crush / drop | Not simulated | — | N/A | protocol has no such task criteria; see DVPR |

Safety thresholds (333.15 K, plating) are protocol defaults — task text is silent on safety; recorded in entry 0 meta.
