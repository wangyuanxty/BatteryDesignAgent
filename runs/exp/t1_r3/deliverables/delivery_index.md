# Delivery Package Index — t1_r3

**Document number**: VBF-EXPT1R3-IDX-01

## Cover Information

| Field | Value |
|---|---|
| Case name | t1_r3 (next-generation pure electric sedan battery: ED ≥ 392.61 Wh/kg, 4C fast charge without plating, T_max ≤ 60 °C, overcharge 4.7 V without thermal runaway) |
| Numbering scheme | `VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>`; case ID `exp/t1_r3` → `EXPT1R3` |
| Generation date | 2026-08-26 |
| Prepared by | (blank) |
| Reviewed by | (blank) |
| Approved by | (blank) |

## Document Code Reference

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | `design_spec.md` |
| BOM | Bill of Materials | `bom.xlsx` |
| DSH | Datasheet | `datasheet.md` |
| CALC | Calculation sheet | `calc.xlsx` |
| DVPR | Design verification report | `dvpr.md` |
| DFMEA | Failure analysis | `dfmea.md` |
| CAD | Structure model | not produced (optional; headless session — no user clarification requesting it; honestly skipped) |
| IDX | Delivery index | `delivery_index.md` |

## File List

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-EXPT1R3-DS-01 | md | generated per `references/deliverable-design-spec.md`; all values from parameter set + `r5_v11_*.json` outputs |
| design_spec.pdf | VBF-EXPT1R3-DS-01 | pdf | md→pdf release export via reportlab |
| report.html | VBF-EXPT1R3-DS-02 | html | `bda render --case-dir runs/exp/t1_r3` seven-section log report (ancillary to DS) |
| bom.xlsx | VBF-EXPT1R3-BOM-01 | xlsx | generated per `references/deliverable-bom.md` via openpyxl |
| bom.pdf | VBF-EXPT1R3-BOM-01 | pdf | xlsx→pdf release export via reportlab |
| datasheet.md | VBF-EXPT1R3-DSH-01 | md | generated per `references/deliverable-datasheet.md` |
| datasheet.pdf | VBF-EXPT1R3-DSH-01 | pdf | md→pdf release export via reportlab |
| calc.xlsx | VBF-EXPT1R3-CALC-01 | xlsx | generated per `references/deliverable-calc-sheet.md` via openpyxl (5 sheets) |
| calc.pdf | VBF-EXPT1R3-CALC-01 | pdf | xlsx→pdf release export via reportlab |
| dvpr.md | VBF-EXPT1R3-DVPR-01 | md | generated per `references/deliverable-dvpr.md` (virtual-test version) |
| dvpr.pdf | VBF-EXPT1R3-DVPR-01 | pdf | md→pdf release export via reportlab |
| dfmea.md | VBF-EXPT1R3-DFMEA-01 | md | generated per `references/deliverable-dfmea.md` (qualitative version) |
| dfmea.pdf | VBF-EXPT1R3-DFMEA-01 | pdf | md→pdf release export via reportlab |
| delivery_index.md | VBF-EXPT1R3-IDX-01 | md | this file (cover + controlled file list) |
| delivery_index.pdf | VBF-EXPT1R3-IDX-01 | pdf | md→pdf release export via reportlab (blueprint-style cover) |
