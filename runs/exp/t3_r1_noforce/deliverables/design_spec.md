# Cell Design Specification — Power-Tool Battery Cell (final design V8)

**Document no.: VBF-T3R1NOFORCE-DS-01** · Case `exp/t3_r1_noforce` · 2026-08-25
Values are mechanically taken from the parameter set / simulation outputs and annotated line by line; missing items are written "Not provided".

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Chen2020 teaching parameterization, PyBaMM) | `--base Chen2020` |
| Rated capacity (Ah) | 3.0 (design rating) / 2.6683 simulation-verified at 1C | bridge/params_v8.json `Nominal cell capacity [A.h]` / cell/r4_v8_1c_dfn.json `capacity_ah` |
| Voltage window (V) | 2.5 – 4.2 | base parameter set (lower/upper voltage cut-off) |
| Cell dimensions (mm) | electrodes 65 × 1580 unrolled; stack thickness 0.147 (50 pos + 60 neg + 9 sep + 16 Al + 12 Cu µm); shell: Not provided (no shell parameter) | base parameter set + params_v8.json + cell/r4_v8_energy.json `thickness_m` |
| Electrolyte formulation | baseline EC/EMC + LiPF6-class defaults; conductivity override σ = 1.4 S/m; t⁺ = 0.5 (advanced concentrated-electrolyte class, estimate — marked) | params_v8.json `Electrolyte conductivity [S.m-1]`, `Cation transference number` |
| Thermal management | Total heat transfer coefficient h = 45 W/m²K (ducted forced-air pack cooling; design value) | params_v8.json |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | AMVF | Particle radius (µm) | Density (kg/m³) | Current collector |
|---|---|---|---|---|---|---|
| Positive (NMC811) | 50 | 0.40 | 0.58 | 1.2 | 3262 | Al 16 µm (2700 kg/m³) |
| Negative (graphite) | 60 | 0.42 | 0.56 | 2.0 | 1657 | Cu 12 µm (8960 kg/m³) |
| Separator | 9 | 0.55 | — | — | 397 | — |

**N/P ratio** (negative electrode capacity density × thickness ÷ positive electrode capacity density × thickness, capacity density = c_max × F/3600 × AMVF on electrode-volume basis):
N/P = (33133 × 0.56 × 60e-6) / (63104 × 0.58 × 50e-6) = **0.61** (full-lithiation caliber; c_max from base parameter set, thicknesses/AMVF from params_v8.json).
Design note: the cell is deliberately **anode-capacity-limited** — the 1C capacity scales with the negative AMVF (V6 2.9907 Ah × 0.56/0.63 = 2.658 vs V8 measured 2.6683 Ah), and the charged-state anode stoichiometry (29866/33133 = 0.9014 from the base-set initial concentration) leaves the anode below saturation at the 4C charge end, which is what yields the plating margin (see §5). The positive electrode cycles only in its low-stoichiometry region, so its excess full-lithiation capacity is inactive.

## 3. Process design parameters

| Parameter | Value | Formula / note |
|---|---|---|
| Areal density, positive (g/m²) | 97.9 | thickness × (1 − porosity) × density = 50e-6 × 0.60 × 3262 |
| Areal density, negative (g/m²) | 57.7 | 60e-6 × 0.58 × 1657 |
| Compaction density, positive (g/cm³) | 1.96 | 3262 × 0.60 / 1000 |
| Compaction density, negative (g/cm³) | 0.96 | 1657 × 0.58 / 1000 |
| Electrolyte fill amount (g) | 6.18 | pore volume 5.15e-6 m³ × 1.2 g/cm³ (literature value, annotated) × fill factor 1.0 |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; production-line value requires tuning |

## 4. Mass breakdown (g/cell)

| Component | Mass (g) | Formula / source |
|---|---|---|
| Positive active material (NMC811) | 9.715 | 50e-6 × 0.1027 × 0.58 × 3262 |
| Positive binder (PVDF, 1.5 vol%) | 0.137 | 50e-6 × 0.1027 × 0.015 × 1780 (PVDF density = literature default, no parameter in set) |
| Positive conductive additive (carbon black, 0.5 vol%) | 0.057 | 50e-6 × 0.1027 × 0.005 × 2200 (literature default) |
| Negative active material (graphite) | 5.717 | 60e-6 × 0.1027 × 0.56 × 1657 |
| Negative binder (SBR/CMC, 2 vol%) | 0.160 | 60e-6 × 0.1027 × 0.02 × 1300 (literature default) |
| Separator | 0.165 | 9e-6 × 0.1027 × (1 − 0.55) × 397 |
| Positive current collector (Al) | 4.437 | 16e-6 × 0.1027 × 2700 |
| Negative current collector (Cu) | 11.042 | 12e-6 × 0.1027 × 8960 |
| Electrolyte | 6.180 | pore volume × 1.2 g/cm³ (excluded from contract mass — parameter set lacks electrolyte density) |
| Enclosure, tabs | Not modeled | outside pure-simulation boundary |
| **Total (contract caliber)** | **31.616** | Σ layer thickness × area × (1 − porosity) × density, electrolyte excluded (cell/r4_v8_energy.json `mass_kg`) |
| Total incl. electrolyte | 37.796 | 31.616 + 6.180 |

BOM component sum (excl. electrolyte) 31.430 g vs contract 31.616 g: 0.6 % difference, binder/additive-density caliber (noted; no number altered).

## 5. Performance verification (vs entry-0 criteria, mechanical log-evaluate)

| Metric | Value | Threshold | Verdict | Source |
|---|---|---|---|---|
| Nominal capacity (Ah) | 2.6683 | ≥ 2.0 | PASS | cell/r4_v8_1c_dfn.json:capacity_ah |
| 5C discharge retention | 0.9842 | ≥ 0.95 | PASS | cell/r4_v8_5c_dfn.json ÷ cell/r4_v8_1c_dfn.json (cell/r4_v8_derived.json) |
| Power density (W/kg) | 73121.8 | ≥ 4000 | PASS | cell/r4_v8_energy.json:power_density_w_kg |
| T_max 5C discharge (K) | 308.45 | ≤ 333.15 | PASS | cell/r4_v8_5c_dfn.json:T_max_K |
| T_max 4C charge @45 °C (K) | 323.57 | ≤ 333.15 | PASS | cell/r4_v8_4c45_dfn.json:T_max_K |
| Plating on 4C charge | false (anode potential min +0.0119 V) | false | PASS | cell/r4_v8_4c45_dfn.json:anode_potential_v |
| Rated energy (Wh) | 9.833 | — | info | cell/r4_v8_energy.json:energy_wh |
| Energy density | 311.0 Wh/kg / 651.3 Wh/L | — | info | cell/r4_v8_energy.json |

## 6. Design notes (what changed vs baseline Chen2020 and why)

- Particle radii: positive 5.22 → 1.2 µm (solid-diffusion time τ_D = r²/D drops 6812 → 360 s — the root cause of the 8.7 % baseline 5C retention, fixed in round 2 and retained); negative 5.86 → 2.0 µm (interface surface for the 4C charge uniformity).
- Electrode thickness 75.6/85.2 → 50/60 µm; porosity 0.335/0.25 → 0.40/0.42; AMVF 0.665/0.75 → 0.58/0.56; separator 12 → 9 µm with porosity 0.47 → 0.55 — the rate/transport package that carries both the 5C retention and the plating margin (round 4, see log evaluate entries).
- Electrolyte σ 0.95 → 1.4 S/m, t⁺ 0.2594 → 0.5 — transport-class overrides (estimates, marked in propose entries).
- Cooling h 10 → 45 W/m²K — thermal-management freedom used to hold T_max ≤ 333.15 K.
- **Rated capacity 5.0 → 3.0 Ah**: the reference set's 5.0 Ah belongs to the 75.6/85.2 µm electrode cell; the designed cell is rated at its own capacity so that 5C/4C protocols test the cell's own C-rates (probe-verified: cell/probe_nominal_1c_dfn.json). Rounds 1–3 had tested the thinned designs at effective 6.7–8.6C.
- V8 vs alternatives: V7 (rated 3.6 Ah, 3.5321 Ah, retention 0.9775) is the higher-capacity alternative with a 10 mV plating margin; V8 was selected for the widest margins (retention 0.984, 4C thermal margin 9.6 K, plating margin 11.9 mV, 73.1 kW/kg).
