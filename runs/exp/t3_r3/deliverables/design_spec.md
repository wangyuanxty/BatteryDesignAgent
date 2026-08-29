# Cell Design Specification - Power-Tool Battery (case t3_r3)

> VBF-T3R3-DS-01. All values are mechanically taken from the parameter set, simulation results, and literature, with per-line sources. Missing items are written "Not provided"; no numbers from memory.

## 1. Basic Specification

| Field | Value | Source |
|------|------|------|
| Electrochemical system | NMC811 (LiNi0.8Mn0.1Co0.1O2) / graphite | Chen2020 parameter set (Chen et al., J. Electrochem. Soc. 167 (2020) 080534); deterministic default mapping (task text names no system), recorded in funnel log entry |
| Nominal capacity | 5.0 Ah nominal (parameter set); 4.3176 Ah verified at 1C (DFN simulation) | r5_v12_1c_dfn.json:capacity_ah; criterion >= 2.0 Ah |
| Voltage window | 2.5-4.2 V | pybamm Chen2020 parameter set |
| Cell dimensions | height 65.0 mm x width 1.580 m unwound strip (wound geometry) x layer stack 153.82 um; shell dimensions Not provided (no shell parameter) | pybamm Chen2020 + params |
| Electrolyte | EC/EMC + LiPF6 base (c_e0 = 1000 mol/m3); design-lever overrides: kappa = 1.5 S/m, t+ = 0.35, D = 8.0e-10 m2/s; additive candidates: none exercised (no Stage-2 escalation; architecture space judged sufficient - funnel log) | pybamm Chen2020 (base), r5_v12_hip_final_params.json (overrides) |
| Cation transference number | 0.35 | r5_v12_hip_final_params.json |

## 2. Electrode and Separator

| Layer | Thickness (um) | Porosity | Particle radius (um) | Other | Source |
|------|------|------|------|------|------|
| Positive electrode (NMC811) | 51.391 | 0.55 | 0.80 | density 3262 kg/m3 | r5_v12_hip_final_params.json / pybamm Chen2020 |
| Negative electrode (graphite) | 76.424 | 0.50 | 1.00 | density 1657 kg/m3 | r5_v12_hip_final_params.json / pybamm Chen2020 |
| Separator | 12.0 | 0.50 | - | density 397 kg/m3 | params override / pybamm Chen2020 |
| Positive current collector (Al) | 8 | - | - | density 2700 kg/m3 | r5_v12_hip_final_params.json |
| Negative current collector (Cu) | 6 | - | - | density 8960 kg/m3 | r5_v12_hip_final_params.json |

N/P ratio: 0.8393 loading ratio (negative/positive areal density) divided by the baseline loading ratio 0.6456 = **x1.30 in capacity terms** - a +30% negative capacity margin against the Chen2020 baseline stoichiometric parity (mechanical derivation from r5_v12_energy.json:layer_kg_m2 and r1_base_energy.json:layer_kg_m2; per-electrode specific capacities are not separately exposed by the parameter set).

## 3. Process Design Parameters

| Parameter | Formula | Value | Source |
|------|------|------|------|
| Positive areal density | thickness x (1 - porosity) x density | 75.44 g/m2 | mechanical from params |
| Negative areal density | thickness x (1 - porosity) x density | 63.32 g/m2 | mechanical from params |
| Positive compaction density | density x (1 - porosity) | 1.468 g/cm3 (kg/m3 divided by 1000) | mechanical from params |
| Negative compaction density | density x (1 - porosity) | 0.829 g/cm3 (kg/m3 divided by 1000) | mechanical from params |
| Electrolyte fill amount | pore volume x electrolyte density x fill factor | 8.932 g | pore volume from porosity params x 1.2 g/cm3 (literature value, annotated; fill factor 1) |
| Formation recommendation | e.g. 0.1C CC to 4.2 V, 25 C, 2 cycles | design-recommended value | actual production-line value requires tuning |
| Thermal management | cooling via h coefficient | 25 W/m2/K | r5_v12_hip_final_params.json (design requirement on pack thermal system) |

## 4. Mass Breakdown

| Component | Mass (g) | Note |
|------|------|------|
| Positive coating (94% NMC811 / 3% CB / 3% PVDF, literature default split) | 7.747 | layer_kg_m2 x area_m2 |
| Negative coating (94% graphite / 1% CB / 3% CMC+SBR, literature default split) | 6.503 | layer_kg_m2 x area_m2 |
| Separator | 0.245 | layer_kg_m2 x area_m2 |
| Positive current collector (Al) | 2.218 | layer_kg_m2 x area_m2 |
| Negative current collector (Cu) | 5.521 | layer_kg_m2 x area_m2 |
| Electrolyte (fill) | 8.932 | pore volume x 1.2 g/cm3 (lit.) |
| **Total stack mass** (calc-energy contract caliber, electrolyte excluded) | **22.234** | r5_v12_energy.json:mass_kg |
| Total including electrolyte | 31.166 | mechanical sum |

The calc-energy contract formula excludes electrolyte from mass and volume (parameter set lacks electrolyte density); the electrolyte row is provided for completeness.

## 5. Performance Verification (vs entry-0 criteria)

| Metric | Simulated value | Criterion | Determination | Source |
|------|------|------|------|------|
| Nominal capacity | 4.3176 Ah at 1C | >= 2.0 Ah | PASS | r5_v12_1c_dfn.json:capacity_ah |
| 5C discharge retention | 98.62% (5C capacity 4.2581 Ah / 1C capacity) | >= 95% | PASS | r5_v12_derived.json:retention_5c |
| 4C fast-charge max temperature | 329.75 K (56.60 C) | <= 333.15 K (60 C) | PASS | r5_v12_4c_dfn.json:T_max_K |
| 5C discharge max temperature | 319.57 K (46.42 C) | <= 333.15 K | PASS (informational) | r5_v12_5c_dfn.json:T_max_K |
| Lithium plating at 4C | anode potential min +41.7 mV | < 0 V -> plated | PASS (no plating) | r5_v12_4c_dfn.json:anode_potential_v |
| Power density | 181,557 W/kg | >= 4,000 W/kg | PASS (non-binding) | r5_v12_energy.json:power_density_w_kg |
| Energy density | 706.3 Wh/kg | not thresholded (information) | - | r5_v12_energy.json:energy_density_wh_kg |

## 6. Design Notes

Round-by-round changes with evaluate-log citations (all values DFN judge grade at round 5):

- **R1 baseline (evaluate_r1_Chen2020-baseline = fail)**: Chen2020 default thick-electrode energy cell is polarization-limited: 5C retention 8.7%, anode min -537 mV (plating), T_max 354 K, 4C CC acceptance 0.176 Ah.
- **R2 V1-V3 (evaluate_r2, all fail)**: porosity +0.05 and loading scale 0.55 -> retention reaches 95.0-98.2% but 4C T_max remains 340+ K; particle refinement 1.5 um alone insufficient.
- **R3 V4-V7 (evaluate_r3, all fail)**: N/P x1.3 (V4) gives clean no-plating margin (+36 mV); h=20 cooling (V5) clears 5C T_max (325.3 K); combos V6/V7 push 4C acceptance to 0.774 Ah but 4C T_max 334.2-334.5 K still over.
- **R4 V8-V11 (evaluate_r4)**: fine positive particles 0.8 um (V8, T_max 332.65 K - 0.5 K margin), fast D 8e-10 alone insufficient (V9, 333.76 K), h=25 alone passes (V10, 332.34 K); combo V11 champion at screening: T_max 329.87 K, retention 98.5%, anode +39.6 mV, acceptance 0.729 Ah.
- **R5 judge grade (evaluate_r5, both pass)**: V11 re-verified at DFN (329.85 K, +37.9 mV); V12-HiP-final combines the V7 high-porosity loading profile with V11 refinements: T_max 329.75 K, anode +41.7 mV, acceptance 0.811 Ah, capacity 4.318 Ah -> **champion**.

Honest residual: at 4C CC charge the 4.2 V ceiling is reached after 0.811 Ah (effective ~4.6C vs the 5.0 Ah nominal); the no-plating criterion is judged on anode-potential evidence, and charging beyond the window was not simulated.
