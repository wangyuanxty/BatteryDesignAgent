# Delivery Package Index

- Case name: t4_r1_noforce (extreme-cold equipment battery, virtual battery factory)
- Numbering scheme: VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO> (case id uppercase, non-alphanumeric removed: t4_r1_noforce -> T4R1NOFORCE; SEQ-NO two-digit per doc code from 01)
- Generation date: 2026-08-25
- Prepared: ______   Reviewed: ______   Approved: ______

## Document code reference (protocol-fixed)

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet | datasheet.md |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| IDX | Delivery index | delivery_index.md |
| CAD | Structure model | not requested this case — skipped |

## File list

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T4R1NOFORCE-DS-01 | md | generated per deliverable-design-spec; values from Chen2020 set + params_r6_v10a_h45.json + round-6 tool outputs |
| design_spec.pdf | VBF-T4R1NOFORCE-DS-01 | pdf | PDF release of design_spec.md (reportlab) |
| report.html | VBF-T4R1NOFORCE-DS-02 | html | bda render of log.jsonl (ancillary to DS) |
| bom.xlsx | VBF-T4R1NOFORCE-BOM-01 | xlsx | generated per deliverable-bom (openpyxl); layer masses from r6_final_energy_dfn.json, additive/binder literature defaults annotated |
| bom.pdf | VBF-T4R1NOFORCE-BOM-01 | pdf | PDF release of bom.xlsx (reportlab) |
| datasheet.md | VBF-T4R1NOFORCE-DSH-01 | md | generated per deliverable-datasheet |
| datasheet.pdf | VBF-T4R1NOFORCE-DSH-01 | pdf | PDF release of datasheet.md (reportlab) |
| calc.xlsx | VBF-T4R1NOFORCE-CALC-01 | xlsx | generated per deliverable-calc-sheet (openpyxl): input parameters -> capacity/energy -> energy density -> N/P and mass -> process parameters |
| calc.pdf | VBF-T4R1NOFORCE-CALC-01 | pdf | PDF release of calc.xlsx (reportlab) |
| dvpr.md | VBF-T4R1NOFORCE-DVPR-01 | md | generated per deliverable-dvpr (virtual test version) |
| dvpr.pdf | VBF-T4R1NOFORCE-DVPR-01 | pdf | PDF release of dvpr.md (reportlab) |
| dfmea.md | VBF-T4R1NOFORCE-DFMEA-01 | md | generated per deliverable-dfmea (qualitative version) |
| dfmea.pdf | VBF-T4R1NOFORCE-DFMEA-01 | pdf | PDF release of dfmea.md (reportlab) |
| delivery_index.md | VBF-T4R1NOFORCE-IDX-01 | md | this file |
| delivery_index.pdf | VBF-T4R1NOFORCE-IDX-01 | pdf | PDF release of this file (reportlab, blueprint style) |
