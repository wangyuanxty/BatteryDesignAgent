# DFMEA - Design L (Case T2R1NOCEILING, negative-result case)

Ranking: S = severity (1-10), O = occurrence (1-10), D = detection (1-10, 10 = undetectable at design time).

| # | Failure mode | Effect | Cause (tool-diagnosed) | S | O | D | RPN | Current design control | Action / status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 4C charge lithium plating | Dendrite risk, fast-charge function not delivered | 4C test start state (full 1C discharge leaves anode deeply lithiated) + SPMe surface response at ~195 A/m2 + electrolyte potential drop at separator interface; abort is a ~5 s event | 10 | 10 | 2 | 200 | None found in admissible space (10 lever axes swept, best -0.3868 V vs >= 0) | Out of scope: requires material system / electrode modification (locked) or test at far lower effective current |
| 2 | SEI overgrowth at 500 cyc (811.3 nm vs 550) | Impedance growth, lithium loss | Per-cycle 4.2 V charge-end depth drives ec-reaction-limited SEI; isothermal 25 C aging | 8 | 10 | 2 | 160 | None found (levers moved SEI500 only -6.5..+208 nm) | Out of scope: SEI kinetics (electrode modification, locked) or lower charge cut-off (usage mode, excluded) |
| 3 | SEI100 margin erosion with thick anodes | 100-cycle criterion failure (H: 540.0 nm) | Longer charge step per cycle with higher anode headroom | 7 | 3 | 1 | 21 | Thick-anode direction rejected (R3 dose-response) | Design rule: N/P 1.16 baseline; do not raise |
| 4 | Near-zero 4C charge acceptance (0.0461 Ah, 8.4 s, ~0.9% SOC) | Grid fast-charge function not delivered even absent plating | 4.2 V abort driven by cell polarization + cathode surface depletion at 4C | 7 | 10 | 2 | 140 | None (inherent to Chen2020 SPMe at 4C) | Documented as system-level limitation |
| 5 | lowT retention margin erosion with aggressive cooling | Retention drops (I: 0.9919) | h 100 cools the cell toward -20 C during the lowT test | 4 | 3 | 1 | 12 | h = 10 selected (thermal lever dead for plating anyway) | Keep h 10 |
| 6 | 4C test temperature rise (T_max 333.2 K) | Aging acceleration under fast-charge use | Ohmic + polarization heating in the 4C burst | 3 | 8 | 2 | 48 | None needed (below red line; test 45 C ambient) | Monitor only |
| 7 | Energy density overestimate (electrolyte excluded) | Real built-cell ED lower than reported | calc-energy contract formula excludes electrolyte mass (parameter set lacks density) | 4 | 10 | 1 | 40 | Annotated in calc.xlsx / datasheet | Re-calc when electrolyte density available |

Top risks FM1/FM2 are boundary-level (outside the admissible design space of this task) - the
negative-result conclusion of this case rests on them. See final log entry escalation layers.
