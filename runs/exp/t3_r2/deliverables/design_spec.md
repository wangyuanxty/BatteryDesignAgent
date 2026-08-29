# Cell Design Specification — VBF-T3R2-DS-01

Case: `t3_r2` — Power-tool battery (nominal capacity >= 2 Ah; 5C discharge retention >= 95 %; 4C fast charge without lithium plating; T_max <= 60 °C; power density >= 4000 W/kg)
Base system: Chen2020 (NMC811 | graphite pouch). All values mechanically taken from parameter set / simulation outputs / literature; source annotated per line.

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 (positive) / graphite (negative), pouch, lumped-thermal model | Chen2020 parameter set (J. Electrochem. Soc. 167, 080534 (2020)) |
| Nominal capacity | 3.32 Ah (parameter), 3.328 Ah (1C DFN measured) | `cell/r2_p1_params_final.json`; `cell/r2_p1_1c_dfn.json:capacity_ah` |
| Voltage window | 2.5 – 4.2 V | parameter set `Lower/Upper voltage cut-off [V]` |
| Electrode area | 0.1027 m^2 (0.065 m × 1.58 m) | parameter set `Electrode height/width [m]` |
| Cell layer stack thickness | 141 um (pos 45 + sep 12 + neg 56 + Al 16 + Cu 12) | parameter set + design overrides; `cell/r2_p1_energy.json:thickness_m` |
| Shell / external dimensions | Not provided (no shell parameter in parameter set) | honest omission |
| Electrolyte formulation | 1 M Li+ (1000 mol/m3 electrolyte initial concentration); high-transport override: conductivity 1.5 S/m, diffusivity 6e-10 m2/s (constant, replaces Nyman2008 functions); solvent system not parameterized — Not provided | parameter set `Initial concentration in electrolyte [mol.m-3]`; design overrides (literature-informed estimate, see DS §6) |
| Cation transference number | 0.2594 | parameter set `Cation transference number` |
| Additive candidates | Not provided (no additive chemistry in this Stage-3 architecture workflow) | honest omission |

## 2. Electrode and separator

| Layer | Thickness (um) | Porosity | Active-material volume fraction (model) | Particle radius (um) | Current collector | Source |
|---|---|---|---|---|---|---|
| Positive | 45 | 0.45 | 0.665 | 1.3 | Al, 16 um | `cell/r2_p1_params_final.json` + parameter set |
| Separator | 12 | 0.47 | — | — | — | parameter set |
| Negative | 56 | 0.40 | 0.75 | 1.6 | Cu, 12 um | `cell/r2_p1_params_final.json` + parameter set |

N/P ratio:

| Quantity | Value | Source |
|---|---|---|
| Theoretical full-range N/P (deliverable formula: neg capacity density × thickness ÷ pos …) | 0.74 | mechanical: neg 33133 mol/m3 × 0.75 × 56 um ÷ (pos 63104 mol/m3 × 0.665 × 45 um) — parameter set + design thicknesses |
| Operating-point balance (1C discharge stoichiometry probe) | pos x 0.2700 -> 0.9102; neg y 0.9014 -> 0.0326; consumed areal capacity pos = neg = cell = 32.403 Ah/m2 (identity 1.0000 / 1.0000) | `_logs/p1_stoich_probe.json` (DFN re-solve of the delivered design) |
| Anode lithiation headroom at full charge | 9.86 % (y starts at 0.9014) | same probe |

## 3. Process design parameters

| Parameter | Value | Formula / notes | Source |
|---|---|---|---|
| Positive areal density | 80.73 g/m2 | thickness × (1 - porosity) × electrode density = 45 um × 0.55 × 3262 kg/m3 | parameter set + design |
| Negative areal density | 55.68 g/m2 | 56 um × 0.60 × 1657 kg/m3 | parameter set + design |
| Positive compaction density | 1.794 g/cm3 | 3262 × (1 - 0.45) / 1000 | parameter set + design (divide by 1000) |
| Negative compaction density | 0.994 g/cm3 | 1657 × (1 - 0.40) / 1000 | parameter set + design |
| Electrolyte fill amount | 5.95 g | pore volume (0.45×45 + 0.47×12 + 0.40×56) um × 0.1027 m2 = 4.96 cm3 × 1.2 g/cm3 (literature density) | literature value, annotated |
| Formation recommendation | 0.1C CC charge to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning | annotated recommendation |

## 4. Mass breakdown

| Component | Mass (g) | Mass (kg/kWh) | Source |
|---|---|---|---|
| Positive electrode layers (incl. binder/additive as one solids fraction) | 8.29 | 0.684 | `cell/r2_p1_energy.json:layer_kg_m2.positive_electrode` × area |
| Negative electrode layers | 5.72 | 0.472 | `layer_kg_m2.negative_electrode` |
| Positive current collector (Al) | 4.44 | 0.366 | `layer_kg_m2.positive_cc` |
| Negative current collector (Cu) | 11.04 | 0.911 | `layer_kg_m2.negative_cc` |
| Separator | 0.26 | 0.021 | `layer_kg_m2.separator` |
| Electrolyte (excluded from energy-density caliber) | 5.95 (informative) | 0.491 (informative) | pore volume × lit. density; `energy.json:electrolyte_included=false` |
| Enclosure, tabs | Not modeled | Not modeled | honest omission |
| **Total (bda contract caliber, electrolyte excluded)** | **29.75** | **2.453** | `cell/r2_p1_energy.json:mass_kg` |

## 5. Performance verification (criteria of entry 0 vs measured)

| # | Criterion (task text) | Threshold | Measured | Judgment | Source |
|---|---|---|---|---|---|
| 1 | Nominal capacity | >= 2 Ah | 3.328 Ah | PASS | `cell/r2_p1_1c_dfn.json:capacity_ah` |
| 2 | 5C discharge capacity retention | >= 95 % | 98.89 % (3.2911 / 3.3278 Ah) | PASS | `cell/r2_p1_derived.json:capacity_retention_5c` |
| 3 | 4C fast charge, no Li plating | plated == false | anode potential min +0.0364 V (>= 0) -> not plated | PASS | `cell/r2_p1_4c_dfn.json:anode_potential_v` |
| 4 | Maximum temperature | <= 60 °C (333.15 K) | 4C/45 °C charge T_max 332.52 K (59.37 °C); 5C/25 °C discharge T_max 322.22 K (49.07 °C) | PASS | `cell/r2_p1_4c_dfn.json:T_max_K`; `cell/r2_p1_derived.json:t_max_5c_k` |
| 5 | Power density | >= 4000 W/kg | 63,130 W/kg | PASS | `cell/r2_p1_energy.json:power_density_w_kg` |
| — | Rated energy / energy density (informative) | — | 12.13 Wh; 407.6 Wh/kg; 837.4 Wh/L | — | `cell/r2_p1_energy.json` |
| — | DCR (start-to-10% formula) | — | 2.265 mOhm | — | `cell/r2_p1_energy.json:dcr_ohm` |

## 6. Design notes (what changed in this case and why)

The Chen2020 base stack failed the power metrics at baseline (5C retention 8.7 %; 4C plated; 4C T_max 354.3 K — log round 1). Ceiling assessment localized the gap to transport kinetics at the cell scale (Stage 3): positive solid-diffusion time constant tau ~ r^2/D dominated, plus liquid transport. Round 2 power stack (this design) applied: particle radii 5.22/5.86 -> 1.3/1.6 um (tau ~ r^2), porosity 0.335/0.25 -> 0.45/0.40, electrode thickness 75.6/85.2 -> 45/56 um, electrolyte conductivity/diffusivity overridden to constants 1.5 S/m / 6e-10 m2/s (high-transport formulation, literature-informed estimate — log `propose_r2`). Attribution isolate (round 2, `P2_no_particles`, same levers minus particle radii) retained only 62.5 % 5C retention — particle size is the dominant 5C lever (~36 pp of the gap). Audited design rule: each candidate's `Nominal cell capacity [A.h]` is re-based to its delivered 1C capacity (converged to < 2 % drift, here 3.3219 Ah) so that 5C/4C protocols test true C-rates of the resized cell (log `plan_update_r1`). Model: DFN (no SPMe fallback) for all protocols — `model_used` in every run file.

Worth-noting boundary datums (honest reporting): alloy tab/spot-weld and external thermal management are pack-level DoF outside the cell simulation boundary; the 4C T_max margin is 0.63 K under the default cooling coefficient h = 10 W/m2K with 45 °C ambient — a production power-tool pack must confirm cooling at system level; low-temperature and cycle-life behavior were not part of the task contract (aging-capable set available in toolchain).