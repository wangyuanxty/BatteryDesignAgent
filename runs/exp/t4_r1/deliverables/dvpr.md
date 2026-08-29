# Design Verification Plan and Report (virtual test version) — VBF-T4R1-DVPR-01

One row per verification item; result values from simulation outputs; uncovered conditions honestly marked N/A.

| Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C constant-current discharge, 25 °C, 2.5 V cutoff | 5.0368 Ah | pass (vs nominal 5.0 Ah: 100.7 %) | cell/r6_t2_1c_dfn.json:capacity_ah |
| −20 °C 1C capacity retention | 1C discharge, 253.15 K cold-soaked start, h = 80 (self-heating removed) | 0.99267 | pass (≥ 0.95) | cell/r6_t2_retention.json:lowT_retention |
| Energy density | contract formula (∫V·I dt / Σ layer thickness×(1−ε)×density×area) | 471.55 Wh/kg | pass (≥ 327.18) | cell/r6_t2_energy.json:energy_density_wh_kg |
| Volumetric energy density | energy ÷ stack volume (188.8 µm × 0.1027 m²) | 925.77 Wh/L | pass (≥ 880) | cell/r6_t2_energy.json:energy_density_wh_l |
| 4C fast-charge temperature rise | 4C charge after 1C discharge to 2.5 V, 45 °C ambient, lumped thermal | T_max 327.70 K (+9.6 K above ambient) | pass (≤ 333.15 K) | cell/r6_t2_4c45C_dfn.json:T_max_K |
| 4C fast-charge plating | same protocol, plating submodel | anode potential min +0.0205 V (≥ 0 V) | pass (no plating) | cell/r6_t2_4c45C_dfn.json:anode_potential_v |
| Voltage window | parameter-set cut-offs | 2.5 – 4.2 V | pass (per design) | Chen2020 parameter set |
| DC resistance | calc-energy DCR caliber | 4.06 mΩ | informational (no threshold) | cell/r6_t2_energy.json:dcr_ohm |

Items explicitly N/A (beyond pure simulation boundary, require physical experiment): nail penetration; overcharge to thermal runaway; crush; drop; cycle life (no aging model); rate-pulse internal resistance.

## Conclusion

All seven simulation-based verification items pass against the entry-0 criteria. Uncovered items (mechanical abuse, cycle life, pulse resistance) are outside the pure-simulation boundary and require physical prototypes — listed above for the paper's limitations section. The −20 °C retention value is computed under the flat-transport design-target profile (LHCE-class idealization); physical confirmation of electrolyte conductivity at −20 °C is recommended.
