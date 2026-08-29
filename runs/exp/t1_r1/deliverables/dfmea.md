# Design FMEA (qualitative version) — VBF-T1R1-DFMEA-01

Case: t1_r1 | Date: 2026-08-25 | Prepared: ____________ | Reviewed: ____________ | Approved: ____________

Qualitative version, based on simulation signals (S/O: high/medium/low; basis = magnitude of the simulated value vs threshold). RPN = simplified S×O qualitative matrix (annotated qualitative caliber).

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Negative electrode plating (fast charge) | Anode surface potential < 0 V vs Li/Li+ during 4C CC charge from deep discharge (transport/kinetic polarization at 20 A) | cell/r3_I_4c_dfn.json:anode_potential_v min = +0.0249 V (24.9 mV margin; round-1 baseline was −0.4385 V) | high | low | Implemented: graphite particles 2.5 µm, anode porosity 0.40 (120 µm), separator 6 µm, σ = 1.8 S/m, t+ = 0.55, liquid cooling h = 100. Residual note: formula-caliber N/P = 0.752 (usable-window ≈ 1.0) — no N/P headroom; plating safety relies on kinetics/transport margin. Recommend: pack-level 4C charge with CV phase before production. |
| Thermal runaway risk (temperature exceedance) | Cell temperature above 60 °C red line under 4C charge | cell/r3_I_4c_dfn.json:T_max_K = 325.655 K vs 333.15 K (margin 7.50 K); overcharge TR triggered = false (cell/r3_I_tr.json) | high | low | Implemented: liquid cooling h = 100 W/m2K; high-conductivity electrolyte cuts ohmic heat. Recommend: verify margin under pack-level insulation; monitor CV-phase charging heat. |
| Electrolyte oxidative decomposition (voltage window) | Electrolyte HOMO/oxidation limit vs cathode potential | Not assessed this case: molecular-layer criteria (max_homo_ev) unchecked, real_compute = false (no DFT) | high | medium (unverified — honest) | Not yet implemented. Recommend: Stage-5 true DFT endorsement (HOMO level vs 4.2 V-class cathode) before production; overcharge to 4.7 V already simulated without TR (cell/r3_I_oc.json) but does not prove long-term electrolyte stability. |
| Insufficient capacity | Design capacity below target | cell/r3_I_1c.json:capacity_ah = 5.6505 Ah vs parameter nominal 5.0 Ah (no registered capacity criterion) | medium | low | Implemented: capacity verified at 1C. Round-2 lesson: anode AMVF 0.65 became near-limiting (capacity −2.4%); round-3 thickness compensation (120 µm) restored margin — retained in finalist. |
| Anode-limited discharge (capacity loss) | Anode active-material share too low after porosity increase | round-2 evaluate: 1C capacity 5.743 → 5.602 Ah at AMVF 0.65 | medium | low | Implemented: anode thickness 110 → 120 µm (params_r3_I.json); finalist 1C capacity 5.6505 Ah. |

## Conclusion

Highest-risk items: electrolyte oxidative stability (unverified at molecular level — recommend Stage-5 DFT endorsement before production) and plating-margin erosion at pack level (recommend CV-phase and pack-thermal verification). All simulation-signal items with registered criteria have mitigation implemented and verified in the finalist (r3-I). Complete FMEA including process/supplier failure modes: N/A (beyond pure simulation boundary).
