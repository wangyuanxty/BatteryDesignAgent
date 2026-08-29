# Design Plan — t2_r1_noforce (grid energy storage battery)

Case: design a grid-storage battery. Thresholds (contract, parsed verbatim from task text, entry 0):
energy density ≥ 327.18 Wh/kg · 4C fast charge without Li plating · anode SEI ≤ 500 nm after 100×1C cycles · discharge capacity retention ≥ 90% at −20 °C · SEI ≤ 550 nm after 500×1C cycles.
Ablation: `exploration_force` OFF (no forced 2–4 architecture variants per round; variants proposed at relevant moments only). `ceiling_escalation`, `funnel_voting` ON (defaults). `real_compute=false`. `start_stage=3` (no materials named in task) on `Chen2020` (anchor-table default, no system named).

## 1. Objective decomposition (decision layers + expected trade-offs)

| Metric | Layer (entry 0) | Expected binding? | Primary lever (scale) |
|---|---|---|---|
| ED ≥ 327.18 Wh/kg (calc-energy contract caliber, electrolyte excluded) | stage2 | **Yes — likely binds** | Architecture: electrode thickness ↑, porosity ↓, current collector ↓, separator ↓ |
| SEI ≤ 500 nm @100 cyc | stage2 | Probably passes (Chen2020 baseline ≈ 449 nm @100cyc per signal-scale reference in SKILL.md) | Coating bridge (`SEI kinetic rate constant`) if needed |
| SEI ≤ 550 nm @500 cyc | stage2 | **Yes — likely binds** (ec-limited SEI keeps growing; 449→~700–1000 nm extrapolated) | Coating (SEI kinetics ↓), N/P ↑ (shallower anode lithiation), particle radius ↑ (less area) |
| Retention ≥ 90% @−20 °C (vs 25 °C, 1C) | stage2 | **Yes — likely binds** (carbonate transport at 253 K) | Electrolyte σ/D ↑ (formulation bridge), electrode thickness ↓, porosity ↑, particle radius ↓ |
| 4C @45 °C, no plating (anode potential ≥ 0 V) | stage3 | Maybe (thick-ED variants worsen) | Particle radius ↓, N/P ↑, electrolyte σ ↑, thickness ↓ |

**Trade-off map**:
- ED ↑ (thick/dense electrodes) **vs** 4C plating & low-T retention ↓ (transport-limited) — Pareto front; must not overshoot thickness.
- High-conductivity electrolyte: win–win for 4C + low-T, zero ED cost (electrolyte excluded from contract mass). Most promising single lever for two binding metrics.
- SEI suppression: no ED/rate cost; only visible in aging protocol (~3 s/100 cycles SPMe).
- Cooling h: helps T_max (monitored, no task threshold) and indirectly plating margin via temperature; grid storage would have active cooling — available lever.

## 2. Candidate strategy

- **Round 1**: baseline characterization — 1C discharge (SPMe quick-screen → DFN precise), `calc-energy`, `lowT_discharge`, `4C_charge_45C` (thermal lumped + plating), `aging_1C_100cyc`, `aging_1C_100cyc --cycles 500`. Opening ceiling assessment (thin-CC/thin-sep/low-porosity/high-σ combination limits) → decides material escalation.
- **Rounds 2+**: targeted architecture variants against measured gaps (expected: ED + lowT + SEI@500). Variants proposed at relevant moments only (exploration_force OFF).
- **Escalation (ceiling_escalation ON)**: if low-T retention or 500-cycle SEI is shown to be material-bottlenecked after architecture space is probed → Stage 2 formulation/coating candidates (electrolyte σ/D/t⁺ overrides; SEI kinetic rate constant reduction), values from literature or marked estimate (never masquerading as simulation output).
- **Final round**: full protocol battery on the winning design (1C DFN + calc-energy + lowT + 4C + aging 100 + aging 500) — every contract metric with mechanical evidence.

## 3. Budget allocation (rounds)

1. Baseline + ceiling assessment (this round).
2–5. Architecture sweep (ED ↔ rate/lowT Pareto; SEI-relevant geometry).
6–8. Electrolyte transport + coating escalation (as ceiling assessment dictates).
9–10. 500-cycle aging verification on finalists (SPMe; DFN if affordable).
11. Final candidate full protocol battery + closing.

## 4. Risk and fallback plan

- **R1 (low-T 90%)**: if architecture+electrolyte levers saturate below 90% → three-strike questioning (electrolyte σ ceiling in this parameterization; task boundary: formulation adjustable → not exhausted until σ/D levers tried); if still unreachable → honest negative-result final with "reachable if relaxed to X" statement. Never relax thresholds.
- **R2 (ED 327.18)**: NMC811/graphite cell-level practical ED with aggressive architecture ≈ 320–350 Wh/kg (domain experience, no precise source) — margin is thin; fallback route: thin collectors (Al 10 µm / Cu 8 µm), separator 16–20 µm, porosity 0.25–0.30, thickness balance. If ceiling < target → escalate to system-switch candidate (anchor table) — recorded, not silently drifted.
- **R3 (SEI@500)**: coating bridge (SEI kinetic rate constant ↓, ec-limited model; signal-scale reference: ×0.1 kinetics → 449→385 nm @100cyc) + N/P ↑; compare coating vs baseline **on the same system**.
- **R4 (4C plating)**: if thick-ED variants plate → negative particle radius ↓, N/P ↑, σ ↑; plating judgment strictly mechanical (`anode_potential_v` min < 0 → plated=true, tool-derived).
- **Solver/numerical risk**: DFN fallback auto-degrades to SPMe; aging must stay on Chen2020 (aging-capable).
- **Artifact-awareness**: aging capacity trajectory may climb-then-saturate (voltage-window artifact) — annotate honestly; rely on `sei_thickness_nm_end`.

## 5. References (domain basis, real sources only)

- SEI growth, ec-reaction-limited model and its parameter dependence → PyBaMM documentation, SEI models (pybamm.readthedocs.io); S. E. J. O'Kane et al., "Lithium-ion battery degradation: how to model it", Phys. Chem. Chem. Phys., 2022, 24, 7909.
- Electrolyte transport as the dominant low-temperature limitation (viscosity/conductivity/D of carbonate electrolytes at −20 °C) → K. Xu, "Nonaqueous Liquid Electrolytes for Lithium-Based Rechargeable Batteries", Chem. Rev. 2004, 104, 4303; low-T electrolyte reviews → domain experience (no precise source).
- Fast-charge lithium plating criterion (negative electrode potential < 0 V vs Li/Li⁺) → domain experience (no precise source); coupled thermal-electrochemical fast-charge models → domain experience (no precise source).
- NMC811/graphite cell energy-density ceiling ~320–350 Wh/kg with thin foil/separator → domain experience (no precise source).
- Chen2020 teaching parameterization (NMC811/graphite) → C.-H. Chen et al., J. Electrochem. Soc. 167 (2020) 080534.

## 6. Revision history

- R5 closing update (three-strike trigger): SEI@500 <= 550 nm measured unreachable across three rounds (R3 coating kinetics x0.4 -> 745.7 nm; R4 N/P rebalance -> 933.8/1012.8 nm; R5 strongest coating x0.1 -> 701.4 nm and system switch OKane2022 -> 1067.7 nm). Growth-law analysis: the harness ec-reaction-limited SEI model cannot saturate (grown regime j_sei -> F*c0*D_ec/L); measured minimum growth ratio 100->500cyc = x1.68 (F1); k-saturation floor L(100) ~385 nm -> L(500) >= ~650 nm for any sanctioned design. Direction change: stop SEI tuning; F1 (neg r 3 um + porosity 0.42 + ceramic coating k_SEI x0.4) locked as best design - 4 of 5 criteria pass, plating solved (+0.0071 V min anode potential); closing with three-strike questioning documented in the final entry (escalation field). Proposals to the protocol (recorded, not applied): (a) extend the coating bridge with 'SEI solvent diffusivity [m2.s-1]'; (b) expose a saturating (electron-tunneling-limited) SEI model in the aging harness.
