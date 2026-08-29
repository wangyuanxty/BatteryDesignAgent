# Cell Design Specification — Long-Endurance Drone Battery (t8_r1_noforce)

Document number: VBF-T8R1NOFORCE-DS-01 · Generation date: 2026-08-25 · Status: virtual design (simulation-based)

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 (positive) / graphite (negative) | Chen2020 parameter set (base selection per anchor table, task text names no system) |
| Nominal capacity | 5.0 Ah (parameter set) / 5.2725 Ah (simulated 1C discharge) | `cell/r6_v9_1c_dfn.json:capacity_ah` |
| Voltage window | 2.5 – 4.2 V | Chen2020 parameter set (`Lower/Upper voltage cut-off [V]`) |
| Cell dimensions (electrode) | 65 mm height × 1891 mm width × 0.1848 mm stack thickness | parameter set + `r6_v9_energy.json:thickness_m`, `area_m2` |
| Shell/casing thickness | Not provided (no parameter) | — |
| Electrolyte formulation | 1 M LiPF6 in EC:DMC 1:1; κ = 1.4 S/m, D = 3.7e-10 m²/s (literature, Nyman 2008 transport parameterization) | params `r6_v9_kin_el.json` (literature values, marked literature in R6 propose) |
| Cation transference number | 0.2594 | Chen2020 parameter set (baseline) |
| Cooling requirement | h = 60 W/m²/K forced-air (ducted prop-wash airflow at pack level) | params `r6_v9_kin_el.json` (thermal-management freedom) |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | AM volume fraction | Particle radius (µm) | Source |
|---|---|---|---|---|---|
| Positive (NMC811) | 75.6 | 0.40 | 0.60 | 0.7 (nano-NMC) | params + Chen2020 set |
| Negative (graphite) | 85.2 | 0.35 | 0.65 | 1.2 (fine graphite) | params + Chen2020 set |
| Separator | 10 | 0.47 | — | — | params + Chen2020 set |
| Positive current collector (Al) | 8 | — | — | — | params |
| Negative current collector (Cu) | 6 | — | — | — | params |

N/P ratio = (negative capacity density × thickness) ÷ (positive capacity density × thickness) =
(33133 × 0.65 × 85.2e-6) ÷ (63104 × 0.60 × 75.6e-6) = **0.641** (mechanical from parameter set; the cell is negative-limited — see design notes).

## 3. Process design parameters

| Parameter | Formula | Value | Source |
|---|---|---|---|
| Positive areal density | t × (1−ε) × ρ | 75.6e-6 × 0.60 × 3262 = **147.96 g/m²** | parameter set |
| Negative areal density | t × (1−ε) × ρ | 85.2e-6 × 0.65 × 1657 = **91.76 g/m²** | parameter set |
| Positive compaction density | ρ × (1−ε) | 3262 × 0.60 = 1957 kg/m³ = **1.96 g/cm³** | parameter set |
| Negative compaction density | ρ × (1−ε) | 1657 × 0.65 = 1077 kg/m³ = **1.08 g/cm³** | parameter set |
| Electrolyte fill amount | pore volume × density × fill factor | 7.960e-6 m³ × 1200 kg/m³ × 1.0 = **9.55 g** | pore volume mechanical from layers; density 1.2 g/cm³ literature value (annotated); fill factor 1.0 (design assumption) |
| Formation recommendation | — | 0.1C CC charge to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning |

## 4. Mass breakdown (contract caliber; electrolyte excluded per calc-energy)

| Layer | kg/m² | g/cell (area 0.122915 m²) | Source |
|---|---|---|---|
| Positive electrode (active) | 0.14796 | 18.19 | `r6_v9_energy.json:layer_kg_m2` × area |
| Negative electrode (active) | 0.09176 | 11.28 | same |
| Positive current collector (Al 8 µm) | 0.02160 | 2.65 | same |
| Negative current collector (Cu 6 µm) | 0.05376 | 6.61 | same |
| Separator (10 µm) | 0.00210 | 0.26 | same |
| **Total (contract)** | 0.31718 | **38.99 g** | `r6_v9_energy.json:mass_kg` ✓ ≤ 40 g |
| Electrolyte (excluded from contract mass) | — | 9.55 g (BOM row, literature density) | see process table |

Note: contract-caliber mass formula = Σ layer thickness × (1−porosity) × density × area; electrolyte excluded (`electrolyte_included: false` in calc-energy output — parameter set lacks electrolyte density).

## 5. Performance verification (vs entry-0 criteria)

| Metric | Result | Criterion (entry 0) | Determination | Source |
|---|---|---|---|---|
| Energy density | 497.97 Wh/kg | ≥ 446.18 Wh/kg | ✓ PASS | `r6_v9_energy.json:energy_density_wh_kg` |
| 5C capacity retention | 0.9896 | ≥ 0.90 | ✓ PASS | `r6_v9_retention.json:capacity_retention_5c` |
| Cell mass | 38.99 g | ≤ 40 g | ✓ PASS | `r6_v9_energy.json:mass_kg` |
| Lithium plating (4C charge, 45 °C) | anode min +0.00635 V | plated = false | ✓ PASS (thin margin +6.3 mV) | `r6_v9_4c_charge45_plating.json:anode_potential_v` |
| Max temperature (4C charge, 45 °C) | 326.81 K | ≤ 333.15 K | ✓ PASS | same file `T_max_K` |
| Max temperature (5C discharge) | 313.64 K | ≤ 333.15 K | ✓ PASS | `r6_v9_5c_dfn.json:T_max_K` |
| 1C discharge capacity | 5.2725 Ah | no entry-0 threshold (feeds ED) | informational | `r6_v9_1c_dfn.json:capacity_ah` |

## 6. Design notes (change log; reasoning cited from log.jsonl)

- R1 baseline (Chen2020 defaults): ED 400.75, 5C retention 0.087, mass 43.45 g → all three fail; diagnosis: solid-diffusion-limited at 5C (D_p = 4e-15 m²/s, τ ≈ 6800 s at r = 5.22 µm) + inert mass 0.153 kg/m² (Cu CC largest single inert item).
- R2 attribution: inert lean-out (V1) solves ED/mass but not rate; particles (V2) 0.2325; porosity (V3) 0.1998.
- R3: all rate levers combined (r_p 0.7 µm, r_n 2 µm, porosity 0.40/0.35, κ 1.1 / D 2.9e-10 electrolyte) → retention 0.9524, ED 493.6, mass 33.0 g — stage2 achieved.
- R4: sizing (width 1.891 m → 39.0 g) + thermal (5C T_max 369 K at h=10 → h=40) — stage2 pass, stage3 fail: plated (anode −0.030 V) and 4C-exam T_max 334.14 K.
- R5 (V8, thicker anode N/P 1.13): backfired — anode min −0.194 V (plating dip is charge-end electrolyte-transport polarization, not capacity shortage; longer anode path worsens it) and 5C solver failure IDA_CONV_FAIL recorded verbatim.
- R6 (final): anode kinetics (r_n 1.2 µm) + EC:DMC electrolyte (κ 1.4, D 3.7e-10) + h 60 → anode min +0.00635 V (no plating), 4C T_max 326.81 K, retention 0.9896, ED 497.97, mass 38.99 g — all five criteria pass (R6 evaluate, checked=5).
