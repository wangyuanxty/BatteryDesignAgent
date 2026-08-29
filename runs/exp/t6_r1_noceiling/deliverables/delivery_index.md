# Delivery Package Index — VBF-T6R1NOCEILING-IDX-01

## Cover

| Field | Value |
|---|---|
| Case name | `exp/t6_r1_noceiling` (smartphone cell; ablation: ceiling_escalation OFF) |
| Numbering scheme | `VBF-T6R1NOCEILING-<DOC-CODE>-<SEQ-NO>` |
| Generation date | 2026-08-25 |
| Prepared | (blank — for manual signing) |
| Reviewed | (blank — for manual signing) |
| Approved | (blank — for manual signing) |

## Document code reference (fixed by protocol)

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | `design_spec.md` |
| BOM | Bill of Materials | `bom.xlsx` |
| DSH | Datasheet technical parameter sheet | `datasheet.docx` |
| CALC | Calculation sheet | `calc.xlsx` |
| DVPR | Design verification report | `dvpr.md` |
| DFMEA | Failure analysis | `dfmea.md` |
| CAD | Structure model | `cell_model.stl` (not generated — see note) |

## File list (actually generated files only)

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T6R1NOCEILING-DS-01 | md | design_spec.md generated per the deliverable-design-spec spec |
| design_spec.pdf | VBF-T6R1NOCEILING-DS-01 | pdf | md→pdf exported by reportlab one-off script |
| report.html | VBF-T6R1NOCEILING-DS-02 | html | `bda render --case-dir runs/exp/t6_r1_noceiling` (ancillary case report under DS) |
| bom.xlsx | VBF-T6R1NOCEILING-BOM-01 | xlsx | bom.xlsx generated per the deliverable-bom spec (openpyxl) |
| bom.pdf | VBF-T6R1NOCEILING-BOM-01 | pdf | xlsx→pdf exported by openpyxl/reportlab |
| datasheet.docx | VBF-T6R1NOCEILING-DSH-01 | docx | datasheet.docx generated per the deliverable-datasheet spec (python-docx) |
| datasheet.pdf | VBF-T6R1NOCEILING-DSH-01 | pdf | docx→pdf exported by reportlab |
| calc.xlsx | VBF-T6R1NOCEILING-CALC-01 | xlsx | calc.xlsx generated per the deliverable-calc-sheet spec (openpyxl, 5-sheet chain) |
| calc.pdf | VBF-T6R1NOCEILING-CALC-01 | pdf | xlsx→pdf exported by openpyxl/reportlab |
| dvpr.md | VBF-T6R1NOCEILING-DVPR-01 | md | dvpr.md generated per the deliverable-dvpr spec |
| dvpr.pdf | VBF-T6R1NOCEILING-DVPR-01 | pdf | md→pdf exported by reportlab one-off script |
| dfmea.md | VBF-T6R1NOCEILING-DFMEA-01 | md | dfmea.md generated per the deliverable-dfmea spec |
| dfmea.pdf | VBF-T6R1NOCEILING-DFMEA-01 | pdf | md→pdf exported by reportlab one-off script |
| delivery_index.md | VBF-T6R1NOCEILING-IDX-01 | md | closing package index per the deliverable-package spec |
| delivery_index.pdf | VBF-T6R1NOCEILING-IDX-01 | pdf | md→pdf exported by reportlab one-off script (cover + identical inner file list) |

## Notes

- CAD structure model (`cell_model.stl`): not generated — optional deliverable per SKILL.md Step 7; the task did not request a 3D structure model. Recorded skip.
- The four log-evaluate batch-input files live at `cell/batch/r*_batch.json` (moved from `cell/` so the case-report loader sees curve outputs only; the log entries reference candidate names and evidence outputs, not batch paths — audit chain unaffected).
- All conclusion-grade numbers in the package trace to log.jsonl (27 entries: entry 0 criteria, plan, funnel, R1–R4 propose + evaluate, comparison, plan-update, endorse-skip, final with escalation) and to the `cell/*.json` tool output files.
