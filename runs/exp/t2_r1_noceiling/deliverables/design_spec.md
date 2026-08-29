# Design Specification - Grid Energy Storage Cell (Case T2R1NOCEILING)

**Case**: t2_r1_noceiling | **Ablation**: ceiling_escalation OFF (no proactive material-design escalation)
**Status**: NEGATIVE RESULT - 3 of 5 criteria met; 2 criteria infeasible in the admissible design
space (evidence: 4 rounds, 14 evaluated designs, 10 lever axes, all mechanically evaluated via
`bda log-evaluate` against entry-0 criteria).

## 1. Task criteria (thresholds verbatim from task text, log.jsonl entry 0)

| Criterion | Threshold | Decision layer |
|---|---|---|
| Gravimetric energy density | >= 327.18 Wh/kg | stage2 |
| 4C fast charge, no lithium plating | plated = false (min anode surface potential difference at separator interface >= 0 V) | stage3 |
| Anode SEI thickness after 100 cycles of 1C cycling | <= 500 nm | stage2 |
| Discharge capacity retention at -20 C | >= 0.90 | stage2 |
| Anode SEI thickness after 500 cycles of 1C cycling | <= 550 nm | stage2 |

## 2. Selected design: L "AnPorUp" (best-effort)

Base parameter set: Chen2020 (NMC811/graphite teaching parameterization), SPMe, start_stage 3.
Degrees of freedom per entry 0: electrode_system locked, electrolyte_formulation adjustable,
electrode_modification locked, cell_architecture adjustable, thermal_management adjustable.

| Parameter | Baseline | Design L |
|---|---|---|
| Positive current collector thickness [m] | 1.6e-05 | 1.0e-05 |
| Negative current collector thickness [m] | 1.2e-05 | 8.0e-06 |
| Negative electrode porosity | 0.25 | 0.35 |
| Nominal cell capacity [A.h] | 5.0 | 4.9506 (measured 1C, honest C-rate bookkeeping) |

All other parameters at Chen2020 baseline: separator 12 um / porosity 0.47, negative electrode
85.2 um, positive electrode 75.6 um / porosity 0.335, particle radii 5.86 / 5.22 um, electrolyte
Nyman2008 transport functions, t+ 0.2594, cooling h 10 W/m2/K.

Design rationale: the thin current collectors are a pure energy-density bank (verified inert
w.r.t. plating/SEI, R2-A). The anode-porosity lever is the only admissible direction that moved
the 4C plating metric favorably (R4-L: +0.052 V vs R2-A) by relieving the anode-side electrolyte
potential drop at the metric point; it also lowers cell mass (active-material fraction) and DCR
to 0.199 mOhm, the lowest measured in this case.

## 3. Measured performance (all values from tool outputs under cell/)

| Criterion | Target | Measured | Verdict |
|---|---|---|---|
| Energy density | >= 327.18 Wh/kg | 476.72 Wh/kg | PASS |
| 4C no plating | anode min >= 0 V | -0.3868 V | FAIL |
| SEI 100 cycles | <= 500 nm | 467.6 nm | PASS |
| lowT retention | >= 0.90 | 0.9944 | PASS |
| SEI 500 cycles | <= 550 nm | 811.3 nm | FAIL |

Supporting cell values (calc-energy / protocol outputs): capacity 4.9520 Ah, energy 17.4766 Wh,
mass 36.660 g, area 0.1027 m2, stack thickness 190.8 um, volume 19.60 cm3, midpoint voltage
3.9474 V, DCR 0.199 mOhm, power density 558.7 kW/kg (tool formula V_OC^2/(4 DCR)/mass),
energy density (volumetric) 891.88 Wh/L. 4C charge acceptance at 19.80 A: 0.0461 Ah in 8.4 s
to the 4.2 V abort (~0.9% SOC), T_max 333.2 K.

## 4. Infeasibility evidence (the two failing criteria)

Full sweep (all 14 mechanically evaluated designs; values from log evaluate entries):

| Design | ED Wh/kg | SEI100 nm | SEI500 nm | lowT | anode min V |
|---|---|---|---|---|---|
| Baseline Chen2020 | 400.3 | 449.1 | 777.9 | 0.9943 | -0.4385 |
| A ThinCC | 456.4 | 449.1 | 777.9 | 0.9943 | -0.4386 |
| B HiCond (sigma x2, D x1.7, t+ 0.4) | 404.1 | 476.8 | 829.8 | 0.9945 | -0.4494 |
| C SmallNeg (r 3.5 um) | 407.0 | 452.9 | 771.4 | 0.9944 | -0.4368 |
| D LowLoad (x0.728) | 355.6 | 481.0 | 836.8 | 0.9940 | -0.4067 |
| E ThickNeg (N/P 1.5) | 478.6 | 494.6 | 865.6 | 0.9999 | -0.4643 |
| F ThinSep (9 um / 0.55) | 458.6 | 455.0 | 787.9 | 0.9943 | -0.4348 |
| G ThickNeg+ThinSep | 480.0 | 496.2 | 868.9 | 0.9999 | -0.4704 |
| H ThickNeg2 (N/P 1.77) | 452.1 | 540.0 | 979.9 | 1.0000 | -0.5027 |
| I Cool (h 100) | 454.1 | 454.1 | 786.4 | 0.9919 | -0.4337 |
| J CathPartUp (12.5 um) | 376.4 | 463.3 | 856.7 | 0.9999 | -0.4455 |
| K TransDown (degenerate) | 238.2 | 68.0 | 68.0 | 1.0000 | +0.1178 |
| L AnPorUp (SELECTED) | 476.7 | 467.6 | 811.3 | 0.9944 | -0.3868 |

4C plating: the metric is pinned by (a) the protocol start state - the test first discharges the
cell at 1C to 2.5 V, leaving the anode deeply lithiated; (b) the SPMe surface response at ~195
A/m2; (c) the electrolyte potential drop at the separator interface. The 4C abort is a ~5 s
transport event. Lever outcomes: current collectors (no effect), electrolyte transport up/down
(B worse -0.4494 / K breaks the cell), anode particle size (neutral), electrode loading (D
+0.032), N/P thickness (monotonic WORSE: -0.4643 / -0.4704 / -0.5027), separator (neutral),
thermal cooling (dead, +0.005 - abort too fast for cell-level cooling), cathode particle size
(J worse), anode porosity (best, +0.052). Best measured: -0.3868 V (L); required >= 0 V.
Largest single-lever move across all rounds: 0.052 V.

SEI500: driven by the per-cycle 4.2 V charge-end depth (SEI ec-reaction-limited, isothermal
25 C aging). Best measured: 771.4 nm (C); required <= 550 nm. Admissible levers moved it only
-6.5 nm (C) to +208 nm (H). The levers that would reduce it - SEI kinetics (electrode
modification, locked) and charge cut-off (usage mode, excluded) - are outside the boundary.

## 5. Pareto alternates (documented, not selected)

- A ThinCC: best SEI500 among ED-strong designs (777.9 nm), ED 456.4, plating -0.4386.
- G ThickNeg+ThinSep: best ED 480.0, but SEI500 868.9 and plating -0.4704.
- C SmallNeg: best SEI500 overall (771.4), ED 407.0, plating -0.4368.
- D LowLoad: second-best plating (-0.4067), ED 355.6, SEI500 836.8.

## 6. Honest protocol annotations

- lowT_discharge (tool definition): 1C discharge, ambient 253.15 K (-20 C), lumped thermal from
  the parameter set's 25 C initial temperature; the cell cools during the test (T_max 298.15 K =
  initial). Retention is the ratio of this run's capacity to the same-rate 1C reference.
- Aging: isothermal 25 C, SEI ec-reaction-limited, 1C cycles between the parameter set's own
  voltage limits. PyBaMM "Discharge capacity [A.h]" per cycle is the NET (discharge - charge)
  integral; the climb-then-saturate trajectory is an artifact of the shrinking charge step -
  SEI thickness is the direct criterion used here.
- calc-energy contract formula; electrolyte excluded from mass (parameter set lacks density) -
  the reported ED is an overestimate of a fully-built cell (annotated in calc.xlsx).
- 4C test: 1C discharge to 2.5 V, then 4C charge to 4.2 V at 45 C ambient; plating judged by
  min "Negative electrode surface potential difference at separator interface" >= 0 V
  (plated = min < 0).

## 7. Verdict

NEGATIVE RESULT. Design L is the best-effort deliverable: ED, SEI100 and lowT pass with margin,
and it holds the best 4C plating margin and lowest DCR of all 14 evaluated designs. The 4C-plating
and SEI500 criteria are infeasible within the admissible design space (see final log entry,
escalation layers 1-3). Thresholds were not relaxed.
