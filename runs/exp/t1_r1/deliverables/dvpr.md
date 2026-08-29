# Design Verification Plan and Report (virtual test) — VBF-T1R1-DVPR-01

Case: t1_r1 | Date: 2026-08-25 | Prepared: ____________ | Reviewed: ____________ | Approved: ____________

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | run-pyamm --protocol 1C_discharge, SPMe, 298.15 K | 5.6505 Ah | PASS vs parameter nominal 5.0 Ah (no registered capacity criterion) | cell/r3_I_1c.json:capacity_ah |
| 4C fast-charge temperature rise | run-pyamm --protocol 4C_charge_45C, DFN, lumped thermal, T_amb 318.15 K | T_max 325.655 K = 52.51 °C, rise +7.50 K | PASS vs criterion ≤ 333.15 K (margin 7.50 K) | cell/r3_I_4c_dfn.json:T_max_K |
| 4C fast-charge plating | same protocol + plating module; negative electrode potential vs Li/Li+ | min anode potential +0.0249 V (≥ 0 → plated = false) | PASS vs criterion plated = false (margin 24.9 mV) | cell/r3_I_4c_dfn.json:anode_potential_v (DFN authoritative; SPMe corroborates +0.0135 V in cell/r3_I_4c.json) |
| Voltage window | parameter set limits | 2.5 – 4.2 V | PASS (design envelope per Chen2020) | Chen2020 cut-off parameters |
| Overcharge without thermal runaway | run-pyamm --protocol overcharge (0.5C to 4.2 V + 0.5 V = 4.7 V), then run-tr with mass-kg from calc-energy | terminal voltage 4.7000 V; overcharge peak 299.552 K; TR triggered = false | PASS vs criterion triggered = false | cell/r3_I_oc.json (voltage tail, T_max_K); cell/r3_I_tr.json:triggered |
| Nail penetration | — | N/A (requires physical experiment) | N/A (beyond pure simulation boundary, requires physical experiment) | — |
| Crush / drop | — | N/A (requires physical experiment) | N/A (beyond pure simulation boundary, requires physical experiment) | — |
| Cycle life | — | N/A (no aging model in this case; aging protocol not part of registered criteria) | N/A (beyond pure simulation boundary) | — |
| Rate-pulse internal resistance | — | N/A (requires physical experiment) | N/A (beyond pure simulation boundary; DC resistance proxy available: dcr_ohm 0.155 mΩ, cell/r3_I_energy.json) | — |

## Conclusion

- PASS summary: energy density 553.977 Wh/kg (criterion ≥ 392.61, round-4 evaluate PASS); 4C fast charge without plating (DFN authoritative, anode min +0.0249 V); T_max 325.655 K ≤ 333.15 K; overcharge 4.7000 V without thermal runaway (triggered = false). All four registered stage2/stage3 criteria satisfied by candidate r3-I.
- Per-round funnel record: round 0 baseline fail (plating −0.4385 V); round 1 architecture all fail (plating); round 2 formulation fallback, Tmax solved, plating −0.0149 V; round 3 all four candidates pass, finalist r3-I (margins: ED +161 Wh/kg, Tmax 7.50 K, anode potential 24.9 mV).
- Uncovered items (paper limitations): molecular-layer criteria (max_energy_ev / max_homo_ev) unchecked — no molecular candidates proposed, real_compute = false; nail penetration / crush / drop / cycle life N/A (requires physical experiment).
