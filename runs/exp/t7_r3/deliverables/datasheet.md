# VBF Technical Datasheet — HEV Battery Cell (virtual design)

**Document number**: VBF-T7R3-DSH-01 · **Case**: t7_r3 · **Date**: 2026-08-26
All values are simulation/parameter-set sourced; caliber noted per row. Prepared / Reviewed / Approved: ________

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 6.28 Ah (nominal, set) — verified 6.2569 Ah at 1C discharge (SPMe); 6.28 Ah (DFN) | `r7_v19_final_1c.json`, `r6_v19_1c_dfn.json` |
| Nominal voltage / window | 3.7 V class; window 2.5 – 4.2 V (midpoint voltage at 1C: 4.047 V) | Chen2020 cut-offs; `r7_v19_final_energy.json:midpoint_voltage_v` |
| Rated energy (Wh) | 22.491 Wh (∫V·I₁C dt, I₁C = 6.28 A) | `r7_v19_final_energy.json:energy_wh` |
| Energy density | **482.4 Wh/kg** (contract caliber, electrolyte excluded); 417.9 Wh/kg incl. 7.21 g electrolyte; volumetric 970.7 Wh/L | `r7_v19_final_energy.json` + electrolyte derivation (1.2 g/cm³ literature density) |
| Maximum continuous discharge rate | 1C (6.28 A) verified to 2.5 V; higher-rate discharge not simulated (5C protocol exists but not run — no criterion) | `r7_v19_final_1c.json` |
| Fast-charge capability (4C) | 4C = 25.12 A: CC charge accepts 0.778 Ah (12.4 % SOC) before hitting 4.2 V; **no lithium plating** (anode surface potential min +0.0171 V, 0 negative instants); T_max during charge 363.2 K (90.1 °C, lumped thermal) | `r7_v19_final_4c45c.json` |
| Operating temperature range | 25 °C (1C discharge, simulation default) and 45 °C (4C charge + aging) verified; below 0 °C models **not simulated** | protocols used |
| Cycle life | 100 cycles @ 45 °C (1C, SEI ec-reaction-limited model) simulated: SEI thickness end-of-test 512.9 nm (criterion ≤ 550 nm PASS); per-cycle net capacity entries ≈0.23–0.26 Ah reflect the charge-imbalance metric of the aging model, **not** a cell-level usable-capacity retention curve — end-of-life retention extrapolation **Not simulated** | `r7_v19_final_aging45c.json` |
| Safety determination | Nail penetration 10 W with designed cooling hA = 0.5 W/K: **no thermal runaway** (T_max 318.2 K); 4C charge: plating-free (above). Mandatory cooling requirement: hA ≥ 0.3 W/K | `r7_v19_final_nail_hA05.json`, sweep logs |
| Dimensions | 65 mm × 1580 mm unwound electrode strip; stack thickness 225.6 µm (excludes shell — not modeled) | Chen2020 geometry; `thickness_m` |
| Mass | 46.62 g (electrolyte excluded, contract); 53.83 g incl. electrolyte | `r7_v19_final_energy.json:mass_kg` + derivation |
| DC internal resistance | 0.120 mΩ (V(t₀)−V(10 %)) / I₁C) | `r7_v19_final_energy.json:dcr_ohm` |

**Customer-facing notes**: Chemistry NMC811/“graphite with low-transference (t⁺ ≈ 0.6) electrolyte formulation” — the exact salt/solvent recipe is a formulation estimate (see DS-01 Note 1), to be fixed by electrolyte qualification. All safety/performance claims above are simulation-caliber (virtual design); physical qualification (UN 38.3, cycle-life ext, thermal runaway physical) requires prototype build.