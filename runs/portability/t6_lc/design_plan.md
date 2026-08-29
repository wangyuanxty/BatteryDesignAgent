# Design Plan — Smartphone Battery (t6_lc)

## Objective decomposition (decision-layer thresholds)
- **Stage-2 (cell performance, pipeline Stage 3)**
  - volumetric energy density `energy_density_wh_l` >= 950 Wh/L (aggressive; NMC811 baseline stack is far below after overheads)
  - voltage plateau `midpoint_voltage_v` >= 4.1 V — **cathode-OCP material property**; NMC811 ~3.6 V cannot reach it
  - anode SEI thickness `sei_thickness_nm_end` <= 500 nm after 100 cycles (Chen2020-kinetics baseline ~449 nm, close to limit)
- **Stage-3 (safety, pipeline Stage 4)**
  - 4C fast charge without lithium plating: `plated == false` (anode potential stays >= 0 V during 4C charge at 45 C)
  - max temperature `T_max_K` <= 323.15 K (50 C) during the 4C/45 C extreme protocol (only 5 K of rise budget)

## Candidate strategy
1. **Baseline characterization (opening ceiling assessment)**: Chen2020 1C discharge + `calc-energy` to record NMC811 plateau & ED and prove the voltage ceiling (expected midpoint ~3.6 V < 4.1 V → material bottleneck).
2. **Material escalation (ceiling_escalation)**: switch to high-voltage LNMO spinel system (`data/LNMO.json`, 4.7 V-class OCP, cell discharge midpoint ~4.17 V per anchor table) — the only library system able to satisfy >= 4.1 V plateau.
3. **Cell architecture optimization**: thinner separator/current collectors, thicker electrodes, lower porosity, higher active-material fraction to push `energy_density_wh_l` >= 950 Wh/L (2-4 variants/round per exploration_force).
4. **Durability + safety**: LNMO aging_1C_100cyc (SEI) then 4C_charge_45C with lumped thermal + plating; adjust cooling `Total heat transfer coefficient`, N/P, and anode particle size for plating/temperature.

## Budget allocation
~8-10 simulation rounds: 1 baseline + 1 system switch + 2-3 architecture (ED) + 2-3 safety (4C/T/plating) + 1 closing.

## Risk and fallback plan
- ED < 950 Wh/L → Stage-3 architecture fallback (thin separator/CC, thick electrodes, low porosity).
- Plating at 4C → Stage-3 fallback (higher N/P, smaller anode particle radius, higher anode porosity) or Stage-2 electrolyte-transport escalation.
- T_max > 323.15 K → thermal-management lever (raise cooling coefficient) + lower DC resistance.
- If ED ceiling unreachable within boundary → three-strike questioning; report negative with "if X relaxed to Y" condition (never relax thresholds silently).

## References (directional, no fabrication)
- 4.7 V-class LNMO spinel raises cell voltage and volumetric ED → library `data/LNMO.json` cites Markovsky/Duncan 4.7 V plateau (skill parameter-set note).
- Thinner separator/current collectors reduce inactive-volume overhead → industry cell-design practice (domain experience, no precise source).
- Smaller anode particle raises high-rate plating resistance → SKILL Stage-3 particle-size note (T1 measured +14.6 contribution).
