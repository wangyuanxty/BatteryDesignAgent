# Delivery Package Index — VBF-T7R1NOFORCE-IDX-01

- **Case name**: `t7_r1_noforce` (HEV battery design, NMC811/graphite Chen2020 baseline)
- **Numbering scheme**: `VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>` — case ID `t7_r1_noforce` → `T7R1NOFORCE`; two-digit serial per document code starting at `01`. Editable source and PDF release share the same number (distinguished in file name / format columns).
- **Generation date**: 2026-08-25
- **Signature block** — Prepared: ________  Reviewed: ________  Approved: ________ (left blank for manual signing)

## Document Code Reference Table (fixed by protocol)

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | `design_spec.md` |
| BOM | Bill of Materials | `bom.xlsx` |
| DSH | Datasheet technical parameter sheet | `datasheet.md` / `datasheet.docx` |
| CALC | Calculation sheet | `calc.xlsx` |
| DVPR | Design verification report | `dvpr.md` |
| DFMEA | Failure analysis | `dfmea.md` |
| IDX | Delivery package index | `delivery_index.md` |
| CAD | Structure model | not produced — optional deliverable requiring user clarification (headless session, not requested); no CAD number registered |

## File List (only actually generated files registered)

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T7R1NOFORCE-DS-01 | md | generated per deliverable-design-spec spec; values from Chen2020 parameter dump + R5 simulation outputs |
| design_spec.pdf | VBF-T7R1NOFORCE-DS-01 | pdf | PDF release, reportlab export |
| report.html | VBF-T7R1NOFORCE-DS-02 | html | case report rendered by `bda render` from log.jsonl (workspace root, copied to deliverables/) |
| bom.xlsx | VBF-T7R1NOFORCE-BOM-01 | xlsx | generated per deliverable-bom spec (openpyxl), dual caliber g/cell and kg/kWh |
| bom.pdf | VBF-T7R1NOFORCE-BOM-01 | pdf | PDF release, reportlab export |
| datasheet.md | VBF-T7R1NOFORCE-DSH-01 | md | generated per deliverable-datasheet spec (editable source) |
| datasheet.docx | VBF-T7R1NOFORCE-DSH-01 | docx | docx release (python-docx), content identical to md source |
| datasheet.pdf | VBF-T7R1NOFORCE-DSH-01 | pdf | PDF release, reportlab export |
| calc.xlsx | VBF-T7R1NOFORCE-CALC-01 | xlsx | generated per deliverable-calc-sheet spec (openpyxl), 5 sheets: inputs → capacity/energy → energy density → N/P & mass → process parameters |
| calc.pdf | VBF-T7R1NOFORCE-CALC-01 | pdf | PDF release, reportlab export |
| dvpr.md | VBF-T7R1NOFORCE-DVPR-01 | md | generated per deliverable-dvpr spec (virtual test version) |
| dvpr.pdf | VBF-T7R1NOFORCE-DVPR-01 | pdf | PDF release, reportlab export |
| dfmea.md | VBF-T7R1NOFORCE-DFMEA-01 | md | generated per deliverable-dfmea spec (qualitative version, simulation signals) |
| dfmea.pdf | VBF-T7R1NOFORCE-DFMEA-01 | pdf | PDF release, reportlab export |
| delivery_index.md | VBF-T7R1NOFORCE-IDX-01 | md | this index (editable source) |
| delivery_index.pdf | VBF-T7R1NOFORCE-IDX-01 | pdf | PDF release, reportlab export with engineering-blueprint cover style |

**Verdict summary** (audit anchor: log.jsonl, final entry): all four contract criteria achieved by round-5 design — ED 491.47 Wh/kg ≥ 327.18; 4C @45 °C plated = false (anode min +0.0153 V); SEI 510.51 nm ≤ 550 after 100 cycles @45 °C; nail 10 W triggered = false. Mechanical evaluation: `bda log-evaluate --round 5` → verdict pass (checked 4, unchecked 2).
