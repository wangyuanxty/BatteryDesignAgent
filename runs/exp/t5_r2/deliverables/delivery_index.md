# Delivery Package Index - VBF-T5R2-IDX-01

**Case**: t5_r2 **Verdict**: achieved **Date**: 2026-08-26 **Protocol**: Virtual Battery Factory

## Status summary

| Criterion | Threshold | Measured | Verdict |
|---|---|---|---|
| Energy density | >= 500.94 Wh/kg | 666.30 | PASS |
| Max temperature @4C | <= 333.15 K | 330.98 K | PASS |
| Lithium plating @4C | none | anode potential min +0.0506 V | PASS |

closing audit chain: entry 0 contract -> plan -> ceiling -> 7 propose rounds each with
same-round evaluate -> endorse (skipped, real_compute=false, justified) -> final (achieved).

## Controlled file list (only actually generated files are registered)

| VBF number | File | Format | Source |
|---|---|---|---|
| VBF-T5R2-DS-01 | design_spec.md | md | Design specification - stack/parameters/process/verification; generated per deliverable-design-spec spec |
| VBF-T5R2-DS-02 | design_spec.pdf | pdf | PDF release of VBF-T5R2-DS-01 (reportlab) |
| VBF-T5R2-DSH-01 | datasheet.md | md | Cell datasheet - finalist f2_h70_C verified figures |
| VBF-T5R2-DSH-02 | datasheet.pdf | pdf | PDF release of VBF-T5R2-DSH-01 (reportlab) |
| VBF-T5R2-BOM-01 | bom.xlsx | xlsx | Bill of materials - dual caliber g/cell + kg/kWh, estimates marked |
| VBF-T5R2-BOM-02 | bom.pdf | pdf | PDF release of VBF-T5R2-BOM-01 (openpyxl -> reportlab) |
| VBF-T5R2-CALC-01 | calc.xlsx | xlsx | 5-sheet calculation chain: inputs -> mass -> energy -> stack/process -> verification |
| VBF-T5R2-CALC-02 | calc.pdf | pdf | PDF release of VBF-T5R2-CALC-01 |
| VBF-T5R2-DVPR-01 | dvpr.md | md | Design verification plan & report - 6 PASS rows + 5 honest N/A rows |
| VBF-T5R2-DVPR-02 | dvpr.pdf | pdf | PDF release of VBF-T5R2-DVPR-01 |
| VBF-T5R2-DFMEA-01 | dfmea.md | md | Design FMEA - qualitative S/O/RPN with simulation signals |
| VBF-T5R2-DFMEA-02 | dfmea.pdf | pdf | PDF release of VBF-T5R2-DFMEA-01 |
| VBF-T5R2-IDX-01 | delivery_index.md | md | This index |
| VBF-T5R2-IDX-02 | delivery_index.pdf | pdf | This index (PDF release) |

Notes:
- cell_model.stl was **not** requested by the task and is therefore not provided (recorded
  honestly in log.jsonl `final` entry caveats).
- report.html is a post-close audit presentation produced by `bda render`; it is not part
  of this controlled package.
- Simulation outputs and the audit ledger live in the case workspace (cell/*.json, log.jsonl,
  bridge/p_r6_f2.json) as the evidence chain for every number above.
