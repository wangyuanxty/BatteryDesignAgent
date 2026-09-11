# VBF-T9R4-DVPR-001 Design Verification Plan & Results

t9_r4 - grid-storage cell cathode on the Chen2020 NMC811/graphite profile
Result: HONEST NEGATIVE (no candidate satisfies the full contract; nothing reported as passing)

| # | Requirement | Method | Result | Verdict |
|---|---|---|---|---|
| 1 | avg voltage >= 4.6 V | run-comp x3 batches (42 layered) | max 4.6413 V (AlB55) | pass for AlB55 only |
| 2 | charging potential <= 4.8 V | gate_charging.py incremental profile | 7.410 V | FAIL (decisive) |
| 3 | catalogue/hull exclusion | comp_envelope_check.py --formula/--point | PASS (outside envelope) | pass |
| 4 | supported family | run-comp strict dispatch | layered LiMO2 | pass |
| 5 | ED >= 327.18 Wh/kg | run-pyamm 1C + calc-energy | not reached (no survivor) | n/a |
| 6 | no plating 4C/45C | run-pyamm 4C_charge_45C --plating | not reached | n/a |
| 7 | no TR trigger | run-tr | not reached | n/a |
| 8 | SEI <= 500 nm @100cyc | run-pyamm aging_1C_100cyc | not reached | n/a |
| 9 | true voltage >= 4.6 V | envelope re-compute + literature | 4.6354 V independent re-compute | informative |

Verification closure: the mechanical audit chain is complete (log.jsonl: entry 0 criteria,
plan, 4 propose rounds each with same-round evaluate entries, 4 funnels, final entry).
close-loop: run-comp replay (envelope --formula re-computation, 4.6354 V) + public-catalogue
search (no results for LiAl0.5B0.5O2 / LiAlO2 cathodes - 'not found in the searched scope').
run-qe not performed: no candidate survived to Stage 5 (Al/B pseudopotentials were added to
the QE map in preparation; recorded honestly).