# Design FMEA (qualitative version) — t1_r1_noforce (C7)

VBF-T1R1NOFORCE-DFMEA-01 · Generation date: 2026-08-25 · Qualitative ratings based on simulation signals; severity/occurrence three-level (high/medium/low); RPN = simplified S×O matrix (qualitative caliber). Complete process/supplier FMEA: N/A (beyond pure simulation boundary).

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Negative-electrode lithium plating during 4C fast charge | anode surface potential < 0 V at end of CC charge (high anode x ≈ 0.7+ at cutoff) | `anode_potential_v` min = +0.00824 V (SPMe) / +0.00515 V (DFN) — margin positive but thin | High | Medium (thin 5 mV DFN margin) | Fine graphite anode (0.8 µm, kinetic cut); charge terminates in safe anode window; recommend prototype 4C validation and CV-limited charging control |
| Thermal runaway from 4.7 V overcharge | side-reaction self-heating at overcharge | overcharge 0.5C to 4.7 V: T_max 298.22 K, triggered=false, dT/dt max −8.6e-7 K/s | High | Low | BMS overcharge protection with hard cut at 4.7 V; double-face liquid cooling removes heat |
| Excessive temperature at 45 °C 4C charge | heat generation vs cooling capacity | T_max 318.79 K vs 333.15 K limit (margin 14.4 K) | Medium | Low | Pouch double-face cold-plate cooling (h 25 W/m²K, A 0.2054 m²) |
| Insufficient capacity / energy | electrode utilization, anode-limited inventory | 1C 5.654 Ah; ED 457.93 Wh/kg vs 392.61 (margin +65.3) | Medium | Low | Anode 95 µm restores inventory (R4); single-crystal 1.2 µm cathode utilization |
| Electrolyte oxidative decomposition near 4.7 V | solvent oxidation at high voltage | benign overcharge thermal response (no exotherm in 4.7 V protocol); molecular HOMO/IE-EA endorsement skipped (real_compute=false) | Medium | Medium (unverified molecular caliber) | Oxidation-resistant additive screening as future work (outside virtual scope, stated honestly) |
| Particle fracture / cracking of fine anode (0.8 µm) and single-crystal cathode | volume change cycling | no cracking model in Chen2020 — no simulation signal | Medium | Medium (unverified) | Single-crystal cathode practice; prototype cycling validation recommended |

## Conclusion

Highest-risk item: lithium plating margin (+5 mV DFN) — mitigation already implemented in design (anode kinetics + charge-window balance) with prototype validation recommended. Overcharge thermal runaway shows no trigger signal in the virtual model. Items without simulation signals are marked honestly as unverified rather than assumed safe.
