# Design Verification Plan & Report (Virtual Test) — VBF-T5R3-DVPR-01

**Case**: t5_r3 · **Design under verification**: Y4 (primary, `cell/params_y4.json`) and Y3 (alternate, `cell/params_y3.json`) · **Date**: 2026-08-26 · **Scope**: simulation-based verification only; uncovered conditions marked N/A honestly.

## Verification Results — Y4 (Primary)

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C CC discharge, 298.15 K, full-order DFN | 5.0442 Ah | No capacity threshold in contract (information) | `cell/r6_y4_1c_dfn.json:capacity_ah` |
| Rated energy | same | 18.2855 Wh | Information | `cell/r6_y4_energy_dfn.json:energy_wh` |
| Energy density (gravimetric) | 25 °C 1C, contract formula | 535.72 Wh/kg | ✓ PASS vs ≥ 500.94 Wh/kg | `cell/r6_y4_energy_dfn.json:energy_density_wh_kg` |
| Volumetric energy density | same | 995.79 Wh/L | Information | `cell/r6_y4_energy_dfn.json:energy_density_wh_l` |
| 4C fast-charge temperature rise | 4C CC charge, 318.15 K ambient, lumped thermal, DFN | T_max = 327.60 K (54.4 °C) | ✓ PASS vs ≤ 333.15 K | `cell/r6_y4_4c_dfn.json:T_max_K` |
| 4C fast-charge plating | same, `--plating`; anode surface potential | min +0.0200 V (never < 0 V) | ✓ PASS (plated = false) | `cell/r6_y4_4c_dfn.json:anode_potential_v` |
| 4C CC charge window | 20 A CC from 2.5 V to 4.2 V cut-off | 3.48 Ah (≈69 % SOC) in 626 s | Information (task = support 4C without plating; CV tail not simulated) | `cell/r6_y4_4c_dfn.json:time_s/voltage_v` |
| Voltage window | parameter set limits | 2.5 – 4.2 V | Information | `param_dump.txt` |

## Verification Results — Y3 (Supply-friendly alternate, Al 8 µm / sep 9 µm)

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| Energy density | 25 °C 1C, contract formula | 526.24 Wh/kg | ✓ PASS vs ≥ 500.94 Wh/kg | `cell/r6_y3_energy_dfn.json:energy_density_wh_kg` |
| 4C fast-charge temperature rise | lumped thermal, DFN | T_max = 329.38 K | ✓ PASS vs ≤ 333.15 K | `cell/r6_y3_4c_dfn.json:T_max_K` |
| 4C fast-charge plating | `--plating`, DFN | min +0.0162 V | ✓ PASS (plated = false) | `cell/r6_y3_4c_dfn.json:anode_potential_v` |
| 1C capacity | DFN | 5.0442 Ah | Information | `cell/r6_y3_1c_dfn.json:capacity_ah` |

## Items Explicitly N/A (beyond pure simulation boundary, requires physical experiment)

| Item | Status |
|---|---|
| Nail penetration | N/A (requires physical experiment) |
| Overcharge to thermal runaway | N/A (requires physical experiment) |
| Crush / drop | N/A (requires physical experiment) |
| Cycle life | N/A (no aging model run; task has no durability metric — must not fabricate) |
| Rate-pulse internal resistance | N/A (parameter-caliber DCR 2.723 mΩ available as reference: `r6_y4_energy_dfn.json:dcr_ohm`) |
| Enclosure / tabs / manufacturing line validation | N/A (beyond pure-simulation boundary) |

## Conclusion

**All contractual criteria PASS at full-order DFN precision.** Pass criteria: energy density ≥ 500.94 Wh/kg ✓ (535.72), 4C fast charge without lithium plating ✓ (min anode potential +0.0200 V), maximum temperature ≤ 60 °C ✓ (327.60 K). Plating margin is thin by design trade (kinetic warmth ↔ temperature) — recommend physical-cell validation sequence: foil handling (5 µm Cu handling sensitivity), 4C CC charging anode reference-electrode test, and CV-tail confirmation before productization. Uncovered items listed above are the paper limitations.