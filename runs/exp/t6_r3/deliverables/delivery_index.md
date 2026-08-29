# Delivery Index — Virtual Battery Factory Package

| Item | Value |
|---|---|
| Case ID | t6_r3 |
| Title | Smartphone high-voltage fast-charge cell — V27_combo (DFN-verified) |
| Document scheme | VBF-T6R3-<CODE>-01 (DS, BOM, DSH, CALC, DVPR, DFMEA, IDX) |
| Date | 2026-08-26 |
| Version | 01 |
| Status | Released (virtual design; no physical cell) |
| Prepared by | ____________ |
| Approved by | ____________ |
| Verification | verify-deliverables PASS and bda render complete — audit trail t6_r3/log.jsonl; all 7 deliverable categories present with PDF releases |

## Document list

| No | Doc code | Document number | Title | Source file | PDF release |
|---|---|---|---|---|---|
| 1 | DS | VBF-T6R3-DS-01 | Design Specification | design_spec.md | design_spec.pdf |
| 2 | BOM | VBF-T6R3-BOM-01 | Bill of Materials | bom.xlsx | bom.pdf |
| 3 | DSH | VBF-T6R3-DSH-01 | Datasheet | datasheet.md | datasheet.pdf |
| 4 | CALC | VBF-T6R3-CALC-01 | Calculation Sheet | calc.xlsx | calc.pdf |
| 5 | DVPR | VBF-T6R3-DVPR-01 | Design Verification Plan & Report (virtual) | dvpr.md | dvpr.pdf |
| 6 | DFMEA | VBF-T6R3-DFMEA-01 | Design FMEA | dfmea.md | dfmea.pdf |
| 7 | IDX | VBF-T6R3-IDX-01 | Delivery Index (this file) | delivery_index.md | delivery_index.pdf |

## Package notes

- Verdict: **achieved** (log.jsonl `final` entry). All five entry-0 criteria pass with DFN precision; margins: ED +33.61 Wh/L, plateau +55.1 mV, T -4.23 K, anode potential +105.0 mV, SEI -186.3 nm.
- Every performance value in this package carries a per-row source annotation (output JSON key or parameter file line). No fabricated or DFT/MD-derived values exist (real_compute=false; endorse skipped honestly).
- Audit trail: t6_r3/log.jsonl — entry 0 (criteria), plan, 11 evaluate rounds (rounds 5-10 incl. round-9 DFN rejection), endorse (skipped), final (achieved).
- Known limitations are disclosed in design_spec.md section 7 and DVPR notes (4C protocol initial state, aging trajectory artifact, fixed electrolyte transport).

## Signatures

| Prepared by | Date | Reviewed by | Date | Approved by | Date |
|---|---|---|---|---|---|
| ____________ | | ____________ | | ____________ | |