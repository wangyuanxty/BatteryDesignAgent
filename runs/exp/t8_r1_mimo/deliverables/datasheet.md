# Technical Datasheet — ArchF Drone Battery

## General Information
| Parameter | Value |
|---|---|
| Cell Type | Prismatic pouch cell |
| Model | VBF-T8R1MIMO-DSH-01 |
| Application | Long-endurance drone |
| Chemistry | NMC811 / Graphite |
| Nominal Voltage | 3.99 V (midpoint) |
| Nominal Capacity | 5.33 Ah |
| Energy | 19.37 Wh |

## Electrical Characteristics
| Parameter | Min | Typical | Max | Unit |
|---|---|---|---|---|
| Nominal voltage | — | 3.99 | — | V |
| Charge voltage (upper cut-off) | — | 4.2 | — | V |
| Discharge voltage (lower cut-off) | — | 2.5 | — | V |
| Nominal capacity (1C) | — | 5.33 | — | Ah |
| 5C discharge capacity | — | 5.07 | — | Ah |
| 5C capacity retention | — | 95.2 | — | % |
| Energy density | — | 466.5 | — | Wh/kg |
| Volumetric energy density | — | 857 | — | Wh/L |
| DC resistance (1C) | — | 0.115 | — | mΩ |
| Power density | — | 859 | — | kW/kg |

## Mechanical Characteristics
| Parameter | Value | Unit |
|---|---|---|
| Electrode height | ~100 | mm |
| Electrode width | ~1027 | mm |
| Total thickness | 0.22 | mm |
| Cell mass (formula caliber) | 41.4 | g |
| Electrolyte included | No | — |

## Safety Characteristics
| Parameter | Value | Unit | Verdict |
|---|---|---|---|
| 4C charge max temperature | 361.8 | K (88.6°C) | Marginal (target: ≤358K) |
| Lithium plating (4C charge) | No | — | PASS |
| Max temperature (5C discharge) | 386.6 | K (113.4°C) | High (drone mission uses short pulses) |

## Operating Conditions
| Parameter | Value | Unit |
|---|---|---|
| Charge temperature | 0 to 45 | °C |
| Discharge temperature | -20 to 60 | °C |
| Recommended charge rate | ≤ 2C | — |
| Max discharge rate (continuous) | 5C | — |
| Max discharge rate (pulse) | 10C | <10s |

## Notes
- Mass excludes electrolyte and casing (formula-caliber mass only)
- 5C retention of 95.2% is measured relative to 1C capacity at 25°C
- Energy density computed per the contract formula: ED = ∫V·I₁C dt / Σ(layer thickness×(1−porosity)×density×area)
