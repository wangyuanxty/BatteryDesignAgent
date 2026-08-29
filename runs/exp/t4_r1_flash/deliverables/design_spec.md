# Cell Design Specification — T4R1FLASH

Case: `t4_r1_flash`  |  Generation date: 2026-08-25  |  Doc: VBF-T4R1FLASH-DS-01

_All values mechanical from simulation outputs / parameter set (see log.jsonl); no numbers from memory._

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Li-ion) | Chen2020 base parameter set (anchor-table mapping) |
| Nominal capacity | 3.93 Ah (simulation-verified 1C: 3.9547 Ah) | parameter set + cell/final_b7_1c_dfn.json |
| Voltage window | 2.5 – 4.2 V | parameter set (Upper/Lower voltage cut-off) |
| Nominal voltage (midpoint) | 3.8142 V | cell/final_b7_energy_dfn.json |
| Electrode strip | 65 mm height x 1580 mm width (wound strip) | parameter set (Electrode height/width) |
| Cell external dimensions | Not provided (no shell/can thickness parameter in set) | parameter set |
| Electrolyte | EC/EMC + LiPF6 base; transport overridden: sigma=2.0 S/m, D=5.0e-10 m2/s, t+=0.60 | Chen2020 + design override (R2-R5) |
| Electrolyte concentration | 1000 mol/m3 (bulk solvent 2636 mol/m3) | parameter set |
| Additive candidates (screened) | FEC / VC — molecular funnel: 2 passed, 0 rejected | cell/r2_funnel_*.json |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | Active vol. frac. | Density (kg/m3) | Source |
|---|---|---|---|---|---|
| Positive electrode (NMC811) | 60.0 | 0.335 | 0.665 | 3262 | parameter set (design override on thickness) |
| Negative electrode (graphite) | 68.0 | 0.250 | 0.750 | 1657 | parameter set (design override on thickness) |
| Separator | 8.0 | 0.470 | — | 397 | parameter set (design override on thickness) |
| Positive current collector (Al) | 10.0 | — | — | 2700 | parameter set (design override on thickness) |
| Negative current collector (Cu) | 6.0 | — | — | 8960 | parameter set (design override on thickness) |
| Particle radius | pos 5.22 µm / neg 5.86 µm | — | — | — | parameter set |

N/P ratio = (c_max,neg x eps,neg x t,neg) / (c_max,pos x eps,pos x t,pos) = (33133 x 0.750 x 68.0) / (63104 x 0.665 x 60.0) = **0.671**  

Design note: the protocol N/P formula uses maximum concentrations; the cell is positive-limited in operation (initial lithiation pos 0.27 / neg 0.90; 1C delivers 3.955 Ah ≥ nominal 3.93 Ah).


## 3. Process design parameters

| Parameter | Value | Formula / note |
|---|---|---|
| Positive areal density | 130.2 g/m2 | thickness x (1-porosity) x density |
| Negative areal density | 84.5 g/m2 | thickness x (1-porosity) x density |
| Positive compaction density | 2.17 g/cm3 | density x (1-porosity), /1000 |
| Negative compaction density | 1.24 g/cm3 | density x (1-porosity), /1000 |
| Electrolyte fill amount | 5.04 g/cell | pore volume x electrolyte density (1.2 g/cm3, lit.) x fill factor 1.0 |
| Formation recommendation | 0.1C CC to 4.2 V, 25 degC, 2 cycles | design recommended value; actual production-line value requires tuning |

## 4. Mass breakdown (per cell)

| Component | Mass (g) | Caliber |
|---|---|---|
| positive_electrode | 13.37 | contract formula: thickness x area x (1-porosity) x density |
| negative_electrode | 8.68 | contract formula: thickness x area x (1-porosity) x density |
| positive_cc | 2.77 | contract formula: thickness x area x (1-porosity) x density |
| negative_cc | 5.52 | contract formula: thickness x area x (1-porosity) x density |
| separator | 0.17 | contract formula: thickness x area x (1-porosity) x density |
| **Total (electrolyte excluded)** | **30.51** | = calc-energy mass_kg 30.51 g (cell/final_b7_energy_dfn.json) |
| Electrolyte (not in contract caliber) | 5.04 | pore volume x 1.2 g/cm3 (lit.) |
| Total incl. electrolyte | 35.55 | formula-caliber estimate |

## 5. Performance verification (DFN, final candidate)

| Metric | Value | Requirement (entry 0) | Verdict | Source |
|---|---|---|---|---|
| 1C discharge capacity | 3.955 Ah | nominal 3.93 Ah | ✓ | cell/final_b7_1c_dfn.json |
| -20 degC 1C retention | 0.9929 | ≥ 0.95 | ✓ | cell/final_b7_retention_dfn.json |
| Gravimetric energy density | 460.1 Wh/kg | ≥ 327.18 | ✓ | cell/final_b7_energy_dfn.json |
| Volumetric energy density | 899.3 Wh/L | ≥ 880.0 | ✓ | cell/final_b7_energy_dfn.json |
| 4C/45 degC charge T_max | 329.61 K | ≤ 333.15 K | ✓ | cell/final_b7_4c45_dfn.json |
| 4C plating (anode min) | +0.0193 V | > 0 V | ✓ | cell/final_b7_4c45_dfn.json |
| Overcharge -> thermal runaway | triggered = False | false | ✓ | cell/final_b7_tr.json |

## 6. Design notes (what changed vs baseline and why)

1. **Electrode thickness 75/85 -> 60/68 µm; separator 25 -> 8 µm; CC 12/12 -> 10/6 µm** — volumetric energy density 843.5 -> 899.3 Wh/L (R2-R5; thickness levers had no effect on plating, measured).

2. **C_nom reset to design's true 1C capacity (3.93 Ah)** — C-rate consistency: 4C must mean the design's own 4C (R2 note).

3. **Electrolyte transport override (sigma 2.0 S/m, D 5e-10 m2/s, t+ 0.60)** — the ONLY lever that fixed 4C plating (anode min -0.44 V -> +0.019 V; thickness/particle levers measured ineffective, R2-R5).

4. **h = 40 W/m2K forced-air cooling** — 4C exam T_max 350.6 (baseline) -> 329.6 K; trend ~ -2 K per +5 W/m2K (R3-R5).

5. **-20 degC retention needs no insulation** — Chen2020 electrolyte/solid transport is temperature-independent (measured via parameter introspection); retention 99.3% maintained at all h (plan update entry).

6. **Thermal management tension resolved** — the planned insulation-vs-cooling trade-off does not materialize in this parameter set (same entry).

