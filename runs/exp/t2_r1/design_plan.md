# t2_r1 — Grid Energy Storage Battery — Stage 1 Design Plan

Case: grid energy storage battery.
Contract (entry 0, verbatim from task text):
- energy density ≥ 327.18 Wh/kg
- 4C fast charge with no lithium plating
- anode SEI thickness ≤ 500 nm after 100 cycles of 1C cycling
- discharge capacity retention ≥ 90% at −20 °C
- SEI ≤ 550 nm after 500 cycles

## 1. Objective decomposition

| Decision layer | Metric | Threshold | Judged from |
|---|---|---|---|
| stage2 (cell) | `energy_density_wh_kg` | ≥ 327.18 | `calc-energy` (contract formula, electrolyte excluded) |
| stage2 (cell) | `sei_100cyc_nm` | ≤ 500 | `run-pyamm aging_1C_100cyc --cycles 100` (bridge copy of `sei_thickness_nm_end`) |
| stage2 (cell) | `sei_500cyc_nm` | ≤ 550 | `run-pyamm aging_1C_100cyc --cycles 500` (bridge copy) |
| stage2 (cell) | `lowT_retention_pct` | ≥ 90 | capacity(lowT_discharge, 253.15 K) ÷ capacity(1C_discharge, 298.15 K), same params, bridge ratio |
| stage3 (safety) | `plated` | false | `run-pyamm 4C_charge_45C --thermal lumped --plating` → `anode_potential_v` min < 0 V |
| — (monitored) | `T_max_K` | no contract red line | 4C charge output (metric extracted, not judged) |

Trade-off expectations (multi-objective):
- ED vs plating: raising N/P (thicker negative) lifts anode potential at charge end (anti-plating) but adds mass (ED ↓). Higher electrolyte conductivity σ_e helps plating, lowT, and rate with no ED cost — first-priority lever.
- ED vs lowT: thinner electrodes reduce transport polarization at 253 K but raise dead-mass fraction (ED ↓). Particle-size/porosity/electrolyte levers act on both.
- ED vs SEI: SEI kinetic constants (coating) have no ED cost — the cheapest contract to buy.
- Priority: all five are hard contracts; ED is the metric most threatened by mitigation levers (N/P, thickness), so verify the ED ceiling early.

## 2. Baseline facts (Chen2020, parameter dump verified)

- Nominal 5 Ah; area 0.065×1.58 = 0.1027 m².
- Positive: 75.6 μm, porosity 0.335, ρ 3262 kg/m³ (active frac 0.665); particle r 5.22 μm.
- Negative: 85.2 μm, porosity 0.25, ρ 1657 kg/m³ (active frac 0.75); particle r 5.86 μm.
- Separator: 12 μm, porosity 0.47, ρ 397 kg/m³. Collectors: Al 16 μm (2700), Cu 12 μm (8960).
- Layer mass ≈ 0.164 (pos) + 0.106 (neg) + 0.043 (Al) + 0.108 (Cu) + 0.0025 (sep) ≈ 0.423 kg/m² → ≈ 43.5 g cell.
- SEI: k_sei = 1e-12 m/s (ec reaction limited); j_SEI = 1.5e-7 A/m². Protocol signal-scale reference: Chen2020 k_sei ×0.1 → 100-cycle SEI 449 → 385 nm.
- Electrolyte: σ/D Nyman2008 functions (T-dependent), t⁺ = 0.2594.
- Known artifact: Chen2020 initial state is cathode-27%-lithiated → first-cycle discharge capacity low vs nominal; ED computed mechanically from the discharge output; ceiling assessment quantifies the cap.
- Anchor verification: NMC811/graphite OCP functions (`nmc_LGM50_ocp_Chen2020`/`graphite_LGM50_ocp_Chen2020`), SEI kinetics present (aging-capable) — deterministic anchor-table match for "no electrode system named" → Chen2020.

## 3. Candidate strategy

Round 1 (baseline characterization): Chen2020 defaults, full sweep — 1C_discharge (SPMe + DFN) + calc-energy, lowT_discharge, aging_1C_100cyc ×100 and ×500, 4C_charge_45C (DFN, lumped, plating). → gap vector.

Expected gaps (domain expectation, to be verified by measurement):
1. Plating at 4C: graphite at 4C charge is aggressive → likely `plated=true` on baseline.
2. lowT retention: standard Nyman2008 electrolyte transport at 253 K → retention likely < 90%.
3. SEI at 500 cycles: baseline 100-cycle SEI ≈ 449 nm (protocol reference) with sublinear growth → 500-cycle likely > 550 nm.
4. ED: unknown until calc-energy; first-cycle-capacity artifact applies systematically.

Lever ladder per gap (all freedoms adjustable — widest interpretation):
- Plating@4C: ① negative particle radius ↓ (surface area ↑, plating-resistant); ② electrolyte σ ↑ (formulation); ③ negative porosity ↑ / thickness ↑ (N/P); ④ t⁺ ↑.
- lowT: ① electrolyte σ/D formulation overrides with weak T-dependence (literature-grounded values); ② porosity ↑; ③ particle radius ↓; ④ thinner electrodes.
- SEI: ① anode coating candidate (inorganic ALD-Al2O3 type — molecular funnel skipped per protocol for ionic solids) → k_sei ↓; ② j_SEI ↓ (electron-migration-limited branch).
- ED: thinner collectors (Al 16→10 μm, Cu 12→8 μm), thinner separator, thicker electrodes, N/P rebalance; if best-architecture ceiling < 327.18 → **escalate to Stage 2 material design** (system switch: OKane2022 NMC811/graphite+SiOx — higher negative capacity, thinner negative, higher ED).

Rounds 2–6: targeted variants per measured gaps; each candidate re-run on the affected protocols; batch `log-evaluate` every round (one entry per candidate).

## 4. Budget allocation

| Round | Work | Cost |
|---|---|---|
| R1 | Baseline full sweep (5 protocols + calc-energy) | ~1 min |
| R2–R4 | Architecture + transport variants (plating/lowT/ED) | minutes each |
| R5 | SEI-kinetics coating variants (100 + 500 cyc) | minutes |
| R6 | Final verification sweep of best design (all protocols) | ~1 min |
| Closing | endorse (skip, real_compute=false) + final + render + deliverables | — |

True compute: none (real_compute=false, headless default).

## 5. Risk and fallback plan

- lowT retention may hit model-level limits (SPMe/DFN at 253 K, T-dependence of transport functions). Three-strike rule: same failure cause 3 consecutive rounds → question assumptions layer-by-layer (system reachability / task boundary / metric reachability) and record in `final.escalation`; close as negative result only if the questioning conclusion is "unreachable within boundary", with "reachable if X relaxed" noted.
- ED ceiling: if architecture+formulation optimization cannot reach 327.18 (including the initial-lithiation artifact), gap attribution = material/system level → escalate to Stage 2 (system switch), not blind architecture tuning.
- 4C plating with fixed plating kinetics: if cell-scale levers cannot clear anode potential, escalate to Stage 2 (electrolyte additive / system switch). Wrong-scale fallback is thrashing — capacity/temperature/plating from transport are cell+parameter issues, potential-window/stability issues are molecular.
- SEI: verify the coating variant satisfies both 100-cycle (≤500) and 500-cycle (≤550) contracts; if k_sei alone insufficient, add the j_SEI branch.
- Simulation failures: read stderr verbatim, record to log, fix per hint (unknown parameter name → fix key per bridge table; solver error → adjust protocol/parameters), never swallow and blind-retry.
- Audit integrity: every propose round gets a same-round evaluate (log-evaluate); derived bridge files document formula + source file:key; no threshold relaxation (entry 0 is the contract).

## 6. References (real sources)

- Chen C.-H., Brosa Planella F., O'Regan K., Gastol D., Widanage W.D., Kendrick E., "Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models", J. Electrochem. Soc. 167, 080534 (2020) — Chen2020 parameter-set basis (5 Ah NMC811/graphite pouch).
- Sulzer V., Marquis S.G., Timms R., Robinson M., Chapman S.J., "Python Battery Mathematical Modelling (PyBaMM)", Journal of Open Research Software 9, 14 (2021) — simulation framework and SEI aging model structure.
- Zhang S.S., Xu K., Jow T.R., "The low temperature performance of Li-ion batteries", J. Power Sources 115, 137 (2003) — low-temperature electrolyte transport limitation direction.
- Colclasure A.M., Dunlop A.R., Trask S.E., Polzin B.J., Jansen A.N., Smith K., "Requirements for Enabling Extreme Fast Charging of High Energy Density Li-Ion Cells while Avoiding Lithium Plating", J. Electrochem. Soc. 166, A1412 (2019) — fast-charge plating mitigation direction.
- Jung Y.S., Cavanagh A.S., Riley L.A., et al., "Ultrathin Direct Atomic Layer Deposition on Composite Electrodes for Highly Durable and Safe Li-Ion Batteries", Adv. Mater. 22, 2172 (2010) — ALD Al2O3 anode coating suppressing SEI growth.
- Domain experience (no precise source): electrolyte-conductivity lever magnitude, particle-size effect on plating resistance (protocol measured reference: small particle contribution +14.6), N/P anti-plating direction.

## Revision history
- v1 (2026-08-25): initial plan.
