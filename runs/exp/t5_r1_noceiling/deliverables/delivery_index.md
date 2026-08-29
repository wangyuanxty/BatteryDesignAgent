# Delivery Index — VBF-T5R1NOCEILING-IDX-01

## Cover Information

- Case name: t5_r1_noceiling (next-generation flagship vehicle battery: energy density >= 500.94 Wh/kg, 4C fast charge without lithium plating, maximum temperature <= 60 degC; ablation: ceiling_escalation OFF)
- Numbering scheme: VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>; case ID with non-alphanumeric characters removed: T5R1NOCEILING; SEQ-NO is a two-digit serial under each document code starting from 01
- Generation date: 2026-08-25
- Signature block (left blank for manual signing): Prepared / Reviewed / Approved

## Document Code Reference Table (fixed by protocol)

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet technical parameter sheet | datasheet.md |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| CAD | Structure model | cell_model.stl (not produced — optional deliverable, requires user clarification; zero-interaction case) |

## File List

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T5R1NOCEILING-DS-01 | md | generated per references/deliverable-design-spec.md; values mechanically taken from parameter set + simulation outputs (cell/r4_A_*.json) |
| design_spec.pdf | VBF-T5R1NOCEILING-DS-01 | pdf | PDF release of design_spec.md (reportlab) |
| report.html | VBF-T5R1NOCEILING-DS-02 | html | bda render log.jsonl report (seven sections, self-contained) |
| bom.xlsx | VBF-T5R1NOCEILING-BOM-01 | xlsx | generated per references/deliverable-bom.md (openpyxl); masses from cell/r4_A_calc_dfn.json layer_kg_m2 x area; additive/binder/electrolyte literature defaults annotated as estimates |
| bom.pdf | VBF-T5R1NOCEILING-BOM-01 | pdf | PDF release of bom.xlsx (reportlab) |
| datasheet.md | VBF-T5R1NOCEILING-DSH-01 | md | generated per references/deliverable-datasheet.md; values from parameter set + simulation outputs |
| datasheet.pdf | VBF-T5R1NOCEILING-DSH-01 | pdf | PDF release of datasheet.md (reportlab) |
| calc.xlsx | VBF-T5R1NOCEILING-CALC-01 | xlsx | generated per references/deliverable-calc-sheet.md (openpyxl): inputs -> capacity/energy -> energy density -> N/P and mass -> process parameters |
| calc.pdf | VBF-T5R1NOCEILING-CALC-01 | pdf | PDF release of calc.xlsx (reportlab) |
| dvpr.md | VBF-T5R1NOCEILING-DVPR-01 | md | generated per references/deliverable-dvpr.md (virtual-test version); determinations mechanical vs entry-0 criteria |
| dvpr.pdf | VBF-T5R1NOCEILING-DVPR-01 | pdf | PDF release of dvpr.md (reportlab) |
| dfmea.md | VBF-T5R1NOCEILING-DFMEA-01 | md | generated per references/deliverable-dfmea.md (qualitative, simulation-signal based) |
| dfmea.pdf | VBF-T5R1NOCEILING-DFMEA-01 | pdf | PDF release of dfmea.md (reportlab) |
| delivery_index.md | VBF-T5R1NOCEILING-IDX-01 | md | this index (cover + controlled file list) |
| delivery_index.pdf | VBF-T5R1NOCEILING-IDX-01 | pdf | PDF release of delivery_index.md (reportlab, blueprint-style cover) |

