# Delivery Package Index — t8_r3 (VBF-T8R3-IDX-01)

| Field | Value |
|---|---|
| Case name | t8_r3 |
| Numbering scheme | VBF-&lt;CASE-ID-UPPER&gt;-&lt;DOC-CODE&gt;-&lt;SEQ&gt; → VBF-T8R3-DS-01 style |
| Generation date | 2026-08-26 |
| Prepared / Reviewed / Approved | (blank) / (blank) / (blank) — left for manual signing |

## Document code reference

| Code | Meaning | File |
|---|---|---|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet | datasheet.md |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| IDX | Delivery index | delivery_index.md |

CAD (cell_model.stl): not requested (zero-interaction session, no structure-model clarification) — not produced, not registered.

## File list

| File | Number | Format | Source |
|---|---|---|---|
| design_spec.md | VBF-T8R3-DS-01 | md | generated per deliverable-design-spec spec (values from Chen2020 parameter set + r4 sim outputs) |
| design_spec.pdf | VBF-T8R3-DS-01 | pdf | md→pdf via reportlab release |
| report.html | VBF-T8R3-DS-02 | html | bda render log.jsonl audience report (copied into deliverables/) |
| bom.xlsx | VBF-T8R3-BOM-01 | xlsx | openpyxl; component masses from calc-energy layer_kg_m2 + parameter set; AM/CB/binder split literature defaults |
| bom.pdf | VBF-T8R3-BOM-01 | pdf | xlsx→pdf via reportlab release |
| datasheet.md | VBF-T8R3-DSH-01 | md | generated per deliverable-datasheet spec |
| datasheet.pdf | VBF-T8R3-DSH-01 | pdf | md→pdf via reportlab release |
| calc.xlsx | VBF-T8R3-CALC-01 | xlsx | openpyxl; 5 sheets: inputs / capacity-energy / energy density / NP-mass / process |
| calc.pdf | VBF-T8R3-CALC-01 | pdf | xlsx→pdf via reportlab release |
| dvpr.md | VBF-T8R3-DVPR-01 | md | generated per deliverable-dvpr spec (virtual version); N/A items stated |
| dvpr.pdf | VBF-T8R3-DVPR-01 | pdf | md→pdf via reportlab release |
| dfmea.md | VBF-T8R3-DFMEA-01 | md | generated per deliverable-dfmea spec (qualitative) |
| dfmea.pdf | VBF-T8R3-DFMEA-01 | pdf | md→pdf via reportlab release |
| delivery_index.md | VBF-T8R3-IDX-01 | md | this file (cover + controlled file list) |
| delivery_index.pdf | VBF-T8R3-IDX-01 | pdf | md→pdf via reportlab release |
