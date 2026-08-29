# Design Verification Plan & Report - Case T2R1NOCEILING

Plan and mechanical results of every protocol run for the selected design L and the round sweep.
All results from tool outputs (cell/*.json) and log-evaluate entries.

## Verification matrix

| # | Criterion | Protocol (bda run-pyamm) | Output file (L) | Measured | Threshold | Verdict |
|---|---|---|---|---|---|---|
| 1 | Energy density | 1C_discharge + calc-energy | cell/r4_L_1c_spme.json + cell/r4_L_energy.json | 476.72 Wh/kg | >= 327.18 | PASS |
| 2 | 4C no plating | 4C_charge_45C --plating | cell/r4_L_4c45.json | anode min -0.3868 V | >= 0 V | FAIL |
| 3 | SEI 100 cyc | aging_1C_100cyc | cell/r4_L_aging100.json | 467.6 nm | <= 500 | PASS |
| 4 | lowT retention | lowT_discharge vs 1C ref | cell/r4_L_lowT.json / r4_L_1c_spme.json | 0.9944 | >= 0.90 | PASS |
| 5 | SEI 500 cyc | aging_1C_100cyc --cycles 500 | cell/r4_L_aging500.json | 811.3 nm | <= 550 | FAIL |

## Sweep coverage (14 designs, all mechanically evaluated)

Rounds: R1 baseline; R2 current collectors / electrolyte transport up / anode particle size /
electrode loading; R3 anode thickness (N/P dose-response) / separator; R4 thermal cooling /
cathode particle size / electrolyte transport down / anode porosity. Every propose round has a
same-round log-evaluate entry (verify-deliverables audit-chain check PASS).

## Per-criterion commentary

- ED: passes for 13/14 designs (327.18+); K fails (238.2, transport-down cell collapse).
- 4C plating: fails for 13/13 non-degenerate designs; best -0.3868 V (L). K's mechanical pass is
  an artifact (nominal collapse -> 4C = 4.64 A = 45 A/m2; charge never reached 4.2 V within the
  experiment window) and K fails ED anyway.
- SEI100: passes for 13/14; H fails (540.0, thick-anode direction).
- SEI500: fails for 13/13 non-degenerate designs (771.4..979.9); K's 68.0 nm is an artifact of
  the crippled cell barely cycling.
- lowT: passes for all 14 (0.9919..1.0000).

## Protocol honesty notes

- lowT_discharge: ambient 253.15 K with lumped thermal from 25 C initial (tool definition);
  T_max 298.15 K in all runs = initial temperature.
- Aging: isothermal 25 C (task text says "1C cycling" without temperature; 25 C standard used,
  protocol default).
- PyBaMM per-cycle "Discharge capacity [A.h]" is the net integral; capacity-trajectory climb is
  an artifact (lithium loss shifts the voltage window) - SEI thickness is the direct criterion.
- calc-energy: contract formula, electrolyte excluded (parameter set lacks density).

## Conclusion

3/5 criteria PASS (ED, SEI100, lowT). 4C-plating and SEI500 FAIL for every design in the
admissible space - negative result, documented with the full sweep as evidence.
