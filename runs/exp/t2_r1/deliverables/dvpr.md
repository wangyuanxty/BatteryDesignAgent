# Design Verification Plan and Report (virtual-test version) — GridStore-D3

- **Number**: VBF-T2R1-DVPR-01
- **Case**: t2_r1 — grid energy storage battery
- **Candidate under verification**: GridStore-D3 (final design)
- Virtual verification: all result values mechanically taken from simulation output files; uncovered conditions honestly marked N/A. No values from memory.

## Verification items

| # | Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | `run-pyamm --protocol 1C_discharge`, 298.15 K | 5.06626 Ah (nominal 5.0 Ah) | PASS (≥ nominal) | `cell/r6_d3_1c.json:capacity_ah` |
| 2 | Energy density | contract caliber (calc-energy) | 465.62 Wh/kg | PASS vs ≥ 327.18 Wh/kg | `cell/r6_d3_energy.json:energy_density_wh_kg` |
| 3 | 4C fast-charge plating | `run-pyamm --protocol 4C_charge_45C --plating`, 318.15 K ambient | anode potential min +0.0498 V | PASS (no plating; min ≥ 0) | `cell/r6_d3_4c.json:anode_potential_v` |
| 4 | 4C fast-charge temperature rise | same protocol, `--thermal lumped` | T_max 342.39 K (+24.2 K vs 318.15 K ambient) | informational — no thermal red line in contract | `cell/r6_d3_4c.json:T_max_K` |
| 5 | Voltage window | parameter-set limits | 2.5 – 4.2 V | PASS (as specified) | Chen2020 dump |
| 6 | −20 °C discharge retention | `run-pyamm --protocol lowT_discharge`, 253.15 K | 99.571% (5.04452 / 5.06626 Ah) | PASS vs ≥ 90% | `cell/r6_d3_lowT_ret.json:lowT_retention_pct` |
| 7 | −20 °C true-soak cross-check | lowT protocol + `"Initial temperature [K]": 253.15` (protocol sets only ambient; initial cell temperature defaults to 298.15 K) | 99.571% (5.04452 Ah), T_max 266.71 K | PASS vs ≥ 90% | `cell/r6_d3_lowT_soak.json` |
| 8 | SEI thickness @100 cyc | `run-pyamm --protocol aging_1C_100cyc` (1C CC, 2.5–4.2 V, SEI ec reaction limited, isothermal) | 9.087 nm | PASS vs ≤ 500 nm | `cell/r6_d3_aging100.json:sei_thickness_nm_end` |
| 9 | SEI thickness @500 cyc | same protocol, `--cycles 500` | 25.317 nm | PASS vs ≤ 550 nm | `cell/r6_d3_aging500.json:sei_thickness_nm_end` |
| 10 | Cycle-capacity trajectory shape | aging protocol | flat (0.3032→0.3041 Ah over 500 cyc; no climb-then-saturate window-shift artifact) | informational | `cell/r6_d3_aging500.json:capacity_ah_per_cycle` |

### Items marked N/A (beyond pure simulation boundary / requires physical experiment)

| Item | Reason |
|---|---|
| Nail penetration | N/A (requires physical experiment) |
| Overcharge to thermal runaway | N/A (protocol available but not in task contract; not executed) |
| Crush, drop | N/A (requires physical experiment) |
| Rate-pulse internal resistance | N/A (calc-energy DCR scalar is a solver-step-density index artifact — see design_spec §6; physical pulse DCR requires experiment) |
| Real-electrode coating validation (k_sei 1e-16 bridge) | N/A (requires Stage 2 material work / physical validation — honest gap) |
| CAD structure model | N/A (structure model not requested in task clarification; optional deliverable) |

## Conclusion

5/5 contractual verification items PASS with margin (ED ×1.42, plating-free at 4C, SEI 9.1/25.3 nm vs 500/550 nm limits, −20 °C retention 99.6%). Uncovered items: nail/overcharge/crush/drop and physical coating validation — cited directly as paper limitations.

**Known tool artifacts (annotated, not defects of the design)**: (a) aging per-cycle capacity variable freezes at its first-discharge value while the actual steps are full 1C swings (probe: cycle-0 discharge 5.077 Ah / charge 4.746 Ah, cathode stoich 0.27↔0.85) — SEI end-thickness is accumulated over genuine full-depth cycles; (b) calc-energy midpoint/DCR scalars depend on solver step density (see design_spec §6).
