# Design Verification Plan and Report (virtual-test version) — t1_r1_noforce (C7)

VBF-T1R1NOFORCE-DVPR-01 · Generation date: 2026-08-25 · All results are simulation outputs (PyBaMM cell model + thermal-runaway ODE)

| # | Verification item | Condition | Result value | Determination (vs criteria) | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC, 25 °C ambient, lumped thermal, to 2.5 V | 5.654 Ah | Informational (no task threshold) | `cell/r6_c7_1c_spme.json:capacity_ah` |
| 2 | Energy density | contract formula: ∫V·I dt ÷ Σ thickness×(1−ε)×density×area | 457.93 Wh/kg | ✓ PASS (≥ 392.61) | `cell/r6_c7_energy.json:energy_density_wh_kg` |
| 3 | 4C fast-charge temperature rise | 4C CC at 45 °C ambient, lumped thermal, with plating model | T_max = 318.79 K | ✓ PASS (≤ 333.15 K, margin 14.4 K) | `cell/r6_c7_4c.json:T_max_K` |
| 4 | 4C fast-charge lithium plating | anode surface potential vs Li/Li⁺, plating if any value < 0 V | min = +0.00824 V (SPMe); +0.00515 V (DFN cross-check) | ✓ PASS (never < 0 V) | `cell/r6_c7_4c.json` / `cell/r6_c7_4c_dfn.json:anode_potential_v` |
| 5 | Overcharge → thermal runaway | 0.5C charge to 4.7 V (4.2 + 0.5), then three-side-reaction ODE (mass 44.705 g → mcp = mass×900) | triggered = false; T_max = 298.22 K; dT/dt max = −8.6e-7 K/s | ✓ PASS (no thermal runaway) | `cell/r6_c7_oc.json`, `validation/r6_c7_tr.json` |
| 6 | Voltage window | parameter set | 2.5 – 4.2 V (overcharge window verified to 4.7 V) | Informational | Chen2020 dump |
| 7 | 4C CC charge acceptance | 4C CC from fully discharged, 45 °C, until 4.2 V | 4.63 Ah = 81.9 % SOC in ≈836 s (charge-side capacity = raw ×5, nominal-capacity factor, mechanically derived) | ✓ met design-quality gate (~80 %) | `cell/r6_c7_4c.json:capacity_ah` |

Items explicitly N/A (beyond pure simulation boundary / outside task scope, requires physical experiment):
nail penetration; crush; drop; cycle life (aging model available on Chen2020 but not part of this task); −20 °C low-temperature discharge; 5C rate discharge.

## Conclusion

All task criteria pass for C7: energy density 457.93 Wh/kg ≥ 392.61; 4C charge at 45 °C with T_max 318.79 K ≤ 333.15 K and no lithium plating (SPMe + DFN cross-check); overcharge to 4.7 V without thermal runaway. Uncovered items listed above — the plating margin under DFN is +5 mV, so a physical-prototype 4C validation is recommended (paper limitation, stated honestly).
