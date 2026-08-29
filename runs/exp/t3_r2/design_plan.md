# Design Plan — t3_r2: Power-Tool Battery

Case: `runs/exp/t3_r2` · Base system: Chen2020 (NMC811/graphite pouch, nominal 5 Ah, area 0.1027 m²) · `start_stage: 3` · `real_compute: false`
Written before any simulation (Stage 1, zero simulation budget). Revision history appended at bottom on material direction changes only.

## 1. Objective decomposition (decision thresholds, verbatim from task text)

| # | Metric | Threshold | Judgment layer | Simulation evidence source |
|---|---|---|---|---|
| 1 | Nominal capacity | ≥ 2 Ah | stage2 | 1C DFN discharge `capacity_ah` |
| 2 | 5C discharge capacity retention | ≥ 95 % | stage2 | 5C DFN `capacity_ah` ÷ same-params 1C DFN `capacity_ah` (mechanical, derived file) |
| 3 | 4C fast charge, no lithium plating | `plated == false` | stage3 | 4C charge at 45 °C `anode_potential_v` min ≥ 0 V |
| 4 | Maximum temperature | ≤ 60 °C = 333.15 K | stage3 | **both** operating scenarios: 4C/45 °C charge `T_max_K` AND 5C/25 °C discharge `T_max_K` (derived key `t_max_5c_k`) |
| 5 | Power density | ≥ 4000 W/kg | stage2 | `calc-energy` contract formula: P = V_OC²/(4·DCR)/mass |

**Trade-off expectations (multi-objective map):**
- **Power density & rate capability vs capacity-per-area**: thinner electrodes shorten ionic transport → lower DCR and better 5C/4C behavior, but cut capacity per unit area and raise the mass share of current collectors/separator. Capacity is then recovered by electrode area (area cancels in W/kg to first order; capacity ≥ 2 Ah is soft — the 5 Ah pouch class already has margin).
- **DCR & heat vs E-rate stress**: every lever that lowers DCR (thin electrodes, small particles, thin separator, high-σ electrolyte) also lowers I²R heat in BOTH scenarios → one lever family serves metrics 2, 3, 4, 5.
- **Plating vs anode porosity/N-P**: 4C charge suppresses plating via anode charge acceptance — higher negative porosity (Li⁺ supply to separator interface), smaller anode particles, and higher N/P (thicker negative relative to positive) all raise the plating margin but add mass (W/kg penalty) — the tightest trade to balance.
- **T_max vs heat generation**: heat gen ∝ I²·DCR + reversible term; heat rejection = h·A·(T−T_amb). Levers: DCR reduction (above) + thermal management h (allowed DoF; 4C/45 °C case has only 15 K headroom → expect h > contract default 10 W/m²K, e.g. forced-air class 40–100 W/m²K).

## 2. Candidate strategy

- **Round 1 — baseline + first architecture family**: characterize the Chen2020 baseline stack (75.6/85.2 µm electrodes, ε_pos 0.335/ε_neg 0.25, r_p 5.22/5.86 µm, sep 12 µm) on all four protocols; in parallel propose 2 architecture variants pushing the power design direction: high-rate porosity variant (ε↑ both electrodes, neg more) and a thin-electrode variant (≈50/60 µm + area compensation to hold ≥ 2 Ah margin). Thermal lever (h) held at contract default 10 in round 1 to expose the raw thermal gap, then sized in round 2.
- **Follow-up direction per fallback routing**: capacity short → area/thickness compensation (Stage 3); retention/power short → thinner electrodes + smaller particles + electrolyte σ override (Stage 3); plating → anode porosity / N-P / particle size / σ (Stage 3); T_max short → DCR levers first, then h escalation (Stage 3 thermal DoF). Material-scale issues (potential window) are not expected; ceiling assessment (below) gates whether Stage 2 escalation is ever needed — expected answer: no, architecture space suffices.
- **Exploration discipline**: 2–4 variants per round (`exploration_force` ON); each candidate gets its own 1C/5C/4C + calc-energy suite and its own `log-evaluate` entry (batch mode, one entry per candidate).

## 3. Opening ceiling assessment (executed during R1 baseline; decides escalation)

Estimate the best-possible architecture+formulation of Chen2020 chemistry vs the objective:
- **Power density**: with the most aggressive honest stack (≈35/45 µm electrodes, ε≈0.45/0.45, 5/8 µm separator, small particles 2–4 µm, σ_e boosted toward 1.2–1.5 S/m, thin CC 10 µm) DCR ≈ 5–8 mΩ and mass ≈ 90–120 g → P/kg ≈ 3.7²/(4×0.007)/0.11 ≈ 4 400–6 000 W/kg → **4000 W/kg reachable in the architecture space; no material escalation expected**. If measured R1 numbers contradict (baseline DCR much higher than design-track expectation), reassess per plan-update trigger.
- **5C retention ≥ 95 %**: classic power-cell territory (thin + small-particle + high-σ); expected reachable; verify numerically.
- **4C no plating**: reachable with anode-side levers (N/P ↑, ε_neg ↑, r_neg ↓); the 45 °C ambient actually aids plating margin but tightens T_max.
- **T_max ≤ 60 °C at 4C/45 °C**: only 15 K headroom — hardest metric; expects DCR reduction + escalated h. Fallback position if still short after h escalation: honest negative result with the relaxation noted (per three-strike questioning discipline).

## 4. Budget allocation

- R1: baseline (4 protocols) + 2 architecture variants + ceiling write-up → 1 evaluate batch (3 entries).
- R2–R3: refine toward all five thresholds (composition of levers by measured gap), 2–3 candidates/round.
- R4: best-candidate full confirmation suite + safety re-check; residual rounds only if a metric sits within tuning distance.
- Closing: deliverables (design_spec/BOM/datasheet/calc/DVPR/DFMEA/delivery index + PDFs), `verify-deliverables`, `render`, `endorse` (honest skip for real_compute=false), `final`.
- Contingency: if 3 consecutive rounds fail the same metric → three-strike questioning (system/boundary/metric), plan update, direction change — no blind re-tries.

## 5. Risk and fallback plan

- **Risk A — T_max unachievable at 4C/45 °C**: mitigate via DCR↓ and h↑; questioning path: is h beyond ~100 W/m²K (liquid-class) still a power-tool design? If the metric stays unreachable, final reports the negative result + precise relaxation (e.g., "T_max ≤ 60 °C met at h=X; without it T_max=Y").
- **Risk B — plating margin and retention fight each other** (high porosity helps anode but hurts volumetric transport?): decouple by neg-side porosity and pos-side thickness; measure per side.
- **Risk C — Chen2020 initial-SOC artifact**: fixed globally at the test-fixture level (entry-0 meta), not per candidate.
- **Risk D — DFN stiffness at 5C/4C**: DFN auto-degrades to SPMe; rate-scenario evidence then uses the fallback model with honest `model_used` annotation (SPMe underestimation is documented in SKILL; the final design will be re-run DFN).
- **Risk E — solver failures from aggressive params**: read error verbatim, adjust protocol legality, rerun (no blind retries); failures are logged, not hidden.

## 6. References (domain basis — all real, no fabricated sources)

- Power/energy cell design trade & areal-capacity limits → Gallagher et al., "Optimizing Areal Capacities through Understanding the Limitations of Lithium-Ion Electrodes", J. Electrochem. Soc. 163(2) A138–A149 (2016).
- Fast-charge lithium-plating fundamentals on graphite → Weiss et al., "Fast Charging of Lithium-Ion Batteries: A Review of Materials Aspects", Adv. Energy Mater. 11, 2101126 (2021).
- Chen2020 parameterization itself (the system we design on) → Chen, C.-H., Brosa Planella, F., O'Regan, K., Gastol, D., Widanage, W. D., Kendrick, E., "Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models", J. Electrochem. Soc. 167, 080534 (2020).
- Power-oriented electrode design methodology (thin/porous/small-particle) → domain experience (no precise source pinned); consistent with the Gallagher et al. design map above.
- Lumped-thermal fast-charge temperature control → domain experience (no precise source pinned).

## Revision history

- (initial) — written before R1 simulation.
- after R1 (material direction change, mirrored in log `plan_update_r1`): R1 measured retention 8.7–18.9 % (5C) with DCR 4.1–5.4 mΩ and power density 22.4–24.5 kW/kg → power density/capacity were soft, retention + plating + T_max are the binding metrics. Root cause localized: solid-diffusion alone (τ_pos ≈ 6800 s vs 720 s test) plus liquid transport — **architecture/formulation space, Stage 3 only** (ceiling confirmed, log `funnel_ceiling`). R2 strategy: multi-lever power stack (particle radii 5.22/5.86 → 1.3/1.6 µm; porosity 0.45/0.40; thickness 45/56 µm; electrolyte overrides σ = 1.5 S/m, D_e = 6e-10 m²/s) + a no-particles attribution isolate. New audited design rule: **each candidate's `Nominal cell capacity [A.h]` is re-based to its own delivered 1C capacity (iterated to < 2 % drift)** so 5C/4C protocols test true C-rates of the resized cell.