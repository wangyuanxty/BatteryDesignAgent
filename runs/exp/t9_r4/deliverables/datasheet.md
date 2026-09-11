# VBF-T9R4-DSH-001 Datasheet (Target vs Measured)

t9_r4 - grid-storage cell cathode on the Chen2020 NMC811/graphite profile
Result: HONEST NEGATIVE (no candidate satisfies the full contract; nothing reported as passing)

| Criterion | Threshold | Best measured | Verdict |
|---|---|---|---|
| Computed avg voltage | >= 4.6 V | 4.6413 V (AlB55) | window pass, then REJECTED on compatibility |
| Charging potential | <= 4.8 V | 7.410 V (AlB55, V(0.4->0.3)) | FAIL - decisive |
| Catalogue exclusion | not of 115 | PASS (outside envelope) | pass |
| Hull exclusion | outside 102-point hull | PASS (outside envelope) | pass |
| Supported family | six families | layered LiMO2 | pass |
| Energy density 1C | >= 327.18 Wh/kg | not reached (no survivor to stage 3) | n/a |
| ED_active report | V x C x 0.9 | AlB55: 4.6413 x 324.38 x 0.9 = 1355 (Wh/kg-active, informative only) | n/a |
| 4C/45C plating | none | not reached | n/a |
| Thermal runaway | no trigger | not reached | n/a |
| SEI @100 x 1C | <= 500 nm | not reached (baseline Chen2020 ~449 nm signal) | n/a |
| True-voltage guard | >= 4.6 beyond proxy | envelope re-computation 4.6354 V (independent run) | informative |

Overall: NOT ACHIEVED. The only window-passer fails the electrolyte compatibility limit by
2.6 V; no candidate passes both stage-1 co-gates, so stages 2-4 were never reached.