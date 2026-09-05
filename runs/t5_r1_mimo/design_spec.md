# Design Specification — Candidate E2

## Selection basis

Candidate E2 was selected because it satisfies all three task targets:

1. Energy density >= 500.94 Wh/kg.
2. 4C fast charge without lithium plating.
3. Maximum temperature <= 60C.

## Final design parameters

| Parameter | Value | Unit |
| --- | --- | --- |
| Positive electrode thickness | 9.828e-05 | m |
| Negative electrode thickness | 0.00011076 | m |
| Separator thickness | 8e-06 | m |
| Positive electrode porosity | 0.35 | - |
| Negative electrode porosity | 0.27 | - |
| Positive CC thickness | 1e-05 | m |
| Negative CC thickness | 8e-06 | m |
| Positive particle radius | 3.45e-06 | m |
| Negative particle radius | 3.86e-06 | m |
| Heat transfer coefficient | 60.0 | W.m-2.K-1 |
| Electrolyte diffusivity | 8.2e-10 | m2.s-1 |
| Electrolyte conductivity | 1.35 | S.m-1 |
| Cation transference number | 0.4 | - |

## Performance summary

| Metric | Value | Unit |
| --- | --- | --- |
| Energy density | 517.8298883826939 | Wh/kg |
| Volumetric energy density | 975.3875141711424 | Wh/L |
| Nominal capacity | 6.543863466458118 | Ah |
| Discharge energy | 23.544496852671656 | Wh |
| Cell active mass | 0.045467628232520006 | kg |
| Active stack thickness | 0.00023504000000000003 | m |
| 4C max temperature | 330.86233607651576 | K |
| 4C min anode potential | 4.0244993311427946e-05 | V |

## Notes

- The final design uses an architecture-first tuning path within the Chen2020 baseline system.
- Electrolyte density was not included in the mass calculation due to parameter-set limitations.
- The recommended design assumes enhanced cooling relative to the default contract baseline.
