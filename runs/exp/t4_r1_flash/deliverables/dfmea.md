# Design FMEA — T4R1FLASH (qualitative version, based on simulation signals)

Case: `t4_r1_flash`  |  Generation date: 2026-08-25  |  Doc: VBF-T4R1FLASH-DFMEA-01

Qualitative caliber: S/O rated High/Medium/Low (H=3, M=2, L=1); RPN = S x O, simplified qualitative matrix.

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | RPN | Design-side mitigation (implemented) |
|---|---|---|---|---|---|---|
| Negative electrode lithium plating (fast charge) | Li+ transport limitation / anode overpotential < 0 V at 4C | anode_potential_v min = +0.0193 V (baseline was -0.44 V) | H | L (post-mitigation) | 3 | Electrolyte transport override sigma=2.0 S/m, D=5e-10, t+=0.60 (R2-R5); verified margin +19 mV |
| Thermal runaway (fast charge) | Charge heat accumulation exceeding cooling | T_max 329.61 K vs 333.15 K limit (baseline 350.6 K) | H | L (post-mitigation) | 3 | Forced-air cooling h=40 W/m2K; overcharge-to-TR ODE triggered=False |
| Electrolyte oxidative decomposition | Cell voltage beyond electrolyte stability window | HOMO/IE-EA vs 4.2 V window (molecular funnel; FEC/VC screened, 2 passed) | M | L | 2 | Additive screening at Stage 2; final DFT endorsement not run (real_compute=false) |
| Insufficient capacity | Electrode loading / N-P mismatch | 1C capacity 3.955 Ah vs nominal 3.93 Ah | M | L | 2 | Thickness re-balance 60/68 µm, C_nom reset to true 1C (R2) |

## Conclusion

Highest-risk items: plating and thermal runaway — both mitigated in the final design with simulation-verified margins (see DVPR). Complete FMEA including process/supplier failures: N/A (beyond pure simulation boundary).
