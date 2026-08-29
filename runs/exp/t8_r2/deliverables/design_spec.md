# Cell Design Specification - VBF-T8R2-DS-01

Case: t8_r2 (long-endurance drone battery). Base parameter set: Chen2020 (NMC811/graphite); final design V_G. Every value below is read from the parameter set or tool output files; source noted per line.

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 (positive) / graphite (negative), Chen2020 parameter set | parameter set |
| Nominal capacity (Ah) | 5.000  (simulated 1C DFN: 5.0351) | Nominal cell capacity [A.h]; cell/r3_VG_1c_dfn.json:capacity_ah |
| Voltage window (V) | 2.5 - 4.2 | Lower/Upper voltage cut-off [V] (parameter set) |
| Cell dimensions (mm) | height 65.0 x width 1990.8 x stack thickness 0.1506 (shell thickness: Not provided - no shell parameter in set) | Electrode height/width; cell/r3_VG_energy.json:thickness_m |
| Electrolyte transport | D = 4.20e-10 m2/s, t+ = 0.400, sigma = 1.20 S/m (parameter-bridge values); initial Li concentration 1000 mol/m3 | parameter set (V_G overrides); solvent/salt identity carried by Chen2020 set; no additive composed this case (Stage-2 funnel not run, real_compute=false) |
| Cation transference number | 0.400 | parameter set (V_G override) |

## 2. Electrode and separator

| Layer | Thickness (um) | Porosity | Current collector | Source |
|---|---|---|---|---|
| Positive electrode (NMC811 coating) | 60.0 | 0.335 | Al, 8.0 um (density 2700 kg/m3) | parameter set |
| Negative electrode (graphite coating) | 67.62 | 0.250 | Cu, 6.0 um (density 8960 kg/m3) | parameter set |
| Separator | 9.0 | 0.470 | - | parameter set |

N/P = (c_max_neg x eps_am_neg x th_neg) / (c_max_pos x eps_am_pos x th_pos) = 0.6674 (mechanical; c_max 33133 / 63104 mol/m3, eps_am 0.75 / 0.665, thickness 67.62 / 60.0 um per parameter set).

Positive particle radius 3.0 um; negative 3.5 um (V_G microstructure design lever). Solid-phase diffusivity left at parameter-set values (pos 4.0e-15 m2/s excluded from levers - recorded unchanged here for trace).

## 3. Process design parameters

| Parameter | Value | Formula | Source |
|---|---|---|---|
| Positive areal density (g/m2) | 130.15 | thickness x (1 - porosity) x electrode density x 1000 | cell/r3_VG_energy.json:layer_kg_m2.positive_electrode |
| Negative areal density (g/m2) | 84.03 | thickness x (1 - porosity) x electrode density x 1000 | cell/r3_VG_energy.json:layer_kg_m2.negative_electrode |
| Positive compaction density (g/cm3) | 2.1692 | electrode density x (1 - porosity) / 1000 | parameter set |
| Negative compaction density (g/cm3) | 1.2428 | electrode density x (1 - porosity) / 1000 | parameter set |
| Electrolyte fill amount (g) | 6.403 | pore volume x electrolyte density (1200 kg/m3 literature value, annotated) x fill factor 1.0 | mechanical derivation from parameter porosities |
| Formation recommendation | 0.1C CC to 4.2V, 25C, 2 cycles | design recommended value; actual production-line value requires tuning | design note |

## 4. Mass breakdown (contract caliber: layer mass = thickness x (1 - porosity) x density x area; electrolyte excluded - parameter set lacks density, per cell/r3_VG_energy.json note)

| Layer | Mass (g) | Source |
|---|---|---|
| Positive electrode coating | 16.842 | cell/r3_VG_energy.json:layer_kg_m2 x area_m2 |
| Negative electrode coating | 10.874 | cell/r3_VG_energy.json:layer_kg_m2 x area_m2 |
| Positive current collector (Al) | 2.795 | cell/r3_VG_energy.json:layer_kg_m2 x area_m2 |
| Negative current collector (Cu) | 6.957 | cell/r3_VG_energy.json:layer_kg_m2 x area_m2 |
| Separator | 0.245 | cell/r3_VG_energy.json:layer_kg_m2 x area_m2 |
| Total (contract caliber, no electrolyte) | 37.713 | cell/r3_VG_energy.json:mass_kg |
| Electrolyte (annotated, excluded) | 6.403 | pore volume x 1200 kg/m3 (literature default) |

## 5. Performance verification (vs criteria registered in log entry 0)

| Item | Result | Criterion | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity (Ah) | 5.0351 | none (informational; ED derives from it) | record | cell/r3_VG_1c_dfn.json:capacity_ah |
| Energy density (Wh/kg) | 483.4 | >= 446.18 | PASS | cell/r3_VG_energy.json:energy_density_wh_kg |
| 5C retention (5C/1C same params) | 0.9631 | >= 0.90 | PASS | cell/r3_VG_5c_dfn.json:capacity_ah / cell/r3_VG_1c_dfn.json:capacity_ah |
| Cell mass (g) | 37.71 | <= 40 | PASS | cell/r3_VG_energy.json:mass_kg |
| 4C-charge temperature (K) | 351.93 (rise 33.78 K vs 45 C ambient) | none (honest record; Stage-3 criteria carry no T threshold) | record | cell/r3_VG_safety.json:T_max_K |
| 4C-charge plating | anode min potential 0.0215 V > 0 -> plated = False | plated == false | PASS | cell/r3_VG_safety.json:anode_potential_v (min) |

## 6. Design notes

- Baseline (Chen2020 default, log round 1): ED 400.75 Wh/kg, retention_5c 0.0874, mass 43.45 g, 4C-charge plating (anode min -0.1918 V).
- R2 (transport): electrolyte D 4.0e-10 / t+ 0.36 / sigma 1.2 lifted retention 0.087 -> 0.676, resolving positive-side salt depletion (c_e 0 -> 355 mol/m3 at 5C); plateau 0.722 on electrode-thickness variants; V_D met ED 467.0 and mass 37.7 but not retention.
- R2 diagnosis (cell/_diag_vd.py): limiting process = positive solid-phase surface depletion (surface stoich 0.312 at separator face, tau_diff ~ 6812 s vs 720 s 5C time). Particle radius is the sanctioned microstructure lever.
- R3 (V_G selected): particle radii 5.22/5.86 -> 3.0/3.5 um, plus electrolyte margin t+ 0.36 -> 0.40 and D -> 4.2e-10 (plating buffer for the 4C-charge exam). Result: retention 0.9631 >= 0.90, ED 483.37 Wh/kg, mass 37.71 g, no plating.
- All four contract criteria pass mechanically (bda log-evaluate round 3, candidate V_VG). Margins: ED +37.19 Wh/kg, retention +0.0631, mass 2.29 g slack, plating margin +21.5 mV.
