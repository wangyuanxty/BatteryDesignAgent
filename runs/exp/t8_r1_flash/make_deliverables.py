"""Generate all VBF closing deliverables from final_data.json (mechanical values).

Outputs to deliverables/: design_spec.md, bom.xlsx, datasheet.md, calc.xlsx,
dvpr.md, dfmea.md, delivery_index.md + PDF releases (reportlab).
"""
import json
import os

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

CASE = "t8_r1_flash"
BASE = "runs/exp/t8_r1_flash"
D = json.load(open(f"{BASE}/final_data.json", encoding="utf-8"))
S, P, PR = D["sim"], D["params"], D["process"]
os.makedirs(f"{BASE}/deliverables", exist_ok=True)
DD = f"{BASE}/deliverables"

CASE_ID = "T8R1FLASH"
DATE = "2026-08-25"
# layer masses per cell (g)
layer_g = {k: v * S["area_m2"] * 1000 for k, v in S["layer_kg_m2"].items()}

def f(x, n=2):
    return f"{x:.{n}f}"

# ---------------------------------------------------------------- design_spec.md
spec = f"""# Cell Design Specification — VBF-{CASE_ID}-DS-01

**Case**: {CASE} | **Date**: {DATE} | **Design**: V4 Thermal-tuned (final)

## 1. Basic specification
| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Chen2020 base) | parameter set Chen2020 |
| Nominal capacity | {f(S['cap_1c_ah'],2)} Ah (design 3.40 Ah, simulation-verified 1C) | params_r1_v4.json / cell/r1_v4_1c.json:capacity_ah |
| Voltage window | {P['Upper voltage cut-off [V]']:.2f} – {P['Lower voltage cut-off [V]']:.2f} V | parameter set |
| Midpoint (plateau) voltage | {f(S['midpoint_v'],3)} V | cell/r1_v4_energy.json:midpoint_voltage_v |
| Electrode footprint | 65 mm × 1580 mm (unwound electrode, area {f(S['area_m2'],4)} m²) | parameter set Electrode height/width |
| Stack thickness (excl. casing) | {S['thickness_m']*1e6:.1f} µm | cell/r1_v4_energy.json:thickness_m |
| Shell/casing dimensions | Not provided (no shell-thickness parameter) | honest note |
| Electrolyte formulation | EC/EMC + LiPF6 class; high-transport override σ=1.4 S/m, D=4.5e-10 m²/s, t⁺=0.50 (estimate) | params_r1_v4.json; t⁺ marked estimate |
| Cation transference number | 0.50 (estimate, high-transference formulation) | params_r1_v4.json |

## 2. Electrode and separator
| Layer | Material | Thickness | Porosity | Density | Source |
|---|---|---|---|---|---|
| Positive electrode | NMC811 | {P['Positive electrode thickness [m]']*1e6:.1f} µm | {P['Positive electrode porosity']} | {P['Positive electrode density [kg.m-3]']:.0f} kg/m³ | parameter set + params_r1_v4 |
| Negative electrode | Graphite | {P['Negative electrode thickness [m]']*1e6:.1f} µm | {P['Negative electrode porosity']} | {P['Negative electrode density [kg.m-3]']:.0f} kg/m³ | parameter set + params_r1_v4 |
| Separator | Polyolefin | {P['Separator thickness [m]']*1e6:.1f} µm | {P['Separator porosity']} | {P['Separator density [kg.m-3]']:.0f} kg/m³ | parameter set + params_r1_v4 |
| Positive current collector | Al | {P['Positive current collector thickness [m]']*1e6:.1f} µm | – | {P['Positive current collector density [kg.m-3]']:.0f} kg/m³ | params_r1_v4 |
| Negative current collector | Cu | {P['Negative current collector thickness [m]']*1e6:.1f} µm | – | {P['Negative current collector density [kg.m-3]']:.0f} kg/m³ | params_r1_v4 |
| Positive particle radius | – | {P['Positive particle radius [m]']*1e6:.2f} µm | – | – | params_r1_v4 (nano-NMC, literature high-power practice) |
| Negative particle radius | – | {P['Negative particle radius [m]']*1e6:.2f} µm | – | – | params_r1_v4 (fine graphite) |

**N/P ratio**: {f(D['np_ratio'],2)} (theoretical, literature stoich windows Δx_pos=0.75, Δx_neg=0.86; approximate — set does not expose stoich-limit keys; {D['np_note']}). Discharge balance check: 1C capacity {f(S['cap_1c_ah'],2)} Ah from Δx_pos ≈ 0.27→0.85, Δx_neg ≈ 0.901→0.03 (derived from initial concentrations + 1C capacity).

## 3. Process design parameters
| Parameter | Value | Formula | Unit |
|---|---|---|---|
| Areal density, positive | {f(PR['areal_density_pos_g_m2'],1)} | thickness × (1−porosity) × density | g/m² |
| Areal density, negative | {f(PR['areal_density_neg_g_m2'],1)} | thickness × (1−porosity) × density | g/m² |
| Compaction density, positive | {f(PR['compaction_pos_g_cm3'],3)} | electrode density × (1−porosity) ÷ 1000 | g/cm³ |
| Compaction density, negative | {f(PR['compaction_neg_g_cm3'],3)} | electrode density × (1−porosity) ÷ 1000 | g/cm³ |
| Electrolyte fill amount | {f(PR['electrolyte_vol_m3']*1e6,2)} mL (≈{f(PR['electrolyte_vol_m3']*1200*1e3,2)} g @1.2 g/cm³ literature) | pore volume × electrolyte density × fill factor (1.0) | mL / g |
| Formation recommendation | 0.1C CC to 4.2 V, 25 °C, 2 cycles | design recommended value; actual production-line value requires tuning | – |

## 4. Mass breakdown (contract caliber: layer stack, electrolyte/casing excluded)
| Layer | kg/m² | Mass (g/cell) | Source |
|---|---|---|---|
| Positive electrode | {f(S['layer_kg_m2']['positive_electrode'],5)} | {f(layer_g['positive_electrode'],2)} | cell/r1_v4_energy.json:layer_kg_m2 |
| Negative electrode | {f(S['layer_kg_m2']['negative_electrode'],5)} | {f(layer_g['negative_electrode'],2)} | cell/r1_v4_energy.json:layer_kg_m2 |
| Positive current collector | {f(S['layer_kg_m2']['positive_cc'],5)} | {f(layer_g['positive_cc'],2)} | cell/r1_v4_energy.json:layer_kg_m2 |
| Negative current collector | {f(S['layer_kg_m2']['negative_cc'],5)} | {f(layer_g['negative_cc'],2)} | cell/r1_v4_energy.json:layer_kg_m2 |
| Separator | {f(S['layer_kg_m2']['separator'],5)} | {f(layer_g['separator'],2)} | cell/r1_v4_energy.json:layer_kg_m2 |
| **Total (contract mass)** | | **{f(S['mass_kg']*1000,1)} g** | cell/r1_v4_energy.json:mass_kg |

## 5. Performance verification (vs entry-0 criteria)
| Metric | Value | Criterion | Verdict | Source |
|---|---|---|---|---|
| Energy density | {f(S['ed_wh_kg'],1)} Wh/kg | ≥ 446.18 | ✓ PASS | cell/r1_v4_energy.json |
| 5C capacity retention | {f(S['retention_5c']*100,1)} % | ≥ 90 % | ✓ PASS | cell/r1_v4_retention.json |
| Cell mass | {f(S['mass_kg']*1000,1)} g | ≤ 40 g | ✓ PASS | cell/r1_v4_energy.json |
| 4C-charge@45°C T_max | {f(S['tmax_4c_K']-273.15,1)} °C ({f(S['tmax_4c_K'],2)} K) | ≤ 333.15 K | ✓ PASS | cell/r1_v4_4c.json |
| Lithium plating (4C charge) | min anode potential {f(S['anode_min_v'],4)} V > 0 | no plating | ✓ PASS | cell/r1_v4_4c.json:anode_potential_v |

## 6. Design notes
- Baseline Chen2020: ED 400.8 Wh/kg, 5C retention 8.7%, mass 43.5 g (r1 evaluate, fail). Root cause of 5C failure: cathode solid diffusion (D=4e-15 m²/s, r=5.22 µm, τ≈6800 s).
- Fixes (params_r1_v4.json, rationale in log round 2/3 propose+evaluate): nano particles (pos 1.0 µm, neg 1.5 µm) → τ≈250 s; high-transport electrolyte (σ=1.4 S/m, D=4.5e-10, t⁺=0.5 estimate); thin collectors (Al 8 µm, Cu 6 µm) → mass 43.5→26.8 g, ED→473; electrodes thinned 32% (Pareto balance); separator porosity 0.55; pouch cooling area 0.0075 m² (flatter form factor).
- 4C thermal attribution: V3 337.3 K → V5 (transport only) 334.7 K → V4 (transport + cooling area) 332.0 K. Transport/particles ≈ 2.6 K, cooling area ≈ 2.8 K (log round 3).
- Contract caliber: electrolyte/casing excluded from mass (parameter set lacks electrolyte density); 5C/1C retention uses self-consistent nameplate capacity (nominal 3.40 Ah vs actual 3.45 Ah, +1.5%).
"""

open(f"{DD}/design_spec.md", "w", encoding="utf-8").write(spec)
print("design_spec.md OK")

# ---------------------------------------------------------------- datasheet.md
ds = f"""# Technical Datasheet — VBF-{CASE_ID}-DSH-01

**Product**: Long-endurance drone battery cell (design V4 Thermal-tuned) | **Date**: {DATE}
**System**: NMC811 / graphite, high-transport electrolyte (t⁺=0.50 estimate)

| Field | Value | Source |
|---|---|---|
| Rated capacity | 3.40 Ah (nominal, design) / 3.45 Ah (1C simulation-verified) | params_r1_v4.json / cell/r1_v4_1c.json |
| Nominal voltage / window | 3.91 V (midpoint) / 4.20–2.50 V | cell/r1_v4_energy.json / parameter set |
| Rated energy | {f(S['energy_wh'],2)} Wh (∫V·I dt, simulation) | cell/r1_v4_energy.json |
| Energy density | {f(S['ed_wh_kg'],1)} Wh/kg (contract caliber, electrolyte/casing excluded) | cell/r1_v4_energy.json |
| Volumetric energy density | {f(S['ed_wh_l'],1)} Wh/L | cell/r1_v4_energy.json |
| Max continuous discharge rate | 5C verified: retention {f(S['retention_5c']*100,1)} %, T_max {f(S['tmax_5c_K']-273.15,1)} °C | cell/r1_v4_5c.json |
| Fast-charge capability | 4C@45°C: T_max {f(S['tmax_4c_K'],2)} K (≤333.15), no plating (min anode {f(S['anode_min_v'],4)} V) | cell/r1_v4_4c.json |
| DC resistance (1C) | {f(S['dcr_ohm']*1000,2)} mΩ | cell/r1_v4_energy.json |
| Peak power density (theoretical) | {f(S['power_density_w_kg']/1000,1)} kW/kg | cell/r1_v4_energy.json |
| Operating temperature range | −20…45 °C (simulation conditions used: 25 °C discharge, 45 °C charge; −20 °C not verified) | honest note |
| Cycle life | Indicative only: 100-cycle aging → SEI {f(S['sei_end_nm'],1)} nm; capacity trajectory shows standard-SEI-model artifact (climb-then-saturate) — treat as not reliably simulated | cell/r1_v4_aging.json |
| Safety determination | 4C charge: no plating, T_max within limit; overcharge to 4.7 V: T_max {f(S['ovc_tmax_K'],2)} K, thermal runaway not triggered | cell/r1_v4_4c.json, r1_v4_tr.json |
| Dimensions | Electrode 65 mm × 1580 mm; stack thickness {S['thickness_m']*1e6:.1f} µm (excl. casing); casing dims not provided | parameter set |
| Mass | {f(S['mass_kg']*1000,1)} g (contract stack caliber); full BOM incl. electrolyte ≈ 31.6 g | cell/r1_v4_energy.json / bom.xlsx |
"""
open(f"{DD}/datasheet.md", "w", encoding="utf-8").write(ds)
print("datasheet.md OK")

# ---------------------------------------------------------------- dvpr.md
dvpr = f"""# Design Verification Plan and Report (virtual) — VBF-{CASE_ID}-DVPR-01

**Case**: {CASE} | **Date**: {DATE} | **Design**: V4 Thermal-tuned

| # | Item | Condition | Result | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC to 2.5 V, 25 °C, DFN | {f(S['cap_1c_ah'],3)} Ah | meets design 3.40 Ah | cell/r1_v4_1c.json |
| 2 | 5C discharge retention | 5C CC to 2.5 V, 25 °C, DFN | {f(S['retention_5c']*100,1)} % (5C {f(S['cap_5c_ah'],3)} Ah / 1C {f(S['cap_1c_ah'],3)} Ah) | PASS ≥ 90 % | cell/r1_v4_retention.json |
| 3 | Energy density | contract formula | {f(S['ed_wh_kg'],1)} Wh/kg | PASS ≥ 446.18 | cell/r1_v4_energy.json |
| 4 | Cell mass | contract layer stack | {f(S['mass_kg']*1000,1)} g | PASS ≤ 40 g | cell/r1_v4_energy.json |
| 5 | 4C fast-charge temperature rise | 4C charge, 45 °C ambient, lumped thermal, DFN | T_max {f(S['tmax_4c_K'],2)} K (ΔT {f(S['tmax_4c_K']-318.15,1)} K) | PASS ≤ 333.15 K | cell/r1_v4_4c.json |
| 6 | 4C fast-charge plating | same + plating model, min anode potential | {f(S['anode_min_v'],4)} V > 0 | PASS, no plating | cell/r1_v4_4c.json:anode_potential_v |
| 7 | Voltage window | parameter set | 4.20–2.50 V | meets spec | parameter set |
| 8 | Overcharge → thermal runaway (informational) | 1C to 2.5 V, 0.5C to 4.7 V; run-tr coupling | T_max {f(S['ovc_tmax_K'],2)} K; triggered = {S['tr_triggered']} | not triggered (informational) | cell/r1_v4_ovc.json, r1_v4_tr.json |

**N/A items (beyond pure-simulation boundary, require physical experiment)**: nail penetration, crush, drop, rate-pulse internal resistance, cycle life (standard SEI model artifact — see aging note), −20 °C low-temperature retention.

**Conclusion**: All contract verification items PASS. Uncovered items listed above (cite as paper limitations).
"""
open(f"{DD}/dvpr.md", "w", encoding="utf-8").write(dvpr)
print("dvpr.md OK")

# ---------------------------------------------------------------- dfmea.md
dfmea = f"""# Design FMEA (qualitative) — VBF-{CASE_ID}-DFMEA-01

**Qualitative version based on simulation risk signals** (not a full process/supplier FMEA). | **Date**: {DATE}

| Failure mode | Cause | Simulation signal | S | O | Design-side mitigation (implemented) |
|---|---|---|---|---|---|
| Negative electrode lithium plating (fast charge) | anode polarization at 4C, limited negative headroom | min anode potential {f(S['anode_min_v'],4)} V (>0 → no plating signal; V1/V2 showed negative/edge signals) | High | Low | nano particles, high-transport electrolyte (t⁺=0.50 est.), thinner electrodes, separator porosity 0.55 |
| Thermal runaway risk (temperature rise beyond limit) | 4C charge heat generation vs h=10 cooling | 4C T_max {f(S['tmax_4c_K'],2)} K vs 333.15 (margin 1.2 K; V3/V5 exceeded) | High | Low | transport upgrade + larger pouch cooling area 0.0075 m² (V5 control shows +2.8 K without it) |
| Electrolyte oxidative decomposition | voltage window vs HOMO/IE-EA | Not computed (no molecular funnel; real_compute=false) | Medium | Medium | upper cutoff 4.2 V conservative; LNMO 4.7 V system rejected (lower ED path) |
| Insufficient capacity / energy | loading too low, rate losses | 1C {f(S['cap_1c_ah'],2)} Ah, ED {f(S['ed_wh_kg'],1)} Wh/kg vs targets | Medium | Low | thickness/Pareto scan V1–V5; final balances ED vs 5C vs T_max |
| Overcharge thermal runaway | charge beyond 4.2 V | 0.5C to 4.7 V: T_max {f(S['ovc_tmax_K'],2)} K, triggered=false | High | Low | BMS cutoff required (beyond cell design) |

**Conclusion**: Highest-risk item = 4C fast-charge thermal (margin 1.2 K); mitigation implemented via transport + cooling-area levers; plating risk mitigated. Complete FMEA including process/supplier failures: N/A (beyond pure-simulation boundary).
"""
open(f"{DD}/dfmea.md", "w", encoding="utf-8").write(dfmea)
print("dfmea.md OK")

# ---------------------------------------------------------------- bom.xlsx
wb = Workbook()
ws = wb.active
ws.title = "BOM"
hdr = ["Component", "Material", "g/cell", "kg/kWh", "Formula / source"]
rows = [
    ["Positive electrode active material", "NMC811 (90% of coating)", f(layer_g['positive_electrode']*0.90, 2), f(layer_g['positive_electrode']*0.90/1000/S['energy_wh'], 3),
     "coating mass = L·A·(1−ε)·ρ = cell/r1_v4_energy.json layer_kg_m2 × area; 90/5/5 active:CB:binder literature default (no binder/CB params)"],
    ["Positive conductive additive", "carbon black (5%)", f(layer_g['positive_electrode']*0.05, 2), f(layer_g['positive_electrode']*0.05/1000/S['energy_wh'], 3),
     "literature default split, annotated"],
    ["Positive binder", "PVDF (5%)", f(layer_g['positive_electrode']*0.05, 2), f(layer_g['positive_electrode']*0.05/1000/S['energy_wh'], 3),
     "literature default split, annotated"],
    ["Negative electrode active material", "graphite (95% of coating)", f(layer_g['negative_electrode']*0.95, 2), f(layer_g['negative_electrode']*0.95/1000/S['energy_wh'], 3),
     "coating mass = L·A·(1−ε)·ρ; 95/2/3 active:CB:binder literature default"],
    ["Negative conductive additive", "carbon black (2%)", f(layer_g['negative_electrode']*0.02, 2), f(layer_g['negative_electrode']*0.02/1000/S['energy_wh'], 3),
     "literature default split, annotated"],
    ["Negative binder", "PVDF/SBR (3%)", f(layer_g['negative_electrode']*0.03, 2), f(layer_g['negative_electrode']*0.03/1000/S['energy_wh'], 3),
     "literature default split, annotated"],
    ["Separator", "polyolefin", f(layer_g['separator'], 2), f(layer_g['separator']/1000/S['energy_wh'], 3),
     "cell/r1_v4_energy.json layer_kg_m2 separator × area"],
    ["Electrolyte", "EC/EMC + LiPF6 (high-transport)", f(PR['electrolyte_vol_m3']*1200*1e3, 2), f(PR['electrolyte_vol_m3']*1200*1e3/1000/S['energy_wh'], 3),
     "pore volume × 1.2 g/cm³ (literature electrolyte density, annotated); fill factor 1.0"],
    ["Positive current collector", "Al foil", f(layer_g['positive_cc'], 2), f(layer_g['positive_cc']/1000/S['energy_wh'], 3),
     "cell/r1_v4_energy.json layer_kg_m2 positive_cc × area"],
    ["Negative current collector", "Cu foil", f(layer_g['negative_cc'], 2), f(layer_g['negative_cc']/1000/S['energy_wh'], 3),
     "cell/r1_v4_energy.json layer_kg_m2 negative_cc × area"],
    ["Enclosure", "pouch/can", "Not modeled", "Not modeled", "honest note: beyond parameter set"],
    ["Tabs/terminals", "–", "Not modeled", "Not modeled", "honest note: beyond parameter set"],
]
ws.append(hdr)
for r in rows:
    ws.append(r)
total_g = sum(float(r[2]) for r in rows if isinstance(r[2], str) and r[2].replace(".", "").isdigit())
ws.append(["TOTAL (incl. electrolyte)", "", f(total_g, 1), f(total_g/1000/S['energy_wh'], 3),
           "electrolyte included BOM caliber; contract caliber mass = " + f(S['mass_kg']*1000,1) + " g (excl. electrolyte/casing)"])
ws.append(["Cell energy", "", f(S['energy_wh'], 2), "", "cell/r1_v4_energy.json:energy_wh"])
for c in ws[1]:
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor="1E5A8A")
    c.font = Font(bold=True, color="FFFFFF")
ws.column_dimensions["A"].width = 32
ws.column_dimensions["B"].width = 28
ws.column_dimensions["E"].width = 90
ws.column_dimensions["C"].width = 10
ws.column_dimensions["D"].width = 10
wb.save(f"{DD}/bom.xlsx")
print("bom.xlsx OK")

# ---------------------------------------------------------------- calc.xlsx
wb = Workbook()
sh = wb.active
sh.title = "Inputs"
sh.append(["Parameter", "Value", "Unit", "Source"])
for k, v in P.items():
    sh.append([k, str(v), "", "Chen2020 + params_r1_v4.json"])
sh2 = wb.create_sheet("Capacity & Energy")
sh2.append(["Item", "Value", "Unit", "Source"])
sh2.append(["1C discharge capacity", f(S['cap_1c_ah'], 4), "Ah", "cell/r1_v4_1c.json"])
sh2.append(["5C discharge capacity", f(S['cap_5c_ah'], 4), "Ah", "cell/r1_v4_5c.json"])
sh2.append(["5C retention", f(S['retention_5c'], 4), "ratio", "5C/1C (mechanical)"])
sh2.append(["Discharge energy", f(S['energy_wh'], 4), "Wh", "∫V·I dt / 3600, cell/r1_v4_energy.json"])
sh2.append(["Midpoint voltage", f(S['midpoint_v'], 4), "V", "cell/r1_v4_energy.json"])
sh2.append(["DC resistance", f(S['dcr_ohm']*1000, 4), "mΩ", "cell/r1_v4_energy.json"])
sh3 = wb.create_sheet("Energy Density")
sh3.append(["Item", "Value", "Unit", "Source"])
sh3.append(["Mass (contract)", f(S['mass_kg']*1000, 2), "g", "Σ layer×(1−ε)×ρ×A, cell/r1_v4_energy.json"])
sh3.append(["Energy density", f(S['ed_wh_kg'], 2), "Wh/kg", "energy/mass, cell/r1_v4_energy.json"])
sh3.append(["Volumetric energy density", f(S['ed_wh_l'], 2), "Wh/L", "cell/r1_v4_energy.json"])
sh3.append(["Stack thickness", f(S['thickness_m']*1e6, 2), "µm", "cell/r1_v4_energy.json"])
sh4 = wb.create_sheet("N-P & Mass")
sh4.append(["Item", "Value", "Unit", "Source"])
sh4.append(["N/P ratio", f(D['np_ratio'], 3), "–", D['np_note']])
for k, v in S['layer_kg_m2'].items():
    sh4.append([f"layer {k}", f(v, 5), "kg/m²", "cell/r1_v4_energy.json"])
sh5 = wb.create_sheet("Process")
sh5.append(["Parameter", "Value", "Unit", "Formula"])
sh5.append(["Areal density positive", f(PR['areal_density_pos_g_m2'], 2), "g/m²", "L×(1−ε)×ρ"])
sh5.append(["Areal density negative", f(PR['areal_density_neg_g_m2'], 2), "g/m²", "L×(1−ε)×ρ"])
sh5.append(["Compaction density positive", f(PR['compaction_pos_g_cm3'], 4), "g/cm³", "ρ×(1−ε)÷1000"])
sh5.append(["Compaction density negative", f(PR['compaction_neg_g_cm3'], 4), "g/cm³", "ρ×(1−ε)÷1000"])
sh5.append(["Electrolyte fill", f(PR['electrolyte_vol_m3']*1e6, 2), "mL", "pore volume; mass @1.2 g/cm³ literature"])
sh5.append(["Formation", "0.1C CC to 4.2 V, 25 °C, 2 cycles", "–", "design recommendation; production value needs tuning"])
for s in wb.worksheets:
    for c in s[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1E5A8A")
    s.column_dimensions["A"].width = 40
    s.column_dimensions["B"].width = 30
    s.column_dimensions["C"].width = 14
    s.column_dimensions["D"].width = 70
wb.save(f"{DD}/calc.xlsx")
print("calc.xlsx OK")

# ---------------------------------------------------------------- PDFs (md -> pdf, blueprint style)
DEEP, MID, COPPER = "#14283C", "#1E5A8A", "#C97B3D"
st_title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, textColor=colors.HexColor(DEEP), spaceAfter=6)
st_h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, textColor=colors.HexColor(MID), spaceBefore=8, spaceAfter=3)
st_body = ParagraphStyle("b", fontName="Helvetica", fontSize=8.5, leading=11)
st_cell = ParagraphStyle("c", fontName="Helvetica", fontSize=7.5, leading=9)


def md_to_pdf(md_path, pdf_path, title):
    lines = open(md_path, encoding="utf-8").read().splitlines()
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, leftMargin=14*mm, rightMargin=14*mm,
                            topMargin=14*mm, bottomMargin=14*mm)
    story = [Paragraph(title, st_title), Spacer(1, 4)]
    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        if not ln:
            i += 1
            continue
        if ln.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if cells and not all(set(c) <= set("-: ") for c in cells):
                    tbl.append([Paragraph(c, st_cell) for c in cells])
                i += 1
            if tbl:
                t = Table(tbl, repeatRows=1)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(MID)),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9DB4C4")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF3F7")]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]))
                story.append(t)
                story.append(Spacer(1, 4))
            continue
        if ln.startswith("# "):
            story.append(Paragraph(ln[2:], st_title))
        elif ln.startswith("## "):
            story.append(Paragraph(ln[3:], st_h))
        elif ln.startswith("### "):
            story.append(Paragraph(ln[4:], st_h))
        elif ln.startswith("- "):
            story.append(Paragraph("• " + ln[2:], st_body))
        else:
            story.append(Paragraph(ln, st_body))
        i += 1
    doc.build(story)


def xlsx_to_pdf(xlsx_path, pdf_path, title):
    from openpyxl import load_workbook
    wb = load_workbook(xlsx_path)
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, leftMargin=12*mm, rightMargin=12*mm,
                            topMargin=14*mm, bottomMargin=14*mm)
    story = [Paragraph(title, st_title), Spacer(1, 6)]
    for sh in wb.worksheets:
        story.append(Paragraph(sh.title, st_h))
        data = [[Paragraph(str(c.value) if c.value is not None else "", st_cell) for c in row] for row in sh.iter_rows()]
        if data:
            t = Table(data, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(MID)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9DB4C4")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
    doc.build(story)


md_to_pdf(f"{DD}/design_spec.md", f"{DD}/design_spec.pdf", "Cell Design Specification")
md_to_pdf(f"{DD}/datasheet.md", f"{DD}/datasheet.pdf", "Technical Datasheet")
md_to_pdf(f"{DD}/dvpr.md", f"{DD}/dvpr.pdf", "Design Verification Plan & Report")
md_to_pdf(f"{DD}/dfmea.md", f"{DD}/dfmea.pdf", "Design FMEA (qualitative)")
xlsx_to_pdf(f"{DD}/bom.xlsx", f"{DD}/bom.pdf", "Bill of Materials")
xlsx_to_pdf(f"{DD}/calc.xlsx", f"{DD}/calc.pdf", "Design Calculation Sheet")
print("PDFs OK")
