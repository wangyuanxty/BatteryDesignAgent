# Delivery Package Index - Power-Tool Battery (case t3_r3)

> VBF-T3R3-IDX-01. Cover + controlled list of all deliverables generated for this case. The index registers only actually generated files.

## Cover Information

- **Case name**: t3_r3 - power-tool battery (nominal capacity >= 2 Ah, 5C retention >= 95%, 4C fast charge without plating, T_max <= 60 C, power density >= 4000 W/kg)
- **Numbering scheme**: VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>; case ID t3_r3 -> T3R3 (non-alphanumeric removed)
- **Generation date**: 2026-08-26
- **Signature block**: Prepared ______ / Reviewed ______ / Approved ______ (left blank for manual signing)

## Document Code Reference (fixed by protocol)

| Document code | Meaning | Corresponding file |
|------|------|------|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet technical parameter sheet | datasheet.docx |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| CAD | Structure model | cell_model.stl (not generated: no 3D structure model requested this case) |

## File List

| File name | Number | Format | Source description |
|------|------|------|------|
| design_spec.md | VBF-T3R3-DS-01 | md | Cell design specification generated per deliverable-design-spec format (build script, values from tool outputs) |
| design_spec.pdf | VBF-T3R3-DS-01 | pdf | PDF release of design_spec.md, rendered with reportlab |
| report.html | VBF-T3R3-DS-02 | html | Case report deterministically rendered from log.jsonl (bda render --case-dir runs/exp/t3_r3); belongs to DS |
| bom.xlsx | VBF-T3R3-BOM-01 | xlsx | Bill of Materials, dual caliber g/cell and kg/kWh (openpyxl; formulas and sources per row) |
| bom.pdf | VBF-T3R3-BOM-01 | pdf | PDF release of bom.xlsx, sheets rendered with reportlab |
| datasheet.docx | VBF-T3R3-DSH-01 | docx | Customer-facing technical datasheet (python-docx; per-line sources) |
| datasheet.pdf | VBF-T3R3-DSH-01 | pdf | PDF release of datasheet.docx, rendered with reportlab |
| calc.xlsx | VBF-T3R3-CALC-01 | xlsx | Design calculation sheet: inputs -> capacity and energy -> energy density -> N/P and mass -> process parameters (openpyxl) |
| calc.pdf | VBF-T3R3-CALC-01 | pdf | PDF release of calc.xlsx, sheets rendered with reportlab |
| dvpr.md | VBF-T3R3-DVPR-01 | md | Design Verification Plan and Report, virtual test version (simulation protocols) |
| dvpr.pdf | VBF-T3R3-DVPR-01 | pdf | PDF release of dvpr.md, rendered with reportlab |
| dfmea.md | VBF-T3R3-DFMEA-01 | md | Design FMEA, qualitative version based on simulation risk signals |
| dfmea.pdf | VBF-T3R3-DFMEA-01 | pdf | PDF release of dfmea.md, rendered with reportlab |
| delivery_index.md | VBF-T3R3-IDX-01 | md | Delivery package index: cover + controlled file list (this file) |
| delivery_index.pdf | VBF-T3R3-IDX-01 | pdf | PDF release of delivery_index.md, reportlab with blueprint colors |
