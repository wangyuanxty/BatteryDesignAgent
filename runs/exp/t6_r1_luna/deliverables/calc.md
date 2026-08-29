# Calculation Sheet — VBF-T6_R1_LUNA-CALC-001

## Contract calculation
For the baseline, `calc-energy` reports energy 17.3945221 Wh, mass 0.04345453 kg, volume 2.0622160e-05 m³, and 843.4869143 Wh/L. For Architecture-V3, the tool reports 895.5999365 Wh/L. Energy density is calculated by the simulation library as discharge-energy divided by active modeled volume; electrolyte is excluded.

## Safety conversion
Architecture-V3 T_max = 321.6325618 K − 273.15 = 48.4825618 °C.

## Audit sources
`cell/r1_baseline_energy.json`; `cell/r3_v3_energy.json`; `cell/r3_v3_safety.json`; `cell/r3_v3_aging.json`.
