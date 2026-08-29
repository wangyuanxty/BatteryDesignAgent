# Delivery Package Index — VBF-T6R1-IDX-01

## Cover Information

| Field | Value |
|---|---|
| Case name | t6_r1 (smartphone battery: ED ≥ 950 Wh/L, 4C no-plating, T_max ≤ 50 °C, SEI ≤ 500 nm @100 cyc, plateau ≥ 4.1 V) |
| Numbering scheme | VBF-T6R1-&lt;DOC-CODE&gt;-&lt;SEQ&gt; |
| Generation date | 2026-08-25 |
| Signature | Prepared: ______ / Reviewed: ______ / Approved: ______ |

## Document Code Reference

| Code | Meaning | Corresponding file |
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
| design_spec.md | VBF-T6R1-DS-01 | md | generated per deliverable-design-spec format; values from parameter set / cell/r8_d6_*.json |
| design_spec.pdf | VBF-T6R1-DS-01 | pdf | md → pdf via reportlab one-off script |
| bom.xlsx | VBF-T6R1-BOM-01 | xlsx | openpyxl one-off script; layer masses from cell/r8_d6_energy_dfn.json:layer_kg_m2 |
| bom.pdf | VBF-T6R1-BOM-01 | pdf | xlsx → pdf via reportlab one-off script |
| datasheet.md | VBF-T6R1-DSH-01 | md | generated per deliverable-datasheet format |
| datasheet.pdf | VBF-T6R1-DSH-01 | pdf | md → pdf via reportlab one-off script |
| calc.xlsx | VBF-T6R1-CALC-01 | xlsx | openpyxl one-off script; 5 sheets: inputs / capacity_energy / energy_density / np_mass / process |
| calc.pdf | VBF-T6R1-CALC-01 | pdf | xlsx → pdf via reportlab one-off script |
| dvpr.md | VBF-T6R1-DVPR-01 | md | generated per deliverable-dvpr format (virtual test version) |
| dvpr.pdf | VBF-T6R1-DVPR-01 | pdf | md → pdf via reportlab one-off script |
| dfmea.md | VBF-T6R1-DFMEA-01 | md | generated per deliverable-dfmea format (qualitative version) |
| dfmea.pdf | VBF-T6R1-DFMEA-01 | pdf | md → pdf via reportlab one-off script |
| delivery_index.md | VBF-T6R1-IDX-01 | md | generated per deliverable-package format |
| delivery_index.pdf | VBF-T6R1-IDX-01 | pdf | md → pdf via reportlab one-off script (blueprint cover #14283C/#1E5A8A/#C97B3D) |
| report.html | VBF-T6R1-DS-02 | html | `bda render --case-dir` — self-contained seven-section report from log.jsonl |

**Honesty notes:** all values are tool-output sourced (cell/r8_d6_*.json, parameter-set dump, calc-energy contract formulas); estimates are marked "estimate". Enclosure/tabs and manufacturability drawings are outside the pure-simulation boundary and are "Not provided". True DFT/MD endorsement skipped (real_compute=false) and recorded in log entry `endorse`.
