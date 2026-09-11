# VBF-T9R4-BOM-001 Bill of Materials

t9_r4 - grid-storage cell cathode on the Chen2020 NMC811/graphite profile
Result: HONEST NEGATIVE (no candidate satisfies the full contract; nothing reported as passing)

Fixed cell stack (Chen2020 baseline, unchanged by design - the cathode composition is the only
free variable):

| Item | Specification | Source |
|---|---|---|
| Positive current collector | Al, 16 um | Chen2020 |
| Negative current collector | Cu, 12 um | Chen2020 |
| Positive electrode coating | 75.6 um, eps_am 0.665, rho 3262 kg/m3 (NMC811 baseline) | Chen2020 |
| Negative electrode | 85.2 um, eps_am 0.75, graphite rho 1657 kg/m3 | Chen2020 |
| Separator | 12 um, porosity 0.47 | Chen2020 |
| Electrolyte | EC/EMC + LiPF6 (anodic limit 4.8 V) - FIXED | contract |
| Cathode active material | NOT RESOLVED - no candidate passed; screening space: 42 layered LiMO2 compositions | negative result |
| Electrode area | 0.1027 m2 (0.065 x 1.58 m); nominal 5.0 Ah | Chen2020 |

Screened cathode-active candidates (3 run-comp batches, all layered LiMO2 prototypes):
round 1: LiCuO2, LiFeO2, CuNi55, CuMn55, CuFe55, CuCo55, NiFe55, CoFe55, FeMn55, LiVO2,
CuAl91, CuZr91, CuMn73, CuNi82; round 2: LiScO2, LiAlO2, LiGaO2, LiZnO2, FeNi73, FeNi37,
CrFe55, CrNi55, CrCo55, FeCo91, NiFe91, FeNi91, ZnNi55, ScFe55; round 3: LiBO2, AlB55, AlB73,
AlB91, BAl73, BAl91, AlB82, AlB64, AlB95, GaAl55, AlSc55, BGa55, BSc55, GaAl91.
All rejected (window, compatibility, or both).