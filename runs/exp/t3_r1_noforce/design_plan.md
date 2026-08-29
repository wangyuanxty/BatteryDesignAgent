# Design Plan — Power-Tool Battery Cell

**Case**: `exp/t3_r1_noforce` · **Date**: 2026-08-25 · **Mode**: headless zero-interaction execution
**Ablation**: `exploration_force = OFF` (no forced 2–4 architecture variants per round; propose variants at relevant moments, free exploration)

## 1. Objective decomposition (thresholds verbatim from task text)

| # | Metric | Threshold | Decision layer | Judged by |
|---|---|---|---|---|
| 1 | Nominal capacity | ≥ 2 Ah | stage2 | 1C discharge DFN `capacity_ah` |
| 2 | 5C discharge capacity retention | ≥ 95 % (5C cap ÷ same-params 1C cap, mechanical ratio) | stage2 | 5C discharge DFN + 1C DFN → `rate_retention_5c` |
| 3 | Power density | ≥ 4000 W/kg (V_OC²/(4·DCR)/mass, contract formula) | stage2 | calc-energy on 1C discharge `power_density_w_kg` |
| 4 | 4C fast charge without lithium plating | anode surface potential never < 0 V → `plated = false` | stage3 | 4C charge 45 °C DFN + plating module |
| 5 | Maximum temperature | ≤ 60 °C = 333.15 K | stage3 | T_max_K on 5C discharge (298.15 K amb.) and 4C charge (318.15 K amb.), worst case governs |

**Multi-objective trade-off expectations (marked at plan time):**
- **Energy density is NOT constrained** by the task → design freedom favors power: thin electrodes, thin current collectors, small particles are all admissible.
- **Capacity headroom**: baseline Chen2020 is a 5.0 Ah nominal cell (verified by parameter dump) vs the 2 Ah requirement → electrodes may be thinned by up to ~2.5× (capacity ∝ thickness×area) while meeting the target. Thinning simultaneously raises power density, lowers heat generation and improves rate capability — objectives are aligned along this direction.
- **T_max at 4C charge / 45 °C ambient is expected to be the binding constraint** (only 15 K margin above ambient). Mitigation levers, in order of preference: (a) lower heat generation via DCR reduction (thinner electrodes, small particles, high-σ electrolyte); (b) cooling design (raise `Total heat transfer coefficient`, thermal-management freedom, contract default h = 10 W/m²K).
- **5C retention and plating resistance share the same transport levers** (porosity, particle radius, electrolyte σ/t⁺, electrode thickness) — largely aligned objectives.
- **N/P trade-off**: raising N/P protects against plating but adds negative-electrode mass (power density ↓) — a mild, quantifiable trade-off to balance per round.

## 2. Starting point and degrees of freedom

- **start_stage = 3** (cell design): the task names no new materials/additives/electrode design → architecture/formulation case; materials use the system baseline (source marked `baseline`).
- **base_params = Chen2020** (NMC811/graphite + SEI teaching parameterization): task text names no electrode system → anchor-table default, recorded. Anchor verified by parameter dump: positive OCP `nmc_LGM50_ocp_Chen2020`, negative OCP `graphite_LGM50_ocp_Chen2020` (pure graphite, no SiOx), negative electrode density 1657 kg/m³, SEI kinetic rate constant present (aging-capable), nominal capacity 5.0 Ah, wound geometry (0.065 m × 1.58 m unrolled).
- **Degree-of-freedom boundary (five categories, widest interpretation — task text is silent on each, so all adjustable; recorded in entry 0 `meta.freedoms`):**

| Category | Status | Baseline default |
|---|---|---|
| Electrode system | adjustable | Chen2020 (system switch only if cell-level ceiling fails) |
| Electrolyte formulation | adjustable | Chen2020 σ/D/t⁺ (overrides via parameter bridge; literature/estimate values marked) |
| Electrode modification | adjustable | none (coating/doping only if a deficit demands it) |
| Cell architecture | adjustable | Chen2020 thickness/porosity/N-P/separator/CC/particle size |
| Thermal management | adjustable | h = 10 W/m²K (cooling design is a legitimate lever for the 60 °C constraint) |

## 3. Candidate strategy

- **Round 1 — baseline characterization (no overrides)**: 1C discharge (SPMe quick screen → DFN), 5C discharge DFN (lumped thermal), 4C charge 45 °C DFN (lumped thermal + plating), calc-energy on the 1C DFN. Establishes the gap to each of the 5 criteria and feeds the opening ceiling assessment.
- **Round 2+ — free exploration** (exploration_force OFF; variants proposed at relevant moments, typically 2–4 per round when several hypotheses compete):
  - Power-density deficit → thinner positive/negative electrodes + thinner current collectors (mass ↓, DCR ↓).
  - 5C-retention deficit → smaller particle radii, higher porosity, thinner electrodes, higher electrolyte σ.
  - Plating at 4C → higher N/P, smaller negative particles, higher negative porosity, higher σ/t⁺.
  - T_max deficit → raise cooling h into the forced-air class (≈20–30 W/m²K), lower DCR.
- **Per-round loop**: propose (struct-type candidates, rationale + parameter sources listed *before* running) → simulate → `log-evaluate` batch → diagnose → fallback to the scale where the cause lives (capacity/temperature rise → architecture/thermal; transport-limited plating → electrolyte formulation at cell scale).

## 4. Budget allocation

| Phase | Rounds |
|---|---|
| Baseline characterization + ceiling assessment | 1 |
| Architecture / formulation exploration | 3–6 |
| Safety fine-tuning (4C plating + T_max) | 1–2 |
| Closing (endorse/final/render/deliverables) | 1 |
| **Total expected** | **6–10** (no hard cap: iterate until achieved or budget exhausted) |

## 5. Risk and fallback plan

- **R1 — T_max unreachable with h = 10**: expected binding risk (15 K margin at 45 °C ambient). Fallback: cooling-h escalation within the declared thermal-management freedom; evidence package records value vs 333.15 K per round.
- **R2 — plating not cleared at 4C**: mitigation chain negative particle radius → negative porosity → N/P → σ/t⁺. Only after three strikes on the same cause does the three-strike rule trigger layer-by-layer questioning (system assumption / task boundary / metric reachability); a system switch (e.g., LFP via Prada2013) is a direction change of last resort, not a blind retry.
- **R3 — 5C retention ≥ 95 % physically demanding**: mitigation chain particle radius → porosity → electrode thinning → electrolyte formulation. If exhausted → honest negative-result close with a "reachable if retention relaxed to X" statement (never relax the registered threshold silently).
- **R4 — power density ≥ 4000 W/kg**: thin electrodes + thin CCs + small particles; ceiling quantified after baseline.
- **Failure evidence packages**: every failed metric is recorded per evaluate entry (metric, value vs threshold, output file), enabling informed (not blind) reruns.
- **Pre-closing self-check** (7 failure modes): simulation failure ≠ achievement; no hallucinated values; no shortcut dependence; no bug-as-discovery; no threshold relaxation; unit correctness (K not °C); no early lock-in.

## 6. References (directional basis; real sources only)

- System baseline / SEI parameterization: Chen, C.-H., Brosa Planella, F., O'Regan, K., Gastol, D., Widanage, W. D., Kendrick, E., "Development of Experimental Techniques and Parameterization of a Physically Based Battery Model", *J. Electrochem. Soc.* 167, 080534 (2020) — the Chen2020 parameter set shipped with PyBaMM.
- High-rate NMC811/graphite power-cell design practice (thin electrodes, small particles, high-conductivity electrolyte for 5C-class cells) — domain experience (no precise source).
- Fast-charge plating criterion (negative surface potential < 0 V vs Li/Li⁺ during charge) — standard porous-electrode electrochemistry criterion (Newman-class modeling literature) — domain experience (no precise source).
- Cooling-coefficient engineering ranges (natural convection ≈ 10, forced air ≈ 20–50 W/m²K) — standard heat-transfer practice — domain experience (no precise source).
- Simulation-library definitions: this skill's `references/cli-commands.md` and `SKILL.md` (protocols, contract formulas, error handling).

## 7. Plan revision history

- 2026-08-25 — initial plan written (Stage 1, zero simulation budget).
- 2026-08-25 — **plan update after round 3** (update entry appended to log.jsonl): (1) N/P 1.3 direction overturned — retention regressed 0.951 → 0.736 because the thick anode lets the cathode reach its deep low-x region at 1C (inflated denominator) while 5C capacity stayed flat ~2.65 Ah; new direction: rebalance N/P to ~1.15–1.2 (negative 60 µm) so the anode limits the 1C denominator again, plus raise cathode 5C accessibility (pos r_p 1.2 µm, τ = 360 s). (2) C-rate rating corrected — probe (cell/probe_nominal_1c_dfn.json) verified the protocol C-rate current follows the `Nominal cell capacity [A.h]` parameter (1C discharge 3638.7 s at 3.6 A vs 2609.6 s at 5 A under nominal 5.0); rounds 1–3 had therefore tested the 2.8–3.6 Ah designs at effective 6.7–8.6C. From round 4 on, the cell is rated at its designed capacity so 5C/4C protocols use the cell's own C-rates (rating is a design output, not an excluded parameter). Plating fix pivots from N/P to anode interface uniformity: neg r_p 2.0 µm, neg porosity 0.42, separator 9 µm / porosity 0.55, t⁺ 0.5, plus h 45 for the 4C T_max margin.
