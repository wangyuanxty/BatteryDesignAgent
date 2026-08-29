# VBF Design Specification — HEV Battery Cell (virtual design)

**Document number**: VBF-T7R3-DS-01 · **Case**: t7_r3 · **Date**: 2026-08-26
**Base parameter set**: Chen2020 (PyBaMM) · **Design candidate**: v19_final — `candidates/r7_v19_final_params.json`
**Status**: virtual design (simulation caliber; no physical build). Prepared / Reviewed / Approved: ________ (blank for signature)

---

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 (positive) / graphite (negative), LiPF₆-class carbonate electrolyte | Chen2020 base set |
| Nominal capacity | 6.28 Ah (set), simulated 1C capacity 6.2569 Ah (SPMe) / 6.28 Ah (DFN) | `r7_v19_final_1c.json:capacity_ah`, `r6_v19_1c_dfn.json` |
| Voltage window | 2.5 V – 4.2 V | Chen2020 `Upper/Lower voltage cut-off [V]` |
| Electrode dimensions | height 0.065 m × width 1.58 m (unwound strip); stack thickness 225.6 µm (pos 75.6 + sep 12 + neg 110 + Al 16 + Cu 12 µm) | Chen2020 geometry + `r7_v19_final_energy.json:thickness_m` |
| Shell / case thickness | **Not provided** (no parameter in set) | Chen2020 |
| Electrolyte formulation | carrier: Chen2020 electrolyte functions replaced by fractional values: **cation transference number 0.6**, **diffusivity 1.0×10⁻⁹ m²/s**, conductivity 1.5 S/m | `r7_v19_final_params.json` (formulation **estimate** — see Note 1) |
| SEI additive candidate | FEC (film-forming additive) — proposed in plan, **not simulated** (Stage 2 skipped, `meta.start_stage=3`) | `log.jsonl` entry 0 meta |

Note 1: transference number 0.6 / Dₑ 1×10⁻⁹ m²/s are **formulation-level estimates**, not a specific salt/solvent recipe. Literature data (Valøen & Reimers 2005, J. Electrochem. Soc.) show t⁺ ≈ 0.26–0.4 for conventional LiPF₆/EC systems; concentrated or salt-tuned electrolytes and fluorinated ether blends reach t⁺ 0.5–0.7. A real formulation must be down-selected and measured; the values here are the cell-design target properties.

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | Active volume fraction | Particle radius (µm) | Inventive value |
|---|---|---|---|---|---|
| Positive (NMC811) | 75.6 | 0.335 | 0.665 | **2.0** (base 5.22) | `r7_v19_final_params.json` |
| Negative (graphite) | **110** (base 85.2) | 0.25 | 0.75 | **2.0** (base 5.86) | `r7_v19_final_params.json` |
| Separator | 12 | 0.47 | — | — | Chen2020 |

| Current collector | Thickness (µm) | Density (kg/m³) | Source |
|---|---|---|---|
| Positive (Al) | 16 | 2700 | Chen2020 |
| Negative (Cu) | 12 | 8960 | Chen2020 |

**N/P ratio** = (Q_neg × ε_s,neg × L_neg) / (Q_pos × ε_s,pos × L_pos) = (33133 × 0.75 × 110×10⁻⁶) / (63104 × 0.665 × 75.6×10⁻⁶) = **0.862** (mechanical from Chen2020 max concentrations + layer geometry). Note: below the 1.05–1.15 industry practice for graphite anodes; the virtual design passes 4C plating at this balance — see §6.

## 3. Process design parameters

| Parameter | Value | Formula / source |
|---|---|---|
| Positive areal density | 164.0 g/m² | thickness×(1−ε)×density = 75.6 µm×0.665×3262 kg/m³ (energy contract) |
| Negative areal density | 136.7 g/m² | 110 µm×0.75×1657 kg/m³ (energy contract) |
| Positive compaction density | 2.17 g/cm³ | 3262×(1−0.335) kg/m³ ÷ 1000 |
| Negative compaction density | 1.24 g/cm³ | 1657×(1−0.25) kg/m³ ÷ 1000 |
| Electrolyte fill amount | 7.21 g/cell (≈6.00 mL) | pore volume 6.004×10⁻⁶ m³ (Σ Lt×ε×A) × 1200 kg/m³ (literature density 1.2 g/cm³, annotated default), fill factor 1.0 |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | **design-recommended value; actual production parameter requires line tuning** |

## 4. Mass breakdown (contract caliber: electrolyte excluded)

| Layer | kg/m² | g/cell (×0.1027 m²) | Source |
|---|---|---|---|
| Positive electrode | 0.1640 | 16.84 | `r7_v19_final_energy.json:layer_kg_m2` |
| Negative electrode | 0.1367 | 14.04 | 〃 |
| Positive CC (Al) | 0.0432 | 4.44 | 〃 |
| Negative CC (Cu) | 0.1075 | 11.04 | 〃 |
| Separator | 0.00252 | 0.259 | 〃 |
| **Sum (contract)** | — | **46.62 g** | `mass_kg = 0.0466198` |
| Electrolyte (additive) | — | +7.21 g | literature density, see §3 |
| **Total incl. electrolyte** | — | **53.83 g** | derived |

## 5. Performance verification vs criteria (entry 0)

| Criterion | Threshold | Result | Verdict | Evidence |
|---|---|---|---|---|
| Energy density | ≥ 327.18 Wh/kg | **482.4 Wh/kg** (contract; electrolyte excluded) / 417.9 Wh/kg incl. electrolyte | ✓ PASS | `r7_v19_final_energy.json:energy_density_wh_kg` |
| SEI after 100 cyc @45 °C | ≤ 550 nm | **512.9 nm** | ✓ PASS | `r7_v19_final_aging45c.json:sei_thickness_nm_end` |
| 4C charge plating | plated = false | anode_potential_v min = **+0.0171 V** (0 negative instants) | ✓ PASS | `r7_v19_final_4c45c.json:anode_potential_v` |
| Nail 10 W thermal runaway | triggered = false | **false**, T_max 318.2 K @ hA = 0.5 W/K | ✓ PASS | `r7_v19_final_nail_hA05.json` |

Additional measured values: 1C discharge capacity 6.2569 Ah (SPMe); rated energy 22.491 Wh; midpoint voltage 4.047 V; DCR 0.120 mΩ; volumetric energy density 970.7 Wh/L; 4C CC charge accepts 0.778 Ah (12.4 % SOC) before 4.2 V cutoff, T_max during 4C 363.2 K.

## 6. Design notes (what changed and why — from evaluate log)

| Parameter | Base → Final | Reason (log) |
|---|---|---|
| Negative electrode thickness | 85.2 → 110 µm | capacity/ED balance toward 6.28 Ah nominal |
| Cation transference number | 0.2594 → 0.6 | electrolytic concentration polarization was the 4C plating root cause (R4 V9 flipped plated true→false) |
| Electrolyte diffusivity | Nyman2008 fn → 1.0×10⁻⁹ m²/s | same root cause; combination with t⁺ gives full CC window margin |
| Electrolyte conductivity | fn → 1.5 S/m | minor contribution (R2/R4: σ alone inert for plating) |
| Positive particle radius | 5.22 → 2.0 µm | charge-depth limiter after electrolyte fix = positive solid diffusion (Chen2020 D_s,pos = 4×10⁻¹⁵ m²/s) |
| Negative particle radius | 5.86 → 2.0 µm | anode surface-area margin for plating robustness |
| Nominal cell capacity | 5.0 → 6.28 Ah | honesty correction: rating set to simulated 1C capacity → true 4C = 25.12 A |

Thermal-management design requirement (from nail sweep): active cooling with **hA ≥ 0.3 W/K** (measured minimum passing), design point **hA = 0.5 W/K** (T_max 318.2 K). At hA = 0.2 W/K the cell triggers (T = 405 K at 2097 s); at 0.05 W/K near-adiabatic it triggers at 346 s. hA = 0.5 W/K corresponds to ≈2.4 W/m²K over the 0.205 m² double-sided pouch surface — forced-air level cooling, realistic for HEV pack.

N/P = 0.862 note: mechanically derived from the returned set values; the design passes 4C plating under this balance. For production intent, N/P 1.05–1.15 (thicker negative) is recommended and would further increase the +17 mV anode margin; it would trade ~5 % energy density.

Structure model (`cell_model.stl`): **not requested in this headless session** (per protocol, decided by user clarification); recommended presentation if requested later: pouch stacked, exploded view with real thickness annotations.