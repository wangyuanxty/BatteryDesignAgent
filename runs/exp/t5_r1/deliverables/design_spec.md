# Cell Design Specification — VBF-T5R1-DS-01

**Case**: t5_r1 — next-generation flagship vehicle battery.
**Contract** (log.jsonl entry 0, verbatim): energy density ≥ 500.94 Wh/kg; 4C fast charge without lithium plating; maximum temperature ≤ 60 °C (= 333.15 K, mechanical conversion).
**Verdict**: ACHIEVED — design R7B, DFN-validated under both Chen2020 and OKane2022 (dual judgment).
**Generation date**: 2026-08-25. All values below are mechanically taken from parameter-set dumps, `bda run-pyamm` outputs, `bda calc-energy` output, or `bda log-evaluate` entries (source annotated per line). Missing items are marked "Not provided".

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite(-SiOx) pouch cell | `--base Chen2020` (recorded default) + `--base OKane2022` cross-validation; OKane2022 negative contains SiOx + native plating/cracking physics |
| Nominal capacity | 5.0 Ah | `Nominal cell capacity [A.h]` (both parameter sets) |
| Simulation-verified 1C capacity | 6.2104 Ah (Chen2020) / 6.2086 Ah (OKane2022), DFN | `cell/r7b_{chen,okane}_1c_dfn.json` via `calc-energy` capacity_ah |
| Voltage window | 2.5 – 4.2 V | `Lower/Upper voltage cut-off [V]` (both sets) |
| Cell dimensions (layer stack) | 0.065 m × 1.58 m × 203.4 µm | `Electrode height/width [m]` (both sets); thickness = Σ layer thicknesses (calc-energy) |
| Shell/housing thickness | Not provided (no parameter) | parameter set |
| Electrolyte formulation | EC-based liquid + 1 M LiPF6 (`EC initial concentration in electrolyte` = 4541 mol/m³, `Initial concentration in electrolyte` = 1000 mol/m³) with **design-target transport overrides**: σ = 2.0 S/m, D_e = 4.5×10⁻¹⁰ m²/s, t⁺ = 0.45 | parameter set (base values); overrides from `bridge/r7b_negR261.json`, flagged as literature-upper-bound estimates in proposals R5C/R5D/R6D |
| Cation transference number | 0.45 (design override) | `bridge/r7b_negR261.json` |

## 2. Electrode and separator

| Layer | Thickness | Porosity | Material / note | Source |
|---|---|---|---|---|
| Positive electrode | 75.6 µm | 0.335 (set default, not overridden) | NMC811 composite, density 3262 kg/m³ | `bridge/r7b_negR261.json` + set dump |
| Negative electrode | 105.8 µm | 0.45 (override) | graphite(-SiOx) composite, density 1657 kg/m³ | same |
| Separator | 8 µm | 0.55 (override) | polyolefin-class, density 397 kg/m³ (set value) | same |
| Positive current collector | 8 µm Al | — | density 2700 kg/m³ | same |
| Negative current collector | 6 µm Cu | — | density 8960 kg/m³ | same |
| Particle radius (pos/neg) | 2.61 µm / 2.61 µm | — | high-power small-grain class; negative was the decisive plating lever (R7) | `bridge/r7b_negR261.json` |
| N/P ratio | 1.40 | — | = negative/positive thickness ratio 105.8/75.6 (caliber used in proposals R4C–R6B; the parameter set defines fully-charged initial concentrations but has no 0%-SOC stoichiometry keys, so the capacity-density form cannot be computed from set keys alone). Empirically consistent: 1C discharge is anode-limited (R4C: capacity jumped 5.73 → 6.42 Ah when anode grew 85.2 → 110 µm) | propose entries + R4C evaluate |
| Thermal management | h = 60 W/(m²·K) (design override; set default 10) | — | immersion-class liquid cooling requirement, cooling area 0.00531 m² | `bridge/r7b_negR261.json`; `Cell cooling surface area [m2]` |

## 3. Process design parameters

| Parameter | Formula | Value | Source |
|---|---|---|---|
| Positive areal density | L × (1−ε) × ρ | 75.6e-6 × (1−0.335) × 3262 = **163.99 g/m²** | mechanical from §2 |
| Negative areal density | L × (1−ε) × ρ | 105.8e-6 × (1−0.45) × 1657 = **96.42 g/m²** | mechanical from §2 |
| Positive compaction density | ρ × (1−ε) / 1000 | 3262 × 0.665 / 1000 = **2.169 g/cm³** | mechanical from §2 |
| Negative compaction density | ρ × (1−ε) / 1000 | 1657 × 0.55 / 1000 = **0.911 g/cm³** | mechanical from §2 |
| Electrolyte fill amount | pore volume × 1.2 g/cm³ (literature density, annotated) | pores = (75.6e-6×0.335 + 105.8e-6×0.45 + 8e-6×0.55) × 0.1027 m² = 7.943 cm³ → **9.53 g** | mechanical; electrolyte density 1.2 g/cm³ = literature default (parameter set lacks the key) |
| Formation recommendation | — | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning |

## 4. Mass breakdown (contract caliber: electrolyte excluded)

Area = 0.065 × 1.58 = 0.1027 m². Per-layer kg/m² from `calc-energy` output `layer_kg_m2`.

| Layer | kg/m² | g/cell | Share |
|---|---|---|---|
| Positive electrode | 0.163994 | 16.842 | 48.6% |
| Negative electrode | 0.096421 | 9.902 | 28.6% |
| Positive CC (Al 8 µm) | 0.021600 | 2.218 | 6.4% |
| Negative CC (Cu 6 µm) | 0.053760 | 5.521 | 15.9% |
| Separator (8 µm) | 0.001429 | 0.147 | 0.4% |
| **Total** | **0.337204** | **34.631** | 100% |

Source: `cell/r7b_chen_energy.json:layer_kg_m2` × `area_m2` (mechanical). Electrolyte (9.53 g) excluded from contract mass — `electrolyte_included: false` annotated in output.

## 5. Performance verification

| Metric | Threshold (entry 0) | Chen2020 (DFN) | OKane2022 (DFN) | Verdict |
|---|---|---|---|---|
| Energy density | ≥ 500.94 Wh/kg | **642.098 Wh/kg** | **641.118 Wh/kg** | ✓ pass (both) |
| Rated energy | — | 22.236 Wh | 22.202 Wh | report |
| Volumetric ED (contract caliber) | — | 1064.49 Wh/L | 1062.87 Wh/L | report |
| 1C capacity | — | 6.210 Ah | 6.209 Ah | report |
| 4C charge T_max (45 °C ambient) | ≤ 333.15 K | **326.829 K** (53.7 °C) | **328.189 K** (55.0 °C) | ✓ pass (both) |
| 4C plating | false | anode surface potential min **+0.01826 V** (>0 → no plating) | min **+0.01798 V** (>0 → no plating) | ✓ pass (both) |
| Midpoint voltage | — | 3.798 V | 3.591 V | report |
| DC resistance (calc-energy caliber) | — | 3.50 mΩ | 17.93 mΩ | report |
| 4C charge acceptance (physical) | — | 4.73 Ah | 5.00 Ah | report (see caveat below) |

Sources: `cell/r7b_{chen,okane}_energy.json`, `cell/r7b_{chen,okane}_4c_dfn.json`, mechanically judged by `bda log-evaluate` round 7 (verdict=pass, checked=3).
Caveat: 4C-output `capacity_ah` is under-reported 5× by a library bug (`t×C_rate/3600` missing the 5 Ah nominal factor); physical charge acceptance computed separately as charge-segment duration × 20 A ÷ 3600. Does not affect the judgments above (plated from `anode_potential_v`, T_max from lumped thermal).

## 6. Design notes (what changed vs baseline and why — cited from the audit log)

- **Thin collectors** (Al 16→8 µm, Cu 12→6 µm) + slim cathode 75.6 µm + thick anode 105.8 µm: ED 400.8 → 630 Wh/kg class (R1 ceiling assessment → R3 → R6; N/P 1.40 unlocks anode-limited 1C capacity, R4C).
- **Electrolyte transport overrides** σ 2.0 S/m, D_e 4.5e-10 m²/s, t⁺ 0.45, plus ε_neg 0.45 and separator 8 µm: closed most of the plating gap (−0.13 V → −0.016 V, R4–R6) but saturated — literature-upper-bound estimates, flagged.
- **Negative particle radius 5.86 → 2.61 µm**: the decisive fix (R7, after three-strike questioning localized the dip to an end-of-charge solid-phase diffusion overpotential, τ = R²/Ds ≈ 1040 s vs ~800 s charge). Anode surface potential crossed positive: +18 mV margin under both systems.
- **h = 60 W/(m²·K)** immersion-class cooling: T_max ≤ 60 °C requirement (R5).
- Full per-round rationale: log.jsonl propose/evaluate entries R1–R7; plan + three-strike update in design_plan.md.
