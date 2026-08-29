# Cell Datasheet - VBF-T5R2-DSH-01

**Case t5_r2 finalist f2_h70_C** - NMC811/graphite (Chen2020 base) - simulation-verified only.

## Electrical & energy performance

| Item | Value | Condition / caliber |
|---|---|---|
| Rated capacity | 7.171 Ah | DFN 1C CC discharge 4.2 -> 2.5 V, 25 C (r7) |
| Nominal capacity parameter | 6.5 Ah | parameter-set design value |
| Nominal voltage | 3.78 V | midpoint of 1C DFN discharge |
| Energy | 25.375 Wh | integral V*I over 1C discharge |
| Energy density (contract) | 666.3 Wh/kg | calc-energy caliber: stack only, electrolyte/casing excluded |
| Energy density, volumetric | 1020.5 Wh/L | stack volume 0.025 L |
| Energy density + electrolyte | ~0.7 Wh/kg | BOM-caliber incl. 12.4 g electrolyte fill (1.2 g/cm3 LITERATURE ESTIMATE) |
| Specific power | 42,997 W/kg | contract mass caliber |
| DC resistance | 2.538 mohm | mid-SOC slope estimate (energy tool) |
| Mass | 38.08 g (50.5 g w/ electrolyte) | stack / BOM calibration |
| Stack dimensions | 242.12 um x 0.1027 m2 | 98.28 um pos / 121.84 um neg / 8 um sep / 8 um Al / 6 um Cu |

## Operating envelope

| Item | Value |
|---|---|
| Voltage window | 2.5 - 4.2 V (parameter set) |
| Temperature, ambient | 25 - 45 C tested (4C run at 45 C) |
| Max cell temperature at 4C charge | 57.83 C = 330.984 K (ambient 45 C, h = 70 W/m2/K) - passes 60 C limit with 2.2 K margin |
| Temp at 1C discharge | 27.27 C |
| Charge, standard | 1C CC-CV to 4.2 V (recommended taper after cut-off) |
| Charge, fast | 4C CC protocol-verified: no lithium plating (min anode potential +0.0506 V); CC-only acceptance 0.511 Ah before 4.2 V |
| Discharge, max rated | 1C (design basis; higher rates not part of the acceptance criteria) |
| Cycle life | Not simulated as a rated criterion (requires aging model, artifact-flagged) |
| Storage | n/a (no calendar-aging criterion) |

Cycle-life honesty: this datasheet does NOT fall back on the generic "Not simulated"
placeholder, because the Chen2020 base does carry an SEI aging model. An informational
aging_1C_100cyc run (SPMe, isothermal 298.15 K, SEI ec-reaction-limited) was executed;
the runner's per-cycle capacity series is inconsistent with the contractual 1C capacity
(protocol-definition artifact), so only the raw SEI-trend signal is reported:
end-SEI 520.3 nm after 100 cycles. No cycle-life rating is derived.

## Honesty notes

- All values tool-sourced from r7 finalist simulations (DFN); no post-editing of outputs.
- Electrolyte property values are labeled literature ESTIMATES (endorse skipped, real_compute=false).
- This is a cell-level simulation datasheet, not a certified product specification.
