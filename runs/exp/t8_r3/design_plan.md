# Stage 1 — Overall Design Plan (t8_r3)

**Case**: t8_r3 — long-endurance drone battery
**Task text (contract)**: energy density ≥ 446.18 Wh/kg · 5C discharge with ≥ 90% capacity retention · cell mass ≤ 40 g
**Mode**: zero-interaction execution (headless). All thresholds parsed verbatim into log.jsonl entry 0.

## 1. Objective decomposition / decision-layer criteria

| Layer | Metric | Threshold | Tool / source |
|---|---|---|---|
| stage1 (molecular) | max_energy_ev (mace) | ≤ 0.0 eV | run-mlp (only if molecular candidates arise) |
| stage1 (molecular) | max_homo_ev (xtb) | ≤ −6.0 eV | run-xtb (only if molecular candidates arise) |
| stage2 (cell) | energy_density_wh_kg | ≥ 446.18 | calc-energy (contract formula, 1C energy ÷ stack mass) |
| stage2 (cell) | retention_5c | ≥ 0.90 | 5C DFN capacity ÷ same-params 1C DFN capacity (mechanical) |
| stage2 (cell) | mass_kg | ≤ 0.04 (40 g) | calc-energy mass_kg |
| stage3 (safety) | T_max_K (4C/45°C charge) | ≤ 333.15 (60 °C default red line, task text unspecified) | run-pyamm 4C_charge_45C, thermal=lumped |
| stage3 (safety) | plated | false | run-pyamm 4C_charge_45C --plating (min anode potential ≥ 0 V) |

**Multi-objective trade-off expectations**
- *ED vs 5C retention (the central Pareto front)*: 1C discharge energy is fixed by chemistry × electrode loading per area; ED = energy ÷ mass. Thicker electrodes raise capacity per area (more energy within the 40 g mass budget) but worsen 5C polarization → retention loss. Expect a frontier: find the thickest electrodes that still hold retention ≥ 0.90, using thin inactive layers (Cu/Al foil, separator) to keep mass ≤ 40 g.
- *Mass budget reallocation*: mass_kg comes from Σ(layer thickness × (1−ε) × density × area). Current collectors and separator are pure dead mass: thinning them transfers the 40 g budget to active material → more energy at equal mass → higher ED. Chen2020 defaults: Cu 12 µm / Al 16 µm / separator 12 µm — all have thinner commercial grades (8–10 µm Cu, 10 µm Al, 9 µm separator) usable for a drone cell.
- *Area scaling*: contract energy is per-area-independent (PyBaMM PDE per unit area; I_1C from Nominal capacity), mass is ∝ area. Chen2020 default area (0.065 × 1.58 m) gives ≈43.5 g stack → exceeds the 40 g cap, so some mass reduction is mandatory. Strategy: thin the dead layers first (keeps full electrode area and nominal 5 Ah class), and only shrink width/height if dead-mass thinning alone does not reach ≤ 40 g. Target finished mass ≈ 39.5–39.9 g (constraint-satisfying, not formula-gamed smaller).
- *Voltage/capacity lever (fallback)*: 446.18 Wh/kg at 40 g ⇔ 1C discharge energy ≥ 17.85 Wh ⇔ ≈4.82 Ah at 3.7 V midpoint. Chen2020 mid-voltage ≈3.6–3.7 V and nominal capacity 5 Ah → expected energy ≈18.0–18.5 Wh → ED at 40 g ≈ 450–460 Wh/kg. Margin is thin; if 1C capacity falls below ~4.82 Ah, escalate to a higher-voltage system candidate (LNMO 4.7 V spinel, midpoint ≈4.17 V) — a Stage 2 *system* candidate (skips molecular funnel, direct Stage 3 simulation).

## 2. Candidate strategy

- **Round 1 — baseline characterization + first architecture variants** (exploration_force ON: 2–4 arch variants/round):
  1. `C0 baseline` (Chen2020, no overrides): contract ED, mass, 1C DFN capacity, 5C DFN retention, 4C/45°C safety. Establishes every target-facing number at default geometry.
  2. `V1 mass-fit-40g`: thin collectors + separator (Cu 12→8 µm, Al 16→10 µm, sep 12→9 µm) to bring mass under 40 g at full area.
  3. `V2 active-boost`: V1 + thicker electrodes (+10–20%) within the 40 g budget → higher energy; watch 5C retention.
  4. `V3 rate-margin`: V1 + smaller negative particle radius (5.86→4.0 µm) and/or higher electrolyte conductivity (+25% constant) → 5C retention headroom if baseline retention is short.
- **Directions afterward** (fallback routing):
  - retention_5c < 0.90 → Stage 3 rate fixes (particle size, electrolyte σ, electrode thickness down, porosity up) — architecture-scale cause.
  - ED < 446.18 at 40 g with retention saturated → Stage 2 escalation: system candidate LNMO (voltage jump) or SiOx anode set (OKane2022); if composition-level, run-comp NMC811 substitution (CUDA env `D:/anaconda/envs/py312`).
  - T_max_K > 333.15 → thermal-management freedom (h ↑, cooling surface area) — record cooling as design, not magic.
  - plated → Stage 3 rate-side fixes (thicker negative vs positive, lower charge polarization) — plating is stage-3-scale (capacity/temperature).

## 3. Budget allocation

- Rounds 1–3: baseline + architecture frontier (mass fit, thickness sweep) with per-candidate full metric set [1C SPMe→DFN, calc-energy, 5C DFN + derived retention, 4C charge safety]. ~4 sims + calc per candidate.
- Rounds 4–6: fine-tuning of the winning branch (particle size / electrolyte transport / porosity / thermal h).
- Rounds 7+: only if a Stage 2 escalation or aging/coating sub-loop is triggered; else closing.
- SPMe first as a quick screen (second-scale), DFN for passers and for all contract-grade numbers (5C must be DFN).

## 4. Risk and fallback plan

- **Risk A — 1C capacity < 4.82 Ah at fixed chemistry** (ED unreachable at 40 g): escalate Stage 2 → LNMO system candidate (midpoint voltage ≈4.17 V gives +13–15% energy); second option OKane2022 SiOx. Ceiling assessment in Round 1 states the numbers.
- **Risk B — 5C retention < 90% even at thin electrodes**: transport/kinetic fixes in order: negative-particle radius ↓ → electrolyte σ ↑ (constant override, marked estimate) → electrode thickness ↓. Re-evaluate after each; three strikes on the same cause → stop and question assumptions (recorded in final `escalation` field).
- **Risk C — T_max_K at 4C/45°C**: Chen2020 has complete thermal parameters (Cell volume 2.42e-5 m³, h=10 W/m²K); thin electrodes at 4C charge ⇒ modest heat. If breached: raise Total heat transfer coefficient (thermal-management freedom) and re-check plating.
- **Risk D — solver failures**: DFN failure auto-degrades to SPMe (output `model_used` records it); for contract numbers prefer DFN; if a parameter override is rejected (`unknown parameter name(s)`), fix key names per mapping table and rerun.
- **Three-strike rule**: same candidate family failing the same metric 3 consecutive rounds → stop blind tuning, run layer-by-layer questioning (system assumption / task boundary assumption / metric assumption), decide direction-change vs honest negative result. Never silently relax a threshold (entry 0 is the contract).

## 5. References (domain basis — real sources only)

- Base parameter set origin: Chen, C.-H., Brosa Planella, F., O'Regan, K., Gastol, D., Widanage, W. D., & Kendrick, E. (2020). *Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models.* Journal of The Electrochemical Society, 167, 080534 — the Chen2020 NMC811/graphite parameterization used as system baseline.
- Electrolyte transport functions: Nyman et al. (2008) conductivity/diffusivity correlations — inside Chen2020 (`Electrolyte conductivity [S.m-1]` functional parameters).
- High-voltage spinel as energy-density lever (LNMO 4.7 V class): domain experience from LiNi0.5Mn1.5O4 literature (high-voltage cathode design direction); precise source to be pinned at escalation time if used. (no fabricated citation)
- Thin-foil current collector practice (8–10 µm Cu / 10 µm Al commercial grades for high-energy mobile cells): domain experience (no precise source).
- Smaller negative particles → rate capability/plating resistance improvement: domain experience (no precise source); parameter-set particle radii are Chen2020 values (5.22/5.86 µm).
- Drone endurance ∝ pack specific energy, high-rate launch/hover transients require power cells or hybrid packs: domain experience (no precise source).

## Revision history

- v1 (initial plan, 2026-08-26): baseline direction; no updates yet.
- v2 (after Round 1 evaluate, 2026-08-26): all R1 candidates fail — mass/ED fixed by V1 (457.9 Wh/kg @ 38.05 g) but 5C retention 8.4–9.7% (target 0.90) and 4C/45°C T_max 354–357 K + plating everywhere. Direct DFN state-variable probe (scratch/diag_physics.py) located the 5C collapse: positive particle surface concentration saturates at ~96% of c_max at t≈62 s while the negative stays mid-range → bottleneck scale is positive solid-phase surface area/diffusion path. Solid diffusivity is a forbidden lever, so the architecture-scale fix is smaller particles + higher electrolyte transport. Risk B path activated (particle radius ↓, electrolyte σ/D/t⁺, not thickness ↓ — V2 showed thicker electrodes make saturation worse).
- v3 (after Round 2 evaluate, 2026-08-26): rate problem solved — V4 (pos 1.5 µm / neg 2.5 µm + σ=2.0 S/m, D=6e-10, t⁺=0.4 formulation overlay) gives retention_5c = 0.9805 (target 0.90) with ED 485.3 Wh/kg and 38.05 g; V6 thickboth pushes ED to 500.9 Wh/kg at 39.50 g with retention 0.9808. Failure frontier narrowed to exactly one binding pair: 4C/45°C — V4/V5/V6 (h=10) T_max 352.5–356.4 K > 333.15 K, while V7 (h=60 forced-air) cools to 328.5 K but plates (anode min −0.0102 V, colder cell slows anode kinetics). Trade-off confirmed: thermal cooling vs anode kinetic margin. (Mechanical evaluate entries re-run with corrected last-wins file order so T_max_K is judged from the 4C safety-protocol file — superseding entries recorded.)
- v4 (Round 3 proposal, 2026-08-26): strike the thermal-plating intersection from the anode side — V8 (h=60 + neg particle 1.5 µm), V9 (h=60 + neg electrode 100 µm, N/P up ~17%), V10 (h=40 + neg 1.5 µm, trade-off-curve midpoint probe), V11 (h=60 + both anode margins). V9/V11 width shrunk 1.51→1.504 m (mass-fit arithmetic ≤40 g, correction note logged to audit chain). Expected masses pre-checked in-script (38.22 g V8/V10; ~39.78 g V9/V11).
- v5 (after Round 3 evaluate, 2026-08-26): exit-condition reached — V8 (h=60 + neg 1.5 µm) PASSES all five criteria (retention 0.9862, ED 487.8 Wh/kg, 38.05 g, 4C/45°C T_max 327.27 K, anode +7.3 mV no plating); V10 (h=40) also passes (retention 0.9869, T_max 331.09 K, anode +10.7 mV). V9/V11 fail plating (−26.5/−10.8 mV): the thicker-negative capacity-margin route is empirically a plating *liability* at 4C/45°C (through-anode electrolyte polarization dominates the shallower end-of-charge state) — recorded as a negative result for the final report. V8 selected as primary: better thermal margin (5.9 K vs 2.1 K) at nearly identical ED/retention. Round 4 = margin confirmation around V8 (V12 neg 1.2 µm; V13 neg porosity 0.30) before Stage 4 abuse check and closing.
- v6 (final, 2026-08-26): CONVERGED — V13 porousanode selected and closed. Final metrics (all mechanical, tool-sourced): 1C 5.073 Ah · 18.568 Wh · ED 497.5 Wh/kg ≥ 446.18 ✓ · retention_5c 98.66% ≥ 90% ✓ · mass 37.32 g ≤ 40 g ✓ · 4C/45°C T_max 326.53 K ≤ 333.15 ✓ · anode_min +17.7 mV → plated=false ✓ · overcharge→run-tr triggered=false ✓. Final entry (action "final", verdict "achieved") + endorse-skip (real_compute=false) appended; report rendered; deliverables produced and verified per protocol.