# Design Verification Plan and Report (virtual) — VBF-T8R1FLASH-DVPR-01

**Case**: t8_r1_flash | **Date**: 2026-08-25 | **Design**: V4 Thermal-tuned

| # | Item | Condition | Result | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC to 2.5 V, 25 °C, DFN | 3.452 Ah | meets design 3.40 Ah | cell/r1_v4_1c.json |
| 2 | 5C discharge retention | 5C CC to 2.5 V, 25 °C, DFN | 99.0 % (5C 3.418 Ah / 1C 3.452 Ah) | PASS ≥ 90 % | cell/r1_v4_retention.json |
| 3 | Energy density | contract formula | 473.0 Wh/kg | PASS ≥ 446.18 | cell/r1_v4_energy.json |
| 4 | Cell mass | contract layer stack | 26.8 g | PASS ≤ 40 g | cell/r1_v4_energy.json |
| 5 | 4C fast-charge temperature rise | 4C charge, 45 °C ambient, lumped thermal, DFN | T_max 331.98 K (ΔT 13.8 K) | PASS ≤ 333.15 K | cell/r1_v4_4c.json |
| 6 | 4C fast-charge plating | same + plating model, min anode potential | 0.0247 V > 0 | PASS, no plating | cell/r1_v4_4c.json:anode_potential_v |
| 7 | Voltage window | parameter set | 4.20–2.50 V | meets spec | parameter set |
| 8 | Overcharge → thermal runaway (informational) | 1C to 2.5 V, 0.5C to 4.7 V; run-tr coupling | T_max 300.57 K; triggered = False | not triggered (informational) | cell/r1_v4_ovc.json, r1_v4_tr.json |

**N/A items (beyond pure-simulation boundary, require physical experiment)**: nail penetration, crush, drop, rate-pulse internal resistance, cycle life (standard SEI model artifact — see aging note), −20 °C low-temperature retention.

**Conclusion**: All contract verification items PASS. Uncovered items listed above (cite as paper limitations).
