# Design Plan — t8_r1_noforce: Long-Endurance Drone Battery

Case: energy density ≥ 446.18 Wh/kg · 5C discharge with capacity retention ≥ 90% · cell mass ≤ 40 g.
Ablation: exploration_force OFF (free exploration — architecture variants proposed at relevant moments only).
start_stage = 3 (task names no new materials). Base system: Chen2020 (NMC811/graphite, anchor-table default — task names no electrode system).

## 1. Objective decomposition (decision thresholds)

| Metric | Threshold | Judge source | Priority / trade-off direction |
|---|---|---|---|
| energy_density_wh_kg | ≥ 446.18 | calc-energy (contract: electrolyte excluded) | Primary. ↑ with thicker electrodes, leaner inert stack, higher porosity (contract quirk: porosity reduces counted solid mass) |
| capacity_retention_5c | ≥ 0.90 | Q(5C,dfn)/Q(1C,dfn), same params, mechanical | Primary. ↓ with electrode thickness (diffusion); ↑ with smaller particles, higher porosity, faster electrolyte transport |
| mass_kg | ≤ 0.040 | calc-energy | Primary. Mass ∝ area (ED area-independent) → ED set by stack, mass set by area. Baseline ≈ 43.5 g (hand estimate) → lean-out required |
| plated | false | 4C charge 45 °C exam, anode_potential_v min<0 | Stage 3 gate (pipeline Stage 4) |
| T_max_K | ≤ 333.15 | 4C charge / 5C discharge, thermal lumped | Stage 3 gate, protocol default red line (60 °C) |

Key trade-off: **ED vs 5C retention** (thick vs fast). Lever set that helps both: porosity (↑ε → rate ↑ and contract-ED ↑), thin separator (mass ↓, transport path ↓), thin current collectors (mass ↓ only), small particle radius (rate ↑).

Expected Pareto direction: ED rises toward the chemistry ceiling as electrodes thicken and inert mass dilutes; 5C retention collapses past a diffusion-limited thickness. Target: the maximum thickness on the 90%-retention boundary, with maximally lean inert stack.

## 2. Candidate strategy

- **R1 — baseline characterization + opening ceiling assessment**: Chen2020 defaults; 1C discharge SPMe → DFN, 5C discharge DFN, calc-energy. Ceiling estimate: lean-stack limit (CC 8/8 µm, separator 10 µm, porosity ~0.40/0.30, particle radii ↓, thickness sweep) vs 446.18. Gap → escalate to Stage 2 system switch (below); no gap → stay in architecture space.
- **R2 — lean-stack variants** (exploration_force OFF: propose at relevant moments; R2 is one): thin CC (8 µm Al / 8 µm Cu), thinner separator (10 µm), raised porosity (0.40 pos / 0.30 neg), smaller particles (radius ~3 µm). One-lever-ish variants for clean attribution.
- **R3+ — combine winners, tune thickness on the ED×5C Pareto; mass via area**.
- **Escalation path (ceiling_escalation ON)**: if Chen2020 ceiling < 446.18 → system switch candidate `OKane2022` (NMC811/graphite+SiOx, cracking model; SiOx negative raises negative capacity → less anode mass/thickness → ED headroom). Anchor verification per §1.5 (negative active contains SiOx). Fallback direction: LNMO 4.7 V system (voltage lever) if SiOx rate-capped. System candidates skip the molecular funnel (direct Stage 3 simulation).
- **Finalist → Stage 4 safety exam**: 4C charge 45 °C, thermal lumped, plating enabled; 5C discharge with thermal lumped (extreme operating condition heating). Adjust via N/P, porosity, cooling h if needed.
- **Stage 5**: real_compute=false → endorse records honest skip; render; final.

## 3. Budget allocation

~8 rounds: R1 baseline+ceiling, R2 lean variants, R3-4 Pareto/refinement, R5 escalation if needed, R6 architecture re-tune on new system, R7 safety exam, R8 closing+deliverables. Trim when converged.

## 4. Risk and fallback plan

| Risk | Symptom → fallback |
|---|---|
| Chen2020 ED ceiling < 446.18 | Ceiling assessment evidence → escalate to OKane2022 (SiOx), then LNMO (voltage) |
| 5C retention < 0.90 at required thickness | particle radius ↓, porosity ↑, electrolyte σ/D/t⁺ overrides (formulation lever), thickness ↓ + leaner inert |
| Mass > 40 g | thinner CC/separator, then area scale-down (ED unaffected) |
| Plating on 4C charge exam | N/P adjustment (negative thickness/porosity); plating is a hard gate |
| T_max > 333.15 K | cooling h ↑ (thermal-management lever, adjustable) |
| Solver failures | record verbatim; DFN auto-degrades to SPMe; adjust protocol legality per bda error |

## 5. References (domain basis)

- SiOx/Si alloy anodes raise negative capacity → Obrovac & Chevrier, "Alloy Negative Electrodes for Li-Ion Batteries", Chem. Rev. 114, 2014.
- Thick electrodes raise energy density but diffusion-limit rate capability → Gallagher et al., "Optimizing Areal Capacities through Understanding the Limitations of Lithium-Ion Electrodes", J. Electrochem. Soc. 163, 2016.
- Smaller active particles shorten solid-state diffusion length → rate benefit: Newman & Thomas-Alyea, "Electrochemical Systems" (textbook), Chapter 22; domain experience.
- Electrolyte transport (σ, t⁺, D) limits high-rate performance → Nyman et al., Electrochim. Acta 53, 2008 (LiPF6-EC/EMC transport parameterization).
- LNMO spinel 4.7 V high-voltage cathode → Manthiram, Chemelewski & Lee, Energy Environ. Sci. 7, 2014.
- Commercial NMC811/graphite cell-level ED ~250–300 Wh/kg; contract formula (electrolyte excluded) reads higher than commercial cell-level ED → protocol definition (this skill, cli-commands.md calc-energy); domain experience (no precise source).
