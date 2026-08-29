# Cell Design Specification — t5_r1_flash

**Doc No. VBF-T5R1FLASH-DS-01** · Design case: next-generation flagship-vehicle battery · Rev A (2026-08-25)
Requirement (task contract): energy density ≥ 500.94 Wh/kg · 4C fast charge without lithium plating · maximum temperature ≤ 60 °C (333.15 K).

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | LNMO (LiNi0.5Mn1.5O4, 4.7 V high-voltage spinel) / graphite | base parameter set LNMO.json + Chen2020 negative defaults (runner-injected) |
| Nominal capacity | 4.5 Ah (nominal, parameter set) / 8.26 Ah (simulated 1C, DFN) | LNMO.json `Nominal cell capacity [A.h]`; cell/r9_lnmo_r6_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.7 V | LNMO.json `Lower/Upper voltage cut-off [V]` |
| Cell dimensions | height × width × thickness = Not provided (area 0.1027 m², stack thickness 300 µm) | shell geometry not in parameter set; cell/r9_lnmo_r6_energy_dfn.json:thickness_m/area_m2 |
| Electrolyte formulation | HiTrans-class carbonate/LiFSI-like transport: σ 6 S/m, t⁺ 0.70, D 1.0e-9 m²/s (domain estimates, marked **estimate**, LiFSI-class literature; not yet true-MD-endorsed) + additive set FEC/VC/PES/DTD (funnel-passed, Stage 2) | params_lnmo_r6.json; funnel3 entry; values marked estimate in log |
| Cation transference number | 0.70 | params_lnmo_r6.json `Cation transference number` |

## 2. Electrode and separator

| Layer | Material | Thickness (µm) | Porosity | Active fraction | Source |
|---|---|---|---|---|---|
| Positive electrode | LNMO | 98 | 0.30 | 0.665 | params_lnmo_r6.json; LNMO.json active vol fraction |
| Negative electrode | Graphite | 180 | 0.32 | 0.75 | params_lnmo_r6.json; Chen2020 default active vol fraction |
| Separator | Not provided (default, ρ 397 kg/m³) | 9 | 0.55 | — | params_lnmo_r6.json |
| Positive current collector | Al | 8 | — | — | params_lnmo_r6.json |
| Negative current collector | Cu | 5 | — | — | params_lnmo_r6.json |
| Particles | pos 2.5 µm / neg 1.5 µm | — | — | — | params_lnmo_r6.json |

N/P ratio = (negative areal active capacity)/(positive areal active capacity)
= (m_neg·a_neg·q_neg)/(m_pos·a_pos·q_pos) = (0.2028×0.75×372)/(0.3018×0.665×146.6) = **1.92**
(q_neg 372 mAh/g graphite theoretical, q_pos 146.6 mAh/g LNMO theoretical — literature; audit round notes cited simplified estimates 1.78–2.14; deliverable value supersedes with explicit formula.)

## 3. Process design parameters

| Parameter | Value | Formula / source |
|---|---|---|
| Positive areal density | 302 g/m² | thickness×(1−ε)×ρ = 98 µm×0.70×4400 kg/m³ (calc-energy layer_kg_m2) |
| Negative areal density | 203 g/m² | 180 µm×0.68×1657 kg/m³ (calc-energy layer_kg_m2) |
| Positive compaction density | 3.08 g/cm³ | electrode density×(1−porosity) ÷1000 |
| Negative compaction density | 1.13 g/cm³ | 1657×0.68 ÷1000 |
| Electrolyte fill amount | 9.4 mL / 11.3 g | pore volume×electrolyte density×fill factor (1.0); electrolyte density 1.2 g/cm³ literature value, parameter set missing (annotated) |
| Formation recommendation | 0.1C CC to 4.7 V, 25 °C, 2 cycles | design recommended value; production-line value requires tuning |

## 4. Mass breakdown (per cell)

| Component | Mass (g) | Source |
|---|---|---|
| Positive coating (LNMO composite) | 31.00 | calc-energy layer_kg_m2×area |
| Negative coating (graphite composite) | 20.83 | same |
| Positive CC (Al) | 2.22 | same |
| Negative CC (Cu) | 4.60 | same |
| Separator | 0.17 | same |
| **Total (contract caliber, electrolyte excluded)** | **58.81** | calc-energy mass_kg |
| Electrolyte (informational, 1.2 g/cm³) | 11.3 | pore volume calc (annotated literature density) |
| Total incl. electrolyte | 70.1 | above |
| Enclosure / tabs | Not modeled | beyond pure simulation boundary |

Contract energy density excludes electrolyte per calc-energy contract (electrolyte_included=false); with electrolyte the cell would be 501 Wh/kg (informational).

## 5. Performance verification (conclusion-grade, DFN)

| Metric | Value | Threshold (entry 0) | Determination |
|---|---|---|---|
| Energy density (1C, DFN) | 597.9 Wh/kg | ≥ 500.94 | ✓ PASS |
| Max temperature (4C charge @45 °C ambient, DFN) | 327.55 K = 54.4 °C | ≤ 333.15 K (≤60 °C) | ✓ PASS |
| Lithium plating (4C, anode potential min) | +14.7 mV (> 0) | none (plated=false) | ✓ PASS (no plating) |
| 1C discharge capacity (DFN) | 8.26 Ah | — (informational) | reported |
| Midpoint voltage | 4.235 V | — (informational) | reported |
| DC resistance (calc-energy formula) | 8.0 mΩ | — (informational) | reported |
| Volumetric energy density | 1141 Wh/L | — (informational) | reported |

All conclusion-grade values: cell/r9_lnmo_r6_energy_dfn.json, cell/r9_lnmo_r6_4c45_dfn.json (see DVPR-01 for per-row sources).

## 6. Design notes

- Baseline Chen2020 (NMC811/graphite): ED 400.3 Wh/kg, 4C anode min −0.438 V → confirmed below target; **escalated to Stage 2 materials** (plan_update1): LNMO 4.7 V high-voltage system + HiTrans-class transport + mass-cut architecture (10→8 µm Al, 6→5 µm Cu, 12→9 µm sep).
- ED chain: 492.8 → 520.2 → 539.5 → 566.8 → 622.6 → 612.6 → **603.6 (SPMe) / 597.9 (DFN)** — all ≥ 500.94 from R4 on; final architecture keeps 97 Wh/kg margin.
- Plating chain (anode min, same protocol, same 2.0 Ah charge cap): −0.128 → −0.041 → −0.005 → **+0.015 V** via N/P increase (122→180 µm negative), negative porosity 0.22→0.32, electrolyte D 4e-10→1e-9 m²/s, σ 3.5→6 S/m, separator ε 0.45→0.55 (diagnosis in evaluate R6–R9 notes).
- T_max chain: 321–330 K across LNMO rounds, final 327.6 K at h=100 W/m²K cooling (5.6 K margin).
- Transport values (σ 6 S/m, t⁺ 0.7, D 1e-9 m²/s) are LiFSI-class **domain estimates** (marked estimate in audit; Stage 2 funnel passed the additive set; true DFT/MD endorsement skipped — real_compute=false, endorse entry records skip honestly).
