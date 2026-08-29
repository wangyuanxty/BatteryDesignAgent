# Technical Datasheet — VBF-T7R1NOFORCE-DSH-01

**Case**: `t7_r1_noforce` — HEV cell (NMC811/graphite, Chen2020 baseline + design overrides) · **Date**: 2026-08-25
Values mechanically taken from parameter set / simulation outputs; sources annotated. Not simulated = annotated, never fabricated.

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah (nominal); 5.0065 Ah (1C simulation-verified) | Chen2020 `Nominal cell capacity [A.h]`; `cell/r5_slim_1c_dfn.json` |
| Nominal voltage / voltage window | 3.826 V (discharge midpoint); 2.5 – 4.2 V | `cell/r5_slim_energy.json`; Chen2020 cut-offs |
| Rated energy | 17.804 Wh | `cell/r5_slim_energy.json` (V·I time integration) |
| Energy density | 491.47 Wh/kg (contract caliber: electrolyte excluded from mass); 928.06 Wh/L | `cell/r5_slim_energy.json` (calc-energy) |
| Fast-charge capability | 4C @45 °C: CC phase 379.7 s (~2.11 Ah) to 4.2 V, then CV hold to protocol end; **no lithium plating** (anode surface potential min +0.0153 V); T_max 325.54 K (+7.39 K over ambient) | `cell/r5_slim_4c45.json` |
| Maximum continuous discharge rate | 1C verified by simulation (capacity 5.0065 Ah, T_max 299.43 K @25 °C ambient); higher continuous rates not simulated | `cell/r5_slim_1c_dfn.json` |
| Operating temperature range | 25 – 45 °C verified by simulation (1C discharge @25 °C; 4C charge + 100-cycle aging @45 °C); beyond this range N/A (not simulated) | protocol definitions (`pybamm_runner.PROTOCOLS`) |
| Cycle life | **Not determined** — 100-cycle 45 °C aging simulated with ec-reaction-limited SEI model only (SEI thickness 510.5 nm at cycle 100); cycles-to-end-of-life requires a capacity-fade model beyond SEI — Not simulated | `cell/r5_slim_aging45.json`; honesty note: per-cycle capacity trajectory artifact annotated in evaluate entries |
| Safety determination | 4C charge @45 °C: no plating (✓). Nail penetration 10 W (t_init = 4C T_max 325.54 K, ambient 298.15 K, hA = 0.531 W/K): triggered = false, T_final 317.0 K (✓). Overcharge/crush/drop: N/A (beyond pure simulation boundary) | `cell/r5_slim_4c45.json`; `validation/r5_slim_nail.json` |
| Dimensions | 65 mm × 1580 mm (unfolded electrode); 186.8 µm layer stack thickness; shell dimensions Not provided | Chen2020 geometry; calc-energy `thickness_m` |
| Mass | 36.23 g (contract caliber, electrolyte excluded); ~42.6 g incl. electrolyte estimate (1.2 g/cm³ literature density) | `cell/r5_slim_energy.json`; design_spec §3 |
| DC internal resistance | 2.6415 mΩ | `cell/r5_slim_energy.json` (calc-energy) |
| Power density | 43.24 kW/kg | `cell/r5_slim_energy.json` (calc-energy) |
| Cooling requirement | Liquid cooling, total heat transfer coefficient ≥ 100 W/m²/K (cell-level hA ≥ 0.531 W/K) — **load-bearing design element**: without it the nail criterion triggers (R1 evidence) | `params_r5_slim.json`; `validation/r1_*_nail.json` |

Design parameter highlights: negative 85.2 µm graphite, 4.0 µm particles with Al₂O₃ ALD coating (SEI k 7.5×10⁻¹³ m/s); positive 75.6 µm NMC811; separator 10 µm; Cu 6 µm / Al 10 µm; high-transport electrolyte (σ 2.5 S/m, D 5×10⁻¹⁰ m²/s, t⁺ 0.5 — bridge estimates, flagged). Full audit trail: workspace `log.jsonl` (entry 0 criteria + rounds R1–R5 + final).
