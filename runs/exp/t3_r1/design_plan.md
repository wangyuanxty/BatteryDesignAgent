# Design Plan — Power-Tool Battery (Case t3_r1)

Revision history:
- R0 (2026-08-25): initial plan (Stage 1).
- R1 (2026-08-25): measurement-setup correction — the Chen2020 default initial state is empirically nearly charged (start OCV 4.036 V, 1C discharge 4.95 Ah); the planned charged-state initial-concentration override was dropped; all discharge protocols run with parameter-set defaults (log entries: plan update + criteria_meta_correction).

## 1. Objective decomposition (thresholds verbatim from task text)

| Metric | Threshold | Decision layer | Measurement source |
|---|---|---|---|
| Nominal capacity | ≥ 2 Ah | stage2 | 1C DFN discharge capacity from fully-charged state |
| 5C discharge capacity retention | ≥ 95 % | stage2 | 5C DFN capacity ÷ same-params 1C DFN capacity (mechanical) |
| 4C fast charge, no lithium plating | plated = false | stage3 | anode surface potential ≥ 0 V throughout 4C charge @ 45 °C (DFN, lumped thermal, plating module) |
| Maximum temperature | ≤ 60 °C (333.15 K) | stage3 | max of lumped-thermal T_max over 5C discharge (25 °C amb.) and 4C charge (45 °C amb.) |
| Power density | ≥ 4000 W/kg | stage2 | calc-energy contract: V_OC²/(4·DCR)/mass (mass = Σ layer×(1−ε)×density×area) |

Multi-objective trade-off expectations:
- **Power density vs capacity**: P/m ≈ V_OC²/(4·DCR·m); both areal resistance and areal mass fall with electrode thickness, so power density rises ~1/L² while capacity falls ~L. This is a *power-tool* cell: push toward the thin side while holding capacity ≥ 2 Ah (binding lower bound).
- **5C retention vs capacity**: same tension (thinner = better retention).
- **4C plating vs rate capability**: aligned, not conflicting — higher N/P (thinner cathode / thicker anode) and smaller anode particles suppress plating *and* raise rate capability; the cost is capacity.
- **T_max vs DCR**: every DCR reduction (thin electrodes, high-κ electrolyte, small particles) cuts heat; cooling coefficient h is the direct thermal-design lever. 4C charge at 45 °C ambient leaves only ~15 K headroom — the binding thermal case.

## 2. System and boundary

- **Base parameter set: Chen2020** (NMC811/graphite, nominal 5 Ah, wound geometry 0.065 m × 1.58 m). Task text names no electrode system → anchor-table default with record. Dump verification (2026-08-25): no SiOx parameter keys → not OKane2022; `SEI kinetic rate constant [m.s-1]` present (aging-capable); complete thermal/geometry parameters present (Cell volume, cooling surface area, h, collector/electrode densities and specific heats) → no injected defaults expected.
- **start_stage = 3** (task text contains no new-material/additive/electrolyte-design objective; performance and architecture task → materials use system baseline).
- **Degrees of freedom** (task text declares none → widest interpretation; recorded in log entry 0 `meta.freedoms`): electrode system, electrolyte formulation, electrode modification, cell architecture, thermal management — all adjustable.
- **Measurement notes** (audit-recorded): Chen2020 parameter-set default initial state is nearly charged (positive electrode 27 % lithiated = delithiated = high OCP; measured start OCV 4.036 V and 1C discharge capacity 4.95 Ah). All discharge protocols therefore run with parameter-set default initial conditions — **no initial-concentration override** (corrected in revision R1). The 4C-charge protocol keeps the runner's discharge-first experiment (charge from empty — worst case for plating).

## 3. Candidate strategy

- **Round 1 — baseline characterization**: Chen2020 defaults (1C/5C discharge, 4C charge @ 45 °C + plating, calc-energy); plus one as-is 1C run to document the discharged-initial-state artifact.
- **Round 2 — single-lever architecture variants** (attribute each metric to its driver): thin electrodes; small particles; fast-electrolyte transport; thin current collectors + thin separator; raised cooling h.
- **Rounds 3+ — composite candidates** combining passing levers; refinement on the binding metric.
- **Opening ceiling assessment**: after rounds 1–2, best-possible architecture+formulation vs objective; if the gap is transport/material-bound → escalate to Stage 2 (electrolyte formulation candidates / system switch), not more tuning.

## 4. Budget allocation

~10 rounds. Per candidate: 1C DFN + 5C DFN + 4C-charge DFN (lumped + plating) + calc-energy + mechanically-derived metrics + batch log-evaluate. SPMe reserved for quick screens.

## 5. Risk and fallback plan

- **Power density 4000 W/kg is aggressive for a 5-Ah-class cell** → if the architecture+electrolyte space tops out below threshold: three-strike questioning (model/system, boundary, metric), then an honest negative result with a "reachable if relaxed to X" note.
- Plating at 4C → Stage 3 fallback: N/P ↑, anode particle radius ↓, t⁺/κ/D ↑, porosity ↑.
- 5C retention < 95 % → Stage 3 fallback: thinner electrodes, smaller particles, electrolyte κ ↑.
- T_max > 333.15 K → Stage 3 fallback: h ↑ (cooling design), DCR ↓.
- Capacity < 2 Ah → stop thinning; re-check N/P and voltage window.

## 6. Domain basis (no fabricated references)

- Thin electrodes raise rate capability and power density (electrode-engineering practice — domain experience, no precise source).
- Small particle radius lowers charge-transfer resistance via higher active surface area (domain experience).
- High-conductivity / high-transference electrolytes suppress salt depletion and lithium plating under fast charge (battery-transport literature — domain experience, no precise source).
- Power-tool cells: high-rate NMC/graphite cylindrical/pouch, 5–10C rated, thin electrodes (industry practice, e.g., Sony VTC-class cells — domain experience).
- N/P ≈ 1.05–1.15 typical fast-charge plating margin (cell-design practice — domain experience).
- Natural convection h ≈ 10 W/m²/K; forced air ≈ 15–30 W/m²/K (heat-transfer engineering practice — domain experience).
