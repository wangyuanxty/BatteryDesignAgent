# Design Plan — c1_t1_r1: Next-Generation Pure Electric Sedan Battery

**Task (verbatim):** "Design a battery for a next-generation pure electric sedan: energy density >= 392.61 Wh/kg, support 4C fast charge (no lithium plating), maximum temperature <= 60 C, overcharge to 4.7 V without triggering thermal runaway"

**Execution mode:** headless zero-interaction — thresholds parsed and pre-registered in log.jsonl entry 0; degrees of freedom take the widest interpretation (recorded in entry-0 meta.freedoms). `real_compute=false`. Ablation switches all ON (full protocol). `start_stage=3` (task names no new materials); ceiling escalation available.

---

## 1. Objective decomposition and trade-off expectations

| Metric (entry-0 key) | Threshold | Judgment basis | Decision layer |
|---|---|---|---|
| `energy_density_wh_kg` | ≥ 392.61 | calc-energy contract formula: ED = ∫V·I₁C dt ÷ Σ(layer thickness × (1−porosity) × density × area); electrolyte excluded | stage2 |
| `plated` | == false | 4C_charge_45C with `--plating`: any `anode_potential_v` < 0 V → plating | stage3 |
| `T_max_K` | ≤ 333.15 (60 °C) | max cell temperature in **all** simulated scenarios (4C charge, overcharge); lumped thermal | stage3 |
| `triggered` | == false | overcharge protocol (0.5C to 4.2+0.5 = **4.7 V**) → `run-tr --sim` mechanical TR judgment | stage3 |

**Multi-objective trade-off expectations (Pareto structure):**
- **ED ↔ T_max**: thicker/higher-loading electrodes raise ED but increase polarization heat and thermal path length → higher T_max at 4C. Mitigation levers: cooling coefficient h↑ (thermal management freedom), porosity↑, thinner current collectors/separator (raise ED without thickness growth).
- **ED ↔ plating**: plating margin improves with N/P↑ (thicker anode → lower anode utilization → higher anode potential during 4C charge) but N/P↑ adds anode mass. Particle-size ↓ adds active surface (plating margin ↑, polarization ↓) at no mass cost.
- **Overcharge robustness ↔ ED**: lower cell resistance (electrolyte σ↑, thinner electrodes) reduces overcharge heating; cooling h↑ helps directly. Overcharge heating and 4C heating share the same mitigation levers — no conflict expected.
- **Voltage window constraint**: "overcharge to 4.7 V" pins the upper cut-off at 4.2 V (overcharge protocol = cut-off +0.5 V) → NMC811-family cathode systems (Chen2020/OKane2022 and derivatives). LNMO.json (4.7 V cut-off → overcharge 5.2 V) and ORegan2022 (4.4 V → 4.9 V) do not reproduce the task's 4.7 V overcharge and are deprioritized; charge cut-off is an excluded design lever.

## 2. Candidate strategy

**Round 1 (baseline characterization, not a proposal round):** Chen2020 default system, unmodified parameters:
- `1C_discharge` (SPMe) → `calc-energy` → true baseline ED, mass, capacity, DCR, midpoint voltage.
- `4C_charge_45C` (SPMe, `--thermal lumped --plating`) → baseline T_max_K, anode_potential_v.
- `overcharge` (SPMe, lumped) → `run-tr --sim` with `--mass-kg` from calc-energy → baseline `triggered`.
- Opening ceiling assessment (Section 4): compute the best-possible architecture+formulation ED ceiling of the 4.2 V NMC811/graphite family and decide: architecture-only achievable → Stage 3 loop; objective above ceiling → **escalate into Stage 2 material design** (higher-capacity anode system / electrolyte formulation), per ceiling_escalation (ON).

**ED improvement ladder (priority order, cheapest mass first):**
1. Thin current collectors (Al 16→8 µm, Cu 12→6 µm) and separator (12→8 µm, porosity↑): pure mass removal, no electrochemical penalty (minor DCR trade-off).
2. Anode supply ↑ if discharge is anode-limited: thicker negative electrode / higher negative active-material fraction (N/P↑) — also helps plating margin.
3. Cathode loading ↑ (thickness, active fraction) if cathode-headroom-limited.
4. Porosity ↑ (lighter electrodes) — must watch polarization/DCR.
5. If the architecture ceiling < 392.61 → **Stage 2 escalation**: custom high-capacity anode system JSON (SiOx blend: literature-sourced `Maximum concentration in negative electrode`, density, OCP-consistent window) or electrolyte formulation for transport; molecular additive funnel if electrolyte formulation route is taken.

**Safety improvement ladder (4C plating + T_max, overcharge heating):**
1. `Total heat transfer coefficient` h: 10 → 20–50 (liquid-cooling-class, thermal management freedom).
2. `Negative particle radius` 5.86 → 2–3 µm (rate capability, plating margin).
3. Electrolyte `Electrolyte conductivity`/`Cation transference number` ↑ (formulation freedom; literature-sourced values).
4. N/P↑ via negative thickness (plating margin) — shared with ED lever 2; balance jointly.
5. Overcharge TR: the mechanical `run-tr` ODE decides; mitigations = cooling h, thermal mass (mass_kg from calc-energy).

**Exploration discipline:** `exploration_force` ON → 2–4 architecture/system variants per proposal round, each simulated individually (SPMe first; DFN for 5C/rate-sensitive confirmations and finalists).

## 3. Budget allocation

- R1: baseline characterization + ceiling assessment (4 simulations + calc-energy + run-tr).
- R2–R6: ED architecture loop (2–4 variants/round, SPMe 1C + calc-energy each; DFN spot-check for best variants).
- R7–R10: safety loop (4C + overcharge + run-tr per candidate; tune h / particle size / N/P / electrolyte).
- R11–R15: joint fine-tuning, aging check if coating/doping candidates emerge, finalist DFN re-verification, closing.
- Trim or extend per fallback routing; no round cap — iterate until achieved or budget exhausted (honest negative result otherwise).

## 4. Risk and fallback plan

- **R1 — ED ceiling below 392.61 (most likely hard constraint).** Diagnosis via ceiling assessment: compute asymptotic ED (infinite electrode thickness, zero overhead) vs 392.61. If architecture+formulation cannot reach → **escalate to Stage 2**: high-capacity SiOx anode system (custom JSON, literature parameter values, recorded in propose) or electrolyte formulation. Symptom→scale: ED shortfall rooted in material capacity/voltage → Stage 2; rooted in mass overhead/polarization → Stage 3.
- **R2 — 4C plating unavoidable.** Ladder: particle size ↓ → electrolyte σ↑ → N/P↑ → cooling. If still plated after 3 strikes → three-strike questioning (system assumption / boundary assumption / metric assumption) and honest record.
- **R3 — overcharge T_max > 60 °C or run-tr triggered.** Cooling h↑ and resistance ↓ first; re-check mass_kg correctness in run-tr (`--mass-kg` mandatory, t7_r1 lesson). If TR is mechanically unavoidable at 4.7 V for this family → record negative on that metric honestly.
- **R4 — SPMe/DFN solver failures.** Read errors verbatim, fix parameter legality, retry; DFN auto-degrades to SPMe (recorded in `model_used`).
- **R5 — Chen2020 first-cycle low-capacity artifact** (initial state discharged, cathode 27% lithiated): do not compare first cycles across systems; rely on calc-energy contract numbers per system, per protocol note.
- **Three-strike rule**: same failure cause 3 consecutive rounds → stop blind tuning, question assumptions layer-by-layer (system/boundary/metric), plan-update entry with direction change or honest negative close (escalation field in final).

## 5. References (domain basis — direction → source)

- SiOx/high-capacity alloy anodes raise anode specific capacity → Obrovac & Chevrier, *Chem. Rev.* 114 (2014) 11444 (Si-alloy anodes); literature SiOx blend capacities (≈1200–1500 mAh/g for SiO_x, ~3300–3600 mAh/g for Si).
- NMC811/graphite cell parameterizations → Chen et al., *J. Electrochem. Soc.* 167 (2020) 160534; O'Regan et al., *Electrochim. Acta* 425 (2022) 140700; O'Kane et al., *J. Electrochem. Soc.* 169 (2022) 040530.
- Plating criterion (negative potential < 0 V vs Li/Li⁺ during charge) → Waldmann et al., *J. Power Sources* 384 (2018) 107; standard fast-charge literature (domain experience).
- Electrolyte transport (σ, t⁺, D) determines 4C polarization → Nyman et al. (2008) / Landesfeind et al. (2019) parameterizations built into the PyBaMM sets; Logan & Dahn, *J. Electrochem. Soc.* 167 (2020) 140546 (electrolyte design for fast charge).
- Smaller particles → higher active surface → lower local current density, improved rate capability (domain experience, no precise source).
- LNMO 4.7 V spinel cathode → Markovsky et al. / Duncan et al. LNMO OCP plateau (as cited in the skill library `data/LNMO.json`).
- Thermal runaway three-reaction kinetics (SEI decomposition / anode–electrolyte / cathode–electrolyte) → Kim et al. (2019), Coman et al. (2016), as implemented in `bda.simulators.thermal_runaway`.
- EV battery cooling (liquid cooling h ≈ 20–60 W/m²/K class) → industry practice (domain experience, no precise source).
