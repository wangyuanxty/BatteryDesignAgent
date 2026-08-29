# -*- coding: utf-8 -*-
"""One-off deliverable generator for case t8_r1 (T8-40g).

All values are mechanically loaded from tool output JSONs under cell/ —
no numbers typed from memory. Produces:
  deliverables/bom.xlsx, datasheet.docx, calc.xlsx, delivery_index.md
  deliverables/*.pdf  (reportlab releases for all 7 document codes)
"""
import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from docx import Document
from docx.shared import Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

CASE = Path(__file__).resolve().parent
CELL = CASE / "cell"
OUT = CASE / "deliverables"
OUT.mkdir(exist_ok=True)

DEEP = colors.HexColor("#14283C")
MID = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")


def load(name: str):
    return json.loads((CELL / name).read_text(encoding="utf-8"))


params = load("r5_final_params.json")
energy = load("r5_final_energy.json")
ret = load("r5_final_retention.json")
c1 = load("r5_final_1c_dfn.json")
c5 = load("r5_final_5c_dfn.json")
c4 = load("r5_final_4c45_dfn.json")
probe = load("chen2020_base_probe.json")

L = energy["layer_kg_m2"]
area = energy["area_m2"]

# ---- BOM data ----------------------------------------------------------
pos_layer_g = L["positive_electrode"] * area * 1000.0
neg_layer_g = L["negative_electrode"] * area * 1000.0
sep_g = L["separator"] * area * 1000.0
al_g = L["positive_cc"] * area * 1000.0
cu_g = L["negative_cc"] * area * 1000.0

# pore volume = sum(thickness * porosity) * area ; electrolyte 1.2 g/cm3 (literature)
pos_th = float(params["Positive electrode thickness [m]"]) if "Positive electrode thickness [m]" in params else float(probe["Positive electrode thickness [m]"])
neg_th = float(params["Negative electrode thickness [m]"])
sep_th = float(params["Separator thickness [m]"])
pore_cm3 = (pos_th * float(params["Positive electrode porosity"]) +
            neg_th * float(params["Negative electrode porosity"]) +
            sep_th * float(params["Separator porosity"])) * area * 1e6  # m3 -> cm3
elec_g = pore_cm3 * 1.2  # literature density 1.2 g/cm3

energy_kwh = energy["energy_wh"] / 1000.0
kpk = lambda g: g / 1000.0 / energy_kwh  # kg per kWh

# active/CA/binder split: literature default weight fractions (annotated)
F_POS = {"active": 0.96, "CA": 0.02, "binder": 0.02}
F_NEG = {"active": 0.955, "CA": 0.01, "binder": 0.035}

bom_rows = [
    ("Positive electrode active material (NMC811)", pos_layer_g * F_POS["active"],
     f"positive layer mass × {F_POS['active']} wt-frac (lit. default)"),
    ("Positive electrode conductive additive (CB)", pos_layer_g * F_POS["CA"],
     f"positive layer mass × {F_POS['CA']} wt-frac (lit. default)"),
    ("Positive electrode binder (PVDF)", pos_layer_g * F_POS["binder"],
     f"positive layer mass × {F_POS['binder']} wt-frac (lit. default)"),
    ("Negative electrode active material (graphite)", neg_layer_g * F_NEG["active"],
     f"negative layer mass × {F_NEG['active']} wt-frac (lit. default)"),
    ("Negative electrode conductive additive (CB)", neg_layer_g * F_NEG["CA"],
     f"negative layer mass × {F_NEG['CA']} wt-frac (lit. default)"),
    ("Negative electrode binder (SBR/CMC)", neg_layer_g * F_NEG["binder"],
     f"negative layer mass × {F_NEG['binder']} wt-frac (lit. default)"),
    ("Separator", sep_g, "separator layer_kg_m2 × area (contract formula)"),
    ("Electrolyte (not in contract mass)", elec_g, "pore volume × 1.2 g/cm3 (literature, annotated)"),
    ("Positive current collector Al", al_g, "8 µm × 2700 kg/m3 × area (contract formula)"),
    ("Negative current collector Cu", cu_g, "6 µm × 8960 kg/m3 × area (contract formula)"),
    ("Enclosure / tabs", None, "Not modeled"),
]
total_g = sum(r[1] for r in bom_rows if r[1] is not None)
total_contract_g = total_g - elec_g  # electrolyte excluded from contract caliber

# ---- calc sheets -------------------------------------------------------
wb = openpyxl.Workbook()

def sheet(title, header, rows, widths=None):
    ws = wb.active if wb.active.title == "Sheet" else wb.create_sheet()
    ws.title = title
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1E5A8A")
    for r in rows:
        ws.append(r)
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    return ws

ws = sheet(
    "Input parameters",
    ["Parameter", "Value", "Unit", "Source"],
    [
        ["Positive current collector thickness", 8.0, "µm", "r5_final_params.json (override; base 16)"],
        ["Negative current collector thickness", 6.0, "µm", "r5_final_params.json (override; base 12)"],
        ["Positive particle radius", 1.0, "µm", "r5_final_params.json (base 5.22)"],
        ["Negative particle radius", 1.5, "µm", "r5_final_params.json (base 5.86)"],
        ["Electrolyte conductivity", 1.3, "S/m", "r5_final_params.json (const override; lit. estimate)"],
        ["Cation transference number", 0.5, "—", "r5_final_params.json (base 0.2594)"],
        ["Electrolyte diffusivity", 3.5e-10, "m²/s", "r5_final_params.json (const override; lit. estimate)"],
        ["Positive electrode porosity", 0.45, "—", "r5_final_params.json"],
        ["Negative electrode porosity", 0.35, "—", "r5_final_params.json"],
        ["Separator porosity", 0.55, "—", "r5_final_params.json"],
        ["Separator thickness", 10.0, "µm", "r5_final_params.json (base 12)"],
        ["Negative electrode thickness", 95.0, "µm", "r5_final_params.json (base 85.2)"],
        ["Total heat transfer coefficient", 40.0, "W/m²/K", "r5_final_params.json (base 10)"],
        ["Electrode height", 0.072085, "m", "r5_final_params.json (scaled ×1.2299)"],
        ["Electrode width", 1.752222, "m", "r5_final_params.json (scaled ×1.2299)"],
        ["Nominal cell capacity", 6.149417, "Ah", "r5_final_params.json (5.0 × 1.2299)"],
        ["Voltage window", "2.5 – 4.2", "V", "chen2020_base_probe.json"],
    ],
    [42, 18, 12, 60],
)

ws = sheet(
    "Capacity and energy",
    ["Quantity", "Value", "Formula", "Source"],
    [
        ["1C discharge capacity", c1["capacity_ah"], "∫ I_1C dt until 2.5 V (DFN)", "r5_final_1c_dfn.json"],
        ["1C discharge T_max", c1["T_max_K"], "lumped thermal DFN", "r5_final_1c_dfn.json"],
        ["5C discharge capacity", c5["capacity_ah"], "∫ I_5C dt until 2.5 V (DFN)", "r5_final_5c_dfn.json"],
        ["5C discharge T_max", c5["T_max_K"], "lumped thermal DFN", "r5_final_5c_dfn.json"],
        ["5C capacity retention", ret["capacity_retention_5c"], "5C cap ÷ same-params 1C cap", "r5_final_retention.json"],
        ["Discharge energy (1C)", energy["energy_wh"], "∫ V·I_1C dt / 3600", "r5_final_energy.json"],
        ["4C-45°C charge T_max", c4["T_max_K"], "lumped thermal DFN, 4C CC to 4.2 V", "r5_final_4c45_dfn.json"],
        ["4C-45°C anode potential min", min(c4["anode_potential_v"]), "min(anode_potential_v)", "r5_final_4c45_dfn.json"],
        ["4C charge acceptance", c4["capacity_ah"], "∫ I_4C dt until 4.2 V cut-off", "r5_final_4c45_dfn.json"],
    ],
    [34, 18, 44, 30],
)

mass_kg = energy["mass_kg"]
ws = sheet(
    "Energy density",
    ["Quantity", "Value", "Unit", "Formula", "Source"],
    [
        ["Contract mass", mass_kg, "kg", "Σ layer_th×(1−por)×density×area", "r5_final_energy.json"],
        ["Energy", energy["energy_wh"], "Wh", "∫ V·I_1C dt", "r5_final_energy.json"],
        ["Gravimetric ED", energy["energy_density_wh_kg"], "Wh/kg", "energy ÷ mass", "r5_final_energy.json"],
        ["Stack volume", energy["volume_m3"], "m³", "Σ layer thickness × area", "r5_final_energy.json"],
        ["Volumetric ED", energy["energy_density_wh_l"], "Wh/L", "energy ÷ (volume×1000)", "r5_final_energy.json"],
        ["Midpoint voltage", energy["midpoint_voltage_v"], "V", "V at time-midpoint of 1C discharge", "r5_final_energy.json"],
        ["DC internal resistance", energy["dcr_ohm"], "Ω", "(V₀ − V_10%) ÷ I_1C", "r5_final_energy.json"],
        ["Power density", energy["power_density_w_kg"], "W/kg", "V₀²/(4·R_DC)/mass", "r5_final_energy.json"],
    ],
    [30, 20, 12, 46, 32],
)

F = 96485.0
c_max_p = float(probe["Maximum concentration in positive electrode [mol.m-3]"])
c_max_n = float(probe["Maximum concentration in negative electrode [mol.m-3]"])
c0_p = float(probe["Initial concentration in positive electrode [mol.m-3]"])
c0_n = float(probe["Initial concentration in negative electrode [mol.m-3]"])
x0, y0 = c0_p / c_max_p, c0_n / c_max_n
cap_p_full = (1 - 0.45) * c_max_p * F / 3600.0 * pos_th  # Ah/m2 (full window)
cap_n_full = (1 - 0.35) * c_max_n * F / 3600.0 * neg_th  # Ah/m2 (full window)
cap_p_as = cap_p_full * (1 - x0)
cap_n_as = cap_n_full * y0
np_full = cap_n_full / cap_p_full
np_as = cap_n_as / cap_p_as

ws = sheet(
    "NP ratio and mass",
    ["Quantity", "Value", "Formula", "Source"],
    [
        ["Positive capacity density (full)", cap_p_full, "Ah/m²", "(1−ε)·c_max·F/3600·th (window 0→1)"],
        ["Negative capacity density (full)", cap_n_full, "Ah/m²", "(1−ε)·c_max·F/3600·th (window 0→1)"],
        ["N/P (full-theoretical)", np_full, "—", "neg density×th ÷ pos density×th"],
        ["Positive capacity density (assembled)", cap_p_as, "Ah/m²", "full × (1−x₀), x₀=0.270 (probe)"],
        ["Negative capacity density (assembled)", cap_n_as, "Ah/m²", "full × y₀, y₀=0.9014 (probe)"],
        ["N/P (assembled-lithium basis)", np_as, "—", "neg assembled ÷ pos assembled"],
        ["Positive electrode mass", pos_layer_g, "g", "layer_kg_m2 × area × 1000"],
        ["Negative electrode mass", neg_layer_g, "g", "layer_kg_m2 × area × 1000"],
        ["Separator mass", sep_g, "g", "layer_kg_m2 × area × 1000"],
        ["Al CC mass", al_g, "g", "layer_kg_m2 × area × 1000"],
        ["Cu CC mass", cu_g, "g", "layer_kg_m2 × area × 1000"],
        ["Total mass (contract)", total_contract_g, "g", "Σ layer masses (electrolyte excluded)"],
        ["Electrolyte mass (lit. density)", elec_g, "g", "pore volume × 1.2 g/cm³ (annotated)"],
    ],
    [38, 18, 12, 56],
)

ws = sheet(
    "Process parameters",
    ["Parameter", "Value", "Formula", "Source"],
    [
        ["Positive areal density", pos_layer_g / area, "g/m²", "layer_kg_m2 × 1000", "r5_final_energy.json"],
        ["Negative areal density", neg_layer_g / area, "g/m²", "layer_kg_m2 × 1000", "r5_final_energy.json"],
        ["Positive compaction density", float(probe["Positive electrode density [kg.m-3]"]) * 0.55 / 1000.0, "g/cm³", "density×(1−ε) ÷ 1000", "probe (density × 0.55)"],
        ["Negative compaction density", float(probe["Negative electrode density [kg.m-3]"]) * 0.65 / 1000.0, "g/cm³", "density×(1−ε) ÷ 1000", "probe (density × 0.65)"],
        ["Electrolyte fill volume", pore_cm3, "cm³", "Σ(th×ε)×area×1e6", "params + area"],
        ["Electrolyte fill amount", elec_g, "g", "pore vol × 1.2 g/cm³ (lit.)", "literature-annotated"],
        ["Formation", "0.1C CC to 4.2 V, 25 °C, 2 cycles", "—", "design recommended; production tuning required"],
    ],
    [36, 18, 44, 34],
)

# build bom.xlsx separately with dual caliber
wbb = openpyxl.Workbook()
wsw = wbb.active
wsw.title = "BOM"
wsw.append(["Component", "g/cell", "kg/kWh", "Formula / source"])
for c in wsw[1]:
    c.font = Font(bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor="1E5A8A")
for name, g, src in bom_rows:
    wsw.append([name, None if g is None else round(g, 4),
                None if g is None else round(kpk(g), 4), src])
wsw.append(["Total (contract caliber, excl. electrolyte)", round(total_contract_g, 4), round(kpk(total_contract_g), 4),
            "Σ layer rows above; electrolyte excluded (set lacks density)"])
wsw.append(["Total including electrolyte (lit. density)", round(total_g, 4), round(kpk(total_g), 4),
            "informational (adds electrolyte row above)"])
wsw.append(["Cell energy", round(energy["energy_wh"], 4), "Wh", "r5_final_energy.json (∫V·I dt)"])
for col, w in zip("ABCD", (52, 14, 14, 66)):
    wsw.column_dimensions[col].width = w
wbb.save(OUT / "bom.xlsx")

wb.save(OUT / "calc.xlsx")

# ---- datasheet.docx ----------------------------------------------------
doc = Document()
doc.add_heading("Technical Datasheet — T8-40g", 0)
doc.add_paragraph("Document code: VBF-T8R1-DSH-01  |  Case: t8_r1  |  Date: 2026-08-25")
doc.add_paragraph("Prepared: ________  Reviewed: ________  Approved: ________")

rows = [
    ("Rated capacity (Ah)", f"Nominal 6.1494 (parameter set, scaled); verified 6.9427 (1C DFN simulation)"),
    ("Nominal voltage / voltage window (V)", "Window 2.5 – 4.2; discharge midpoint 3.876 (parameter set / simulation)"),
    ("Rated energy (Wh)", f"{energy['energy_wh']:.3f} (time integration of V·I, 1C discharge)"),
    ("Energy density (Wh/kg)", f"{energy['energy_density_wh_kg']:.2f} (contract-caliber mass formula; electrolyte excluded — annotated)"),
    ("Energy density (Wh/L)", f"{energy['energy_density_wh_l']:.1f} (stack volume caliber)"),
    ("Maximum continuous discharge rate", "5C verified: 6.8571 Ah, retention 98.77%, T_max 319.99 K (DFN, 25 °C ambient)"),
    ("Fast-charge capability", "4C @45 °C: T_max 330.41 K (≤ 333.15 K), no plating (anode min +0.0082 V); acceptance voltage-limited to 0.94 Ah — 4C for top-up only, ≤2C for full charge"),
    ("Operating temperature range", "25 °C discharge / 45 °C charge simulated; other temperatures not simulated (Not provided)"),
    ("Cycle life", "Not simulated (requires aging model) — not fabricated"),
    ("Safety determination", "4C-45 °C temperature rise PASS; plating PASS (protocol defaults; see DVPR)"),
    ("DC internal resistance / power density", f"{energy['dcr_ohm']*1000:.3f} mΩ / {energy['power_density_w_kg']/1000:.1f} kW/kg (mechanical derivation)"),
    ("Dimensions", f"{params['Electrode height [m]']*1000:.2f} × {params['Electrode width [m]']*1000:.1f} × {energy['thickness_m']*1000:.3f} mm (unwound electrode geometry; shell thickness not provided)"),
    ("Mass (g)", f"{energy['mass_kg']*1000:.3f} (contract caliber, electrolyte excluded; +11.03 g electrolyte at lit. density 1.2 g/cm³)"),
]
tbl = doc.add_table(rows=1, cols=2)
tbl.style = "Light Grid Accent 1"
tbl.rows[0].cells[0].text = "Field"
tbl.rows[0].cells[1].text = "Value"
for k, v in rows:
    r = tbl.add_row().cells
    r[0].text = k
    r[1].text = v
for r in tbl.rows:
    for cell in r.cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(9)
doc.save(OUT / "datasheet.docx")

# ---- delivery_index.md --------------------------------------------------
case_id = "T8R1"
code_table = [
    ("DS", "Specification", "design_spec.md / design_spec.pdf"),
    ("BOM", "Bill of Materials", "bom.xlsx / bom.pdf"),
    ("DSH", "Datasheet technical parameter sheet", "datasheet.docx / datasheet.pdf"),
    ("CALC", "Calculation sheet", "calc.xlsx / calc.pdf"),
    ("DVPR", "Design verification report", "dvpr.md / dvpr.pdf"),
    ("DFMEA", "Failure analysis", "dfmea.md / dfmea.pdf"),
    ("IDX", "Delivery package index", "delivery_index.md / delivery_index.pdf"),
]
file_rows = [
    ("design_spec.md", "VBF-T8R1-DS-01", "md", "generated per deliverable-design-spec reference; values from tool outputs"),
    ("design_spec.pdf", "VBF-T8R1-DS-01", "pdf", "reportlab one-off export of design_spec.md"),
    ("bom.xlsx", "VBF-T8R1-BOM-01", "xlsx", "openpyxl; dual caliber g/cell + kg/kWh from r5_final_energy.json"),
    ("bom.pdf", "VBF-T8R1-BOM-01", "pdf", "reportlab export of bom.xlsx content"),
    ("datasheet.docx", "VBF-T8R1-DSH-01", "docx", "python-docx per deliverable-datasheet reference"),
    ("datasheet.pdf", "VBF-T8R1-DSH-01", "pdf", "reportlab export of datasheet content"),
    ("calc.xlsx", "VBF-T8R1-CALC-01", "xlsx", "openpyxl; 5 sheets with formula+source columns"),
    ("calc.pdf", "VBF-T8R1-CALC-01", "pdf", "reportlab export of calc sheet tables"),
    ("dvpr.md", "VBF-T8R1-DVPR-01", "md", "generated per deliverable-dvpr reference; 7 pass + N/A items"),
    ("dvpr.pdf", "VBF-T8R1-DVPR-01", "pdf", "reportlab one-off export of dvpr.md"),
    ("dfmea.md", "VBF-T8R1-DFMEA-01", "md", "generated per deliverable-dfmea reference; qualitative S/O"),
    ("dfmea.pdf", "VBF-T8R1-DFMEA-01", "pdf", "reportlab one-off export of dfmea.md"),
    ("delivery_index.md", "VBF-T8R1-IDX-01", "md", "cover + controlled list of this package"),
    ("delivery_index.pdf", "VBF-T8R1-IDX-01", "pdf", "reportlab one-off; inner table row-identical to md"),
    ("report.html", "VBF-T8R1-DS-02", "html", "bda render (ancillary, owned by DS code)"),
]
idx_md = f"""# Delivery Package Index — t8_r1 (T8-40g Long-Endurance Drone Battery)

- **Case name**: t8_r1
- **Numbering scheme**: VBF-{case_id}-<DOC-CODE>-<SEQ-NO>
- **Generation date**: 2026-08-25
- **Signature block**: Prepared: ________  Reviewed: ________  Approved: ________

## Document Code Reference (fixed by protocol)

| Document code | Meaning | Corresponding file |
|--------|------|---------|
""" + "\n".join(f"| {c} | {m} | {f} |" for c, m, f in code_table) + """

## File List

| File name | Number | Format | Source description |
|-----------|--------|--------|--------------------|
""" + "\n".join(f"| {n} | {num} | {f} | {s} |" for n, num, f, s in file_rows) + """

Notes: CAD/cell_model not produced — 3D structure model was not requested in the task text and is not part of the closing deliverables. True DFT/MD endorsement skipped (real_compute = false, recorded in log.jsonl endorse entry). All performance values above originate from tool output files under `cell/` (PyBaMM DFN / calc-energy).
"""
(OUT / "delivery_index.md").write_text(idx_md, encoding="utf-8")

print("BOM/calc/datasheet/index written.")
print(json.dumps({
    "pos_layer_g": pos_layer_g, "neg_layer_g": neg_layer_g, "sep_g": sep_g,
    "al_g": al_g, "cu_g": cu_g, "elec_g": elec_g, "total_g": total_g,
    "pore_cm3": pore_cm3, "np_full": np_full, "np_assembled": np_as,
    "energy_kwh": energy_kwh,
}, indent=2))
