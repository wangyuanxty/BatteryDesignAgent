# Delivery Package Index — t8_r1 (T8-40g Long-Endurance Drone Battery)

- **Case name**: t8_r1
- **Numbering scheme**: VBF-T8R1-<DOC-CODE>-<SEQ-NO>
- **Generation date**: 2026-08-25
- **Signature block**: Prepared: ________  Reviewed: ________  Approved: ________

## Document Code Reference (fixed by protocol)

| Document code | Meaning | Corresponding file |
|--------|------|---------|
| DS | Specification | design_spec.md / design_spec.pdf |
| BOM | Bill of Materials | bom.xlsx / bom.pdf |
| DSH | Datasheet technical parameter sheet | datasheet.docx / datasheet.pdf |
| CALC | Calculation sheet | calc.xlsx / calc.pdf |
| DVPR | Design verification report | dvpr.md / dvpr.pdf |
| DFMEA | Failure analysis | dfmea.md / dfmea.pdf |
| IDX | Delivery package index | delivery_index.md / delivery_index.pdf |

## File List

| File name | Number | Format | Source description |
|-----------|--------|--------|--------------------|
| design_spec.md | VBF-T8R1-DS-01 | md | generated per deliverable-design-spec reference; values from tool outputs |
| design_spec.pdf | VBF-T8R1-DS-01 | pdf | reportlab one-off export of design_spec.md |
| bom.xlsx | VBF-T8R1-BOM-01 | xlsx | openpyxl; dual caliber g/cell + kg/kWh from r5_final_energy.json |
| bom.pdf | VBF-T8R1-BOM-01 | pdf | reportlab export of bom.xlsx content |
| datasheet.docx | VBF-T8R1-DSH-01 | docx | python-docx per deliverable-datasheet reference |
| datasheet.pdf | VBF-T8R1-DSH-01 | pdf | reportlab export of datasheet content |
| calc.xlsx | VBF-T8R1-CALC-01 | xlsx | openpyxl; 5 sheets with formula+source columns |
| calc.pdf | VBF-T8R1-CALC-01 | pdf | reportlab export of calc sheet tables |
| dvpr.md | VBF-T8R1-DVPR-01 | md | generated per deliverable-dvpr reference; 7 pass + N/A items |
| dvpr.pdf | VBF-T8R1-DVPR-01 | pdf | reportlab one-off export of dvpr.md |
| dfmea.md | VBF-T8R1-DFMEA-01 | md | generated per deliverable-dfmea reference; qualitative S/O |
| dfmea.pdf | VBF-T8R1-DFMEA-01 | pdf | reportlab one-off export of dfmea.md |
| delivery_index.md | VBF-T8R1-IDX-01 | md | cover + controlled list of this package |
| delivery_index.pdf | VBF-T8R1-IDX-01 | pdf | reportlab one-off; inner table row-identical to md |
| report.html | VBF-T8R1-DS-02 | html | bda render (ancillary, owned by DS code) |

Notes: CAD/cell_model not produced — 3D structure model was not requested in the task text and is not part of the closing deliverables. True DFT/MD endorsement skipped (real_compute = false, recorded in log.jsonl endorse entry). All performance values above originate from tool output files under `cell/` (PyBaMM DFN / calc-energy).
