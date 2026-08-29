# Design Verification Plan & Report (DVPR) — t8_r1_noforce

Document number: VBF-T8R1NOFORCE-DVPR-01 · Generation date: 2026-08-25 · Status: virtual design verification (simulation-based)

## Executed verification items

| # | Verification item | Method / condition | Result | Criterion (entry 0) | Determination | Source |
|---|---|---|---|---|---|---|
| 1 | Gravimetric energy density | `bda calc-energy` contract caliber (1C discharge integral ÷ layer mass, electrolyte excluded) | 497.968 Wh/kg | ≥ 446.18 Wh/kg | **PASS** | `cell/r6_v9_energy.json` |
| 2 | 5C capacity retention | DFN discharge 5C vs 1C, same parameters, same temperature | 0.9896 | ≥ 0.90 | **PASS** | `cell/r6_v9_retention.json` (computed mechanically from `r6_v9_5c_dfn.json` / `r6_v9_1c_dfn.json`) |
| 3 | Cell mass | calc-energy layer-mass sum × area | 38.99 g | ≤ 40 g | **PASS** | `cell/r6_v9_energy.json:mass_kg` |
| 4 | Lithium plating under fast charge | 4C charge protocol at 45 °C ambient, plating module (anode potential min < 0 → plated) | anode min +0.00635 V → plated = false | plated = false | **PASS (margin +6.3 mV — flagged)** | `cell/r6_v9_4c_charge45_plating.json` |
| 5 | Max cell temperature — fast charge | same run, lumped thermal | 326.81 K | ≤ 333.15 K | **PASS** | same file `T_max_K` |
| 6 | Max cell temperature — 5C discharge | DFN 5C discharge, 25 °C ambient | 313.64 K | ≤ 333.15 K | **PASS** | `cell/r6_v9_5c_dfn.json:T_max_K` |
| 7 | 1C discharge capacity | DFN 1C discharge, 25 °C | 5.2725 Ah | no entry-0 threshold (feeds items 1–2) | PASS (informational) | `cell/r6_v9_1c_dfn.json` |

Result: **7 / 7 executed items PASS.** All five entry-0 stage2/stage3 criteria verified green on the final design (R6-V9). Verification trail: log.jsonl round 6 propose → evaluate (checked = 5, mechanical).

## Uncovered conditions (honest N/A list)

| Condition | Reason not executed | Materiality for this task |
|---|---|---|
| Cycle life / long-term aging | Not a task criterion; not simulated (no fabricated values) | Medium — endurance drones accumulate cycles; recommend future case with `--cycles` |
| Nail penetration | Requires physical experiment (no simulation model in this library) | Low for pouch drone pack (soft pack, no cell-level nail scenario in protocol) |
| Crush / drop / vibration | Requires physical experiment | Medium — drone airframe vibration is real; recommend qualification tests |
| Thermal runaway abuse (overcharge beyond protocol) | Overcharge protocol exists in library but out of task scope; not run | Low for this case (4C charge exam covers the task's thermal red line) |
| Low-temperature retention (−20 °C) | Not a task criterion | Medium — drone operation at altitude is cold; flag for next iteration |
| Self-discharge / storage | Not simulated | Low (single-flight-cycle use pattern) |
| DCR pulse measurement | calc-energy DCR is a formulation estimate, not a pulse test | Low (power density 150.5 kW/kg far exceeds drone demand) |

## Verification conclusion

The R6-V9 design satisfies all entry-0 acceptance criteria. Two margins deserve engineering attention before physical prototyping: (a) plating margin on 4C charge is +6.3 mV — thin; recommended mitigation is a 45 °C charge-temperature floor and/or 3C charge in cold conditions (see DFMEA); (b) the 10 µm separator and 6–8 µm current collectors are aggressive and must be validated for pouch winding/lasering capability. These are recorded as risks, not criterion failures — the criteria themselves are all met.
