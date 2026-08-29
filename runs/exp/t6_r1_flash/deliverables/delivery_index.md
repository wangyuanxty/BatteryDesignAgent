# Delivery Index — Case t6_r1_flash (Smartphone Battery, LNMO 4.7 V-class)

**Document**: VBF-T6R1F-IDX-01 | **Date**: 2026-08-25 | **Status**: Complete (DFN-verified; M4 documented boundary)

## Document List

| VBF Number | Document | File | Contents |
|---|---|---|---|
| VBF-T6R1F-DS-01 | Design Specification | design_spec.md | Objective, final parameters, verified performance, M4 boundary statement, rationale, references |
| VBF-T6R1F-BOM-01 | Bill of Materials | bom.md | Layer stack, masses, electrolyte formulation, thermal stack |
| VBF-T6R1F-DSH-01 | Datasheet | datasheet.md | Electrical/thermal/aging characteristics, compliance summary |
| VBF-T6R1F-CALC-01 | Calculation Report | calc.md | ED formula & values, thermal h-sweep, SEI scaling, plating-boundary calculation |
| VBF-T6R1F-DVPR-01 | Design Verification Plan & Report | dvpr.md | Criterion-by-criterion verification matrix, evidence, DFN cross-validation |
| VBF-T6R1F-DFMEA-01 | DFMEA | dfmea.md | 6 failure modes, RPN ranking, mitigations, residual risks |
| VBF-T6R1F-IDX-01 | Delivery Index | delivery_index.md | This index |

## Verdict Summary

| Criterion | Value | Threshold | Verdict |
|---|---|---|---|
| M1 Volumetric ED | 1171.7 Wh/L | ≥ 950 | PASS |
| M2 Plateau voltage | 4.145 V | ≥ 4.1 | PASS |
| M3 SEI @100 cycles | 292.2 nm | ≤ 500 | PASS |
| M4 No plating @4C | plated (−0.019 V) | false | **FAIL — documented protocol-level boundary** |
| M5 T_max @4C | 322.5 K | ≤ 323.15 | PASS |

**Design**: finN-2e19 — LNMO 74 µm / graphite 120 µm (ε 0.65) / 8 µm separator / Al 8 + Cu 6 µm / high-transference electrolyte (t⁺ 0.9, σ 20 S/m, D 1e-9) / LiF-rich SEI (D_ec 2e-19) / h = 300 W/m²K. Real 4C charge 6.68 Ah (DFN) / 6.97 Ah (SPM).

**Honesty note (M4)**: the only configurations that mechanically "pass" the plating check deliver 0–0.003 Ah at 4C (degenerate charge legs) — these are not claimed as designs. The final design delivers a real 4C charge and records the plating fail with full mechanism documentation (design_spec §4, calc §4, dvpr §3, dfmea FM-1).

## Audit Trail (log.jsonl)

- Entry 0: criteria (M1–M5), meta (real_compute false, start_stage 2, freedoms: all five categories adjustable)
- Plan (initial) + 2 plan updates (three-strike M4; DFN thermal redesign)
- Propose R1–R5 (12 candidates) / Evaluate R1–R5 (26 candidate-runs, mechanical verdicts)
- Design entry: finN-2e19; Verify entry: DFN precision verification
- Simulation outputs: cell/*.json (SPMe + DFN)
