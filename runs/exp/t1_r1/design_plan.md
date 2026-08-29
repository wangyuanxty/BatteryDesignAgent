# Design Plan — Next-Generation Pure Electric Sedan Battery (case t1_r1)

Headless zero-interaction run. All thresholds parsed verbatim from the task text; all
five degree-of-freedom categories take the **widest interpretation** (recorded in
log.jsonl entry 0 `meta.freedoms`).

## 1. Objective decomposition (contract, entry 0)

| # | Metric | Threshold | Decision layer | Judged by |
|---|---|---|---|---|
| 1 | Gravimetric energy density | ≥ 392.61 Wh/kg | stage2 | `calc-energy` contract formula (stack mass: electrodes + current collectors + separator; electrolyte and casing excluded — annotated honestly) |
| 2 | 4C fast charge, no Li plating | `plated = false` | stage3 | `run-pyamm --protocol 4C_charge_45C --thermal lumped --plating` (318.15 K ambient, 900 s); plating ⇔ `anode_potential_v` < 0 V at any instant |
| 3 | Maximum temperature | ≤ 60 °C = ≤ 333.15 K (mechanical conversion) | stage3 | `T_max_K` of the same 4C run (coupled lumped thermal) |
| 4 | Overcharge to 4.7 V, no thermal runaway | `triggered = false` | stage3 | `run-pyamm --protocol overcharge` (1C discharge → 0.5C charge to cut-off +0.5 V = 4.2+0.5 = **4.7 V**, matches task verbatim) → `run-tr --sim` ODE coupling (cell mass from calc-energy, `--mass-kg` mandatory) |

Trade-off map:
- **ED vs 4C**: thicker / lower-porosity electrodes raise ED but increase polarization → plating and heat. Thin current collectors and thin separator raise ED *without* rate penalty → primary ED levers.
- **Plating vs T_max**: faster transport (higher electrolyte conductivity/transference, smaller particles) helps both; cooling coefficient h helps T_max only.
- **Overcharge TR**: levers are overcharge heat (impedance), cell thermal mass (mcp = mass×900), and heat rejection (hA); cathode oxidative stability at 4.7 V is the material-level risk.

## 2. Candidate strategy

1. **R0 baseline** — Chen2020 defaults on all four protocols (anchor values).
2. **Ceiling probe** — best-architecture Chen2020: thin current collectors (Al/Cu down to ~6/4 µm), thin separator (~8–10 µm), moderate electrode thickening if 4C allows, lower porosity, smaller anode particles, elevated h. Test whether ED ≥ 392.61 Wh/kg and 4C-safety can coexist within the architecture space.
3. **Escalation (if ceiling insufficient or plating persists)** — Stage 2 material design:
   - system candidate **OKane2022** (NMC811/graphite+SiOx: higher anode capacity, higher lithiation plateau → plating margin, includes plating/cracking parameterization);
   - electrolyte **formulation candidates** (conductivity / transference-number / diffusivity overrides via the parameter bridge).
4. **Safety fine-tuning** — h for T_max; N/P, anode particle radius, porosity for plating; hA / mass for overcharge TR.

## 3. Budget allocation

| Phase | Rounds |
|---|---|
| R0 baseline + ceiling probe | 2 |
| Architecture exploration | 2–3 |
| Stage-2 escalation (system / formulation), if triggered | 2–3 |
| Safety fine-tuning | 2 |
| Deliverables + closing (render, verify) | fixed |

## 4. Risk and fallback plan

- **Risk A** — Chen2020 ED ceiling below 392.61 under 4C-safe architecture → escalate system switch (OKane2022 SiOx anode).
- **Risk B** — 4C plating → raise N/P ratio, smaller anode particles, higher electrolyte conductivity (formulation), higher anode porosity. Fallback scale: Stage 2 (formulation) or Stage 3 (architecture), per gap attribution.
- **Risk C** — T_max > 333.15 K → raise `Total heat transfer coefficient` (liquid cooling), reduce impedance.
- **Risk D** — TR triggered at 4.7 V overcharge → reduce overcharge heat (impedance), raise hA in run-tr (thermal-management DOF), larger thermal mass; material escalation only if architecture+formulation space is exhausted.
- **Three-strike rule** — same failure cause 3 consecutive rounds → stop blind tuning; question (1) model/system reachability, (2) task-boundary assumptions (DOF scope), (3) metric reachability — layer by layer, recorded in the `final` escalation field. Close as a negative result only if the questioning concludes "unreachable within the boundary".

## 5. References (domain basis — real sources only)

- Si/SiOx anodes raise capacity and lithiation plateau (plating margin): Obrovac & Chevrier, *Chem. Rev.* 2014, 114, 11444–11502 ("Alloy Negative Electrodes for Li-Ion Batteries").
- Electrolyte transport and interphases (σ, t⁺, D levers): Xu, *Chem. Rev.* 2014, 114, 11503–11618 ("Electrolytes and Interphases in Li-Ion Batteries and Beyond").
- Overcharge / thermal-runaway mechanisms (trigger physics): Feng, Ouyang et al., *Energy Storage Mater.* 2018, 10, 246–267 ("Thermal runaway mechanism of lithium ion battery for electric vehicles: A review").
- Plating criterion (anode potential < 0 V vs Li/Li⁺ under load): electrochemistry standard — domain experience (no precise source).
- Cooling coefficient ranges (air ≈ 5–10, liquid cold plate ≈ 50–200 W/m²K): domain experience (no precise source).

## 6. Non-adjudicated items (honest scope statement)

Not in the task contract → not judged: cycle life / aging, 5C rate retention, −20 °C
low-temperature retention, capacity Ah, volumetric density, nail penetration, cell
mass/dimension constraints. The 4C/T_max judgments use the 45 °C fast-charge protocol
(the library's standard extreme fast-charge scenario).

## 7. Revision history (plan-update mechanism)

- **R0–R1 (no revision)** — baseline + architecture round executed per original plan.
- **2026-08-25, before R2 (trigger 2+3: scale mismatch revealed by higher-fidelity measurement; key assumption overturned)** — diagnostic (`diag_protocol.py`, current profile extracted from the exact library experiment, reproducing cached outputs bit-for-bit) showed the 4C exam is a full 1C discharge followed by a true 20 A CC charge; the SPMe charge segment accepts only 0.21 Ah (37.9 s) making the SPMe plating readout near-vacuous, while the DFN accepts 1.59 Ah (~28% SOC) and plates from ~8% SOC onward (min −0.1357 V). Plating is transport/kinetic-limited high-rate charging from deep discharge — **not** end-of-charge saturation, so the N/P lever (plan Risk B) is irrelevant; root cause lives at electrolyte/anode-transport scale → fallback routing Stage 3 → Stage 2 formulation candidates (σ = 1.8 S/m, t⁺ = 0.45; parameter bridge, no new molecule, molecular funnel skipped, real_compute = false). Strategy updated: round 2 = formulation ladder E<F<G<H on Arch-D; round 3 reserve: t⁺ 0.5+, porosity 0.40 (with anode thickness compensation), particles 2.0–2.5 µm, separator 6 µm. DFN designated the authoritative 4C exam (also the stricter thermal exam: 342.0 K vs 325.8 K SPMe at h = 50).
- **2026-08-25, before R3 (execution deviation note, no-silent-drift rule)** — round-2 outcome: T_max solved (h = 100 → 328.3/327.4 K), plating −0.0149 V (H) = 15 mV short at the 4.2 V cut-off; measured side effect: H's 1C capacity fell 5.743 → 5.602 Ah (AMVF 0.65 anode near-limiting) → round-3 porosity increase is paired with anode thickness 110 → 120 µm (the round-2 reserve note's 95–100 µm direction is inverted by the measurement; recorded in r3 propose `llm_reason`).
- **2026-08-25, R3 outcome (no further revision)** — all four round-3 candidates pass (DFN): plating +7.5…+24.9 mV, T_max 325.7–326.3 K, ED 549.7–554.0 Wh/kg. **Finalist r3-I** (full package: t⁺ 0.55, porosity 0.40 + 120 µm anode, particles 2.5 µm, separator 6 µm, h = 100, σ = 1.8): ED 553.977 Wh/kg, 4C DFN T_max 325.655 K, anode min +0.0249 V, overcharge 4.7000 V with triggered = false (round-4 evaluate verdict: pass, all four registered criteria).

