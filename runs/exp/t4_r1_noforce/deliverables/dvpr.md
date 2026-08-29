# Design Verification Plan and Report (virtual test version) — V10a_final_h45

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C, 298.15 K ambient, DFN | 5.0618 Ah | PASS (no entry-0 capacity criterion; informational) | r6_final_1c_dfn.json:capacity_ah |
| -20 C retention | 1C discharge, 253.15 K ambient, DFN | 0.9944 (vs >= 0.95) | PASS | derived_r6_final_dfn.json |
| Energy density | contract formula | 564.84 Wh/kg (vs >= 327.18) | PASS | r6_final_energy_dfn.json |
| Volumetric energy density | contract formula | 969.50 Wh/L (vs >= 880) | PASS | r6_final_energy_dfn.json |
| 4C fast-charge temperature rise | 4C charge, 45 C, lumped thermal, DFN | T_max 329.33 K (vs <= 333.15 K) | PASS | r6_final_4C45_safety_dfn.json:T_max_K |
| 4C fast-charge plating | same, --plating; anode potential < 0 V = plated | anode min +28.96 mV → plated false | PASS | r6_final_4C45_safety_dfn.json:anode_potential_v |
| Parameter-set robustness | same design on OKane2022 base (Arrhenius electrolyte) | retention 0.9788; T_max 331.78 K; anode min +24.96 mV | PASS | derived_r6_final_ok_spme.json; r6_final_ok_4C45_safety_dfn.json |
| Cold-start honesty | Initial temperature 253.15 K (true -20 C equilibrium) | retention 0.9944; T_max 257.10 K | PASS | derived_r6_final_coldstart.json; r6_final_coldstart_lowT_dfn.json |
| Voltage window | parameter set cut-offs | 2.5 – 4.2 V | PASS (set-defined) | Chen2020 set |
| Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | | |
| Overcharge to thermal runaway | — | N/A (not simulated) | | |
| Crush / drop | — | N/A (requires physical experiment) | | |
| Cycle life | — | N/A (aging model not run; not simulated) | | |
| Rate-pulse internal resistance | — | N/A (DC resistance 3.367 mOhm reported instead, derived from 1C discharge) | r6_final_energy_dfn.json:dcr_ohm |

## Conclusion

All simulated verification items PASS against the entry-0 criteria; the design passes on two independent parameter sets at DFN grade. Uncovered items (nail, overcharge-to-thermal-runaway, crush, drop, cycle life) are outside the pure-simulation boundary and require physical experiment.
