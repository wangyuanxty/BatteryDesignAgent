# Technical Datasheet — Grid Energy Storage Cell

> VBF-T2R3-DSH-01 | Case t2_r3 | Virtual simulation calibre (PyBaMM DFN/SPMe, Chen2020 base) | Generated 2026-08-26 | Prepared: ______ Reviewed: ______ Approved: ______

## 1. General

| Field | Value | Source |
|---|---|---|
| Cell chemistry | NMC811 / graphite, LiPF6 in EC:EMC (3:7 w/w) electrolyte | Chen2020 parameter set |
| Rated capacity | 5.0 Ah (parameter-set nominal) / 5.0648 Ah simulated (1C CC, 25 °C, 2.5–4.2 V, DFN) | `Nominal cell capacity [A.h]`; cell/r7_final_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V (cut-offs); simulated 1C discharge midpoint 3.9118 V | Chen2020; cell/r7_final_energy_dfn.json:midpoint_voltage_v |
| Rated energy | 18.457 Wh (1C discharge, DFN time-integration of V·I) | cell/r7_final_energy_dfn.json:energy_wh |
| Energy density | 447.12 Wh/kg; 895.02 Wh/L (contract calibre — electrolyte excluded from mass); incl. electrolyte estimate: 374.4 Wh/kg (derived) | cell/r7_final_energy_dfn.json; electrolyte mass = pore volume × 1.2 g/cm³ [estimate] |
| Dimensions | Electrode sheet 65 mm × 1580 mm; layer stack thickness 200.8 µm (pos 75.6 + neg 85.2 + sep 12 + Al 16 + Cu 12 µm); cell envelope / jelly-roll: Not provided (not parameterized) | Chen2020 geometry keys |
| Mass | 41.28 g (contract calibre, electrolyte excluded); 49.30 g incl. electrolyte estimate | cell/r7_final_energy_dfn.json:mass_kg; pore-volume × 1.2 g/cm³ [estimate] |

## 2. Electrical performance

| Field | Value | Source |
|---|---|---|
| Maximum continuous discharge rate | 1C (5 A) — simulated, DFN; DCR 2.612 mΩ; power density 39.08 kW/kg | cell/r7_final_1c_dfn.json; cell/r7_final_energy_dfn.json:dcr_ohm / power_density_w_kg |
| Fast-charge capability | 4C (20 A) at 45 °C: NO lithium plating (anode surface potential min +0.0443 V); T_max 347.70 K (+29.55 K vs 318.15 K ambient, lumped thermal h = 10 W/m²/K); charge phase ≈ 693 s to 4.2 V cut-off (after 1C pre-discharge) | cell/r7_final_4c_dfn.json:anode_potential_v / T_max_K / time_s |
| Low-temperature performance | −20 °C 1C discharge retention 99.57 % (vs 25 °C, same parameters, DFN) | cell/r7_final_lowT_retention.json:lowT_retention |

## 3. Operating range and durability

| Field | Value | Source |
|---|---|---|
| Operating temperature range (simulated) | −20 °C (discharge) … +45 °C (charge); 25 °C nominal cycling | protocols lowT_discharge / 4C_charge_45C / 1C_discharge |
| Durability / SEI | Anode SEI 276.22 nm @ 100 cyc (limit 500 nm) and 393.00 nm @ 500 cyc (limit 550 nm), 1C cycling, SEI model | cell/r6_combo-v5-final_aging100/500_spme.json:sei_thickness_nm_end |
| Cycle-life capacity (information) | Per-cycle capacity in the SEI-only aging model decays (0.331 → 0.216 Ah @ 100 cyc; 0.0123 Ah @ 500 cyc) — SEI lithium-inventory-loss model only, no calendar/fatigue mechanisms; known low-first-cycle Chen2020 artifact. Full cycle life: Not provided (beyond model scope) | cell/r6_combo-v5-final_aging100/500_spme.json:capacity_ah_per_cycle |
| Safety determination | 4C fast charge plating-free (virtual test). Overcharge / nail / thermal-runaway abuse: not required by task, N/A | cell/r7_final_4c_dfn.json; entry-0 criteria |

## 4. Design levers (vs Chen2020 baseline)

| Field | Value | Source |
|---|---|---|
| Electrode particle radii | positive 2.5 µm (baseline 5.22); negative 2.0 µm (baseline 5.86) | r6_combo-v5-final_params.json |
| Electrolyte transport (override) | σ 1.7 S/m const (baseline Nyman2008 σ(298 K) = 0.9487); D 5e-10 m²/s (baseline 1.769e-10); t⁺ 0.45 (baseline 0.2594) — literature-class estimates | r6_combo-v5-final_params.json |
| Negative porosity | 0.40 (baseline 0.25) | r6_combo-v5-final_params.json |
| SEI-suppressing coating bridge | SEI kinetic rate constant 2e-13 m/s (×0.2); SEI partial molar volume 4.7925e-5 m³/mol (×0.5, denser film) — estimate-calibre bridges | r6_combo-v5-final_params.json |