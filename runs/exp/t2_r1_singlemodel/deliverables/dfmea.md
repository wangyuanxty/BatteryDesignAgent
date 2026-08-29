# Design FMEA (qualitative, simulation-signal based) — VBF-T2R1SINGLEMODEL-DFMEA-01

> Qualitative version, based on simulation signals; severity/occurrence three-level (high/medium/low),
> basis = magnitude of the simulation value vs threshold. Generation date 2026-08-25.

| Failure mode | Failure cause | Simulation signal | Severity | Occurrence | Mitigation (design side) |
|---|---|---|---|---|---|
| Negative-electrode lithium plating (fast charge) | 4C reaction-zone crowding near separator | ap_min +0.112 V / +0.111 V (margin > 0) | high (if occurred) | low | Implemented: 250 um anode + neg i0 = 2.0 A/m2; conservative 25 C start verified |
| Thermal runaway from overcharge | heating in 4.7 V charge phase | DFN overcharge unsolved (IDA failure at 4.7 V phase — recorded); TR coupling not triggered at 322.7 K | medium | unknown | Physical overcharge test required; BMS voltage clamp (not simulated) |
| Thermal runaway from nail | internal short heat | triggered, T_max 408.4 K | high | medium | External short protection / thermal fuse (design-side, not simulated) |
| Electrolyte oxidative decomposition | voltage window vs HOMO | not assessed (funnel_voting OFF: xtb HOMO line unavailable; real_compute=false) | medium | unknown | Conservative 4.2 V cut-off retained |
| Insufficient capacity / energy density | thin electrodes / low utilization | ED 358.0 vs 327.18 Wh/kg (+30.8 margin) | medium | low | 100 um cathode retained; margin documented |
| Low-temperature performance loss | sluggish transport at 253.15 K | retention 99.59 % (>= 90 criterion) | medium | low | Verified at -20 C; below -20 C untested |
| SEI overgrowth | solvent diffusion through film | 194.6 nm @100 / 439.7 nm @500 vs 500/550 nm | medium | low | D_ec 8e-20 m2/s densified film (bridge extension, recorded as estimate) |

## Conclusion

Highest-risk items: overcharge TR (virtual test unresolved — physical test mandatory) and nail TR
(triggered in virtual test — protection measures required). Complete FMEA incl. process/supplier
failures: N/A (beyond pure simulation boundary).
