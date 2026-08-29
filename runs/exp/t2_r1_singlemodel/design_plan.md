# Design Plan — t2_r1_singlemodel: Grid Energy Storage Battery

**Case**: Grid energy storage cell | **Run**: t2_r1_singlemodel (funnel_voting OFF ablation)
**Protocol**: Virtual Battery Factory five-stage funnel | **Date**: 2026-08-25

## 1. Objective decomposition (entry-0 contract)

| # | Metric | Threshold | Decision layer | Key levers |
|---|---|---|---|---|
| 1 | Gravimetric energy density | ≥ 327.18 Wh/kg | stage2 | collectors, separator, porosity, electrode thickness (mass); achievable discharge window (capacity) |
| 2 | 4C fast charge, no lithium plating | anode potential ≥ 0 V throughout | stage3 | negative porosity/particle size/N–P, electrolyte conductivity |
| 3 | Anode SEI after 100 × 1C cycles | ≤ 500 nm | stage2 | SEI kinetic rate constant (film-forming additive bridge) |
| 4 | Anode SEI after 500 × 1C cycles | ≤ 550 nm | stage2 | SEI kinetics (expected binding constraint, ~sqrt(t) growth) |
| 5 | Discharge capacity retention at −20 °C | ≥ 90% of 25 °C 1C capacity | stage2 | electrolyte conductivity (low-T formulation bridge), positive electrode thickness/porosity |

No T_max red line is given in the task text → T_max_K is monitored and reported, not a criterion.
Trade-off expectation: ED ↑ (thicker/denser electrodes) vs low-T rate capability and 4C plating margin ↓ (transport) — Pareto frontier to be located by simulation.

## 2. Candidate strategy

**Round 1 — molecular funnel (mace only, funnel_voting OFF) + baseline characterization.**
Funnel candidates (electrolyte additives, roles targeting the three failure modes):
- FEC (fluoroethylene carbonate) — SEI film former, suppresses SEI growth & plating
- VC (vinylene carbonate) — SEI film former
- PS (1,3-propane sultone) — SEI film former, graphite protection
- EP (ethyl propionate) — low-viscosity ester co-solvent, low-T conductivity
- LiDFOB (difluoro(oxalato)borate anion) — SEI/CEI film, low-T interfacial impedance
- LiDFP (difluorophosphate anion) — interfacial film, low-T impedance reduction

Hard elimination lines: mace `converged` must be true; mace `energy_ev` ≤ 0.0 eV. (xtb HOMO line unavailable in this ablation — no run-xtb.)

Baseline characterization (Chen2020): 1C discharge (SPMe → DFN), `calc-energy`, `aging_1C_100cyc`, `aging_1C_100cyc --cycles 500`, `lowT_discharge`, `4C_charge_45C --thermal lumped --plating`.

**Round 2+ — parameter bridge + architecture variants (exploration_force ON: 2–4 per round).**
Bridge map (values marked estimate unless a tool output):
- FEC / VC / PS → `"SEI kinetic rate constant [m.s-1]"` ×0.3 (literature: fluorinated/oligomeric SEI grows slower — Zhang 2006)
- LiDFOB → `"SEI reaction exchange current density [A.m-2]"` reduction (electron-migration-limited SEI suppression)
- EP (+LiDFP) → `"Electrolyte conductivity [S.m-1]"` override (low-T formulation; flattens Arrhenius dependence — approximation, marked)
Architecture variants: thin collectors (Al 8 µm / Cu 6 µm), thin separator (10 µm), negative porosity 0.30 / particle radius 4 µm (plating margin), positive thickness/porosity sweep (low T vs ED).

## 3. Budget allocation

R1 funnel + baseline ≈ 8 runs · R2 bridge + architecture ≈ 5 runs · R3 refinement ≈ 4 runs · R4 Stage-4 safety on final + closing. Aging-500 runs only on shortlisted candidates. No round cap; iterate until achieved or session budget exhausted.

## 4. Risk and fallback plan

- **500-cycle SEI** (expected binding): ×0.3 kinetics → check; if > 550 nm, strengthen (×0.1, or SEI exchange-current cut); if model-impossible → three-strike questioning → honest negative result.
- **−20 °C retention ≥ 90%** (hardest): conductivity override + thin positive electrode; watch ED trade-off; escalation questioning if infeasible within allowed levers.
- **4C plating**: negative-electrode architecture first (porosity/particle/N–P), electrolyte σ second; verify in coupled thermal at 45 °C.
- **ED**: mass-side levers are model-exact; capacity-side depends on the set's initial-lithiation window (initial concentrations excluded as levers — baseline comparability).

## 5. References (domain basis)

| Direction | Source |
|---|---|
| FEC/VC/PS film-forming SEI suppression | Zhang, S.S., J. Power Sources 162 (2006) 1379–1394 |
| Li plating mechanisms & mitigation | Liu, Q. et al., RSC Adv. 6 (2016) 88683–88700 |
| Ester co-solvents for low-temperature electrolytes | Smart & Ratnakumar et al., J. Electrochem. Soc. (2010–2011 series) |
| SEI growth kinetics, sqrt-time aging | Broussely, M. et al., J. Power Sources 146 (2005) 90–96 |
| Chen2020 parameter set | Chen, C.-H. et al., J. Electrochem. Soc. 167 (2020) 080534 |
| Agent protocol / evaluation-and-fallback design | this skill's references/ (papers-confident: Expert-Guided LLM Reasoning for Battery Discovery) |
| Grid-cell design margins (collector/separator thickness floors) | domain experience (no precise source) |


## Revision history

- 2026-08-25 (D_ec finalization): aging-500 @8e-20 dies deterministically at cycle ~174
  (IDA_CONV_FAIL, retried identically) -> cannot complete 500 cycles. Fallback 1e-19
  completes 500 cycles, SEI500 439.74 nm <= 550. FINAL D_ec = 1e-19 (params_r3*.json
  updated; 4C/energy/lowT unaffected — D_ec only enters SEI growth; SEI100 re-measured).