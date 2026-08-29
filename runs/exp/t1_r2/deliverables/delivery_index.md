# Delivery Package Index — VBF-T1R2-IDX-01

## Cover information

| Field | Value |
|---|---|
| Case name | t1_r2 — next-generation pure electric sedan cell (ED ≥ 392.61 Wh/kg; 4C fast charge without plating; T_max ≤ 60 °C; overcharge to 4.7 V without thermal runaway) |
| Numbering scheme | `VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>` (case id `t1_r2` → `T1R2`; non-alphanumeric removed; SEQ-NO two-digit serial under each doc code from `01`) |
| Generation date | 2026-08-26 |
| Prepared | (blank) |
| Reviewed | (blank) |
| Approved | (blank) |

## Document code reference (protocol-fixed)

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | `design_spec.md` |
| BOM | Bill of Materials | `bom.xlsx` |
| DSH | Datasheet | `datasheet.md` |
| CALC | Calculation sheet | `calc.xlsx` |
| DVPR | Design verification report | `dvpr.md` |
| DFMEA | Failure analysis | `dfmea.md` |
| IDX | Delivery index | `delivery_index.md` (this file) |

## File list (registers only actually generated files)

| File name | Number | Format | Source note |
|---|---|---|---|
| design_spec.md | VBF-T1R2-DS-01 | md | Design specification generated per the `deliverable-design-spec` spec; all values from parameter set / simulation outputs / annotated literature |
| design_spec.pdf | VBF-T1R2-DS-01 | pdf | md → PDF release via reportlab (one-off script) |
| bom.xlsx | VBF-T1R2-BOM-01 | xlsx | Bill of materials, dual caliber g/cell + kg/kWh, generated per the `deliverable-bom` spec (openpyxl) |
| bom.pdf | VBF-T1R2-BOM-01 | pdf | xlsx → PDF release via openpyxl+reportlab |
| datasheet.md | VBF-T1R2-DSH-01 | md | Technical datasheet generated per the `deliverable-datasheet` spec |
| datasheet.pdf | VBF-T1R2-DSH-01 | pdf | md → PDF release via reportlab |
| calc.xlsx | VBF-T1R2-CALC-01 | xlsx | Design calculation sheet (inputs → capacity/energy → energy density → N/P/mass → process), formula + source columns (openpyxl) |
| calc.pdf | VBF-T1R2-CALC-01 | pdf | xlsx → PDF release via openpyxl+reportlab |
| dvpr.md | VBF-T1R2-DVPR-01 | md | Design verification plan & report, virtual-test version, generated per the `deliverable-dvpr` spec |
| dvpr.pdf | VBF-T1R2-DVPR-01 | pdf | md → PDF release via reportlab |
| dfmea.md | VBF-T1R2-DFMEA-01 | md | Design FMEA, qualitative version, generated per the `deliverable-dfmea` spec |
| dfmea.pdf | VBF-T1R2-DFMEA-01 | pdf | md → PDF release via reportlab |
| delivery_index.md | VBF-T1R2-IDX-01 | md | This index (cover + controlled file list) |
| delivery_index.pdf | VBF-T1R2-IDX-01 | pdf | md → PDF release via reportlab (blueprint-style cover colors #14283C / #1E5A8A / #C97B3D) |
| report.html | VBF-T1R2-DS-02 | html | Full audit report rendered from log.jsonl by `bda render` (ancillary file owned by DS) |

## Audit note

The complete decision audit chain is in `../log.jsonl` (entry 0 criteria → plan → propose R1–R4 → funnel → evaluate R1–R4 → endorse → final). All verdicts mechanical (`bda log-evaluate`); closing verified by `bda verify-deliverables`.
