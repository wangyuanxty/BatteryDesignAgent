# Cell Design Specification — V4b "h60 + anode margin"

| | |
|---|---|
| Document number | VBF-T1R2-DS-01 |
| Case | t1_r2 — next-generation pure electric sedan cell |
| Design target | ED ≥ 392.61 Wh/kg; 4C fast charge, no lithium plating; T_max ≤ 60 °C (333.15 K); overcharge to 4.7 V without thermal runaway |
| Nominated design | V4b (Round 4) — all mechanical criteria pass |
| Base parameter set | Chen2020 (PyBaMM, NMC811 / graphite) |

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 positive / graphite negative, LiPF6 in EC/EMC | base parameter set Chen2020 |
| Nominal capacity | 5.0 Ah | parameter set `Nominal cell capacity [A.h]` |
| Simulated 1C discharge capacity | 5.6997 Ah | `cell/r4_v4b_1c_spme.json:capacity_ah` |
| Voltage window | 2.5 – 4.2 V | parameter set `Lower/Upper voltage cut-off [V]` |
| Electrode stack thickness | 194.6 µm (75.6 + 96 + 9 + 8 + 6) | `cell/r4_v4b_energy.json:thickness_m` (mechanical sum of layer thicknesses) |
| Electrode area | 0.1027 m² | `cell/r4_v4b_energy.json:area_m2` |
| Cell height × width | Not provided (cell-can form factor not modeled) | — |
| Design cell volume (thermal sim) | 2.514e-5 m³ | `cell/params_v4b.json:Cell volume [m3]` (scaled 2.42e-5 × 208.6/200.8; corresponds to the pre-collector-thinning stack — conservative for temperature, see §6 note) |
| Electrolyte formulation | σ = 1.8 S/m; D = 6.0e-10 m²/s; t⁺ = 0.4 (base 0.2594) | bridge values: literature-based estimates, marked `estimate` (recorded in propose R2–R4) |
| Additive candidates | None proposed (case started at Stage 3; molecular funnel skipped, entry-0 meta) | log.jsonl entry 0 |
| Cation transference number | 0.4 | `cell/params_v4b.json` |

## 2. Electrode and separator

| Layer | Thickness | Porosity | Active material / collector | Particle radius | Source |
|---|---|---|---|---|---|
| Positive electrode | 75.6 µm | 0.36 | NMC811 | 2.0 µm | thickness = parameter set `Positive electrode thickness [m]`; porosity/particle `cell/params_v4b.json` |
| Negative electrode | 96 µm | 0.32 | Graphite | 1.5 µm | `cell/params_v4b.json` |
| Separator | 9 µm | 0.50 | polyolefin (density 397 kg/m³, parameter set) | — | `cell/params_v4b.json` |
| Positive current collector | 8 µm | — | Al (2700 kg/m³, parameter set) | — | `cell/params_v4b.json` |
| Negative current collector | 6 µm | — | Cu (8960 kg/m³, parameter set) | — | `cell/params_v4b.json` |

**N/P ratio ≈ 1.35** — formula: N/P = (negative capacity density × thickness) ÷ (positive capacity density × thickness).
Mechanical inputs: negative areal mass 108.17 g/m² × C_neg = 372 mAh/g (graphite theoretical, literature); positive areal mass 157.83 g/m² × C_pos = 190 mAh/g (NMC811 practical at 4.2 V, literature range 180–200 mAh/g, midpoint `estimate`) → 40.24 / 29.99 = 1.34; with C_pos in range → 1.31–1.38, quoted as ≈ 1.35 (consistent with propose R4). Areal masses: `cell/r4_v4b_energy.json:layer_kg_m2`.

## 3. Process design parameters

| Parameter | Value | Formula | Source note |
|---|---|---|---|
| Positive areal density | 157.83 g/m² | thickness × (1−porosity) × electrode density | `r4_v4b_energy.json:layer_kg_m2.positive_electrode` (75.6e-6 × 0.64 × 3262) |
| Negative areal density | 108.17 g/m² | same | `layer_kg_m2.negative_electrode` (96e-6 × 0.68 × 1657) |
| Positive compaction density | 2.09 g/cm³ | electrode density × (1−porosity) ÷ 1000 | 3262 × 0.64 = 2087.7 kg/m³; densities = parameter set |
| Negative compaction density | 1.13 g/cm³ | same | 1657 × 0.68 = 1126.8 kg/m³ |
| Electrolyte fill amount | 7.69 g/cell | pore volume × electrolyte density × fill factor | pore volume 6.41 cm³ = (75.6×0.36 + 9×0.5 + 96×0.32) µm × 0.1027 m²; electrolyte density 1.2 g/cm³ (literature, `estimate`); fill factor 1.0 assumed |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | — | design recommended value; actual production-line value requires tuning |

## 4. Mass breakdown (per cell)

Formula caliber: mass = layer thickness × (1−porosity) × density × area (contract formula, electrolyte excluded — parameter set has no electrolyte density); electrolyte row added with literature density 1.2 g/cm³ (`estimate`).

| Component | Mass (g) | Source |
|---|---|---|
| Positive electrode coating | 16.21 | `r4_v4b_energy.json:layer_kg_m2.positive_electrode` × 0.1027 m² |
| Negative electrode coating | 11.11 | `layer_kg_m2.negative_electrode` × 0.1027 m² |
| Separator | 0.18 | `layer_kg_m2.separator` × 0.1027 m² |
| Positive current collector (Al) | 2.22 | `layer_kg_m2.positive_cc` × 0.1027 m² |
| Negative current collector (Cu) | 5.52 | `layer_kg_m2.negative_cc` × 0.1027 m² |
| **Subtotal (contract caliber, electrolyte excluded)** | **35.24** | `r4_v4b_energy.json:mass_kg` (0.0352409 kg) |
| Electrolyte (literature density estimate) | 7.69 | §3 fill amount |
| **Total incl. electrolyte** | **42.93** | subtotal + electrolyte |
| Enclosure / tabs | Not modeled | — |

Energy density: contract caliber 583.2 Wh/kg (`r4_v4b_energy.json:energy_density_wh_kg`); incl. electrolyte estimate 20.553 Wh / 0.04293 kg = 478.7 Wh/kg (`inferred`, formula noted).

## 5. Performance verification (V4b vs entry-0 criteria)

| Item | Value | Criterion | Verdict | Source |
|---|---|---|---|---|
| Energy density | 583.2 Wh/kg | ≥ 392.61 Wh/kg | ✓ pass | `cell/r4_v4b_energy.json:energy_density_wh_kg` |
| 1C discharge capacity | 5.6997 Ah | ≥ nominal 5.0 Ah | ✓ pass | `cell/r4_v4b_1c_spme.json:capacity_ah` |
| 4C fast-charge max temperature | 326.46 K (53.31 °C) | ≤ 333.15 K | ✓ pass (margin 6.69 K) | `cell/r4_v4b_4c_dfn.json:T_max_K` (326.459 K) |
| 4C lithium plating | anode potential min +0.0215 V → plated = false | plated == false | ✓ pass | `cell/r4_v4b_4c_dfn.json:anode_potential_v` min (mechanical) |
| 4C CC acceptance | 4.53 Ah = 79% of 5.70 Ah | (informational) | — | `inferred`: (t_end − t_vmin) × 20 A / 3600 = 815 s × 20 A / 3600; `capacity_ah` key unreliable for charge protocols (PyBaMM cycle-split artifact, recorded in evaluate R1 note) |
| Overcharge to 4.7 V (0.5C, 4.2+0.5 V protocol) max temperature | 299.43 K | no thermal runaway | ✓ pass | `cell/r4_v4b_overcharge.json:T_max_K` |
| Thermal runaway after overcharge | triggered = false | triggered == false | ✓ pass | `cell/r4_v4b_tr.json:triggered` (mcp = 31.72 J/K = mass×900; hA = 0.3186 = 60 × 0.00531 design-consistent) |

Mechanical verdicts logged via `bda log-evaluate` round 4 (main + safety entries, both pass). Margin note: 4C T_max margin 6.69 K and anode margin +21.5 mV are the best combined margins across all four rounds.

## 6. Design notes (what was changed and why)

Baseline (Chen2020, R1) met energy density (400.3 Wh/kg) but failed 4C: T_max 354.29 K and anode −0.192 V (plating), acceptance 0.88 Ah → binding constraint = 4C polarization at cell scale → fallback to Stage 3 (architecture + thermal), no Stage 2 escalation (ED ceiling ≈ 550 Wh/kg assessment, R1).

- **R2 (kinetics + transport)** — plating fixed by: fine particles (positive 2.0 µm / negative 1.5–2.5 µm), electrolyte bridge σ 1.8 S/m / D 6e-10 / t⁺ 0.4 (`estimate`), negative porosity 0.32; geometry alone insufficient (V2c still plated, evaluate R2).
- **R3 (thermal)** — T_max fixed by liquid cooling h = 45 W/m²·K (V3b/V3c pass all criteria; h = 30 fails by 2.0 K, evaluate R3).
- **R4 (robustness)** — h = 60 W/m²·K (cold-plate class), negative thickness 96 µm (N/P ≈ 1.35), negative particle 1.5 µm (surface ×1.33) to widen both margins (evaluate R4).

Transparency notes:
- The `Cell volume [m3]` override (2.514e-5) was scaled from the pre-collector-thinning stack (208.6 µm); the as-designed stack is 194.6 µm, so the thermal simulation volume is ~7% larger than the as-built stack — conservative direction for T_max (larger volume → larger lumped heat input at equal heat flux).
- Electrolyte σ/D/t⁺ are literature-based bridge estimates, not simulation outputs; they are marked `estimate` in the audit log and are the parameters a Stage 2 formulation round or true MD endorsement would verify (skipped: entry-0 meta `real_compute: false`, endorse entry records the skip honestly).
- `capacity_ah` in charge/overcharge protocol outputs is unreliable (PyBaMM cycle-split artifact); 4C acceptance derived mechanically from the voltage curve (formula in §5).

All conclusion-grade values above are tool-output values (`sourced`) or mechanically derived from them (`inferred`); no fabricated values.
