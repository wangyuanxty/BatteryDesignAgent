# VBF-T9R4-CALC-001 Calculation Record (decisive numbers)

t9_r4 - grid-storage cell cathode on the Chen2020 NMC811/graphite profile

ED feasibility (binds the family choice):
- Chen2020 positive active mass M_am = 75.6e-6 x 0.1027 x 0.665 x 3262 = 16.84 g.
- calc-energy total mass = 43.45 g (porosity-corrected layers, no electrolyte).
- Baseline 1C discharge measured 4.948 Ah / 17.39 Wh -> ED 400.29 Wh/kg.
- Family capacity bounds (C = 0.7 x F/3.6 / MW): layered 180-285, olivine <= 128, spinel <= 113,
  tavorites <= 111, NASICON <= 46 mAh/g.
- Non-layered ED under the 0.9 rule: olivine at 4.8 V/128 mAh/g ~ 322 Wh/kg; LiNiPO4 at its
  true 5.1 V ~ 317 Wh/kg - both < 327.18 -> only layered LiMO2 can pass (ED ~ 445-465 Wh/kg).
- Plateau-OCP mapped discharge is anode-limited (~5.1 Ah, LNMO.json precedent): ED ~ 450-500
  Wh/kg for any layered at 4.6-4.8 V -> the binding constraint is the computed voltage itself.

Voltage screening (run-comp CHGNet, bcc Li reference e_li = -1.87848 eV):
- TM-redox layered band: 2.56-3.99 V (42-candidate sweep + known set; NiFe55 3.990 max).
- d0/d10 O-redox line: LiScO2 4.298, LiGaO2 4.479, LiZnO2 4.492, LiAlO2 4.598, AlB55 4.641,
  BGa55 4.504, GaAl55 4.494, LiBO2 4.253.

Charging-potential gate (comp/gate_charging.py, same machinery/seed; nested removal order):
- V(0.4 -> 0.3) = -(E(0.4) - E(0.3) - 1 x e_li) / 1
- E(0.4) = -295.256 eV (gate relaxation), E(0.3) = -285.968 eV (batch3), e_li = -1.878 eV
- charging_potential_v = 7.410 V >> 4.8 V -> FAIL. The x=0.3 endpoint sits ~9 eV off its
  composition neighbors; the 50:50 avg peak was this artifact's signature.

Capacity proxy: C = 0.7 x 26801.481 / MW. AlB55: MW 82.57 -> 324.38 mAh/g.
Relaxed-cell density (gate full state): 2.836 g/cm3 (relaxed-final-structure).