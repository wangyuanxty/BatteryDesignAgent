# Design Calculation Sheet

**Case ID**: t3_r1_mimo  
**Document Number**: VBF-T3R1MIMO-CALC-001  
**Date**: 2026-08-30  

---

## 1. Capacity Calculation

| Parameter | Value | Source |
|-----------|-------|--------|
| Nominal cell capacity | 2.3077 Ah | r4_enhanced_1c.json:capacity_ah |
| 1C current | 2.3077 A | I = capacity × 1C |
| 5C current | 11.539 A | I = capacity × 5C |
| 5C discharge capacity | 2.2345 Ah | r4_enhanced_5c.json:capacity_ah |
| **5C retention** | **96.83%** | 2.2345 / 2.3077 |

## 2. Energy Density Calculation (Contract Caliber)

| Parameter | Value | Formula | Source |
|-----------|-------|---------|--------|
| Discharge energy | 8.339 Wh | ∫V·I₁C dt / 3600 | r4_energy.json:energy_wh |
| Cell mass (excl. electrolyte) | 0.02704 kg | Σ layer thickness×(1−ε)×ρ×area | r4_energy.json:mass_kg |
| **Gravimetric ED** | **308.4 Wh/kg** | Energy / mass | r4_energy.json:energy_density_wh_kg |
| Cell volume | 1.171×10⁻⁵ m³ | Σ layer thickness×area | r4_energy.json:volume_m3 |
| **Volumetric ED** | **712.3 Wh/L** | Energy / volume | r4_energy.json:energy_density_wh_l |

## 3. Power Density Calculation

| Parameter | Value | Formula | Source |
|-----------|-------|---------|--------|
| OCV (midpoint) | 3.845 V | Voltage at discharge midpoint | r4_energy.json:midpoint_voltage_v |
| DC Resistance | 2.35 mΩ | (V_start − V_10%) / I₁C | r4_energy.json:dcr_ohm |
| Max power (Ragone) | V²/(4·DCR) | Theoretical max | Derived |
| **Power density** | **65,280 W/kg** | Max power / mass | r4_energy.json:power_density_w_kg |

## 4. Thermal Analysis

| Parameter | Value | Source |
|-----------|-------|--------|
| T_max (1C discharge) | 300.2 K (27.1°C) | r4_enhanced_1c.json:T_max_K |
| T_max (5C discharge) | 316.0 K (42.9°C) | r4_enhanced_5c.json:T_max_K |
| T_max (4C charge at 45°C) | 327.6 K (54.5°C) | r4_enhanced_4c.json:T_max_K |
| **Thermal limit** | **333.15 K (60°C)** | Task criterion |
| **Thermal margin** | **5.5 K** | 333.15 − 327.6 |

## 5. Plating Analysis

| Parameter | Value | Criterion | Status |
|-----------|-------|-----------|--------|
| Anode potential minimum | +0.005 V | ≥ 0 V (no plating) | ✓ PASS |
| Plating determination | No plating | — | ✓ SAFE |

## 6. Layer Thickness Budget

| Layer | Thickness (µm) | Cumulative (µm) |
|-------|----------------|-----------------|
| Positive CC (Al) | 16 | 16 |
| Positive electrode | 35 | 51 |
| Separator | 12 | 63 |
| Negative electrode | 39 | 102 |
| Negative CC (Cu) | 12 | 114 |
| **Total** | **114 µm** | — |

## 7. Key Design Ratios

| Ratio | Value | Notes |
|-------|-------|-------|
| Pos electrode thickness / Neg electrode | 0.897 | Designed for N/P ≈ 1.1 |
| Pos porosity | 0.42 | High for rate capability |
| Neg porosity | 0.32 | Moderate |
| Separator porosity | 0.50 | High for electrolyte access |
| Pos particle radius | 2.0 µm | Reduced from 5.22 µm baseline |
| Neg particle radius | 2.0 µm | Reduced from 5.86 µm baseline |
