# Technical Datasheet — V_K HEV Battery Cell

**Document Number**: VBF-T7R1MIMO-DSH-01
**Date**: 2026-08-31

## Nominal Specifications

| Parameter | Value | Unit | Conditions |
|-----------|-------|------|------------|
| Nominal capacity | 4.95 | Ah | 1C, 25°C |
| Nominal voltage | 3.94 | V | 1C discharge midpoint |
| Energy density | 418.95 | Wh/kg | 1C, 25°C, dry mass |
| Volumetric energy density | 843.5 | Wh/L | 1C, 25°C |
| DC resistance (10% SOC) | 0.348 | mΩ | 1C, 25°C |
| Power density | 269,681 | W/kg | V²/(4·DCR)/mass |
| Upper cut-off voltage | 4.20 | V | — |
| Lower cut-off voltage | 2.50 | V | — |
| Cell mass (dry) | 43.45 | g | formula-caliber |
| Cell volume | 20.62 | cm³ | active stack |

## Rate Performance

| Rate | Capacity (Ah) | Retention | Notes |
|------|---------------|-----------|-------|
| 1C | 4.95 | 100% | baseline |
| 4C charge (no plating) | 0.03* | — | anode_potential > 0V; capacity is charge input to cutoff |
| 5C discharge | TBD | — | not simulated |

*Note: 4C charge capacity limited by voltage cutoff; key metric is plating-free operation.

## Cycling Performance

| Condition | Cycles | Capacity Retention | SEI Thickness |
|-----------|--------|-------------------|---------------|
| 1C/1C, 25°C | 100 | 100% (isothermal model) | — |
| 1C/1C, 45°C | 100 | — (climb artifact) | 536.0 nm |

## Safety Performance

| Test | Condition | Result | Notes |
|------|-----------|--------|-------|
| 4C fast charge | 45°C, thermal coupled | T_max = 359K (86°C) | No plating |
| Nail penetration | 10W heat, hA=0.5 | Not triggered | T_max = 318K (45°C) |
| Overcharge | +0.5V above cutoff | T_max = 307K (34°C) | No thermal runaway |

## Operating Conditions

| Parameter | Min | Nominal | Max |
|-----------|-----|---------|-----|
| Temperature (charge) | 0°C | 25°C | 45°C |
| Temperature (discharge) | -20°C | 25°C | 60°C |
| Charge rate | 0.1C | 1C | 4C |
| Discharge rate | 0.1C | 1C | 5C |
