# Design FMEA (Qualitative Version, Based on Simulation Signals) — F1

**VBF-T2R1NOFORCE-DFMEA-001** | Case: t2_r1_noforce | Date: 2026-08-25 | Qualitative ratings S/O = High/Medium/Low, basis = magnitude of simulation value vs threshold. This is the qualitative version based on simulation signals only.

| Failure mode | Failure cause | Simulation signal (detectability basis) | S | O | Design-side mitigation recommendation |
|---|---|---|---|---|---|
| Negative electrode lithium plating (fast charge) | Anode surface potential drops below 0 V at 4C charge end | `anode_potential_v` min = +0.0071 V (margin 7 mV — thin but positive) | H | M | Implemented: 3 µm particles + porosity 0.42. Residual: widen margin via porosity 0.45 or electrolyte σ if the task is re-opened |
| SEI overgrowth beyond spec at 500 cyc | ec-reaction-limited SEI growth never saturates; coating lever saturates | SEI@500 = 738.43 nm vs 550 nm limit (FAIL) | M | H | Implemented: ceramic coating k_SEI ×0.4. Residual: protocol proposal — extend coating bridge to SEI solvent diffusivity (dense ALD film reduces D_ec) or saturating SEI model |
| Thermal runaway risk on 4C fast charge | Excessive heat accumulation during 4C charge | T_max = 359.92 K vs 573 K red line (huge margin) | H | L | Cooling h=10 default sufficient; monitor in pack-level design |
| Electrolyte oxidative decomposition at high voltage | Electrolyte HOMO above cathode potential at 4.2 V | Not computed (no molecular candidate entered Stage 2; NMC811/EC-EMC 4.2 V is standard-compatible per domain experience) | M | L | Keep 4.2 V cut-off; additive screening is a Stage-2 option if re-opened |
| Insufficient capacity | Anode-limited under-utilization | 5.0282 Ah measured vs 5.0 Ah nominal | L | L | N/A — capacity verified PASS |
| Low-temperature capacity loss | Electrolyte transport limitation at −20 °C | Retention 99.45 % vs 90 % limit (lumped model; warm-start artifact fixed via initial-temperature override) | M | L | PASS with margin; keep cold-start protocol fix documented |
| Cathode cracking / structural degradation | Mechanical strain over cycling | Not modeled (Chen2020 has no cracking model) | M | M | N/A (beyond pure-simulation boundary); monitor via OKane2022-class sets if re-opened |

**Conclusion (highest-risk items)**: (1) SEI@500 overgrowth — open, mitigation partially implemented (coating), root cause is model-family limitation, documented in final entry; (2) plating margin at 7 mV — passing but thin, residual recommendations recorded. Complete FMEA including process/supplier failures: **N/A (beyond pure-simulation boundary)**.
