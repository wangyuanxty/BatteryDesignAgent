# Technical Datasheet — t8_r3 V13 porousanode (VBF-T8R3-DSH-01)

Virtual-design datasheet; values from parameter set and simulation outputs (no physical cell exists).

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah nominal (parameter set); 5.0728 Ah simulated 1C DFN | Chen2020; r4_V13_porousanode_1c_dfn.json |
| Nominal voltage / window | window 2.5–4.2 V; discharge midpoint 3.957 V | Chen2020 cut-offs; energy:midpoint_voltage_v |
| Rated energy | 18.568 Wh | energy:energy_wh (∫V·I dt, 1C DFN) |
| Energy density | 497.54 Wh/kg (962.7 Wh/L) | contract formula: energy ÷ calc-energy stack mass (electrolyte excluded) |
| Maximum continuous discharge | 5C verified: 5.005 Ah, retention 98.66% vs 1C | r4_V13_porousanode_5c_dfn.json / derived |
| Fast-charge capability | 4C/45 °C charge: T_max 326.53 K (limit 333.15) | 4c_safety:T_max_K |
| Operating temperature range | verified 298.15 K (discharge) and 318.15 K ambient (charge); 5C discharge peak cell temperature 314.0 K | protocol definitions; 5c_dfn:T_max_K |
| Cycle life | Not simulated (task has no cycle-life criterion; no aging protocol run) — must not be fabricated | log.jsonl stage4 note |
| Safety determination | no plating (anode min +0.0177 V); overcharge→thermal runaway ODE: triggered=False | 4c_safety / run-tr |
| Dimensions and mass | 65 × 1580 × 187.8 µm; stack 37.32 g (electrolyte excluded) + 6.79 g electrolyte fill | parameter set + energy:mass_kg |
| DC resistance (10% point) | 1.27 mΩ | energy:dcr_ohm |
