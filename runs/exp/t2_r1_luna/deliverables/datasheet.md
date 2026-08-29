# Technical datasheet

| Item | Value | Source |
|---|---:|---|
| Base parameter set | Chen2020 | deterministic protocol mapping |
| Energy density | 405.375 Wh/kg | `cell/r2_variant_energy.json:energy_density_wh_kg` |
| 1C capacity | 4.95633 Ah | `cell/r2_variant_1c.json:capacity_ah` |
| −20 °C capacity | 4.92932 Ah | `cell/r2_variant_lowt.json:capacity_ah` |
| −20 °C retention | 99.455% | inferred from the two capacities |
| 4C min anode potential | +0.04444 V | derived from `cell/r2_variant_4c.json:anode_potential_v` |
| 4C max temperature | 348.786 K | `cell/r2_variant_4c.json:T_max_K` |
| 100-cycle SEI | 300.359 nm | `cell/r2_variant_age100.json:sei_thickness_nm_end` |
| 500-cycle SEI | 333.097 nm | `cell/r2_variant_age500.json:sei_thickness_nm_end` |
