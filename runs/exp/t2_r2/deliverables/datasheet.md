# t2_r2 — Grid Energy Storage Cell Design Package

**File code: VBF-T2R2-DSH-01** — Technical Datasheet (source: this md; PDF release: datasheet.pdf).

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah (nominal parameter); 6.9089 Ah (1C DFN simulated, 25 C) | chen2020_dump.json / final_1c_dfn.json |
| Nominal voltage / window | 3.8751 V (1C midpoint); window 2.5-4.2 V | final_calc.json / chen2020_dump.json |
| Rated energy | 25.3513 Wh | final_calc.json (time integration of V x I) |
| Energy density | 522.4524 Wh/kg (869.1832 Wh/L) | final_calc.json; contract caliber - electrolyte excluded (no electrolyte density in parameter set): '电解液不计入质量与体积（参数集缺密度）' |
| Maximum continuous discharge | 1C verified: 6.9089 Ah, T_max 305.20 K (25 C amb) | final_1c_dfn.json |
| Fast-charge capability | 4C (45 C amb): NO plating (min anode potential +0.0410 V); T_max 360.09 K = 86.9 degC; charge accepted 0.958 Ah before 4.2 V cutoff (~13.9 % of 1C capacity - acceptance-limited, honestly reported) | final_4c_dfn.json |
| Operating temperature range | verified endpoints per simulation protocols: -20 C (99.62 % retention) to +45 C (4C charge); beyond-endpoint behavior not simulated | final_lowt_spme.json / final_4c_dfn.json (honest scope statement) |
| Cycle life (SEI-growth, task-caliber) | 99.9 nm @ 100 cyc (<= 500 PASS); 330.1 nm @ 500 cyc (<= 550 PASS) | final_aging100.json / final_aging500.json |
| Cycle life (EOL cycle count) | Not simulated: aging protocol reports SEI thickness only; the capacity trajectory starts from the set's as-dumped initial state and is not an EOL basis (it reads 0.547 -> 0.531 Ah) - annotation, not fabricated | final_aging500.json capacity_ah_per_cycle |
| Safety determination | 4C plating: PASS (min anode potential > 0 V); T_max 86.94 degC at 4C with no task red-line exceeded; no other abuse protocols run | final_4c_dfn.json |
| Dimensions and mass | 65 x 1580 x 284 um layer stack; 48.524 g (contract caliber, electrolyte excluded); 61.033 g incl. electrolyte (annotation-caliber extension) | chen2020_dump geometry / final params / final_calc.json / pore-volume calc |
