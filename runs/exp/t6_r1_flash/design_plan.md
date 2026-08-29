# VBF Case t6_r1_flash — Smartphone Battery Design Plan (Stage 1)

Generated: 2026-08-25 · Mode: headless zero-interaction (flash budget) · Start stage: 2 (materials/system design)

## 1. Objective decomposition (criteria contract, verbatim from task text)

| # | Task metric (verbatim) | Decision layer | Criteria key | Threshold | Tool source |
|---|---|---|---|---|---|
| M1 | volumetric energy density >= 950 Wh/L | stage2 (cell) | `energy_density_wh_l` | min 950 | calc-energy output |
| M2 | voltage plateau >= 4.1 V | stage2 (cell) | `midpoint_voltage_v` (calc-energy plateau approximation, mechanical) | min 4.1 | calc-energy output |
| M3 | anode SEI thickness <= 500 nm after 100 cycles | stage2 (cell/aging) | `sei_thickness_nm_end` | max 500 | aging_1C_100cyc output |
| M4 | 4C fast charge (no lithium plating) | stage3 (safety) | `plated` | false | 4C_charge_45C --plating, min(anode_potential_v) < 0 → plated |
| M5 | maximum temperature <= 50 C | stage3 (safety) | `T_max_K` | max 323.15 (=50°C) | 4C_charge_45C --thermal lumped |
| — | molecular elimination lines (defaults; used if molecular candidates proposed) | stage1 | `max_energy_ev` / `max_homo_ev` | max 0.0 / max −6.0 eV | run-mlp/run-xtb |

- Priority / trade-off map: M1 (ED, thick electrode + high voltage) vs M4/M5 (fast-charge heat & plating, thin/low-resistance) vs M2 (thick electrode → polarization → plateau drop below 4.1 V). M1 and M2 both benefit from the high-voltage system (LNMO) — the 4.1 V plateau is the decisive system driver.

## 2. System determination (deterministic anchor mapping + record)

- Task text names **no electrode system** → anchor-table default would be Chen2020 (NMC811/graphite). **But** the task's own threshold M2 (plateau ≥ 4.1 V) is unreachable for NMC811 (cell-level discharge midpoint ≈ 3.61 V per anchor table; NMC811 OCP max ≈ 4.2 V only at 0% SOC, midpoint ~3.6–3.7 V). Ceiling assessment therefore forces a high-voltage cathode.
- Adopted system: **LNMO (LiNi0.5Mn1.5O4, 4.7 V-class spinel)** — anchor-table high-voltage system entry (`scripts/bda/simulators/data/LNMO.json`, passed as `--base` path; Chen2020 base + LNMO overlay, OCP bound to `lnmo_ocp` symbol). Anchor: OCP(0.5)≈4.4 V (formula), discharge midpoint ≈ 4.17 V (measured, anchor table) vs NMC811 3.61 V.
- LNMO inherits from Chen2020: negative electrode (graphite), electrolyte, separator, geometry, thermal, **SEI aging model** (aging-capable). Recorded in funnel log + entry 0 meta.

## 3. Candidate strategy (round roadmap)

- **R1 — baseline + ceiling assessment (0–1.5 rounds):** characterize LNMO baseline (1C discharge + calc-energy → ED/plateau; aging 100 cyc → SEI; 4C charge 45°C lumped+plating → T_max/plating) and Chen2020 reference (1C + calc-energy → ceiling proof for plateau). Identifies which of the 5 criteria bind and by how much.
- **R2 — architecture variants (ED push):** positive/negative thickness up (~1.5–2.2×), porosity down (~0.25), thin separator (~8–10 µm) & thin current collectors (~8/6 µm), anode particle size down (plating resistance). Each: 1C + calc-energy; best → aging + 4C safety.
- **R3 — electrolyte + thermal (safety pass):** if 4C fails: electrolyte σ/t⁺/D overrides (high-conductivity, high-t⁺ formulation) + cooling h (thermal management DOF) on best architecture; re-run 4C safety + 1C + calc + aging.
- **R4 — DFN precision** on finalists (1C discharge DFN + calc-energy; 4C safety DFN if needed).
- **R5+ — fallback:** three-strike questioning → plan update (e.g., SEI kinetic coating, electrode composition) only if forced.

## 4. Budget allocation (flash)

- R1: 4 sims + 2 calc-energy (all SPMe-seconds). R2: 4–6 sims + calc. R3: 3–5 sims. R4: 2–4 DFN. Target ≤ 5 rounds; closing deliverables + render + verify.

## 5. Risk & fallback plan

| Risk | Signal | Fallback route |
|---|---|---|
| M1 (950 Wh/L) unreachable at acceptable polarization | calc-energy < 950 on thickest sane variant | quantify ceiling; if architecture space exhausted → escalation: electrolyte formulation (transport) or electrode composition (run-comp) — Stage 2 |
| M2 (plateau 4.1 V) breached by thickening (polarization) | midpoint < 4.1 on thick variants | reduce thickness/polarization (thinner electrode, high-σ electrolyte) — Stage 3 |
| M4/M5 (plating / T_max) fail at 4C | plated=true or T_max > 323.15 | high-t⁺/σ electrolyte + cooling h + small anode particles — Stage 3; if model/system boundary suspected → three-strike questioning |
| M3 (SEI 500 nm) | sei_thickness_nm_end > 500 | SEI kinetics coating (SEI kinetic rate constant bridge, coating candidate at Stage 2) or additive funnel |
| Protocol-scale note | nominal 4.5 Ah vs model single-layer capacity — 4C = fixed 18 A | measure; if 4C unphysical for all candidates, record honestly and question boundary at three-strike |

## 6. References (domain basis, no fabrication)

- High-voltage spinel LNMO (4.7 V) cathode for 4.1 V+ plateau & energy density → LNMO parameter set docstring in this skill (`scripts/bda/simulators/data/LNMO.json` + `lnmo_parameters.py`, citing Markovsky et al./Duncan et al. LNMO OCP curves; theoretical capacity 147 mAh/g, density 4.4 g/cm³).
- NMC811/graphite baseline midpoint 3.61 V vs LNMO 4.17 V → skill anchor table (measured with this toolchain).
- SEI growth model (ec-reaction-limited) & Chen2020 100-cycle SEI magnitude ~449 nm (kinetics ×0.1 → 385 nm) → skill signal-scale reference (measured, Chen2020 set).
- 4C plating criterion: negative surface potential < 0 V → plating → skill protocol (OKane2022 plating parameterization, constant approximation in runner).
- Thick-electrode ED vs rate trade-off, small particle → plating resistance → domain experience (no precise source); smartphone cell energy density ~700–770 Wh/L cell-level → domain experience (no precise source).

## 7. Anti-pattern guard

- No fabricated values; all judgments from tool outputs via `bda log-evaluate`.
- No threshold relaxation; negative results reported honestly with three-strike questioning records.
- Real compute (run-orca/run-md) NOT executed — `real_compute: false` (default, no user request).

---

## Revision History

### Rev 2 (2026-08-25) — DFN thermal redesign (plan update 2)
DFN verification of the final design showed the lumped-SPM thermal under-predicted the 4C peak by 4.3 K (326.1 vs 321.9 K at h=120). DFN h-sweep: h=200 fail (323.8), h=250 pass (323.1, margin 0.10), h=300 pass (322.5, margin 0.65). Final thermal spec: h = 300 W/m²K (vapor chamber + graphite + Al frame). DFN confirmed M4 plated (−0.019 V) with a real 6.68 Ah charge; DFN aging capped at 1 cycle (27.4 nm, consistent with SPM √t scaling).

### Rev 1 (2026-08-25) — Three-strike M4 questioning conclusion (plan update 1)
Rounds 3–5 (15+ configurations) share one root cause: at the 4.7 V charge cutoff the anode potential is pinned by the cathode side — LNMO OCP ceiling (4.706 V) ≈ cutoff (4.7 V), so ap = U_pos+η_pos−4.7−φ_e(sep) ≈ −0.2 V for every real charge; anode-side levers cancel by construction; φ_e(sep) ≈ +0.2 V would need σ ≳ 100 S/m to overcome. M4 declared a protocol-level feasibility boundary. Final design = finN-2e19 (L_neg 120 µm, ε_neg 0.65, σ 20, t⁺ 0.9, D 1e-9, r_pos 2.0 µm, r_neg 3 µm, D_ec 2e-19, h 120→300): M1 1172 Wh/L ✓, M2 4.25 V ✓, M3 292 nm ✓, M5 ✓ (DFN 322.5 K @h300), M4 ✗ (documented).
