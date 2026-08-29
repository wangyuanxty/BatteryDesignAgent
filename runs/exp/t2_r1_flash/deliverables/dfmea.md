# Design FMEA (qualitative, simulation-signal based) — VBF-T2R1FLASH-DFMEA-01

*Qualitative caliber: severity/occurrence rated 3-level (H/M/L) from simulation deviation magnitude vs threshold; RPN = S x O qualitative matrix. Complete FMEA (process/supplier) N/A (beyond pure simulation boundary).*

| # | Failure mode | Failure cause | Simulation signal (detectability) | S | O | RPN | Design-side mitigation (implemented) |
|---|---|---|---|---|---|---|---|
| 1 | Negative electrode Li plating @4C fast charge | Transport/kinetics overpotential pushes anode potential < 0 V | anode_potential_v min = +12.3 mV (baseline -191.8 mV) | H | L | M | Small negative particles (2.5 um), high-sigma/high-t+ electrolyte, porosity 0.30 |
| 2 | Thermal runaway risk (temp rise over red line) | Ohmic + reaction heat at 4C | T_max 329.2 K vs 333.15 K (baseline 354.3 K) | H | L | M | Active liquid cooling h=60 W/m2K + polarization reduction |
| 3 | SEI overgrowth -> capacity fade | Baseline SEI kinetics | SEI 262 nm @500cyc vs 550 (baseline 778 nm) | M | L | L | SEI-suppression coating bridge (k x0.002, artificial-SEI class) |
| 4 | Low-T capacity loss | Transport freeze-out at -20C | retention 99.4 % vs 90 % (baseline 99.4 %) | M | L | L | High-transport electrolyte (sigma/D/t+ overrides) |
| 5 | Insufficient energy density | Electrode loading/mass balance | 425.4 Wh/kg vs 327.18 (baseline 400.8) | H | L | L | n/a needed (margin) |
| 6 | Electrolyte oxidative decomposition | High-voltage exposure | HOMO/IE-EA vs window: N/A (real_compute=false, no DFT endorsement) | M | L | L | Voltage window 4.2 V within NMC811 stability (lit.); true DFT endorsement not run (case meta) |

**Conclusion**: highest-risk item (4C plating) mitigated in design (anode min +12 mV margin); all simulated signals within limits. Nail/overcharge/crush/process failure modes: N/A (beyond pure simulation boundary).
