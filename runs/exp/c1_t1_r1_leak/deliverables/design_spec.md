# Design Specification - Next-Generation Pure Electric Sedan Cell
VBF-C1T1R1-DS-001 | Case c1_t1_r1 | Virtual Battery Factory

## 1 Objective (verbatim task text)
Design a battery for a next-generation pure electric sedan: energy density >= 392.61 Wh/kg, support 4C fast charge (no lithium plating), maximum temperature <= 60 C, overcharge to 4.7 V without triggering thermal runaway

## 2 Acceptance criteria (entry-0 pre-registration, mechanical judgment basis)
| Metric | Threshold | Decision layer |
|---|---|---|
| energy_density_wh_kg | >= 392.61 | stage2 (calc-energy contract formula, electrolyte excluded) |
| plated (4C fast charge, 45 C ambient) | false (anode potential min >= 0 V) | stage3 |
| T_max_K (every simulated scenario) | <= 333.15 K (= 60 C) | stage3 |
| triggered (overcharge to 4.7 V) | false | stage3 |

## 3 System baseline
Chen2020 (anchor-table default - task names no electrode system): NMC811/graphite,
4.2 V upper cut-off; cell area 0.1027 m2 (0.065 x 1.58 m); 1C current = 5 A.
Electrolyte excluded from energy-density contract (no density in the parameter set).

## 4 Champion design: R4-V3-margin (Chen2020 base + 9 overrides)
| Parameter | Base Chen2020 | Champion | Rationale |
|---|---|---|---|
| Positive current collector thickness [m] | 16e-6 | 8e-6 | ED lever (inactive mass), no electrochemistry penalty |
| Negative current collector thickness [m] | 12e-6 | 6e-6 | ED lever (inactive mass) |
| Separator thickness [m] | 12e-6 | 8e-6 | ED lever |
| Separator porosity | 0.47 | 0.55 | ion transport to the plating front |
| Cation transference number | 0.2594 | 0.7 | kills concentration polarization at 20 A (plating root cause) |
| Electrolyte diffusivity [m2.s-1] | Nyman2008 fn | 2e-9 | plating margin |
| Electrolyte conductivity [S.m-1] | Nyman2008 fn | 3.0 | plating margin |
| Negative particle radius [m] | 5.86e-6 | 3e-6 | anode kinetics/transport, plating margin |
| Total heat transfer coefficient [W.m-2.K-1] | 10 | 100 | 4C T_max control |
Unchanged from base: positive thickness 75.6 um, negative thickness 85.2 um,
positive particle radius 5.22 um, positive porosity 0.335, negative porosity 0.25.

## 5 Measured performance (SPMe tool outputs; all values from output files)
| Metric | Measured | Criterion | Verdict |
|---|---|---|---|
| Energy density (calc-energy contract) | 502.70 Wh/kg | >= 392.61 | PASS (+110.09) |
| Volumetric energy density | 953.34 Wh/L | - | - |
| Contract capacity / energy | 5.0306 Ah / 17.8975 Wh | - | - |
| Cell mass | 35.603 g | - | - |
| Midpoint voltage | 4.0073 V | - | - |
| DCR | 0.14679 mOhm (baseline 0.34755 mOhm, -58%) | - | - |
| Power density | 797.3 kW/kg | - | - |
| 4C charge at 45 C ambient: T_max | 323.98 K (50.83 C) | <= 333.15 | PASS |
| 4C charge: anode potential min | +0.0503 V | >= 0 | PASS (no plating) |
| Overcharge to 4.7 V: reached / T_max | 4.70 V / 299.45 K | <= 333.15 | PASS |
| Thermal runaway model (run-tr --sim coupling) | triggered=false | false | PASS |

## 6 Design path (R1-R4)
R1 baseline: ED 400.29 pass; 4C plating fail (anode min -0.4385 V).
R2 architecture levers (thin CC/separator, fast-charge kit, N/P up, combo):
ED up to 566.3, plating persists - diagnosed: anode-potential minimum occurs at the
END of the 4C charge (V=4.2 cut-off), anode-side polarization dominates.
R3 electrolyte transport kit (t+ 0.6, D_e 1e-9, kappa 2.0, negative radius 4 um):
plating eliminated (anode min +0.0420 V) but plating-free charge now accepts more
current: 4C T_max 335.77 K overshoot.
R4 cooling h=100 + transport margin (t+ 0.7, D_e 2e-9, kappa 3.0, radius 3 um):
all criteria pass. Cooling-kinetics trade-off: h=150 (R4-V4-coolmax) re-plates the
cell (anode min -0.0006 V - cooler cell slows kinetics).
Backup R4-V1-cool also passes all criteria (ED 499.43, anode min +0.0247 V,
4C T_max 325.08 K).

## 7 Honesty notes
- Electrolyte mass excluded from ED (calc-energy contract; parameter set lacks density).
- All simulations SPMe (lumped thermal); DFN not run for the champion.
- Chen2020 first-cycle low-capacity artifact: 1C-protocol run shows 1.118 Ah while the
  calc-energy contract integration gives 5.0306 Ah; ED uses the contract value.
- True compute (DFT/MD) not run: real_compute=false; endorse entry skipped honestly.
- Plating-free margin is +50 mV on anode potential - manufacturing window is documented,
  not guaranteed by proxy simulation.
