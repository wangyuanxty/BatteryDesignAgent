# Battery Datasheet - G2_kappa0175

**Case**: t6_r1_singlemodel | **Document**: VBF-T6R1SINGLEMODEL-DSH-001 | **Model**: SPMe (the DFN cross-check noted)

## Electrical

| Parameter | Value | Condition |
|---|---|---|
| Nominal capacity | 5.4142 Ah | 1C discharge to 2.5 V |
| Discharge midpoint voltage | 4.2078 V | 1C |
| Volumetric energy density | 1107.02 Wh/L | the calc-energy output |
| Gravimetric energy density | 477.18 Wh/kg | the calc-energy output |
| Cell mass / volume | 47.4 g / 20.44 cm3 | |
| Thickness | 199 um | the stack |
| DC resistance | 5.39307e-07 ohm | the calc-energy output |

## Fast charge (the 4C protocol: the 1C discharge to 2.5 V, then the 4C charge to 4.7 V, the 45 degC ambient)

| Parameter | Value | Note |
|---|---|---|
| 4C charge duration | 64.7 s | to the 4.7 V voltage limit |
| 4C charge capacity | 0.0719 Ah (1.33% of the nominal) | voltage-limited |
| Lithium plating | NONE (the anode surface potential min +0.0454 V) | the whole protocol |
| Max temperature | 321.442 K | <= 323.15 K (50 degC) PASS |

## Aging (the 1C x 100 cycles at the 45 degC, the SEI growth)

| Parameter | Value |
|---|---|
| SEI thickness after 100 cycles | 133.56 nm (<= 500 nm PASS) |

## Verification note

DFN cross-check: model DFN, T_max 321.238 K, anode surface potential min 0.0071 V (plated: False), capacity metric 0.3954 Ah.

## Honest limitations

The 4C fast-charge profile is voltage-limited: the charge terminates after ~65 s at
the 4.7 V limit with ~1.3% of the capacity delivered. The no-plating margin is
45 mV on the anode surface potential. The electrolyte conductivity
0.175 S/m is an extreme low-salt/quasi-solid formulation point.
