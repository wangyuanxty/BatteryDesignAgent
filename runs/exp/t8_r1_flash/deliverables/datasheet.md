# Technical Datasheet — VBF-T8R1FLASH-DSH-01

**Product**: Long-endurance drone battery cell (design V4 Thermal-tuned) | **Date**: 2026-08-25
**System**: NMC811 / graphite, high-transport electrolyte (t⁺=0.50 estimate)

| Field | Value | Source |
|---|---|---|
| Rated capacity | 3.40 Ah (nominal, design) / 3.45 Ah (1C simulation-verified) | params_r1_v4.json / cell/r1_v4_1c.json |
| Nominal voltage / window | 3.91 V (midpoint) / 4.20–2.50 V | cell/r1_v4_energy.json / parameter set |
| Rated energy | 12.68 Wh (∫V·I dt, simulation) | cell/r1_v4_energy.json |
| Energy density | 473.0 Wh/kg (contract caliber, electrolyte/casing excluded) | cell/r1_v4_energy.json |
| Volumetric energy density | 912.2 Wh/L | cell/r1_v4_energy.json |
| Max continuous discharge rate | 5C verified: retention 99.0 %, T_max 48.1 °C | cell/r1_v4_5c.json |
| Fast-charge capability | 4C@45°C: T_max 331.98 K (≤333.15), no plating (min anode 0.0247 V) | cell/r1_v4_4c.json |
| DC resistance (1C) | 1.38 mΩ | cell/r1_v4_energy.json |
| Peak power density (theoretical) | 114.8 kW/kg | cell/r1_v4_energy.json |
| Operating temperature range | −20…45 °C (simulation conditions used: 25 °C discharge, 45 °C charge; −20 °C not verified) | honest note |
| Cycle life | Indicative only: 100-cycle aging → SEI 467.2 nm; capacity trajectory shows standard-SEI-model artifact (climb-then-saturate) — treat as not reliably simulated | cell/r1_v4_aging.json |
| Safety determination | 4C charge: no plating, T_max within limit; overcharge to 4.7 V: T_max 300.57 K, thermal runaway not triggered | cell/r1_v4_4c.json, r1_v4_tr.json |
| Dimensions | Electrode 65 mm × 1580 mm; stack thickness 135.3 µm (excl. casing); casing dims not provided | parameter set |
| Mass | 26.8 g (contract stack caliber); full BOM incl. electrolyte ≈ 31.6 g | cell/r1_v4_energy.json / bom.xlsx |
