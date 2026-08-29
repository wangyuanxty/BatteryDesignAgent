# Delivery Index — VBF Power-Tool Cell (V4 Margin-fix)

Case: t3_r1_flash | Generation date: 2026-08-25 | Doc: VBF-T3R1FLASH-IDX-01
Objective (entry 0): capacity ≥ 2 Ah · 5C discharge retention ≥ 95% · 4C fast charge no lithium plating · T_max ≤ 60 °C · power density ≥ 4000 W/kg. **Final verdict: achieved (V4 Margin-fix).**

## Design summary

| Metric | Threshold | Value | Verdict |
|---|---|---|---|
| capacity_ah | ≥ 2.0 Ah | 3.438 Ah | ✓ |
| retention_5c | ≥ 0.95 | 0.987 | ✓ |
| power_density_w_kg | ≥ 4000 W/kg | 111,807 W/kg | ✓ |
| T_max_K (4C @45 °C) | ≤ 333.15 K | 321.94 K | ✓ |
| plated (4C charge) | false | false (+22.6 mV) | ✓ |

## File list

| VBF number | File | Format | Description |
|---|---|---|---|
| VBF-T3R1FLASH-DS-01 | deliverables/design_spec.md | md | Cell design specification (basic spec, electrodes, process, mass, verification, rationale) |
| VBF-T3R1FLASH-DS-02 | deliverables/design_spec.pdf | pdf | Release of DS-01 |
| VBF-T3R1FLASH-DS-03 | report.html | html | VBF funnel report (bda render) |
| VBF-T3R1FLASH-BOM-01 | deliverables/bom.xlsx | xlsx | Bill of materials with masses and kg/kWh |
| VBF-T3R1FLASH-BOM-02 | deliverables/bom.pdf | pdf | Release of BOM-01 |
| VBF-T3R1FLASH-DSH-01 | deliverables/datasheet.md | md | Technical datasheet |
| VBF-T3R1FLASH-DSH-02 | deliverables/datasheet.pdf | pdf | Release of DSH-01 |
| VBF-T3R1FLASH-CALC-01 | deliverables/calc.xlsx | xlsx | Calculation workbook (inputs, energy, density, N/P, process) |
| VBF-T3R1FLASH-CALC-02 | deliverables/calc.pdf | pdf | Release of CALC-01 |
| VBF-T3R1FLASH-DVPR-01 | deliverables/dvpr.md | md | Design verification plan and report |
| VBF-T3R1FLASH-DVPR-02 | deliverables/dvpr.pdf | pdf | Release of DVPR-01 |
| VBF-T3R1FLASH-DFMEA-01 | deliverables/dfmea.md | md | Design FMEA (qualitative) |
| VBF-T3R1FLASH-DFMEA-02 | deliverables/dfmea.pdf | pdf | Release of DFMEA-01 |
| VBF-T3R1FLASH-IDX-01 | deliverables/delivery_index.md | md | This index |
| VBF-T3R1FLASH-IDX-02 | deliverables/delivery_index.pdf | pdf | Release of IDX-01 |

## Audit trail pointers

- Criteria and meta: log.jsonl entry 0 (stage1/stage2/stage3/meta layers)
- Plan: design_plan.md + log.jsonl `plan`
- Funnel rounds: log.jsonl `propose`/`evaluate`/`endorse` (R0 baseline fail → R1 thin+transport (plating marginal) → R2 V4/V5 pass)
- Simulation outputs: cell/r2_v4_1c_dfn.json, cell/r2_v4_5c_dfn.json, cell/r2_v4_4c_dfn.json, cell/r2_v4_energy.json, cell/r2_v4_derived.json, cell/params_r2_v4.json
- All conclusion-grade values trace to tool outputs (honesty: electrolyte density, casing mass, cycle life are annotated estimates/N-A, not simulated)
