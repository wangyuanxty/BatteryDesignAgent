VBF-T7R2-DSH-001 | Cell Datasheet | t7_r2 HEV (R4_F1_Fine2_Tp05_Por32_H80)

Electrical:
  1C discharge capacity  5.0438 Ah   (mass 42.4 g -> 119 Ah/kg)
  Midpoint voltage       3.7919 V
  DC resistance          3.391 mOhm
  Power density          29066 W/kg (calc-energy contract formula)

Energy:
  Cell energy            17.98 Wh
  Gravimetric ED         423.62 Wh/kg   (contract: electrolyte excluded)
  Volumetric ED          871.80 Wh/L

Mechanical:
  Stacking               pouch, area 0.1027 m2, total thickness 200.8 um
  Layer stack            pos 75.6 | sep 12 | neg 85.2 | Al 16 | Cu 12 (um)

Fast charge (protocol 4C_charge_45C = 1C discharge to 2.5 V then 4C CC to 4.2 V, 45 C):
  anode interface potential min +0.009007 V vs Li/Li+  (no lithium plating)
  charge acceptance before 4.2 V cutoff  0.3844 Ah (~69 s at 4C)
  T_max during 4C        329.80 K

Cycle life (aging_1C_100cyc_45C, isothermal SPMe + SEI ec-reaction-limited):
  capacity cycle 1       0.8087 Ah ; cycle 100 0.7472 Ah (retention 92.4%)
  SEI thickness end      463.14 nm  (criterion <= 550)

Abuse - nail penetration (10 W internal short-circuit, hA = 0.4248 W/K):
  thermal runaway        triggered = False ; T_max 321.73 K ; dT/dt max 0.259 K/s
  hot-soak probe (45 C start)  triggered = False ; T_max 321.73 K ; dT/dt 0.039 K/s

Basis: PyBaMM DFN/SPMe + bda calc-energy + bda run-tr; parameter set Chen2020
with deltas Chen2020 + {r_neg: 5.86->2.0 um; t+ 0.2594->0.5; negative porosity 0.25->0.32; h 10->80 W/m2/K}.