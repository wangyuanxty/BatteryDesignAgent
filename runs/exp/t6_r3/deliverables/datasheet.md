# Datasheet — Smartphone High-Voltage Fast-Charge Cell V27_combo

| Doc No: VBF-T6R3-DSH-01 | Case: t6_r3 | Rev: 01 | Date: 2026-08-26 |

## Electrical

| Item | Value | Condition | Source |
|---|---|---|---|
| Nominal capacity | 5.0569 Ah | 1C discharge, 4.7 -> 2.5 V, DFN | r10_V27_combo_1c.json capacity_ah |
| Rated energy | 21.1125 Wh | discharge integral | r10_V27_combo_energy.json energy_wh |
| Voltage plateau (midpoint) | 4.1551 V | contract metric (calc-energy) | r10_V27_combo_energy.json midpoint_voltage_v |
| Upper / lower cut-off | 4.7 V / 2.5 V | LNMO window | LNMO.json |
| Initial cell voltage (model initial state) | 4.1995 V | cell born nearly full | r10_V27_combo_1c.json voltage_v[0] |
| DC resistance (DCR) | 4.986 mOhm | calc-energy | r10_V27_combo_energy.json dcr_ohm |

## Energy and power density

| Item | Value | Formula / basis | Source |
|---|---|---|---|
| Volumetric energy density | 983.61 Wh/L | energy / stack volume (21.4643 mL) | r10_V27_combo_energy.json energy_density_wh_l |
| Gravimetric energy density | 442.80 Wh/kg | energy / dry mass (47.6800 g) | r10_V27_combo_energy.json energy_density_wh_kg |
| Power density | 18544.4 W/kg | calc-energy | r10_V27_combo_energy.json power_density_w_kg |
| Cell thickness | 209 um | stack sum | r10_V27_combo_energy.json thickness_m |
| Dry / wet mass | 47.6800 g / 54.2105 g | wet = dry + electrolyte pore fill | calculated from layers |

## Fast charge (4C, 18 A) and thermal

| Item | Value | Note | Source |
|---|---|---|---|
| Max cell temperature | 318.922 K = 45.77 C | limit 50 C (323.15 K); margin 4.23 K | r10_V27_combo_4c.json T_max_K |
| Min anode potential | +0.1050 V | >= 0 V required; no lithium plating | r10_V27_combo_4c.json anode_potential_v |
| 4C CC phase duration | ~16.2 ms | cell starts at 4.1995 V -> 4.7 V cut-off reached almost immediately; charge adds 8.09e-05 Ah (protocol artifact, disclosed — see DVPR row 8) | derived: Q4C/18A |
| 1C max temperature | 299.034 K | reference | r10_V27_combo_1c.json T_max_K |

## Cycle life / durability

| Item | Value | Note | Source |
|---|---|---|---|
| Anode SEI thickness after 100 cycles | 313.7 nm | limit 500 nm; margin 186.3 nm | r10_V27_combo_aging.json sei_thickness_nm_end |
| Initial SEI thickness | 5 nm | Chen2020 base | Chen2020.py:240 |
| Capacity trajectory | cycle 1: -0.618 Ah -> cycle 100: 2.732 Ah | SEI-model lithium-inventory climb artifact; NOT a real capacity gain; durable metric is SEI thickness | r10_V27_combo_aging.json capacity_ah_per_cycle |

## Composition (dry cell, contract basis)

| Component | Mass | Share |
|---|---|---|
| LNMO spinel active (positive) | 17.3088 g | 36.3 % |
| Graphite active (negative) | 13.2161 g | 27.7 % |
| Carbon black conductive additive | 0.7780 g | 1.6 % |
| PVDF binder | 0.3606 g | 0.8 % |
| SBR/CMC binder | 0.2782 g | 0.6 % |
| Separator (polyolefin, 12 um) | 0.2593 g | 0.5 % |
| Aluminium foil (16 um) | 4.4366 g | 9.3 % |
| Copper foil (12 um) | 11.0423 g | 23.2 % |

Electrolyte 6.5305 g (5.44 mL pore volume at 1.2 g/mL) is excluded from the contract mass and energy-density basis (electrolyte_included=False in energy output).

## Notes

- All performance values are DFN simulation outputs (model_used=DFN). No physical cell exists; no true DFT/MD was run (real_compute=false, endorse skipped honestly).
- Nominal reference capacity of the base set is 4.5 Ah [LNMO.json]; the simulated 1C discharge yields 5.0569 Ah under the 2.5-4.7 V window.
- N/P (layer capacity ratio) = 1.5787, first-principles formula; early probe labels used a thickness-scaled shorthand.