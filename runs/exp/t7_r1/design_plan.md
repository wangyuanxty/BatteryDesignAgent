# t7_r1 Design Plan — HEV Battery (headless case run)

Date: 2026-08-25 · Zero-interaction execution (SKILL.md §0): all parameters parsed from task text, widest degree-of-freedom interpretation, no clarification round.

## 1. Objective decomposition (decision-layer criteria — contract: log.jsonl entry 0)

| Layer | Metric | Threshold | Likely difficulty (pre-simulation) |
|---|---|---|---|
| stage2 (cell) | Gravimetric energy density `energy_density_wh_kg` (calc-energy contract caliber) | ≥ 327.18 Wh/kg | LOW–MED: baseline mass estimate ≈ 43.5 g, ~18 Wh at 1C → ≈ 420 Wh/kg. Expected to pass with margin; margin is the trading budget for safety levers. |
| stage2 (cell) | SEI thickness after 100×1C cycles at 45 °C `sei_thickness_nm_end` | ≤ 550 nm | MED: Chen2020 baseline ≈ 449 nm at 25 °C (skill measured signal); 45 °C acceleration unknown (SEI growth activation energy = 0 in this set → T-dependence weak; must measure). |
| stage3 (safety) | 4C fast charge, no lithium plating `plated` | false (anode surface potential never < 0 V) | HIGH: 4C charge of thick high-loading NMC811/graphite typically dips the graphite potential below 0 V. Likely the binding constraint. |
| stage3 (safety) | Nail penetration, 10 W short-circuit heat, no thermal runaway `triggered` | false | HIGH at contract cooling (hA≈0.05 W/K ⇒ T_eq ≈ 498 K → SEI decomposition + anode-electrolyte reaction cascade). Thermal-management design freedom is the answer. |
| stage1 (molecular) | Elimination lines for possible Stage-2 escalation | `max_energy_ev` ≤ 0.0 eV, `max_homo_ev` ≤ −6.0 eV | inactive at start_stage=3; pre-registered for escalation traceability. |

Not adjudicated (absent from task text → NOT criteria, recorded in entry 0): capacity Ah, volumetric ED, 5C retention, −20 °C retention, overcharge, 4C T_max red line, cell mass/dimension constraints.

**Trade-off direction (Pareto expectation):**
- ED vs plating: thicker/denser electrodes ↑ ED but ↑ anode polarization at 4C (plating risk). ED margin (if confirmed) is spent on plating robustness.
- ED vs nail safety: heavier cell buffers heat but mass-normalized ED unchanged; inert mass ↑ ED↓. Better lever: cooling h (thermal management freedom).
- SEI vs rate: SEI-suppressing coating reduces capacity loss but changes anode kinetics only weakly; expect near-zero plating interaction at the parameter-bridge level.

## 2. Candidate strategy

**Base system:** Chen2020 (NMC811/graphite, 5 Ah, 0.065×1.58 m, pos 75.6 µm / neg 85.2 µm, sep 12 µm, cc 16/12 µm, SEI k=1e-12 m/s, j0_SEI=1.5e-7 A/m²). Deterministic anchor-table default (task names no system). Dump-verified: complete thermal/geometry set, positive OCP function `nmc_LGM50_ocp_Chen2020` → NMC811 confirmed.

**R1 — baseline characterization** (no parameter changes): 1C discharge SPMe + DFN, calc-energy, 4C charge @45 °C lumped+plating (DFN), aging 100×1C @45 °C, nail run-tr (q=10 W, mass from calc-energy). Plus **opening ceiling assessment**: best-case architecture (thin collectors/separator, low porosity, high transport electrolyte) ED estimate vs 327.18 → decide whether escalation to Stage 2 (system switch / material design) is needed.

**R2+ — targeted variants** (2–4 per round, each simulated through the full protocol set):
- Plating levers (architecture + formulation): negative particle radius ↓ (5.86→2–3 µm), N/P ↑ (negative thickness/porosity ↑), electrolyte conductivity 1.1→2–3 S/m (constant override), cation transference 0.2594→0.5, cooling h ↑.
- SEI levers (electrode-modification bridge, literature estimate): SEI kinetic rate constant ×0.1 (1e-13 m/s; FEC/VC-class SEI-suppression coating) and/or SEI reaction exchange current density ×0.1 (1.5e-8 A/m²; Al2O3-class electron-blocking coating). Compared against baseline on the SAME system.
- Nail levers (thermal management): hA = h × cooling area; contract h=10 W/m²K ⇒ hA≈0.053 W/K is near-adiabatic for a 10 W source. Design answer: liquid/forced-air cooling (h = 50–500 W/m²K) so T_eq < ~345 K; consistent h applied in the 4C lumped-thermal model.
- ED levers (only if margin erodes): separator 12→8–9 µm, collectors 16/12→10/6 µm, porosity optimization.

**Escalation triggers (proactive Stage-2 entry):** if the ceiling assessment shows ED ≥ 327.18 is unreachable within the NMC811/graphite architecture space → system-switch candidates (OKane2022 NMC811/graphite+SiOx) or LNMO high-voltage (library LNMO.json); if plating is transport-limited beyond formulation reach → same escalation.

## 3. Budget allocation

~10 rounds. R1 baseline+ceiling (1 round) → R2–R4 plating-focused architecture/formulation set (3 rounds) → R5 SEI coating → R6–R7 nail/thermal consolidation → R8 full-criteria re-verification of best design (DFN-precision pass) → R9 closing (endorse skip — real_compute=false — final, deliverables, render, verify). Shift budget toward whichever metric is still failing at R4 (plan-update mechanism).

## 4. Risk & fallback plan

- **Plating unreachable in architecture space** (3 strikes on anode potential < 0 V at 4C) → three-strike questioning: ① is 4C no-plating reachable for NMC811/graphite at 45 °C with this parameter set? ② is electrolyte transport override (σ/t⁺) within scope (freedom declared: yes)? ③ is the task itself reachable; if not, honest negative result with "reachable if X relaxed" note. Before concluding negative: escalate to system switch (SiOx anode shifts anode capacity; LNMO raises V but not anode margin).
- **SEI > 550 nm at 45 °C**: coating bridge params (kinetic rate ×0.1 / j0 ×0.1, literature-validated, marked `estimate`); if still failing → electrolyte formulation (additive) via molecular funnel (Stage 2 escalation, candidates FEC/VC-class), elimination lines per entry 0 stage1.
- **Nail TR triggered**: raise hA via cooling design (thermal-management freedom) until `triggered: false` with T_eq ≤ 345 K; record h as design value; keep consistency with 4C thermal model.
- **ED < 327.18**: architecture ED levers first (thin separator/collectors), then Stage-2 escalation (SiOx system switch / LNMO) — ED ceiling assessment at R1 decides pre-emptively.
- **Solver/numerical failures**: read errors verbatim, record, fix parameter legality or degrade DFN→SPMe (auto), never fabricate values.

## 5. References (domain basis — real sources only)

- Chen2020 parameter set (NMC811/graphite, 5 Ah): Chen et al., J. Electrochem. Soc. 167 080534 (2020) — PyBaMM parameter set; direction: baseline for NMC811/graphite fast-charge studies.
- OKane2022 parameter set (NMC811/graphite+SiOx): O'Kane et al., PCCP 24 7909 (2022) — direction: SiOx anode raises negative capacity → plating margin & ED (system-switch candidate).
- Nyman2008 electrolyte transport functions (used by Chen2020): Nyman, Behm, Lindbergh, Electrochim. Acta 53 6356 (2008) — direction: transport-limited fast-charge response to σ/t⁺.
- Thermal-runaway three-side-reaction kinetics: Kim et al. 2019 / Coman et al. 2016 (as cited by the bda `thermal_runaway` model source) — direction: SEI-decomposition → anode-electrolyte cascade; nail heat source as external Q.
- SEI suppression by film-forming additives / surface coatings (FEC/VC, Al2O3): domain experience (no precise source) — direction: SEI growth rate constant reduction, bridge to `SEI kinetic rate constant` / `SEI reaction exchange current density`.
- Plating avoidance at high C-rate: domain experience (no precise source) — direction: small negative particles, high-transference electrolyte, N/P margin, thermal control.
- LNMO high-voltage set: this skill's library `scripts/bda/simulators/data/LNMO.json` — direction: 4.7 V-class cathode for ED escalation.

*Revision history:* (appended on plan updates)
