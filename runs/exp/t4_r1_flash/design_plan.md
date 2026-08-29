# VBF Case t4_r1_flash — Design Plan (Stage 1)

Case: **Extreme-cold environment equipment battery**
Goal (verbatim contract): 1C discharge capacity retention ≥ 95% at −20 °C; energy density ≥ 327.18 Wh/kg; volumetric energy density ≥ 880 Wh/L.

## 1. Objective decomposition

| Metric (entry-0 key) | Threshold | Decision layer | Expected trade-off |
|---|---|---|---|
| `low_temperature_retention` = capacity(−20 °C 1C) ÷ capacity(25 °C 1C), same params | ≥ 0.95 | stage2 | **Hard metric.** Low-T loss is driven by charge-transfer kinetics (Chen2020 i0 carries Arrhenius E≈35 kJ/mol neg / 17.8 kJ/mol pos → i0 ×0.081 / ×0.28 at 253 K if cell fully cooled) + cell cooling (lumped thermal, starts 298.15 K, ambient 253.15 K). Electrolyte σ/D are T-independent in Chen2020 (Nyman2008, measured) and solid diffusivities are T-independent (measured). |
| `energy_density_wh_kg` = ∫V·I dt / Σ layer kg (calc-energy, electrolyte excluded) | ≥ 327.18 | stage2 | Easy headroom: baseline NMC811/graphite ≈ 400 Wh/kg by this formula. Trade-off: thin electrodes help retention but raise active-material overhead. |
| `energy_density_wh_l` = energy / Σ layer thickness×area (electrolyte excluded) | ≥ 880 | stage2 | Tight-ish: baseline ≈ 850 Wh/L estimate. Thin separator/CC and thick active layers help; conflicts with retention-oriented thinning. |
| `plated` (4C_charge_45C exam) | false | stage3 (protocol default; task text has no safety metrics) | Thin/thick trade-off. |
| `T_max_K` (4C_charge_45C exam) | ≤ 333.15 K (60 °C red line, protocol default) | stage3 | Strong cooling (high h) for 4C heat vs insulation (low h) for cold retention — **expected Pareto tension**, the central risk of this case. |
| `triggered` (overcharge→TR) | false | stage3 (protocol default) | Run only if relevant at closing. |

Safety criteria note: task text specifies no safety metrics; entry-0 stage3 holds protocol-standard defaults (4C@45 °C plating + 60 °C red line + no TR on overcharge). Recorded as defaults, not task text.

## 2. Candidate strategy (first rounds)

- **R1 baseline characterization (no overrides)**: Chen2020 (NMC811/graphite, task text names no electrode system → anchor-table default). Run 1C_discharge / lowT_discharge / 4C_charge_45C+plating / calc-energy. Establish retention gap, T_max magnitude, ED headroom → **opening ceiling assessment** (which levers assessed, limits, gap).
- **R2** (start_stage=2 material layer, electrolyte-first): electrolyte formulation candidates (solvent/salt formulation → no molecular funnel per protocol; parameter bridge σ/D/t⁺, literature-grounded low-viscosity ester/low-freezing-point formulations — Smart et al. 1999 ternary aliphatic carbonate electrolytes for low T; Zhang et al. 2002 low-T performance) + architecture variants (small particle radius → lower charge-transfer overpotential via larger specific surface; thin separator/CC → volumetric ED; porosity/thickness sweep).
- **R3+**: combine winning levers; iterate retention→0.95; verify ED with calc-energy at each step (mass/volume tracked per candidate). If thermal tension (retention wants insulation, 4C wants cooling) blocks stage3, document the operating-envelope consequence honestly.
- **Fallback routing**: retention shortfall → diagnose cause: (a) charge-transfer limited → particle radius / (if boundary allows) system switch; (b) transport-limited → σ/D/t⁺ up; (c) cell cooled → insulation h↓ (thermal DOF). ED_wh_l shortfall → separator/CC thinning + thickness balance. Three-strike → question assumptions (layer 1: is 95% at 253 K reachable in this parameterization; layer 2: task boundary on thermal/architecture levers; layer 3: metric reachability) → plan update.
- **System switch**: allowed DOF (widest interpretation); only on evidence (e.g., OKane2022 SiOx anode kinetics at low T, or LNMO high-voltage for ED) — not by impression.

## 3. Budget allocation (flash case — lean)

- R1 baseline + ceiling: 4 runs
- R2: 3–4 candidates × (1C + lowT + calc-energy) + optional funnel on additives (cheap, ms-scale) — ~12 runs
- R3+: 2–4 combined rounds — ~12 runs
- Stage 4 + closing: ~4 runs + render + deliverables
- Total ≈ 30–35 simulation runs; SPMe quick-screen, DFN only for final confirmation.

## 4. Risk and fallback plan

1. **Retention < 95% even with all levers** (highest risk): quantification at R1. Questioning path: insulation h (thermal DOF) → if h needed for retention conflicts with 4C T_max, decide by evidence: report operating envelope (cold-environment equipment plausibly never 4C-charges; the exam result reported verbatim, no threshold fiddling).
2. **ED_wh_l < 880** (medium): mechanical; thin separator (12→8 µm) + CC (16/12→10/6 µm) + balanced thickness; calc-energy each round.
3. **Model parameterization limits** (transport T-independent): documented honestly in funnel log; conclusions labeled "within Chen2020 parameterization" where applicable.
4. **3 strikes on same cause** → escalation entries (assumption → conclusion → continue/stop), never blind retries.

## 5. References (domain basis)

- Low-temperature capacity loss & electrolyte design → Zhang, S.S., Xu, K., Jow, T.R., "The low temperature performance of Li-ion batteries", J. Power Sources 115 (2002) 137–140.
- Ternary aliphatic-carbonate electrolytes for low-T (EC/DEC/DMC blends) → Smart, M.C., Ratnakumar, B.V., Surampudi, S., J. Electrochem. Soc. 146 (1999) 486.
- Electrolyte transport fundamentals → Xu, K., "Nonaqueous liquid electrolytes for lithium-based rechargeable batteries", Chem. Rev. 104 (2004) 4303.
- Cold-environment battery thermal management (insulation/self-heating strategy) → Jaguemont, J., Boulon, L., Dubé, Y., "A comprehensive review of lithium-ion batteries used in hybrid and electric vehicles at cold temperatures", Appl. Energy 164 (2016) 99.
- Base parameterization Chen2020 → Chen, C.-H. et al., "Development of experimental techniques for parameterization of multi-scale lithium-ion battery models", J. Electrochem. Soc. 167 (2020) 080534; electrolyte transport Nyman2008 → Nyman, A., Behm, M., Lindbergh, G., Electrochim. Acta 53 (2008) 6356.
- Small particle radius → lower charge-transfer overpotential (larger specific surface): general electrode-design knowledge (domain experience, no precise single source).

## 6. Degree-of-freedom boundary (zero-interaction parse, widest interpretation)

- electrode system: **adjustable** (base = Chen2020 per anchor-table default; switches only on evidence)
- electrolyte formulation: **adjustable** (σ/D/t⁺ bridge; primary lever for low T)
- electrode modification: **adjustable** (coating/doping → SEI/cracking bridge; aging not in task metrics, so secondary)
- cell architecture: **adjustable** (thickness/porosity/N-P/separator/CC/particle radius)
- thermal management: **adjustable** (Total heat transfer coefficient; both cooling-up and insulation-down directions considered)
- excluded (no design chain): solid-phase conductivity/diffusivity, initial concentration/lithiation, Initial SEI thickness, charge cut-off voltage, intercalation exchange-current densities.

## Revision history

- v1 2026-08-25: initial plan.


---

## Closing status (2026-08-25)

- Final candidate **B7_ThinCellE2_h40** confirmed at **DFN precision** (model_used=DFN, no fallback) in round-6 evaluate:
  -20 degC 1C retention 0.99286 (>= 0.95) | ED 460.06 Wh/kg (>= 327.18) | 899.25 Wh/L (>= 880.0) | 4C/45 degC T_max 329.61 K (<= 333.15) | plating-free (anode min +0.019 V) | overcharge 0.5C->4.7 V without thermal runaway (triggered=false).
- Stage 5 true DFT/MD endorsement: **skipped** (real_compute=false, contract meta); recorded as skipped, not fabricated.
- Audit: log.jsonl complete (entry 0 criteria/meta, plan + 1 plan update, R1-R5 propose/evaluate, round-6 final evaluate, endorse, final verdict **achieved**).
- Deliverables: 14 files in deliverables/ (7 sources + 7 PDFs), `bda verify-deliverables` ALL PASS.
