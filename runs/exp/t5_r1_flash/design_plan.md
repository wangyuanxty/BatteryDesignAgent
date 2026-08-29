# Design Plan — T5-R1-Flash (Flagship Vehicle Battery)

**Task**: next-generation flagship vehicle battery: energy density ≥ 500.94 Wh/kg, 4C fast charge without lithium plating, maximum temperature ≤ 60 °C (333.15 K).
**Date**: 2026-08-25 · **Workspace**: `runs/exp/t5_r1_flash` · **Mode**: headless (zero-interaction), flash run, `real_compute: false`

## 1. Objective decomposition

| # | Metric | Threshold | Decision layer | Primary levers | Trade-off |
|---|--------|-----------|----------------|----------------|-----------|
| 1 | energy_density_wh_kg | ≥ 500.94 | stage2 (cell) | system chemistry (high-V cathode / high-capacity anode), architecture (thin collectors/separator, thick electrodes, low porosity), mass | thicker electrodes ↑ED but ↓heat dissipation & ↑plating risk |
| 2 | plated | false @ 4C | stage3 (safety) | thin negative electrode, small particle radius, high electrolyte σ/t⁺, N/P margin | high σ electrolyte + thin anode ↑ cost/complexity |
| 3 | T_max_K | ≤ 333.15 (60 °C) | stage3 (safety) | cooling h, low DCR (thin electrodes, high σ), 4C at 45 °C ambient → only 15 K rise budget | stronger cooling = system-level constraint |

**Priority**: ED is the binding constraint (500.94 Wh/kg is far beyond conventional Li-ion ~250–300 Wh/kg — a material-level jump is required); plating and T_max are hard safety gates. Expected trade-off: ED↑ (thick electrodes) vs T_max/plating — resolve via electrolyte transport + cooling rather than sacrificing ED.

## 2. Candidate strategy

- **R1 — baseline characterization** (Chen2020, the anchor default): 1C discharge (SPMe → DFN), `calc-energy`, 4C_charge_45C safety (thermal lumped + plating). Establishes the starting point and the ceiling gap.
- **Ceiling assessment** (inside R1–R2): best-possible *existing-system* architecture+formulation (10 µm Al / 6 µm Cu collectors, 9 µm separator, ε≈0.25–0.3 electrodes, high-σ electrolyte, strong cooling) → estimate ~350–450 Wh/kg for NMC811/graphite-class → gap to 500.94 confirmed → **escalate to Stage 2 materials** (not just architecture tuning).
- **R2 — materials**:
  - *System candidates* (direct Stage-3 simulation, no molecular funnel): **LNMO high-voltage spinel** (4.7 V, `--base LNMO.json`) — voltage lever; **OKane2022** (NMC811 / graphite+SiOx, cracking model) — anode capacity lever.
  - *Electrolyte formulation*: transport-parameter overrides (high-σ LiFSI-class electrolyte, σ ↑ / t⁺ ↑) via parameter bridge — fast-charge plating + heat levers.
  - *Molecular additives* (funnel: run-mlp mace/chgnet + run-xtb): FEC / VC / LiFSI-class film-forming + plating-suppression additives — SEI/plating levers (only if budget allows; additive ED contribution is indirect).
- **R3+ — combined design**: best system × best architecture (thin everything, thick active layers) × electrolyte × cooling h; per-round: 1C discharge + calc-energy + 4C safety; iterate toward all three gates.
- **Closing**: endorse (skip, real_compute=false), render, deliverables.

## 3. Budget allocation (flash run)

| Round | Work | Outputs |
|-------|------|---------|
| R1 | Chen2020 baseline 1C + 4C safety + calc-energy | 3 sim files + 1 evaluate |
| R2 | Ceiling architecture variant + Stage-2 funnel (additives) + formulation bridge list | 2–4 sim + funnel + 1–2 evaluate |
| R3 | System candidate 1 (LNMO) full cell sim | 2 sim + calc + evaluate |
| R4 | System candidate 2 (OKane2022 SiOx) full cell sim | 2 sim + calc + evaluate |
| R5 | Best-of combined full design | 2 sim + calc + evaluate |
| R6+ | Refinement / fallback per diagnosis (max ~3 more) | as needed |

## 4. Risk and fallback plan

- **Risk 1 — ED unreachable**: 500.94 Wh/kg is near/above practical Li-metal-cell level; library systems (LNMO, OKane2022 SiOx) may cap at ~400–480 Wh/kg even idealized. *Fallback*: architecture space exhausted (3 strikes, same cause: ED gap) → question system boundary (electrode-composition route via run-comp; Li-metal approximation unavailable → honest note), then close negative **or** direction change; never relax thresholds.
- **Risk 2 — T_max fail**: symptom at cell scale (heat generation/transfer) → fix at Stage 3 (cooling h, electrode thickness, collector thickness), not material scale. Verify first at R1.
- **Risk 3 — plating at 4C**: symptom = transport/kinetics at anode → fix via electrolyte σ/t⁺ bridge (Stage 2 scale) or negative thickness/particle radius (Stage 3). Small-particle + thin-negative lever measured +14.6 contribution (protocol T1).
- **Verify order**: ED ceiling first (decides whether materials are mandatory), then safety gates.

## 5. References (direction → source; honesty: none fabricated)

- 500 Wh/kg-class cell requires Li metal / high-Si anode + high-V cathode → industry roadmap direction (USABC/DOE long-term targets; **domain experience, no precise source**).
- LNMO high-voltage spinel 4.7 V → in-repo library parameter set `scripts/bda/simulators/data/LNMO.json`; high-voltage spinel review direction (Manthiram et al.; **domain experience, no precise source**).
- SiOx-blended graphite anode capacity uplift + degradation/cracking model → OKane2022 parameter set (O'Kane, S. E. J. et al., *J. Electrochem. Soc.* 2022, "Lithium-ion battery degradation: what you need to know") — in-repo set, name from repo.
- Electrolyte conductivity / transference as 4C plating lever → transport-property literature (e.g., Valøen & Reimers 2005, LiPF6 conductivity in carbonate mixtures; **domain memory, approximate**).
- Plating onset = anode surface potential < 0 V vs Li/Li⁺ → standard plating model literature (O'Kane et al. 2020; **domain memory, approximate**).

## Revision history
- v1 (2026-08-25): initial plan as above.
