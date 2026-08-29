# Design Plan — t1_r2: Next-Generation Pure Electric Sedan Battery

Case: `exp/t1_r2` · generated 2026-08-26 (headless, zero-interaction execution)
Protocol: Virtual Battery Factory (five-stage funnel, evaluation-and-fallback control loop)

## 1. Objective decomposition (decision layers)

Task text (verbatim contract): energy density ≥ 392.61 Wh/kg; 4C fast charge with no
lithium plating; maximum temperature ≤ 60 °C; overcharge to 4.7 V without thermal
runaway.

| Layer | Metric | Threshold | Tool / source of truth |
|---|---|---|---|
| stage2 (cell performance) | energy_density_wh_kg | ≥ 392.61 Wh/kg (contract caliber, electrolyte excluded) | `calc-energy` on 1C discharge |
| stage3 (safety) | plated | false (no Li plating during 4C charge @45 °C) | `run-pyamm --protocol 4C_charge_45C --thermal lumped --plating` → `anode_potential_v` min ≥ 0 V |
| stage3 (safety) | T_max_K | ≤ 333.15 K (= 60 °C, mechanical conversion) | run-pyamm non-isothermal outputs (4C charge; overcharge) |
| stage3 (safety) | triggered | false (overcharge → no thermal runaway) | `run-pyamm --protocol overcharge` (charges to upper cut-off + 0.5 V = 4.7 V for Chen2020) → `run-tr --sim` coupling |
| stage1 (molecular, only if Stage 2 escalation) | max_energy_ev / max_homo_ev | ≤ 0.0 eV / ≤ −6.0 eV (default elimination lines) | run-mlp / run-xtb funnel |

**Parsing notes (recorded in entry 0 `meta.parsing`):** "overcharge to 4.7 V" maps to
the protocol's overcharge = upper cut-off + 0.5 V. The default system Chen2020 has an
upper cut-off of 4.2 V (verified by parameter dump), so the overcharge protocol
charges to exactly 4.7 V — matching the task text verbatim. "60 °C" → 333.15 K. 4C
fast charge is judged by the plating flag and T_max of the 4C charge protocol at
45 °C ambient.

**Trade-off directions (expectations to test, not conclusions):**
- ED vs plating (central Pareto): thicker electrodes / thinner collectors raise ED
  but thick electrodes increase concentration polarization at 4C (anode potential
  dips → plating). Lower porosity raises contract ED (mass ↓) but degrades ionic
  transport → plating risk.
- ED vs T_max: thicker electrodes lower areal resistance (ASR ↓ → I²R heat ↓ at
  fixed 4C current) — may *help* both ED and heat; lower porosity raises heat.
- N/P ratio: higher N/P (thicker negative) gives anode lithiation headroom at 4C
  (anti-plating) but costs mass → ED ↓ (~2.4 % per +10 % negative thickness).
- Particle size: smaller negative particle radius ↑ surface area → ↓ activation
  overpotential (anti-plating) at unchanged mass. Protocol-internal measurement
  (SKILL.md): small-particle lever measured a +14.6 plating-resistance contribution
  in a prior case — direction confirmed, magnitude to be measured here.
- Overcharge heat: at 4.7 V the NMC811 OCP is in the steep high-stoichiometry
  region; 0.5C overcharge heat raises T; run-tr triggers only from high initial T
  (Arrhenius three-reaction model). Levers: lower ASR, higher cooling h.

## 2. Candidate strategy

- **Round 1 — baseline characterization + ceiling assessment (no variants):**
  Chen2020 baseline 1C discharge (SPMe) → `calc-energy` (ED); 4C charge 45 °C
  (lumped thermal + plating); overcharge (→4.7 V) + `run-tr` coupling. This
  establishes where the baseline sits vs each threshold and which metric is the
  bottleneck.
- **Round 2 — 2–4 architecture variants (exploration_force ON):**
  - V1 "ED-boost": thinner collectors (Al 16→8 µm, Cu 12→6 µm), thinner separator
    (12→9 µm), thicker electrodes (pos 75.6→95 µm, neg 85.2→110 µm), porosity
    pos 0.335→0.31 / neg 0.25→0.28.
  - V2 "Plating guard": negative particle radius 5.86→3.0 µm (and positive
    5.22→3.5 µm) — applied on the best-ED architecture if 4C plating occurs.
  - V3 "Thermal": total heat transfer coefficient 10→30 W/m²K (liquid-cooling
    class) — applied if T_max breaches 333.15 K.
- **Rounds 3+ — fallback-routed fixes** per evaluate verdict (symptom → scale):
  plating → Stage 3 (particle size / N/P / porosity / electrolyte transport bridge);
  T_max → Stage 3 thermal (h) + ASR reduction; ED → Stage 3 thickness/CC/separator.
  If the architecture space proves insufficient for any threshold (three-strike
  triggers questioning first), escalate to Stage 2 material design:
  high-conductivity electrolyte formulation (σ/t⁺ bridge), or system switch
  (OKane2022 SiOx-capable set; LNMO high-voltage cathode via library `LNMO.json`).
- **Final round:** re-verify the winning configuration end-to-end (1C + calc-energy
  + 4C + overcharge + run-tr) as the single nominated design.

## 3. Budget allocation

~6–8 rounds, ≈15–25 cell-scale simulations (SPMe seconds-scale; DFN only if 5C or
needed). Molecular funnel reserved for Stage 2 escalation only (not expected —
see ceiling estimate). True compute: OFF (`real_compute: false`); `endorse` will
record the skip honestly.

## 4. Risk and fallback plan

| Risk | Likelihood | First check | Fallback (symptom → scale) |
|---|---|---|---|
| ED below 392.61 Wh/kg | Low (baseline estimate ≈ 410–430 Wh/kg; architecture ceiling ≈ 550 Wh/kg contract caliber) | R1 `calc-energy` | Stage 3: thinner CC/sep, thicker electrodes; else Stage 2 escalation |
| 4C plating (anode potential < 0 V) | Medium-high — the key risk | R1 4C charge | Stage 3: negative particle radius ↓, N/P ↑, negative porosity ↑, electrolyte σ/t⁺ bridge (literature values, marked estimate); exhausted → Stage 2 (transport-formulation candidates) |
| T_max > 333.15 K at 4C | Medium | R1 4C charge | Stage 3: cooling h ↑ (thermal-management freedom), ASR ↓ via thicker electrodes |
| Overcharge 4.7 V triggers TR | Low-medium (run-tr Arrhenius ignition needs T_init ≫ 400 K) | R1 overcharge + run-tr | Stage 3: lower overcharge heat (ASR, cooling); else Stage 2 (stable high-voltage cathode / coating bridge) |
| Solver failures on variants | Low | each run | read `bda error` verbatim, adjust parameter legality, rerun (DFN auto-falls back to SPMe) |

**Ceiling assessment preview (to be executed in R1, written to funnel log):** best
architecture of the existing NMC811/graphite system — Al 8 µm / Cu 6 µm collectors,
9 µm separator, pos 100 µm / neg 120 µm, porosity 0.31/0.28 — estimated ED
≈ 550 Wh/kg contract caliber (mass ≈ 0.044 kg at ~6.9 Ah), far above 392.61 →
the objective is reachable within the cell-architecture space; Stage 2 escalation
not expected unless transport/safety limits bite.

## 5. References (domain basis, directional)

- NMC811/graphite baseline parameterization: Chen, Brosa Planella, O'Regan, Gastol,
  Widanage, Kendrick, J. Electrochem. Soc. 167, 080534 (2020) — the Chen2020 set.
- Fast charge / plating at high C-rate: Colclasure et al., J. Electrochem. Soc.
  166, A1412 (2019) — anode potential governs plating onset; N/P and surface area
  are the primary cell-level levers.
- Thermal runaway mechanisms & kinetics: Feng, Ouyang et al., Energy Storage
  Materials 10, 246 (2018) — TR review; run-tr module implements Kim et al. 2019 /
  Coman et al. 2016 Arrhenius three-reaction kinetics (as annotated in the module).
- Alloy/high-capacity anodes (fallback only): Obrovac & Chevrier, Chem. Rev. 114,
  11444 (2014).
- Ni-rich cathode direction (fallback only): Manthiram, Nat. Commun. 11, 1550 (2020).
- Protocol-internal measured signals: small-particle plating-resistance contribution
  (+14.6, SKILL.md); Chen2020 SEI kinetics ×0.1 → 100-cycle SEI 449→385 nm
  (SKILL.md, coating-effect calibration reference).

## Revision history

- 2026-08-26: initial plan (entry 0 + this document).
