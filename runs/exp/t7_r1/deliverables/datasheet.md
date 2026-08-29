# Technical Datasheet — HEV Fast-Charge Pouch Cell (Case t7_r1)

Document: VBF-T7R1-DSH-01 · Prepared 2026-08-25 · Signature: Prepared ______ / Reviewed ______ / Approved ______

| Field | Value | Source |
|---|---|---|
| Rated capacity | 6.03 Ah (nominal 6.0313 Ah; simulated 6.032209 Ah, DFN) | params_v11.json; cell/r5_v11_1c_dfn.json:capacity_ah |
| Nominal voltage / voltage window | 3.72 V (discharge midpoint) / 2.5 – 4.2 V | cell/r5_v11_energy.json:midpoint_voltage_v; parameter set |
| Rated energy | 21.797 Wh (1C discharge integration) | cell/r5_v11_energy.json:energy_wh |
| Gravimetric energy density | 483.25 Wh/kg (contract formula, electrolyte excluded) | cell/r5_v11_energy.json:energy_density_wh_kg |
| Volumetric energy density | 920.38 Wh/L | cell/r5_v11_energy.json:energy_density_wh_l |
| Maximum continuous discharge rate | 1C (6.03 A) — simulated at 25 °C ambient; higher rates not adjudicated | cell/r5_v11_1c_dfn.json |
| Fast-charge capability | 4C (24.1 A) at 45 °C ambient: no lithium plating (anode surface min +0.0476 V); max cell temperature 330.13 K (56.98 °C) | cell/r5_v11_4c45.json |
| DC internal resistance (DCR) | 2.882 mΩ | cell/r5_v11_energy.json:dcr_ohm |
| Power density | 32 559.7 W/kg | cell/r5_v11_energy.json:power_density_w_kg |
| Operating temperature range | Verified by simulation at 298.15 K (1C discharge) and 318.15 K (4C charge, 100-cycle aging). Other temperatures: not simulated. | run outputs (ambient per protocol) |
| Cycle life (SEI) | SEI thickness 465.47 nm after 100 cycles at 45 °C (≤ 550 nm limit). Cycle count to failure beyond 100 cycles: **not simulated** (aging model runs 100 cycles only). | cell/r5_v11_aging45.json:sei_thickness_nm_end |
| Cycle-life capacity trajectory | Per-cycle capacities show a model artifact (thick SEI film resistance dominates at µm-scale film); the adjudicable metric is sei_thickness_nm_end — see DVPR note. | cell/r5_v11_aging45.json; evaluate R3–R5 notes |
| Safety — fast charge | No plating at 4C/45 °C (anode potential never below 0 V) | cell/r5_v11_4c45.json |
| Safety — nail penetration | 10 W short-circuit heat source, virtual TR test: thermal runaway NOT triggered (T_max 336.32 K = 63.17 °C; dT/dt max 0.245 K/s), with h = 50 W/(m²·K) cooling (hA = 0.2655 W/K). Cooling floor: h ≈ 40 W/(m²·K) (h=30 triggers at 666 s per sensitivity run r5_v8_nail_h30). Physical nail test: N/A (requires experiment). | cell/r5_v11_nail.json; cell/r5_v8_nail_h30.json |
| Dimensions | Electrode stack: 65 mm × 1580 mm × 0.2306 mm (parameter-set pouch geometry; shell not modeled) | parameter set; cell/r5_v11_energy.json:thickness_m |
| Mass | 45.11 g cell stack (contract, electrolyte excluded); +8.92 g electrolyte (literature estimate) ≈ 54.03 g total | cell/r5_v11_energy.json:mass_kg; process formula |
| Charge voltage limit | 4.2 V (parameter set) | parameter set |

Notes: all values are virtual — simulated with PyBaMM (DFN for rated data) and the three-side-reaction thermal-runaway ODE; no physical cell was built or tested. True first-principles (DFT/MD) endorsement skipped: real_compute = false (entry 0).
