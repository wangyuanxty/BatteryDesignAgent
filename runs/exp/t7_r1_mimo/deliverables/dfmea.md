# Design FMEA — V_K HEV Battery Cell

**Case**: HEV Battery Design - V_K Extreme Transport
**Document Number**: VBF-T7R1MIMO-DFMEA-01
**Date**: 2026-08-31

---

## Failure Mode and Effects Analysis

| # | Failure Mode | Potential Effect | Potential Cause | Current Design Control | Severity (S) | Occurrence (O) | Detection (D) | RPN | Action |
|---|-------------|-----------------|----------------|----------------------|-------------|---------------|--------------|-----|--------|
| 1 | Lithium plating at 4C | Internal short circuit, capacity fade, safety hazard | Insufficient Li⁺ transport at high rate | High porosity (0.45), thin separator (8µm), small particles (3µm); DFN verified anode_potential > 0V | 9 | 2 | 3 | 54 | Monitor anode potential in production QC |
| 2 | Excessive SEI growth at elevated temperature | Capacity fade, increased impedance | High temperature accelerates SEI formation kinetics | Chen2020 SEI model verified at 45°C: 536 nm < 550 nm limit | 6 | 3 | 4 | 72 | Consider FEC additive for wider margin |
| 3 | Thermal runaway on nail penetration | Cell fire, propagation to adjacent cells | Internal short from nail, exothermic reactions | Verified: no TR at 10W heat input (hA=0.5); cell mass provides thermal buffer | 10 | 1 | 3 | 30 | Maintain separator integrity in production |
| 4 | Overcharge-induced thermal event | Cell swelling, venting, potential fire | Charging above voltage cutoff | Verified: T_max=34°C at +0.5V overcharge; BMS voltage cutoff required | 9 | 1 | 2 | 18 | BMS overvoltage protection mandatory |
| 5 | High porosity reduces mechanical strength | Electrode delamination, particle disconnection | Porosity 0.45 exceeds standard 0.33 | Not tested in simulation (outside scope); production validation needed | 7 | 3 | 5 | 105 | Mechanical testing recommended |
| 6 | Thin separator (8µm) reduces puncture resistance | Internal short from dendrite or manufacturing defect | Separator thinner than standard 25µm | Ceramic coating recommended; not modeled in simulation | 9 | 2 | 4 | 72 | Ceramic-coated separator required |
| 7 | Numerical instability in thermal runaway model | False positive safety assessment | ODE solver instability at low hA | Sensitivity analysis shows hA>0.1 gives stable results | 5 | 2 | 2 | 20 | Use hA≥0.5 for nail penetration modeling |

**RPN Scale**: Severity (1-10) × Occurrence (1-10) × Detection (1-10). RPN > 100 requires action.

**Highest RPN items**: #5 (RPN=105, mechanical strength at high porosity) — requires physical testing validation.

**Design risk summary**: The V_K design achieves all simulated performance targets but introduces manufacturing risks from high porosity and thin separator. These are identified as areas requiring physical prototype validation.
