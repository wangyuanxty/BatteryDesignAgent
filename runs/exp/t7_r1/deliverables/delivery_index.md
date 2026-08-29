# Delivery Index — Virtual Battery Factory Case t7_r1

Document: VBF-T7R1-IDX-01 · Generated 2026-08-25 · Signature: Prepared ______ / Reviewed ______ / Approved ______

- **Case name**: t7_r1 — HEV battery design (energy density ≥ 327.18 Wh/kg, 4C fast charge without lithium plating, SEI ≤ 550 nm after 100 cycles @ 45 °C, nail penetration 10 W without thermal runaway)
- **Numbering scheme**: `VBF-<CASE-ID-UPPER>-<DOC-CODE>-<SEQ-NO>`; case ID `t7_r1` → alphanumeric token **T7R1** (non-alphanumeric characters removed per numbering rule); SEQ-NO two digits from 01
- **Generation date**: 2026-08-25
- **Result**: achieved (final entry verdict; V11-final passes 4/4 criteria at DFN precision)

## Document Code Reference

| Document code | Meaning | File |
|---|---|---|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet | datasheet.md |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| IDX | Delivery index | delivery_index.md |

## File List

| File name | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T7R1-DS-01 | md | generated per deliverable-design-spec spec; all values from parameter-set dump + R5 tool outputs |
| design_spec.pdf | VBF-T7R1-DS-01 | pdf | md → PDF release via reportlab one-off script |
| bom.xlsx | VBF-T7R1-BOM-01 | xlsx | openpyxl; component masses from calc-energy layer masses + literature split fractions (annotated) |
| bom.pdf | VBF-T7R1-BOM-01 | pdf | xlsx → PDF release via reportlab |
| datasheet.md | VBF-T7R1-DSH-01 | md | generated per deliverable-datasheet spec |
| datasheet.pdf | VBF-T7R1-DSH-01 | pdf | md → PDF via reportlab |
| calc.xlsx | VBF-T7R1-CALC-01 | xlsx | openpyxl; five sheets: inputs / capacity-energy / energy density / N-P-mass / process parameters; formula + source columns |
| calc.pdf | VBF-T7R1-CALC-01 | pdf | xlsx → PDF via reportlab |
| dvpr.md | VBF-T7R1-DVPR-01 | md | generated per deliverable-dvpr spec (virtual test version) |
| dvpr.pdf | VBF-T7R1-DVPR-01 | pdf | md → PDF via reportlab |
| dfmea.md | VBF-T7R1-DFMEA-01 | md | generated per deliverable-dfmea spec (qualitative) |
| dfmea.pdf | VBF-T7R1-DFMEA-01 | pdf | md → PDF via reportlab |
| delivery_index.md | VBF-T7R1-IDX-01 | md | this file, per deliverable-package spec |
| delivery_index.pdf | VBF-T7R1-IDX-01 | pdf | md → PDF via reportlab (blueprint-style cover) |
| report.html | VBF-T7R1-DS-02 | html | `bda render` output (seven-section HTML report from log.jsonl; ancillary of DS) |

## Notes

- **CAD structure model (cell_model.stl): not produced** — optional deliverable, requires user clarification for form/presentation; none given in this headless run.
- PDFs generated with a one-off reportlab script (`.venv`); cover style follows engineering-blueprint colors.
- All conclusion-grade values in this package trace to tool output files under `cell/` (run-pyamm / calc-energy / run-tr) or to the Chen2020 parameter-set dump; no value written from memory.
- True first-principles endorsement skipped: real_compute = false (entry 0 meta; see endorse entry in log.jsonl).
