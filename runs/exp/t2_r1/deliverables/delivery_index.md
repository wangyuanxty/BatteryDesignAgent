# Delivery Package Index — t2_r1

## Cover information

| Field | Value |
|---|---|
| Case name | `t2_r1` — grid energy storage battery design (ED ≥ 327.18 Wh/kg; 4C no plating; SEI ≤ 500/550 nm @100/500 cyc; −20 °C ≥ 90%) |
| Numbering scheme | `VBF-T2R1-<DOC-CODE>-<SEQ-NO>` |
| Generation date | 2026-08-25 |
| Prepared | ____________ |
| Reviewed | ____________ |
| Approved | ____________ |

## Document code reference (protocol-fixed)

| Code | Meaning | File |
|---|---|---|
| DS | Specification | `design_spec.md` |
| BOM | Bill of Materials | `bom.xlsx` |
| DSH | Datasheet | `datasheet.docx` |
| CALC | Calculation sheet | `calc.xlsx` |
| DVPR | Design verification report | `dvpr.md` |
| DFMEA | Failure analysis | `dfmea.md` |
| IDX | Delivery index | `delivery_index.md` |

## File list

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T2R1-DS-01 | md | Generated per deliverable-design-spec spec; values mechanically from Chen2020 dump + sim outputs |
| design_spec.pdf | VBF-T2R1-DS-01 | pdf | PDF release, md → reportlab (blueprint style) |
| report.html | VBF-T2R1-DS-02 | html | `bda render` self-contained report (ancillary, belongs to DS) |
| bom.xlsx | VBF-T2R1-BOM-01 | xlsx | Generated per deliverable-bom spec (openpyxl); dual caliber g/cell + kg/kWh |
| bom.pdf | VBF-T2R1-BOM-01 | pdf | PDF release, xlsx → reportlab table export |
| datasheet.docx | VBF-T2R1-DSH-01 | docx | Generated per deliverable-datasheet spec (python-docx) |
| datasheet.pdf | VBF-T2R1-DSH-01 | pdf | PDF release, docx content → reportlab |
| calc.xlsx | VBF-T2R1-CALC-01 | xlsx | Generated per deliverable-calc-sheet spec (openpyxl); 5 sheets, formula + source columns |
| calc.pdf | VBF-T2R1-CALC-01 | pdf | PDF release, xlsx → reportlab table export |
| dvpr.md | VBF-T2R1-DVPR-01 | md | Virtual-test verification report (simulation values, mechanical) |
| dvpr.pdf | VBF-T2R1-DVPR-01 | pdf | PDF release, md → reportlab |
| dfmea.md | VBF-T2R1-DFMEA-01 | md | Qualitative design FMEA (simulation-signal based) |
| dfmea.pdf | VBF-T2R1-DFMEA-01 | pdf | PDF release, md → reportlab |
| delivery_index.md | VBF-T2R1-IDX-01 | md | This index |
| delivery_index.pdf | VBF-T2R1-IDX-01 | pdf | PDF release, md → reportlab |

## Notes

- CAD structure model: not produced — the structure model is an optional deliverable decided by user clarification, and was not requested in this task; recorded honestly rather than fabricated.
- All values in all files are mechanically sourced (parameter-set dump, simulation output JSONs, bridge JSONs, or annotated literature defaults); per-line source columns included.
- `report.html` lives in the workspace root (`runs/exp/t2_r1/report.html`), all other files in `runs/exp/t2_r1/deliverables/`.
