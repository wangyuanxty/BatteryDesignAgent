# Stage 1 Design Plan — t4_r1 Extreme-Cold Battery

Case: VBF-T4_R1 (workspace `runs/exp/t4_r1`). Headless execution — zero-interaction rules apply.

## 1. Objective decomposition (entry-0 contract)

| # | Metric | Threshold | Decision layer | Expected difficulty |
|---|---|---|---|---|
| 1 | -20°C 1C discharge capacity retention | ≥ 95% (0.95 fraction) | stage2 (`lowT_retention`) | **Binding constraint** |
| 2 | Gravimetric energy density | ≥ 327.18 Wh/kg | stage2 (`energy_density_wh_kg`) | Moderate (contract formula baseline ≈ 410–420 Wh/kg, est.) |
| 3 | Volumetric energy density | ≥ 880 Wh/L | stage2 (`energy_density_wh_l`) | Borderline (baseline ≈ 860–900 Wh/L, est. — needs verification + likely thin separator/collector) |
| S | Safety exam (protocol default) | T_max ≤ 333.15 K (60°C) at 4C/45°C charge; no Li plating | stage3 | Low-moderate (1C-class design; 4C is beyond the mission profile) |

Trade-off map (expected):
- **lowT retention ↔ ED/VED**: thicker electrodes raise ED/VED but lengthen ionic/diffusion paths → worse cold polarization. Pareto front to be walked.
- **lowT retention ↔ cooling h**: low h (insulation) → stronger self-heating at −20°C → better cold retention; but higher T_max at 4C/45°C. Same parameter serves both exams — will measure both.
- **VED ↔ ED**: thinner separator/current collectors and lower porosity raise both (no trade-off); only electrode thickness trades them against retention.

## 2. Candidate strategy

- **Round 1 — baseline characterization + opening ceiling assessment**: Chen2020 (anchor-verified: pure-graphite negative, NMC811 positive, SEI-capable; dump recorded). Run 1C discharge 298.15 K (SPMe + DFN), lowT discharge 253.15 K, calc-energy (contract formula). Ceiling assessment: with maximum-transport electrolyte (flat κ/D_e, t⁺=0.6), thin electrodes, small particles, thin separator — is the objective reachable within this system? Written to funnel log.
- **Round 2 — electrolyte formulation candidates** (Stage-3-scale parameter bridge; no molecular funnel — transport values are formulation props, sources: literature/estimate, never masqueraded as simulation): candidate values κ ∈ {0.8, 1.1} S/m (flat, T-independent — models a low-T electrolyte keeping conductivity at cold; literature best-case κ(−20°C) ≈ 0.3–0.6 S/m for LiFSI/ester systems, so 0.8 is an optimistic design target marked estimate), D_e ∈ {2.58e-10} m²/s flat, t⁺ ∈ {0.5, 0.6} (LiFSI-class, literature ~0.45–0.65).
- **Round 3 — architecture variants**: thinner electrodes (pos 75.6→50 µm; neg 85.2→60 µm), smaller particles (pos 5.22→2.5 µm, neg 5.86→3 µm — rate capability ↑, surface area ↑, SEI baseline changes not judged here), thinner separator (12→8 µm) for VED, thin collectors (16/12→10/8 µm) for VED.
- **Direction routing**: retention gap traced to electrolyte transport → formulation props (same scale, fallback to Stage-3 parameter bridge); residual gap from charge-transfer kinetics (j0 T-dependence, not an allowed lever) → particle-size reduction (surface-area compensation) → if still short: three-strike questioning (system assumption: would OKane2022 SiOx change the outcome? boundary assumption: is a scalar κ override too idealized? metric assumption: reachability).
- **System switch**: only if baseline ED/VED is insufficient (anchor says default Chen2020; freedom allows switch) or three-strike questioning points there. OKane2022 (SiOx, 4.6 Ah-class) as fallback system candidate.

## 3. Budget allocation

| Phase | Rounds | Notes |
|---|---|---|
| Baseline + ceiling | 1 | R1 |
| Electrolyte formulation screen | 2 (R2–R3) | flat κ/D_e/t⁺ grid, each ≈ 3 runs (1C + lowT + calc-energy) |
| Architecture screen | 2–3 (R3–R5) | thickness/particle/separator/collector |
| Combined refinement | 2 (R6–R7) | best formulation × best architecture; DFN verification |
| Stage 4 safety | 1 (R8) | 4C_charge_45C lumped + plating on finalist(s) |
| Closing | — | endorse-skip (real_compute=false), render, deliverables |

## 4. Risk and fallback plan

1. **VED borderline at baseline** → thin separator/collectors (both raise VED; separator 12→8 µm is production-plausible, collectors 16/12→10/8 µm).
2. **lowT retention unattainable via κ/D_e/t⁺ + architecture** (residual CT-kinetics loss, j0 not an allowed lever) → particle-size reduction first; then three-strike questioning; honest negative result with "reachable if X relaxed to Y" quantification if truly unreachable.
3. **SPMe/DFN divergence at 253.15 K** → DFN for final judgment (protocol: SPMe screens, DFN certifies).
4. **Model idealizations must be labeled**: scalar κ override = T-independent electrolyte (optimistic vs real electrolytes); t⁺/κ literature values carry citations; every estimate marked `estimate`.
5. **No durability metric in task** → aging protocol not required; SEI levers not used (recorded in entry 0).

## 5. References (domain basis — all real)

- Nyman2008 electrolyte conductivity/diffusivity temperature dependence → Valøen, L.O., Reimers, J.N., "Transport Properties of LiPF6-Based Li-Ion Battery Electrolytes", J. Electrochem. Soc. 152 (2005) A882–A898.
- Chen2020 parameter set (NMC811/graphite teaching parameterization) → Chen, C.-H., Brosa Planella, F., O'Regan, K., Gastol, D., Widanage, W.D., Kendrick, E., "Development of Experimental Techniques and Parameter Identification of a Lithium-Ion Battery Model", J. Electrochem. Soc. 167 (2020) 080534.
- Low-T electrolyte conductivity retention with LiFSI/low-viscosity ester blends; high transference numbers of LiFSI → Xu, K., "Nonaqueous Liquid Electrolytes for Lithium-Based Rechargeable Batteries", Chem. Rev. 104 (2004) 4303–4417; specific κ(−20°C) ≈ 0.3–0.6 S/m values: domain experience (no precise source).
- Particle-size reduction shortens solid-diffusion time constant (τ ∝ R²/D) and raises exchange area → domain experience (no precise source).
- Cell self-heating under adiabatic/insulated conditions raises effective operating temperature at cold → domain experience (no precise source).
