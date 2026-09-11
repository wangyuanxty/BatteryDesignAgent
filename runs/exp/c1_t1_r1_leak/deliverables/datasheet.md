# Cell Datasheet - R4-V3-margin (champion)
VBF-C1T1R1-DSH-001 | Case c1_t1_r1 | Virtual Battery Factory

## General
| Item | Value | Source |
|---|---|---|
| System | NMC811 / graphite (Chen2020 base), 4.2 V upper cut-off | parameter dump |
| Cell area | 0.1027 m2 (0.065 x 1.58 m) | calc-energy output |
| Cell mass | 35.603 g | calc-energy output |
| Cell thickness | 182.8 um | calc-energy output |
| 1C current | 5 A | contract |

## Electrical
| Item | Value |
|---|---|
| Contract capacity | 5.0306 Ah |
| Contract energy | 17.8975 Wh |
| Gravimetric energy density | 502.70 Wh/kg (threshold 392.61: PASS) |
| Volumetric energy density | 953.34 Wh/L |
| Midpoint voltage | 4.0073 V |
| DCR | 0.14679 mOhm |
| Power density | 797.3 kW/kg |

## Fast charge (4C = 20 A, 45 C ambient, SPMe + lumped thermal)
| Item | Value |
|---|---|
| T_max | 323.98 K = 50.83 C (threshold 60 C: PASS) |
| Anode potential minimum | +0.0503 V (>= 0 V: no lithium plating) |

## Abuse tolerance
| Item | Value |
|---|---|
| Overcharge protocol (0.5C to upper cut-off + 0.5 V) | reached 4.70 V |
| Overcharge T_max | 299.45 K |
| Thermal runaway model (run-tr --sim coupling, mass 0.0356025 kg) | triggered = false; T_max 299.45 K |

## Key design parameters (overrides over Chen2020)
Positive CC 8 um (Al); negative CC 6 um (Cu); separator 8 um / porosity 0.55;
t+ 0.7; D_e 2e-9 m2/s; kappa 3.0 S/m; negative particle radius 3 um; h = 100 W/m2/K.
