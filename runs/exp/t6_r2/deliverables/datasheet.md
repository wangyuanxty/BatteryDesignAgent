# Datasheet — LNMO/Graphite 4C Smartphone Cell (VBF-T6R2-DSH-001)

**Case**: exp/t6_r2 · **Candidate**: R12a_h140 · **Date**: 2026-08-26
All values are tool-output sourced (DFN precise model unless noted).

## Electrical

| Item | Value | Source |
|---|---|---|
| Nominal capacity | 6.374 Ah (1C discharge) | cell/r12_a_1c_dfn.json:capacity_ah |
| Discharge energy | 26.52 Wh | cell/r12_a_energy_dfn.json:energy_wh |
| Volumetric energy density | 1096.0 Wh/L | cell/r12_a_energy_dfn.json:energy_density_wh_l |
| Gravimetric energy density | 493.2 Wh/kg | cell/r12_a_energy_dfn.json:energy_density_wh_kg |
| Voltage plateau (discharge midpoint) | 4.1301 V | cell/r12_a_energy_dfn.json:midpoint_voltage_v |
| Charge cut-off / discharge cut-off | 4.7 V / 2.5 V | LNMO system file |
| DC internal resistance (1C, 10% point) | 6.87 mΩ | cell/r12_a_energy_dfn.json:dcr_ohm |
| Peak power density (theoretical) | 12.25 kW/kg | cell/r12_a_energy_dfn.json:power_density_w_kg |

## Fast charge (4C, 45 °C ambient)

| Item | Value | Source |
|---|---|---|
| 4C charge support | Pass, no lithium plating (min anode potential +0.0382 V) | cell/r12_a_4c45_dfn.json:anode_potential_v |
| Max temperature during 4C charge | 49.55 °C (322.70 K) at 45 °C ambient | cell/r12_a_4c45_dfn.json:T_max_K |
| Note | Protocol current uses system-file nominal 4.5 Ah (~2.8C effective vs 6.374 Ah); true 25.5 A validation recommended | — |

## Life

| Item | Value | Source |
|---|---|---|
| Anode SEI thickness after 100 × 1C cycles | 415.6 nm | cell/r12_a_aging.json:sei_thickness_nm_end |
| SEI control | Dense FEC/VC-class film (EC diffusivity 5.0e-19 m²/s), k_sei 3.0e-13 m/s | params r12_a_h140.json |

## Mechanical / thermal interface

| Item | Value |
|---|---|
| Stack thickness (Σ layers) | 235.6 µm |
| Electrode geometric area | 0.1027 m² |
| Cell mass | 53.77 g |
| Cooling surface area (exposed) | 0.0106 m² (double-sided thin pouch) |
| Heat transfer coefficient requirement | ≥ 140 W/m²·K (vapor-chamber / chassis-coupled; binding) |

## Construction

LNMO spinel cathode (density 4400 kg/m³, 74.75 µm, porosity 0.335, particle 3.0 µm) ·
graphite anode (120 µm, porosity 0.25, particle 1.5 µm) · 25 µm separator ·
EC/EMC + LiPF6 electrolyte (Chen2020 baseline) · Al/Cu current collectors.
Layer areal masses: cathode 0.2212, anode 0.1491, Al CC 0.0432, Cu CC 0.1075,
separator 0.0025 kg/m² (cell/r12_a_energy_dfn.json:layer_kg_m2).

## Caveats

- LNMO file's deprecated positive-electrode diffusivity override is ignored by pybamm
  (positive particle diffusivity used instead) — disclosed, not compensated.
- Aging protocol per-cycle capacities are negative artifacts of the LNMO parameterization;
  SEI thickness is the reliable degradation indicator.
- True-compute endorsement skipped (real_compute=false); values are DFN-simulation grade.
