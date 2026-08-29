# Cell Design Specification — VBF-T4R1-DS-01

Case: t4_r1 — battery for extreme-cold environment equipment. Base parameter set: Chen2020 (PyBaMM). All values mechanically taken from the parameter set / simulation outputs; sources annotated per line.

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 positive / graphite negative | Chen2020 parameter set (entry-0 base) |
| Nominal capacity | 5.0 Ah | parameter set `Nominal cell capacity [A.h]` |
| Measured 1C capacity (25 °C) | 5.0368 Ah | cell/r6_t2_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V | parameter set `Lower/Upper voltage cut-off [V]` |
| Electrode dimensions (height × width) | 65 mm × 1580 mm (unwound flattened electrode) | parameter set `Electrode height/width [m]` |
| Stack thickness (pos+sep+neg+Al+Cu) | 188.8 µm | cell/r6_t2_energy.json:thickness_m |
| Cell envelope (shell) thickness | Not provided | no shell parameter in set (not modeled) |
| Electrolyte formulation | Design-target transport profile (LHCE-class): κ = 1.1 S/m, D_e = 3e-10 m²/s, weak c_e/T dependence; concrete salt/solvent composition **not determined** (molecular funnel skipped: start_stage=3) | parameter-bridge overrides (bridge/params_r6_t2.json); composition not provided |
| Cation transference number t⁺ | 0.6 | parameter override `Cation transference number` |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | Active-material volume fraction | Density (kg/m³) | Notes / source |
|---|---|---|---|---|---|
| Positive electrode (NMC811) | 75.6 | 0.335 | 0.665 | 3262 | Chen2020 parameter set |
| Separator (polyolefin) | 10.0 | 0.47 | — | — | Chen2020 default 12 µm → 10 µm (design override, round 2) |
| Negative electrode (graphite) | 85.2 | 0.25 | 0.75 | 1657 | Chen2020 parameter set |
| Positive current collector (Al) | 10.0 | — | — | 2700 | Chen2020 default 16 µm → 10 µm (design override, round 2) |
| Negative current collector (Cu) | 8.0 | — | — | 8960 | Chen2020 default 12 µm → 8 µm (design override, round 2) |

| Field | Value | Source / formula |
|---|---|---|
| Positive particle radius | 5.22 µm | parameter set `Positive particle radius [m]` |
| Negative particle radius | 2.5 µm | design override (baseline 5.86 µm → 2.5 µm, round 6; fine-fraction graphite) |
| N/P ratio (total capacity density basis) | 0.667 | formula: (ε_am,neg × c_max,neg × L_neg) / (ε_am,pos × c_max,pos × L_pos) = (0.75×33133×85.2) / (0.665×63104×75.6); parameter-set values |
| N/P operational balance | ≈ 1.0 | same 5.037 Ah window both electrodes: neg 90.1% → 3.7%, pos 27.0% → 84.7% (initial stoichiometries from parameter set; window from measured 1C capacity) |

## 3. Process design parameters

| Parameter | Value | Formula | Notes / source |
|---|---|---|---|
| Areal density, positive | 163.99 g/m² | L × (1−ε) × ρ = 75.6e-6 × 0.665 × 3262 | cell/r6_t2_energy.json:layer_kg_m2 |
| Areal density, negative | 105.88 g/m² | L × (1−ε) × ρ = 85.2e-6 × 0.75 × 1657 | cell/r6_t2_energy.json:layer_kg_m2 |
| Compaction density, positive | 2.169 g/cm³ | ρ × (1−ε) / 1000 | parameter-set ρ, ε |
| Compaction density, negative | 1.243 g/cm³ | ρ × (1−ε) / 1000 | parameter-set ρ, ε |
| Electrolyte fill amount | 6.325 g (5.271 mL) | pore volume × electrolyte density (1.2 g/cm³, literature default, annotated estimate) | pore volume = (L_pos·ε_pos + L_sep·ε_sep + L_neg·ε_neg) × area = 5.271 mL |
| Formation recommendation | 0.1C CC charge to 4.2 V, 25 °C, 2 cycles | — | design recommended value; actual production-line value requires tuning |

## 4. Mass breakdown (formula caliber: mass = thickness × (1−porosity) × density × area; electrolyte excluded from cell mass)

| Layer | Mass (g) | Source |
|---|---|---|
| Positive electrode coating | 16.842 | cell/r6_t2_energy.json:layer_kg_m2 × 0.1027 m² |
| Negative electrode coating | 10.874 | same |
| Al collector | 2.773 | same |
| Cu collector | 7.362 | same |
| Separator | 0.216 | same |
| **Total (electrolyte excluded)** | **38.067** | cell/r6_t2_energy.json:mass_kg |
| Electrolyte (fill, reference only) | 6.325 | pore volume × 1.2 g/cm³ (literature default) |

## 5. Performance verification (vs entry-0 criteria)

| Metric | Criterion | Measured | Determination | Source |
|---|---|---|---|---|
| Energy density | ≥ 327.18 Wh/kg | 471.55 Wh/kg | ✓ pass | cell/r6_t2_energy.json:energy_density_wh_kg |
| Volumetric energy density | ≥ 880 Wh/L | 925.77 Wh/L | ✓ pass | cell/r6_t2_energy.json:energy_density_wh_l |
| −20 °C 1C retention (cold-soak) | ≥ 0.95 | 0.99267 | ✓ pass | cell/r6_t2_retention.json:lowT_retention |
| 1C discharge T_max | — | 299.58 K | informational | cell/r6_t2_1c_dfn.json:T_max_K |
| 4C/45 °C charge T_max | ≤ 333.15 K | 327.70 K | ✓ pass | cell/r6_t2_4c45C_dfn.json:T_max_K |
| 4C/45 °C plating | plated = false | anode min +0.0205 V | ✓ pass | cell/r6_t2_4c45C_dfn.json:anode_potential_v |

## 6. Design notes (changes vs baseline and why — per evaluate log)

- Round 1 (baseline Chen2020): ED 400.75, VED 844.45 (fail), retention 0.9942 → binding metric is VED.
- Round 2: thin collectors 10/8 µm + separator 10 µm (V3): VED 898.14 ✓, ED 457.48 ✓, retention ✓; true-1C compliant (cap 4.948 Ah ≈ nominal).
- Round 3 (Stage-4 exam on V3): FAIL — T_max 355.55 K, anode min −0.1848 V (plated).
- Rounds 4–5 (anti-plating/thermal): particle radius ↓, t⁺ ↑, N/P ↑ (dropped — made plating worse), κ flat 1.1, h 30/60/80 — localized cause to electrolyte salt-depletion transport collapse at end of 4C charge (anode potential minimum at charge end; S4 vs S6 contrast isolates T-dependent D_e).
- Round 6 (final T2): completes LHCE transport profile (κ 1.1 flat, D_e 3e-10 flat, t⁺ 0.6, R_neg 2.5 µm) + immersion cooling h = 80 W/m²/K → all five criteria pass.
- Caveats (honesty notes, see final log entry): flat-transport profile is optimistic at −20 °C (real LHCE κ ≈ 0.3 S/m, estimate; retention margin 4.27 pt); h = 80 assumes active immersion cooling; 2.5 µm particle radius is fine-fraction graphite (domain experience).
