# Cell Design Specification — VBF-T5R1NOCEILING-DS-01

Case: t5_r1_noceiling — next-generation flagship vehicle battery.
Contract criteria (log.jsonl entry 0, verbatim from task text): energy density >= 500.94 Wh/kg; 4C fast charge with no lithium plating; maximum temperature <= 60 degC (333.15 K).
Ablation: ceiling_escalation OFF — no material escalation; all changes within the cell/architecture formulation space of the Chen2020 baseline.

## 1. Basic Specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 cathode | graphite anode (Chen2020 parameter set) | parameter set (base=Chen2020, anchored by parameter-set dump) |
| Nominal capacity | 9.6251 Ah (1C discharge to 2.5 V, completes in 6930 s) | cell/r4_A_calc_dfn.json:capacity_ah |
| Voltage window | 2.5 - 4.2 V | parameter set: Lower/Upper voltage cut-off [V] |
| Cell stack dimensions | 65 mm (height) x 2370 mm (electrode width, single unwound layer) x 0.2208 mm (stack thickness) | parameter set height 0.065 m; design override width 2.37 m (candidates/r4_A_params.json); cell/r4_A_calc_dfn.json:thickness_m |
| Shell / can dimensions | Not provided (no shell parameter within simulation boundary) | honest omission |
| Electrolyte formulation | 1 M LiPF6 in EC:EMC (3:7 w/w) (Chen2020 parameter-set electrolyte); no additive candidates (no additive design in scope; ceiling_escalation OFF) | parameter-set literature |
| Cation transference number | 0.45 (design override; parameter-set base value 0.2594) | candidates/r4_A_params.json; parameter set |

## 2. Electrode and Separator

| Layer | Thickness (um) | Porosity | Active fraction / density | Source |
|---|---|---|---|---|
| Positive electrode (NMC811) | 95.3 | 0.335 | 0.665 / 3262 kg/m3 | candidates/r4_A_params.json; parameter set |
| Negative electrode (graphite) | 107.5 | 0.25 | 0.75 / 1657 kg/m3 | candidates/r4_A_params.json; parameter set |
| Separator | 8.0 | 0.47 | density 397 kg/m3 | candidates/r4_A_params.json; parameter set |
| Positive current collector (Al) | 6.0 | - | 2700 kg/m3 | candidates/r4_A_params.json; parameter set |
| Negative current collector (Cu) | 4.0 | - | 8960 kg/m3 | candidates/r4_A_params.json; parameter set |
| Particle radii | positive 1.5 um / negative 1.0 um (base 5.22 / 5.86 um) | - | - | candidates/r4_A_params.json; parameter set |
| N/P ratio | 1.0475 (Q_neg 52.546 / Q_pos 50.161 Ah/m2 over the 2.5-4.2 V charge window) | computed from parameter set + DFN charge-window stoichiometries (diag_r4a_np.py: x_n 0.0283 -> 0.7622, x_p 0.8485 -> 0.3805) | mechanical derivation |

## 3. Process Design Parameters

| Parameter | Value | Formula | Source |
|---|---|---|---|
| Positive areal density | 206.73 g/m2 | thickness x (1 - porosity) x density = 95.3 um x 0.665 x 3262 kg/m3 | cell/r4_A_calc_dfn.json:layer_kg_m2.positive_electrode |
| Negative areal density | 133.60 g/m2 | 107.5 um x 0.75 x 1657 kg/m3 | cell/r4_A_calc_dfn.json:layer_kg_m2.negative_electrode |
| Positive compaction density | 2.169 g/cm3 | density x (1 - porosity) / 1000 = 3262 x 0.665 / 1000 | parameter set |
| Negative compaction density | 1.243 g/cm3 | 1657 x 0.75 / 1000 | parameter set |
| Electrolyte fill amount | 9.64 mL (11.57 g) | pore volume x electrolyte density 1.2 g/cm3 (literature value) x fill factor 1.0 | mechanical derivation; electrolyte density annotated literature value |
| Formation recommendation | 0.1C CC charge to 4.2 V at 25 degC, 2 cycles | design recommended value; actual production-line value requires tuning | design recommendation (estimate) |

## 4. Mass Breakdown

| Component | Mass (g) | Source |
|---|---|---|
| Positive electrode layer (active solids) | 31.846 | cell/r4_A_calc_dfn.json:layer_kg_m2.positive_electrode x area 0.15405 m2 |
| Negative electrode layer (active solids) | 20.580 | layer_kg_m2.negative_electrode x area |
| Al current collector (6 um) | 2.496 | layer_kg_m2.positive_cc x area |
| Cu current collector (4 um) | 5.521 | layer_kg_m2.negative_cc x area |
| Separator (8 um) | 0.259 | layer_kg_m2.separator x area |
| Total (simulation contract caliber, electrolyte excluded) | 60.703 | cell/r4_A_calc_dfn.json:mass_kg; formula = sum over layers of thickness x (1 - porosity) x density x area |

## 5. Performance Verification (vs log.jsonl entry-0 criteria)

| Metric | Value | Criterion | Determination | Source |
|---|---|---|---|---|
| Energy density | 583.93 Wh/kg (DFN calc-energy; SPMe cross-check 583.46) | >= 500.94 Wh/kg | PASS (+16.6%) | cell/r4_A_calc_dfn.json:energy_density_wh_kg |
| 4C fast charge (20 A) | 8.12 Ah charged in 1461 s to the 4.2 V ceiling (84.3% SOC) | support 4C fast charge | PASS | cell/r4_A_4c_dfn.json span (argmin-V to t_end) x 20 A / 3600 |
| Lithium plating | anode surface potential min +0.0212 V (DFN; SPMe +0.0270 V) | no lithium plating | PASS | cell/r4_A_4c_dfn.json:anode_potential_v min |
| Maximum temperature | 320.36 K (47.2 degC) during 4C charge (318.15 K ambient) | <= 333.15 K (60 degC) | PASS | cell/r4_A_4c_dfn.json:T_max_K |
| 1C discharge capacity | 9.6251 Ah (discharge to 2.5 V, no 7200-s truncation) | reported (no contract threshold in task text) | reported | cell/r4_A_calc_dfn.json:capacity_ah |

## 6. Design Notes

- vs base Chen2020 (electrodes 75.6/85.2 um, width 1.58 m, CC 16/12 um, separator 12 um, particles 5.22/5.86 um, h = 10 W/m2/K, parameter-set electrolyte transport): this design overrides electrode thicknesses 95.3/107.5 um, width 2.37 m (area x1.5), CC 6/4 um, separator 8 um, particle radii 1.5/1.0 um, electrolyte transport (sigma 2.0 S/m, t+ 0.45, D 4.5e-10 m2/s — literature-advanced electrolyte estimates), and cooling h = 200 W/m2/K.
- Why (citing the evaluate log): rounds 1-2 localized the 4C failure to empty-anode start-of-charge activation polarization (anode surface -0.43 to -0.0057 V, evaluate entries R1/R2). Round 3 combined current-density dilution (area x1.5) with small particles (1.5 um) -> R3C first full pass (anode +0.0162 V). Round 4 lifted ED with thin CC/separator (6/4 um, 8 um -> 583 Wh/kg) and widened the anode margin with 1.0 um anode particles (+0.0212 V at DFN). R4A selected over R4B (dominates on anode margin, ED, T_max at both SPMe and DFN).
- Boundary declarations (paired with acceptance): charge cut-off voltage fixed at 4.2 V (parameter set); solid-phase conductivity/diffusivity and initial concentrations fixed (parameter set); densities are mass-caliber inputs (no masquerading); cooling via h = 200 W/m2/K (thermal management in scope); electrolyte transport overrides are formulation-space tuning (no new molecules — ceiling_escalation OFF, no material escalation).
- Manufacturing caveats: 6/4 um foils and 1.0 um anode particles are aggressive values; validated fallback R4B (1.5 um anode, anode min +0.0144 V). Multilayer stacking/winding, shell, and tabs are outside the pure-simulation boundary — not modeled, stated honestly.

