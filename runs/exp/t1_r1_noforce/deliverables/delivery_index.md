# Delivery Package Index — t1_r1_noforce

**Case name**: t1_r1_noforce (battery for next-generation pure electric sedan: ED ≥ 392.61 Wh/kg, 4C fast charge without lithium plating, T_max ≤ 60 °C, 4.7 V overcharge without thermal runaway; ablation: exploration_force OFF, free exploration)

**Numbering scheme**: `VBF-T1R1NOFORCE-<DOC-CODE>-<SEQ-NO>`

**Generation date**: 2026-08-25

**Signature block**: Prepared: __________ · Reviewed: __________ · Approved: __________

## Document code reference

| Document code | Meaning | Corresponding file |
|---|---|---|
| DS | Specification | design_spec.md |
| BOM | Bill of Materials | bom.xlsx |
| DSH | Datasheet | datasheet.md |
| CALC | Calculation sheet | calc.xlsx |
| DVPR | Design verification report | dvpr.md |
| DFMEA | Failure analysis | dfmea.md |
| IDX | Delivery index | delivery_index.md |
| CAD | Structure model | not generated (optional, not requested) |

## File list

| File | Number | Format | Source |
|---|---|---|---|
| design_spec.md | VBF-T1R1NOFORCE-DS-01 | md | generated per deliverable-design-spec spec, values from Chen2020 dump + r6_c7_* outputs |
| design_spec.pdf | VBF-T1R1NOFORCE-DS-01 | pdf | md → pdf exported by reportlab one-off script |
| bom.xlsx | VBF-T1R1NOFORCE-BOM-01 | xlsx | generated per deliverable-bom spec (openpyxl), layer masses from calc-energy |
| bom.pdf | VBF-T1R1NOFORCE-BOM-01 | pdf | xlsx → pdf exported by reportlab one-off script |
| datasheet.md | VBF-T1R1NOFORCE-DSH-01 | md | generated per deliverable-datasheet spec |
| datasheet.pdf | VBF-T1R1NOFORCE-DSH-01 | pdf | md → pdf exported by reportlab one-off script |
| calc.xlsx | VBF-T1R1NOFORCE-CALC-01 | xlsx | generated per deliverable-calc-sheet spec (openpyxl), 5 sheets with formula+source columns |
| calc.pdf | VBF-T1R1NOFORCE-CALC-01 | pdf | xlsx → pdf exported by reportlab one-off script |
| dvpr.md | VBF-T1R1NOFORCE-DVPR-01 | md | generated per deliverable-dvpr spec (virtual test version) |
| dvpr.pdf | VBF-T1R1NOFORCE-DVPR-01 | pdf | md → pdf exported by reportlab one-off script |
| dfmea.md | VBF-T1R1NOFORCE-DFMEA-01 | md | generated per deliverable-dfmea spec (qualitative version) |
| dfmea.pdf | VBF-T1R1NOFORCE-DFMEA-01 | pdf | md → pdf exported by reportlab one-off script |
| delivery_index.md | VBF-T1R1NOFORCE-IDX-01 | md | generated per deliverable-package spec |
| delivery_index.pdf | VBF-T1R1NOFORCE-IDX-01 | pdf | md → pdf exported by reportlab one-off script |

## Design summary

Endorsed design **C7** (round 6): Chen2020 NMC811/graphite baseline + single-crystal cathode 1.2 µm, fine graphite anode 0.8 µm (95 µm thick), high-transport electrolyte (σ 1.8 S/m, D 5e-10 m²/s, t⁺ 0.5), pouch double-face liquid cold-plate cooling (h 25 W/m²K, A 0.2054 m²). All criteria pass: ED 457.93 Wh/kg; 4C@45 °C T_max 318.79 K, no plating (anode min +0.0082 V SPMe / +0.0052 V DFN); overcharge 4.7 V without thermal runaway (triggered=false). Audit chain: log.jsonl entries 0–25 (plan/funnel/propose/evaluate R1–R7/endorse/final); report.html rendered from log.
