# Design FMEA (qualitative, simulation-signal based) — VBF-T6LC-DFMEA-01

Qualitative version based on simulation signals; complete process/supplier FMEA is N/A (beyond pure-simulation boundary).

| Failure mode | Failure cause | Simulation signal (detectability) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Negative-electrode lithium plating (fast charge) | anode potential < 0 V at 4C | `anode_potential_v` min +0.0894 V (margin 0.089 V) | High | Low | N/P raised to 1.68 (110 µm anode) |
| Thermal runaway risk (temperature over limit) | 4C heat generation exceeds cooling | `T_max_K` 322.59 K vs 323.15 K (margin 0.56 K) | High | Low | cooling h = 45 W/m²/K |
| Electrolyte oxidative decomposition (voltage window) | 4.7 V upper cut-off | not directly simulated (true DFT endorsement skipped, real_compute=false) | Medium | Medium | high-voltage electrolyte/additive validation recommended before production |
| Insufficient capacity / energy density | thin electrodes / high overhead | ED 1005.8 Wh/L vs 950 (margin 5.9%) | Medium | Low | thin separator/CC reclaim volume |
| Excessive SEI growth | high 4.7 V charge drives anode SEI | SEI 233 nm (SPMe) vs 500 nm | Medium | Low | anode coating k_SEI = 1e-15 m/s |

## Conclusion

Highest-risk item: electrolyte oxidative decomposition at 4.7 V (unverified in this virtual run — true DFT endorsement skipped). Mitigations implemented for plating, temperature, and SEI; the complete process/supplier FMEA is annotated N/A.
