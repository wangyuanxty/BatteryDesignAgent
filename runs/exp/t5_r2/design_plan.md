# Design Plan — t5_r2: Next-Generation Flagship Vehicle Battery

**Case**: VBF-T5-R2 | **Task**: energy density ≥ 500.94 Wh/kg, 4C fast charge without
lithium plating, maximum temperature ≤ 60 °C (T_max_K ≤ 333.15 K).
**Headless zero-interaction run** — all parameters parsed from task text; undeclared
parameters take protocol defaults (recorded in log.jsonl entry 0).

## 1. Objective decomposition (decision layers)

| Layer | Metric | Threshold | Note |
|---|---|---|---|
| stage2 (cell) | energy_density_wh_kg | ≥ 500.94 | contract caliber (calc-energy): 1C discharge energy ÷ electrode+collector+separator mass, electrolyte excluded |
| stage3 (safety) | plated | false | mechanical: anode_potential_v min < 0 V during 4C_charge_45C ⇒ plated |
| stage3 (safety) | T_max_K | ≤ 333.15 | ≤ 15 K rise over the 318.15 K fast-charge starting temperature |
| stage1 (molecular) | max_energy_ev / max_homo_ev | 0.0 eV / −6.0 eV | funnel elimination lines (active only if molecular candidates enter the funnel) |

**Trade-off expectations (Pareto structure):**
- ED ↔ 4C plating: thicker/denser electrodes raise ED but degrade transport and
  anode lithiation margins → plating.
- ED ↔ T_max: ed mass cuts (thin collectors/separator) raise ED but raise per-mass
  heat flux under 4C.
- Voltage lever (system switch): raises ED at constant transport burden — the
  cleanest lever if a higher-voltage system is available.
- Electrolyte transport (σ, t⁺, D) reduces ohmic/concentration overpotential →
  directly attacks both plating and T_max without touching ED.
- Cooling (h) attacks T_max only (contract-honest thermal design lever).

## 2. Candidate strategy

1. **Round 1 — baseline characterization (Stage 3, Chen2020 default).**
   `1C_discharge` → `calc-energy` → `4C_charge_45C (lumped, plating)`. Fixes
   measured baseline ED / plating / T_max and executes the opening ceiling
   assessment.
2. **Opening ceiling assessment (Chen2020)** — evaluate best-possible
   architecture+formulation of the existing system (thin collectors, thin
   separator, tuned porosity/thickness, high-σ electrolyte) against the
   500.94 target. Measured via calc-energy on an aggressive ceiling variant,
   not by hand. Expectation: NMC811/graphite architecture space alone cannot
   close the gap (cathode-specific-energy bound) → **escalate to Stage 2
   system design** (ceiling_escalation, ON).
3. **Round 2 — system candidates (Stage 2 propose, direct Stage 3 screening):**
   - LNMO high-voltage spinel (skill library `LNMO.json`, 4.7 V class) — voltage lever;
   - keep Chen2020 NMC811/graphite as the reference arm;
   - note honestly: OKane2022 build 26.7.1.0 parameter dump shows graphite negative
     (OCP graphite_LGM50, max conc 33133 mol/m³) — the anchor-table "SiOx" discriminant
     is not present in this PyBaMM build, so OKane2022 is not an ED lever here (it is a
     degradation-model-rich NMC811/graphite set).
4. **Rounds 3+ — architecture × electrolyte × thermal tuning on the surviving
   system** (exploration_force: 2–4 variants/round, one at a time, mechanically
   evaluated): electrode thickness scaling for ED; thin collectors/separator;
   porosity; negative particle size & negative thickness (N/P) for plating
   margin; electrolyte transport overrides (σ/t⁺/D — literature-anchored
   estimates, marked `estimate`); cooling h for the 15 K budget.
5. **Safety fine-tune:** 4C_charge_45C must pass plating + T_max on the same
   final architecture that carries the ED.

## 3. Budget allocation

- R1 baseline + ceiling: 1 round (3 simulations + 1 evaluate).
- System screening: 1–2 rounds.
- Architecture/electrolyte/thermal tuning: up to ~8 rounds, 2–4 variants each.
- Safety fine-tune: up to ~3 rounds.
- Closing endorsements + deliverables after achievement (or honest negative
  `final` on budget exhaustion). No fixed round cap; three-strike rule applies
  per failure cause.

## 4. Risk and fallback plan

- **ED unreachable in a system's architecture space** → symptom = capacity/
  mass bound ⇒ material/system scale ⇒ escalate to Stage 2 (already planned).
- **4C plating persists after architecture tuning** ⇒ transport-scale cause ⇒
  electrolyte formulation (σ/t⁺/D) + N/P + particle size; last step within
  boundary: anode thickness. Three strikes ⇒ question the boundary (see §5).
- **T_max misses the 333.15 K line** ⇒ stage-3 thermal lever: cooling h
  (liquid-cooling class, 25–200 W/m²K), plus reduced ohmic heat via σ.
- **LNMO system insufficient** (possible low effective capacity per mass at
  default geometry) ⇒ thickness re-scaling; if still failing, fall back to the
  best NMC811/graphite arm and maximize overhead reduction honestly.
- **Overall unreachable within protocol levers** ⇒ three-strike questioning,
  then honest negative result with quantified "reachable if … relaxed" report.
  No threshold relaxation, no definition changes.

## 5. Three-strike questioning checklist (invoked only on repeated same-cause failure)

1. Model/system assumption: is the target physically reachable by the chosen
   system under a 1C/4C dual protocol within this library's parameter sets?
2. Task-boundary assumption: are the five freedoms (electrode system /
   electrolyte / modification / architecture / thermal) correctly wide? Any
   lever wrongly assumed locked would be questioned here (record: all five
   recorded adjustable in entry 0 — widest interpretation).
3. Metric assumption: is ≥500.94 Wh/kg + 4C no-plating + ≤333.15 K jointly
   reachable? If not, close as a negative result and state the nearest
   feasible relaxation quantitatively (never silently relax).

## 6. References (domain basis)

- NMC811/graphite LGM50 multiscale parameterization (baseline set) →
  Chen et al., J. Electrochem. Soc. 167, 080534 (2020).
- Alloy (Si-class) anode capacity/volume behavior →
  Obrovac & Chevrier, Chem. Rev. 114, 11444 (2014).
- High-voltage LNMO spinel cathodes →
  Manthiram, Chemelewski & Lee, Energy Environ. Sci. 7, 1339 (2014).
- High-Li⁺-transference electrolyte strategies (t⁺ lever) →
  Diederichsen, McShane & McCloskey, ACS Energy Lett. 2, 2563 (2017).
- EC/EMC LiPF₆ transport properties (σ(T)) →
  Nyman, Behm & Lindbergh, Electrochim. Acta 53, 6356 (2008).
- Lithium plating at fast charge (failure signature, anode potential) →
  Waldmann, Hogg & Wohlfahrt-Mehrens, J. Power Sources 384, 107 (2018).
- Liquid-cooling heat-transfer coefficients for automotive packs →
  domain experience (no precise source; h range 25–200 W/m²K).

## Revision history

- v1 (initial plan, written before round 1).