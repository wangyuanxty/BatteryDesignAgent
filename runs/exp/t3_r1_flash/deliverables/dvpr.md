# Design Verification Plan and Report — VBF Power-Tool Cell (V4 Margin-fix)

Case: t3_r1_flash | Generation date: 2026-08-25 | Doc: VBF-T3R1FLASH-DVPR-01
Virtual-test version (pure simulation boundary).

## Verification Items

| # | Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | run-pyamm 1C_discharge, DFN, 25 °C | 3.438 Ah | ✓ ≥ 2.0 Ah | cell/r2_v4_1c_dfn.json:capacity_ah |
| 2 | 5C discharge capacity retention | run-pyamm 5C_discharge, DFN, 25 °C; retention = 5C/1C | 3.393 Ah; retention 0.987 | ✓ ≥ 0.95 | r2_v4_5c_dfn.json + r2_v4_derived.json |
| 3 | 4C fast-charge temperature | run-pyamm 4C_charge_45C, DFN, thermal lumped | T_max 321.94 K (48.8 °C) | ✓ ≤ 333.15 K (60 °C) | r2_v4_4c_dfn.json:T_max_K |
| 4 | 4C fast-charge plating | same + --plating; negative surface potential < 0 V = plated | anode potential min +22.6 mV | ✓ plated=false | r2_v4_4c_dfn.json:anode_potential_v |
| 5 | Power density | calc-energy (V_OC²/4DCR/mass) | 111,807 W/kg | ✓ ≥ 4000 W/kg | r2_v4_energy.json:power_density_w_kg |
| 6 | Voltage window | parameter set upper/lower limits | 2.5 – 4.2 V | ✓ | parameter set |
| 7 | Energy density (informational) | calc-energy contract formula | 410 Wh/kg / 864 Wh/L | informational | r2_v4_energy.json |

## Items N/A (beyond pure simulation boundary, requires physical experiment)

- Nail penetration, overcharge-to-thermal-runaway, crush, drop
- Cycle life (aging model not part of this task's criteria)
- Rate-pulse internal resistance (DCR measured per contract formula instead)
- Shell/casing mechanical design, tab/weld design

## Conclusion

All 6 adjudicable verification items pass; 0 fail. The V4 design meets every entry-0 criterion (capacity ≥ 2 Ah, 5C retention ≥ 95%, no plating at 4C, T_max ≤ 60 °C, power density ≥ 4000 W/kg). Uncovered items listed above are the honest limitations of the pure-simulation boundary.
