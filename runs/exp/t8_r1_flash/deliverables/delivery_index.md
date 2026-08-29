# Delivery Index — VBF-T8R1FLASH

**Case name**: t8_r1_flash — long-endurance drone battery (energy density ≥ 446.18 Wh/kg, 5C discharge retention ≥ 90%, cell mass ≤ 40 g)
**Design**: V4 Thermal-tuned — NMC811/graphite, nano particles, high-transport electrolyte, thin collectors, flatter-pouch cooling
**Key results**: ED 473.0 Wh/kg | 5C retention 99.0 % | mass 26.8 g | 4C-charge T_max 331.98 K | no plating | **verdict: achieved**
**Generation date**: 2026-08-25
**Numbering scheme**: VBF-T8R1FLASH-<DOC-CODE>-<SEQ-NO> (uppercase case ID, non-alphanumerics removed)

| File | Number | Format | Source description |
|---|---|---|---|
| design_spec.md | VBF-T8R1FLASH-DS-01 | md | generated per deliverable-design-spec spec; values from parameter set + cell/r1_v4_*.json (mechanical) |
| design_spec.pdf | VBF-T8R1FLASH-DS-01 | pdf | md -> pdf release (reportlab) |
| report.html | VBF-T8R1FLASH-DS-02 | html | bda render from log.jsonl (audit report, seven sections) |
| delivery_index.md | VBF-T8R1FLASH-DS-03 | md | package cover + controlled file list (this file) |
| delivery_index.pdf | VBF-T8R1FLASH-DS-03 | pdf | md -> pdf release, blueprint cover style (reportlab) |
| bom.xlsx | VBF-T8R1FLASH-BOM-01 | xlsx | openpyxl from final_data.json (g/cell + kg/kWh, per-line source column) |
| bom.pdf | VBF-T8R1FLASH-BOM-01 | pdf | xlsx -> pdf release (reportlab) |
| datasheet.md | VBF-T8R1FLASH-DSH-01 | md | generated per deliverable-datasheet spec; simulation-verified values |
| datasheet.pdf | VBF-T8R1FLASH-DSH-01 | pdf | md -> pdf release (reportlab) |
| calc.xlsx | VBF-T8R1FLASH-CALC-01 | xlsx | openpyxl: inputs/capacity&energy/ED/N-P&mass/process sheets, formula+source columns |
| calc.pdf | VBF-T8R1FLASH-CALC-01 | pdf | xlsx -> pdf release (reportlab) |
| dvpr.md | VBF-T8R1FLASH-DVPR-01 | md | virtual-test verification report; per-row source to cell/r1_v4_*.json |
| dvpr.pdf | VBF-T8R1FLASH-DVPR-01 | pdf | md -> pdf release (reportlab) |
| dfmea.md | VBF-T8R1FLASH-DFMEA-01 | md | qualitative FMEA from simulation risk signals |
| dfmea.pdf | VBF-T8R1FLASH-DFMEA-01 | pdf | md -> pdf release (reportlab) |

**Notes**
- CAD structure model: not generated (optional deliverable requiring user clarification; headless run — honestly skipped).
- Signature block: prepared / reviewed / approved — left blank for manual signing.
- Official release format = PDF; editable sources retained (md/xlsx).
