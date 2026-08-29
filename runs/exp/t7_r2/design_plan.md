# t7_r2 — HEV Battery Design Plan (Stage 1)

Case: Design a battery for a hybrid electric vehicle
- Energy density ≥ **327.18 Wh/kg**
- **4C fast charge without lithium plating**
- **SEI ≤ 550 nm** after 100 cycles at **45 °C**
- **Nail penetration (10 W short-circuit heat generation) without thermal runaway**

Headless zero-interaction execution: parameters parsed from task text; all unspecified degrees of freedom take the
widest interpretation (recorded in log.jsonl entry 0 `meta.freedoms`). Thresholds are the contract — no post-hoc revision.

## 1. Objective decomposition (metrics → decision layers)

| # | Metric | Layer | Protocol (mechanical) | Design levers |
|---|--------|-------|-----------------------|---------------|
| 1 | ED ≥ 327.18 Wh/kg | stage2 | `calc-energy` contract formula (electrolyte excluded) | inactive-mass cut (CC/separator thickness), porosity, electrode utilization; SiOx system switch |
| 2 | SEI ≤ 550 nm @45 °C/100 cyc | stage2 | `aging_1C_100cyc_45C` → `sei_thickness_nm_end` | anode SEI kinetics (coating bridge: SEI kinetic rate constant / exchange current density) |
| 3 | 4C no plating | stage3 | `4C_charge_45C --thermal lumped --plating` → min(`anode_potential_v`) < 0 V ⇒ plated | N/P ratio, negative particle radius, porosity, electrolyte σ/t⁺, SiOx OCP shift |
| 4 | Nail (10 W) no TR | stage3 | `run-tr --q-nail 10 --mass-kg M` → `triggered` | cell thermal mass, cooling h (thermal-management freedom) |

Not criteria (absent from task text): T_max red line, capacity/voltage targets, 5C or low-T retention, cell
mass/dimension limits. Meanwhile T_max_K and plated are recorded every round for report trends.

**Trade-off map**
- ED ↑ (less inert mass / tighter porosity / thicker coatings) ⇄ 4C plating risk ↑ — this is the central Pareto tension.
- Higher cooling h helps metric 3's T_max and metric 4; no penalty elsewhere → HEV pack liquid cooling is a one-way door.
- SiOx anode ↑ capacity and lifts anode OCP away from 0 V (plating margin), but interacts with SEI/cracking — aging must be compared on the same system.

## 2. Candidate strategy

1. **R1** — Baseline Chen2020 (task text names no electrode system → anchor-table deterministic default; aging-capable,
   full thermal/geometry set, dump-verified) across the full four-protocol suite + **opening ceiling assessment**:
   best-possible Chen2020 architecture vs 327.18 Wh/kg.
2. **Escalation gate** (`ceiling_escalation` ON): if Chen2020 ceiling < objective → Stage 2 system candidate
   **OKane2022** (NMC811/graphite+SiOx, cracking model, aging-capable) — system candidates skip the molecular funnel,
   simulated directly at Stages 3/4.
3. **R2+** — 2–4 architecture/formulation variants per round (`exploration_force` ON), each simulated and judged
   mechanically: CC/separator thinning, porosity, N/P, particle-size classes, electrolyte σ/t⁺ bridge, SEI-coating bridge.
4. **Nail** — cooling design = thermal-management freedom: HEV pack active liquid cooling `h_eff = 20 W/m²/K`
   (domain estimate); `hA = h × cell cooling surface area` passed to `run-tr`. Near-adiabatic default (hA = 0.05 W/K)
   recorded alongside (paired boundary declaration — the unfavorable condition is not hidden).
5. **Closing** — Top candidates endorsed (real_compute=false → endorse skipped honestly), `render` report + deliverables.

## 3. Budget allocation

- R1 baseline + ceiling: 5–7 runs · R2 system switch / architecture push: 4–6 · R3–R6 trade-off tuning: 2–4 each ·
  R7+ safety settle + closing. Foreseen **8–12 rounds, ~40–60 runs**; each round evaluated via `bda log-evaluate`.

## 4. Risk and fallback

- **ED gap** → ceiling assessment decides Stage-2 escalation before architecture tuning (avoid thrashing).
- **4C plating persists** → lever chain: N/P ↑ → negative particle radius ↓ → electrolyte σ/t⁺ ↑; same cause failing
  3 consecutive rounds triggers **three-strike questioning** (system assumption / task-boundary assumption / metric
  reachability), recorded in the final entry's `escalation` field.
- **SEI @45 °C overshoot** → coating bridge (SEI kinetic rate constant ×0.1; measured magnitude reference on the
  Chen2020 set: 449 → 385 nm at 25 °C/100 cyc); compare vs baseline on the same system only.
- **Nail TR at near-adiabatic hA** → cooling-design lever, both conditions logged (no favorable-only testing).
- **Iron rules**: no threshold relaxation, no fabricated values, no completion claim without log evidence.

## 5. References (directional basis; honesty constraint — no fabricated sources)

| Direction | Source |
|---|---|
| Si/SiOx anodes raise capacity; alloy OCP shifts | Obrovac & Chevrier, *Chem. Rev.* 114(23), 2014, 11444–11502 |
| Avoiding lithium plating under fast charge (transport, particle size, N/P) | Colclasure et al., *J. Electrochem. Soc.* 166(8), 2019, A1412 |
| Thermal runaway mechanism in Li-ion (abuse scaling) | Feng et al., *Energy Storage Mater.* 10, 2018, 246–267 |
| SEI growth kinetics and coating control | Peled & Menkin, *J. Electrochem. Soc.* 164(7), 2017, A1703 |
| Thermal-runaway three-reaction kinetics (run-tr model calibration) | Kim et al. 2019 / Coman et al. 2016 (cited by bda run-tr docstring) |
| HEV pack active liquid cooling effective h ≈ 20–100 W/m²/K | domain experience (no precise source) |

## Revision history

- 2026-08-26 (R0): initial plan — baseline Chen2020 + ceiling gate + HEV liquid-cooling nail strategy.
- 2026-08-26 (post-R1): Chen2020 baseline measured — ED 400.75 Wh/kg, SEI 476.09 nm @45C/100cyc (both pass); 4C plating (anode min −0.1918 V) and nail (triggers 322 s near-adiabatic) fail. Ceiling: no ED gap → no Stage-2 material escalation for ED; OKane2022 negative OCP 0.076 V vs Chen2020 0.092 V (at x=1.0) → system switch would not fix plating either.
- 2026-08-26 (post-R2): single-lever probes — best plating gains: t⁺ 0.4 (+0.089 V) and anode particles 3 μm (+0.054 V); thicker anode backfires (−0.2482 V, SEI 542.7 nm) → rejected; σ=1.5 S/m no gain → not binding. Nail: h=50 (hA=0.2655) passes protocol defaults (T_max 336.3 K) but hot-soak probe (318.15 K) triggers at 588.6 s (ignition ≈ 356 K) → cooling design raised to h=80 W/m²/K (hA=0.4248) for hot-soak margin.
- 2026-08-26 (R3): combination round — fine particles × t⁺ × anode porosity, all with h=80 liquid cooling (see log.jsonl propose round 3).
- 2026-08-26 (post-R3): nail criterion closed at h=80 (hA=0.4248): T_max 321.7 K, hot-soak probe also no trigger; plating narrowed to −0.0097 V (T4 = 3 µm + t⁺ 0.5 + porosity 0.32) — ~10 mV residual electrolyte-phase droop at the separator interface.
- 2026-08-26 (R4, achieved): F1 = 2.0 µm anode + t⁺ 0.5 + anode porosity 0.32 + h=80 → 4C anode min +0.0090 V (no plating); SEI 463.1 nm; ED 423.6 Wh/kg; nail T_max 321.7 K (hot probe 321.7 K, no trigger). All four criteria pass (log-evaluate verdicts pass, checked=4). F1 selected over F4 (separator-porosity variant) to preserve standard-separator mechanical/melt-integrity margin.