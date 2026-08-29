# Cell Design Specification — VBF-T1R1-DS-01

Case: t1_r1 | Date: 2026-08-25 | Prepared: ____________ | Reviewed: ____________ | Approved: ____________

Objective (task text, verbatim thresholds): energy density ≥ 392.61 Wh/kg; 4C fast charge without lithium plating; maximum temperature ≤ 60 °C (333.15 K); overcharge to 4.7 V without thermal runaway.

## 1. Basic Specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (LiNi0.8Mn0.1Co0.1O2 cathode, graphite anode) | Chen2020 parameter set (task names no electrode system → default per anchor table; funnel log entry) |
| Nominal capacity | 5.0 Ah (parameter nominal); 5.6505 Ah simulated 1C | Chen2020 "Nominal cell capacity [A.h]"; cell/r3_I_1c.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V | Chen2020 "Lower voltage cut-off [V]" / "Upper voltage cut-off [V]" |
| Nominal (midpoint) voltage | 4.0067 V | cell/r3_I_energy.json:midpoint_voltage_v (calc-energy mechanical derivation) |
| Cell dimensions | Electrode sheet 65 mm × 1580 mm; stack thickness 214.6 µm; shell dimensions Not provided (no parameter) | Chen2020 "Electrode height [m]" 0.065, "Electrode width [m]" 1.58; cell/r3_I_energy.json:thickness_m |
| Electrolyte formulation | 1M LiPF6 EC/EMC class with design overrides: conductivity 1.8 S/m (constant; estimate simplification vs temperature-dependent Nyman2008), transference number 0.55 | Chen2020 electrolyte functions (defaults); design overrides params_r3_I.json "Electrolyte conductivity [S.m-1]" / "Cation transference number" (formulation DOF, estimate class per propose r2/r3) |
| Cation transference number | 0.55 (default 0.2594) | params_r3_I.json |
| Thermal management | Total heat transfer coefficient 100 W/m2K (liquid cold-plate class) | params_r3_I.json "Total heat transfer coefficient [W.m-2.K-1]" (default 10.0) |

## 2. Electrode and Separator

| Layer | Thickness (µm) | Porosity | Active material volume fraction | Density (kg/m3) | Particle radius (µm) | Current collector |
|---|---|---|---|---|---|---|
| Positive (NMC811) | 75.6 (default) | 0.335 (default) | 0.665 (default) | 3262 (default) | 5.22 (default) | Al 8 µm (default 16) |
| Negative (graphite) | 120 (default 85.2) | 0.40 (default 0.25) | 0.60 (default 0.75) | 1657 (default) | 2.5 (default 5.86) | Cu 5 µm (default 12) |
| Separator | 6 (default 12) | 0.47 (default) | — | 397 (default) | — | — |

All values: Chen2020 parameter dump (dump_params.py) for defaults; params_r3_I.json for overrides.

N/P ratio: formula caliber = (negative capacity density × thickness) ÷ (positive capacity density × thickness) = (33133 × 0.60 × 120 µm) / (63104 × 0.665 × 75.6 µm) = 0.752. Usable-window caliber ≈ 1.0 (anode operates over 0.860 of full theoretical capacity vs cathode 0.647 at the 2.5–4.2 V envelope: 1C discharge 5.6505 Ah vs full-theoretical anode 6.567 Ah / cathode 8.732 Ah, derived from c_max × AMVF × F × thickness × area). Plating safety is delivered by kinetics/transport (small particles, porous anode, high-conductivity high-t+ electrolyte) and verified by the DFN 4C exam (anode potential min +0.0249 V), not by N/P headroom — see Design Notes.

## 3. Process Design Parameters

| Parameter | Value | Formula | Source |
|---|---|---|---|
| Positive areal density | 163.994 g/m2 = 16.399 mg/cm2 | thickness × (1−porosity) × density = 75.6 µm × 0.665 × 3262 | Chen2020 + params_r3_I.json |
| Negative areal density | 119.304 g/m2 = 11.930 mg/cm2 | 120 µm × 0.60 × 1657 | params_r3_I.json + Chen2020 density |
| Positive compaction density | 2169.2 kg/m3 = 2.169 g/cm3 | density × (1−porosity) ÷ 1000 | Chen2020 3262 × 0.665 |
| Negative compaction density | 994.2 kg/m3 = 0.994 g/cm3 | density × (1−porosity) ÷ 1000 | Chen2020 1657 × 0.60 |
| Electrolyte fill amount | 9.384 g | pore volume × 1.2 g/cm3 × fill factor 1.0; pore volume = (75.6×0.335 + 120×0.40 + 6×0.47) µm × 0.1027 m2 = 7.820 cm3 | literature electrolyte density 1.2 g/cm3 (estimate, annotated); geometry from parameter set |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | — | design recommended value; actual production-line value requires tuning (annotated) |

## 4. Mass Breakdown (contract caliber: layer thickness × (1−porosity) × density × area; electrolyte excluded)

| Component | Mass (g) | Source |
|---|---|---|
| Positive electrode layer | 16.842 | calc-energy caliber: 75.6 µm × 0.665 × 3262 × 0.1027 m2 (matches r3_I_energy.json layer breakdown) |
| Negative electrode layer | 12.253 | 120 µm × 0.60 × 1657 × 0.1027 m2 |
| Positive current collector (Al) | 2.218 | 8 µm × 2700 × 0.1027 m2 |
| Negative current collector (Cu) | 4.601 | 5 µm × 8960 × 0.1027 m2 |
| Separator | 0.130 | 6 µm × (1−0.47) × 397 × 0.1027 m2 |
| Total | 36.044 | cell/r3_I_energy.json:mass_kg = 0.0360436 kg (verified: recomputation matches to 1e-12) |

With electrolyte fill (BOM caliber): +9.384 g → 45.43 g. Electrolyte excluded from the ED denominator per contract (electrolyte_included: false).

## 5. Performance Verification

| Metric | Value | Criterion (log entry 0) | Determination | Source |
|---|---|---|---|---|
| Energy density | 553.977 Wh/kg | ≥ 392.61 Wh/kg | PASS | cell/r3_I_energy.json:energy_density_wh_kg |
| Volumetric energy density | 905.983 Wh/L | no registered criterion | informational | cell/r3_I_energy.json:energy_density_wh_l |
| 4C fast-charge max temperature | 325.655 K (52.51 °C) | ≤ 333.15 K | PASS (margin 7.50 K) | cell/r3_I_4c_dfn.json:T_max_K |
| 4C fast-charge plating | plated = false (anode potential min +0.0249 V ≥ 0) | plated = false | PASS (margin 24.9 mV) | cell/r3_I_4c_dfn.json:anode_potential_v (DFN authoritative) |
| Overcharge 4.7 V | terminal voltage 4.7000 V; peak T 299.552 K | reaches 4.7 V | PASS | cell/r3_I_oc.json (voltage tail, T_max_K) |
| Thermal runaway after overcharge | triggered = false | triggered = false | PASS | cell/r3_I_tr.json:triggered (mcp = mass_kg × 900) |
| 1C discharge capacity | 5.6505 Ah | no registered criterion (vs parameter nominal 5.0 Ah) | PASS vs nominal | cell/r3_I_1c.json:capacity_ah |

## 6. Design Notes (parameters changed in this case, with round rationale)

- Thin current collectors (Al 16→8 µm, Cu 12→5 µm, round 1): converts inactive mass into ED headroom (round-1 evaluate: ED 500–547 Wh/kg all pass).
- Anode 110→120 µm with porosity 0.40 and AMVF 0.60 (round 1 → round 3): the DFN diagnosis (plan-update entry) showed 4C plating is transport/kinetic-limited charging from deep discharge, not end-of-charge saturation; porosity is the anti-plating spend. The round-2 AMVF 0.65 anode became near capacity-limiting (1C capacity dropped 5.743→5.602 Ah), so round 3 pairs the porosity increase with thickness compensation (recorded deviation from the round-2 reserve note, no-silent-drift rule).
- Graphite particles 5.86→2.5 µm (rounds 1–3): larger kinetic area and shorter solid-diffusion path at 20 A.
- Separator 12→6 µm (rounds 2–3): shorter ionic path (ultrathin ceramic-coated class).
- Electrolyte conductivity 1.8 S/m and transference number 0.55 (round 2–3, Stage-2 formulation fallback): the dominant plating levers — t+ alone moved the anode potential minimum from −0.1309 V to −0.0365 V (round-2 evaluate). Values are formulation-class estimates (constant-with-temperature simplification documented); not derived from a molecular funnel (no new molecule proposed, real_compute=false).
- Cooling h 10→100 W/m2K (rounds 1–3): closes the DFN Tmax gap (342.0 K at h=50 → 325.7 K at h=100, round-2/3 evaluates).
