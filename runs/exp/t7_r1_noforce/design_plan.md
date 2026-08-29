# Stage 1 Design Plan — HEV Battery Cell (t7_r1_noforce)

**Case**: Design a hybrid electric vehicle battery cell:
- energy density ≥ 327.18 Wh/kg (calc-energy contract caliber, electrolyte excluded)
- 4C fast charge (900 s, 45 °C ambient) without lithium plating (anode potential ≥ 0 V vs Li/Li⁺ throughout)
- SEI ≤ 550 nm after 100 cycles at 45 °C (aging_1C_100cyc_45C)
- Nail penetration with 10 W short-circuit heat generation → NO thermal runaway (run-tr: dT/dt > 1 K/s or T ≥ 573 K = triggered)

**Ablation**: exploration_force OFF (task text) — no forced 2–4 architecture variants per round; variants proposed only when a metric demands them. ceiling_escalation ON, funnel_voting ON (defaults). real_compute = false (default).

**Starting point**: start_stage = 3 (task names no new materials/additives; metrics-only objective). Base = Chen2020 (protocol default for unnamed systems; anchor verified by parameter dump: pure-graphite negative, NMC811 positive, SEI aging model present, 5 Ah nominal).

## 1. Objective decomposition (with trade-off expectations)

| Metric | Threshold | Layer | Expected tension |
|---|---|---|---|
| energy_density_wh_kg | ≥ 327.18 | stage2 | vs 4C plating: thicker electrodes raise ED but worsen Li⁺ transport / anode overpotential |
| sei_thickness_nm_end (100 cyc, 45 °C) | ≤ 550 nm | stage2 | vs ED: SEI-suppressing coatings add mass (small); mostly free via kinetics, not mass |
| plated (4C charge 45 °C) | false | stage3 | vs ED: N/P margin (thicker negative) and porosity (transport) cost mass |
| triggered (nail 10 W) | false | stage3 | vs ED: thermal margin via cooling hA / mass; bigger cells absorb more heat |

T_max_K has no task-text red line → recorded in metrics for trend reporting only, not judged.

Baseline geometry (parameter dump): positive 75.6 µm/ε 0.335 (3262 kg/m³), negative 85.2 µm/ε 0.25 (1657 kg/m³), separator 12 µm (397 kg/m³), Cu CC 12 µm (8960), Al CC 16 µm (2700), t⁺ 0.2594, SEI k 1e-12 m/s, heat transfer 10 W/m²/K, area 0.1027 m², 5 Ah nominal.
Mass budget estimate: pos 0.164 + neg 0.106 + sep 0.0025 + CC 0.151 = 0.423 kg/m² → ≈43 g cell. **Cu collector alone ≈ 25 % of cell mass** — the single largest mass lever in the architecture space.

## 2. Candidate strategy

- **Round 1 — baseline characterization + ceiling probe** (exploration_force OFF: two candidates proposed because they are directly relevant to the ceiling decision):
  - Candidate A "Baseline Chen2020": all protocols, no overrides.
  - Candidate B "Ceiling Probe A": mass-minimized architecture (Cu 6 µm, Al 10 µm, separator 10 µm) + high-transport electrolyte (σ×~2, t⁺ 0.5, D×~2 — domain estimates, labeled) → probes the best-possible Chen2020-system ED and 4C plating margin.
- **Opening ceiling assessment** (from R1 outputs): ED ceiling ≈ baseline ED × mass-reduction factor (mechanical: collectors/separator minimized, electrode fractions maximized). If ceiling < 327.18 → escalate to Stage 2 (system switch to OKane2022 NMC811/graphite+SiOx — higher negative capacity per gram; aging-capable with SEI + cracking models).
- **Rounds 2+ — targeted fixes** per failing metric (symptom→scale mapping):
  - SEI fail → Stage 2 electrode modification (negative coating → "SEI kinetic rate constant [m.s-1]" reduction; inorganic coating skips molecular funnel, judged in aging; bridge value marked estimate).
  - Plating fail → Stage 3 architecture/formulation: N/P (negative thickness), particle radius, porosity, electrolyte transport overrides (σ/t⁺/D).
  - Nail triggered → Stage 3/4: thermal management ("Total heat transfer coefficient [W.m-2.K-1]"), operating T_max, mass.
  - ED fail → mass reduction (CC/separator), then Stage 2 system switch.
- No forced variant count per round (exploration_force OFF): propose only what the failing metric demands.

## 3. Budget allocation

- R1: baseline (1C spme+dfn, calc-energy, 4C@45C dfn+plating, aging 45C, run-tr nail) + ceiling probe (1C dfn, calc-energy, 4C@45C dfn+plating) — ~8 sims.
- R2–R5: targeted candidates, 1–3 sims each, evaluate per round via log-evaluate.
- Closing: endorse (skipped, real_compute=false), final, render, deliverables. No fixed round cap; iterate until achieved or turn budget exhausted.

## 4. Risk & fallback plan

- R1 risk: Chen2020 first-cycle capacity is known-low (initial state discharged, cathode 27 % lithiated) — do not compare first cycles; judge on stage2/stage3 keys only.
- Risk ED: if baseline ED is far below 327.18 and mass reduction is insufficient → three-strike questioning → system switch (OKane2022, SiOx) — Stage 2 system candidate (skips molecular funnel, direct Stage 3 sims).
- Risk plating: 20 A charge current in a 5 Ah cell — transport-limited; if anode potential dips below 0 V, verify with dfn (SPMe underestimates), then apply particle-size/N-P/transport levers in that order.
- Risk SEI: Chen2020 SEI growth has zero activation energy in the rate constant itself; 45 °C effect enters via transport/kinetics — if sei_thickness_nm_end > 550, coating lever (SEI kinetic rate constant ×0.5 step) on the SAME system for comparability.
- Risk nail: mass is tiny (≈43 g → mcp ≈ 39 J/K); 10 W continuous → equilibrium 498 K with hA 0.05 — if triggered, increase cooling hA / thermal design; if still triggered, escalate questioning (boundary: thermal management freedom is adjustable, recorded).
- Three-strike rule: same failure cause ×3 rounds → stop blind tuning, question model/system/task-boundary/metric assumptions layer-by-layer (recorded in final escalation field), plan-update entry, then continue with new direction or close as honest negative result.

## 5. References (domain basis)

- SiOx/graphite negative raises capacity & ED vs graphite (system-switch direction) → Obrovac & Chevrier, *Chem. Rev.* 114 (2014) 11444–11502.
- High-transport / tuned electrolyte mitigates fast-charge plating → Logan & Dahn, *Trends Chem.* 2 (2020) 354–366.
- SEI growth model lineage (ec-reaction-limited growth used by PyBaMM aging) → Ramadass et al., *J. Electrochem. Soc.* 151 (2004) A196.
- Nail/thermal-abuse modeling basis (run-tr three-reaction ODE) → Kim, Pesaran & Spotnitz, *J. Power Sources* 170 (2007) 476–489; ODE Arrhenius form per tool source (Kim et al. 2019 / Coman et al. 2016).
- Chen2020 parameter set (baseline cell) → Chen et al., *J. Electrochem. Soc.* 167 (2020) 080534.
- Electrolyte transport functions (Nyman2008) → Nyman, Behm & Lindbergh, *Electrochim. Acta* 53 (2008) 6356–6365.
- Plating criterion: negative electrode potential < 0 V vs Li/Li⁺ → domain experience (no precise source).
- Smaller active particles improve rate capability / plating resistance → domain experience (no precise source); skill-measured signal: T1 particle-size lever +14.6 % rate contribution.
- OKane2022 parameter set (potential system switch; plating + cracking modeling) → O'Kane et al., *J. Electrochem. Soc.* 169 (2022) 100501.
