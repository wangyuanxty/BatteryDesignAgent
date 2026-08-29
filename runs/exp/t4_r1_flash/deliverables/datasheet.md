# Technical Datasheet — T4R1FLASH

Case: `t4_r1_flash`  |  Generation date: 2026-08-25  |  Doc: VBF-T4R1FLASH-DSH-01

_All values mechanical from simulation outputs / parameter set (see log.jsonl); no numbers from memory._

| Field | Value | Source |
|---|---|---|
| Rated capacity | 3.93 Ah nominal; 3.955 Ah verified at 1C, 25 degC | parameter set + cell/final_b7_1c_dfn.json |
| Nominal voltage / window | 3.814 V midpoint; 2.5–4.2 V | cell/final_b7_energy_dfn.json + parameter set |
| Rated energy | 14.04 Wh (integral of V·I over 1C discharge) | cell/final_b7_energy_dfn.json |
| Gravimetric energy density | 460.1 Wh/kg (contract caliber, electrolyte excluded) | cell/final_b7_energy_dfn.json |
| Volumetric energy density | 899.3 Wh/L (contract caliber) | cell/final_b7_energy_dfn.json |
| Maximum continuous discharge | 1C verified (3.955 Ah delivered); higher rates not simulated | cell/final_b7_1c_dfn.json |
| Fast-charge capability | 4C at 45 degC: T_max 329.6 K (56.5 degC), no lithium plating (anode min +0.0193 V) | cell/final_b7_4c45_dfn.json |
| Operating temperature range | -20 degC (retention 0.9929 at 1C) to 45 degC (4C exam ambient), per simulated conditions | cell/final_b7_lowt_dfn.json, cell/final_b7_4c45_dfn.json |
| Cycle life | **Not simulated (requires aging model)** | — |
| Safety determination | No plating; T_max within red line; overcharge (0.5C to 4.7 V) does not trigger thermal runaway (triggered=False) | cell/final_b7_4c45_dfn.json, cell/final_b7_tr.json |
| Dimensions / mass | Electrode strip 65 x 1580 mm; stack thickness 152 µm; mass 30.5 g (contract caliber, excl. electrolyte) / ~35.5 g incl. electrolyte | parameter set + calc-energy |
| DC resistance | 3.85 mOhm (1C, 50% SOC estimate) | cell/final_b7_energy_dfn.json |
