# Delivery Package Index — VBF Case t2_r3

**Case name**: t2_r3 — Grid energy storage cell (ED ≥ 327.18 Wh/kg · 4C no plating · SEI ≤ 500/550 nm · −20 °C ≥ 90 %)
**Numbering scheme**: `VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>` (case id `t2_r3` → `T2R3`)
**Generation date**: 2026-08-26
**Prepared**: ______  **Reviewed**: ______  **Approved**: ______

## Document codes

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet technical parameter sheet | datasheet.docx |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| IDX | Delivery index (this file) | delivery_index.md |
| CAD | Structure model | **not generated** (optional deliverable; not requested in this headless case — no user clarification) |

## File list

| File | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T2R3-DS-01 | md | cell design specification, generated per deliverable-design-spec spec; values from `cell/r7_final_*_dfn.json`, `r6_combo-v5-final_aging*_spme.json`, `r6_combo-v5-final_params.json`, Chen2020 parameter dump |
| design_spec.pdf | VBF-T2R3-DS-01 | pdf | PDF release of design_spec.md (reportlab) |
| report.html | VBF-T2R3-DS-02 | html | seven-section activity report, mechanically rendered by `bda render` from log.jsonl (case root) |
| bom.xlsx | VBF-T2R3-BOM-01 | xlsx | bill of materials, dual calibre g/cell + kg/kWh (openpyxl); masses from calc-energy layer_kg_m2 × area; binder/CA split 96/2/2 = industry-typical estimate, annotated |
| bom.pdf | VBF-T2R3-BOM-01 | pdf | PDF release of bom.xlsx (reportlab) |
| datasheet.docx | VBF-T2R3-DSH-01 | docx | customer-facing technical datasheet (python-docx); every field sourced from simulation outputs |
| datasheet_docx_content.md | VBF-T2R3-DSH-02 | md | content mirror of datasheet.docx used as the reportlab input for the PDF release (build intermediate) |
| datasheet.pdf | VBF-T2R3-DSH-01 | pdf | PDF release of datasheet.docx (reportlab) |
| calc.xlsx | VBF-T2R3-CALC-01 | xlsx | design calculation sheet, 5 sheets: inputs → capacity/energy → energy density → N/P + mass → process parameters (openpyxl) |
| calc.pdf | VBF-T2R3-CALC-01 | pdf | PDF release of calc.xlsx (reportlab) |
| dvpr.md | VBF-T2R3-DVPR-01 | md | design verification plan and report, virtual-test version; 5/5 contract criteria PASS at DFN calibre; N/A items listed |
| dvpr.pdf | VBF-T2R3-DVPR-01 | pdf | PDF release of dvpr.md (reportlab) |
| dfmea.md | VBF-T2R3-DFMEA-01 | md | design FMEA, qualitative, simulation-signal based; highest risk = aged-cell 4C plating margin |
| dfmea.pdf | VBF-T2R3-DFMEA-01 | pdf | PDF release of dfmea.md (reportlab) |
| delivery_index.md | VBF-T2R3-IDX-01 | md | this delivery index (cover + controlled file list) |
| delivery_index.pdf | VBF-T2R3-IDX-01 | pdf | PDF release of delivery_index.md (reportlab) |

## Notes

- All concluded numerical values are mechanically sourced from tool outputs (PyBaMM DFN/SPMe via `bda run-pyamm`, `bda calc-energy`, `bda log-evaluate` round 7) — no values written from memory. Estimates (literature-transport overrides σ/D/t⁺, SEI bridge k/V̄, binder/CA split, electrolyte density 1.2 g/cm³) are flagged inline.
- True DFT/MD endorsement skipped by case configuration (`real_compute = false`); recorded in the `endorse` log entry.
- Engineering manufacturability drawings (with tolerances), material specifications and line process cards are outside the pure-simulation boundary — not provided.
- Editable sources (md/docx/xlsx) retained alongside PDF releases; official deliverables are the PDF release versions.