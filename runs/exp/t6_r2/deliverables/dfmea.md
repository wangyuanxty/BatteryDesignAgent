# Design FMEA — LNMO/Graphite 4C Smartphone Cell (VBF-T6R2-DFMEA-001)

**Case**: exp/t6_r2 · **Candidate**: R12a_h140 · **Date**: 2026-08-26
Severity (S) / Occurrence (O) / Detection (D): 1–10 scale; RPN = S·O·D. Mitigations
reflect the design decisions actually simulated (log rounds R1–R12).

| # | Failure mode | Effect | S | Cause | Design mitigation | O | D | RPN |
|---|---|---|---|---|---|---|---|---|
| 1 | Lithium plating at 4C charge | Capacity loss, dendrite risk, safety | 9 | Anode surface saturation cliff at the 4.7 V cutoff of fast charge from deep discharge (log R6/R8 root cause) | N/P margin: negative 120 µm; negative particle 1.5 µm; positive particle 3.0 µm ⇒ min anode potential +0.0382 V (DFN) | 2 | 2 | 36 |
| 2 | Overheating during 4C charge in hot ambient | T > 50 °C, thermal aging | 8 | DFN internal-gradient heat ~3.3× SPMe; ambient 45 °C leaves 5 K budget | Cooling surface 0.0106 m² + h = 140 W/m²·K (vapor-chamber grade) ⇒ 322.70 K. Binding constraint: margin 0.45 K | 3 | 3 | 72 |
| 3 | Thermal-interface degradation | T margin loss → criteria breach | 7 | Contact loss, dust, chassis decoupling | Spec as hard requirement (h ≥ 140, A ≥ 0.0106); periodic thermal verification in DVPR | 3 | 2 | 42 |
| 4 | SEI overgrowth > 500 nm by 100 cycles | Impedance growth, capacity fade | 6 | High-voltage end-of-charge SEI growth (LNMO 4.7 V) | Dense FEC/VC-class film: EC diffusivity 5.0e-19 m²/s + k_sei 3.0e-13 m/s ⇒ 415.6 nm @ 100 cyc | 2 | 2 | 24 |
| 5 | Effective C-rate mismatch | Verification gap: 4C judged at system-file nominal 4.5 Ah (~2.8C vs 6.374 Ah actual) | 5 | Nominal-capacity basis of the 4C protocol | Disclosed in DVPR/datasheet; follow-up DFN run at true 25.5 A recommended before build | 4 | 1 | 20 |
| 6 | Cathode particle cracking / fading (long term) | Capacity fade beyond 100 cycles | 5 | High-voltage spinel structural stress (not modeled in Chen2020 aging: no cracking parameters) | Not addressed in-simulation (parameter set lacks cracking model) — flag for material-stage follow-up | 5 | 4 | 100 |
| 7 | Electrolyte oxidation at 4.7 V | Gas generation, impedance growth | 6 | High upper cut-off of LNMO system | 4.7 V cut-off is system-file fixed (usage mode, not a design lever — per excluded-lever contract) | 4 | 3 | 72 |
| 8 | LNMO file parameterization artifact | Wrong diffusion input, misleading aging trajectory | 4 | Deprecated positive-electrode diffusivity ignored by pybamm; negative per-cycle aging capacities | Disclosed in datasheet/design_spec; SEI thickness used as the reliable metric | 3 | 1 | 12 |

Top RPN: #6 (long-term cracking, not simulatable in this parameter set) and #2/#7 (thermal
margin and electrolyte oxidation). Recommended follow-ups: true 25.5 A DFN validation,
material-stage cracking screening, and real_compute=true endorsement for paper-grade claims.
