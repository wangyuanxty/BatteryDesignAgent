# Design Verification Plan and Report (virtual test) — VBF-T1R1FLASH-DVPR-01

Case: next-generation BEV sedan battery · Generation date: 2026-08-25

## Verification items (all from bda simulation; sources file:key)

| # | Item | Condition | Result | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC to 2.5 V, 25 °C, DFN | 4.936 Ah | informational (nominal 5.0 Ah) | cell/final_1c_dfn.json:capacity_ah |
| 2 | Discharge energy | trapezoid ∫V·I dt | 17.51 Wh | — | cell/final_energy.json:energy_wh |
| 3 | Gravimetric energy density | contract caliber (electrolyte excluded) | 459.41 Wh/kg | PASS vs ≥392.61 | cell/final_energy.json:energy_density_wh_kg |
| 4 | Volumetric energy density | contract caliber | 893.5 Wh/L | informational | cell/final_energy.json:energy_density_wh_l |
| 5 | 4C fast-charge temperature rise | 4C charge, 45 °C ambient, lumped thermal, DFN | T_max 323.39 K (50.2 °C) | PASS vs ≤333.15 K | cell/archA_h150_f4b_4c.json:T_max_K |
| 6 | 4C fast-charge plating | same + plating module; anode potential ≥ 0 V | anode min +0.0114 V, plated=false | PASS | cell/archA_h150_f4b_4c.json:anode_potential_v |
| 7 | Cooling robustness | 4C at h=120 W/m²·K | T_max 324.55 K, anode min +0.0123 V | PASS (margin preserved) | cell/archA_h120_f4b_4c.json |
| 8 | Voltage window | parameter set | 2.5–4.2 V | PASS | OKane2022 params |
| 9 | Overcharge to 4.7 V | 0.5C charge to cutoff+0.5 V (4.7 V), then TR ODE | overcharge T_max 299.12 K; triggered=false | PASS (no thermal runaway) | cell/final_oc.json:T_max_K; cell/final_tr.json:triggered |
| 10 | DC resistance | (OCV − V@10% DOD)/I | 20.3 mΩ | informational | cell/final_energy.json:dcr_ohm |

## Items NOT covered (beyond pure-simulation boundary, require physical experiment)

Nail penetration, crush, drop, cycle life / calendar aging (aging model not part of this task's criteria), rate-pulse internal resistance, electrolyte oxidation voltage-window endorsement (real_compute=false), production-level formation tuning.

## Conclusion

All simulated verification items PASS vs the entry-0 contract (ED ≥ 392.61 Wh/kg; T_max ≤ 333.15 K; plated=false; overcharge→TR triggered=false). Uncovered items listed above are the honest boundary of this virtual-design package.
