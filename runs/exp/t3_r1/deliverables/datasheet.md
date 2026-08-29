# Technical Datasheet — VBF-T3R1-DSH-001

## Product

| Item | Value | Source |
|---|---|---|
| Cell designation | V12_BalancedCooling (power-tool high-rate cell) | cell/p_v12.json |
| Chemistry | NMC811 / graphite, LiPF6 EC/EMC electrolyte | Chen2020 base |
| Nominal capacity | 3.08 Ah (measured 1C: 3.075 Ah) | p_v12 / r4_v12_1c.json |
| Nominal energy | 11.09 Wh | calc-energy |
| Cell mass | 29.26 g (electrolyte excluded by contract) | calc-energy |
| Dimensions (active stack) | 0.065 m x 1.58 m x 132 um | Chen2020 / layer sum |
| Voltage window | 2.5 - 4.2 V | Chen2020 |

## Rated performance (DFN-verified)

| Specification | Rated | Measured | Margin | Source |
|---|---|---|---|---|
| Capacity @ 1C, 25 C | >= 2.0 Ah | 3.075 Ah | +1.075 Ah | r4_v12_1c.json |
| 5C discharge retention (5C cap / 1C cap) | >= 95 % | 97.53 % | +2.53 pp | r4_v12_derived.json |
| Max temperature, 4C charge @ 45 C amb | <= 60 C | 56.62 C | 3.38 C below red line | r4_v12_4c.json |
| Plating at 4C charge | none | none (anode potential min +12.1 mV vs 0 V) | 12.1 mV | r4_v12_4c.json |
| Power density | >= 4000 W/kg | 32630 W/kg | x8.2 | calc-energy |

## Additional characteristics

| Item | Value | Source |
|---|---|---|
| Energy density | 379.0 Wh/kg (gravimetric), 818.2 Wh/L (volumetric) | calc-energy |
| DC resistance (10% discharge) | 4.41 mOhm | calc-energy |
| Discharge midpoint voltage | 3.844 V | calc-energy |
| 5C discharge capacity | 2.999 Ah | r4_v12_5c.json |
| 4C CC charge capacity (to 4.2 V) | 0.808 Ah (CV phase required for full charge) | r4_v12_4c.json |

## Recommended operating conditions

- Continuous discharge: up to 5C (15.4 A); Fast charge: 4C CC (12.32 A) with CV taper, ambient <= 45 C.
- Cooling: heat transfer >= 20 W/m2/K (tool-body conduction + light airflow) — required to keep T <= 60 C.
- Charge termination 4.2 V; discharge cut-off 2.5 V.
