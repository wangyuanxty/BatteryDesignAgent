# Design FMEA (qualitative version) — VBF-T6R1NOCEILING-DFMEA-01

Design under analysis: ED-Compact B-p (Chen2020 NMC811/graphite smartphone cell). Qualitative version, based on simulation signals (per deliverable-dfmea spec); severity/occurrence three-level qualitative ratings (H/M/L); RPN by simplified S×O matrix (qualitative caliber, annotated).

| # | Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|---|
| 1 | Lithium plating on negative electrode during 4C fast charge | Compaction (0.20 neg porosity, 85.2 µm, 4 µm particles) + baseline electrolyte transport cannot support 4C current | `cell/r2_bp_4c.json:anode_potential_v` min = −0.2566 V → plated (mechanical) | H (safety) | H (occurs at the advertised 4C) | Firmware charge derating (≤ 2C recommendation, qualitative); electrolyte transport upgrade or anode coating — excluded in-boundary (ceiling_escalation OFF), recorded |
| 2 | Temperature limit exceed at 4C/45 °C | Heat load at 4C vs hA ≤ 0.133 W/K (A = 0.00531 m² locked, h ≤ 25) | `cell/r2_bp_4c.json:T_max_K` = 351.0 K > 323.15 K; h = 25 family datum 338.7 K still > limit | M | H (at 4C/45 °C) | Larger cooling envelope (pouch hA ≥ ~1.5 W/K) — excluded in-boundary, recorded; charge derating; ambient derating |
| 3 | Voltage plateau shortfall vs 4.1 V spec | NMC811 cathode OCP ceiling ≈ 4.0 V (material property) | `cell/r2_bp_energy.json:midpoint_voltage_v` = 3.9214 V < 4.1 (best in-case 3.998 V) | L (spec compliance) | H (inherent to the system) | High-voltage cathode system (LNMO-class) — excluded in-boundary, recorded |
| 4 | Electrolyte oxidative decomposition | Upper voltage 4.2 V near NMC811 window edge | No HOMO/IE-EA data computed (real_compute = false — endorse skipped honestly); voltage window from parameter set only | M | L (≤ 4.2 V window, qualitative) | Keep charge cut-off at 4.2 V (parameter-set value); DFT HOMO verification recommended in a real-compute run |
| 5 | Insufficient capacity vs nominal | Nominal (5.6 Ah) set from loading estimate, measured 5.3222 Ah (−5%) | `cell/r2_bp_1c.json:capacity_ah` | L | L | Datasheet rating reconciliation (report measured 5.32 Ah) |
| 6 | Excessive SEI growth / aging | Local current density in compacted negative | `cell/r4_bp_aging.json:sei_thickness_nm_end` = 417.74 nm ≤ 500 nm (pass); capacity trajectory climb-then-saturate artifact annotated | L | L | Pass at 1C/25 °C; 45 °C aging verification recommended (protocol available, not run for this candidate) |
| 7 | Enclosure / tab / mechanical integrity failures | Outside simulation boundary | none | Not rated | Not rated | N/A (beyond pure-simulation boundary — complete FMEA incl. process/supplier failures N/A) |

## Conclusion

- Highest-risk items: #1 plating at 4C (S×O = H) and #2 thermal exceed at 4C/45 °C (M×H). Both are boundary-locked in this ablation (mitigation levers excluded: electrolyte formulation, coatings, cooling envelope redesign) — the honest in-boundary mitigation is charge derating, recorded in the datasheet fast-charge field.
- Mitigations implemented in the design itself: dead-layer thinning and compaction (ED objective), 4 µm negative particles (+0.022 V anode-potential margin, insufficient to clear 4C), SEI budget verified ≤ 500 nm.
- Complete FMEA (process/supplier failures): N/A (beyond pure simulation boundary).
