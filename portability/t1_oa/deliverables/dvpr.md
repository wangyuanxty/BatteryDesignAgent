# Design Verification Plan and Report (virtual test) — VBF-T1OA-DVPR-01

> Virtual-test version. Values from simulation output; uncovered conditions marked N/A.

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C, 298.15 K | 5.057 Ah | ✓ (nominal 5.0 Ah) | `cell/T10_1c_dfn.json:capacity_ah` |
| Energy density | contract caliber | 426.89 Wh/kg | ✓ (≥ 392.61) | `cell/T10_energy_dfn.json:energy_density_wh_kg` |
| 4C fast-charge temperature rise | 4C, 318.15 K, lumped thermal | T_max 324.55 K | ✓ (≤ 333.15 K = 60 °C) | `cell/T10_4c_dfn.json:T_max_K` |
| 4C fast-charge plating | 4C + plating module | anode min +0.0341 V | ✓ (plated = false) | `cell/T10_4c_dfn.json:anode_potential_v` |
| Overcharge → thermal runaway | 0.5C charge to 4.70 V + run-tr ODE | triggered = false | ✓ | `cell/T10_tr.json:triggered` |
| Voltage window | parameter set | 2.5 – 4.2 V | ✓ | parameter set |
| Nail penetration | — | — | N/A (beyond simulation boundary, requires physical experiment) | — |
| Crush / drop | — | — | N/A | — |
| Cycle life | aging | — | N/A (aging model not run for this chemistry) | — |
| Rate-pulse internal resistance | — | — | N/A (DCR 0.0185 Ω from 1C discharge available as proxy) | `cell/T10_energy_dfn.json:dcr_ohm` |

## Conclusion

**Pass** on all task criteria: energy density ≥ 392.61 Wh/kg (426.89), 4C no plating (anode +0.0341 V), T_max ≤ 60 °C (51.4 °C), overcharge 4.7 V no thermal runaway (triggered=false).

Uncovered (paper limitations): nail penetration, crush, drop, cycle life, full temperature range — all beyond pure-simulation boundary.
