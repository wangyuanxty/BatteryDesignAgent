# Design Verification Plan and Report (virtual-test version) — VBF-T1R2-DVPR-01

Case t1_r2; nominated design V4b. All results below are simulation results (PyBaMM SPMe/DFN + lumped thermal + zero-D thermal runaway); physical-test items are honestly marked N/A.

| # | Verification item | Condition | Result value | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | `run-pyamm --protocol 1C_discharge`, 298.15 K | 5.6997 Ah | PASS (≥ nominal 5.0 Ah) | `cell/r4_v4b_1c_spme.json:capacity_ah` |
| 2 | Voltage window | parameter set cut-offs | 2.5 – 4.2 V | PASS (design target; overcharge limit 4.7 V = upper + 0.5 V protocol) | parameter set `Lower/Upper voltage cut-off [V]` |
| 3 | 4C fast-charge temperature rise | `run-pyamm --protocol 4C_charge_45C` equivalent — DFN, lumped thermal, h = 60 W/m²·K, 298.15 K ambient | T_max 326.46 K (53.31 °C) | PASS (≤ 333.15 K; margin 6.69 K) | `cell/r4_v4b_4c_dfn.json:T_max_K` |
| 4 | 4C fast-charge plating | same run; negative electrode potential vs Li/Li⁺ | min +0.0215 V → plated = false | PASS (≥ 0 V required) | `cell/r4_v4b_4c_dfn.json:anode_potential_v` (min, mechanical) |
| 5 | Energy density | `bda calc-energy` contract formula (∫V·I dt ÷ Σ layer mass; electrolyte excluded) | 583.2 Wh/kg | PASS (≥ 392.61 Wh/kg) | `cell/r4_v4b_energy.json:energy_density_wh_kg` |
| 6 | Overcharge to 4.7 V → thermal runaway | `run-pyamm --protocol overcharge` (0.5C to 4.7 V) + `bda run-tr` (mcp 31.72 J/K = mass×900; hA 0.3186 = 60 × 0.00531 design-consistent) | T_max 299.43 K; triggered = false | PASS (no thermal runaway; note: lumped 0-D proxy caliber — physical validation requires experiment) | `cell/r4_v4b_overcharge.json:T_max_K`; `cell/r4_v4b_tr.json:triggered` |
| 7 | Fast-charge CC acceptance (informational) | 4C charge to 4.2 V, CC-only | 4.53 Ah (79% of 1C capacity) | INFO (no criterion; documents the voltage-limited stop) | `inferred`: (t_end − t_vmin) × 20 A / 3600, from `cell/r4_v4b_4c_dfn.json` voltage curve |

**Not covered (N/A, beyond pure simulation boundary — requires physical experiment):**
- Nail penetration — N/A
- Crush — N/A
- Drop / mechanical shock — N/A
- Cycle life (aging) — N/A for this case (durability not in criteria; Chen2020 set is aging-capable, protocol available for follow-up)
- Rate-pulse internal resistance (HPPC) — N/A; DCR 80.4 µΩ available as 1C-point estimate (`cell/r4_v4b_energy.json:dcr_ohm`)
- True DFT/MD molecular endorsement — skipped by design (entry-0 meta `real_compute: false`; endorse entry in log.jsonl records the skip honestly)

## Conclusion

All simulation-verifiable items PASS against the entry-0 criteria (mechanical `bda log-evaluate` verdicts, round 4, in `log.jsonl`). Uncovered items listed above are cited as paper limitations.
