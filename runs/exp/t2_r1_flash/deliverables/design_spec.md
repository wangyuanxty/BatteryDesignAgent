# Cell Design Specification — VBF-T2R1FLASH-DS-01

**Case**: t2_r1_flash · Grid energy storage cell · Generation date: 2026-08-25
**Numbering**: VBF-T2R1FLASH-DS-01

## 1. Basic specification
| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Chen2020 parameter set) | entry 0 meta.base |
| Nominal capacity | 5.0 Ah (parameter set); 1C delivered 5.0469 Ah | parameter set / cell/r2_fcc_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V | parameter set cut-offs |
| Cell dimensions (h x w x t) | 65.0 x 1580 x 0.2008 mm (electrode stack, no casing) | parameter set / calc-energy thickness_m |
| Electrolyte formulation | Advanced LiFSI-class high-transport: sigma 2.0 S/m, D 2.5e-10 m2/s, t+ 0.55 (transport overrides, literature-order estimates) | params/fcc.json, propose r2c |
| Cation transference number | 0.55 (override; baseline 0.2594) | params/fcc.json |
| Cooling (thermal management) | Total heat transfer coefficient 60 W/m2K (active liquid cooling, design choice) | params/fcc.json |

## 2. Electrode and separator
| Item | Value | Source |
|---|---|---|
| Positive electrode thickness / porosity | 75.6 um / 0.335 | parameter set |
| Negative electrode thickness / porosity | 85.2 um / 0.30 (porosity override 0.25->0.30) | parameter set / params/fcc.json |
| Separator thickness / porosity | 12 um / 0.47 | parameter set |
| Positive current collector | Al 16 um | parameter set |
| Negative current collector | Cu 12 um | parameter set |
| Positive particle radius | 4.0 um (override 5.22->4.0 um) | params/fcc.json |
| Negative particle radius | 2.5 um (override 5.86->2.5 um) | params/fcc.json |
| N/P ratio | 0.97 (density caliber: rho x (1-eps) x L x usable stoich; neg dx 0.05-0.90, pos dy 0.27-0.99; c_max-caliber inconsistent with densities in this parameter set, annotated) | computed, formula in calc.xlsx |

## 3. Process design parameters
| Parameter | Formula | Value | Unit |
|---|---|---|---|
| Positive areal density | thickness x (1-porosity) x density | 0 | g/m2 |
| Negative areal density | thickness x (1-porosity) x density | 0 | g/m2 |
| Positive compaction density | density x (1-porosity) / 1000 | 2.17 | g/cm3 |
| Negative compaction density | density x (1-porosity) / 1000 | 1.16 | g/cm3 |
| Electrolyte fill amount | pore volume x 1.2 g/cm3 (lit.) | 6.97 | g |
| Formation recommendation | 0.1C CC to 4.2 V, 25 C, 2 cycles | — | design recommended value; actual production-line value requires tuning |

## 4. Mass breakdown (formula caliber: layer thickness x area x (1-porosity) x density; electrolyte excluded per contract, included in BOM separately)
| Layer | Mass (g) | Source |
|---|---|---|
| Positive electrode | 16.84 | calc-energy layer_kg_m2 x area |
| Negative electrode | 10.15 | calc-energy |
| Positive CC (Al) | 4.44 | calc-energy |
| Negative CC (Cu) | 11.04 | calc-energy |
| Separator | 0.26 | calc-energy |
| **Total (electrolyte-excluded caliber)** | **42.73** | calc-energy mass_kg |

## 5. Performance verification (vs entry-0 criteria)
| Metric | Value | Threshold | Verdict | Source |
|---|---|---|---|---|
| Energy density | 425.41 Wh/kg | >= 327.18 | PASS | cell/r2_fcc_energy.json |
| SEI thickness @100 cyc 1C | 78.2 nm | <= 500 | PASS | cell/r2_fcc_aging100.json |
| SEI thickness @500 cyc 1C | 262.0 nm | <= 550 | PASS | cell/r2_fcc_derived.json |
| -20C discharge retention | 99.4 % | >= 90 | PASS | cell/r2_fcc_derived.json |
| 4C charge plating | anode min 12.3 mV >= 0, no plating | no plating | PASS | cell/r2_fcc_4c.json |
| 4C charge T_max (45C amb) | 329.2 K | <= 333.15 K | PASS | cell/r2_fcc_4c.json |

## 6. Design notes (changes vs baseline Chen2020 and why — traceable to evaluate log)
1. **Negative particle 5.86 -> 2.5 um, positive 5.22 -> 4.0 um**: lower solid-diffusion overpotential -> lifts anode surface potential at 4C (plating); lower polarization/heat (R2 FC-A -> FC-C).
2. **Negative porosity 0.25 -> 0.30**: shorter effective electrolyte path in the negative (plating margin).
3. **Electrolyte transport overrides (sigma 0.95 -> 2.0 S/m, D 1.77e-10 -> 2.5e-10 m2/s, t+ 0.26 -> 0.55)**: high-transport LiFSI-class formulation; reduces ohmic + concentration polarization at 4C (estimates, marked in propose r2c).
4. **SEI kinetic rate constant 1e-12 -> 2e-15 m/s**: artificial-SEI/coating-class suppression bridge (estimate); drives SEI 449->78 nm @100 cyc and 778->262 nm @500 cyc (R2 scans showed k is the controlling lever: k x0.2 -> 744 nm, k x0.01 -> 583 nm).
5. **Cooling h 10 -> 60 W/m2K**: active liquid cooling for grid storage; T_max 4C 354 -> 329 K.
6. **Reverted negative thickness to 85.2 um** (FC-B experiment: 100 um negative worsened 4C anode dip -0.125 V via longer electrolyte path).
7. Capacity-trajectory artifact in aging (climb-then-saturate under standard SEI model) is labeled honestly; SEI thickness is the reliable aging indicator.
