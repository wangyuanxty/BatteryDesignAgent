# Design FMEA (qualitative, simulation-signal based) — t5_r1_flash

**Doc No. VBF-T5R1FLASH-DFMEA-01** · Rev A (2026-08-25) · Qualitative caliber: severity/occurrence rated from simulation signal magnitude vs threshold; S/O ∈ high/medium/low; RPN = simplified S×O matrix (annotated qualitative).

| Failure mode | Failure cause | Simulation signal (detectability) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Negative-electrode Li plating (fast charge) | anode potential < 0 V at 4C: deep-charge lithiation + electrolyte depletion | anode_potential_v min = **+14.7 mV** (margin vs 0) | low (caught before onset; plating risk currently absent) | low | N/P 1.92 (180 µm negative), negative ε 0.32, D 1e-9/σ 6 (transport), sep ε 0.55 — R4→R9 chain −41→+15 mV |
| Thermal runaway risk (4C charge) | heat generation > dissipation at 4C | T_max 327.55 K vs 333.15 K limit (margin 5.6 K) | high (consequence if triggered) | low | h=100 W/m²K cooling; margin 5.6 K; transport gains cut ohmic heat |
| Electrolyte oxidative decomposition (4.7 V window) | high-voltage oxidation at 4.7 V cathode | Stage 2 funnel: additive set FEC/VC/PES/DTD passed elimination lines (HOMO < −6 eV threshold; HOMO −12.8…−12.0 eV); true DFT endorsement skipped (real_compute=false) | medium | low | 4.7 V-class LNMO system + film-forming additives (SEI/CEI) |
| Insufficient capacity / energy | electrode utilization loss | 1C capacity 8.26 Ah, ED 597.9 Wh/kg vs 500.94 (margin 97 Wh/kg) | medium | low | positive-limited design; stoich window 0.9→0.3 |
| Electrolyte transport degradation at low T | conductivity drop | not simulated (low-T out of scope) | medium | not evaluated | N/A (beyond simulation boundary) |

**Conclusion:** highest-risk items are high-consequence/low-occurrence (thermal) — mitigated by 5.6 K T_max margin and plating-free anode (+14.7 mV margin). All identified failure modes have design-side mitigations implemented in LNMO-R6. Complete FMEA incl. process/supplier failure modes: **N/A (beyond pure simulation boundary)**.
