# Delivery Index — ArchF Drone Battery

## Cover Information
| Field | Value |
|---|---|
| Case Name | t8_r1_mimo |
| Case ID | T8R1MIMO |
| Generation Date | 2026-08-31 |
| Prepared By | [blank — for manual signing] |
| Reviewed By | [blank — for manual signing] |
| Approved By | [blank — for manual signing] |

## Document Numbering Scheme
`VBF-T8R1MIMO-<DOC-CODE>-<SEQ>`

## File List

| # | Document Number | File Name | Format | Source / Description |
|---|---|---|---|---|
| 1 | VBF-T8R1MIMO-DS-01 | design_spec.md | md | Design specification generated per deliverable-design-spec format |
| 2 | VBF-T8R1MIMO-BOM-01 | bom.xlsx | xlsx | Bill of materials from parameter set mass calculation |
| 3 | VBF-T8R1MIMO-DSH-01 | datasheet.md | md | Technical datasheet with electrical/mechanical/safety specs |
| 4 | VBF-T8R1MIMO-CALC-01 | calc.xlsx | xlsx | Design calculation sheet (mass, ED, rate, safety) |
| 5 | VBF-T8R1MIMO-DVPR-01 | dvpr.md | md | Design verification plan and report (virtual test results) |
| 6 | VBF-T8R1MIMO-DFMEA-01 | dfmea.md | md | Design FMEA (qualitative, 7 failure modes) |
| 7 | — | report.html | html | Simulation report (rendered from log.jsonl) |
| 8 | VBF-T8R1MIMO-DS-01 | design_spec.md | md → pdf | PDF release version (source: design_spec.md) |

## Notes
- All values sourced from simulation output files (log.jsonl entries and calc-energy output)
- Mass excludes electrolyte and casing (formula-caliber mass per protocol)
- Transport parameters (σ, D, t+) are domain estimates, not measured values — marked as such in design spec
- PDF export to be completed in post-processing step
