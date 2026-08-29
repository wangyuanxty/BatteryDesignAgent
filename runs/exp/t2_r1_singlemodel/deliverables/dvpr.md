# Design Verification Plan and Report (virtual) — VBF-T2R1SINGLEMODEL-DVPR-01

> Virtual-test version: all results are simulation outputs; uncovered conditions honestly
> "N/A (requires physical experiment)". Generation date 2026-08-25.

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C CC to 2.5 V, 298.15 K, DFN | 6.9555 Ah | informational (no capacity criterion in entry 0) | cell/r3_1c_dfn.json |
| 5C discharge capacity | 5C CC to 2.5 V, DFN | 0.4939 Ah (7% of 1C; voltage collapses to cut-off in ~71 s — severely rate-limited; informational, no 5C criterion) | informational (no 5C criterion in entry 0) | cell/r3_5c_dfn.json |
| 4C fast-charge temperature rise | 4C CC to 4.2 V, 45 C start, lumped thermal | T_max 342.5 K (rise +24.3 K) | informational (T_max monitored, no red line) | cell/r3_4c45.json |
| 4C fast-charge plating | same + plating module | ap_min +0.112 V (45 C); +0.111 V (25 C conservative start) | PASS (plated == false) | cell/r3_4c45.json / cell/r3_4c25_conservative.json |
| Voltage window | parameter set cut-offs | 2.5 – 4.2 V | informational | parameter set |
| Low-temperature retention | 1C discharge, 253.15 K (-20 C), DFN | 99.59 % vs 298.15 K | PASS (>= 90 %) | cell/derived_retention_lowT_r3.json |
| SEI growth @100 cycles | aging 1C cycling, ec reaction limited, DFN | 194.56 nm | PASS (<= 500 nm) | cell/r3_aging100.json |
| SEI growth @500 cycles | aging 1C cycling, 500 completed cycles, DFN | 439.74 nm | PASS (<= 550 nm) | cell/r3_aging500_d1e19.json |
| Overcharge to thermal runaway | 0.5C charge to 4.7 V (overcharge protocol) | DFN solver failure in 4.7 V charge phase (IDA, recorded verbatim); TR coupling on partial-run T_max 322.7 K -> not triggered | conditional (virtual test incomplete; physical test required) | cell/r3_overcharge.json / cell/r3_tr.json |
| Nail penetration | 5 W short-circuit heat source, lumped TR ODE | triggered, T_max 408.4 K @ 1159 s | informational (safety screen) | cell/r3_tr_nail.json |
| Crush / drop / storage life | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |

## Conclusion

All entry-0 criteria PASS (energy density, SEI100, SEI500, low-T retention, 4C plating).
Uncovered: overcharge-to-4.7 V virtual test (DFN solver failure recorded; physical overcharge
test recommended), nail/crush/drop physical confirmation, long-term storage.
