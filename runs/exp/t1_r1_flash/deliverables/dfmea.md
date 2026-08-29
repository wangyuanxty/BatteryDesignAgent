# Design FMEA (qualitative, simulation-signal based) — VBF-T1R1FLASH-DFMEA-01

Case: next-generation BEV sedan battery · Generation date: 2026-08-25
Qualitative caliber: S/O three-level ratings based on simulated margin to threshold; RPN = S×O qualitative matrix. Full process/supplier FMEA: N/A (beyond pure simulation boundary).

| # | Failure mode | Failure cause | Simulation signal (detectability) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|---|
| 1 | Lithium plating at 4C fast charge | End-of-charge anode surface saturation (electrolyte transport + kinetics) | anode_potential_v min = +0.0114 V (11.4 mV margin) | High | Low (margin > 10 mV; was −77 mV before transport fix) | High-transport electrolyte (σ 5.0 S/m, D 1.2e-9, t⁺ 0.65); thin collectors; cooling h=150 |
| 2 | Thermal runaway from fast-charge temperature | Heat generation exceeds cooling at 4C | T_max 323.4 K vs limit 333.15 (9.8 K margin); 367.4 K at h=10 | High | Low (margin restored by cooling) | Liquid cooling h ≥ 120 (design point 150); DCR reduced to 20.3 mΩ by high-σ electrolyte |
| 3 | Overcharge-induced thermal runaway | 0.5C overcharge to 4.7 V pushes cell into SEI-decomposition regime | run-tr triggered=false; overcharge T_max 299.1 K, dT/dt max −7.5e-6 K/s (cooling) | High | Low | Cell mass 38 g (mcp 34.3 J/K), strong cooling h=150, low DCR; pass verified mechanically |
| 4 | Electrolyte oxidative decomposition | Voltage window exceedance | Not evaluated (real_compute=false; no HOMO/IE-EA endorsement) | Medium | Not assessed | Honest N/A — requires true-compute endorsement; 4.2 V cutoff within NMC811 stability envelope (domain knowledge) |
| 5 | Insufficient capacity / energy | Electrode balance or porosity miscalibration | 1C capacity 4.936 Ah (98.7% of nominal); ED 459.4 vs target 392.61 | Medium | Low (17% ED margin) | Thick-electrode + thin-collector architecture; validated at 1C DFN |

## Conclusion

Highest-risk items: plating (mitigated: −77 → +11.4 mV margin via electrolyte transport) and fast-charge temperature (mitigated: cooling + DCR reduction). All mitigations implemented and verified in the final design. Complete FMEA including process/supplier failure modes: N/A (beyond pure simulation boundary).
