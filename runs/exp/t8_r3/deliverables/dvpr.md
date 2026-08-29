# Design Verification Plan and Report (virtual test version) — t8_r3 (VBF-T8R3-DVPR-01)

All results below are simulation outputs (no physical cell exists); uncovered conditions marked N/A honestly.

| Item | Condition | Result | Determination | Source |
|---|---|---|---|---|
| Energy density | 1C discharge energy ÷ stack mass | 497.54 Wh/kg | ✓ pass vs ≥446.18 | energy:energy_density_wh_kg |
| 5C retention | 5C DFN capacity ÷ 1C DFN capacity | 98.66% | ✓ pass vs ≥90% | derived retention_5c |
| Mass | calc-energy stack mass | 37.32 g | ✓ pass vs ≤40 g | energy:mass_kg |
| 4C fast-charge temperature rise | 4C charge, 45 °C chamber, thermal lumped | 326.53 K | ✓ pass vs ≤333.15 K | 4c_safety:T_max_K |
| 4C fast-charge plating | same run, anode_potential_v vs 0 V | min +0.0177 V → plated=false | ✓ pass | 4c_safety:anode_potential_v |
| 1C discharge capacity | 1C CC discharge to 2.5 V | 5.0728 Ah | informational (no capacity criterion in entry 0) | 1c_dfn:capacity_ah |
| Voltage window | parameter set limits | 2.5–4.2 V | within parameter-set bounds | Chen2020 cut-offs |
| Overcharge → thermal runaway | overcharge + 3-reaction ODE, T0=overcharge T_max | triggered=False (299.33 K → 299.33 K) | ✓ not triggered (informational) | overcharge + run-tr outputs |
| Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | — |
| Crush / drop | — | N/A (requires physical experiment) | N/A | — |
| Cycle life | aging protocol not in objective | N/A (not simulated — no entry-0 criterion) | N/A | — |


**Conclusion**: all five entry-0 criteria pass (see rows 1–5); safety-related informational checks pass; nail/crush/drop/cycle-life remain beyond virtual-testing boundary.
