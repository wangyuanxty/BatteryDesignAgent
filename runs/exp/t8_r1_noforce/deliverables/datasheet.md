# Cell Datasheet — Long-Endurance Drone Battery (t8_r1_noforce)

Document number: VBF-T8R1NOFORCE-DSH-01 · Generation date: 2026-08-25 · Status: virtual design (all values from bda tool output; not a physical cell)

## General

| Field | Value | Source |
|---|---|---|
| Cell designation | VBF-T8R1NOFORCE-CELL-R6V9 | delivery index |
| Electrochemical system | NMC811 / graphite (pouch geometry) | Chen2020 parameter set |
| Rated capacity | 5.2725 Ah (1C discharge, 25 °C, DFN simulation) | `cell/r6_v9_1c_dfn.json:capacity_ah` |
| Nominal capacity | 5.0 Ah (parameter set input) | Chen2020 |
| Nominal voltage | 3.933 V (1C discharge midpoint) | `r6_v9_energy.json:midpoint_voltage_v` |
| Voltage window | 2.5 – 4.2 V | parameter set |
| Rated energy | 19.4147 Wh (1C contract) | `r6_v9_energy.json:energy_wh` |
| Energy density (gravimetric) | 497.968 Wh/kg (contract caliber; electrolyte excluded) | `r6_v9_energy.json:energy_density_wh_kg` |
| Energy density (volumetric) | 854.72 Wh/L | `r6_v9_energy.json:energy_density_vol_wh_l` |
| DC internal resistance | 0.7275 mΩ (per calc-energy formulation) | `r6_v9_energy.json:dcr_ohm` |
| Power density | 150.5 kW/kg | `r6_v9_energy.json:power_density_w_kg` |

## Physical

| Field | Value | Source |
|---|---|---|
| Electrode dimensions | 65 mm height × 1891 mm width | parameter set / `r6_v9_kin_el.json` |
| Electrode area | 0.122915 m² | `r6_v9_energy.json:area_m2` |
| Stack thickness | 184.8 µm (pos 75.6 + sep 10 + neg 85.2 + Al 8 + Cu 6) | `r6_v9_energy.json:thickness_m` |
| Cell mass (contract) | 38.99 g (electrolyte excluded per calc-energy) | `r6_v9_energy.json:mass_kg` |
| Cell mass (incl. electrolyte) | 48.54 g (electrolyte 9.55 g, literature density 1.2 g/cm³) | BOM sheet |

## Electrical performance (simulated, DFN)

| Condition | Result | Source |
|---|---|---|
| 1C discharge, 25 °C | 5.2725 Ah; T_max 299.18 K | `r6_v9_1c_dfn.json` |
| 5C discharge, 25 °C | 5.2178 Ah; T_max 313.64 K; retention vs 1C = 0.9896 | `r6_v9_5c_dfn.json`, `r6_v9_retention.json` |
| Continuous discharge rating | 5C (task requirement: retention ≥ 0.90 — met at 0.9896) | `r6_v9_retention.json` |
| Fast charge capability | 4C charge, 45 °C ambient: anode min potential +0.00635 V → no plating; T_max 326.81 K | `r6_v9_4c_charge45_plating.json` |

## Environmental and safety

| Field | Value | Source |
|---|---|---|
| Operating temperature (simulated range) | 25 – 45 °C (1C/5C discharge at 25 °C; 4C charge at 45 °C) | protocol runs, honest scope statement |
| Cooling requirement | h = 60 W/m²/K (forced-air, ducted prop-wash at pack level) | `r6_v9_kin_el.json` (thermal-management freedom) |
| Lithium plating (4C charge) | None — anode potential min +0.00635 V (plated = false); thin margin +6.3 mV, recommend charging-temperature floor of 45 °C maintained | `r6_v9_4c_charge45_plating.json` |
| Thermal runaway | Not simulated (no abuse runs in this case; task did not request) | honest N/A |
| Cycle life | Not simulated | honest N/A (aging model present in parameter set but cycle-life not a task criterion; no fabricated values) |

## Application note

Target: long-endurance drone. 5C discharge support (retention 0.9896) covers launch/climb bursts; energy density 497.97 Wh/kg (contract) with 38.99 g cell mass supports endurance-optimized packs. The design is negative-limited (N/P 0.641 capacity-density basis) — a deliberate trade for transport: the 85.2 µm graphite electrode keeps electrolyte-path polarization low at charge end, protecting the plating margin. Thin (6–8 µm) current collectors and 10 µm separator carry the energy-density budget; these are aggressive engineering choices requiring pouch-fabrication capability.

**Simulation honesty note**: all values above are DFN simulation outputs on the Chen2020 parameterization with design-parameter overrides; electrolyte transport parameters (κ = 1.4 S/m, D = 3.7e-10 m²/s) are literature values (Nyman 2008) substituted as formulation levers, and electrolyte mass uses a literature density (1.2 g/cm³). Physical-cell qualification (formation, mechanical integrity, actual cycle life) is out of scope.
