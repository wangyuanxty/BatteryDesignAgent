import datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

DEL = Path("runs/portability/t1_lc/deliverables")
DEL.mkdir(parents=True, exist_ok=True)

CASE_ID = "T1LC"
DATE = "2026-08-26"
DEEP = colors.HexColor("#14283C")
MID = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")


def sanitize(s: str) -> str:
    return (
        s.replace("≥", ">=").replace("≤", "<=").replace("✓", "[PASS]")
        .replace("✗", "[FAIL]").replace("→", "->").replace("°", " deg ")
        .replace("µm", "um").replace("μ", "u").replace("÷", "/")
        .replace("×", "x").replace("⁺", "+").replace("≈", "~").replace("−", "-")
    )


def pdf_from_lines(path: str, number: str, title: str, lines: list[str]):
    doc = SimpleDocTemplate(str(DEL / path), pagesize=A4,
                            leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=16*mm, bottomMargin=16*mm)
    styles = getSampleStyleSheet()
    h1 = styles["Title"]
    h1.textColor = colors.white
    h1.fontSize = 15
    h2 = styles["Heading2"]
    h2.textColor = MID
    body = styles["BodyText"]
    body.fontSize = 8.5
    body.leading = 11
    story = []
    # cover header
    header = Table(
        [[Paragraph(f'<font color="white"><b>{sanitize(number)}</b><br/>{sanitize(title)}</font>', h1)]],
        colWidths=[174*mm],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DEEP),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(header)
    story.append(Spacer(1, 4*mm))
    meta = Table(
        [[Paragraph(f'<b>Case:</b> t1_lc &nbsp;|&nbsp; <b>Date:</b> {DATE}', body)],
         [Paragraph(f'<b>Prepared:</b> __________ &nbsp; <b>Reviewed:</b> __________ &nbsp; <b>Approved:</b> __________', body)]],
        colWidths=[174*mm],
    )
    meta.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, MID),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(meta)
    story.append(Spacer(1, 3*mm))
    for ln in lines:
        s = sanitize(ln.rstrip("\n"))
        if not s.strip():
            story.append(Spacer(1, 2))
        elif s.startswith("# "):
            story.append(Paragraph(f"<b>{s[2:]}</b>", h2))
        elif s.startswith("## "):
            story.append(Paragraph(f"<b>{s[3:]}</b>", h2))
        else:
            story.append(Paragraph(s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), body))
    doc.build(story)


# ---- BOM xlsx ----
energy_wh = 17.947732073851554
energy_kwh = energy_wh / 1000.0

bom_rows = [
    ("Component", "Mass (g/cell)", "kg/kWh", "Source / note"),
    ("Positive electrode active (NMC811)", 16.842, 0.016842/energy_kwh, "mechanical: t x area x (1-eps) x density"),
    ("Positive conductive additive (carbon black)", 0.351, 0.000351/energy_kwh, "literature default ~2 wt% (estimate)"),
    ("Positive binder (PVDF)", 0.351, 0.000351/energy_kwh, "literature default ~2 wt% (estimate)"),
    ("Negative electrode active (graphite)", 10.874, 0.010874/energy_kwh, "mechanical"),
    ("Negative conductive additive (carbon black)", 0.112, 0.000112/energy_kwh, "literature default ~1 wt% (estimate)"),
    ("Negative binder (CMC/SBR)", 0.224, 0.000224/energy_kwh, "literature default ~2 wt% (estimate)"),
    ("Separator (polyolefin)", 0.259, 0.000259/energy_kwh, "mechanical"),
    ("Electrolyte (EC/EMC + LiPF6)", 5.797, 0.005797/energy_kwh, "pore vol 5.37 cm3 x 1.2 g/cm3 x 0.9 fill (estimate)"),
    ("Positive current collector (Al)", 4.437, 0.004437/energy_kwh, "mechanical"),
    ("Negative current collector (Cu)", 11.042, 0.011042/energy_kwh, "mechanical"),
    ("Enclosure / tabs", "Not modeled", "Not modeled", "beyond parameter set"),
    ("Total (contract caliber, excl. electrolyte)", 43.45, 0.04345/energy_kwh, "cell/r3_V3_energy.json:mass_kg"),
    ("Total incl. electrolyte (estimate)", 49.25, 0.04925/energy_kwh, "contract mass + electrolyte estimate"),
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
for r in bom_rows:
    ws.append(list(r))
ws["A1"].font = Font(bold=True)
ws["B1"].font = Font(bold=True)
ws["C1"].font = Font(bold=True)
ws["D1"].font = Font(bold=True)
for col, w in zip("ABCD", (46, 16, 12, 52)):
    ws.column_dimensions[col].width = w
wb.save(str(DEL / "bom.xlsx"))

# ---- calc.xlsx ----
wb2 = openpyxl.Workbook()

ws_in = wb2.active
ws_in.title = "input_parameters"
ws_in.append(["Parameter", "Value", "Unit", "Source"])
inputs = [
    ("Electrode height", 0.065, "m", "Chen2020"),
    ("Electrode width", 1.58, "m", "Chen2020"),
    ("Positive electrode thickness", 75.6e-6, "m", "Chen2020"),
    ("Negative electrode thickness", 85.2e-6, "m", "Chen2020"),
    ("Separator thickness", 12e-6, "m", "Chen2020"),
    ("Positive current collector thickness", 16e-6, "m", "Chen2020"),
    ("Negative current collector thickness", 12e-6, "m", "Chen2020"),
    ("Positive electrode porosity", 0.335, "-", "Chen2020"),
    ("Negative electrode porosity", 0.25, "-", "Chen2020"),
    ("Separator porosity", 0.47, "-", "Chen2020"),
    ("Positive electrode density", 3262, "kg/m3", "Chen2020"),
    ("Negative electrode density", 1657, "kg/m3", "Chen2020"),
    ("Separator density", 397, "kg/m3", "Chen2020"),
    ("Positive CC density (Al)", 2700, "kg/m3", "Chen2020"),
    ("Negative CC density (Cu)", 8960, "kg/m3", "Chen2020"),
    ("Nominal cell capacity", 5.0, "Ah", "Chen2020"),
    ("Upper voltage cut-off", 4.2, "V", "Chen2020"),
    ("Lower voltage cut-off", 2.5, "V", "Chen2020"),
    ("Electrolyte conductivity (override)", 2.5, "S/m", "formulation estimate"),
    ("Cation transference number (override)", 0.6, "-", "formulation estimate"),
    ("Electrolyte diffusivity (override)", 4.0e-10, "m2/s", "formulation estimate"),
    ("Negative particle radius (override)", 3.0e-6, "m", "design"),
    ("Total heat transfer coefficient (override)", 60.0, "W/m2/K", "design (liquid cooling)"),
]
for r in inputs:
    ws_in.append(list(r))
for col, w in zip("ABCD", (42, 14, 10, 24)):
    ws_in.column_dimensions[col].width = w

ws_cap = wb2.create_sheet("capacity_energy")
ws_cap.append(["Quantity", "Value", "Unit", "Source"])
ws_cap.append(["1C discharge capacity", 5.029950574, "Ah", "cell/r3_V3_1c_dfn.json"])
ws_cap.append(["Discharge energy", 17.947732074, "Wh", "cell/r3_V3_energy.json:energy_wh"])
ws_cap.append(["Midpoint voltage", 3.823581498, "V", "cell/r3_V3_energy.json"])
ws_cap.append(["DC resistance", 0.003382564, "ohm", "cell/r3_V3_energy.json"])
for col, w in zip("ABCD", (30, 16, 8, 40)):
    ws_cap.column_dimensions[col].width = w

ws_ed = wb2.create_sheet("energy_density")
ws_ed.append(["Quantity", "Value", "Unit", "Source"])
ws_ed.append(["Cell mass (contract)", 0.043454528, "kg", "cell/r3_V3_energy.json:mass_kg"])
ws_ed.append(["Gravimetric energy density", 413.023293, "Wh/kg", "cell/r3_V3_energy.json"])
ws_ed.append(["Volumetric energy density", 870.312910, "Wh/L", "cell/r3_V3_energy.json"])
ws_ed.append(["Total layer thickness", 200.8e-6, "m", "cell/r3_V3_energy.json"])
for col, w in zip("ABCD", (30, 16, 8, 40)):
    ws_ed.column_dimensions[col].width = w

ws_np = wb2.create_sheet("NP_mass")
ws_np.append(["Layer", "kg/m2", "g/cell", "Source"])
layers = [
    ("Positive electrode", 0.163993788, 16.842, "cell/r3_V3_energy.json:layer_kg_m2"),
    ("Negative electrode", 0.105882300, 10.874, "same"),
    ("Positive current collector", 0.043200000, 4.437, "same"),
    ("Negative current collector", 0.107520000, 11.042, "same"),
    ("Separator", 0.002524920, 0.259, "same"),
    ("Total", 0.423121008, 43.45, "sum"),
]
for r in layers:
    ws_np.append(list(r))
ws_np.append([])
ws_np.append(["N/P ratio", 0.667, "-", "(33133*0.75*85.2e-6)/(63104*0.665*75.6e-6)"])
for col, w in zip("ABCD", (30, 16, 10, 44)):
    ws_np.column_dimensions[col].width = w

ws_pr = wb2.create_sheet("process_parameters")
ws_pr.append(["Parameter", "Formula", "Value", "Unit", "Source"])
proc = [
    ("Positive areal density", "t x (1-eps) x rho", 163.99, "g/m2", "75.6e-6*0.665*3262"),
    ("Negative areal density", "t x (1-eps) x rho", 105.88, "g/m2", "85.2e-6*0.75*1657"),
    ("Positive compaction density", "rho x (1-eps)", 2.169, "g/cm3", "3262*0.665/1000"),
    ("Negative compaction density", "rho x (1-eps)", 1.243, "g/cm3", "1657*0.75/1000"),
    ("Electrolyte fill amount", "pore vol x 1.2 x 0.9", 5.80, "g", "pore vol 5.37 cm3, estimate"),
    ("Formation recommendation", "0.1C CC to 4.2V, 25C, 2 cycles", "", "", "design recommended"),
]
for r in proc:
    ws_pr.append(list(r))
for col, w in zip("ABCDE", (30, 26, 10, 8, 30)):
    ws_pr.column_dimensions[col].width = w

wb2.save(str(DEL / "calc.xlsx"))

# ---- PDFs from markdown ----
for fname, num, title in [
    ("design_spec.md", "VBF-T1LC-DS-01", "Cell Design Specification"),
    ("datasheet.md", "VBF-T1LC-DSH-01", "Technical Datasheet"),
    ("dvpr.md", "VBF-T1LC-DVPR-01", "Design Verification Plan & Report"),
    ("dfmea.md", "VBF-T1LC-DFMEA-01", "Design FMEA (qualitative)"),
]:
    lines = (DEL / fname).read_text(encoding="utf-8").splitlines()
    pdf_from_lines(fname.replace(".md", ".pdf"), num, title, lines)

# ---- BOM PDF ----
bom_lines = ["# Bill of Materials", "", "Dual caliber: g/cell and kg/kWh. Energy = 17.948 Wh (0.01795 kWh).", ""]
bom_lines += [" | ".join(map(str, r)) for r in bom_rows]
pdf_from_lines("bom.pdf", "VBF-T1LC-BOM-01", "Bill of Materials", bom_lines)

# ---- CALC PDF ----
calc_lines = ["# Design Calculation Sheet", "", "Contract formula: ED = discharge energy / layer mass; mass = sum(thickness x area x (1-porosity) x density).", ""]
calc_lines += ["[input_parameters]", "Parameter | Value | Unit | Source"]
calc_lines += [" | ".join(map(str, r)) for r in inputs]
calc_lines += ["", "[capacity_energy]", "Quantity | Value | Unit | Source"]
calc_lines += ["1C discharge capacity | 5.029950574 | Ah | cell/r3_V3_1c_dfn.json"]
calc_lines += ["Discharge energy | 17.947732074 | Wh | cell/r3_V3_energy.json"]
calc_lines += ["Midpoint voltage | 3.823581498 | V | cell/r3_V3_energy.json"]
calc_lines += ["DC resistance | 0.003382564 | ohm | cell/r3_V3_energy.json"]
calc_lines += ["", "[energy_density]", "Cell mass | 0.043454528 | kg | cell/r3_V3_energy.json"]
calc_lines += ["Gravimetric ED | 413.023293 | Wh/kg | cell/r3_V3_energy.json"]
calc_lines += ["Volumetric ED | 870.312910 | Wh/L | cell/r3_V3_energy.json"]
calc_lines += ["", "[N/P and mass]", "Layer | kg/m2 | g/cell | Source"]
calc_lines += [" | ".join(map(str, r)) for r in layers]
calc_lines += ["N/P ratio | 0.667 | - | (33133*0.75*85.2e-6)/(63104*0.665*75.6e-6)"]
pdf_from_lines("calc.pdf", "VBF-T1LC-CALC-01", "Design Calculation Sheet", calc_lines)

print("deliverables generated in", DEL)
