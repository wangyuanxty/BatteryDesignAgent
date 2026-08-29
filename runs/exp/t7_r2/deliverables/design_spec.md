VBF-T7R2-DS-001 | Design Specification | t7_r2 HEV cell
Case: runs/exp/t7_r2 | date 2026-08-26 | verdict: achieved (round 4)

1. Objective (task verbatim thresholds):
   ED >= 327.18 Wh/kg | 4C charge @45C without lithium plating |
   SEI <= 550 nm after 100 cycles @45C | nail penetration (10 W) without TR

2. Selected design R4_F1_Fine2_Tp05_Por32_H80:
   Chen2020 + {r_neg: 5.86->2.0 um; t+ 0.2594->0.5; negative porosity 0.25->0.32; h 10->80 W/m2/K}
   Cooling: HEV pack active liquid cooling, effective h = 80 W/m2/K
   (hA = 80 x cell cooling surface 0.00531 m2 = 0.4248 W/K)

3. Measured performance (bda outputs, mechanical extraction):
   ED 423.62 Wh/kg (>= 327.18) ; volumetric 871.80 Wh/L
   4C@45C anode potential min +0.009007 V vs Li/Li+ (>0 -> no plating)
   SEI end-of-100-cycles 463.14 nm (<= 550)
   nail 10 W: triggered=False, T_max 321.73 K, dT/dt max 0.259 K/s
   nail hot-soak probe (318.15 K start): triggered=False, T_max 321.73 K

4. Design rationale: R1 baseline passed ED/SEI but failed plating (-0.1918 V) and
   nail (near-adiabatic trigger at 322 s). R2 single levers: t+ 0.4 (+0.089 V) and
   3 um particles (+0.054 V) best; thicker anode rejected (backfire -0.2482 V);
   h=50 passed ambient nail but hot-soak probe ignited near 356 K equilibrium ->
   cooling raised to h=80. R3 combos closed nail and narrowed plating to -0.0097 V.
   R4 F1 stacked 2.0 um + t+ 0.5 + anode porosity 0.32 + h=80 -> +0.0090 V.
   F4 (separator porosity 0.55) marginally better (+0.0111 V) but NOT selected:
   high-porosity separator relaxes mechanical/melt-integrity margin in an abuse task
   for only +2 mV.

5. Simulators: PyBaMM DFN (1C/4C, lumped thermal + plating), SPMe (aging, SEI ec
   reaction limited), calc-energy contract formula (electrolyte excluded),
   run-tr 3-reaction ODE (Kim 2019 / Coman 2016 kinetics).
   real_compute=false: Stage 5 true DFT/MD endorsement skipped (see log endorse).