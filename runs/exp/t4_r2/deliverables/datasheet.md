# Technical Datasheet — VBF-T4R2-DSH-01
Extreme-cold equipment cell · finalist E3-porheadroom · Chen2020 base (NMC811-class/graphite) · 2026-08-26

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah nominal; 5.0392 Ah simulation-verified (DFN 1C, 25 °C, +0.78 %) | parameter set + `cell/r5_E3_1c_dfn.json` |
| Nominal voltage / window | midpoint 3.847 V (1C discharge); window 2.5 – 4.2 V | `r5_E3_energy_dfn.json` midpoint_voltage_v; parameter set |
| Rated energy | 18.16 Wh | `r5_E3_energy_dfn.json` energy_wh (V·I time integration) |
| Energy density | 459.45 Wh/kg (contract caliber, electrolyte excluded from mass) | `r5_E3_energy_dfn.json` |
| Volumetric energy density | 936.82 Wh/L (Σ layer thickness × area) | `r5_E3_1c/energy_dfn.json` |
| Maximum continuous discharge rate | 1C verified at 25 °C (5.0392 Ah) and at −20 °C (5.0078 Ah) | `r5_E3_1c_dfn.json`, `r5_E3_lowt_dfn.json` |
| Fast-charge capability | 4C @ 45 °C: no plating (anode potential min +0.0060 V), T_max 326.96 K (≤ 333.15, margin 6.19 K); 0.589 Ah accepted in 4C leg | `r5_E3_4c_dfn2.json` |
| Operating temperature range | −20 °C discharge verified (cold-soak protocol); 45 °C charge verified. Outside this range: not simulated — honest simulation boundary | protocol conditions recorded |
| Cycle life | **Not simulated (requires aging model) — not fabricated** | template-required honest statement |
| Safety determination | PASS: T_max 326.96 K ≤ 333.15 K; plated = false (0/307 anode-potential points negative) | `r5_E3_4c_dfn2.json` (stage-4 exam) |
| DCR (informational) | 2.07 mΩ at 10 % discharge (start-OCV minus V₁₀% ÷ I₁C) | `r5_E3_energy_dfn.json` dcr_ohm |
| Dimensions and mass | electrode strip 65.0 mm × 1580.0 mm × 0.1888 mm stack; mass 39.54 g (layers, electrolyte excluded) + 6.01 g electrolyte = 45.55 g; wound outer dimensions and enclosure **Not provided** | parameter set + calc-energy + pore-volume formula |
| Electrolyte (formulation estimates) | σ 1.6 S/m, D 3.2e-10 m²/s, t⁺ 0.6 — blended single-ion class estimates, temperature-independent (like the set's flat functions), **not measured** | parameter overrides, R4/R5 evaluate reasoning |
| Cell chemistry notes | NMC811-class positive (r 3.5 µm, por 0.28), graphite-class negative (r 3.0 µm, por 0.28), separator 8 µm, collectors Al 12 µm / Cu 8 µm, N/P = 1.03 (positive-limited) | parameter set + N/P derivation script |