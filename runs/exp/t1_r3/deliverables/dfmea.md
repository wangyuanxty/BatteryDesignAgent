# Design FMEA (qualitative version) — V11 (t1_r3)

**Document number**: VBF-EXPT1R3-DFMEA-01
**Date**: 2026-08-26
**Note**: qualitative version based on simulation risk signals; severity (S) and occurrence (O) are three-level qualitative ratings (high/medium/low) whose basis is the magnitude of the simulation value relative to its threshold. Complete FMEA including process/supplier failures: N/A (beyond pure simulation boundary).

| # | Failure mode | Failure cause | Simulation signal (detectability basis) | S | O | Design-side mitigation |
|---|---|---|---|---|---|---|
| 1 | Lithium plating on fast charge | local anode potential < 0 V during 4C | `r5_v11_4c.json:anode_potential_v` min = +0.0425 V (42.5 mV margin at true 4C / 20.34 A) | high | low | 0.8 µm particles (2× surface), electrolyte D 6.0e-10 m²/s / t⁺ 0.55, 4C current capped at 20.34 A; note: cold-ambient fast charge not simulated — do not 4C-charge below 0 °C without physical validation |
| 2 | Thermal runaway / overheat | excessive heat generation vs cooling | 4C T_max 321.2 K vs 333.15 K limit (margin 12.0 K); overcharge 4.7 V T_max 298.57 K; TR ODE triggered = false | high | low | h = 120 W/m²/K cell cooling design; abuse tolerance verified by coupled overcharge→TR simulation |
| 3 | Electrolyte oxidative decomposition at high voltage | electrolyte HOMO above positive potential window | cell-scale: no thermal signal in 4.7 V overcharge (`r5_v11_oc.json:T_max_K` = 298.57 K), but DFN has no oxidation kinetics and molecular-level HOMO endorsement skipped (real_compute=false) | medium | medium | operate at ≤ 4.2 V; 4.7 V only as abuse-tolerance margin; recommend true DFT HOMO/IE-EA endorsement before production |
| 4 | Insufficient capacity / energy | capacity below task target | 1C capacity 5.0849 Ah; ED 605.33 Wh/kg vs 392.61 (54% margin) | low | low | ED margin maintained by thin collectors (10/6 µm) and thin separator (8 µm) |
| 5 | Mechanical integrity of thinned components | 6 µm Cu foil / 8 µm separator / 10 µm Al foil handling and dendrite puncture | no simulation signal (purely mechanical domain) — qualitative | medium | medium | manufacturing QC on foil handling; separator puncture/dendrite risk bounded by plating-free margin (+0.0425 V); physical mechanical tests N/A in virtual design |

## Conclusion

Highest-risk items: #1 and #2 (safety-critical) — both mitigated in-design with verified simulation margins (plating +42.5 mV, temperature 12 K below limit, no TR trigger after 4.7 V overcharge). Item #3 remains an open molecular-level question (honestly flagged; real_compute=false). Items #4/#5 low-to-medium.
