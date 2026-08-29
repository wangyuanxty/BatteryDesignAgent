# Technical Datasheet — LNMO High-Voltage Smartphone Cell

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 4.5 (nominal) / 6.372 (simulation-verified 1C) | parameter set + `r5_d11_1c.json` |
| Nominal voltage / voltage window (V) | 4.17 / 2.5–4.7 | `r5_d11_energy.json:midpoint_voltage_v` + parameter set |
| Rated energy (Wh) | 26.48 | `r5_d11_energy.json:energy_wh` (V·I time integral) |
| Energy density — gravimetric (Wh/kg) | 596.5 | `r5_d11_energy.json:energy_density_wh_kg` (electrolyte excluded) |
| Energy density — volumetric (Wh/L) | 1260.2 | `r5_d11_energy.json:energy_density_wh_l` (electrolyte excluded) |
| Maximum continuous discharge rate | 1C (6.37 Ah) | `r5_d11_1c.json` (1C discharge protocol) |
| Fast-charge capability | 4C CC charge, no plating (anode min +0.043 V), T_max 321.68 K | `r5_d11_4c.json` (4C_charge_45C + plating, lumped thermal) |
| Operating temperature range | 25 °C–45 °C (simulated); upper bound = 4C-charge ambient | protocol conditions |
| Cycle life | **Not simulated beyond 100 cycles; SEI 193.6 nm after 100×1C cycles** | `r5_d11_aging.json` |
| Safety determination | no lithium plating at 4C; T_max 321.68 K (≤ 323.15 K) | `r5_d11_4c.json` |
| DC resistance (Ω) | 0.0105 | `r5_d11_energy.json:dcr_ohm` |
| Dimensions | electrode 65 mm × 1580 mm (unwound); layer stack 204.6 µm | parameter set + `r5_d11_energy.json` |
| Mass (g) | 44.4 (electrolyte/casing excluded) | `r5_d11_energy.json:mass_kg` |

> Notes: gravimetric/volumetric energy density and mass use the contract-caliber formula (electrolyte and casing excluded, per `calc-energy`). Cycle life beyond 100 cycles is not simulated (no extended aging model run); the value shown is the 100-cycle SEI thickness.
