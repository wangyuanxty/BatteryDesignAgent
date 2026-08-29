# Cell Design Specification — t8_r3 (VBF-T8R3-DS-01)

**Case**: t8_r3 — long-endurance drone battery (zero-interaction design run).  
**System base**: Chen2020 parameter set (NMC811 / graphite).  
**Generation date**: 2026-08-26 (virtual-design session; not a production release).

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (lithium-ion) | base_params=Chen2020 (case config) |
| Nominal capacity | 5.0 Ah (parameter set); simulated 1C DFN capacity 5.0728 Ah | Chen2020 Nominal cell capacity [A.h]; r4_V13_porousanode_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V | Chen2020 Lower/Upper voltage cut-off [V] |
| Cell dimensions | H 65 mm × W 1580 mm × stack 187.8 µm | Chen2020 Electrode height/width [m]; calc-energy thickness_m (layer sum, shell excluded) |
| Shell/casing thickness | Not provided (no parameter) | — |
| Electrolyte formulation | Chen2020 baseline + sigma=2.0 S/m (estimate), D=6e-10 m2/s (estimate) | params_r4_V13_porousanode.json (formulation estimates, marked estimate — not simulation output) |
| Cation transference number | 0.4 (override, estimate) | params_r4_V13_porousanode.json |
| Additive candidates | None (no Stage 2 material candidates; ceiling_escalation OFF ablation) | log.jsonl rounds 1–4 |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | Collector material / thickness | Source |
|---|---|---|---|---|
| Positive electrode | 75.6 | 0.335 | Al 10 µm | Chen2020 (thickness/porosity); override Al 10 µm (params file) |
| Negative electrode | 85.2 | 0.30 (override 0.25→0.30) | Cu 8 µm | Chen2020; overrides: negative porosity 0.30, Cu 8 µm |
| Separator | 9.0 | 0.47 | — | override separator 9 µm, porosity Chen2020 |
| Current collectors | Al 10 / Cu 8 | — | — | round-1 mass-fit overrides (8/10 µm grades) |

N/P ratio (DFN stoichiometric inference): **0.667** — full-swing ratio (vf_neg×c_max_neg×th_neg)/(vf_pos×c_max_pos×th_pos) = (0.75×33133.0×85.2 µm)/(0.665×63104.0×75.6 µm); F/3600 cancels. NOTE: full-swing (0–100% lithiation) ratio — the parameter set carries no direct capacity-density keys and Chen2020 operating windows differ from full swing; treat as approximate.

## 3. Process design parameters

| Parameter | Value | Formula | Notes |
|---|---|---|---|
| Positive areal density | 164.0 g/m² | thickness×(1−porosity)×electrode density | matches calc-energy layer_kg_m2 |
| Negative areal density | 98.8 g/m² | same | matches calc-energy layer_kg_m2 |
| Positive compaction density | 2.17 g/cm³ | electrode density×(1−porosity)/1000 | — |
| Negative compaction density | 1.16 g/cm³ | same | porosity override 0.30 applied |
| Electrolyte fill amount | 6.79 g | pore volume × 1200 kg/m³ × fill 1.0 | electrolyte density 1.2 g/cm³ literature value (parameter set lacks it) |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value | actual production-line value requires tuning |

## 4. Mass breakdown (contract caliber)

| Layer | Mass (g) | Basis | Source |
|---|---|---|---|
| Positive electrode (active layer) | 16.842 | 164.0 g/m² × 0.1027 m² | r4_V13_porousanode_energy.json:layer_kg_m2.positive_electrode |
| Negative electrode (active layer) | 10.149 | 98.8 g/m² × 0.1027 m² | energy:layer_kg_m2.negative_electrode |
| Positive current collector (Al) | 2.773 | 10 µm × 2700 kg/m³ | energy:layer_kg_m2.positive_cc |
| Negative current collector (Cu) | 7.362 | 8 µm × 8960 kg/m³ | energy:layer_kg_m2.negative_cc |
| Separator | 0.194 | 9.0 µm × 397 kg/m³ × (1−0.47) | energy:layer_kg_m2.separator |
| **Stack total** | **37.32** | Σ layers above | energy:mass_kg (electrolyte excluded — contract caliber) |
| Electrolyte (informational) | 6.79 | pore volume × 1.2 g/cm³ | not in calc-energy mass; listed for BOM only |

## 5. Performance verification (vs entry-0 criteria)

| Metric | Threshold (entry 0) | Result | Determination | Source |
|---|---|---|---|---|
| energy_density_wh_kg | ≥ 446.18 | 497.54 | ✓ pass | r4_V13_porousanode_energy.json:energy_density_wh_kg |
| retention_5c | ≥ 0.90 | 0.9866 | ✓ pass | derived: 5C capacity 5.00467 / 1C capacity 5.07280 |
| mass_kg | ≤ 0.04 | 0.03732 kg (37.32 g) | ✓ pass | energy:mass_kg |
| T_max_K (4C/45 °C charge) | ≤ 333.15 | 326.53 K | ✓ pass | r4_V13_porousanode_4c_safety.json:T_max_K |
| plated (4C/45 °C charge) | false | false (anode min +0.0177 V) | ✓ pass | 4c_safety:anode_potential_v min>0 (mechanical) |
| overcharge → thermal runaway | (informational) | triggered=False | ✓ not triggered | r4_V13_overcharge.json (T_max 299.33 K) → r4_V13_runtr.json:triggered |

## 6. Design notes (what changed and why)

- Round 1: thin Cu/Al/separator (8/10/9 µm) fix mass ≤ 40 g; particles remain 5.22/5.86 µm → 5C retention 9% (cathode surface saturation diagnosed at 96% of c_max at t≈62 s via direct DFN probe).
- Round 2: positive/negative particles 1.5/2.5 µm + high-transport electrolyte (σ 2.0 S/m, D 6e-10 m²/s, t⁺ 0.4, formulation estimates) → retention 98.0%; 4C/45 °C thermal still fails at h=10.
- Round 3: h=60 W/m²K forced-air cooling fixes T_max (327.3 K) but low-T anode kinetics plate (−10 mV) — negative particle 1.5 µm restores margin (V8 pass); thick-negative 100 µm route FAILS plating (V9/V11) — recorded negative result (anode thickness is a plating liability here).
- Round 4: negative porosity 0.30 (V13) chosen: ED 497.5 Wh/kg, retention 98.66%, T_max 326.53 K, anode min +17.7 mV — the widest safety margins of the campaign; cooling h≥60 W/m²K is part of the pack-level design.
