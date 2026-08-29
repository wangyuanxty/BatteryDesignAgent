# Delivery Index - Case T2R1NOCEILING

| # | VBF number | Deliverable | File | Status |
|---|---|---|---|---|
| 1 | VBF-T2R1NOCEILING-DS-001 | Design specification (best-effort design L, infeasibility evidence) | design_spec.md + pdf | Complete |
| 2 | VBF-T2R1NOCEILING-BOM-002 | Bill of materials (5-layer stack, masses) | bom.xlsx + pdf | Complete |
| 3 | VBF-T2R1NOCEILING-DSH-003 | Datasheet (cell-level specs, operating envelope) | datasheet.md + pdf | Complete |
| 4 | VBF-T2R1NOCEILING-CALC-004 | Energy-density calculation + full comparison | calc.xlsx + pdf | Complete |
| 5 | VBF-T2R1NOCEILING-DVPR-005 | Design verification plan & report (5 criteria, 14 designs) | dvpr.md + pdf | Complete |
| 6 | VBF-T2R1NOCEILING-DFMEA-006 | Design FMEA (7 failure modes, ranked) | dfmea.md + pdf | Complete |
| 7 | VBF-T2R1NOCEILING-IDX-007 | This index | delivery_index.md + pdf | Complete |
| 8 | VBF-T2R1NOCEILING-RPT-008 | HTML report (rendered from log.jsonl) | report.html | Complete |

Case summary: NEGATIVE RESULT. Best-effort design L passes energy density (476.72 Wh/kg),
SEI100 (467.6 nm) and lowT retention (0.9944); 4C plating (-0.3868 V vs >= 0) and SEI500
(811.3 nm vs <= 550) are infeasible in the admissible design space (14 designs, 10 lever axes,
4 rounds, all mechanically evaluated). real_compute = false: true DFT/MD endorsement skipped
(endorse entry in log.jsonl).
