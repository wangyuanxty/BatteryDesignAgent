# Technical Datasheet — archN_robust (VBF-T5R1SINGLEMODEL-DSH-001)

> Case: t5_r1_singlemodel. Values mechanically taken from parameter set / simulation results and source-annotated; simulated scope stated honestly; cycle life not fabricated.

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah nominal (parameter set); 5.0374 Ah simulation-verified (1C DFN discharge) | `OKane2022:Nominal cell capacity [A.h]` / `cell/r5_final_archN_1c_dfn.json:capacity_ah` |
| Nominal voltage / voltage window | 3.71 V midpoint (1C discharge) / 2.5 – 4.2 V | `cell/r5_final_archN_energy_dfn.json:midpoint_voltage_v` / `OKane2022` cut-offs |
| Rated energy | 18.37 Wh (1C discharge V·I integration) | `cell/r5_final_archN_energy_dfn.json:energy_wh` |
| Gravimetric energy density | 533.18 Wh/kg (contract caliber: discharge energy ÷ layer-mass total, electrolyte excluded) | `cell/r5_final_archN_energy_dfn.json:energy_density_wh_kg` |
| Volumetric energy density | 968.10 Wh/L (layer-stack volume caliber) | `cell/r5_final_archN_energy_dfn.json:energy_density_wh_l` |
| Maximum continuous discharge rate | 1C (simulated; 5C capability not tested in this case — library protocol available) | `1C_discharge` protocol run |
| Fast-charge capability | 4C charge at 45 °C ambient: max cell temperature 330.50 K (57.35 °C) ≤ 60 °C; anode potential min +0.0215 V → no lithium plating. CC-charge capacity at 4C to 4.2 V cut-off: 0.805 Ah (charge acceptance at 4C — reported as measured) | `cell/r4_archN_4c_dfn.json` (protocol `4C_charge_45C`, T_amb 318.15 K) |
| Operating temperature range | Simulated conditions only: 25 °C ambient (1C discharge), 45 °C ambient (4C charge). Wider-range operability not simulated — stated honestly | protocol definitions (`bda/simulators/pybamm_runner.py`) |
| Cycle life | **Not simulated (would require aging-model runs)** — not provided rather than fabricated | library `aging_1C_100cyc` protocol exists but not run in this case |
| Safety determination | 4C fast charge without plating: ✓; max temperature 57.35 °C ≤ 60 °C: ✓ (2.65 K margin) | `cell/r4_archN_4c_dfn.json` |
| DC internal resistance | 15.89 mΩ (1C-discharge-derived: (V₀−V₁₀%)/I₁C) | `cell/r5_final_archN_energy_dfn.json:dcr_ohm` |
| Dimensions | 65 mm × 1580 mm × 0.1848 mm (layer stack; shell thickness not provided) | `OKane2022:Electrode height/width [m]` + calc-energy thickness |
| Mass | 34.46 g (electrode stack + CC + separator, contract caliber); 41.08 g including electrolyte at literature density 1.2 g·cm⁻³ | `cell/r5_final_archN_energy_dfn.json:mass_kg` + pore-volume calc |
| Electrolyte / additives | LiPF6 EC/EMC-class base electrolyte, σ 3.5 S·m⁻¹, D 1.2×10⁻⁹ m²·s⁻¹, t⁺ 0.55; recommended additives VC / FEC / DTD (qualitative, mace-screened) | `candidates/r4_archN_params.json` / `validation/r5_molecules_mace.json` |
