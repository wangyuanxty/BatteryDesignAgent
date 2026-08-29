# Cell Design Specification — VBF-T6R1-DS-01

| | |
|---|---|
| Case | t6_r1 — smartphone battery (ED ≥ 950 Wh/L, 4C no-plating, T_max ≤ 50 °C, SEI ≤ 500 nm @100 cyc, plateau ≥ 4.1 V) |
| Generation date | 2026-08-25 |
| Fidelity | DFN (highest available proxy; real_compute=false — no true DFT/MD endorsement) |

## 1. Basic Specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | LNMO high-voltage spinel cathode (4.7 V-class) / graphite anode; base parameter set `scripts/bda/simulators/data/LNMO.json` (Chen2020 + JSON overrides) | bridge/propose_r1.json; entry 0 |
| Nominal capacity (parameter set) | 4.5 Ah | parameter set `Nominal cell capacity [A.h]` |
| Simulation-verified capacity (1C, DFN) | 6.198 Ah | cell/r8_d6_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 V – 4.7 V | parameter set Lower/Upper voltage cut-off |
| Voltage plateau (discharge midpoint) | 4.1145 V | cell/r8_d6_energy_dfn.json:midpoint_voltage_v |
| Cell dimensions | 65 mm (H) × 1580 mm (W) × 217.8 µm (electrode stack thickness); pouch shell thickness: Not provided (not modeled) | parameter set Electrode height/width; cell/r8_d6_energy_dfn.json:thickness_m |
| Electrode area | 0.1027 m² | cell/r8_d6_energy_dfn.json:area_m2 |
| Electrolyte formulation | EC/EMC + LiPF6 baseline; EC initial concentration 2270.5 mol/m³; EC diffusivity 1.0e-18 m²/s (SEI-limiting, diffusion-limited regime); electrolyte diffusivity 6.0e-10 m²/s constant (low-viscosity fast-charge formulation — caveat: replaces concentration-dependent Nyman2008 function, upper bound of reported carbonate ranges) | bridge/params_final.json |
| Cation transference number | 0.2594 | parameter set (dump) |
| Cooling | h = 400 W/m²K (total heat transfer coefficient) | bridge/params_final.json |

## 2. Electrode and Separator

| Layer | Thickness (µm) | Porosity | Active-material volume fraction | Particle radius (µm) | Density (kg/m³) | Source |
|---|---|---|---|---|---|---|
| Positive electrode (LNMO) | 75.6 | 0.335 | 0.665 | 5.22 | 4400 | parameter set dump |
| Negative electrode (graphite) | 102.2 | 0.25 | 0.75 | 3.5 | 1657 | parameter set dump + params_final.json |
| Separator | 12 | 0.47 | — | — | — | parameter set dump |
| Positive current collector (Al) | 16 | — | — | — | 2700 (layer mass 0.0432 kg/m²) | parameter set dump; calc-energy |
| Negative current collector (Cu) | 12 | — | — | — | 8960 (layer mass 0.10752 kg/m²) | parameter set dump; calc-energy |

**N/P ratio = 0.80.** Formula (contract caliber): N/P = (c_max,neg × ε_am,neg × L_neg) ÷ (c_max,pos × ε_am,pos × L_pos) = (33133 × 0.75 × 102.2e-6) ÷ (63104 × 0.665 × 75.6e-6) = 0.8005.
*Honest labeling correction:* earlier rounds referred to the shipping anode thickness (102.2 µm) as "N/P 1.2" — that was a thickness-ratio shorthand vs the Chen2020 default negative thickness (85.2 µm), not a capacity-ratio N/P. The mechanical computation above supersedes it. *Parameter-set caveat:* LNMO.json carries positive capacity under key "Positive electrode maximum concentration [mol.m-3]", which is inert in PyBaMM 26.7 (current name: "Maximum concentration in positive electrode [mol.m-3]"), so the merged set uses Chen2020's positive c_max = 63104 mol/m³ — library data quirk, recorded.

## 3. Process Design Parameters

| Parameter | Value | Formula | Notes |
|---|---|---|---|
| Positive areal density | 221.2 g/m² | 75.6e-6 × 0.665 × 4400 × 1000 | coating solid-phase mass |
| Negative areal density | 127.0 g/m² | 102.2e-6 × 0.75 × 1657 × 1000 | coating solid-phase mass |
| Positive compaction density | 2.93 g/cm³ | 4400 × 0.665 ÷ 1000 | divide by 1000 |
| Negative compaction density | 1.24 g/cm³ | 1657 × 0.75 ÷ 1000 | divide by 1000 |
| Electrolyte fill amount | 6.27 g | pore volume 5.804 cm³ × 1.2 g/cm³ × 0.9 fill factor | electrolyte density = literature value 1.2 g/cm³ (annotated); pore volume = Σ(thickness × porosity × area) |
| Formation | 0.1C CC to 4.7 V, 25 °C, 2 cycles | — | design-recommended value; actual production-line value requires tuning (annotated) |

## 4. Mass Breakdown

Contract caliber (calc-energy): mass = Σ layer kg/m² × area; electrolyte excluded (parameter set lacks density).

| Component | kg/m² | Mass (g) | Source |
|---|---|---|---|
| Positive electrode coating | 0.221206 | 22.72 | cell/r8_d6_energy_dfn.json:layer_kg_m2 × area_m2 |
| Negative electrode coating | 0.127009 | 13.04 | same |
| Positive CC (Al) | 0.043200 | 4.44 | same |
| Negative CC (Cu) | 0.107520 | 11.04 | same |
| Separator | 0.002525 | 0.26 | same |
| **Total (electrolyte excluded)** | 0.501460 | **51.50** | cell/r8_d6_energy_dfn.json:mass_kg |
| Electrolyte (design estimate) | — | 6.27 | §3 fill amount, literature density |

## 5. Performance Verification (vs entry-0 criteria)

| Metric | Value | Criterion | Verdict | Source |
|---|---|---|---|---|
| Volumetric energy density | 1135.8 Wh/L | ≥ 950 Wh/L | ✓ (+19.6%) | cell/r8_d6_energy_dfn.json:energy_density_wh_l |
| Gravimetric energy density | 493.3 Wh/kg | informational | — | cell/r8_d6_energy_dfn.json:energy_density_wh_kg |
| Voltage plateau (midpoint) | 4.1145 V | ≥ 4.1 V | ✓ (+14.5 mV) | cell/r8_d6_energy_dfn.json:midpoint_voltage_v |
| 4C charge max temperature | 321.42 K (48.27 °C) | ≤ 323.15 K | ✓ (margin 1.73 K) | cell/r8_d6_4c_dfn.json:T_max_K |
| 4C charge plating | min anode potential +10.96 mV | plated = false | ✓ (margin 11.0 mV) | cell/r8_d6_4c_dfn.json:anode_potential_v min |
| SEI thickness after 100 cycles | 385.3 nm | ≤ 500 nm | ✓ (margin 114.7 nm) | cell/r8_d6_aging_dfn.json:sei_thickness_nm_end |

All five contract criteria PASS at DFN fidelity from one params file (bridge/params_final.json).

## 6. Design Notes (which parameters were changed and why)

| Change | Reason | Audit source |
|---|---|---|
| System switch: Chen2020 NMC811 → LNMO (4.7 V spinel) | Chen2020 midpoint 3.935 V < 4.1 V — material bottleneck proven by simulation | log R1 evaluate (systemLNMO) |
| Electrolyte: EC initial concentration 4541 → 2270.5 mol/m³; EC diffusivity 2e-18 → 1.0e-18 m²/s | SEI growth in EC-diffusion-limited regime (L ∝ sqrt(c₀·D_ec)); SEI 753 → 385 nm | log R4–R5 evaluate |
| Anode thickness 85.2 → 102.2 µm; negative particle radius → 3.5 µm | end-of-charge anode surface-saturation dip (plating) | log R3–R4 evaluate |
| Electrolyte diffusivity → 6.0e-10 m²/s constant (fast-charge formulation) | DFN through-plane depletion sag (midpoint 4.0974) and end-of-charge gradients (plating −19.3 mV); +14.5 mV midpoint / +30.3 mV anode margin | log R7–R8 evaluate |
| Cooling h 10 → 400 W/m²K | DFN heat load ~6 W pushed T_max to 323.80 K; h=400 → 321.42 K | log R2, R7 evaluate |
| Radius 3.0 µm probe dropped | counterintuitive: smaller particles worsened DFN midpoint by ~13 mV (depletion profile) | log R7 evaluate (nr30) |
