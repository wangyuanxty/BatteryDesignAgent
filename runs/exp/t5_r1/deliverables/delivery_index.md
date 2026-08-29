# Delivery Package Index — VBF-T5R1-IDX-01

## Cover information

| Field | Value |
|---|---|
| Case name | t5_r1 — next-generation flagship vehicle battery (ED ≥ 500.94 Wh/kg, 4C no plating, T_max ≤ 60 °C) |
| Numbering scheme | `VBF-T5R1-<DOC-CODE>-<SEQ-NO>` |
| Case verdict | ACHIEVED (design R7B, dual-system DFN validation; log.jsonl `final` entry) |
| Generation date | 2026-08-25 |
| Prepared | ____________________ (blank for manual signing) |
| Reviewed | ____________________ (blank for manual signing) |
| Approved | ____________________ (blank for manual signing) |

## Document code reference (fixed by protocol)

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | `design_spec.md` |
| BOM | Bill of Materials | `bom.xlsx` |
| DSH | Datasheet technical parameter sheet | `datasheet.md` |
| CALC | Calculation sheet | `calc.xlsx` |
| DVPR | Design verification report | `dvpr.md` |
| DFMEA | Failure analysis | `dfmea.md` |
| IDX | Delivery index | `delivery_index.md` |
| CAD | Structure model | not produced (not requested in task clarification; zero-interaction session) |

## File list

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T5R1-DS-01 | md | Cell design specification per deliverable-design-spec format; values mechanically from parameter-set dumps + bda outputs |
| design_spec.pdf | VBF-T5R1-DS-01 | pdf | PDF release of design_spec.md (reportlab one-off script) |
| design_plan.md | VBF-T5R1-DS-02 | md | Stage-1 design plan + plan updates (workspace root; audit anchor) |
| report.html | VBF-T5R1-DS-03 | html | Seven-section HTML report rendered by `bda render` from log.jsonl (workspace root) |
| bom.xlsx | VBF-T5R1-BOM-01 | xlsx | Bill of materials, g/cell + kg/kWh dual caliber, openpyxl |
| bom.pdf | VBF-T5R1-BOM-01 | pdf | PDF release of bom.xlsx |
| datasheet.md | VBF-T5R1-DSH-01 | md | Technical datasheet per deliverable-datasheet format |
| datasheet.pdf | VBF-T5R1-DSH-01 | pdf | PDF release of datasheet.md |
| calc.xlsx | VBF-T5R1-CALC-01 | xlsx | Design calculation sheet (inputs → capacity/energy → ED → N/P&mass → process), openpyxl |
| calc.pdf | VBF-T5R1-CALC-01 | pdf | PDF release of calc.xlsx |
| dvpr.md | VBF-T5R1-DVPR-01 | md | Design verification plan and report (virtual-test version) |
| dvpr.pdf | VBF-T5R1-DVPR-01 | pdf | PDF release of dvpr.md |
| dfmea.md | VBF-T5R1-DFMEA-01 | md | Design FMEA (qualitative, simulation-signal based) |
| dfmea.pdf | VBF-T5R1-DFMEA-01 | pdf | PDF release of dfmea.md |
| delivery_index.md | VBF-T5R1-IDX-01 | md | This index (cover + controlled file list) |
| delivery_index.pdf | VBF-T5R1-IDX-01 | pdf | PDF release of this index (blueprint-style cover) |

Notes: all deliverables flat in `deliverables/` (no zip); engineering manufacturability drawings (with tolerances), material specifications and line process cards are outside the pure-simulation boundary — stated honestly, not produced.
