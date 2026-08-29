# Design Verification Plan and Report (virtual test version) - VBF-T8R2-DVPR-01

| Item | Condition | Result | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | run-pyamm 1C_discharge, DFN | 5.0351 Ah | record (no contract capacity threshold; ED derives from it) | cell/r3_VG_1c_dfn.json:capacity_ah |
| 5C discharge retention | run-pyamm 5C_discharge, DFN, same params | 0.9631 (5C 4.8492 Ah / 1C 5.0351 Ah) | PASS (>= 0.90, log entry 0 criterion) | cell/r3_VG_5c_dfn.json / cell/r3_VG_1c_dfn.json |
| Energy density | calc-energy chain (energy_wh / contract mass) | 483.4 Wh/kg | PASS (>= 446.18) | cell/r3_VG_energy.json:energy_density_wh_kg |
| Cell mass | contract caliber layer summation | 37.71 g | PASS (<= 40) | cell/r3_VG_energy.json:mass_kg |
| 4C fast-charge temperature rise | run-pyamm 4C_charge_45C, thermal lumped | T_max 351.93 K (+33.78 K vs 45 C ambient, 78.8 C) | record (no contract threshold) | cell/r3_VG_safety.json:T_max_K |
| 4C fast-charge plating | same run + plating | anode potential min 0.0215 V > 0 -> plated = False | PASS (plated == false, log entry 0 criterion) | cell/r3_VG_safety.json:anode_potential_v (min, mechanical) |
| Voltage window | parameter set limits | 2.5 - 4.2 V | record | parameter set |
| Nail penetration / overcharge-to-TR / crush / drop | - | N/A (beyond pure simulation boundary, requires physical experiment) | N/A | - |
| Cycle life | - | N/A (requires aging model run; not exercised - no durability criterion in contract) | N/A | - |
| Pulse internal resistance | - | N/A (requires physical experiment); curve-derived DCR available: 2.7305 mOhm (cell/r3_VG_energy.json:dcr_ohm, informational) | N/A | cell/r3_VG_energy.json |

## Conclusion

All thresholded verification items PASS (5C retention 0.9631 >= 0.90; ED 483.37 >= 446.18 Wh/kg; mass 37.71 <= 40 g; plating False at 4C/45 C). Uncovered items (abuse tests, cycle life, pulse DCR) are listed above as N/A beyond the pure-simulation boundary - cited for the paper limitations section.