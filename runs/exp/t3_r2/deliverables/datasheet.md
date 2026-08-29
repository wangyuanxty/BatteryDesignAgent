# Technical Datasheet — VBF-T3R2-DSH-01

Power-tool battery cell — NMC811 | graphite pouch (virtual design, Chen2020-based simulation). Values mechanically taken from parameter set / simulation outputs; missing items honestly marked.

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 3.32 (nominal parameter); 3.328 (1C DFN measured) | `cell/r2_p1_params_final.json`; `cell/r2_p1_1c_dfn.json:capacity_ah` |
| Nominal voltage / voltage window (V) | window 2.5 – 4.2 V; discharge midpoint voltage 3.886 V | parameter set; `cell/r2_p1_energy.json:midpoint_voltage_v` |
| Rated energy (Wh) | 12.13 | `cell/r2_p1_energy.json:energy_wh` (time integration of V·I at 1C) |
| Energy density (Wh/kg) | 407.6 (contract caliber: cell mass excludes electrolyte) | `cell/r2_p1_energy.json:energy_density_wh_kg` |
| Volumetric energy density (Wh/L) | 837.4 | `cell/r2_p1_energy.json:energy_density_wh_l` |
| Maximum continuous discharge rate | 5C (16.61 A) verified: 98.89 % capacity retention, peak temperature 49.1 °C | `cell/r2_p1_derived.json:capacity_retention_5c`; `t_max_5c_k` |
| Fast-charge capability | 4C (13.29 A) charge at 45 °C ambient, 900 s protocol: no lithium plating (anode potential min +36.4 mV), peak temperature 59.4 °C (<= 60 °C limit) | `cell/r2_p1_4c_dfn.json:anode_potential_v`, `T_max_K` |
| DC internal resistance | 2.265 mOhm (start-OCV to 10 % -time drop over 1C current) | `cell/r2_p1_energy.json:dcr_ohm` |
| Peak power density | 63,130 W/kg (V_OC^2 / (4·DCR) / mass, contract formula) | `cell/r2_p1_energy.json:power_density_w_kg` |
| Operating temperature range | 25 °C discharge / 45 °C charge ambient verified by simulation; wider range not verified — quoted range is 25–45 °C (simulation conditions only) | protocol conditions of the run files |
| Cycle life | Not simulated (aging-capable parameter set available; not part of task contract) — must not be fabricated | honest annotation |
| Safety determination | 4C/45 °C fast charge: not plated, T_max within 60 °C; abuse scenarios (overcharge/nail/crush/drop) not simulated for this task — N/A beyond pure simulation boundary | `cell/r2_p1_4c_dfn.json` |
| Dimensions | electrode area 0.1027 m2 (0.065 m × 1.58 m); layer stack thickness 141 um; shell/footprint Not provided | parameter set + `cell/r2_p1_energy.json:thickness_m` |
| Mass | 29.75 g cell (contract caliber, electrolyte excluded; with literature-density electrolyte ~35.7 g) | `cell/r2_p1_energy.json:mass_kg` + BOM |

Notes: this datasheet describes a virtual cell designed and verified within the pure-simulation boundary (Model: DFN, lumped thermal, irreversible plating option). Physical prototyping, cycle life, calendar aging, mechanical abuse and pack integration are outside this boundary and must be verified experimentally before production.