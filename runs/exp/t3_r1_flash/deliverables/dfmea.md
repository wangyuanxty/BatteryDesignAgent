# Design FMEA — VBF Power-Tool Cell (V4 Margin-fix)

Case: t3_r1_flash | Generation date: 2026-08-25 | Doc: VBF-T3R1FLASH-DFMEA-01
Qualitative version, based on simulation signals (severity S / occurrence O: high/medium/low; RPN = qualitative S×O matrix).

| Failure mode | Failure cause | Simulation signal (detectability basis) | S | O | RPN | Design-side mitigation |
|---|---|---|---|---|---|---|
| Lithium plating at 4C fast charge | Negative electrode surface potential < 0 V (anode fills, overpotential grows) | r2_v4_4c_dfn.json anode_potential_v min +22.6 mV (baseline −0.19 V; V1 −3.9 mV) | high | low (margin 22.6 mV) | high×low=medium | Thicker anode (N/P↑), ε_neg 0.38, r_neg 1.0 µm, high σ_e/t⁺, 45 °C charge temp |
| Thermal runaway risk from fast-charge heat | Heat generation > cooling at 4C | T_max 321.94 K vs 333.15 K limit (baseline 354.3 K) | high | low | medium | Low-DCR thin-electrode design + forced-air cooling h=100 W/m²/K |
| Insufficient capacity | Electrode thinning cuts capacity | 3.438 Ah vs ≥2.0 Ah (baseline 4.95 Ah) | medium | low | medium | Thickness chosen to keep >3 Ah margin |
| 5C rate capability loss | Slow solid diffusion (D_pos=4e-15 m²/s) limits high-rate utilization | retention 0.987 vs ≥0.95 (baseline 0.087) | high | low | medium | Small particles r_pos 0.8 µm (τ ~160 s), thin electrodes, high-σ electrolyte |
| Electrolyte oxidative decomposition | Cell voltage above electrolyte stability window | Not computed in this case (molecular funnel skipped, start_stage=3; final DFT endorsement caliber not run, real_compute=false) | medium | low | low | Voltage window 2.5–4.2 V within standard EC/EMC LiPF6 stability (literature); honest note: not re-verified at molecular scale |

## Conclusion

Highest-risk items (plating, thermal, rate capability) all show large simulation margins in the final design (plating +22.6 mV, T −11.2 K, retention +3.7 pts) and have been mitigated in the design as implemented. Complete FMEA including process/supplier failure modes: N/A (beyond pure simulation boundary).
