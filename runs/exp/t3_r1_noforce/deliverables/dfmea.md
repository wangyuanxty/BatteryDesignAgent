# Design FMEA (qualitative version) — final design V8

**Document no.: VBF-T3R1NOFORCE-DFMEA-01** · Case `exp/t3_r1_noforce` · 2026-08-25
Qualitative ratings based on simulation risk signals only; this is a qualitative design FMEA, not a process/supplier FMEA.

| # | Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|---|
| 1 | Lithium plating on negative electrode during 4C fast charge | anode interface saturation (non-uniform lithiation at high C-rate); aggravated by production drift of negative particle size / porosity | anode_potential_v min = +0.0119 V at 4C/45 °C (margin 11.9 mV) — rounds 1–3 showed crossings of −0.03 to −0.06 V before the transport package | High | Low | transport package implemented (neg r_p 2.0 µm, neg porosity 0.42, separator 9 µm/0.55, t⁺ 0.5, σ 1.4 S/m); production-tolerance control on negative particle size and porosity; charge rate limited to 4C |
| 2 | Thermal limit exceeded (T > 60 °C) | heat generation > pack cooling under sustained load / higher ambient | T_max = 323.57 K at 4C/45 °C (9.6 K margin) and 308.45 K at 5C/25 °C | Medium | Low | h = 45 W/m²K ducted forced-air cooling assumed — pack must guarantee airflow; derate above 45 °C ambient |
| 3 | Electrolyte oxidative decomposition (voltage window) | upper cut-off overshoot / high-voltage surface states | voltage window 2.5–4.2 V respected in all protocols; molecular-level stability not endorsed (real_compute = false) | Medium | Low | charge cut-off fixed at 4.2 V (no overcharge protocol in use); Stage-5 DFT endorsement pending if real_compute is enabled |
| 4 | Insufficient capacity | electrode loading below tolerance / anode-limited balance drift | 1C capacity 2.6683 Ah vs 2.0 Ah requirement (33 % margin) | Low | Low | electrode thickness/AMVF tolerance control; anode-limited design keeps capacity predictable (scales with negative AMVF, verified 0.4 %) |
| 5 | Internal short via separator defect | 9 µm thin separator (power-cell class) with manufacturing defects | separator thickness 9 µm / porosity 0.55 (design values; defect statistics not simulable) | High | Low | ceramic-coated separator quality control; cell-level short-circuit screening on the production line |
| 6 | Fast-charge aging acceleration | SEI growth / degradation under 4C cycling | not simulated in this case (aging model exists in parameter set but no aging protocol run) | Medium | Low | SEI-kinetics-capable parameter set (Chen2020) available for a follow-up aging study |

## Conclusion

Highest-risk items: #1 plating (thin +11.9 mV margin) and #5 thin separator — both mitigated in the design and flagged for production control. Complete process/supplier FMEA: N/A (beyond pure simulation boundary).
