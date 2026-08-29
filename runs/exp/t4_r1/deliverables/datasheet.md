# Technical Datasheet — VBF-T4R1-DSH-01

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 5.0 nominal / 5.037 measured at 1C, 25 °C | parameter set `Nominal cell capacity [A.h]`; cell/r6_t2_1c_dfn.json |
| Nominal voltage / voltage window (V) | 2.5 – 4.2 (midpoint 3.742 at 1C) | parameter set cut-offs; cell/r6_t2_energy.json:midpoint_voltage_v |
| Rated energy (Wh) | 17.95 (simulated 1C discharge, 25 °C) | cell/r6_t2_energy.json:energy_wh (time integration of V·I) |
| Energy density (Wh/kg) | 471.6 | cell/r6_t2_energy.json:energy_density_wh_kg (contract mass formula, electrolyte excluded) |
| Volumetric energy density (Wh/L) | 925.8 | cell/r6_t2_energy.json:energy_density_wh_l |
| Maximum continuous discharge rate | 1C (5 A) verified by simulation | run-pyamm 1C_discharge protocol |
| −20 °C capability | 1C capacity retention 99.27 % (cold-soaked start, self-heating removed by h = 80) | cell/r6_t2_retention.json (capacity ratio 253.15 K / 298.15 K) |
| Fast-charge capability | 4C/45 °C: +9.6 K temperature rise (T_max 327.7 K ≤ 333.15 K), no lithium plating (anode potential min +20.5 mV); charge is voltage-limited at 4.2 V after 377 s (runner-defined charge-step capacity 0.419 Ah at 4C rate) | cell/r6_t2_4c45C_dfn.json |
| Operating temperature range | Simulated: −20 °C to +45 °C ambient (253.15–318.15 K), plus 25 °C nominal; storage range not simulated | lowT_discharge / 4C_charge_45C / 1C_discharge protocols |
| Cycle life | Not simulated (requires aging model) — must not be inferred from this datasheet | protocol boundary |
| Safety determination | 4C/45 °C: no plating, T_max within 333.15 K red line — pass (simulation) | cell/r6_t2_4c45C_dfn.json |
| DC resistance | 4.06 mΩ (midpoint slope caliber per calc-energy) | cell/r6_t2_energy.json:dcr_ohm |
| Power density | 26.9 kW/kg | cell/r6_t2_energy.json:power_density_w_kg |
| Dimensions | Electrode stack 65 mm × 1580 mm × 188.8 µm (unwound); cell envelope not provided (not modeled) | parameter set + cell/r6_t2_energy.json |
| Mass | 38.07 g (electrolyte excluded) / 44.39 g incl. 6.33 g fill (literature density 1.2 g/cm³) | cell/r6_t2_energy.json:mass_kg + pore-volume calc |

Notes: this datasheet is a virtual (simulation) release; physical-prototype values require cell fabrication and testing. The electrolyte transport values (κ 1.1 S/m, D_e 3e-10 m²/s, t⁺ 0.6) are design targets (LHCE-class idealization) — confirm by measurement before production.
