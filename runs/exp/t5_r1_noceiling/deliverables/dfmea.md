# Design FMEA (qualitative version, based on simulation signals) — VBF-T5R1NOCEILING-DFMEA-01

Cell: R4A MarginAnode1p0. Severity (S) and occurrence (O) are three-level qualitative ratings (high / medium / low) grounded in the magnitude of the simulated value vs threshold; RPN uses the simplified qualitative S x O matrix. Complete FMEA including process/supplier failures: N/A (beyond pure simulation boundary).

| Failure mode | Failure cause | Simulation signal (detectability basis) | S | O | Design-side mitigation |
|---|---|---|---|---|---|
| Lithium plating on negative electrode during 4C fast charge | empty-anode start-of-charge activation polarization drives anode surface potential below 0 V | anode_potential_v min +0.0212 V (DFN) — margin +21 mV above plating onset; SPMe +0.0270 V | high | low | implemented in design: area x1.5 current-density dilution, 1.0 um anode particles (active area x1.5), electrolyte transport overrides (sigma 2.0 S/m, t+ 0.45, D 4.5e-10 m2/s); validated fallback R4B (1.5 um anode, +0.0144 V) |
| Thermal runaway risk from excessive temperature rise | 4C charge heat generation exceeds cooling capacity | T_max 320.36 K vs 333.15 K limit — margin 12.8 K | high | low | implemented: h = 200 W/m2/K cooling, thin 220.8 um stack (low thermal mass) |
| Electrolyte oxidative decomposition at the charge ceiling | high cathode potential at 4.2 V vs electrolyte stability window | not quantified (true DFT skipped: real_compute = false, recorded in endorse entry); qualitative literature signal: standard EC:EMC LiPF6 stable to ~4.3 V vs Li/Li+ | medium | medium | charge ceiling fixed at 4.2 V (parameter-set upper cut-off, not relaxed) |
| Insufficient capacity / energy density | inactive-mass dilution or coating under-loading | ED 583.93 Wh/kg vs 500.94 floor — margin +16.6% | high | low | implemented: 95.3/107.5 um coatings, CC 6/4 um, separator 8 um |
| Current collector mechanical failure (manufacturing) | 6/4 um foils below common production gauge | no mechanical model (signal absent — flag only) | medium | medium (estimate) | flag for manufacturing review; 8/6 um alternative keeps ED at 549.2 (R3C, also fully passing) |
| Anode particle manufacturability / dispersion | 1.0 um primary-particle-scale radius | no process model (signal absent — flag only) | low | medium (estimate) | validated fallback R4B (1.5 um anode, +0.0144 V margin) |

## Conclusion

Highest-risk items are manufacturing-class (thin foils, 1.0 um anode particles) — both have validated fallbacks; every simulation-quantifiable risk (plating, temperature, ED shortfall) is mitigated to PASS with positive margin and its mitigation is already implemented in the selected design. Process/supplier-level FMEA is N/A (beyond pure simulation boundary).

