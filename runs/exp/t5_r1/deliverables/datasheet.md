# Technical Datasheet — VBF-T5R1-DSH-01

**Product**: NMC811/graphite(-SiOx) high-energy pouch cell, design R7B (case t5_r1).
**Generation date**: 2026-08-25. Values mechanically from parameter sets / simulation outputs / log-evaluate entries; dual-system (Chen2020 / OKane2022) columns given where they differ.

| Field | Value | Source |
|---|---|---|
| Rated (nominal) capacity | 5.0 Ah | `Nominal cell capacity [A.h]` (both parameter sets) |
| Verified 1C discharge capacity | 6.210 Ah (Chen) / 6.209 Ah (OKane), DFN | `cell/r7b_*_1c_dfn.json`; design exceeds nominal (N/P 1.40, anode-unlocked) |
| Nominal voltage | 3.798 V (Chen) / 3.591 V (OKane) discharge midpoint | `calc-energy` midpoint_voltage_v |
| Voltage window | 2.5 – 4.2 V | parameter sets |
| Rated energy | 22.236 Wh (Chen) / 22.202 Wh (OKane) | `calc-energy` energy_wh (1C time-integrated V·I) |
| Gravimetric energy density | **642.1 Wh/kg** (Chen) / **641.1 Wh/kg** (OKane) — contract caliber, electrolyte excluded | `calc-energy` energy_density_wh_kg |
| Volumetric energy density | 1064.5 Wh/L (Chen) / 1062.9 Wh/L (OKane) — contract caliber, electrolyte excluded | `calc-energy` energy_density_wh_l |
| Mass (contract caliber, electrolyte excluded) | 34.631 g | `calc-energy` mass_kg |
| Electrolyte mass (reference) | 9.53 g (pore volume × 1.2 g/cm³ literature density) | mechanical, design_spec §3 |
| Maximum continuous discharge | 1C (= 5 A nominal current), verified 6.21 Ah to 2.5 V | 1C_discharge protocol, 25 °C |
| Fast-charge capability | 4C (20 A) CC from 2.5 V to 4.2 V at 45 °C ambient: **T_max 326.8 K (53.7 °C, Chen) / 328.2 K (55.0 °C, OKane) ≤ 60 °C; no lithium plating** (anode surface potential min +0.0183 V / +0.0180 V) | `4C_charge_45C` protocol, lumped thermal + plating, DFN |
| 4C charge acceptance | 4.73 Ah (Chen) / 5.00 Ah (OKane) physical | charge-segment duration × 20 A ÷ 3600 (mechanical; library capacity_ah key under-reports 5×, see caveat) |
| Operating temperature range | Simulated at 25 °C (1C discharge) and 45 °C (4C charge). Wider range not simulated | protocol definitions; honest statement |
| Cycle life | **Not simulated in this case** (aging protocol outside task contract). Chen2020/OKane2022 are aging-capable parameter sets; a 100-cycle aging run was not executed — value not fabricated. | honest annotation |
| Safety determination | 4C fast charge: no plating, temperature below 60 °C red line — PASS under both parameter systems. Abuse scenarios (nail, overcharge-to-TR, crush) not simulated | dvpr.md |
| Dimensions | 65 mm × 1580 mm × 203.4 µm layer stack; shell thickness Not provided | parameter sets + calc-energy |
| DC resistance (calc-energy caliber) | 3.50 mΩ (Chen) / 17.93 mΩ (OKane) | `calc-energy` dcr_ohm |

**Caveats (honest disclosure)**:
1. Energy/mass numbers exclude electrolyte (contract caliber, `electrolyte_included: false`).
2. The 4C-output `capacity_ah` key is under-reported ~5× by a pybamm_runner library bug; physical charge acceptance is computed separately and stated above.
3. Electrolyte transport values (σ 2.0 S/m, D_e 4.5×10⁻¹⁰ m²/s, t⁺ 0.45) are design targets at literature-upper-bound estimates — formulation must be validated experimentally.
4. Plating margin is +18 mV — thin by simulation standards; manufacturing tolerances must preserve the 2.61 µm negative particle size and the stated porosity/thickness.
5. No true DFT/MD endorsement (real_compute=false, recorded in log endorse entry).
