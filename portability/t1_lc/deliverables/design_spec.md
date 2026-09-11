# Cell Design Specification — VBF-T1LC-DS-01

Next-generation pure-electric sedan cell (virtual design). Base parameter set: Chen2020 (NMC811 / graphite). All values mechanically taken from parameter set / simulation outputs; per-line source annotations.

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Chen2020) | parameter set `--base Chen2020` |
| Nominal capacity | 5.0 Ah | parameter set `Nominal cell capacity [A.h]` |
| Verified 1C capacity | 5.030 Ah | cell/r3_V3_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V | parameter set lower/upper cut-off |
| Electrode sheet height | 65 mm (0.065 m) | parameter set `Electrode height [m]` |
| Electrode sheet width | 1580 mm (1.58 m) | parameter set `Electrode width [m]` |
| Total layer thickness | 200.8 µm | cell/r3_V3_energy.json:thickness_m (electrode+separator+collectors) |
| Cell shell thickness | Not provided | no shell parameter in set |
| Electrolyte formulation | EC/EMC + LiPF6 baseline; transport upgraded (σ=2.5 S/m, t⁺=0.6, D=4.0e-10 m²/s) | formulation estimate (cell/r3_V3_params.json) |
| Cation transference number | 0.6 | formulation estimate (baseline 0.2594) |
| Cooling | liquid cooling, h=60 W/m²/K | `Total heat transfer coefficient [W.m-2.K-1]` |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | Active vol. fraction | Density (kg/m³) | Source |
|---|---|---|---|---|---|
| Positive (NMC811) | 75.6 | 0.335 | 0.665 | 3262 | parameter set |
| Negative (graphite) | 85.2 | 0.25 | 0.75 | 1657 | parameter set |
| Separator (polyolefin) | 12.0 | 0.47 | — | 397 | parameter set |
| Positive current collector | 16.0 (Al) | — | — | 2700 | parameter set |
| Negative current collector | 12.0 (Cu) | — | — | 8960 | parameter set |

| Field | Value | Source |
|---|---|---|
| Positive particle radius | 5.22 µm | parameter set (unchanged) |
| Negative particle radius | 3.0 µm | cell/r3_V3_params.json (changed from 5.86 µm) |
| N/P ratio | 0.67 | (33133×0.75×85.2e-6)/(63104×0.665×75.6e-6); anode-limited (consistent with plating sensitivity) |

## 3. Process design parameters

| Parameter | Formula | Value | Source |
|---|---|---|---|
| Positive areal density | t×(1−ε)×ρ | 164.0 g/m² | 75.6e-6×0.665×3262 |
| Negative areal density | t×(1−ε)×ρ | 105.9 g/m² | 85.2e-6×0.75×1657 |
| Positive compaction density | ρ×(1−ε) | 2.169 g/cm³ | 3262×0.665/1000 |
| Negative compaction density | ρ×(1−ε) | 1.243 g/cm³ | 1657×0.75/1000 |
| Electrolyte fill amount | pore vol × 1.2 g/cm³ × 0.9 | 5.80 g | pore vol 5.37 cm³, literature density 1.2 g/cm³, fill factor 0.9 (estimate) |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | — | design recommended value; production-line value requires tuning |

## 4. Mass breakdown (contract caliber, electrolyte excluded)

| Layer | kg/m² | g/cell | Source |
|---|---|---|---|
| Positive electrode (active) | 0.16399 | 16.84 | cell/r3_V3_energy.json:layer_kg_m2 |
| Negative electrode (active) | 0.10588 | 10.87 | same |
| Positive current collector (Al) | 0.04320 | 4.44 | same |
| Negative current collector (Cu) | 0.10752 | 11.04 | same |
| Separator | 0.00252 | 0.26 | same |
| **Total (contract caliber)** | 0.42312 | **43.45 g** | cell/r3_V3_energy.json:mass_kg |

Note: electrolyte (~5.80 g) and casing/tabs are excluded from the contract-caliber mass (parameter set lacks their density); `electrolyte_included: false` in energy output.

## 5. Performance verification table

| Metric | Result | Criteria | Pass | Source |
|---|---|---|---|---|
| Energy density | 413.02 Wh/kg | ≥ 392.61 Wh/kg | ✓ | cell/r3_V3_energy.json:energy_density_wh_kg |
| 1C capacity | 5.030 Ah | nominal 5.0 Ah | ✓ | cell/r3_V3_1c_dfn.json:capacity_ah |
| 4C fast-charge T_max | 328.56 K (55.4 °C) | ≤ 333.15 K | ✓ | cell/r3_V3_4c_dfn.json:T_max_K |
| 4C fast-charge plating | anode_potential_v min +0.0368 V | no value < 0 V | ✓ | cell/r3_V3_4c_dfn.json:anode_potential_v |
| Overcharge 4.7 V thermal runaway | triggered = false | false | ✓ | cell/r3_V3_tr.json:triggered |

## 6. Design notes

- Baseline (Chen2020) already met ED (400.75 Wh/kg) and overcharge-no-TR; failed 4C (plating anode_min −0.19 V; T_max 354.3 K). Root cause localized to cell scale (Stage 3): anode solid-diffusion + electrolyte-transport polarization and limited cooling.
- Fix applied (mass-neutral, ED preserved): high-transport electrolyte (σ 0.95→2.5 S/m, t⁺ 0.26→0.6, D 1.77→4.0e-10 m²/s), negative particle radius 5.86→3.0 µm, liquid cooling h 10→60 W/m²/K.
- Electrolyte transport values are formulation estimates (not simulation-output), marked estimate in log.
- Smaller negative particle was confirmed beneficial (V3 +0.0368 V vs V2 8 µm −0.0228 V); larger particle direction rejected.
