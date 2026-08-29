# Design Plan — t6_r3 Smartphone Battery (≥950 Wh/L, 4C no plating, ≤50°C, SEI ≤500 nm, plateau ≥4.1 V)

## 1. Objective decomposition (parsed thresholds, entry-0 contract)

| Metric | Threshold | Decision layer | Reachability expectation |
|---|---|---|---|
| Volumetric energy density | ≥ 950 Wh/L (`energy_density_wh_l`, calc-energy) | stage2 | Hard: requires dense/thin-layer stack; tension with plating |
| Voltage plateau | ≥ 4.1 V (`midpoint_voltage_v`, calc-energy) | stage2 | **Chemistry-bound**: NMC811/graphite cell midpoint ≈ 3.6 V — no architecture lever can raise it → forces high-voltage cathode (LNMO 4.7 V spinel) |
| Anode SEI thickness @100 cyc | ≤ 500 nm (`sei_thickness_nm_end`, aging_1C_100cyc) | stage2 | Moderate: Chen2020-family baseline ≈ 449 nm (library signal-scale reference); coating bridge (SEI kinetics ×0.1 → ≈385 nm) available |
| 4C fast charge | no plating (`plated: false`, anode_potential_v min ≥ 0) | stage3 | Hard at high ED: dense/thick electrodes shrink anode porosity → plating risk |
| Max temperature | ≤ 50 °C = 323.15 K (`T_max_K`, 4C_charge_45C, thermal lumped) | stage3 | Moderate: 45 °C ambient leaves only ≤5 K rise headroom → cooling h + transport levers |

**Priority & trade-off map**: plateau is a hard chemistry gate (no parameter can fix it → system switch is *necessary*, not optional). ED vs plating/T_max is a Pareto conflict: thicker/denser electrodes raise ED but worsen 4C plating and heating. Electrolyte transport (σ, t⁺) and cooling h are the two levers that help safety **without volume/mass cost** — use them first; geometry levers second.

## 2. Candidate strategy

- **Round 1 — baseline + ceiling assessment** (Stage 3 opening): characterize Chen2020 (default base, task names no system): 1C discharge SPMe + calc-energy + 4C_charge_45C (lumped+plating) + aging_1C_100cyc. Expected: plateau ≈ 3.6 V → **ceiling assessment concludes plateau criterion exceeds NMC811 system ceiling** → escalate to Stage 2 material design.
- **Round 2 — system switch**: candidate `systemLNMO` (`--base <lib>/data/LNMO.json`, Chen2020-inherited negative/SEI/geometry, 4.7 V spinel OCP, 4.5 Ah). Full Stage 3/4 suite on LNMO. Expect plateau ≈ 4.1–4.2 V (anchor table: midpoint 4.17 V); volumetric ED unknown (measure); 4C plating likely fails at baseline geometry.
- **Rounds 3+ — closure loop** on the passing system: (a) electrolyte transport formulation (σ/t⁺ up — plating & heat, zero volume cost); (b) cooling h (T_max, zero volume cost); (c) architecture: thin separator/current collectors, porosity/N-P balance, negative particle radius down (plating resistance); (d) SEI: coating bridge (`SEI kinetic rate constant [m.s-1]` ×0.1) only if baseline > 500 nm. Each round proposes 2–4 architecture variants (exploration_force ON), evaluated one-by-one with `bda log-evaluate`.
- **DFN precision**: SPMe screens; DFN 1C + 4C for any candidate near thresholds (plateau 4.1 V and ED 950 Wh/L decisions).

## 3. Budget allocation

~14 rounds max: R1 baseline/ceiling (4 runs), R2 LNMO baseline (4 runs), R3–R8 transport+cooling+architecture loop (2–4 variants/round), R9–R12 targeted refinement (ED plateau & plating margin), R13–R14 aging verification + DFN finalization. Deliverables after closure (~2 rounds equivalent).

## 4. Risk and fallback plan

- **R1: 950 Wh/L unreachable even with aggressive LNMO stack.** → three-strike questioning: (a) system assumption (is any library set capable? try OKane2022-class SiOx for negative capacity), (b) boundary (all five freedoms already widest), (c) metric (report honest negative with "reachable if ED relaxed to X"). No threshold relaxation.
- **R2: 4C no-plating vs 950 Wh/L conflict.** Safety is contract-critical: prefer plating-safe design; compensate ED with electrolyte/geometry levers that do not degrade anode kinetics (smaller negative particle radius raises plating resistance — measured T1 contribution +14.6%).
- **R3: LNMO aging capability.** LNMO.json inherits Chen2020 (SEI params present — verified in library source); if `bda error` nonetheless → record N/A honestly and reconsider system.
- **R4: solver failures** (4.7 V window, high C-rate) → read error verbatim, adjust protocol/parameters, rerun (never swallow-and-retry-identical).
- **Fallback routing**: capacity/ED/T_max shortfalls with acceptable material metrics → Stage 3 (architecture/params); plateau/potential-window failures → Stage 2 (system/material).

## 5. References (domain basis, direction → source)

- LNMO 4.7 V spinel plateau & OCP shape → library parameter set `scripts/bda/simulators/data/LNMO.json` + docstring (cites Markovsky et al. / Duncan et al. 4.7 V plateau literature) — repo-local, real.
- NMC811 cell-level discharge midpoint ≈ 3.61 V vs LNMO 4.17 V → SKILL.md §1.5 anchor table (repo-local).
- Smaller anode particle radius improves plating resistance at high rate → library protocol note (T1 measured +14.6%) + domain experience (no precise source).
- High-conductivity/high-t⁺ electrolyte mitigates plating & ohmic heating → domain experience (no precise source; transport-parameter literature).
- Thin current collectors/separator and dense electrodes raise volumetric ED → domain experience (no precise source).
- Chen2020-family SEI kinetics ×0.1 → 100-cycle SEI 449→385 nm → SKILL.md Stage 3 aging signal-scale reference (library-measured).

*No fabricated references: items without a precise source are marked "domain experience".*

## 6. Revision history (plan-update events)

### Update 1 — round 9 (key assumption overturned by simulation)

**Event**: SPMe screening margins (T_max +0.89 K, plating +39 mV, plateau +65 mV on the round-8 finalist V21) did not survive DFN precision verification. DFN results: plateau 4.0766 V vs 4.1 (−23 mV), T_max 330.57 K vs 323.15 (+7.4 K), amin −0.0522 V → plated=true. DFN resolves electrolyte concentration gradients and full electrode polarization that SPMe averages away: the 4C CC phase at 18 A lasts 36 s in DFN (vs 6 s in SPMe), driving the anode negative and dissipating ≈12.4 K of heat at h=100. DFN SEI (191.1 nm) is far below SPMe's 394.5 nm — SEI budget available.

**Direction change**: SPMe discredited as the screening layer for this cell class; all subsequent rounds run in DFN mode. Round-10 fix directions: (a) transport probe σ 2.0 / t⁺ 0.5 (plateau + heat); (b) N/P 1.28 plating probe (SEI budget affordable); (c) thin-and-wide repack — all layer thicknesses ×0.695, electrode area ×1.4388 (height 65→77.97 mm, width 1.58→1.8952 m), volume and capacity conserved, areal current density −30%, ionic path −30% (the engineering-correct attack on all three failures); (d) h 250 forced-cooling backstop.

**Budget reallocation**: rounds 10–12 DFN tuning, round 13 DFN final verification, round 14 closing deliverables.
