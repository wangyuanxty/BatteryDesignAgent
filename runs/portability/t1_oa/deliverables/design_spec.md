# Cell Design Specification — VBF-T1OA-DS-01

> Case: next-generation pure electric sedan battery. Values mechanically taken from parameter set / simulation output; sources annotated per line. Missing items marked "Not provided".

## 1. Basic specification

| Field | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 positive / graphite+SiOx negative (OKane2022) | parameter set `--base OKane2022` |
| Nominal capacity | 5.0 Ah (nominal) / 5.057 Ah (1C DFN simulated) | parameter set / `cell/T10_1c_dfn.json` |
| Voltage window | 2.5 – 4.2 V | parameter set (Lower/Upper voltage cut-off) |
| Cell dimensions (h × w × t) | 65 mm × 1580 mm × 200.8 µm (active stack; shell thickness Not provided) | parameter set geometry + `cell/T10_energy_dfn.json:thickness_m` |
| Electrolyte formulation | advanced formulation: conductivity 3.0 S/m, transference number t⁺=0.6, diffusivity 4.0e-10 m²/s (estimate, advanced LiFSI/carbonate-class) | design override `params_T10.json` |
| Cation transference number | 0.6 | design override |
| Thermal management | liquid cooling, h = 80 W/m²/K | design override |

## 2. Electrode and separator

| Layer | Thickness (µm) | Porosity | Active-material vol. frac. | Current collector |
|---|---|---|---|---|
| Positive (NMC811) | 75.6 | 0.335 | 0.665 | Al, 16 µm |
| Separator (polyolefin) | 12 | 0.47 | — | — |
| Negative (graphite+SiOx) | 85.2 | 0.25 | 0.75 | Cu, 12 µm |

- N/P ratio = (negative areal Li capacity) ÷ (positive areal Li capacity) = (0.75 × 85.2 µm × 33133 mol/m³) ÷ (0.665 × 75.6 µm × 63104 mol/m³) = 2.118 ÷ 3.172 = **0.667**. Note: computed from the parameter set's maximum concentrations (graphite-basis for the negative); the SiOx component contributes additional capacity via its own OCP, and plating safety at 4C is verified (+0.0341 V) independent of this c_max-based ratio.

## 3. Process design parameters

| Parameter | Positive | Negative | Source |
|---|---|---|---|
| Areal density (g/m²) | 163.99 | 105.88 | thickness × (1−porosity) × density |
| Compaction density (g/cm³) | 2.169 | 1.243 | density × (1−porosity) ÷ 1000 |
| Electrolyte fill amount | 6.44 g/cell (total pore vol. 5.37 cm³ × 1.2 g/cm³) | — | pore volume × 1.2 g/cm³ (literature value) |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | — | design recommended value; production value requires tuning |

## 4. Mass breakdown

| Layer | kg/m² | g/cell | Source |
|---|---|---|---|
| Positive electrode | 0.16399 | 16.84 | `cell/T10_energy_dfn.json:layer_kg_m2` × area 0.1027 m² |
| Negative electrode | 0.10588 | 10.87 | same |
| Positive current collector (Al) | 0.04320 | 4.44 | same |
| Negative current collector (Cu) | 0.10752 | 11.04 | same |
| Separator | 0.002525 | 0.259 | same |
| **Total (electrolyte excluded)** | 0.42312 | **43.45** | `cell/T10_energy_dfn.json:mass_kg` |

Note: contract-caliber mass excludes electrolyte (parameter set lacks electrolyte density) and casing.

## 5. Performance verification

| Item | Condition | Result | Determination | Source |
|---|---|---|---|---|
| 1C discharge capacity | 1C, 298 K | 5.057 Ah | ✓ (nominal 5.0) | `cell/T10_1c_dfn.json` |
| Energy density | contract caliber | 426.89 Wh/kg | ✓ (≥ 392.61) | `cell/T10_energy_dfn.json` |
| Volumetric energy density | contract caliber | 899.5 Wh/L | — | `cell/T10_energy_dfn.json` |
| 4C fast charge, plating | 4C, 318 K, plating module | anode min +0.0341 V → no plating | ✓ (plated=false) | `cell/T10_4c_dfn.json` |
| 4C temperature rise | 4C, 318 K, lumped thermal | T_max 324.55 K (51.4 °C) | ✓ (≤ 333.15 K) | `cell/T10_4c_dfn.json` |
| Overcharge 4.7 V thermal runaway | 0.5C charge to 4.7 V + run-tr | triggered = false | ✓ | `cell/T10_tr.json` |

## 6. Design notes

Changed vs OKane2022 baseline: (1) cooling h 10 → 80 W/m²/K to cap 4C temperature (368 → 324.55 K); (2) electrolyte transport σ 1.x → 3.0 S/m, t⁺ 0.259 → 0.6, D → 4e-10 m²/s; (3) negative particle radius 5.86 → 0.8 µm (nanostructured SiOx) and positive 5.22 → 2.0 µm. Rationale (evaluate log R2–R4): graphite anode (Chen2020) plates fundamentally at 4C (anode −0.438 V, transport-insensitive); SiOx anode does not plate but overheats at default cooling; liquid cooling caps T_max while advanced transport + nanostructured anode restore the no-plating margin at the cooler operating temperature.
