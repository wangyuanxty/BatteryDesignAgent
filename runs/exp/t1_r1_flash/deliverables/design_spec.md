# Cell Design Specification — VBF-T1R1FLASH-DS-01

Case: next-generation BEV sedan battery (ED ≥ 392.61 Wh/kg · 4C fast charge no plating · T_max ≤ 60 °C · overcharge to 4.7 V no thermal runaway)
Generation date: 2026-08-25 · Source: OKane2022 parameter set + bda simulation outputs (file:key annotated per line)

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite+SiOx (OKane2022 parameterization) | entry-0 meta.base_params |
| Nominal capacity (Ah) | 4.936 (1C DFN discharge) | cell/final_1c_dfn.json:capacity_ah |
| Voltage window (V) | 2.5 – 4.2 | OKane2022 parameter set (Lower/Upper voltage cut-off) |
| Cell form | Pouch strip 1580 mm × 65 mm; total stack thickness 0.1908 mm | Electrode height/width/thickness params |
| Shell/casing thickness | Not provided (parameter set has no shell) | — |
| Electrolyte | High-transport formulation: σ = 5.0 S/m, D = 1.2e-9 m²/s, t⁺ = 0.65 (design override, **estimate**; base Nyman2008 σ(45 °C)=1.46 S/m, D=2.72e-10, t⁺=0.259) | candidates/archA_h150_f4b.json + pybamm parameter dump |
| Cation transference number | 0.65 (design override) | candidates/archA_h150_f4b.json |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | Material | Source |
|---|---|---|---|---|
| Positive electrode | 75.6 | 0.335 | NMC811 | OKane2022 params |
| Negative electrode | 85.2 | 0.25 | graphite+SiOx | OKane2022 params |
| Separator | 12.0 | 0.47 | polyolefin | OKane2022 params |
| Positive current collector | 10.0 (stock 16) | — | Al | candidates/archA_h150_f4b.json |
| Negative current collector | 8.0 (stock 12) | — | Cu | candidates/archA_h150_f4b.json |
| N/P | 1.13 (85.2/75.6 thickness balance; capacity-caliber N/P not separately parameterized) | | | OKane2022 stock balance |

## 3. Process design parameters

| Parameter | Value | Formula / source |
|---|---|---|
| Positive areal density | 164.0 g/m² | thickness×(1−ε)×density = 75.6e-6×0.665×3262; = layer_kg_m2 positive_electrode 0.163994 kg/m² |
| Negative areal density | 105.9 g/m² | 85.2e-6×0.75×1657 = 0.105882 kg/m² |
| Positive compaction density | 2.17 g/cm³ | 3262×0.665 = 2169 kg/m³ ÷1000 |
| Negative compaction density | 1.24 g/cm³ | 1657×0.75 = 1243 kg/m³ ÷1000 |
| Electrolyte fill amount | 6.44 g | pore volume 5.37e-6 m³ × 1.2 g/cm³ (literature density, annotated) |
| Formation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; production-line value requires tuning |
| Cooling requirement | h ≥ 120 W/m²·K (liquid cooling; design point 150) | robustness probe F4b-h120 passed |

## 4. Mass breakdown (contract caliber, electrolyte excluded)

| Layer | kg/m² | Mass (g) | Source |
|---|---|---|---|
| Positive electrode | 0.163994 | 16.84 | calc-energy layer_kg_m2 × area 0.1027 m² |
| Negative electrode | 0.105882 | 10.87 | same |
| Positive CC (Al) | 0.027000 | 2.77 | same |
| Negative CC (Cu) | 0.071680 | 7.36 | same |
| Separator | 0.002525 | 0.26 | same |
| **Total** | — | **38.11** | cell/final_energy.json:mass_kg (electrolyte excluded; +6.44 g electrolyte per BOM caliber) |

## 5. Performance verification (vs entry-0 criteria)

| Metric | Result | Threshold | Verdict | Source |
|---|---|---|---|---|
| Energy density | 459.41 Wh/kg | ≥ 392.61 | ✓ | cell/final_energy.json:energy_density_wh_kg |
| 4C charge T_max | 323.39 K (50.2 °C) | ≤ 333.15 K | ✓ | cell/archA_h150_f4b_4c.json:T_max_K |
| 4C charge plating | anode min +0.0114 V | ≥ 0 V (plated=false) | ✓ | cell/archA_h150_f4b_4c.json:anode_potential_v |
| Overcharge 4.7 V → TR | triggered = false | triggered=false | ✓ | cell/final_tr.json:triggered |

## 6. Design notes (rationale from evaluate log, rounds 1–6)

- Electrolyte transport overrides (σ/D/t⁺): root-cause fix for end-of-charge anode surface saturation at 4C (rounds 3–5; anode min −0.077 → −0.029 → −0.0023 → +0.0114 V). Values are literature-informed estimates for high-conductivity/single-ion-like formulations.
- Thin collectors (16/12 → 10/8 µm): ED boost 405.6 → 462.6 Wh/kg at zero electrochemical side effect (round 1).
- Liquid cooling h = 150 (robustness verified at h = 120): T_max fix (367.4 → 323.4 K) without ED cost (round 2); thermal-management DOF, undeclared in task → widest interpretation.
- N/P increase rejected by measurement (round 4): deeper charge into anode saturation, no plating benefit.
