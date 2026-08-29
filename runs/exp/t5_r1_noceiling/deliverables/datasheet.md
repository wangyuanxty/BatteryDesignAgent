# Technical Datasheet — VBF-T5R1NOCEILING-DSH-01

Cell: R4A MarginAnode1p0 (Chen2020 NMC811|graphite baseline + architecture overrides).
All values mechanically taken from the parameter set / simulation outputs; missing items honestly stated.

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 9.6251 (1C discharge to 2.5 V) | cell/r4_A_calc_dfn.json:capacity_ah |
| Nominal voltage (V) | 3.9016 (1C discharge midpoint) | cell/r4_A_calc_dfn.json:midpoint_voltage_v |
| Voltage window (V) | 2.5 - 4.2 | parameter set (Lower/Upper voltage cut-off) |
| Rated energy (Wh) | 35.446 | cell/r4_A_calc_dfn.json:energy_wh (time integration of V x I at 5 A) |
| Gravimetric energy density (Wh/kg) | 583.93 (SPMe cross-check 583.46) | cell/r4_A_calc_dfn.json:energy_density_wh_kg (contract formula) |
| Volumetric energy density (Wh/L) | 1042.10 | cell/r4_A_calc_dfn.json:energy_density_wh_l |
| Maximum continuous discharge rate | 1C (5 A nominal) simulated and clean to 2.5 V; rates above 1C not simulated | cell/r4_A_1c_dfn.json |
| Fast-charge capability | 20 A (4C protocol; 2.08C of true capacity) accepted: 8.12 Ah in 1461 s to the 4.2 V ceiling at 45 degC ambient; no lithium plating (anode surface min +0.0212 V); T_max 320.36 K | cell/r4_A_4c_dfn.json |
| Operating temperature (simulated conditions) | 1C discharge at 25 degC ambient; 4C charge at 45 degC ambient; T_max during 4C = 47.2 degC | protocol definitions; cell/r4_A_4c_dfn.json:T_max_K |
| Cycle life | Not simulated (requires aging model) — must not be treated as measured | honest omission |
| Safety determination | 4C no-plating PASS (anode min +0.0212 V > 0); temperature PASS (320.36 K <= 333.15 K); abuse tests (nail / overcharge / crush) not simulated | cell/r4_A_4c_dfn.json; log evaluate R4A DFN |
| DC internal resistance (Ohm) | 0.00109 | cell/r4_A_calc_dfn.json:dcr_ohm |
| Power density (W/kg) | 64930 | cell/r4_A_calc_dfn.json:power_density_w_kg |
| Dimensions (mm) | 65 (height) x 2370 (electrode width, single unwound layer) x 0.2208 (stack thickness); multilayer productization not modeled | parameter set + cell/r4_A_calc_dfn.json:thickness_m |
| Mass (g) | 60.70 (electrolyte excluded per contract mass formula) | cell/r4_A_calc_dfn.json:mass_kg |

