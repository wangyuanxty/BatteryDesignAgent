# t1_r3 — Design Plan (Stage 1)

Next-generation pure electric sedan battery:
- **ED ≥ 392.61 Wh/kg** (contract caliber: `bda calc-energy`, electrolyte excluded)
- **4C fast charge, no lithium plating** (`plated == false` from 4C_charge_45C anode potential)
- **T_max ≤ 60 °C (333.15 K)** on all cell-thermal scenarios (4C charge + overcharge)
- **Overcharge to 4.7 V without thermal runaway** (`run-tr.triggered == false`; 4.7 V = NMC811 4.2 V cut-off + 0.5 V, verbatim)

Zero-interaction execution: no user available; thresholds parsed from task text verbatim (entry 0);
all five degree-of-freedom categories take the widest interpretation (entry 0 `meta.freedoms`).

## 1. Objective decomposition and trade-off expectations

| Metric | Decision layer | Threshold | Mechanism levers | Trade-off direction |
|---|---|---|---|---|
| energy_density_wh_kg | stage2 | ≥ 392.61 | CC thickness, separator, porosity, electrode thickness, system switch | ED ↑ ↔ 4C plating ↓ (thick electrodes), ED ↑ ↔ T_max ↑ (thermal mass/heat concentration) |
| plated | stage3 | false | thickness, particle size, N/P, electrolyte σ/t⁺, system (SiOx) | plating-safe ↔ ED (thin = less active mass) |
| T_max_K | stage3 | ≤ 333.15 | cooling h, electrode thickness, porosity, DCR | cooling h is ~free in this virtual world (liquid cooling, sedan standard) |
| triggered | stage3 | false | SEI stability / thermal response of chemistry on overcharge | fixed by chemistry choice; mechanical `run-tr` judgment |

Contract-mass estimate for Chen2020 (from `bridge/base_dump.json`): pos 0.1640 + neg 0.1059 + CCs 0.1507 +
sep 0.0025 ≈ 0.4231 kg/m² → ≈ 43.5 g; energy ≈ 18 Wh → **ED ≈ 415–420 Wh/kg at baseline (estimate)**.
Mass-side headroom (thin Cu/Al CC, thin separator, higher porosity) ≈ −0.10 kg/m² → ED ceiling ≈ 540+ Wh/kg.
**Expected bottleneck: 4C plating, then T_max; ED is expected to be satisfiable even after electrode thinning.**

## 2. Candidate strategy

- **R1 — baseline characterization** (Chen2020, the deterministic default: task names no electrode system):
  1C discharge (SPMe→DFN), `calc-energy`, 4C charge 45 °C (DFN, lumped, plating), overcharge (DFN, lumped)
  + `run-tr` coupling → full mechanical picture + opening ceiling assessment.
- **R2–R5 — architecture/transport/thermal exploration** (2–4 variants per round, `exploration_force` ON):
  - plating: negative particle radius ↓, electrode thinning (both), N/P ↑, electrolyte σ ↑ / t⁺ ↑ (bridge table),
    OKane2022 (SiOx negative, native plating parameters) as system switch if architecture space saturates;
  - ED: Cu CC 12→6–8 μm, Al CC 16→10 μm, separator 12→9 μm, porosity ↑ (pos 0.335→0.40, neg 0.25→0.33);
  - T_max: `Total heat transfer coefficient` 10→50–100 W/m²K (liquid cooling; next-gen sedan standard).
- **R6–R8 — safety pass on finalists**: overcharge (DFN) + `run-tr --mass-kg` mechanical judgment; iterate on
  thermal/chemistry if triggered; then closing (endorse skip with `real_compute=false`, `final`, `render`, deliverables).

## 3. Budget allocation

| Rounds | Purpose |
|---|---|
| 1 | Baseline + ceiling assessment (all four protocols) |
| 2–5 | Fast-charge/ED architecture exploration (≈3 candidates/round) |
| 6–8 | Overcharge/TR safety pass + finalist confirmation |
| 9 | Closing: endorse/final/render/deliverables/verify-deliverables |

## 4. Risk and fallback plan

- **4C plating persists after 3 architecture rounds** (same cause): question assumptions →
  escalate to electrolyte formulation (σ/t⁺ override, literature-basis) → OKane2022 SiOx system switch →
  if still failing, three-strike questioning (system / task-boundary / metric) recorded in `final.escalation`.
- **ED drops below 392.61 after thinning**: restore ED via CC/separator/porosity mass levers (energy-neutral),
  then electrode-thickness re-tune on the ED↔plating Pareto front.
- **Overcharge T_max > 333.15 K or triggered**: raise h on the overcharge scenario, reduce overcharge
  polarization (σ ↑, porosity ↑); if `run-tr.triggered` persists for the chemistry → record honest negative
  on the safety axis or switch system (LNMO: note its overcharge protocol target shifts to 5.2 V — a deviation
  from the verbatim 4.7 V contract, recorded honestly if used).
- **Numerics**: DFN solver failure → auto SPMe fallback (runner handles); parameter-name typos rejected by
  `unknown parameter name(s)` validation.

## 5. References (direction → source)

- Plating onset criterion = negative electrode potential < 0 V vs Li/Li⁺ → Waldmann, Hogg & Wohlfahrt-Mehrens, *J. Power Sources* 384 (2018) 107–124.
- Extreme fast charging without plating requires electrode/particle/electrolyte co-design → Colclasure et al., *J. Electrochem. Soc.* 167 (2020) 120550; Liu et al., *Nature Energy* 4 (2019) 540–550.
- Areal-capacity vs rate capability trade-off → Gallagher et al., *J. Electrochem. Soc.* 163 (2016) A138.
- Overcharge → thermal runaway mechanism chain (SEI decomposition → anode–electrolyte → cathode–electrolyte) → Feng et al., *Energy Storage Mater.* 10 (2018) 246–267; Ren et al., *J. Power Sources* 364 (2017) 328–340.
- SiOx anode raises capacity and anode potential (plating margin) → Feng et al., *Small* 14 (2018) 1702737.
- Liquid-cooling heat-transfer coefficients for EV packs → Rao & Wang, *Renew. Sustain. Energy Rev.* 34 (2014) 311–324.
- Parameter-set anchors → Chen et al., *J. Electrochem. Soc.* 167 (2020) 080534 (Chen2020); O'Kane et al., *Phys. Chem. Chem. Phys.* 24 (2022) 7909–7922 (OKane2022).
- Electrolyte transport basis → Xu, *Chem. Rev.* 104 (2004) 4303–4418 (σ/t⁺ ranges for carbonate + LiPF₆).

## 6. Revision history

- 2026-08-26 — initial plan (R1 baseline + exploration + safety + closing).
