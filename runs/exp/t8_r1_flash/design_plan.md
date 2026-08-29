# Design Plan — VBF Case t8_r1_flash

**Task**: Design a battery for a long-endurance drone.
**Contract thresholds** (verbatim, entry 0):
- Gravimetric energy density ≥ **446.18 Wh/kg** (cell-level, calc-energy contract formula)
- 5C discharge capacity retention ≥ **90%** (5C cap ÷ 1C cap, same params, DFN)
- Cell mass ≤ **40 g** (calc-energy layer-stack mass; electrolyte excluded — honest note)
- Safety exam (protocol standard): 4C charge @45°C, lumped thermal, plating check — T_max ≤ 333.15 K, no plating

## 1. Objective decomposition

| Metric | Threshold | Direction of difficulty |
|---|---|---|
| energy_density_wh_kg | ≥ 446.18 | Chemistry + architecture lever: need high-V and/or high-capacity chemistry AND aggressive inactive-mass dilution |
| capacity_retention_5c | ≥ 0.90 | Rate lever: needs thin electrodes / high transport / small particles. **Directly opposite to ED lever (thick electrodes)** |
| mass_kg | ≤ 0.04 | Stack mass cap: E ≤ 0.04 × 446.18 ≈ 17.8 Wh → moderate cell (≈3.5–4.5 Ah depending on V_avg) |
| T_max_K / plated | ≤ 333.15 / false | Safety; 4C charge at 45°C ambient (318.15 K) leaves only ~15 K budget |

**Expected trade-off**: ED vs 5C retention (electrode thickness); ED vs T_max (thickness & areal loading raise heat). Balance zone must be found by scanning thickness/porosity with thin inactives.

## 2. Candidate strategy (initial)

- **R0 — baseline & ceiling (Chen2020)**: 1C (DFN) + 5C (DFN) + calc-energy. Establish current ED (~250 Wh/kg), mass, 5C retention; opening ceiling assessment: estimate best-possible ED of NMC811/graphite under thin collectors/sep/low porosity/thick electrodes.
  - *Directional estimate (domain):* NMC811 usable ~0.76 Li → ~200+ mAh/g @3.75 V ≈ 0.75–0.78 Wh/g(cathode); graphite 360 mAh/g; ultra-thin inactives (8/5 µm collectors, 9–12 µm separator) + thick electrodes dilute inactives → stack ED ~440–470 Wh/kg reachable **in principle**. 5C retention with such thick electrodes will be the binding constraint.
- **R1 — architecture variants on Chen2020** (2–3 candidates, one round):
  - A "High-ED": thick electrodes + thin inactives → probe ED ceiling & 5C failure.
  - B "Rate-ED balanced": moderate thickness + thin inactives + electrolyte transport boost (σ, t⁺) → probe the ED×5C Pareto.
  - C "Thin-fast": thin electrodes, high σ — check 5C near-pass and ED gap (quantifies trade-off).
- **R2 — refine winner** (thickness/porosity/N-P fine scan, maybe 1–2 variants).
- **R3 — safety + final**: 4C charge @45°C (lumped + plating) on the best cell; if T_max/plating fails → architecture/thermal fallback (still at Stage 3/4 scale).
- **Fallback/escalation**: if ED ceiling < 446 with NMC811/graphite after architecture scan → Stage 2 system escalation: LNMO 4.7 V high-voltage set (library LNMO.json), electrolyte formulation, or electrode composition (run-comp, constant-OCP self-built set) — in that order.
- **Molecular funnel**: only if additive/coating becomes the lever (e.g., SEI suppression not needed here; rate is transport-limited → electrolyte transport overrides preferred; marked as formulation candidates, no funnel).

## 3. Budget allocation (flash case, lean)

- R0 baseline: 3 sims (1C dfn, 5C dfn, calc-energy)
- R1 architecture: 3 candidates × (1C dfn + 5C dfn + calc-energy + retention derive) ≈ 10 sims
- R2 refine: 1–2 candidates × 4 ≈ 6 sims
- R3 safety: 1–2 candidates × (4C charge dfn) ≈ 2 sims + final
- Total ≈ 20–22 pybamm runs; no true DFT (real_compute=false, honest endorse skip)

## 4. Risk & fallback plan

| Risk | Probability | Mitigation |
|---|---|---|
| ED unreachable at 446 with NMC811/graphite (5C forces thin electrodes) | Medium-High | Escalate Stage 2: LNMO system switch; electrolyte transport; run-comp cathode invention |
| 5C retention < 90% on thick electrodes | High | Thin-electrode + high-σ/t⁺ electrolyte; small particle radius; accept Pareto trade-off and document |
| T_max > 333.15 K at 4C/45°C | Medium | Thermal lever locked at h=10 default; if fails → question boundary (record), report honestly |
| calc-energy mass > 40 g | Low | Area/thickness control; mass ∝ area — resize if needed |

**Three-strike escalation question plan**: (1) is NMC811/graphite physically able to hit 446 Wh/kg with 90% 5C retention within the allowed levers → if no, (2) question system-switch boundary → LNMO/high-V or Si anode direction → (3) if still no → honest negative result with "reachable if X relaxed" note.

## 5. References (direction → source; no fabrication)

- NMC811 usable capacity/OCP, graphite 360 mAh/g → Chen2020 PyBaMM parameter set (this skill's library), NMC811 literature ~200 mAh/g practical (domain knowledge; no precise single source)
- High-ED cell architecture (thin collectors 8/5 µm, thin separator ~9–12 µm, thick electrodes 4+ mAh/cm²) → commercial high-energy cell teardown literature direction (domain experience, no precise source)
- 5C retention vs electrode thickness/transport → electrolyte transport parameter literature (σ, t⁺ effects on rate capability — domain experience; no precise source)
- LNMO 4.7 V high-voltage spinel → this skill's library LNMO.json (4.7 V OCP set)
- SiOx anode capacity boost → OKane2022 parameter set (this skill's library)
