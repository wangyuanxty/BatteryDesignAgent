# Design Verification Plan and Report (virtual test version) — VBF-T5R1-DVPR-01

**Case**: t5_r1. **Design under verification**: R7B (`bridge/r7b_negR261.json`), DFN precision, dual system Chen2020 + OKane2022.
**Generation date**: 2026-08-25. All result values mechanically from simulation outputs; determinations are `bda log-evaluate` round-7 verdicts (code-computed vs entry-0 criteria).

| # | Verification item | Condition | Result value | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C (5 A nominal) discharge to 2.5 V, 25 °C, DFN | 6.2104 Ah (Chen2020) / 6.2086 Ah (OKane2022) | PASS (no capacity threshold in contract; nominal 5 Ah exceeded) | `cell/r7b_{chen,okane}_1c_dfn.json:capacity_ah` |
| 2 | Energy density | contract caliber (Σ layer mass, electrolyte excluded) | 642.098 Wh/kg (Chen) / 641.118 Wh/kg (OKane) | **PASS** ≥ 500.94 Wh/kg | `cell/r7b_{chen,okane}_energy.json:energy_density_wh_kg` |
| 3 | 4C fast-charge temperature rise | 1C discharge to 2.5 V, then 20 A CC charge to 4.2 V, 45 °C ambient, lumped thermal | T_max 326.829 K (Chen) / 328.189 K (OKane) | **PASS** ≤ 333.15 K (60 °C) | `cell/r7b_{chen,okane}_4c_dfn.json:T_max_K` |
| 4 | 4C fast-charge lithium plating | same protocol, plating enabled; criterion: anode surface potential < 0 V | anode min +0.01826 V (Chen) / +0.01798 V (OKane) → plated = false | **PASS** (no plating), +18 mV margin | `cell/r7b_{chen,okane}_4c_dfn.json:anode_potential_v` (min>0 derived by log-evaluate) |
| 5 | Voltage window | parameter-set limits | 2.5 – 4.2 V (both sets) | PASS (contract definition) | parameter set dump |
| 6 | Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| 7 | Overcharge to thermal runaway | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| 8 | Crush / drop | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| 9 | Cycle life | — | N/A (aging protocol available on these sets but outside task contract; not executed — value not fabricated) | N/A | — |
| 10 | Rate-pulse internal resistance | — | N/A (only calc-energy DC-resistance caliber available: 3.50 mΩ Chen / 17.93 mΩ OKane, reported for information) | N/A | `calc-energy` dcr_ohm |

## Conclusion

**All simulated verification items PASS under both parameter systems (Chen2020 and OKane2022).** The three contract criteria — ED ≥ 500.94 Wh/kg, 4C no plating, T_max ≤ 60 °C — are each evidenced by file:key sources above and mechanically judged by `bda log-evaluate` (round 7, verdict=pass).

**Uncovered items (paper limitations, cited directly)**: nail penetration, overcharge-to-thermal-runaway, crush, drop, cycle life, rate-pulse internal resistance — all N/A within the pure-simulation boundary of this case.

**Known tool caveat**: 4C-output `capacity_ah` key under-reports charge capacity ~5× (library bug in pybamm_runner; `t×C_rate/3600` missing the 5 Ah nominal factor). It is not used in any determination above (plating from `anode_potential_v`, T_max from lumped thermal, ED from 1C integration).
