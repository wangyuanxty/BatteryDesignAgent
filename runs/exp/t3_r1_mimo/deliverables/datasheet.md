# Technical Datasheet — Power Tool Battery Cell

**Case ID**: t3_r1_mimo  
**Document Number**: VBF-T3R1MIMO-DSH-001  
**Date**: 2026-08-30  

---

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Cell Chemistry** | NMC811 / Graphite Li-ion | Chen2020 parameterization |
| **Rated Capacity** | 2.30 Ah | 1C discharge, 25°C |
| **Nominal Voltage** | 3.84 V | Midpoint voltage from simulation |
| **Voltage Window** | 2.5 – 4.2 V | Chen2020 limits |
| **Rated Energy** | 8.34 Wh | Integration of V·I·t |
| **Energy Density (gravimetric)** | 308.4 Wh/kg | Contract-caliber (excl. electrolyte) |
| **Energy Density (volumetric)** | 712.3 Wh/L | Contract-caliber (excl. electrolyte) |
| **Maximum Continuous Discharge** | 5C (11.5 A) | 96.8% capacity retention vs 1C |
| **Fast-Charge Capability** | 4C at 45°C | No lithium plating (anode min +0.005V) |
| **Maximum Temperature (4C charge)** | 54.5°C (327.6 K) | Thermal limit 60°C: PASS |
| **Power Density** | 65,280 W/kg | V_OC²/(4·DCR)/mass |
| **DC Resistance** | 2.35 mΩ | At 10% discharge |
| **Operating Temperature** | 25°C (simulated) | Simulation conditions |
| **Cycle Life** | Not simulated | Requires aging model — not evaluated |
| **Cell Mass** | 27.04 g | Excl. electrolyte |
| **Cell Dimensions** | 65 × 1580 × 0.114 mm | Height × Width × Total Thickness |
| **Safety — Plating** | No plating at 4C | Anode potential ≥ 0V throughout |
| **Safety — Thermal** | T_max 54.5°C at 4C charge | Below 60°C limit |

### Application Suitability

This cell is designed for **power tool applications** requiring:
- High rate discharge (5C continuous with 96.8% retention)
- Fast charging (4C without lithium plating)
- Thermal safety under aggressive operating conditions

The enhanced electrolyte transport (t⁺=0.45, σ=1.5 S/m) and aggressive thermal management (h=50 W/m²K) are critical design features enabling 4C fast charge capability.
