# Design Verification Plan & Report (virtual tests) — VBF-T3R1-DVPR-001

All tests executed with the bda simulation library, DFN mode, Chen2020 base parameters + design
overrides (cell/p_v12.json). Verdicts are mechanical (bda log-evaluate, round 4).

| # | Test item | Requirement | Method / protocol | Result | Verdict | Evidence |
|---|---|---|---|---|---|---|
| 1 | Nominal capacity | >= 2.0 Ah | 1C_discharge, DFN | 3.075 Ah | PASS | cell/r4_v12_1c.json:capacity_ah |
| 2 | 5C capacity retention | >= 0.95 | 5C_discharge DFN / 1C_discharge DFN | 0.97532 | PASS | cell/r4_v12_derived.json:retention_5c |
| 3 | Fast-charge plating | False (no plating) | 4C_charge_45C, DFN, --plating | anode min +12.1 mV (>0) | PASS | cell/r4_v12_4c.json:anode_potential_v |
| 4 | Max temperature | <= 333.15 K | 4C_charge_45C, DFN, --thermal lumped | 329.77 K (56.62 C) | PASS | cell/r4_v12_derived.json:T_max_K |
| 5 | Power density | >= 4000.0 W/kg | calc-energy contract formula | 32630 W/kg | PASS | cell/r4_v12_energy.json:power_density_w_kg |

## Iteration history (log.jsonl)

| Round | Candidates | Outcome |
|---|---|---|
| 1 | Baseline (Chen2020 defaults) | FAIL: retention 0.0874, T_max 354.29 K, plated — power density/capacity OK. Failures are transport/architecture-scale -> Stage-3 fallback. |
| 2 | V1-V6 single levers + combo | V6_ComboCeiling first full pass (retention 0.9782, T 324.91 K, no plating); Q_nom understated C-rates by ~15% (lesson recorded). |
| 3 | V7-V11 refinements | Attribution: thicker anode insufficient (V7 retention fail), porosity boost load-bearing (V10 plated), moderate electrolyte erodes plating margin (V9 +0.6 mV), h-trade mapped (V8/V11). |
| 4 | V12_BalancedCooling (h=20) | PASS 5/5 with balanced margins (3.38 K thermal, +12.1 mV plating) — final selection. |

## Notes

- Stage-5 true DFT/MD endorsement skipped: real_compute=false (entry-0 meta); endorse entry records the skip.
- Aging/cycle-life not in task criteria; not tested (aging protocol available for follow-up).
