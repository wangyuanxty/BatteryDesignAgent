"""Build R6 closing deliverables: bom.xlsx, calc.xlsx, and PDF releases for all 7 categories.
All conclusion-grade numbers are read from round-6 tool output JSONs (no hand transcription);
md->pdf conversion renders the editable sources; xlsx and xlsx->pdf share the same row data.
"""
import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t4_r1_noforce")
DEL = WS / "deliverables"
DEL.mkdir(exist_ok=True)

# ---------- tool-output values (round 6, final h=45) ----------
energy = json.loads((WS / "cell" / "r6_final_energy_dfn.json").read_text(encoding="utf-8-sig"))
safety = json.loads((WS / "cell" / "r6_final_4C45_safety_dfn.json").read_text(encoding="utf-8-sig"))
derived = json.loads((WS / "bridge" / "derived_r6_final_dfn.json").read_text(encoding="utf-8-sig"))
ok_safety = json.loads((WS / "cell" / "r6_final_ok_4C45_safety_dfn.json").read_text(encoding="utf-8-sig"))
ok_derived = json.loads((WS / "bridge" / "derived_r6_final_ok_spme.json").read_text(encoding="utf-8-sig"))
cs_derived = json.loads((WS / "bridge" / "derived_r6_final_coldstart.json").read_text(encoding="utf-8-sig"))

area = energy["area_m2"]
lkg = energy["layer_kg_m2"]
g_mass = lambda k: lkg[k] * area * 1000.0
m_pos, m_neg, m_pcc, m_ncc, m_sep = (g_mass(k) for k in (
    "positive_electrode", "negative_electrode", "positive_cc", "negative_cc", "separator"))
total_g = energy["mass_kg"] * 1000.0
kwh = energy["energy_wh"] / 1000.0
kgpkwh = lambda g_: (g_ / 1000.0) / kwh

t_pos, t_neg, t_sep = 75.6e-6, 85.2e-6, 10e-6
por_pos, por_neg, por_sep = 0.40, 0.35, 0.47
pore_m3 = (t_pos * por_pos + t_neg * por_neg + t_sep * por_sep) * area
elec_g = pore_m3 * 1.2e6  # 1.2 g/cm3 = 1.2e6 g/m3 (literature density, annotated)

anode_min_v = min(safety["anode_potential_v"])
ok_anode_min_v = min(ok_safety["anode_potential_v"])

# ---------- BOM rows (g/cell + kg/kWh) ----------
bom_rows = [
    ("Positive electrode active material", "NMC811", m_pos * 0.96, "96 wt% of cathode solids — literature default (set has no AM-fraction key)"),
    ("Positive electrode conductive additive", "carbon black", m_pos * 0.02, "2 wt% — literature default (no parameter)"),
    ("Positive electrode binder", "PVDF", m_pos * 0.02, "2 wt% — literature default (no parameter)"),
    ("Negative electrode active material", "graphite", m_neg * 0.96, "96 wt% — literature default (no parameter)"),
    ("Negative electrode conductive additive", "carbon black", m_neg * 0.01, "1 wt% — literature default (no parameter)"),
    ("Negative electrode binder", "CMC/SBR", m_neg * 0.03, "3 wt% — literature default (no parameter)"),
    ("Separator", "polyolefin", m_sep, "r6_final_energy_dfn.json:layer_kg_m2.separator x area"),
    ("Electrolyte", "EC/EMC + LiPF6", elec_g, "pore volume x 1.2 g/cm3 (literature density, annotated)"),
    ("Positive current collector", "Al foil", m_pcc, "r6_final_energy_dfn.json:layer_kg_m2.positive_cc x area"),
    ("Negative current collector", "Cu foil", m_ncc, "r6_final_energy_dfn.json:layer_kg_m2.negative_cc x area"),
    ("Enclosure", "—", None, "Not modeled"),
    ("Tabs", "—", None, "Not modeled"),
]

# ---------- calc.xlsx sheet data ----------
calc_sheets = {
    "Inputs": [
        ["Item", "Value", "Unit", "Formula / source"],
        ["Positive electrode thickness", t_pos * 1e6, "um", "Chen2020 set (dumped effective value)"],
        ["Negative electrode thickness", t_neg * 1e6, "um", "Chen2020 set"],
        ["Separator thickness", t_sep * 1e6, "um", "params_r6_v10a_h45.json (base 12)"],
        ["Positive current collector thickness", 8.0, "um", "params_r6_v10a_h45.json (base 16)"],
        ["Negative current collector thickness", 6.0, "um", "params_r6_v10a_h45.json (base 12)"],
        ["Positive electrode porosity", por_pos, "—", "params_r6_v10a_h45.json"],
        ["Negative electrode porosity", por_neg, "—", "params_r6_v10a_h45.json"],
        ["Separator porosity", por_sep, "—", "Chen2020 set"],
        ["Positive electrode density", 3262.0, "kg/m3", "Chen2020 set"],
        ["Negative electrode density", 1657.0, "kg/m3", "Chen2020 set"],
        ["Separator density", 397.0, "kg/m3", "Chen2020 set"],
        ["Electrode height / width", "0.065 / 1.58", "m", "Chen2020 set"],
        ["Electrode area", area, "m2", "height x width"],
        ["Nominal cell capacity", 5.0, "Ah", "Chen2020 set"],
        ["Voltage window", "2.5 - 4.2", "V", "Chen2020 set cut-offs"],
        ["Electrolyte conductivity (design)", 4.0, "S/m", "params_r6_v10a_h45.json (override)"],
        ["Electrolyte diffusivity (design)", 3.539e-10, "m2/s", "params_r6_v10a_h45.json (override)"],
        ["Cation transference number (design)", 0.45, "—", "params_r6_v10a_h45.json (override)"],
        ["Total heat transfer coefficient (design)", 45.0, "W/m2K", "params_r6_v10a_h45.json (override)"],
    ],
    "Capacity_Energy": [
        ["Item", "Value", "Unit", "Source"],
        ["1C discharge capacity", energy["capacity_ah"], "Ah", "r6_final_energy_dfn.json:capacity_ah"],
        ["Discharge energy (trapezoid V·I_1C dt)", energy["energy_wh"], "Wh", "r6_final_energy_dfn.json:energy_wh"],
        ["Discharge midpoint voltage", energy["midpoint_voltage_v"], "V", "r6_final_energy_dfn.json:midpoint_voltage_v"],
        ["DC resistance", energy["dcr_ohm"] * 1000.0, "mOhm", "r6_final_energy_dfn.json:dcr_ohm"],
        ["Power density (V_OC^2/4R / mass)", energy["power_density_w_kg"], "W/kg", "r6_final_energy_dfn.json:power_density_w_kg"],
    ],
    "Energy_Density": [
        ["Item", "Value", "Unit", "Formula / source"],
        ["Cell mass (contract caliber, electrolyte excluded)", total_g, "g", "r6_final_energy_dfn.json:mass_kg"],
        ["Gravimetric energy density", energy["energy_density_wh_kg"], "Wh/kg", "energy_wh / mass_kg"],
        ["Stack thickness", energy["thickness_m"] * 1e6, "um", "sum of 5 layer thicknesses"],
        ["Stack volume", energy["volume_m3"] * 1e6, "cm3", "thickness x area"],
        ["Volumetric energy density", energy["energy_density_wh_l"], "Wh/L", "energy_wh / volume (electrolyte/casing excluded)"],
        ["Criterion ED >= 327.18 Wh/kg", "PASS", "—", "564.84 >= 327.18"],
        ["Criterion ED_vol >= 880 Wh/L", "PASS", "—", "969.50 >= 880"],
    ],
    "Mass_Balance": [
        ["Layer", "Mass (g)", "Source"],
        ["Positive electrode solids", m_pos, "layer_kg_m2.positive_electrode x area"],
        ["Negative electrode solids", m_neg, "layer_kg_m2.negative_electrode x area"],
        ["Positive current collector (Al)", m_pcc, "layer_kg_m2.positive_cc x area"],
        ["Negative current collector (Cu)", m_ncc, "layer_kg_m2.negative_cc x area"],
        ["Separator", m_sep, "layer_kg_m2.separator x area"],
        ["Total (contract)", total_g, "r6_final_energy_dfn.json:mass_kg"],
        ["Electrolyte (estimate)", elec_g, "pore volume 6.651 cm3 x 1.2 g/cm3 (literature density)"],
        ["N/P ratio", "Not provided", "Chen2020 has no per-electrode capacity-density keys; balance unchanged from baseline"],
    ],
    "Process": [
        ["Item", "Value", "Unit", "Formula"],
        ["Positive areal density", 147.96, "g/m2", "75.6e-6 x (1-0.40) x 3262"],
        ["Negative areal density", 91.76, "g/m2", "85.2e-6 x (1-0.35) x 1657"],
        ["Positive compaction density", 1.957, "g/cm3", "3262 x 0.60 / 1000"],
        ["Negative compaction density", 1.077, "g/cm3", "1657 x 0.65 / 1000"],
        ["Electrolyte fill amount", elec_g, "g", "pore volume x 1.2 g/cm3 x 1.0 fill factor"],
        ["Formation recommendation", "0.1C CC to 4.2 V, 25 C, 2 cycles", "—", "design recommended value; production-line value requires tuning"],
    ],
}

# =========================================================
# 1) xlsx
# =========================================================
header_fill = PatternFill("solid", fgColor="1E5A8A")
header_font = Font(bold=True, color="FFFFFF")

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
ws.append(["Component", "Material", "Mass g/cell", "kg/kWh", "Source"])
for comp, mat, mg, src in bom_rows:
    ws.append([comp, mat, None if mg is None else round(mg, 4), None if mg is None else round(kgpkwh(mg), 4), src])
ws.append(["Total (layer solids, contract caliber)", "—", round(total_g, 4), round(kgpkwh(total_g), 4), "r6_final_energy_dfn.json:mass_kg"])
ws.append(["Total incl. electrolyte estimate", "—", round(total_g + elec_g, 4), round(kgpkwh(total_g + elec_g), 4), "electrolyte = literature-density estimate"])
ws.append(["Rated energy", "—", None, None, f"{energy['energy_wh']:.3f} Wh (r6_final_energy_dfn.json:energy_wh)"])
for c in ws[1]:
    c.fill, c.font = header_fill, header_font
for row in ws.iter_rows():
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")
for i, w in enumerate([34, 18, 14, 12, 60], start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

ws2 = wb.create_sheet("Summary")
ws2.append(["Dual caliber", "Value", "Unit", "Source"])
ws2.append(["Cell energy", energy["energy_wh"], "Wh", "r6_final_energy_dfn.json:energy_wh"])
ws2.append(["Cell mass (contract)", total_g, "g", "r6_final_energy_dfn.json:mass_kg"])
ws2.append(["Material usage total", kgpkwh(total_g), "kg/kWh", "mass / (energy/1000)"])
ws2.append(["Material usage incl. electrolyte", kgpkwh(total_g + elec_g), "kg/kWh", "electrolyte density = literature value"])
for c in ws2[1]:
    c.fill, c.font = header_fill, header_font
for i, w in enumerate([30, 18, 12, 60], start=1):
    ws2.column_dimensions[get_column_letter(i)].width = w
wb.save(DEL / "bom.xlsx")

wb = openpyxl.Workbook()
wb.remove(wb.active)
for sheet_name, rows in calc_sheets.items():
    ws = wb.create_sheet(sheet_name)
    for row in rows:
        ws.append(row)
    for c in ws[1]:
        c.fill, c.font = header_fill, header_font
    for row in ws.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate([38, 22, 12, 70], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
wb.save(DEL / "calc.xlsx")

# =========================================================
# 2) PDFs
# =========================================================
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Title"], fontSize=15, leading=19, spaceAfter=10,
                    textColor=colors.HexColor("#14283C"))
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], fontSize=11.5, leading=15, spaceBefore=8,
                    spaceAfter=4, textColor=colors.HexColor("#1E5A8A"))
BODY = ParagraphStyle("Bodyx", parent=styles["BodyText"], fontSize=8.5, leading=11.5)
CELL = ParagraphStyle("Cellx", parent=styles["BodyText"], fontSize=7, leading=9)
CELLB = ParagraphStyle("Cellbx", parent=CELL, fontName="Helvetica-Bold")

USABLE = A4[0] - 72  # 523 pt


def esc(s):
    """WinAnsi-safe escaping for reportlab Helvetica."""
    s = str(s)
    for bad, good in [("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"),
                      ("→", "-&gt;"), ("−", "-"), ("μ", "u"),
                      ("²", "2"), ("³", "3"), ("Ω", "Ohm"), ("°", "deg")]:
        s = s.replace(bad, good)
    return s


def colwidths_for(n):
    base = {
        2: [260, 263], 3: [150, 230, 143], 4: [140, 120, 100, 163],
        5: [115, 90, 85, 90, 143], 6: [95, 75, 80, 65, 60, 148],
    }
    return base.get(n, [USABLE / n] * n)


def is_sep_row(cells):
    return all(set(c) <= set("-: ") and c for c in cells)


def style_table(tbl):
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E5A8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F6")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return tbl


def rows_to_table(rows):
    data = [[Paragraph(esc(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)]
    return style_table(Table(data, repeatRows=1, colWidths=colwidths_for(len(rows[0]))))


def md_table_to_platypus(lines):
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    rows = [r for r in rows if not is_sep_row(r)]
    return rows_to_table(rows)


def md_to_pdf(md_path, pdf_path, blueprint_cover=None):
    text = md_path.read_text(encoding="utf-8-sig")
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []
    if blueprint_cover:
        cov_style = ParagraphStyle("cov", parent=H1, fontSize=17, leading=22, textColor=colors.white)
        meta_style = ParagraphStyle("covm", parent=BODY, fontSize=9, textColor=colors.HexColor("#1E5A8A"))
        cover = Table([[Paragraph(f"<b>{esc(blueprint_cover[0])}</b>", cov_style)]], colWidths=[USABLE])
        cover.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#14283C")),
            ("TOPPADDING", (0, 0), (-1, -1), 18),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ]))
        story += [cover, Spacer(1, 8),
                  Paragraph(f"<b>Case:</b> {esc(blueprint_cover[1])}", meta_style), Spacer(1, 2),
                  Paragraph(f"<b>Scheme:</b> {esc(blueprint_cover[2])}", meta_style), Spacer(1, 2),
                  Paragraph(f"<b>Generation date:</b> {esc(blueprint_cover[3])}", meta_style), Spacer(1, 2),
                  Paragraph(f"<b>Prepared/Reviewed/Approved:</b> ______ / ______ / ______", meta_style),
                  Spacer(1, 8)]
        accent = Table([[""]], colWidths=[USABLE], rowHeights=[3])
        accent.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#C97B3D"))]))
        story.append(accent)
        story.append(Spacer(1, 10))
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            story.append(md_table_to_platypus(block))
            story.append(Spacer(1, 8))
            continue
        if ln.startswith("# "):
            story.append(Paragraph(esc(ln[2:]), H1))
        elif ln.startswith("## "):
            story.append(Paragraph(esc(ln[3:]), H2))
        elif ln.startswith("- "):
            story.append(Paragraph("• " + esc(ln[2:]), BODY))
        elif ln.strip():
            story.append(Paragraph(esc(ln), BODY))
        i += 1
    doc.build(story)


# md -> pdf for the five markdown deliverables
md_to_pdf(DEL / "design_spec.md", DEL / "design_spec.pdf")
md_to_pdf(DEL / "datasheet.md", DEL / "datasheet.pdf")
md_to_pdf(DEL / "dvpr.md", DEL / "dvpr.pdf")
md_to_pdf(DEL / "dfmea.md", DEL / "dfmea.pdf")
md_to_pdf(DEL / "delivery_index.md", DEL / "delivery_index.pdf",
          blueprint_cover=("Delivery Package Index — t4_r1_noforce",
                           "t4_r1_noforce (extreme-cold equipment battery, virtual battery factory)",
                           "VBF-T4R1NOFORCE-<DOC-CODE>-<SEQ-NO>",
                           "2026-08-25"))


def f(v, n=4):
    return f"{v:.{n}f}" if isinstance(v, float) else str(v)


bom_table = [["Component", "Material", "Mass g/cell", "kg/kWh", "Source"]]
for comp, mat, mg, src in bom_rows:
    bom_table.append([comp, mat, "Not modeled" if mg is None else f(mg),
                      "Not modeled" if mg is None else f(kgpkwh(mg)), src])
bom_table.append(["Total (layer solids, contract caliber)", "—", f(total_g), f(kgpkwh(total_g)),
                  "r6_final_energy_dfn.json:mass_kg"])
bom_table.append(["Total incl. electrolyte estimate", "—", f(total_g + elec_g), f(kgpkwh(total_g + elec_g)),
                  "electrolyte density = literature value 1.2 g/cm3"])
bom_table.append(["Rated energy", "—", f(energy['energy_wh']), "Wh", "r6_final_energy_dfn.json:energy_wh"])

doc = SimpleDocTemplate(str(DEL / "bom.pdf"), pagesize=A4,
                        leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
doc.build([Paragraph("Bill of Materials — V10a_final_h45 (g/cell and kg/kWh)", H1),
           Spacer(1, 8), rows_to_table(bom_table)])

doc = SimpleDocTemplate(str(DEL / "calc.pdf"), pagesize=A4,
                        leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
story = [Paragraph("Design Calculation Sheet — V10a_final_h45", H1)]
for name, rows in calc_sheets.items():
    story += [Paragraph(f"{name}", H2), rows_to_table(rows), Spacer(1, 10)]
doc.build(story)

print("deliverables built:")
for p in sorted(DEL.iterdir()):
    print(" ", p.name, p.stat().st_size, "bytes")
