# DFMEA - t6_r1_singlemodel (G2_kappa0175)

**Document**: VBF-T6R1SINGLEMODEL-DFMEA-001

| Failure mode | Effect | S | O | D | RPN | Mitigation / status |
|---|---|---|---|---|---|---|
| Lithium plating at the 4C charge (the anode potential < 0) | the capacity loss, the dendrite risk | 9 | 3 | 2 | 54 | DESIGNED OUT: the early-trip razor trips the 4.7 V limit at t_ch ~65 s with the anode surface potential min +0.0454 V (the 45 mV margin). The residual risk: the margin is thin by the production-tolerance standards - the BMS must enforce the 4.7 V cutoff strictly. |
| Thermal over-limit (the T > 323.15 K) | the degradation acceleration | 7 | 2 | 2 | 28 | MITIGATED: the h 400.0 W/m2.K cooling holds the 4C T_max at 321.442 K (the 1.71 K margin). |
| SEI growth > 500 nm | the capacity fade | 6 | 2 | 2 | 24 | MITIGATED: the suppressed SEI kinetics (1e-13 m/s) -> 133.56 nm after the 100 cycles (the 366 nm margin). |
| Voltage plateau < 4.1 V | the device incompatibility | 6 | 2 | 2 | 24 | MITIGATED: the midpoint 4.2078 V (the 0.108 V margin). |
| The charge-end state ambiguity (the cathode kinetic saturation discharge) | the under-utilization of the anode | 3 | 5 | 2 | 30 | ACCEPTED (the honest consequence): the discharge ends at the 0.73 x Q_c cathode-saturation point. |
| The 4C fill ~1.3% | the user-facing fast-charge expectation | 4 | 5 | 3 | 60 | ACCEPTED + DISCLOSED: the voltage-limited 4C charge delivers ~0.07 Ah; the datasheet states it explicitly. |
