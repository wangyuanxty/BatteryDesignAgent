# Design Verification Plan and Report — T4R1FLASH (virtual test)

Case: `t4_r1_flash`  |  Generation date: 2026-08-25  |  Doc: VBF-T4R1FLASH-DVPR-01

_All values mechanical from simulation outputs / parameter set (see log.jsonl); no numbers from memory._

| # | Verification item | Condition | Result | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC discharge 25 degC to 2.5 V | 3.9547 Ah | PASS (≥ nominal 3.93 Ah) | cell/final_b7_1c_dfn.json |
| 2 | -20 degC capacity retention | 1C discharge at 253.15 K / 1C at 298.15 K | 0.99286 | PASS (≥ 0.95) | cell/final_b7_retention_dfn.json |
| 3 | Gravimetric energy density | ∫V·I dt / contract mass | 460.06 Wh/kg | PASS (≥ 327.18) | cell/final_b7_energy_dfn.json |
| 4 | Volumetric energy density | ∫V·I dt / layer-stack volume | 899.25 Wh/L | PASS (≥ 880.0) | cell/final_b7_energy_dfn.json |
| 5 | 4C fast-charge temperature rise | 4C CC charge, 45 degC ambient, lumped thermal | T_max 329.61 K | PASS (≤ 333.15 K) | cell/final_b7_4c45_dfn.json |
| 6 | 4C fast-charge plating | anode potential min over 4C charge | +0.0193 V | PASS (> 0 V, plated=false) | cell/final_b7_4c45_dfn.json |
| 7 | Overcharge -> thermal runaway | 0.5C overcharge to 4.7 V + TR ODE | triggered = False | PASS (no runaway) | cell/final_b7_overcharge.json, cell/final_b7_tr.json |
| 8 | Voltage window | parameter set cut-offs | 2.5–4.2 V | PASS | parameter set |
| 9 | Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | — | — |
| 10 | Crush / drop | — | N/A (beyond pure simulation boundary, requires physical experiment) | — | — |
| 11 | Cycle life | — | N/A (no aging model in this case) | — | — |
| 12 | Rate-pulse internal resistance | — | N/A (beyond pure simulation boundary) | — | — |

## Conclusion

8/8 simulation-verifiable items PASS at DFN precision (model_used=DFN, no fallback). Uncovered items: nail penetration, crush, drop, cycle life, rate-pulse DCR — physical-experiment boundary (cited as paper limitations).
