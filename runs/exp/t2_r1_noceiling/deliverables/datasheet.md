# Datasheet - Grid Energy Storage Cell L "AnPorUp" (VBF-T2R1NOCEILING-DSH-003)

Case t2_r1_noceiling | Chen2020 NMC811/graphite SPMe | Best-effort design (negative result case)

## Cell-level specifications (calc-energy output, 1C reference)

| Item | Value |
|---|---|
| Nominal capacity (measured 1C) | 4.9506 Ah |
| 1C discharge capacity (at nominal) | 4.9520 Ah |
| Discharge energy (1C) | 17.4766 Wh |
| Gravimetric energy density | 476.72 Wh/kg |
| Volumetric energy density | 891.88 Wh/L |
| Cell mass (layers, electrolyte excluded) | 36.660 g |
| Stack thickness | 190.8 um |
| Electrode area | 0.1027 m2 |
| Cell volume (stack x area) | 19.60 cm3 |
| Midpoint voltage (1C) | 3.9474 V |
| DC resistance (tool definition) | 0.199 mOhm |
| Power density (tool formula) | 558.7 kW/kg |

## Layer stack

| Layer | Thickness um | Porosity | Areal mass kg/m2 | Mass g |
|---|---|---|---|---|
| Positive electrode (NMC811) | 75.6 | 0.335 | 0.163994 | 16.84 |
| Negative electrode (graphite) | 85.2 | 0.35 | 0.091765 | 9.42 |
| Positive current collector (Al) | 10.0 | - | 0.027000 | 2.77 |
| Negative current collector (Cu) | 8.0 | - | 0.071680 | 7.36 |
| Separator | 12.0 | 0.47 | 0.002525 | 0.26 |
| **Total** | 190.8 | | | 36.66 |

Electrolyte: excluded from mass and volume (parameter set lacks density - tool note).

## Operating envelope (measured)

| Condition | Result |
|---|---|
| 1C discharge, 25 C | 4.9520 Ah to 2.5 V |
| 1C discharge, -20 C ambient (from 25 C initial) | 4.9242 Ah; retention 0.9944 vs 1C |
| 4C charge, 45 C ambient, after full 1C discharge | 0.0461 Ah in 8.4 s to 4.2 V abort; T_max 333.2 K; min anode surface potential difference -0.3868 V (plating risk: FAIL) |
| 1C cycling, 100 cycles, 25 C | SEI thickness 467.6 nm (<= 500 PASS) |
| 1C cycling, 500 cycles, 25 C | SEI thickness 811.3 nm (<= 550 FAIL) |

## Honest limitations

- 4C fast charge is NOT supported: the 4C charge terminates at 4.2 V after ~8.4 s (~0.9% SOC)
  and the anode surface potential difference goes negative (plating onset) - see DFMEA FM1.
- SEI at 500 cycles exceeds the 550 nm target - see DFMEA FM2.
- Energy density excludes electrolyte mass (overestimate vs a built cell).
