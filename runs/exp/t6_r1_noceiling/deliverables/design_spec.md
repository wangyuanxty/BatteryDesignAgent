# Cell Design Specification — VBF-T6R1NOCEILING-DS-01

Case: smartphone battery, volumetric energy density ≥ 950 Wh/L, 4C fast charge without lithium plating, T_max ≤ 50 °C, anode SEI ≤ 500 nm after 100 cycles, voltage plateau ≥ 4.1 V. Ablation: ceiling_escalation OFF (no material-design escalation; Chen2020 NMC811/graphite system, architecture/formulation space only).

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 positive / graphite negative | Chen2020 parameter set (OCP: nmc_LGM50_ocp_Chen2020); task text names no system → anchor-table default, recorded in log entry 0 |
| Nominal capacity | 5.6 Ah (design value); 1C simulation-verified 5.3222 Ah | `cell/r2_bp_1c.json:capacity_ah`; nominal set consistent with designed loading (note: 5% over nominal estimate — recorded) |
| Voltage window | 2.5 – 4.2 V | Chen2020 parameter set (Lower/Upper voltage cut-off) |
| Electrolyte formulation | EC:EMC + LiPF6 (parameter-set electrolyte; transport: Nyman2008 σ/D functions) — salt concentration Not provided in parameter set | Chen2020 parameter set |
| Cation transference number | 0.2594 | Chen2020 parameter set |
| Cell dimensions (strip geometry) | 65 mm (height) × 1580 mm (width) × 0.1878 mm (stack thickness) | `Electrode height/width` Chen2020; thickness = Σ layers (below). Wound-strip geometry of the parameter set; shell thickness Not provided (no parameter) |
| Cell volume (contract) | 19.29 cm³ (= Σ layer thickness × area; electrolyte/casing excluded) | `cell/r2_bp_energy.json:volume_m3` |

## 2. Electrode and separator (design ED-Compact B-p)

| Layer | Thickness | Porosity | Active vol. fraction | Material / note | Source |
|---|---|---|---|---|---|
| Positive electrode | 75.6 µm | 0.30 (baseline 0.335) | 0.70 (baseline 0.665) | NMC811, density 3262 kg/m³, particle radius 5.22 µm | Chen2020 + `cell/params_r2_bp.json` |
| Negative electrode | 85.2 µm | 0.20 (baseline 0.25) | 0.80 (baseline 0.75) | graphite, density 1657 kg/m³, particle radius 4 µm (baseline 5.86 µm — plating-resistance lever) | Chen2020 + `cell/params_r2_bp.json` |
| Separator | 9 µm (baseline 12) | 0.47 | — | polyolefin, density 397 kg/m³ | Chen2020 + `cell/params_r2_bp.json` |
| Positive current collector | 10 µm (baseline 16) | — | — | Al, 2700 kg/m³ | `cell/params_r2_bp.json` |
| Negative current collector | 8 µm (baseline 12) | — | — | Cu, 8960 kg/m³ | `cell/params_r2_bp.json` |
| Total stack thickness | 187.8 µm | — | — | Σ of the five layers | computed |

N/P ratio = 0.83 (negative areal discharge capacity ÷ positive areal discharge capacity; neg: 33133 mol/m³ × 0.80 × 85.2 µm × Δx 0.9; pos: 63104 mol/m³ × 0.70 × 75.6 µm × Δx 0.73 — Chen2020-derived design is negative-limited, consistent with measured 1C capacity 5.32 Ah ≈ negative dischargeable capacity). Note: baseline N/P = 0.82; the design keeps the negative-limited characteristic of the parameter set.

Cooling design: h = 10 W/m²K (contract default; family tested to h = 25 W/m²K — see §5); cooling surface area 0.00531 m² (parameter-set wound-cell value, kept per entry-0 freedoms record).

## 3. Process design parameters

| Parameter | Formula | Value | Source note |
|---|---|---|---|
| Positive areal density | thickness × (1−porosity) × density | 172.6 g/m² | `cell/r2_bp_energy.json:layer_kg_m2.positive_electrode` |
| Negative areal density | thickness × (1−porosity) × density | 112.9 g/m² | `cell/r2_bp_energy.json:layer_kg_m2.negative_electrode` |
| Positive compaction density | density × (1−porosity) | 3262 × 0.70 = 2283 kg/m³ = 2.28 g/cm³ | computed (÷1000 conversion) |
| Negative compaction density | density × (1−porosity) | 1657 × 0.80 = 1326 kg/m³ = 1.33 g/cm³ | computed |
| Electrolyte fill amount | pore volume × electrolyte density | 4.514 cm³ × 1.2 g/cm³ = 5.42 g | pore volume = (75.6×0.30 + 85.2×0.20 + 9×0.47) µm × 0.1027 m²; 1.2 g/cm³ literature value (annotated) |
| Formation recommendation | — | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; production-line value requires tuning |
| Binder / conductive additive | — | no parameters in set; literature defaults applied in BOM with annotation; the parameter-set volume fractions leave zero inert volume (0.70+0.30=1.00) — production formulation must rebalance active fraction | annotated |

## 4. Mass breakdown (contract caliber: electrodes + CCs + separator; electrolyte excluded)

| Component | Mass (g) | Source |
|---|---|---|
| Positive electrode (active) | 17.73 | `cell/r2_bp_energy.json:layer_kg_m2.positive_electrode` × 0.1027 m² |
| Negative electrode (active) | 11.60 | `layer_kg_m2.negative_electrode` × area |
| Al current collector | 2.77 | `layer_kg_m2.positive_cc` × area |
| Cu current collector | 7.36 | `layer_kg_m2.negative_cc` × area |
| Separator | 0.19 | `layer_kg_m2.separator` × area |
| **Total (contract)** | **39.66** | `cell/r2_bp_energy.json:mass_kg` (0.039657 kg) |
| Electrolyte (add-on) | +5.42 | §3 formula, 1.2 g/cm³ literature value |
| Enclosure, tabs | Not modeled | honest note |

## 5. Performance verification (vs entry-0 criteria)

| Metric | Criterion | Measured | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | (reporting) | 5.3222 Ah (nominal 5.6) | within 5% of nominal | `cell/r2_bp_1c.json:capacity_ah` |
| Volumetric energy density | ≥ 950 Wh/L | **964.44 Wh/L** | **✓ PASS** | `cell/r2_bp_energy.json:energy_density_wh_l` |
| Gravimetric energy density | (reporting) | 469.06 Wh/kg | — | `cell/r2_bp_energy.json:energy_density_wh_kg` |
| Voltage plateau | ≥ 4.1 V | 3.9214 V | **✗ FAIL** (NMC811 cathode OCP ceiling ≈ 4.0 V; best in-case 3.998 V) | `cell/r2_bp_energy.json:midpoint_voltage_v` |
| 4C fast charge — plating | plated = false | plated = true (anode potential min −0.2566 V) | **✗ FAIL** | `cell/r2_bp_4c.json:anode_potential_v` |
| 4C fast charge — temperature | ≤ 50 °C (323.15 K) | T_max 351.004 K (h = 10); family datum at h = 25: 338.7 K (B) | **✗ FAIL** | `cell/r2_bp_4c.json:T_max_K`; `cell/r3_bh25_4c.json:T_max_K` |
| 4C charge acceptance | (reporting) | 0.096 Ah at 4C before 4.2 V voltage limit | poor fast-charge support (reported honestly, not a pass) | `cell/r2_bp_4c.json:capacity_ah` |
| Anode SEI after 100 cycles (1C) | ≤ 500 nm | **417.74 nm** | **✓ PASS** | `cell/r4_bp_aging.json:sei_thickness_nm_end` |

Capacity trajectory over 100 cycles climbs then saturates (1.80 → 2.15 Ah, standard SEI-model artifact — lithium loss shifts the voltage window; annotated, not treated as normal degradation; first-cycle low is the known discharged initial state of the Chen2020 set). Reliable aging indicator: `sei_thickness_nm_end`.

## 6. Design notes

- Levers changed (all architecture/formulation, in-boundary per entry-0 freedoms): separator 12→9 µm, CC 16/12→10/8 µm, pos active fraction 0.665→0.70 (porosity 0.335→0.30), neg active fraction 0.75→0.80 (porosity 0.25→0.20), neg particle radius 5.86→4 µm, nominal capacity reconciled to loading (5.6 Ah). Rationale per rounds R1–R2 evaluate entries: dead-layer thinning + negative-loading raise raises contract Wh/L from 843.5 (baseline) to 964.4; smaller negative particles add plating resistance (+0.022 V on anode min; insufficient to clear 4C).
- Not changed (locked, per task ablation note and entry-0 freedoms): electrode system (Chen2020), electrolyte transport parameters, electrode coatings/dopants, cooling surface area.
- Three metrics are boundary-locked (log `final.escalation`): plateau ≥ 4.1 V requires a 4.7 V-class cathode (LNMO-class midpoint 4.17 V — system switch excluded); plating-free 4C at ED ≥ 950 requires electrolyte transport design or a high-capacity anode system (formulation/material, excluded); T_max ≤ 50 °C at 4C/45 °C requires a smartphone-pouch cooling envelope with hA ≥ ~1.5 W/K (thermal-envelope redesign beyond the recorded h ≤ 25 lever).
- Engineering manufacturability drawings (tolerances), material specifications, and line process cards are outside the pure-simulation boundary — stated honestly.
