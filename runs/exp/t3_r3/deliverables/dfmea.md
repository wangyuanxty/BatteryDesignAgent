# Design FMEA - Power-Tool Battery (case t3_r3)

> VBF-T3R3-DFMEA-01. Qualitative version, based on simulation risk signals (annotated caliber). Severity/occurrence: three-level high/medium/low; basis = magnitude of simulation value vs threshold. No numbers from memory.

| Failure mode | Failure cause | Simulation signal (detection basis) | Severity | Occurrence | Design-side mitigation |
|------|------|------|------|------|------|
| Negative electrode lithium plating (4C fast charge) | anode polarization during high-rate charge | anode min +41.7 mV vs 0 V (margin engineered upward 21 -> 41.7 mV across rounds) | high | low | N/P x1.3 negative margin; 1.0 um fine anode particles; D 8e-10 m2/s + t+ 0.35 transport; margin monitoring kept as charge-window gate |
| Thermal excursion (exceeds 60 C) | resistive heating at 5C/4C rates | T_max 329.75 K (56.60 C) vs 333.15 K (3.4 K margin at 4C; 5C margin 13.6 K) | medium | low | h = 25 W/m2/K thermal design requirement; temperature sensors + BMS charge/discharge derating |
| Electrolyte oxidative decomposition | high upper cut-off voltage vs electrolyte stability | voltage window 2.5-4.2 V; real_compute=false: no DFT stability endorsement this case (skip recorded in endorse entry) | medium | low | NMC811 4.2 V practice from literature; additive strategy available as Stage-2 path (not exercised; architecture solved the criteria) |
| Insufficient capacity | loading reduction inherent to power architecture | 1C capacity 4.3176 Ah vs >= 2.0 Ah (2.2x margin) | low | low | margin verified at DFN judge grade; no action |
| Reduced 4C charge acceptance (functional, not safety) | 4.2 V ceiling reached before full charge at 4C | CC acceptance 0.811 Ah before cutoff (effective ~4.6C vs 5 Ah nominal) | low | high | CV phase at ceiling; pack-level nominal sizing; documented as honest residual in final entry |

## Conclusion

Highest-risk item: plating (severity high) - mitigated in design (occurrence low) via N/P margin + electrode kinetics + transport; second: thermal (3.4 K margin at 4C). Mitigations are implemented in the champion design. Complete FMEA including process/supplier failure modes: N/A (beyond pure simulation boundary).
