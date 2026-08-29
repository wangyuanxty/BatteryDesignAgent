# Design FMEA — Smartphone High-Voltage Fast-Charge Cell (t6_r3)

| Doc No: VBF-T6R3-DFMEA-01 | Case: t6_r3 | Rev: 01 | Date: 2026-08-26 |

Scales: Severity (S), Occurrence (O), Detection (D): 1-10; RPN = S x O x D. Virtual-design FMEA on the DFN-verified cell.

| No | Item / function | Failure mode | Effect | S | Cause | O | Current control (virtual evidence) | D | RPN | Recommended action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Anode, 4C charge | Li plating (local anode potential < 0 V) | Capacity loss, dendrite/short risk, thermal hazard | 9 | Thin negative electrode, high areal current, electrolyte depletion | 2 | N/P 1.579 + 60 um cathode collapse CC to ~16.2 ms; DFN min anode pot. +0.1050 V (margin 105.0 mV) | 3 | 54 | Deep-start 4C DFN run (DVPR row 8); physical reference-electrode test |
| 2 | Cell thermal, 4C charge | T_max > 50 C | Electrolyte degradation, safety limit breach | 8 | Ohmic heat at 18 A, insufficient cooling | 2 | h = 250 W/m2/K; DFN T_max 318.922 K (margin 4.23 K) | 2 | 32 | Calorimetry on physical build; verify h assumption |
| 3 | Anode SEI, 100 cycles | SEI thickness > 500 nm | Impedance rise, capacity fade, plating onset | 6 | EC reduction kinetics at anode | 3 | k_sei 5e-14 m/s coating + EC-lean 2000 mol/m3; DFN 313.7 nm (margin 186.3 nm) | 3 | 54 | Longer aging horizon (500 cycles) simulation |
| 4 | Cell voltage, discharge | Plateau < 4.1 V | Energy/UX shortfall vs spec | 5 | Electrolyte concentration gradients (DFN-level polarization) | 2 | sigma 2.0 S/m + t+ 0.5; DFN midpoint 4.1551 V (margin 55.1 mV) | 2 | 20 | None beyond current design; monitor in physical DV |
| 5 | Cell energy density | ED < 950 Wh/L | Requirement miss | 6 | Inactive mass (CC foils, separator) and volume overhead | 2 | Thin 60/109 um stack, 209 um total; DFN 983.61 Wh/L (margin +33.61) | 1 | 12 | None beyond current design |
| 6 | Simulation fidelity | Proxy-model divergence (SPMe-class error) leads to wrong design sign-off | Field failure of a virtually-passed cell | 7 | Model order reduction, unmodeled physics | 4 | DFN everywhere (round-9 SPMe rejection logged); honest limitation disclosure | 2 | 56 | True DFT/MD when real_compute available; physical prototype DV |
| 7 | Aging model | Capacity trajectory artifact misread as real | Wrong durability narrative | 3 | SEI-model lithium-inventory simplification | 5 | SEI thickness used as durable metric; artifact labeled in datasheet/DVPR | 2 | 30 | Full-chemistry aging model or experimental check |
| 8 | Electrolyte properties | sigma / t+ drift from fixed assumed values | Plateau and plating margins erode | 5 | Concentration/temperature dependence replaced by fixed 2.0 S/m, 0.5 | 3 | EC-lean gradient reduction; margins: plateau +55.1 mV, plating +105.0 mV | 3 | 45 | Run DFN with Nyman2008 concentration-dependent conductivity |

## Notes

- Highest RPN = 56 (model fidelity) and 54 (plating, SEI) — actions tracked in DVPR rows 8-9.
- All 'current control' evidence values are DFN outputs from r10_V27_combo outputs; no physical test data is implied.