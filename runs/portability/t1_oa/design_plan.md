# Stage 1 Overall Design Plan — VBF-t1_oa

**Case**: Next-generation pure electric sedan battery.
**Task thresholds** (verbatim contract):
- Energy density ≥ 392.61 Wh/kg (gravimetric, contract caliber, electrolyte excluded)
- 4C fast charge with **no lithium plating** (anode surface potential ≥ 0 V throughout)
- Maximum temperature ≤ 60 °C = 333.15 K (4C charge @45 °C lumped thermal)
- Overcharge to 4.7 V **without thermal runaway** (triggered = false)

## 1. Objective decomposition & trade-off expectation

| Metric | Decision layer | Threshold | Expected trade-off |
|---|---|---|---|
| energy_density_wh_kg | stage2 (cell perf.) | ≥ 392.61 | ↑ED ↔ ↓fast-charge headroom (thicker electrode → higher anode current density → plating) |
| plated (4C) | stage3 (safety) | false | ↑ED ↔ ↑plating risk |
| T_max_K (4C @45C) | stage3 (safety) | ≤ 333.15 | ↑ED (thicker, denser) ↔ worse heat dissipation → ↑T_max |
| triggered (overcharge 4.7 V) | stage3 (safety) | false | high-voltage-stable cathode reduces overcharge severity |

Multi-objective Pareto expectation: ED vs T_max vs plating form a three-way tension. The binding constraint is almost certainly ED (392.61 Wh/kg is aggressive, at/above the practical limit of NMC811/graphite cells ~250–300 Wh/kg cell level).

## 2. Candidate strategy

1. **Round 1 — baseline characterization + opening ceiling assessment** (zero material invention): characterize the deterministic default Chen2020 (NMC811/graphite) 1C discharge + calc-energy, 4C charge @45C (T_max, plating), overcharge→thermal-runaway. Simultaneously characterize the two higher-ED system candidates: **OKane2022** (NMC811/graphite+SiOx, cracking model) and **LNMO.json** (4.7 V-class high-voltage spinel). Estimate the best-possible architecture+formulation ceiling for each system against 392.61 Wh/kg.
2. **Escalate to Stage 2 material design** if and only if the ceiling assessment shows the objective exceeds the reachable ED (expected: Chen2020 ceiling << 392.61; OKane2022/LNMO closer but likely still short → system switch + electrolyte formulation + electrode modification are the levers).
3. **Architecture exploration** (thickness / porosity / N/P / separator / current collector / particle size) + **electrolyte transport override** (σ, t⁺, D) as the primary ED-raising + plating-mitigation knobs.
4. **Safety fine-tuning**: 4C plating elimination (thin electrodes, high-conductivity electrolyte, small particles) and overcharge thermal-runaway avoidance (high-voltage-stable cathode → LNMO reduces overcharge depth relative to its own cutoff).

## 3. Budget allocation (rounds)

- Baseline + ceiling assessment: 2 rounds
- System/material design (Stage 2 escalation): 2–4 rounds
- Architecture + electrolyte exploration: 5–8 rounds
- Safety (plating/T_max/overcharge) fine-tuning: 3–5 rounds
- Total ≈ 12–15 rounds (harness turn budget 300, non-binding)

## 4. Risk & fallback plan

- **ED unreachable in NMC/graphite space** → escalate to SiOx anode (OKane2022) or high-voltage LNMO; if still short, honest negative result with "what would be needed" note (e.g. Li-metal anode, outside parameter-set coverage).
- **Plating at 4C** → thinner electrodes, raise electrolyte conductivity/transference number, reduce particle radius (measured +14.6 contribution in prior work), raise N/P.
- **T_max > 60 °C** → raise cooling h (thermal management DOF), thinner electrodes.
- **Overcharge runaway** → high-voltage cathode (LNMO) so 4.7 V is near-normal cutoff; else accept honest N/A if parameter set lacks stability model.

## 5. References (domain basis)

- SiOx anode raises gravimetric capacity → high-Si anode review / OKane2022 parameterization (NMC811+SiOx cracking model) — domain experience (no precise source)
- High-conductivity/high-transference electrolyte mitigates fast-charge plating → electrolyte transport-parameter literature — domain experience (no precise source)
- High-voltage LNMO spinel (4.7 V) raises cell voltage & overcharge tolerance → LNMO cathode literature — domain experience (no precise source)
- Smaller particle radius improves high-rate capability (reduces plating) — prior in-house measurement (T1) — domain experience
