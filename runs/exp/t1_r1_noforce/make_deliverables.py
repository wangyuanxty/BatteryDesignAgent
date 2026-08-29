"""One-off deliverables builder: bom.xlsx, calc.xlsx, and PDF releases for all 7 categories.
Agent-built input script (allowed); output artifacts are the deliverables themselves."""
import math
import re
import sys
from pathlib import Path

D = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t1_r1_noforce\deliverables")
D.mkdir(exist_ok=True)

AREA = 0.1027
ENERGY_WH = 20.47186640547461
ENERGY_KWH = ENERGY_WH / 1000.0
MASS_G = 44.70530568660001

# ---------------- BOM ----------------
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

rows = [
    ("Positive active material (NMC811)", 16.168, "96 wt% of positive layer 16.842 g (literature default split; parameter set lacks additive/binder keys)"),
    ("Positive conductive additive (carbon)", 0.337, "2 wt% literature default"),
    ("Positive binder (PVDF)", 0.337, "2 wt% literature default"),
    ("Negative active material (graphite)", 11.640, "96 wt% of negative layer 12.125 g (literature default split)"),
    ("Negative conductive additive (carbon)", 0.243, "2 wt% literature default"),
    ("Negative binder", 0.243, "2 wt% literature default"),
    ("Separator (PP 12 um, porosity 0.47)", 0.259, "layer_kg_m2 0.00252492 x 0.1027 m2 (calc-energy r6_c7_energy.json)"),
    ("Electrolyte (EC/EMC + LiPF6)", 6.743, "pore volume 5.6193e-6 m3 x 1200 kg/m3 (literature density, fill factor 1.0; parameter set lacks electrolyte density)"),
    ("Positive current collector (Al 16 um)", 4.437, "layer_kg_m2 0.043200 x 0.1027 m2 (calc-energy)"),
    ("Negative current collector (Cu 12 um)", 11.042, "layer_kg_m2 0.107520 x 0.1027 m2 (calc-energy)"),
    ("Enclosure / tabs", None, "Not modeled"),
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
head = ["Component", "Mass (g/cell)", "kg/kWh", "Source note"]
ws.append(head)
for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor="14283C")
total = 0.0
for name, g, note in rows:
    if g is None:
        ws.append([name, "Not modeled", "", note])
    else:
        ws.append([name, round(g, 3), round(g / 1000.0 / ENERGY_KWH, 4), note])
        total += g
ws.append(["TOTAL (incl. electrolyte estimate)", round(total, 3), round(total / 1000.0 / ENERGY_KWH, 4),
           "mechanical sum; contract mass (electrolyte excluded) = 44.705 g from r6_c7_energy.json:mass_kg"])
for cell in ws[ws.max_row]:
    cell.font = Font(bold=True)
ws.append(["Cell energy (kWh)", ENERGY_KWH, "", "r6_c7_energy.json:energy_wh / 1000"])
for col, w in zip("ABCD", (42, 14, 12, 88)):
    ws.column_dimensions[col].width = w
bom_path = D / "bom.xlsx"
wb.save(bom_path)

# ---------------- CALC ----------------
def sheet(ws, title, header, data):
    ws.append([title])
    ws["A1"].font = Font(bold=True, size=13, color="1E5A8A")
    ws.append([])
    ws.append(header)
    for c in ws[3]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="14283C")
    for row in data:
        ws.append(list(row))

wb2 = openpyxl.Workbook()

s = wb2.active
s.title = "Inputs"
sheet(s, "Input parameters", ["Item", "Value", "Unit", "Formula / Source"],
[
 ("Nominal cell capacity", 5.0, "Ah", "Chen2020 dump 'Nominal cell capacity [A.h]'"),
 ("Voltage window", "2.5 - 4.2", "V", "Chen2020 dump lower/upper cut-off; overcharge = 4.2 + 0.5 = 4.7 V (task spec match)"),
 ("Electrode area", 0.1027, "m2", "0.065 m x 1.58 m (Chen2020 dump height/width)"),
 ("Positive thickness", 75.6e-6, "m", "Chen2020 dump"),
 ("Positive porosity / active fraction", "0.335 / 0.665", "-", "Chen2020 dump"),
 ("Negative thickness", 95e-6, "m", "override (r6_c7_params.json), base 85.2e-6"),
 ("Negative porosity / active fraction", "0.25 / 0.75", "-", "Chen2020 dump"),
 ("Separator thickness / porosity", "12e-6 / 0.47", "m / -", "Chen2020 dump"),
 ("Positive CC (Al) thickness / density", "16e-6 / 2700", "m / kg.m-3", "Chen2020 dump"),
 ("Negative CC (Cu) thickness / density", "12e-6 / 8960", "m / kg.m-3", "Chen2020 dump"),
 ("c_max positive / negative", "63104 / 33133", "mol.m-3", "Chen2020 dump"),
 ("Initial lithiation pos / neg", "0.270 / 0.901", "-", "Chen2020 dump (17038/63104, 29866/33133)"),
 ("Positive particle radius", 1.2e-6, "m", "override (single-crystal NMC811)"),
 ("Negative particle radius", 0.8e-6, "m", "override (fine graphite)"),
 ("Electrolyte conductivity / diffusivity / t+", "1.8 / 5e-10 / 0.5", "S/m / m2/s / -", "overrides (formulation-bridge estimates)"),
 ("Cooling h / A", "25 / 0.2054", "W/m2K / m2", "overrides (pouch double-face cold plate)"),
])

s = wb2.create_sheet("CapacityEnergy")
sheet(s, "Capacity and energy", ["Item", "Value", "Unit", "Formula / Source"],
[
 ("1C discharge capacity", 5.654, "Ah", "r6_c7_1c_spme.json:capacity_ah (1C CC 25 C to 2.5 V)"),
 ("Discharge energy", 20.472, "Wh", "r6_c7_energy.json:energy_wh = integral V x I_1C dt (I_1C = 5 A)"),
 ("Midpoint voltage", 4.1146, "V", "r6_c7_energy.json:midpoint_voltage_v"),
 ("DC resistance (contract)", 4.029e-5, "Ohm", "r6_c7_energy.json:dcr_ohm = (V_start - V@10%) / I_1C"),
 ("Power density (contract)", 2.376e6, "W/kg", "r6_c7_energy.json:power_density_w_kg = V_OC^2/(4 DCR)/mass"),
 ("4C CC charge capacity (true)", 4.630, "Ah", "r6_c7_4c.json:capacity_ah x 5.0 (nominal-capacity factor; runner reports duration x C_rate/3600)"),
 ("4C CC charge acceptance", 81.9, "% SOC", "4.630 / 5.654; duration ~836 s at 20 A (4C x 5 Ah)"),
 ("4C charge T_max @45 C", 318.79, "K", "r6_c7_4c.json:T_max_K (lumped thermal)"),
 ("4C anode potential min", "+0.00824 / +0.00515", "V", "r6_c7_4c.json (SPMe) / r6_c7_4c_dfn.json (DFN) anode_potential_v"),
 ("Overcharge 4.7 V T_max", 298.22, "K", "r6_c7_oc.json:T_max_K"),
 ("Thermal runaway triggered", "false", "-", "validation/r6_c7_tr.json:triggered"),
])

s = wb2.create_sheet("EnergyDensity")
sheet(s, "Energy density", ["Item", "Value", "Unit", "Formula / Source"],
[
 ("Discharge energy", 20.472, "Wh", "r6_c7_energy.json:energy_wh"),
 ("Contract mass (electrolyte excluded)", 44.705, "g", "r6_c7_energy.json:mass_kg = SUM thickness x (1-porosity) x density x area"),
 ("Gravimetric energy density", 457.93, "Wh/kg", "20.4719 Wh / 0.044705 kg (r6_c7_energy.json:energy_density_wh_kg)"),
 ("Stack volume", 2.1629e-5, "m3", "r6_c7_energy.json:volume_m3 = thickness 210.6 um x area"),
 ("Volumetric energy density", 946.52, "Wh/L", "r6_c7_energy.json:energy_density_wh_l"),
 ("Electrolyte in mass/volume", "excluded", "-", "r6_c7_energy.json:electrolyte_included = false (parameter set lacks density)"),
 ("Criterion check", "457.93 >= 392.61", "Wh/kg", "PASS, margin +65.3 (log-evaluate R6)"),
])

s = wb2.create_sheet("NPMass")
sheet(s, "N/P and mass", ["Item", "Value", "Unit", "Formula / Source"],
[
 ("Positive layer mass", 0.163994, "kg/m2", "r6_c7_energy.json:layer_kg_m2.positive_electrode"),
 ("Negative layer mass", 0.118061, "kg/m2", "r6_c7_energy.json:layer_kg_m2.negative_electrode"),
 ("Positive CC (Al) mass", 0.043200, "kg/m2", "r6_c7_energy.json:layer_kg_m2.positive_cc"),
 ("Negative CC (Cu) mass", 0.107520, "kg/m2", "r6_c7_energy.json:layer_kg_m2.negative_cc"),
 ("Separator mass", 0.002525, "kg/m2", "r6_c7_energy.json:layer_kg_m2.separator"),
 ("Negative capacity density", 63.280, "Ah/m2", "33133 x 0.75 x 96485/3600 x 95e-6 (c_max x eps x F/3600 x thickness)"),
 ("Positive capacity density", 85.020, "Ah/m2", "63104 x 0.665 x 96485/3600 x 75.6e-6"),
 ("N/P ratio (capacity basis)", 0.744, "-", "63.280 / 85.020; anode-limited parameterization (R4 evidence: 1C capacity tracks anode inventory)"),
 ("Measured 1C capacity", 5.654, "Ah", "r6_c7_1c_spme.json:capacity_ah"),
])

s = wb2.create_sheet("Process")
sheet(s, "Process parameters", ["Item", "Value", "Unit", "Formula / Source"],
[
 ("Positive areal density", 163.99, "g/m2", "thickness x (1-porosity) x density = layer_kg_m2 x 1000"),
 ("Negative areal density", 118.06, "g/m2", "same formula, negative layer"),
 ("Positive compaction density", 2.169, "g/cm3", "areal density / thickness (163.99 g/m2 / 75.6 um)"),
 ("Negative compaction density", 1.243, "g/cm3", "118.06 g/m2 / 95 um"),
 ("Electrolyte fill amount", 6.74, "g/cell", "pore volume 5.6193e-6 m3 x 1.2 g/cm3 (literature density) x fill factor 1.0"),
 ("Formation recommendation", "0.1C CC to 4.2 V, 25 C, 2 cycles", "-", "design recommended value; production-line value requires tuning"),
])
for name, width in zip(("A", "B", "C", "D"), (34, 22, 12, 96)):
    for s in wb2.worksheets:
        s.column_dimensions[name].width = width
calc_path = D / "calc.xlsx"
wb2.save(calc_path)

# ---------------- PDF releases ----------------
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

BLUE_D = colors.HexColor("#14283C")
BLUE_M = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")

REPL = {"\u2265": ">=", "\u2264": "<=", "\u2248": "~", "\u2192": "->", "\u21D2": "=>",
        "\u226A": "<<", "\u222B": "S", "\u03A3": "SUM", "\u03C3": "sigma", "\u03C4": "tau",
        "\u03B5": "eps", "\u207A": "+", "\u2713": "[PASS]", "\u2212": "-", "\u00D7": "x"}
def san(txt):
    return "".join(REPL.get(ch, ch) for ch in txt)

def md_to_pdf(md_path, pdf_path, subtitle):
    styles = getSampleStyleSheet()
    title = styles["Title"]
    title.textColor = colors.white
    h2 = styles["Heading2"]
    h2.textColor = BLUE_M
    body = styles["BodyText"]
    body.fontSize = 8.5
    body.leading = 11
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=12 * mm, rightMargin=12 * mm, topMargin=14 * mm, bottomMargin=12 * mm)
    story = []
    lines = md_path.read_text(encoding="utf-8").splitlines()
    main_title = lines[0].lstrip("# ").strip() if lines else pdf_path.stem
    story.append(Paragraph(san(main_title), title))
    story.append(Paragraph(san(subtitle), h2))
    story.append(Spacer(1, 2 * mm))
    tbl = Table([[""]], colWidths=[185 * mm], rowHeights=[1.2 * mm])
    tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), COPPER)]))
    story.append(tbl)
    story.append(Spacer(1, 3 * mm))
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# "):
            i += 1
            continue
        if line.startswith("## "):
            story.append(Paragraph(san(line[3:]), h2))
            story.append(Spacer(1, 1 * mm))
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [san(c.strip()) for c in lines[i].strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                ncol = max(len(r) for r in rows)
                rows = [r + [""] * (ncol - len(r)) for r in rows]
                widths = [max(len(r[c]) for r in rows) for c in range(ncol)]
                tot = sum(widths) or 1
                widths = [max(18 * mm, w / tot * 182 * mm) for w in widths]
                t = Table(rows, colWidths=widths, repeatRows=1)
                t.setStyle(TableStyle([
                    ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.5),
                    ("FONT", (0, 1), (-1, -1), "Helvetica", 7),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("BACKGROUND", (0, 0), (-1, 0), BLUE_D),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.93, 0.95, 0.97)]),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.7, 0.75, 0.8)),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]))
                story.append(t)
                story.append(Spacer(1, 2.5 * mm))
            continue
        if line.startswith("- "):
            story.append(Paragraph("&#8226; " + san(line[2:]), body))
            i += 1
            continue
        if line.strip():
            story.append(Paragraph(san(line), body))
        i += 1
    doc.build(story)

def xlsx_to_pdf(xlsx_path, pdf_path, subtitle):
    import openpyxl as op
    styles = getSampleStyleSheet()
    title = styles["Title"]
    title.textColor = colors.white
    body = styles["BodyText"]
    body.fontSize = 8
    body.leading = 10.5
    wb = op.load_workbook(xlsx_path)
    story = []
    story.append(Paragraph(san(xlsx_path.stem.upper() + " (PDF release)"), title))
    story.append(Paragraph(san(subtitle), styles["Heading2"]))
    story.append(Spacer(1, 3 * mm))
    for sname in wb.sheetnames:
        s = wb[sname]
        story.append(Paragraph(san(sname), styles["Heading2"]))
        rows = [[san(str(c.value)) if c.value is not None else "" for c in row] for row in s.iter_rows()]
        rows = [r for r in rows if any(r)]
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        widths = [max(len(r[c]) for r in rows) for c in range(ncol)]
        tot = sum(widths) or 1
        widths = [max(20 * mm, w / tot * 180 * mm) for w in widths]
        t = Table(rows, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.5),
            ("FONT", (0, 1), (-1, -1), "Helvetica", 6.8),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 0), (-1, 0), BLUE_D),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.93, 0.95, 0.97)]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.7, 0.75, 0.8)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t)
        story.append(Spacer(1, 3 * mm))
    SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=12 * mm, rightMargin=12 * mm,
                      topMargin=14 * mm, bottomMargin=12 * mm).build(story)

for name, sub in [
    ("design_spec", "VBF-T1R1NOFORCE-DS-01 - Cell Design Specification, virtual design"),
    ("datasheet", "VBF-T1R1NOFORCE-DSH-01 - Technical Datasheet"),
    ("dvpr", "VBF-T1R1NOFORCE-DVPR-01 - Design Verification Plan and Report (virtual-test version)"),
    ("dfmea", "VBF-T1R1NOFORCE-DFMEA-01 - Design FMEA (qualitative version)"),
    ("delivery_index", "VBF-T1R1NOFORCE-IDX-01 - Delivery Package Index"),
]:
    md_to_pdf(D / f"{name}.md", D / f"{name}.pdf", sub)

xlsx_to_pdf(bom_path, D / "bom.pdf", "VBF-T1R1NOFORCE-BOM-01 - Bill of Materials (g/cell and kg/kWh)")
xlsx_to_pdf(calc_path, D / "calc.pdf", "VBF-T1R1NOFORCE-CALC-01 - Design Calculation Sheet")

print("deliverables built:")
for p in sorted(D.iterdir()):
    print(f"  {p.name}  {p.stat().st_size} B")
