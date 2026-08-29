# Design Plan — t5_r1_noceiling (flagship vehicle battery)

Case: next-generation flagship vehicle battery
Contract (entry 0, pre-registered, not post-hoc revisable):
- `energy_density_wh_kg ≥ 500.94` (stage2)
- 4C fast charge without lithium plating → `plated = false` (stage3)
- maximum cell temperature ≤ 60 °C → `T_max_K ≤ 333.15` (stage3, judged on 4C_charge_45C protocol)
Ablation: `ceiling_escalation = OFF` (task text) — no proactive material design; tune within the existing cell/architecture formulation space. `exploration_force = ON` (default). `real_compute = false`.

## 1. Objective decomposition and trade-off expectations

| Metric | Threshold | Layer | Expected difficulty |
|---|---|---|---|
| Gravimetric energy density | ≥ 500.94 Wh/kg | stage2 | High — needs substantial active-layer mass fraction (contract ED formula excludes electrolyte/casing) |
| 4C charge, no plating | plated=false (anode potential ≥ 0 V throughout 4C charge) | stage3 | Medium — controllable via transport/kinetics/current-density levers |
| Max temperature (4C charge @45 °C) | ≤ 60 °C (333.15 K) | stage3 | High — only 15 K headroom over the 45 °C protocol ambient; needs aggressive cooling + low heat generation |

Decision-relevant mechanics of the contract formula (calc-energy): `ED = ∫V·I_1C dt / Σ(layer thickness × (1−porosity) × density × area)` with I_1C fixed at nominal 5 A.
Consequences that shape the strategy:
1. **Energy scales with capacity extracted at 5 A, mass with total layer mass.** Thickening electrodes raises capacity ~linearly but mass sub-linearly (CC + separator mass is fixed per area) → ED rises toward the active-layer asymptote. Also raises voltage during the 5 A discharge (shallower depth, less overpotential) → extra energy gain.
2. **Area (electrode height × width) is ED-neutral at fixed areal loading** (energy and mass scale together) but is a first-order safety lever: current density falls as 1/area → less plating-driving anode overpotential and I²R heat falls as 1/area (R ∝ 1/area) while thermal mass rises with area. Volume/cost penalties are outside the contract.
3. **CC mass is large** (baseline: pos CC 43 g/m² + neg CC 107 g/m² ≈ 35 % of total areal mass) — thin current collectors are a pure ED win in this framework (in-plane CC resistance is not modeled in DFN/SPMe defaults; thermal mass term only).
4. **4C is a fixed 20 A current** (4 × nominal 5 Ah). Overloaded (thicker) electrodes make the true cell capacity exceed the nominal, so the 900 s / 20 A charge ends at a lower true SOC → anode potential stays positive (plating risk peaks at high SOC) and less total heat per unit cell mass. This is the classic overcapacity design direction.
5. **T_max: lumped thermal balance dT/dt = (Q − hA(T−T_amb))/Cp.** With hA small at h=10 (≈0.053 W/K) the cell is nearly adiabatic over 900 s → heat generation dominates. Meeting ≤60 °C at 45 °C ambient needs (a) heat reduction (transport/kinetic levers, area) and (b) aggressive cooling h (thermal-management freedom; framework records no cooling-system mass penalty — to be noted honestly in the report).

Expected trade-off: ED vs charge safety are **not** strongly opposed in this contract formulation (thickness helps both ED and lowers effective charge C-rate), which makes the 500.94 Wh/kg objective plausibly reachable; the binding pair is ED vs T_max via heat generation and the physical manufacturability floor of CC/separator thickness.

## 2. Candidate strategy

- **Round 1 (baseline + probes):** characterize baseline Chen2020 (1C SPMe→DFN + calc-energy + 4C SPMe w/ lumped thermal + plating), plus 3 architecture variants:
  - `A1 ThickCCslim` — ED direction: electrodes ×2 thickness, CC 16→8 µm / 12→6 µm, separator 12→10 µm (pure ED probe).
  - `A2 TransportCool` — safety direction: baseline geometry, electrolyte σ→2.0 S/m, t⁺→0.45, D→4.5e-10, particle radii ×0.5, h→200, area ×1.5 (transport/kinetic/cooling probe).
  - `CeilProbe` — ceiling assessment (recorded only; escalation disabled): extreme architecture+formulation combo (electrodes ×3, CC 4/4 µm, separator 8 µm, σ 2.2 / t⁺ 0.5 / D 5e-10, particles ×0.5, h 300, area ×2) → estimates the best-possible ED and 4C-safety limits of the existing system.
- **Rounds 2+:** refine along the levers that measured effective (thickness for ED; area/transport/h for plating & T_max; N/P via relative negative thickness; porosity only if needed — low porosity worsens transport). DFN for passers; final candidate re-verified in DFN on both protocols.
- **Safety co-check every round:** each variant gets 4C_charge_45C (lumped + plating) so stage3 metrics advance with stage2.

## 3. Budget allocation

~8 simulation rounds max (each ≤ 4 candidates × [1C SPMe (+DFN for passers) + calc-energy + 4C SPMe/DFN]), then closing deliverables. DFN reserved for passers/finalists to keep rounds fast.

## 4. Risk and fallback plan

- **ED unreachable in architecture space** (likely if asymptote < 500.94): three-strike questioning → if confirmed unreachable within boundaries, honest negative result with "if X relaxed" note; ceiling_escalation OFF forbids the material-design path.
- **T_max > 333.15 K:** raise h (immersion-class), enlarge area, cut heat (transport overrides, smaller particles). If h must exceed physical cooling limits (>~500 W/m²K), record as boundary failure.
- **Plating at 4C:** overcapacity (thicker), area up, particles down, σ/t⁺ up.
- **Parameter-name errors:** `unknown parameter name(s)` validation is the safety net; fix per error and rerun (no blind retries).
- **DFN solver failures:** auto-degrade to SPMe (model_used records fallback); treat as screening-level evidence, not final.

## 5. References (domain basis; no fabricated sources)

- Lithium plating criterion: anode surface potential < 0 V vs Li/Li⁺ during charge — standard fast-charge failure signature; implemented as irreversible plating model (PyBaMM OKane2022 parameterization used as plating defaults) → domain experience (no precise source).
- NMC811/graphite chemistry ceilings (≈200 mAh/g / ≈360 mAh/g practical) → domain experience (no precise source).
- Electrolyte conductivity baseline ≈1.1–1.5 S/m at 1 M LiPF6 EC:EMC (Nyman2008 correlation — the exact function in the Chen2020 parameter set) → Chen2020 parameter set itself (PyBaMM).
- High-conductivity/high-transference electrolyte formulation values (σ 2.0–2.2 S/m, t⁺ 0.4–0.5, D ~4–5e-10 m²/s) → domain estimates marked `estimate` (advanced fluorinated/high-concentration electrolyte literature; no precise source).
- Small particle radius → plating resistance at high rate: skill-internal measurement (T1: +14.6 contribution) → virtual-battery-factory SKILL.md (in-house measured).
- Cooling coefficient ranges (air ≈10, liquid 25–100, immersion ≥200 W/m²K) → domain experience (no precise source).
- LLM-agent battery-design methodology basis: this repo's references/ (e.g., "Advancing battery research through large language models: A review"; "Battery-Sim-Agent: Leveraging LLM-Agent for Inverse Battery Parameter Estimation"; "MatClaw: An Autonomous Code-First LLM Agent for End-to-End Materials Exploration"; "Expert-Guided LLM Reasoning for Battery Discovery") → repo paper library.
