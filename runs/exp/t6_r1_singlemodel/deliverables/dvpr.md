# Design Verification Plan & Results - t6_r1_singlemodel

**Document**: VBF-T6R1SINGLEMODEL-DVPR-001 | the final candidate G2_kappa0175 (the round 10)

| ID | Requirement | Method / protocol | Result | Verdict |
|---|---|---|---|---|
| DV-1 | Volumetric ED >= 950 Wh/L | the calc-energy on the 1C SPMe | 1107.02 Wh/L | PASS |
| DV-2 | Voltage plateau >= 4.1 V | the 1C discharge midpoint | 4.2078 V | PASS |
| DV-3 | SEI <= 500 nm after 100 cycles | the aging_1C_100cyc SPMe | 133.56 nm | PASS |
| DV-4 | No lithium plating at the 4C charge | the 4C_charge_45C (the anode surface potential, the whole protocol) | min +0.0454 V | PASS |
| DV-5 | T_max <= 50 degC (323.15 K) at the 4C charge | the 4C_charge_45C (the lumped thermal) | 321.442 K | PASS |
| DV-6 | Stage-1 molecular line (the mace energy <= 0) | the Stage 2 run-mlp screening (the funnel_voting OFF) | the elimination line applied | PASS |
| DV-7 | DFN cross-check of the final candidate | the 4C DFN (the run-pyamm --mode dfn) | see the datasheet note | PASS |

The verification chain: the rounds R1-R10 (the 10 propose rounds, each with the same-round
evaluate; the R7-R10 notes carry the full mechanism-resolution history - the cathode-kinetic
discharge cutoff, the unreachable clean trip, the anode-saturation plunge, the dead dip trip,
the surviving early-trip razor).
