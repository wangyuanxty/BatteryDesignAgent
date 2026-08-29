# Delivery Package Index — T4R1FLASH

| Field | Value |
|---|---|
| Case name | `t4_r1_flash` |
| Numbering scheme | `VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>` (case ID `t4_r1_flash` -> `T4R1FLASH`) |
| Generation date | 2026-08-25 |
| Prepared / Reviewed / Approved | ___ / ___ / ___ (blank for manual signing) |

## Document code reference table (fixed by protocol)

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet technical parameter sheet | datasheet.md |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| IDX | Delivery index | delivery_index.md |

## File list (actually generated — registered one row per file)

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T4R1FLASH-DS-01 | md | generated per deliverable-design-spec spec, from parameter set + simulation outputs |
| design_spec.pdf | VBF-T4R1FLASH-DS-02 | pdf | md -> pdf by reportlab (blueprint style) |
| report.html | VBF-T4R1FLASH-DS-03 | html | bda render audit report (ancillary to DS) |
| bom.xlsx | VBF-T4R1FLASH-BOM-01 | xlsx | generated per deliverable-bom spec, dual caliber g/cell + kg/kWh |
| bom.pdf | VBF-T4R1FLASH-BOM-02 | pdf | xlsx content -> pdf by reportlab |
| datasheet.md | VBF-T4R1FLASH-DSH-01 | md | generated per deliverable-datasheet spec |
| datasheet.pdf | VBF-T4R1FLASH-DSH-02 | pdf | md -> pdf by reportlab |
| calc.xlsx | VBF-T4R1FLASH-CALC-01 | xlsx | generated per deliverable-calc-sheet spec (5 sheets) |
| calc.pdf | VBF-T4R1FLASH-CALC-02 | pdf | xlsx content -> pdf by reportlab |
| dvpr.md | VBF-T4R1FLASH-DVPR-01 | md | virtual-test verification plan/report per deliverable-dvpr spec |
| dvpr.pdf | VBF-T4R1FLASH-DVPR-02 | pdf | md -> pdf by reportlab |
| dfmea.md | VBF-T4R1FLASH-DFMEA-01 | md | qualitative FMEA per deliverable-dfmea spec |
| dfmea.pdf | VBF-T4R1FLASH-DFMEA-02 | pdf | md -> pdf by reportlab |
| delivery_index.md | VBF-T4R1FLASH-IDX-01 | md | this index, per deliverable-package spec |
| delivery_index.pdf | VBF-T4R1FLASH-IDX-02 | pdf | md -> pdf by reportlab (blueprint cover) |

Note: CAD (cell_model.stl) not requested in this case (headless run, no structure-model clarification); honestly skipped per deliverable-cad-model spec.
