# Design FMEA (qualitative version) — GridStore-D3

- **Number**: VBF-T2R1-DFMEA-01
- **Case**: t2_r1 — grid energy storage battery
- Qualitative version based on simulation risk signals; severity (S) / occurrence (O) rated high/medium/low, basis = magnitude of simulation value deviation from threshold. RPN = simplified qualitative S×O matrix (qualitative caliber annotated). Complete FMEA (process/supplier failures) is N/A (beyond pure simulation boundary).

## Failure-mode table

| # | Failure mode | Failure cause | Simulation signal (detectability basis) | S | O | Design-side mitigation recommendation |
|---|---|---|---|---|---|---|
| 1 | Negative electrode lithium plating at 4C fast charge | transport-limited anode concentration polarization during 4C charge at 45 °C | `anode_potential_v` min +0.0498 V (positive but the thinnest margin in the family; baseline was −0.1918 V) | high | low | Keep transport formulation (σ 3.0 S/m, D 2.5e-9 m²/s, r_n 2.0 µm, r_p 2.5 µm); margin monitoring during charge control; fallback designs with larger margin exist (D1 +0.091 V) if real-cell validation erodes the margin |
| 2 | Excessive temperature rise during fast charge | self-heating at 4C | T_max 342.39 K at 318.15 K ambient (+24.2 K) | medium | medium | No contract red line, but verify cell-level cooling in field use; thermal management (cooling h) was not a design lever in this case (contract default 10 W/m²/K) |
| 3 | Electrolyte oxidative decomposition at high voltage | high cathode potential vs electrolyte stability window | voltage window capped at 4.2 V; HOMO-level endorsement skipped (real_compute=false) — no molecular signal | medium | low | Keep 4.2 V cutoff; run Stage 2 molecular validation of the electrolyte formulation before production (honest gap) |
| 4 | Insufficient capacity / energy density | electrode loading / transport mismatch | 1C 5.066 Ah ≥ 5.0 nominal; ED 465.62 ≥ 327.18 Wh/kg | low | low | None required (margin ×1.42) |
| 5 | Low-temperature capacity loss | electrolyte transport freezing at −20 °C | retention 99.571% (protocol and true-soak, T_max 266.7 K) | low | low | Constant-transport formulation proxy is the enabler; validate real electrolyte at −20 °C physically |
| 6 | Long-term SEI overgrowth (>550 nm @500 cyc) | SEI growth kinetics | 25.32 nm @500 cyc (k_sei 1e-16 coating bridge; baseline 777.9 nm) | medium | low | The k_sei reduction is a coating-parameter bridge — the actual coating must be developed and validated (Stage 2 material work + physical aging test); without it the baseline kinetics give 777.9 nm (FAIL) |
| 7 | Model bookkeeping inconsistency (porosity override) | active volume fraction (0.665/0.75) defined at base porosity; final porosity 0.40 makes active + pore > 1 | parameter-set arithmetic (design_spec §6) | low | low | Physical electrode reformulation (binder/additive accounting) before manufacture; annotated in spec |

## Conclusion

Highest-risk items: #1 (plating margin thin at +0.0498 V) and #6 (SEI-kinetics assumption rests on the coating bridge — physical validation mandatory). Mitigations for both are embedded in the design (transport formulation; k_sei 1e-16 via coating bridge) with fallback designs on record (D1 for margin). Process/supplier-level FMEA: N/A (beyond pure simulation boundary).
