# Virtual Battery Factory — Design Plan

**Case**: t6_oa — Smartphone battery
**Objective (task text verbatim)**: volumetric energy density ≥ 950 Wh/L, 4C fast charge (no lithium plating), maximum temperature ≤ 50°C, anode SEI thickness ≤ 500 nm after 100 cycles, voltage plateau ≥ 4.1 V.

## 1. Objective decomposition (decision-layer criteria)

| Layer | Metric | Threshold | Notes |
|---|---|---|---|
| stage1 (molecular) | max_energy_ev | ≤ 0.0 eV | elimination line |
| stage1 (molecular) | max_homo_ev | ≤ −6.0 eV | elimination line |
| stage2 (cell) | energy_density_wh_l | ≥ 950 Wh/L | volumetric (contract caliber, electrolyte/casing excluded) |
| stage2 (cell) | midpoint_voltage_v | ≥ 4.1 V | plateau approximation |
| stage2 (cell) | sei_thickness_nm_end | ≤ 500 nm | after 100×1C cycles |
| stage3 (safety) | T_max_K | ≤ 323.15 K (50°C) | 4C charge @ 45°C ambient |
| stage3 (safety) | plated | false | anode surface potential ≥ 0 V throughout 4C charge |

**Multi-objective trade-off expectation**: volumetric ED and fast-charge safety (T_max, plating) are in tension. Thicker electrodes + higher active-material fraction raise volumetric ED but increase polarization, heat generation and plating tendency. High-voltage LNMO cathode raises energy per Ah (good for ED) but a 4C charge at a higher average voltage generates more heat per coulomb. Expected Pareto direction: ED ↑ ⟷ (T_max, plating) worsen; the design must find the frontier that satisfies all thresholds.

## 2. Candidate strategy

- **System selection (forced by plateau ≥ 4.1 V)**: the default NMC811 systems plateau at ~3.6 V and cannot meet ≥ 4.1 V. The LNMO high-voltage spinel cathode (4.7 V class, cell-level discharge midpoint ≈ 4.17 V) is the matching system. Base = Chen2020 + `LNMO.json` positive-electrode override (anchor: 4.7 V-class OCP, molar mass 0.1503 kg/mol).
- **Round 1 — baseline characterization**: 1C discharge → calc-energy (ED, plateau); 4C charge @ 45°C + plating (T_max, plating); aging 100×1C (SEI). This establishes the gap to each threshold.
- **Round 2+ — architecture exploration (2–4 variants/round)**: levers for volumetric ED (electrode thickness ↑, current-collector thickness ↓, separator thickness ↓, porosity ↓, active fraction ↑) and for fast-charge safety (anode particle radius ↓, electrolyte conductivity ↑, cooling h ↑, anode thickness ↓).

## 3. Budget allocation

- Round 1: baseline characterization (1 round).
- Rounds 2–7: architecture/material exploration (2–4 variants/round, SPMe quick-screen → DFN for passers).
- Rounds 8–12: safety fine-tuning (4C T_max + plating) and SEI/aging tuning.
- Reserve: fallback rounds for cause-localized rework.

## 4. Risk and fallback plan

- **Risk A — T_max ≤ 323.15 K is very tight** (only +5 K over 45 °C ambient during 4C charge). Mitigation: raise cooling coefficient h, lower DCR (conductivity ↑, particle size ↓, porosity ↑), verify with coupled lumped thermal model. Fallback route → Stage 3 architecture + electrolyte transport (Stage 2 formulation bridge).
- **Risk B — volumetric ED ≥ 950 Wh/L** may be below the architecture ceiling with Chen2020 geometry overhead (16+12 µm collectors, 12 µm separator). Mitigation: thin collectors/separator, thick electrodes, high active fraction. If unreachable → honest negative result with "reachable if X relaxed".
- **Risk C — graphite anode plating at 4C**. Mitigation: smaller anode particle radius, higher electrolyte conductivity, reduced anode thickness/N-P. Fallback → Stage 3 architecture.
- **Risk D — SEI > 500 nm after 100 cycles**. Mitigation: SEI-suppressing coating (SEI kinetic rate constant / exchange current density bridge), compare on same system.

## 5. References (domain basis)

- LNMO spinel (LiNi0.5Mn1.5O4) 4.7 V cathode raises cell energy density — well-established high-voltage cathode (domain experience).
- Thin current collectors/separators reduce inactive volume → higher volumetric ED — battery manufacturing practice (domain experience).
- Smaller anode particles increase active surface area → reduce plating tendency at high C-rate — electrode engineering (domain experience).
- High-conductivity/high-transference electrolyte mitigates fast-charge polarization — transport literature (domain experience, no precise source).
