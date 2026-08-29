# Design Verification Plan & Report (virtual) — VBF-T4R2-DVPR-01
Case t4_r2 · finalist E3-porheadroom · DFN verdict grade · 2026-08-26

> One row per verification item. Values mechanically taken from simulation outputs under `cell/`; uncovered conditions honestly marked "N/A (requires physical experiment)". No values from memory.

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C retention @ −20 °C (W1) | lowT_discharge, T₀=253.15 K cold-soak (warm-start artifact procedure), DFN | 0.9938 (5.0078 / 5.0392 Ah) | ✓ PASS vs ≥ 0.95 (margin +4.6 ppt) | `cell/r5_E3_retention_dfn.json` |
| Gravimetric energy density (W2) | 1C discharge energy ÷ contract-caliber mass (electrolyte excluded) | 459.4465 Wh/kg | ✓ PASS vs ≥ 327.18 (margin +132.3) | `cell/r5_E3_energy_dfn.json` |
| Volumetric energy density (W3) | contract caliber: Σ layer thickness × area | 936.8218 Wh/L | ✓ PASS vs ≥ 880 (margin +56.8) | `cell/r5_E3_energy_dfn.json` |
| 4C fast-charge temperature rise (W4) | 4C_charge_45C (pre-condition 1C discharge to 2.5 V then 4C charge to 4.2 V, ambient 318.15 K), DFN + lumped thermal | T_max 326.96 K | ✓ PASS vs ≤ 333.15 (margin −6.19 K) | `cell/r5_E3_4c_dfn2.json` |
| 4C fast-charge plating (W5) | same protocol + plating module, `anode_potential_v` vs 0 V | min +0.0060 V, 0/307 points negative → plated=false | ✓ PASS (margin 6 mV) | `cell/r5_E3_4c_dfn2.json` |
| Reproducibility | second independent DFN 4C run | identical T_max and anode-potential min | ✓ deterministic | `r5_E3_4c_dfn.json` vs `_dfn2` |
| 1C discharge capacity (25 °C) | 1C_discharge, DFN | 5.0392 Ah | informational (no capacity criterion; +0.78 % vs nominal 5.0) | `cell/r5_E3_1c_dfn.json` |
| Voltage window | parameter set limits | 2.5 – 4.2 V | informational | Chen2020 parameter set |
| Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | — | — |
| Overcharge to thermal runaway | run-tr module exists but no abuse criterion in entry-0 stage set | N/A (requires physical experiment / not in scope) | — | — |
| Crush / drop | — | N/A (requires physical experiment) | — | — |
| Cycle life | aging protocol exists but not in entry-0 scope | N/A — "Not simulated (no aging run)" — not fabricated | — | — |
| Rate-pulse internal resistance | not a protocol | N/A (DCR 2.07 mΩ reported in calc-energy as informational) | — | `r5_E3_energy_dfn.json` dcr_ohm |

## Conclusion

All five entry-0 criteria PASS at DFN verdict grade with margins (retention +4.6 ppt; +132.3 Wh/kg; +56.8 Wh/L; −6.19 K thermal; plating margin 6 mV). Two independent DFN 4C runs agree exactly.

Uncovered (cited for paper limitations): physical abuse (nail/crush/drop), overcharge-to-runaway calibration, cycle life, sub-−20 °C operation, and any molecular-level true-compute endorsement (Stage 5 skipped, real_compute=false). The thinnest margin is the plating headroom (6 mV) — flagged as the top DFMEA risk with mitigations in `dfmea.md`.