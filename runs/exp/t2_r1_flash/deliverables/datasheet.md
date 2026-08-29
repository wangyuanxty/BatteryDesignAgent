# Technical Datasheet — VBF-T2R1FLASH-DSH-01

**Case**: t2_r1_flash · Grid energy storage cell (virtual design, simulation-verified)

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah nominal (parameter set); 5.0469 Ah verified @1C 25C | cell/r2_fcc_1c_dfn.json |
| Nominal voltage / window | midpoint 3.877 V; 2.5 – 4.2 V | calc-energy midpoint_voltage_v / parameter set |
| Rated energy | 18.178 Wh (simulation integration V·I dt) | cell/r2_fcc_energy.json |
| Energy density | 425.4 Wh/kg (contract caliber, electrolyte excluded); 881.5 Wh/L | cell/r2_fcc_energy.json |
| Max continuous discharge rate | 1C verified (5.05 Ah, 1C to 2.5 V) | cell/r2_fcc_1c_dfn.json |
| Fast-charge capability | 4C @45C amb: no plating (anode min +12.3 mV), T_max 329.2 K with h=60 W/m2K | cell/r2_fcc_4c.json |
| Operating temperature range | Simulated: 25 C (1C/aging), -20 C (lowT), 45 C (4C fast charge). Full range not simulated | simulation conditions |
| Cycle life (SEI) | SEI 78.2 nm @100 cyc, 262.0 nm @500 cyc (1C, standard SEI model); capacity-based cycle life to 80% SOH not simulated (standard-SEI-model capacity artifact, honestly noted) | cell/r2_fcc_aging100.json / derived |
| Safety determination | 4C fast charge: no plating, T_max below red line -> PASS | cell/r2_fcc_4c.json |
| Dimensions and mass | 65.0 x 1580 x 0.2008 mm stack (no casing); 42.73 g (electrolyte-excluded caliber) | calc-energy |
| DC resistance | 2.892 mOhm (10% DOD method) | cell/r2_fcc_energy.json |
| Power density | 33.9 kW/kg (V_OC^2/4DCR / mass) | cell/r2_fcc_energy.json |
