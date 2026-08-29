# Cell Design Specification — V10a_final_h45 (extreme-cold equipment battery)

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (baseline teaching parameterization) | anchor table mapping, entry 0 (task text named no system → default Chen2020) |
| Electrolyte | EC/EMC + LiPF6 base (Chen2020); transport design overrides: sigma = 4.0 S/m, D = 3.539e-10 m2/s | params_r6_v10a_h45.json (sigma/D: literature-derived estimates, logged in R3/R4 propose) |
| Cation transference number | 0.45 | params_r6_v10a_h45.json |
| Nominal capacity | 5.0 Ah (parameter set) / 5.0618 Ah (1C DFN simulation) | Chen2020 set "Nominal cell capacity [A.h]"; r6_final_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V | Chen2020 set lower/upper cut-off |
| Cell dimensions | electrode sheet 65 mm height x 1580 mm width x 184.8 um stack thickness | Chen2020 set height/width; r6_final_energy_dfn.json:thickness_m (wound/pouch form factor not parameterized — "Not provided") |

## 2. Electrode and separator

| Layer | Material | Thickness (um) | Porosity | Density (kg/m3) | Source |
|---|---|---|---|---|---|
| Positive electrode | NMC811 | 75.6 | 0.40 (design override, base 0.335) | 3262 | Chen2020 set + params_r6_v10a_h45.json |
| Negative electrode | graphite | 85.2 | 0.35 (design override, base 0.25) | 1657 | Chen2020 set + params_r6_v10a_h45.json |
| Separator | polyolefin | 10 (base 12) | 0.47 | 397 | Chen2020 set + params_r6_v10a_h45.json |
| Positive current collector | Al | 8 (base 16) | — | 2700 | params_r6_v10a_h45.json |
| Negative current collector | Cu | 6 (base 12) | — | 8960 | params_r6_v10a_h45.json |
| Particle radii | pos 3 um / neg 2 um | design overrides | | | params_r6_v10a_h45.json |
| N/P ratio | Not provided — Chen2020 exposes no per-electrode capacity-density keys; electrode thickness balance unchanged from baseline (not a design lever this case) | | | |

## 3. Process design parameters

| Parameter | Formula | Value | Unit | Source |
|---|---|---|---|---|
| Positive areal density | thickness x (1-porosity) x density | 147.96 | g/m2 | 75.6e-6 x 0.60 x 3262 (mechanical) |
| Negative areal density | thickness x (1-porosity) x density | 91.76 | g/m2 | 85.2e-6 x 0.65 x 1657 (mechanical) |
| Positive compaction density | density x (1-porosity) / 1000 | 1.957 | g/cm3 | 3262 x 0.60 / 1000 (mechanical) |
| Negative compaction density | density x (1-porosity) / 1000 | 1.077 | g/cm3 | 1657 x 0.65 / 1000 (mechanical) |
| Electrolyte fill amount | pore volume x electrolyte density x fill factor | 7.98 (fill factor 1.0) | g | pore volume 6.651 cm3 x 1.2 g/cm3 (electrolyte density = literature value, annotated) |
| Formation recommendation | 0.1C CC to 4.2 V, 25 C, 2 cycles | design recommended value; actual production-line value requires tuning | | annotated |

## 4. Mass breakdown (contract caliber: layer solids, electrolyte excluded)

| Layer | Mass (g) | Source |
|---|---|---|
| Positive electrode (solids) | 15.196 | r6_final_energy_dfn.json:layer_kg_m2.positive_electrode x area 0.1027 m2 |
| Negative electrode (solids) | 9.424 | layer_kg_m2.negative_electrode x area |
| Positive current collector (Al) | 2.218 | layer_kg_m2.positive_cc x area |
| Negative current collector (Cu) | 5.521 | layer_kg_m2.negative_cc x area |
| Separator | 0.216 | layer_kg_m2.separator x area |
| Total | 32.576 | r6_final_energy_dfn.json:mass_kg (electrolyte_included: false) |
| Electrolyte (estimate, not in contract mass) | 7.98 | pore volume x 1.2 g/cm3 (literature density, annotated) |

## 5. Performance verification (vs entry-0 criteria)

| Metric | Threshold (entry 0) | Value | Verdict | Source |
|---|---|---|---|---|
| -20 C 1C retention | >= 0.95 | 0.9944 (5.0337 / 5.0618 Ah) | PASS | derived_r6_final_dfn.json (mechanical lowT/1C) |
| Energy density | >= 327.18 Wh/kg | 564.84 Wh/kg | PASS | r6_final_energy_dfn.json:energy_density_wh_kg |
| Volumetric energy density | >= 880 Wh/L | 969.50 Wh/L | PASS | r6_final_energy_dfn.json:energy_density_wh_l |
| 4C/45C max temperature | <= 333.15 K | 329.33 K | PASS | r6_final_4C45_safety_dfn.json:T_max_K |
| 4C/45C lithium plating | plated = false | false (anode min +28.96 mV) | PASS | r6_final_4C45_safety_dfn.json:anode_potential_v min |
| Robustness re-check (OKane2022 base) | same thresholds | retention 0.9788; T_max 331.78 K; anode min +24.96 mV | PASS | derived_r6_final_ok_spme.json; r6_final_ok_4C45_safety_dfn.json |
| Cold-start honesty (Initial temp 253.15 K) | retention >= 0.95 | 0.9944 (T_max 257.10 K confirms cold start) | PASS | derived_r6_final_coldstart.json |

## 6. Design notes (change rationale, citing evaluate log)

1. R1 baseline failed ED_vol (844.45 Wh/L < 880) and 4C plating → architecture scale (Stage 3).
2. R2/R3: thinned current collectors 16/12 → 8/6 um and separator 12 → 10 um (ED_vol), raised anode porosity 0.25 → 0.30, later 0.35 (plating margin at separator interface) — plating persisted until deep transport was applied.
3. R4: deep transport (sigma 4.0 S/m, t+ 0.45, D 3.539e-10 m2/s, particles 3/2 um, cathode porosity 0.40) + cooling h = 40 W/m2K → all five criteria pass at SPMe (T_max 330.67 K, anode +22.6 mV).
4. R5: DFN verification passes (T_max 330.47 K, anode +30.1 mV); cold-start honesty check passes; OKane2022 robustness at h=40 fails T_max by 0.165 K (333.315 K).
5. R6: h = 45 W/m2K adopted → passes both bases at DFN grade (Chen2020 T_max 329.33 K / anode +28.96 mV; OKane2022 T_max 331.78 K / anode +24.96 mV). Final design = V10a_final_h45.
