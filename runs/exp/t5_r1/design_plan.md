# Stage 1 — Overall Design Plan (t5_r1)

Case: next-generation flagship vehicle battery.
Contract (log.jsonl entry 0, verbatim from task text):
- stage2: energy density ≥ 500.94 Wh/kg (contract-caliber `calc-energy` formula, electrolyte excluded by definition)
- stage3: 4C fast charge without lithium plating (`plated = false`), maximum temperature ≤ 60 °C (= 333.15 K, mechanical conversion)
- meta: headless zero-interaction execution; `start_stage: 3`; default base Chen2020 (task names no electrode system — anchor-table default, recorded); `real_compute: false`; all five degree-of-freedom categories adjustable (widest interpretation, recorded in entry 0 `meta.freedoms`).

## 1. Objective decomposition and trade-off expectations

- **ED ≥ 500.94 Wh/kg** (stage2, one metric). Mass basis (per `calc-energy`): positive/negative active layers + both current collectors + separator; electrolyte excluded. Baseline geometry (Chen2020, dumped from the parameter set): pos 75.6 µm/ε0.335/3262 kg/m³, neg 85.2 µm/ε0.25/1657 kg/m³, Al 16 µm, Cu 12 µm, sep 12 µm, area 0.1027 m² → ≈ 0.423 kg/m². Dominant mass terms: Cu collector 0.1075 kg/m² (25%), pos electrode 0.1640 (39%), neg 0.1059 (25%), Al 0.0432 (10%).
  - **Expected Pareto direction: ED ↑ when collector/separator mass is diluted (thin foils, thicker electrodes) — but thicker electrodes raise 4C polarization → plating and heat.** Thin collectors (Cu 6 µm, Al 8 µm — production-realistic flagship values) are a nearly free ED win with no electrochemical penalty (outside the ionic path).
  - Second lever: low porosity gains active mass but throttles ionic transport at 4C — use sparingly.
- **4C charge without plating** (stage3). 4C = 20 A on a 5 Ah nominal cell. Plating risk is anode-transport limited: mitigation levers are small particle radii (5.22→~2.5 µm pos, 5.86→~3 µm neg — surface-area driven, **no mass-formula penalty**), high electrolyte conductivity (parameter bridge, formulation override), moderate electrode thickness, adequate N/P. Judgment is mechanical: `anode_potential_v` series min < 0 V → `plated = true` (auto-derived by `log-evaluate`).
- **T_max ≤ 333.15 K at 4C/45 °C ambient** (stage3) → ΔT budget only 15 K on a 20 A charge. Lever: total heat transfer coefficient h (thermal-management freedom; contract default 10 W/m²K, liquid-cooling-grade values 25–50 W/m²K are vehicle-relevant). Reduces heat generation: thin electrodes, high-σ electrolyte, small particles.
- **Multi-objective tension**: ED wants thick/low-porosity electrodes; 4C+T_max want the opposite. Expected solution region: thin foils + mild thickness increase (≤ +25%) + porosity ≤ baseline + small particles + boosted electrolyte + enhanced h. All quantitative claims to be confirmed by simulation, not assumed.

## 2. Candidate strategy

- **R1 — baseline characterization (Chen2020, the recorded default)**: 1C discharge (SPMe quick-screen → DFN precision), `calc-energy`, 4C charge 45 °C (lumped thermal + plating). Purpose: measure baseline ED, plating, T_max; verify magnitude of each term. Also execute the **opening ceiling assessment**: bound the best-case ED of this system under thin foils/thick electrodes/low porosity vs 500.94 → decide escalation vs architecture work. Expected from mass-basis arithmetic: baseline ED ≈ 400–420, ceiling ≈ 510–540 with architecture alone → **no material bottleneck expected; the gap is architectural + formulation + thermal**.
- **R2 — system candidate OKane2022** (NMC811/graphite-SiOx incl. cracking model; same electrochemical+mass basis as Chen2020, verified by parameter-set diff: OKane2022 ⊇ Chen2020, no geometry/density differences). Motivation: Chen2020 has no native plating parameters (runner injects standard defaults); OKane2022 carries native plating physics. 1C DFN + 4C safety on OKane2022 = plating-judgment cross-check. ED basis identical → not an ED lever. If both agree, continue on Chen2020 (anchor default); if they disagree, final design must pass 4C under **both** (conservative dual judgment, recorded honestly).
- **R3 — "ED push" architecture variants** (2–4 per round): thin collectors (Al 8 µm / Cu 6 µm) + electrode thickness ×1.15–1.25 + porosity pos 0.30 / neg 0.22 + separator 10 µm. Simulate one-by-one; evaluate vs stage2 AND stage3 (both must hold — ED-only variants that plate are rejected by the loop).
- **R4 — "4C mitigation" variants**: particle radii reduction (pos 2.5 µm / neg 3 µm), electrolyte conductivity boost (parameter bridge; literature-anchored values for concentrated/optimized liquid electrolytes, marked `literature`/`estimate`), N/P adjustment if plating persists.
- **R5 — thermal**: raise h (20–40 W/m²K) if T_max > 333.15 K while ED passes.
- **R6 — final confirmation**: DFN precision runs of the winning candidate + `calc-energy` + 4C safety; mechanical `log-evaluate`; closing.
- Escalation path (only if measurement contradicts R1 ceiling assessment): if ED ceiling in architecture space is truly < 500.94 → Stage 2 material design (system candidates with higher voltage/capacity basis — checked options: ORegan2022 4.4 V LGM50 has higher electrode densities and likely net-lower ED; LNMO 4.7 V has low areal capacity → worse under contract formula; conclusion to be re-verified by simulation if needed).

## 3. Budget allocation

~6–8 simulation rounds, each cheap (SPMe seconds, DFN ~1 min, calc-energy instant). R1–R2 characterization, R3–R5 optimization (2–4 variants/round), R6 confirmation. Reserve: +2 rounds for unexpected fallback. No true DFT/MD (real_compute=false — endorsement skipped honestly at closing).

## 4. Risk and fallback plan

- **R1**: 4C plating and/or T_max fail at baseline → expected (that is the design problem); fallback direction: formulation + particle + thermal levers at Stage 3 (same scale — architecture/parameter cause).
- **R2**: OKane2022 disagrees with Chen2020 on plating → dual-system conservative judgment.
- **R3**: ED stalls below 500.94 → cause localization: if capacity/voltage-limited (system basis) → escalate Stage 2 (system candidate re-check incl. ORegan2022/LNMO measurement, not assumption); if mass-limited → further collector/porosity/thickness optimization.
- **R4/R5**: plating persists after particle+electrolyte+N/P levers → re-examine charge depth (voltage window is usage, not design — excluded), then **three-strike questioning** per protocol (system assumption / boundary assumption / metric assumption) with layer-by-layer record; close as honest negative result with "reachable if X relaxed" only if questioning concludes unreachable.
- **Guard**: never thin collectors below process-realistic values (≥ 6 µm Cu, ≥ 8 µm Al) without noting manufacturability caveat; every conclusion-grade number from tool output only.

## 5. References (direction → source)

- Chen2020 parameter set (NMC811/graphite teaching parameterization) → Chen, Bazant et al., "Development of Experimental Techniques and Parameterization of a Physically Based Battery Model", J. Electrochem. Soc. 167, 080534 (2020). [tool source: `pybamm.ParameterValues("Chen2020")`, dumped this case]
- OKane2022 parameter set (NMC811/Gr-SiOx, cracking/plating physics) → O'Kane et al., "Physical Origin of the Differential Voltage Minimum at the 50% State of Charge of NMC811/graphite-SiOx cells", J. Electrochem. Soc. 169, 070529 (2022). [tool source, dumped this case]
- Extreme fast charging vs plating → Colclasure et al., "Requirements for Enabling Extreme Fast Charging of High Energy Density Li-Ion Cells while Avoiding Lithium Plating", J. Electrochem. Soc. 166, A1412 (2019).
- Fast-charge materials/design review → Weiss et al., "Fast Charging of Lithium-Ion Batteries: A Review of Materials Aspects", Adv. Energy Mater. 11, 2101126 (2021).
- Fast-charge gap assessment (electrode design levers) → Ahmed et al., "Enabling fast charging – A battery technology gap assessment", J. Power Sources 367, 250 (2017).
- Electrolyte transport properties (conductivity/diffusivity magnitudes for formulation override) → Valøen & Reimers, "Transport Properties of LiPF6-Based Li-Ion Battery Electrolytes", J. Electrochem. Soc. 152, A882 (2005).
- SiOx anode capacity/energy direction → Obrovac & Chevrier, "Alloy Negative Electrodes for Li-Ion Batteries", Chem. Rev. 114, 11444 (2014).
- Thin current collector foil practice (Cu 6 µm / Al 8–10 µm in high-ED automotive cells) → domain experience (no precise source); no fabricated citation.
- Liquid-cooling heat transfer coefficients (25–50 W/m²K class) → domain experience (no precise source).

## Revision history

- 2026-08-25 initial plan.
- 2026-08-25 plan update (three-strike, R6→R7): R4–R6 all failed on the same single cause (anode surface potential < 0 V during 4C charge). Questioning localized the minimum to the END of the charge segment → end-of-charge solid-phase diffusion overpotential at 5.86 µm anode particles (τ = R²/Ds ≈ 1040 s > ~800 s charge). Direction change: negative particle radius sweep (3.5 / 2.61 / 2.0 µm). R7 closed plating under both systems (R7B 2.61 µm: +18 mV margin) with ED 642/641 Wh/kg and T_max 326.8/328.2 K. Full record in log.jsonl plan-update entry + final escalation field.
- 2026-08-25 closing: verdict achieved (R7B, dual-system DFN validation); endorse skipped honestly (real_compute=false); deliverables phase follows.
