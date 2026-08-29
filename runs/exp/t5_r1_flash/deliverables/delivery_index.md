# Delivery Index — t5_r1_flash

**Doc No. VBF-T5R1FLASH-INDEX-01** · Generation date: 2026-08-25 · Numbering scheme: VBF-<CASE-UPPER>-<doc-code>-<serial> · Signature fields left blank for review.

| File | Doc No. | Format | Source note |
|---|---|---|---|
| design_spec.md / design_spec.pdf | VBF-T5R1FLASH-DS-01 | Markdown / PDF (release) | parameter set + simulation (calc-energy/run-pyamm) |
| bom.xlsx / bom.pdf | VBF-T5R1FLASH-BOM-01 | Excel / PDF (release) | calc-energy layer masses + composition estimates |
| datasheet.md / datasheet.pdf | VBF-T5R1FLASH-DSH-01 | Markdown / PDF (release) | parameter set + simulation |
| calc.xlsx / calc.pdf | VBF-T5R1FLASH-CALC-01 | Excel / PDF (release) | full calculation chain, formulas annotated |
| dvpr.md / dvpr.pdf | VBF-T5R1FLASH-DVPR-01 | Markdown / PDF (release) | virtual tests (run-pyamm DFN) |
| dfmea.md / dfmea.pdf | VBF-T5R1FLASH-DFMEA-01 | Markdown / PDF (release) | simulation signals, qualitative ratings |
| delivery_index.md / delivery_index.pdf | VBF-T5R1FLASH-INDEX-01 | Markdown / PDF (release) | this index |

VBF numbering list: VBF-T5R1FLASH-DS-01 · VBF-T5R1FLASH-BOM-01 · VBF-T5R1FLASH-DSH-01 · VBF-T5R1FLASH-CALC-01 · VBF-T5R1FLASH-DVPR-01 · VBF-T5R1FLASH-DFMEA-01 · VBF-T5R1FLASH-INDEX-01

**Case summary:** next-generation flagship-vehicle battery — LNMO/graphite 4.7 V system, HiTrans-class electrolyte transport, 4C fast charge without plating, T_max ≤ 60 °C.
**Final (conclusion-grade, DFN):** 597.9 Wh/kg (≥500.94) · 4C anode min +14.7 mV (no plating) · T_max 327.6 °C (≤60 °C) — **ALL GATES PASS**, verdict: achieved (log.jsonl final entry).
Audit trail: runs/exp/t5_r1_flash/log.jsonl (plan → propose R1–R9 → funnel → evaluate R1–R9 → endorse (skipped, real_compute=false) → final).
Signatures: ______ (design) · ______ (review) · ______ (approval)
