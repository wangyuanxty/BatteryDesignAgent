# DFMEA - Champion Cell R4-V3-margin (c1_t1_r1)
VBF-C1T1R1-DFMEA-001 | Virtual Battery Factory

S/O/D = severity/occurrence/detection engineering assessments (1-10 scale);
RPN = S x O x D. Mitigation and verification columns cite measured evidence where
available; no assessment below is a simulated value.

| Failure mode | Cause | Effect | S | O | D | RPN | Mitigation in design | Verification evidence |
|---|---|---|---|---|---|---|---|---|
| Lithium plating during 4C charge | anode-side concentration/kinetic polarization at 20 A | capacity loss, dendrite risk | 8 | 4 | 2 | 64 | transport kit (t+ 0.7, D_e 2e-9, kappa 3.0) + negative radius 3 um | anode potential min +0.0503 V (SPMe, 4C45C) |
| Cell overheat > 60 C during 4C | I2R + entropic heating at 20 A | degradation, safety margin loss | 7 | 3 | 2 | 42 | h=100 W/m2/K cooling; thin CCs cut resistance (DCR 0.147 mOhm) | 4C T_max 323.98 K |
| Thermal runaway under overcharge to 4.7 V | excessive overcharge reactions | fire/venting | 10 | 1 | 2 | 20 | 4.2 V cut-off system; low DCR limits overcharge current heating | run-tr: triggered=false, T_max 299.45 K |
| Electrolyte salt depletion at high current | low transference / diffusivity | concentration polarization -> plating | 6 | 2 | 3 | 36 | t+ 0.7, D_e 2e-9 m2/s margin kit | anode min stays positive at charge end |
| Re-plating from over-cooling | h too high slows kinetics | plating despite cooling | 6 | 2 | 2 | 24 | h capped at 100 (h=150 measured to re-plate: -0.0006 V) | R4-V4-coolmax negative control |
| Thin separator (8 um) mechanical failure | manufacturing defect, dendrite | internal short | 9 | 2 | 3 | 54 | porosity 0.55 keeps ionic path; plating suppression removes dendrite driver | plating-free evidence above; residual risk accepted with detection via QC (no sim evidence) |
| Thin current collectors (8/6 um) fatigue | tab weld stress | contact loss | 4 | 2 | 3 | 24 | standard Al/Cu foil practice at these gauges | residual risk documented (no sim evidence) |

Top residual risks: thin-separator mechanical integrity (RPN 54) and salt depletion
(RPN 36) - both mitigated but recommended for cell-level manufacturing validation.
