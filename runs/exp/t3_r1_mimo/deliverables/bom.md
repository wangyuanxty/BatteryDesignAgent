# Bill of Materials (BOM) — Power Tool Battery Cell

**Case ID**: t3_r1_mimo  
**Document Number**: VBF-T3R1MIMO-BOM-001  
**Date**: 2026-08-30  

---

## Cell-Level BOM

| Item # | Component | Material | Quantity | Unit Mass (g) | Total Mass (g) | Source |
|--------|-----------|----------|----------|---------------|----------------|--------|
| 1 | Positive electrode (active) | NMC811 | 1 | 6.62 | 6.62 | r4_energy.json |
| 2 | Negative electrode (active) | Graphite | 1 | 4.39 | 4.39 | r4_energy.json |
| 3 | Positive current collector | Aluminum (16 µm) | 1 | 4.32 | 4.32 | r4_energy.json |
| 4 | Negative current collector | Copper (12 µm) | 1 | 10.75 | 10.75 | r4_energy.json |
| 5 | Separator | PE (12 µm) | 1 | 0.24 | 0.24 | r4_energy.json |
| 6 | Electrolyte | EC/EMC + LiPF6 | ~2 mL | ~2.4 (est.) | ~2.4 | Domain estimate (ρ≈1.2 g/cm³) |
| 7 | Cell housing | Al pouch | 1 | ~3.0 (est.) | ~3.0 | Domain estimate |
| 8 | Tabs (pos + neg) | Al + Ni | 2 | ~0.5 (est.) | ~1.0 | Domain estimate |
| | **Total cell mass** | | | | **~32.7 g** | Sum (electrolyte + housing estimated) |

### Notes

- Items 1-5 are from contract-caliber simulation (electrolyte excluded from simulation mass)
- Items 6-8 are domain estimates (not simulated)
- Electrolyte fill volume ≈ pore volume × fill factor: (35µm×0.42 + 39µm×0.32 + 12µm×0.50) × 0.1027 m² × ~1.2 g/cm³ ≈ estimated
- BOM is per single cell; pack-level BOM requires additional BMS, housing, wiring

## Material Specifications (Key Items)

| Component | Specification | Notes |
|-----------|---------------|-------|
| NMC811 cathode | LiNi₀.₈Mn₀.₁Co₀.₁O₂, D50 ≤ 2 µm | Particle size override from baseline 5.22 µm |
| Graphite anode | Natural/synthetic graphite, D50 ≤ 2 µm | Particle size override from baseline 5.86 µm |
| Electrolyte | EC/EMC (3:7) + 1M LiPF6 + additives | Enhanced transport: σ=1.5 S/m, t⁺=0.45 |
| Separator | PE, 12 µm, porosity 50% | Shutdown temperature ~130°C |
| Positive CC | Al, 16 µm | Standard |
| Negative CC | Cu, 12 µm | Standard |
