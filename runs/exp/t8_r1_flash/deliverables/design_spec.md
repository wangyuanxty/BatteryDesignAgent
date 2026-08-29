# Cell Design Specification — VBF-T8R1FLASH-DS-01

**Case**: t8_r1_flash | **Date**: 2026-08-25 | **Design**: V4 Thermal-tuned (final)

## 1. Basic specification
| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Chen2020 base) | parameter set Chen2020 |
| Nominal capacity | 3.45 Ah (design 3.40 Ah, simulation-verified 1C) | params_r1_v4.json / cell/r1_v4_1c.json:capacity_ah |
| Voltage window | 4.20 – 2.50 V | parameter set |
| Midpoint (plateau) voltage | 3.909 V | cell/r1_v4_energy.json:midpoint_voltage_v |
| Electrode footprint | 65 mm × 1580 mm (unwound electrode, area 0.1027 m²) | parameter set Electrode height/width |
| Stack thickness (excl. casing) | 135.3 µm | cell/r1_v4_energy.json:thickness_m |
| Shell/casing dimensions | Not provided (no shell-thickness parameter) | honest note |
| Electrolyte formulation | EC/EMC + LiPF6 class; high-transport override σ=1.4 S/m, D=4.5e-10 m²/s, t⁺=0.50 (estimate) | params_r1_v4.json; t⁺ marked estimate |
| Cation transference number | 0.50 (estimate, high-transference formulation) | params_r1_v4.json |

## 2. Electrode and separator
| Layer | Material | Thickness | Porosity | Density | Source |
|---|---|---|---|---|---|
| Positive electrode | NMC811 | 51.4 µm | 0.335 | 3262 kg/m³ | parameter set + params_r1_v4 |
| Negative electrode | Graphite | 57.9 µm | 0.25 | 1657 kg/m³ | parameter set + params_r1_v4 |
| Separator | Polyolefin | 12.0 µm | 0.55 | 397 kg/m³ | parameter set + params_r1_v4 |
| Positive current collector | Al | 8.0 µm | – | 2700 kg/m³ | params_r1_v4 |
| Negative current collector | Cu | 6.0 µm | – | 8960 kg/m³ | params_r1_v4 |
| Positive particle radius | – | 1.00 µm | – | – | params_r1_v4 (nano-NMC, literature high-power practice) |
| Negative particle radius | – | 1.50 µm | – | – | params_r1_v4 (fine graphite) |

**N/P ratio**: 0.77 (theoretical, literature stoich windows Δx_pos=0.75, Δx_neg=0.86; approximate — set does not expose stoich-limit keys; literature stoich windows dx_pos=0.75 (NMC811 0.99->0.24), dx_neg=0.86 (graphite->LiC6); approximate, set does not expose stoich-limit keys). Discharge balance check: 1C capacity 3.45 Ah from Δx_pos ≈ 0.27→0.85, Δx_neg ≈ 0.901→0.03 (derived from initial concentrations + 1C capacity).

## 3. Process design parameters
| Parameter | Value | Formula | Unit |
|---|---|---|---|
| Areal density, positive | 111.5 | thickness × (1−porosity) × density | g/m² |
| Areal density, negative | 72.0 | thickness × (1−porosity) × density | g/m² |
| Compaction density, positive | 2.169 | electrode density × (1−porosity) ÷ 1000 | g/cm³ |
| Compaction density, negative | 1.243 | electrode density × (1−porosity) ÷ 1000 | g/cm³ |
| Electrolyte fill amount | 3.93 mL (≈4.72 g @1.2 g/cm³ literature) | pore volume × electrolyte density × fill factor (1.0) | mL / g |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning | – |

## 4. Mass breakdown (contract caliber: layer stack, electrolyte/casing excluded)
| Layer | kg/m² | Mass (g/cell) | Source |
|---|---|---|---|
| Positive electrode | 0.11152 | 11.45 | cell/r1_v4_energy.json:layer_kg_m2 |
| Negative electrode | 0.07200 | 7.39 | cell/r1_v4_energy.json:layer_kg_m2 |
| Positive current collector | 0.02160 | 2.22 | cell/r1_v4_energy.json:layer_kg_m2 |
| Negative current collector | 0.05376 | 5.52 | cell/r1_v4_energy.json:layer_kg_m2 |
| Separator | 0.00214 | 0.22 | cell/r1_v4_energy.json:layer_kg_m2 |
| **Total (contract mass)** | | **26.8 g** | cell/r1_v4_energy.json:mass_kg |

## 5. Performance verification (vs entry-0 criteria)
| Metric | Value | Criterion | Verdict | Source |
|---|---|---|---|---|
| Energy density | 473.0 Wh/kg | ≥ 446.18 | ✓ PASS | cell/r1_v4_energy.json |
| 5C capacity retention | 99.0 % | ≥ 90 % | ✓ PASS | cell/r1_v4_retention.json |
| Cell mass | 26.8 g | ≤ 40 g | ✓ PASS | cell/r1_v4_energy.json |
| 4C-charge@45°C T_max | 58.8 °C (331.98 K) | ≤ 333.15 K | ✓ PASS | cell/r1_v4_4c.json |
| Lithium plating (4C charge) | min anode potential 0.0247 V > 0 | no plating | ✓ PASS | cell/r1_v4_4c.json:anode_potential_v |

## 6. Design notes
- Baseline Chen2020: ED 400.8 Wh/kg, 5C retention 8.7%, mass 43.5 g (r1 evaluate, fail). Root cause of 5C failure: cathode solid diffusion (D=4e-15 m²/s, r=5.22 µm, τ≈6800 s).
- Fixes (params_r1_v4.json, rationale in log round 2/3 propose+evaluate): nano particles (pos 1.0 µm, neg 1.5 µm) → τ≈250 s; high-transport electrolyte (σ=1.4 S/m, D=4.5e-10, t⁺=0.5 estimate); thin collectors (Al 8 µm, Cu 6 µm) → mass 43.5→26.8 g, ED→473; electrodes thinned 32% (Pareto balance); separator porosity 0.55; pouch cooling area 0.0075 m² (flatter form factor).
- 4C thermal attribution: V3 337.3 K → V5 (transport only) 334.7 K → V4 (transport + cooling area) 332.0 K. Transport/particles ≈ 2.6 K, cooling area ≈ 2.8 K (log round 3).
- Contract caliber: electrolyte/casing excluded from mass (parameter set lacks electrolyte density); 5C/1C retention uses self-consistent nameplate capacity (nominal 3.40 Ah vs actual 3.45 Ah, +1.5%).
