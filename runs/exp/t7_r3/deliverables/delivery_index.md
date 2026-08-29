# Delivery Index — Virtual Battery Factory Design Package

**Case**: t7_r3 — HEV battery cell design (ED ≥ 327.18 Wh/kg · 4C plating-free · SEI ≤ 550 nm @100cyc/45 °C · nail 10 W no thermal runaway)
**Numbering scheme**: `VBF-T7R3-<DOC-CODE>-<SEQ>` (case ID t7_r3 → T7R3; two-digit serial under each document code)
**Generation date**: 2026-08-26
**Signature block** — Prepared: ________ · Reviewed: ________ · Approved: ________ (left blank for manual signing)

## File list

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T7R3-DS-01 | md | Cell design specification — generated per deliverable-design-spec spec, all values from Chen2020 set / r7_v19_final simulation outputs |
| design_spec.pdf | VBF-T7R3-DS-01 | pdf | PDF release of design_spec.md — reportlab export |
| report.html | VBF-T7R3-DS-02 | html | Ancillary: closing seven-section HTML report — `bda render` of log.jsonl |
| bom.xlsx | VBF-T7R3-BOM-01 | xlsx | Bill of materials, dual caliber g/cell + kg/kWh — openpyxl generator, values from energy.json layer masses + literature electrolytic density |
| bom.pdf | VBF-T7R3-BOM-01 | pdf | PDF release of bom.xlsx — reportlab table export |
| datasheet.md | VBF-T7R3-DSH-01 | md | Customer-facing technical datasheet — simulation values with per-row source |
| datasheet.pdf | VBF-T7R3-DSH-01 | pdf | PDF release of datasheet.md — reportlab export |
| calc.xlsx | VBF-T7R3-CALC-01 | xlsx | Design calculation sheet (input → capacity/energy → energy density → N/P & mass → process) with formula + source columns — openpyxl generator |
| calc.pdf | VBF-T7R3-CALC-01 | pdf | PDF release of calc.xlsx — reportlab table export |
| dvpr.md | VBF-T7R3-DVPR-01 | md | Design verification plan & report, virtual-test version — 9 rows incl. nail sweep, N/A items listed |
| dvpr.pdf | VBF-T7R3-DVPR-01 | pdf | PDF release of dvpr.md — reportlab export |
| dfmea.md | VBF-T7R3-DFMEA-01 | md | Qualitative design FMEA on simulation signals — 7 failure modes, S×O matrix |
| dfmea.pdf | VBF-T7R3-DFMEA-01 | pdf | PDF release of dfmea.md — reportlab export |
| delivery_index.md | VBF-T7R3-IDX-01 | md | This index (cover + controlled file list) |
| delivery_index.pdf | VBF-T7R3-IDX-01 | pdf | PDF release of this index — reportlab export (blueprint cover colors #14283C / #1E5A8A / #C97B3D) |
| _gen_xlsx.py / _gen_pdf.py | (tooling, no number) | py | One-off generator scripts retained for reproducibility; not controlled deliverables |

**Notes**: (1) CAD structure model `cell_model.stl` is not in this package — the structure model is decided by user clarification per protocol, and this headless session had no user request (recommendation recorded in DS-01: pouch stacked, exploded view with real thickness annotations). (2) The official releases are the PDFs; editable sources (md/xlsx) are retained in this same flat directory. (3) Every value in the package is mechanically taken from parameter set / bda tool outputs / annotated literature constants; per-line sources inside each document.