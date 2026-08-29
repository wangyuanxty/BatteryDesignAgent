# Design Plan — Smartphone Battery (case t6_r2)

Task: Design a battery for a smartphone: volumetric energy density ≥ 950 Wh/L, support 4C fast
charge (no lithium plating), maximum temperature ≤ 50°C, anode SEI thickness ≤ 500 nm after
100 cycles, voltage plateau ≥ 4.1 V.

## 1. Objective decomposition (decision layers)

| Metric | Threshold | Judged by | Decision layer |
|---|---|---|---|
| Volumetric ED | ≥ 950 Wh/L | `calc-energy` → `energy_density_wh_l` (contract formula) | stage2 |
| Voltage plateau | ≥ 4.1 V | `calc-energy` → `midpoint_voltage_v` | stage2 |
| SEI after 100 cyc | ≤ 500 nm | `aging_1C_100cyc` → `sei_thickness_nm_end` | stage2 |
| T_max under 4C charge | ≤ 323.15 K (50 °C) | `4C_charge_45C` (lumped thermal) → `T_max_K` | stage3 |
| Lithium plating | none | `anode_potential_v` min ≥ 0 V → `plated=false` | stage3 |

Trade-off expectations:
- **ED_vol vs 4C plating / T_max (Pareto conflict)**: thick dense electrodes raise Wh/L but
  increase transport overpotential at 4C (plating risk) and heat generation (T_max). The design
  must find the middle: moderate thickness, small anode particles, high-σ electrolyte, high cooling h.
- **Plateau ≥ 4.1 V vs NMC811 chemistry**: NMC811/graphite cell discharge midpoint ≈ 3.6 V
  (anchor table, SKILL.md §1.5); even fully exploited, NMC811 cannot hold a 4.1 V plateau.
  → expected material-property gap → ceiling escalation to a high-voltage system switch (LNMO
  spinel, 4.7 V-class, cell midpoint ≈ 4.17 V per anchor table).
- **SEI ≤ 500 nm**: graphite negative (Chen2020 family); protocol signal-scale reference:
  Chen2020 SEI kinetics ×0.1 → 449→385 nm, so baseline ≈ 450 nm-class likely satisfies ≤ 500 nm.
  Coating levers (SEI kinetic rate constant / exchange current density) available if needed.
- **T_max ≤ 50 °C at 45 °C ambient**: ΔT budget = 5 K — the hardest constraint. Levers:
  cooling coefficient h (thermal management DOF open), DCR reduction, low polarization.

## 2. Candidate strategy

- **Round 1**: baseline characterization on Chen2020 (default system): 1C discharge SPMe→DFN,
  calc-energy, 4C charge @45 °C (lumped + plating), aging 100 cycles. Opening ceiling assessment
  against all five thresholds.
- **Round 2+ (expected)**: ceiling escalation → system-switch candidate **LNMO**
  (`scripts/bda/simulators/data/LNMO.json` as `--base`; skips molecular funnel, direct Stage 3
  simulation; inherits Chen2020 negative/electrolyte/geometry/thermal → aging-capable).
- **Rounds 3–N**: architecture exploration on the winning system, 2–4 variants per round
  (exploration_force ON): electrode thickness, porosity, particle radii, N/P, separator thickness
  & porosity, current collector thickness, electrolyte transport (σ/t⁺/D overrides), cooling h.
- **Fallback routing**: plating → cell architecture (thin electrodes / small particles / high σ);
  T_max → thermal h + DCR reduction; SEI → coating parameter bridge (same system); plateau gap →
  material scale (Stage 2 system candidates).

## 3. Budget allocation

~15 rounds: baseline + ceiling (1) · system switch (1) · architecture exploration (8–10) ·
safety/thermal fine-tune (2–3) · closing. `real_compute: false` → no true DFT/MD endorsement.

## 4. Risk and fallback plan

1. **T_max 5 K rise budget**: if unreachable with default h, raise `Total heat transfer coefficient`
   (thermal management DOF is open) and record the required value honestly in deliverables.
2. **950 Wh/L contract volume**: depends on LNMO 4.7 V platform × dense packing; verify with
   calc-energy early (round 2) — if below, architecture levers first, then electrode composition.
3. **LNMO aging**: SEI parameters inherited from Chen2020 (aging-capable expected; verify at runtime).
4. **LNMO upper cut-off 4.7 V** limits cathode utilization; plateau still expected ≥ 4.1 V (anchor 4.17 V).
5. **Three-strike rule armed**: same failure cause 3 consecutive rounds → question
   system/boundary/metric assumptions layer-by-layer (final `escalation` field).

## 5. References (directional basis — real sources only)

- LNMO 4.7 V OCP parameterization → in-skill `scripts/bda/simulators/data/LNMO.json` +
  `lnmo_parameters.py` (module cites Markovsky et al. / Duncan et al. 4.7 V plateau literature).
- NMC811/graphite vs LNMO plateau anchors → SKILL.md §1.5 anchor table (this skill).
- Plating criterion (negative potential < 0 V vs Li/Li⁺) → domain experience (no precise source).
- Fast-charge heat/plating mitigation via transport parameters and particle size → domain
  experience (no precise source).
- Smartphone volumetric ED 950 Wh/L as roadmap-level target → domain experience (no precise source).
