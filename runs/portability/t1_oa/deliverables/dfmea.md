# Design FMEA (qualitative) — VBF-T1OA-DFMEA-01

> Qualitative version based on simulation signals; severity/occurrence = H/M/L three-level. Complete FMEA (process/supplier failures) is N/A beyond pure-simulation boundary.

| Failure mode | Failure cause | Simulation signal | Severity | Occurrence | Mitigation in design |
|---|---|---|---|---|---|
| Negative electrode lithium plating (fast charge) | anode surface potential < 0 V at 4C | `anode_potential_v` min | H | L (measured +0.0341 V margin) | SiOx anode OCP + nanostructured anode (0.8 µm) + high-transport electrolyte (σ 3.0, t⁺ 0.6) |
| Thermal runaway risk (temperature exceedance) | high-rate heat generation vs cooling | `T_max_K` 324.55 K vs 333.15 K | H | L (8.6 K margin) | liquid cooling h = 80 W/m²/K |
| Overcharge thermal runaway | overcharge to 4.7 V drives side reactions | `triggered` = false | H | L | high-voltage-stable design; verified via run-tr |
| Electrolyte oxidative decomposition (voltage window) | electrolyte oxidation above cutoff | HOMO/IE-EA not computed (real_compute=false) | M | M (not quantified) | advanced electrolyte formulation (estimate) |
| Insufficient capacity | cathode/anode capacity balance | 1C `capacity_ah` 5.057 vs 5.0 | L | L | N/P balance per parameter set |

## Conclusion

Highest-risk items (plating, thermal runaway, overcharge) are mitigated in the design and verified by simulation (all pass). The electrolyte oxidative-decomposition risk is not first-principles-quantified (true DFT skipped, real_compute=false) and is the primary residual uncertainty; the advanced electrolyte transport parameters are marked as estimates. Complete process/supplier FMEA is N/A (beyond pure-simulation boundary).
