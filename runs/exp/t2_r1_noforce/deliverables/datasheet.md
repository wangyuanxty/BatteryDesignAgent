# Technical Datasheet — F1 Grid Energy Storage Cell

**VBF-T2R1NOFORCE-DSH-001** | Case: t2_r1_noforce | Date: 2026-08-25 | Base parameter set: Chen2020 (PyBaMM) | All values from simulation outputs / parameter set; no fabricated numbers.

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah (nominal); 5.0282 Ah (simulation-verified, 1C, 25 °C) | parameter set `Nominal cell capacity [A.h]`; `cell/r5_f1_1c_spme.json` |
| Nominal voltage / window | 2.5 – 4.2 V; discharge midpoint 3.9794 V | parameter set cut-offs; `cell/r5_f1_energy.json:midpoint_voltage_v` |
| Rated energy | 17.848 Wh (1C discharge integration) | `cell/r5_f1_energy.json:energy_wh` |
| Energy density | 435.44 Wh/kg; 865.50 Wh/L (contract caliber, electrolyte excluded) | `cell/r5_f1_energy.json` |
| DC resistance / power | DCR 0.2036 mΩ; 497.31 kW/kg (V_OC²/(4·DCR)/mass) | `cell/r5_f1_energy.json:dcr_ohm,power_density_w_kg` |
| Maximum continuous discharge | 1C (5.03 Ah verified); higher-rate discharge not required by task | `1C_discharge` protocol |
| Fast-charge capability | 4C charge, 45 °C: min anode potential +0.0071 V → **no lithium plating** (✓); T_max 359.92 K (86.8 °C); charge-in 0.3472 Ah before 4.2 V cutoff | `cell/r5_f1_4c_dfn.json` (--plating) |
| Operating temperature | −20 °C retention 99.45 % (✓ vs ≥90 %); 25 °C 1C cycling; 45 °C 4C charge — all simulated conditions | `cell/r5_f1_lowT_spme.json` + derived `derived/r5_f1_retention.json` |
| Cycle life (SEI) | SEI@100 cyc 439.52 nm (✓ ≤500); SEI@500 cyc 738.43 nm (✗ >550 — criterion unreachable in the protocol's SEI model family, three-strike documented; capacity-trajectory interpretation limited by the climb-then-saturate artifact, annotated) | `cell/r5_f1_aging100_spme.json`, `cell/r5_f1_aging500_spme.json` |
| Safety determination | No plating at 4C (anode potential criterion); 4C T_max 359.92 K below any thermal-runaway red line (573 K); overcharge/nail/crush not simulated (beyond pure-simulation boundary) | 4C protocol output |
| Dimensions | 65 × 158 × 0.2008 mm (electrode stack; shell thickness not provided) | parameter set + calc-energy |
| Mass | 40.990 g (electrolyte excluded, contract caliber); +8.23 g electrolyte (annotated, 1.2 g/cm³) | `cell/r5_f1_energy.json` |

**Overall determination**: 4 of 5 task criteria achieved (ED, SEI@100, −20 °C retention, 4C no-plating). SEI@500 ≤ 550 nm not achieved — best measured 738.4 nm; documented as physically unreachable within the protocol's ec-reaction-limited SEI model (see final log entry escalation). If the 500-cycle threshold were relaxed to ≤750 nm, this design meets all five criteria.
