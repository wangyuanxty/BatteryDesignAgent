# Delivery Index — Smartphone Battery Design (VBF-T6R2-IDX-001)

**Case**: exp/t6_r2 · **Date**: 2026-08-26 · **Verdict**: criteria achieved (DFN-verified)

| Doc code | Document | File | VBF number |
|---|---|---|---|
| DS | Design specification | deliverables/design_spec.md (+ pdf) | VBF-T6R2-DS-001 |
| BOM | Bill of materials | deliverables/bom.xlsx (+ pdf) | VBF-T6R2-BOM-001 |
| DSH | Datasheet | deliverables/datasheet.md (+ pdf) | VBF-T6R2-DSH-001 |
| CALC | Compliance calculation book | deliverables/calc.xlsx (+ pdf) | VBF-T6R2-CALC-001 |
| DVPR | Design verification plan & report | deliverables/dvpr.md (+ pdf) | VBF-T6R2-DVPR-001 |
| DFMEA | Design FMEA | deliverables/dfmea.md (+ pdf) | VBF-T6R2-DFMEA-001 |
| IDX | Delivery index (this file) | deliverables/delivery_index.md (+ pdf) | VBF-T6R2-IDX-001 |

## Summary of result (all values tool-sourced, DFN precise model)

- Volumetric energy density: **1096.0 Wh/L** ≥ 950 ✓ (cell/r12_a_energy_dfn.json)
- Voltage plateau: **4.1301 V** ≥ 4.1 ✓ (cell/r12_a_energy_dfn.json)
- Max temperature (4C, 45 °C amb.): **322.70 K** ≤ 323.15 ✓ (cell/r12_a_4c45_dfn.json)
- Lithium plating: **not plated** (min anode potential +0.0382 V) ✓ (cell/r12_a_4c45_dfn.json)
- SEI after 100 cycles: **415.6 nm** ≤ 500 ✓ (cell/r12_a_aging.json)

## Supporting artifacts

- log.jsonl — full audit chain (entry 0 criteria → plan → propose/evaluate R1–R12 → endorse → final)
- report.html — rendered design report
- design_plan.md — Stage 1 planning document
- cell/ — all simulation outputs (SPMe/DFN), parameter files, batch evaluation inputs
  (batches relocated to cell/batches/)

True-compute endorsement skipped per pre-registered real_compute=false; endorse entry
records the skip and the DFN-only endorsement basis.
