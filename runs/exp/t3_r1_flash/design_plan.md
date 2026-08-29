# Design Plan — VBF Power-Tool Cell (t3_r1_flash)

## Case
- Goal (verbatim): "Design a battery for power tools: nominal capacity ≥ 2 Ah, support 5C discharge (capacity retention ≥ 95%), support 4C fast charge (no lithium plating), maximum temperature ≤ 60°C, power density ≥ 4000 W/kg."
- Headless run: zero-interaction execution; all parameters parsed from task text; defaults for unspecified ones.
- Workspace: runs/exp/t3_r1_flash. Case ID: t3_r1_flash.

## Parameter parsing (entry 0 audit)
- Electrode system: task text names no electrode system → deterministic anchor-table default **Chen2020** (recorded; baseline teaching parameterization, NMC/graphite, 5 Ah nominal).
- start_stage: task involves no new materials → **3** (cell design); materials use system baseline (source marked `baseline`).
- real_compute: **false** (default; no explicit true-compute request).
- Criteria (verbatim thresholds → decision layers):
  - stage2: `capacity_ah` ≥ 2.0 (1C discharge capacity = nominal); `retention_5c` ≥ 0.95 (5C capacity ÷ 1C capacity, same params, mechanical); `power_density_w_kg` ≥ 4000 (calc-energy: V_OC²/(4·DCR)/mass).
  - stage3: `T_max_K` ≤ 333.15 (60 °C; measured under 4C_charge_45C protocol, thermal lumped, ambient 318.15 K); `plated` = false (anode_potential_v min ≥ 0 during 4C charge).
  - stage1: none (start_stage 3 — no molecular funnel).
- Degree-of-freedom boundary (widest interpretation, per zero-interaction rule; task text declares no restrictions):
  - electrode_system: adjustable — start Chen2020 (anchor default); system switch (OKane2022/ORegan2022/Prada2013) only if ceiling assessment shows Chen2020 infeasible.
  - electrolyte_formulation: adjustable (σ/t⁺/D transport overrides via parameter bridge).
  - electrode_modification: adjustable (coating/doping — reserve; no aging target in this task, so mainly unused).
  - cell_architecture: adjustable (thickness/porosity/N-P/separator/current collector/particle size).
  - thermal_management: adjustable (Total heat transfer coefficient h; cooling surface area fixed by geometry).
- Excluded levers (protocol): solid-phase conductivity/diffusivity, initial concentrations, initial SEI thickness, charge cut-off voltage.

## Objective decomposition & trade-offs
| Metric | Threshold | Dominant levers | Expected trade-off direction |
|---|---|---|---|
| capacity_ah | ≥ 2.0 (baseline 5.0) | electrode thickness/area; porosity | thinning electrodes reduces capacity & mass together |
| retention_5c | ≥ 0.95 | electrode thickness↓, porosity↑, particle radius↓, electrolyte σ/D↑ | thickness↓ hurts capacity (above); particle↓ hurts energy density slightly |
| power_density_w_kg | ≥ 4000 (baseline ≈1.3–1.6 k) | DCR↓ (thickness↓, transport↑) AND mass↓ (thickness↓) → ∝ 1/(DCR·m) ∝ 1/th² | strongly favors thin, low-mass design |
| T_max (4C charge, 45 °C amb) | ≤ 333.15 K | heat ∝ I²·R_eff (low DCR), cooling h↑; ΔT = P_heat/(h·A) | h is a free thermal lever; low-DCR helps both power & heat |
| plated (4C charge) | false | thin anode, small negative particles, high porosity anode, high σ_e, high T (45 °C helps kinetics) | small particles raise cost/complexity |

Priority: power density and 5C retention are the hardest (baseline likely ~1.4 kW/kg and ~60–75% retention); capacity 2 Ah is easy (baseline 5 Ah); T_max and plating handled via low-DCR design + cooling h + particle/thickness tuning.

## Candidate strategy
- Round 0: baseline characterization (1C dfn + calc-energy, 5C dfn, 4C charge 45C dfn lumped+plating) → quantify gaps; opening ceiling assessment (thin electrode + high-σ electrolyte + high h combination) written to funnel log.
- Round 1 (architecture variants, Chen2020 base): 2–3 thin-electrode designs with N/P preserved:
  - V1 "Power-thin": both electrodes ×~0.6–0.65 thickness, small negative particles (plating/rate), electrolyte transport boost (σ≈+50–100%, t⁺ up), h=50–100 for the safety run.
  - V2 "Power-thinner": ×~0.45–0.5 thickness to reach 95% @5C and 4000 W/kg if V1 short.
  - V3: porosity/particle refinement variant if plating or retention remains the binding constraint.
- Fallback routing: retention/power/T_max failure → Stage 3 (architecture/electrolyte params); plating failure → Stage 3 (anode particle/porosity/σ) then Stage 2 electrolyte design only if transport ceiling binds; three-strike → question assumptions, plan update.

## Budget allocation
- R0 baseline: 3 dfn sims + 1 calc-energy.
- R1–R3: ≤3 candidates/round × (1C dfn + 5C dfn + 4C dfn) ≈ 9 sims/round worst case; keep to spme for 1C screening if dfn too slow, dfn mandatory for 5C/4C and for final passers.
- Closing: deliverables + render + verify. Total target ≤ ~15–20 min wall clock (flash run).

## Risk and fallback plan
- Risk 1: 4000 W/kg out of reach for Chen2020 even at 35 µm (positive solid σ=0.18 S/m is excluded as a lever). → ceiling assessment quantifies the floor DCR; if infeasible, escalate: system switch (e.g., OKane2022 — same NMC811 chemistry, valid cracking model) or accept negative result with "if X relaxed to Y" note.
- Risk 2: 95% retention at 5C needs very thin electrodes (est. ≤35–40 µm) → capacity drops toward ~2.3–2.6 Ah; monitor ≥ 2.0 bound; adjust area/porosity to recover capacity if needed (height/width fixed? no — geometry adjustable).
- Risk 3: T_max at 45 °C ambient with 15 K headroom; ΔT = P_heat/(h·A), A=0.00531 m² fixed → h≈100 W/m²/K forced-air gives ≈0.53 W/K cooling; low-DCR design must keep P_heat ≤ ~8 W at 4C charge.
- Risk 4: plating at 4C — mitigated by small negative particles (measured +14.6 contribution in T1), high anode porosity, high σ_e, thin anode.
- Three-strike question layers: (1) model/system — is Chen2020's transport/geometry physically representative of a power cell; (2) boundary — is cooling h=100 or system switch within the task scope (widest interpretation: yes, recorded); (3) metric — is 4000 W/kg reachable under the excluded-lever constraint; if not, negative result with relaxation note.

## References (domain basis; real sources only)
- Thin electrodes improve rate/power and reduce DCR → H. Zheng, J. Li, X. Song, G. Liu, V.S. Battaglia, Electrochim. Acta 71 (2012) 258–265 (electrode thickness effects on cathode performance).
- Small particles / high anode porosity suppress lithium plating under fast charge → T. Waldmann, B.-I. Hogg, M. Wohlfahrt-Mehrens, J. Power Sources 384 (2018) 107–124 (Li plating review).
- High-conductivity electrolyte reduces polarization and plating → K. Xu, Chem. Rev. 104 (2004) 4303–4418 (nonaqueous electrolytes review).
- Fast-charge plating model → M. O'Kane et al., Phys. Chem. Chem. Phys. 24 (2022) 7909 (basis of OKane2022 parameter set).
- Power density P = V²/(4R) max-power transfer convention → domain standard (no precise source).
- High-power tool packs use forced-air/active cooling in charge stands (h ≥ 50–100 W/m²/K) → domain experience (no precise source).

## Revision history
- v1 (2026-08-25): initial plan, as above.
- v2 (2026-08-25, closing): execution outcome recorded. R0 baseline confirmed the plan's Risk 1/2/3/4 expectations (retention 0.087, plated=true, T_max 354.3 K — root cause: positive solid diffusivity 4e-15 m²/s, particle τ≈6.8 ks at r=5.22 µm; excluded lever → particle-radius fix). R1 thin+transport (V1/V2) met retention/T_max/power/capacity but plating marginal (−3.9 mV at final charge instant). Plan update (fallback routing, same scale): R2 targeted anode-geometry fix (thicker negative 58 µm, ε_neg 0.38, r_neg 1.0 µm, r_pos 0.8 µm, σ_e 2.4 S/m, t⁺ 0.5, D_e 3.5e-10) → V4/V5 pass all 5 criteria (V4: 3.438 Ah, retention 0.987, T_max 321.9 K, plated=false +22.6 mV, 111,807 W/kg). No three-strike trigger (objective achieved in 3 rounds). Final verdict: achieved. Deliverables under deliverables/ (DS/BOM/DSH/CALC/DVPR/DFMEA/IDX, md+xlsx+PDF) + report.html.
