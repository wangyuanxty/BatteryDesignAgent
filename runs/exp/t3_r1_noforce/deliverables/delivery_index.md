# Delivery Package Index — Power-Tool Battery Cell Design

**Case name**: `exp/t3_r1_noforce` — power-tool battery cell (nominal capacity ≥ 2 Ah, 5C discharge retention ≥ 95 %, 4C fast charge without plating, T_max ≤ 60 °C, power density ≥ 4000 W/kg)
**Numbering scheme**: `VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>` (case ID `t3_r1_noforce` → `T3R1NOFORCE`)
**Generation date**: 2026-08-25
**Signature block**: Prepared: ________ / Reviewed: ________ / Approved: ________

## Document code reference table

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet technical parameter sheet | datasheet.docx |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| IDX | Delivery package index (this file; package cover per verify-deliverables code table) | delivery_index.md |
| CAD | Structure model (optional; not requested in this task → not generated, not registered) | — |

## File list (only actually generated files)

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T3R1NOFORCE-DS-01 | md | generated per the deliverable-design-spec spec; values from params_v8.json + Chen2020 base parameter set + simulation outputs |
| design_spec.pdf | VBF-T3R1NOFORCE-DS-01 | pdf | md → pdf release version (reportlab) |
| report.html | VBF-T3R1NOFORCE-DS-02 | html | `bda render` from log.jsonl — seven-section audit report, ancillary to the specification |
| bom.xlsx | VBF-T3R1NOFORCE-BOM-01 | xlsx | openpyxl; component masses from parameter-set densities/volume fractions + literature defaults (annotated) |
| bom.pdf | VBF-T3R1NOFORCE-BOM-01 | pdf | xlsx → pdf release version (reportlab) |
| datasheet.docx | VBF-T3R1NOFORCE-DSH-01 | docx | python-docx per the deliverable-datasheet spec; values from simulation outputs |
| datasheet.pdf | VBF-T3R1NOFORCE-DSH-01 | pdf | docx → pdf release version (reportlab) |
| calc.xlsx | VBF-T3R1NOFORCE-CALC-01 | xlsx | openpyxl per the deliverable-calc-sheet spec (inputs → capacity/energy → energy density → N/P & mass → process) |
| calc.pdf | VBF-T3R1NOFORCE-CALC-01 | pdf | xlsx → pdf release version (reportlab) |
| dvpr.md | VBF-T3R1NOFORCE-DVPR-01 | md | virtual DVP&R per the deliverable-dvpr spec; result values from simulation outputs |
| dvpr.pdf | VBF-T3R1NOFORCE-DVPR-01 | pdf | md → pdf release version (reportlab) |
| dfmea.md | VBF-T3R1NOFORCE-DFMEA-01 | md | qualitative design FMEA per the deliverable-dfmea spec (simulation-signal basis) |
| dfmea.pdf | VBF-T3R1NOFORCE-DFMEA-01 | pdf | md → pdf release version (reportlab) |
| delivery_index.md | VBF-T3R1NOFORCE-IDX-01 | md | package index per the deliverable-package spec |
| delivery_index.pdf | VBF-T3R1NOFORCE-IDX-01 | pdf | md → pdf release version (reportlab) |

Notes: engineering manufacturability drawings (with tolerances), material specifications and line process cards are outside the pure-simulation boundary and are not part of this package (stated honestly per protocol). CAD structure model `cell_model.stl` is an optional deliverable decided by user clarification; it was not requested in this task and is therefore not registered.
