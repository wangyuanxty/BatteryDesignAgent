# Design Verification Plan and Report (virtual test version) — T8-40g

- **Document code**: VBF-T8R1-DVPR-01
- **Case**: t8_r1 — long-endurance drone battery
- **Generation date**: 2026-08-25
- **Signature**: Prepared: ________  Reviewed: ________  Approved: ________

All result values are mechanically taken from tool output files under `cell/`. Determinatios compare against entry-0 criteria (energy density ≥ 446.18 Wh/kg, 5C retention ≥ 90%, mass ≤ 40 g) and protocol safety defaults (T_max ≤ 333.15 K, no plating).

## Verification Items

| # | Item | Condition | Result value | Determination | Source |
|---|------|-----------|--------------|---------------|--------|
| 1 | 1C discharge capacity | `run-pyamm --protocol 1C_discharge` (DFN, lumped thermal) | 6.9427 Ah (T_max 299.76 K) | PASS (capacity consistent with nominal 6.1494 Ah) | `cell/r5_final_1c_dfn.json` |
| 2 | Energy density | `calc-energy` on 1C discharge, contract mass caliber | 634.32 Wh/kg (1027.10 Wh/L) | PASS ≥ 446.18 Wh/kg | `cell/r5_final_energy.json` |
| 3 | Cell mass | contract formula Σ layer×(1−ε)×density×area | 39.798 g | PASS ≤ 40 g | `cell/r5_final_energy.json` |
| 4 | 5C discharge capacity retention | `run-pyamm --protocol 5C_discharge` ÷ same-params 1C capacity | 6.8571 Ah / 98.77% (T_max 319.99 K) | PASS ≥ 90% | `cell/r5_final_5c_dfn.json`, `cell/r5_final_retention.json` |
| 5 | 4C fast-charge temperature rise | `run-pyamm --protocol 4C_charge_45C --thermal lumped` | T_max 330.41 K | PASS ≤ 333.15 K (margin 2.74 K) | `cell/r5_final_4c45_dfn.json` |
| 6 | 4C fast-charge lithium plating | same protocol + `--plating`; negative electrode potential < 0 V | anode potential min +0.0082 V | PASS (no plating) | `cell/r5_final_4c45_dfn.json` |
| 7 | Voltage window | parameter set limits | 2.5 – 4.2 V | PASS (nominal window used by all protocols) | `cell/chen2020_base_probe.json` |
| 8 | Charge acceptance at 4C | `4C_charge_45C` capacity integral | 0.9395 Ah before 4.2 V cut-off | INFORMATIONAL — voltage-limited at 4C; not a task criterion | `cell/r5_final_4c45_dfn.json` |

## Items Marked N/A

| Item | Status |
|------|--------|
| Nail penetration | N/A (beyond pure simulation boundary, requires physical experiment) |
| Overcharge to thermal runaway | N/A (beyond pure simulation boundary, requires physical experiment) |
| Crush | N/A (beyond pure simulation boundary, requires physical experiment) |
| Drop | N/A (beyond pure simulation boundary, requires physical experiment) |
| Cycle life | N/A (aging model exists in Chen2020 base but was not exercised — no cycle-life criterion in task) |
| Rate-pulse internal resistance | N/A (no pulse protocol in task criteria; DC-IR 0.684 mΩ mechanically derived in `r5_final_energy.json` as informational) |

## Conclusion

- **Summary**: 7/7 simulated verification items PASS against entry-0 criteria and protocol safety defaults. Final candidate T8-40g: ED 634.32 Wh/kg, 5C retention 98.77%, mass 39.798 g, 4C-45 °C T_max 330.41 K, no plating.
- **Uncovered items (paper limitations)**: nail penetration, overcharge-to-thermal-runaway, crush, drop, cycle life, rate-pulse internal resistance — all N/A beyond pure simulation boundary or outside task criteria.
- **Honest caveats**: 4C charge acceptance is voltage-limited to 0.94 Ah (item 8); safety thresholds are protocol defaults (task silent on safety); contract-mass caliber excludes electrolyte.
