# Design Plan — HEV Battery Cell (task t7_r3)

**Contract (task text verbatim, pre-registered in log.jsonl entry 0 — no post-hoc revision):**
- Energy density ≥ **327.18 Wh/kg** (calc-energy, contract-caliber formula; electrolyte excluded, annotated)
- **4C fast charge without lithium plating** (protocol `4C_charge_45C`, `plated == false`, i.e., negative surface potential never < 0 V)
- **SEI ≤ 550 nm** after 100 cycles at 45 °C (protocol `aging_1C_100cyc_45C`, `sei_thickness_nm_end`)
- **Nail penetration (10 W short-circuit heat generation) without thermal runaway** (`run-tr --q-nail 10`, `triggered == false`)

**Degrees of freedom (task silent → widest interpretation, recorded as `meta.freedoms` in entry 0):**
electrode system / electrolyte formulation / electrode modification / cell architecture / thermal management — all adjustable.

**System → parameter-set mapping:** task names no electrode system → default **Chen2020** (NMC811/graphite, aging-capable, anchor table default rule). `start_stage: 3` (no new-molecule design named in the task; materials use system baseline where no architecture/coating lever suffices). Plating/thermal lumped-model defaults are injected by `run-pyamm` where Chen2020 lacks them (traceable via `injected_defaults` — T_max evidence marked approximate source where injection applies).

## 1. Objective decomposition & trade-off expectations

| Metric (layer) | Threshold | Simulation source | Expected trade-off |
|---|---|---|---|
| energy_density_wh_kg (stage2) | ≥ 327.18 | calc-energy on 1C discharge | ↑ thickness/↓CC/↓separator ↑ED but ↑DCR, ↑T, worse 4C charge acceptance (plating risk) |
| sei_thickness_nm_end (stage2) | ≤ 550 | aging_1C_100cyc_45C | essentially independent of architecture; controlled by SEI kinetics (coating bridge) |
| plated (stage3) | false | 4C_charge_45C anode_potential_v | ED vs plating is the central Pareto conflict: high-loading electrodes worsen local anode overpotential at 4C |
| triggered (stage3) | false | run-tr q_nail=10 W | independent lever: heat rejection (hA) + cell mass; no conflict with ED |

- **Central trade-off:** ED ↔ 4C plating. Thick, dense electrodes raise ED but increase transport overpotential; anode-side microstructure (particle radius, porosity, N/P) is the compensating lever.
- **SEI** decouples via electrode-modification freedom (coating → lower `SEI kinetic rate constant [m.s-1]`).
- **Nail** decouples via thermal-management freedom (cooling hA for the nail scenario); verify with a hA sweep, then design the cooling solution to the passing hA with margin.

## 2. Candidate strategy

- **R1 — Baseline characterization + opening ceiling assessment** (no overrides): 1C discharge (SPMe), 45 °C aging 100 cyc, 4C charge 45 °C with plating, calc-energy. Ceiling assessment: estimate best-possible Chen2020 ED (extreme thickness / thin CC / thin separator / low porosity) vs 327.18 → if the ceiling is below requirement, **escalate to Stage 2 (system candidate)**: OKane2022 (NMC811/graphite+SiOx, higher capacity, real plating + SEI + thermal params) or LNMO high-voltage set — system candidates skip the molecular funnel and go straight to Stage 3 simulation.
- **R2+ — Architecture/formulation rounds (2–4 variants each, compared with baseline and with each other):** electrode thickness, porosity, N/P balance, separator thickness+porosity, current-collector down-gauging, particle radius (negative small for plating resistance), electrolyte σ / t⁺ overrides (transport), cooling h (4C T_max).
- **SEI:** coating bridge candidate (k_SEI ×0.1–0.5) evaluated on the aging protocol, compared against baseline on the **same system**.
- **Nail:** run-tr with `--mass-kg` from calc-energy (mandatory; prevents the 1 kg-default distortion) — hA sweep from near-adiabatic 0.05 W/K up to a cooling-plate design value; pass = triggered false.
- **Stage 5 true compute:** `real_compute: false` → endorse entry records the skip honestly; no fabricated DFT/MD numbers.

## 3. Budget allocation (rounds of the evaluate loop)

- R1 baseline + ceiling: 4–5 simulations (one round).
- R2–R6 ED + plating exploration: ~2–3 variants/round (SPMe quick screen; DFN for finalists) → ~8–12 rounds at worst.
- R7–R9 SEI coating + 45 °C aging calibration (aging ≈ 3 s/100 cyc, cheap) → ~3 rounds.
- R10 nail hA sweep + passing config verification → 1–2 rounds.
- Final verification round: Top-1 re-run (SPMe + DFN) + full evidence chain → then deliverables, render, verify-deliverables, final entry.

## 4. Risk & fallback plan

| Risk | Symptom | Fallback (scale where the cause lives) |
|---|---|---|
| Chen2020 ED ceiling < 327.18 | ceiling assessment | escalate Stage 2 system switch (OKane2022 SiOx / LNMO) — material scale |
| Plating at 4C persists | anode_potential_v < 0 | Stage 3 microstructure/transport: negative particle radius ↓, anode porosity ↑, N/P ↑, σ/t⁺ ↑; 3 strikes → question boundary, record |
| SEI > 550 nm at 45 °C | sei_thickness_nm_end | Stage 2 coating bridge: k_SEI ↓ (×0.1–×0.3) |
| Nail triggered at hA_low | triggered=true | raise hA stepwise; identify minimum passing hA; if beyond physical cooling plausibility → quantified negative result |
| Aging capacity-climb artifact / first-cycle artifact (Chen2020 discharged initial state) | capacity trajectory | annotate honestly; judge by `sei_thickness_nm_end` only |
| T_max relies on injected thermal defaults (Chen2020 incomplete thermal set) | `injected_defaults` present | mark evidence source as approximate |
| Threshold unreachable within boundary after 3-strike questioning | evaluate fails repeatedly | question model/system assumption, task boundary, metric assumption; honest negative result with "reachable if X" note (never relax threshold) |

## 5. References (direction → source)

- SiOx anode raises capacity vs pure graphite → Obrovac, M. N., Chevrier, V. L., *Alloy Negative Electrodes for Li-Ion Batteries*, Chem. Rev. 114 (2014) 11444–11502.
- Fast-charge plating physics (overpotential, plating risk drivers) → Tomaszewska, A. et al., *Lithium-ion battery fast charging: A review*, eTransportation 1 (2019) 100011.
- Transport properties of EC-based LiPF₆ electrolytes (σ, t⁺ as plating levers) → Valøen, L. O., Reimers, J. N., *Transport Properties of LiPF₆-Based Li-Ion Battery Electrolytes*, J. Electrochem. Soc. 152 (2005) A882.
- SEI growth model & parameterization (base set) → Chen, C.-H., Planella, F. B., et al., *Development of Experimental Techniques and Parameterization of a Physico-Chemical Model for Li-ion Batteries*, J. Electrochem. Soc. 167 (2020) 080534.
- Simulation framework (PyBaMM) → Sulzer, V. et al., *Python Battery Mathematical Modelling (PyBaMM)*, J. Open Res. Softw. 9 (2021) 14.
- Thermal-runaway three-reaction kinetics (run-tr model basis, as stated in the tool docstring) → Kim, G.-H. et al., J. Power Sources (abuse-model calibration); Coman, P. T. et al., J. Power Sources (2016) — cited as the simulator's built-in model source.
- Thick-electrode / down-gauged-collector ED heuristics → domain experience (no precise source).