# -*- coding: utf-8 -*-
"""
t4_r2 headless closing: one-off generator for deliverable binaries.
Produces in deliverables/:
  bom.xlsx, calc.xlsx, datasheet.docx (mirror of datasheet.md),
  7 release PDFs (design_spec, bom, datasheet, calc, dvpr, dfmea, delivery_index),
  delivery_index.md (written last; registers only files that exist).
All numbers are locked values already committed to sources (design_spec.md,
dvpr.md, dfmea.md, datasheet.md) and tool outputs under cell/.
"""
import os
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import docx as _docx_mod  # python-docx
from docx.shared import Pt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

from matplotlib import font_manager

HERE = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t4_r2"
DEL = os.path.join(HERE, "deliverables")

ENERGY_WH = 18.164749335
ENERGY_KWH = ENERGY_WH / 1000.0
AREA_M2 = 0.1027
CAPACITY_AH_1C = 5.039182551
CAPACITY_AH_LOWT = 5.007820865
RETENTION = CAPACITY_AH_LOWT / CAPACITY_AH_1C
MASS_G_NO_EL = 39.536159  # calc-energy mass_kg (electrolyte excluded)
VOL_L = 1.938976e-05 * 1000.0
GED = ENERGY_WH / (MASS_G_NO_EL / 1000.0)
VED = ENERGY_WH / VOL_L

LAYER_GM2 = {
    "pos": 0.177557184,
    "neg": 0.101647008,
    "al": 0.0324,
    "cu": 0.07168,
    "sep": 0.00168328,
}
G = {k: round(v * AREA_M2, 6) for k, v in LAYER_GM2.items()}
PORE_VOL_M3 = 5.0101168e-06
ELYTE_G = PORE_VOL_M3 * 1200.0  # 1.2 g/cm3 literature electrolyte density
POS_CON_NEG_RATIO = 2.0 / 96.0  # binder/conductive additive per active mass
TOTAL_G = sum(G.values()) + ELYTE_G

BOM_ROWS = [
    (1, "Positive active material", "NMC811-class, 3.5 um r, por 0.28", G["pos"], G["pos"] / 1000 / ENERGY_KWH,
     "calc-energy layer_kg_m2 x 0.1027 m2 (r5_E3_energy_dfn.json)"),
    (2, "Positive conductive additive", "carbon, 2 wt% of active (literature default, annotated)", G["pos"] * POS_CON_NEG_RATIO,
     G["pos"] * POS_CON_NEG_RATIO / 1000 / ENERGY_KWH, "96/2/2 split: parameter set has no additive keys"),
    (3, "Positive binder", "PVDF-class, 2 wt% of active (literature default, annotated)", G["pos"] * POS_CON_NEG_RATIO,
     G["pos"] * POS_CON_NEG_RATIO / 1000 / ENERGY_KWH, "96/2/2 split: parameter set has no binder keys"),
    (4, "Negative active material", "graphite-class, 3.0 um r, por 0.28", G["neg"], G["neg"] / 1000 / ENERGY_KWH,
     "calc-energy layer_kg_m2 x 0.1027 m2 (r5_E3_energy_dfn.json)"),
    (5, "Negative conductive additive", "carbon, 2 wt% of active (literature default, annotated)", G["neg"] * POS_CON_NEG_RATIO,
     G["neg"] * POS_CON_NEG_RATIO / 1000 / ENERGY_KWH, "96/2/2 split"),
    (6, "Negative binder", "CMC/SBR-class, 2 wt% of active (literature default, annotated)", G["neg"] * POS_CON_NEG_RATIO,
     G["neg"] * POS_CON_NEG_RATIO / 1000 / ENERGY_KWH, "96/2/2 split"),
    (7, "Separator", "8 um, 397 kg/m3, por 0.47", G["sep"], G["sep"] / 1000 / ENERGY_KWH,
     "calc-energy layer_kg_m2 x 0.1027 m2"),
    (8, "Electrolyte", "sigma 1.6 S/m, D 3.2e-10 m2/s, t+ 0.6 (estimates); fill 1.0 x pore volume", ELYTE_G,
     ELYTE_G / 1000 / ENERGY_KWH, "pore volume 5.0101e-6 m3 x 1.2 g/cm3 (literature default)"),
    (9, "Positive current collector", "Al, 12 um (2700 kg/m3)", G["al"], G["al"] / 1000 / ENERGY_KWH,
     "calc-energy layer_kg_m2 x 0.1027 m2"),
    (10, "Negative current collector", "Cu, 8 um (8960 kg/m3)", G["cu"], G["cu"] / 1000 / ENERGY_KWH,
     "calc-energy layer_kg_m2 x 0.1027 m2"),
    (11, "Enclosure / tabs / terminals / mandrel", "NOT MODELED", 0.0, 0.0,
     "parameter set contains no enclosure/tab keys - honest omission"),
    (12, "TOTAL cell mass", "incl. electrolyte", TOTAL_G, TOTAL_G / 1000 / ENERGY_KWH,
     "kg/kWh = g/1000 / 0.0181647 kWh (18.1647 Wh, r5_E3_energy_dfn.json)"),
    (13, "TOTAL without electrolyte", "contract caliber per calc-energy mass_kg", sum(G.values()),
     sum(G.values()) / 1000 / ENERGY_KWH, "matches calc-energy mass_kg 0.0395362 (electrolyte excluded)"),
]


def fmt(x, nd):
    return round(x, nd)


def write_bom(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "BOM"
    header = ["#", "Component", "Material / detail", "g/cell", "kg/kWh", "Basis / source"]
    ws.append(header)
    hfill = PatternFill("solid", fgColor="14283C")
    for row in BOM_ROWS:
        ws.append([
            row[0], row[1], row[2],
            float(fmt(row[3], 2)) if row[0] not in (11,) else "Not modeled",
            float(fmt(row[4], 3)) if row[0] not in (11,) else "Not modeled",
            row[5],
        ])
    for c in ws[1]:
        c.fill = hfill
        c.font = Font(color="FFFFFF", bold=True)
    widths = [4, 30, 52, 12, 12, 62]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + i)].width = w
    ws.freeze_panes = "A2"
    wb.save(path)


CALC_INPUTS = [
    ("Nominal cell capacity", 5.0, "Ah", "parameter set `Nominal cell capacity [A.h]`"),
    ("Measured 1C capacity 25 C (DFN)", CAPACITY_AH_1C, "Ah", "cell/r5_E3_1c_dfn.json (re-nominalization +0.78 %, kept)"),
    ("Voltage window", "2.5 - 4.2", "V", "parameter set `Lower/Upper voltage cut-off [V]`"),
    ("Electrode height", 0.065, "m", "parameter set `Electrode height [m]`"),
    ("Electrode width", 1.58, "m", "parameter set `Electrode width [m]`"),
    ("Positive thickness", 75.6e-6, "m", "parameter set"),
    ("Negative thickness", 85.2e-6, "m", "parameter set"),
    ("Separator thickness", 8e-6, "m", "parameter set (R2: 12 um -> 8 um)"),
    ("Positive CC thickness", 12e-6, "m", "parameter set (R2: 16 um -> 12 um)"),
    ("Negative CC thickness", 8e-6, "m", "parameter set (R2: 12 um -> 8 um)"),
    ("Stack thickness (sum)", 188.8e-6, "m", "75.6+85.2+8+12+8 um"),
    ("Positive porosity", 0.28, "-", "parameter set (R2 compression)"),
    ("Negative porosity", 0.28, "-", "params_E3.json (R5: 0.22 -> 0.28 headroom)"),
    ("Separator porosity", 0.47, "-", "parameter set"),
    ("Positive particle radius", 3.5e-6, "m", "parameter set"),
    ("Negative particle radius", 3.0e-6, "m", "parameter set"),
    ("Positive material density (derived)", 3262.0, "kg/m3", "layer_kg_m2 / (t x (1-eps))"),
    ("Negative material density (derived)", 1657.0, "kg/m3", "layer_kg_m2 / (t x (1-eps))"),
    ("Al density", 2700.0, "kg/m3", "parameter set"),
    ("Cu density", 8960.0, "kg/m3", "parameter set"),
    ("Positive active-material volume fraction", 0.665, "-", "parameter set `Positive electrode active material volume fraction`"),
    ("Negative active-material volume fraction", 0.75, "-", "parameter set `Negative electrode active material volume fraction`"),
    ("Electrolyte conductivity", 1.6, "S/m", "params_E3.json override (transport escalation, ESTIMATE)"),
    ("Electrolyte diffusivity", 3.2e-10, "m2/s", "params_E3.json override (ESTIMATE)"),
    ("Cation transference number", 0.6, "-", "params_E3.json override (ESTIMATE)"),
    ("Electrolyte initial concentration", 1000.0, "mol/m3", "parameter set"),
    ("Electrolyte density (fill calc)", 1200.0, "kg/m3", "literature default, annotated (set has none)"),
    ("Total heat transfer coefficient", 80.0, "W/(m2 K)", "params_E3.json (liquid-cold-plate class)"),
    ("Cell volume (mechanical refresh)", 1.938976e-5, "m3", "R4 procedure: sum(thickness_outer surfaces) x area"),
    ("Electrode area", AREA_M2, "m2", "0.065 m x 1.58 m"),
    ("Cold-soak initial temperature", 253.15, "K", "lowT protocol `Initial temperature [K]`"),
]

CALC_CAP = [
    ("1C capacity, 25 C", "Q1C = integral(I)dt over 1C_discharge, DFN", CAPACITY_AH_1C, "Ah", "cell/r5_E3_1c_dfn.json"),
    ("1C capacity, -20 C cold-soak", "QlowT = integral(I)dt over lowT_discharge (T0=253.15 K), DFN", CAPACITY_AH_LOWT, "Ah", "cell/r5_E3_lowt_dfn.json"),
    ("Retention", "QlowT / Q1C = 5.0078 / 5.0392", RETENTION, "-", "cell/r5_E3_retention_dfn.json (>= 0.95 required)"),
    ("Discharge energy", "E = integral(V*I)dt over 1C_discharge", ENERGY_WH, "Wh", "cell/r5_E3_energy_dfn.json"),
    ("Midpoint voltage", "V at 50 % discharged capacity", 3.847341, "V", "cell/r5_E3_energy_dfn.json midpoint_voltage_v"),
    ("DCR (informational)", "(start OCV - V10%) / I1C", 0.002068898, "ohm", "cell/r5_E3_energy_dfn.json dcr_ohm"),
]

CALC_ED = [
    ("Gravimetric energy density", "18.1647 Wh / 0.0395362 kg (electrolyte excluded)", GED, "Wh/kg", ">= 327.18, PASS +132.3", "cell/r5_E3_energy_dfn.json"),
    ("Volumetric energy density", "18.1647 Wh / 0.01938976 L (sum layer thickness x area)", VED, "Wh/L", ">= 880, PASS +56.8", "cell/r5_E3_energy_dfn.json"),
]

NEG_WINDOW_AH = 5.253  # full anode window 0 -> 0.9014 (thickness x eps_active x area)
POS_WINDOW_AH = 5.092  # full cathode window 0.2700 -> 0.8531
CALC_NP = [
    ("Anode full-window capacity", "c_max_neg x 0.9014 x F/3600 x t_neg x 0.75 x 0.1027", NEG_WINDOW_AH, "Ah", "C/10 DFN stoich span + eps_active closure (scripts/calc_np_ratio.py)"),
    ("Cathode full-window capacity", "c_max_pos x (0.8531-0.2700) x F/3600 x t_pos x 0.665 x 0.1027", POS_WINDOW_AH, "Ah", "C/10 DFN stoich span + eps_active closure"),
    ("N/P ratio", "5.253 / 5.092", NEG_WINDOW_AH / POS_WINDOW_AH, "-", "positive-limited (cathode exhausts first)"),
    ("Inventory closure check", "electrodes transfer 5.0384 Ah (1C span); computed 5.0385 / 5.0387", 5.0384, "Ah", "consistent at 0.1 % (diag_thermal_variant.py)"),
    *[(f"Mass - {label}", f"layer_kg_m2 x {AREA_M2}", round(g, 4), "g", "calc-energy layer_kg_m2") for label, g in
      [("positive active", G["pos"]), ("negative active", G["neg"]), ("Al CC", G["al"]),
       ("Cu CC", G["cu"]), ("separator", G["sep"])]],
    ("Mass - electrolyte fill", "pore volume 5.0101e-6 m3 x 1200 kg/m3", round(ELYTE_G, 4), "g", "pore-volume formula (literature density)"),
    ("Total mass (no electrolyte) = calc-energy mass_kg", "sum of layer masses", round(sum(G.values()), 4), "g", "matches mass_kg 0.0395362"),
]

CALC_PROC = [
    ("Positive areal density", "layer_kg_m2 x 1000", 177.557184, "g/m2", "check: t x (1-eps) x rho = 75.6e-6 x 0.72 x 3262 = 177.6"),
    ("Negative areal density", "layer_kg_m2 x 1000", 101.647008, "g/m2", "check: 85.2e-6 x 0.72 x 1657 = 101.6"),
    ("Positive compaction density", "rho x (1-eps) / 1000 (kg/m3 -> g/cm3)", 3262 * 0.72 / 1000.0, "g/cm3", "unit conversion /1000 annotated"),
    ("Negative compaction density", "rho x (1-eps) / 1000", 1657 * 0.72 / 1000.0, "g/cm3", "unit conversion /1000 annotated"),
    ("Electrolyte fill amount", "pore volume x 1.2 g/cm3 x fill factor 1.0", ELYTE_G, "g/cell", "pore volume 5.0101e-6 m3 (eps-weighted layers x area)"),
    ("Formation recommendation", "0.1C CC to 4.2 V, 25 C, 2 cycles", "-", "-", "design recommendation (production value requires tuning, annotated)"),
]


def write_calc(path):
    wb = Workbook()
    def sheet(name, title, headers, rows, widths):
        ws = wb.active if wb.active.title == "Sheet" and len(wb.sheetnames) == 1 else wb.create_sheet()
        ws.title = name
        ws.append([title])
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
        ws.append(headers)
        for r in rows:
            ws.append(list(r))
        for c in ws[2]:
            c.fill = PatternFill("solid", fgColor="14283C")
            c.font = Font(color="FFFFFF", bold=True)
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[chr(64 + i)].width = w
        for row in ws.iter_rows(min_row=3):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")

    sheet("Inputs", "Input parameters (finalist E3, params_E3.json)", ["Parameter", "Value", "Unit", "Source"],
          CALC_INPUTS, [42, 14, 12, 62])
    sheet("CapacityEnergy", "Capacity and energy", ["Quantity", "Formula", "Value", "Unit", "Source"],
          CALC_CAP, [26, 44, 12, 8, 46])
    sheet("EnergyDensity", "Energy density vs criteria", ["Quantity", "Formula", "Value", "Unit", "Threshold / verdict", "Source"],
          CALC_ED, [26, 44, 10, 8, 26, 40])
    sheet("NPratioMass", "N/P ratio and mass", ["Quantity", "Formula", "Value", "Unit", "Source"],
          CALC_NP, [32, 52, 10, 8, 56])
    sheet("Process", "Process design parameters", ["Parameter", "Formula", "Value", "Unit", "Notes"],
          CALC_PROC, [32, 40, 12, 10, 62])
    wb.save(path)


def md_table_rows(md_text):
    """Parse markdown tables into list-of-rows (cells). Also returns non-table line blocks."""
    tables, opened, lines = [], [], []
    for raw in md_text.splitlines():
        if raw.strip().startswith("|") and raw.strip().endswith("|"):
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue  # separator row
            opened.append(cells)
        else:
            if opened:
                tables.append(opened)
                opened = []
    if opened:
        tables.append(opened)
    return tables


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def strip_md(t):
    t = t.replace("**", "").replace("`", "")
    return esc(t)


NAVY = colors.HexColor("#14283C")
BLUE = colors.HexColor("#1E5A8A")
ORANGE = colors.HexColor("#C97B3D")
LIGHT = colors.HexColor("#F4F6FA")
GRID = colors.HexColor("#9DB2C9")


def build_pdf(path, title, code, subtitle, blocks, tables, addl_story_builder=None):
    """blocks: list of (kind, text) for cover/narrative; tables: list of dicts {title, rows, widths}."""
    _fp = font_manager.findfont("DejaVu Sans")
    _fp_b = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))
    pdfmetrics.registerFont(TTFont("DejaVu", _fp))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", _fp_b))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=1.4 * cm, rightMargin=1.4 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.4 * cm,
                            title=title, author="Virtual Battery Factory - headless session")
    S = {}
    S["h1"] = ParagraphStyle("h1", fontName="DejaVu-Bold", fontSize=15, leading=19, textColor=NAVY, spaceAfter=6)
    S["sub"] = ParagraphStyle("sub", fontName="DejaVu", fontSize=9, leading=12, textColor=BLUE, spaceAfter=2)
    S["h2"] = ParagraphStyle("h2", fontName="DejaVu-Bold", fontSize=11, leading=15, textColor=NAVY, spaceBefore=10, spaceAfter=4)
    S["body"] = ParagraphStyle("body", fontName="DejaVu", fontSize=8.5, leading=11.5, spaceAfter=3)
    S["bullet"] = ParagraphStyle("bullet", fontName="DejaVu", fontSize=8.5, leading=11.5, leftIndent=10, spaceAfter=2)
    S["quote"] = ParagraphStyle("quote", fontName="DejaVu", fontSize=8, leading=10.5, textColor=colors.HexColor("#555555"),
                                leftIndent=8, spaceAfter=4)
    S["cell"] = ParagraphStyle("cell", fontName="DejaVu", fontSize=7.2, leading=9.4, alignment=TA_LEFT)
    S["cellb"] = ParagraphStyle("cellb", fontName="DejaVu-Bold", fontSize=7.2, leading=9.4, textColor=colors.white)

    story = [Paragraph(esc(title), S["h1"]),
             Paragraph(f"{code} &nbsp;|&nbsp; case t4_r2", S["sub"]),
             Paragraph(esc(subtitle), S["sub"]),
             HRFlowable(width="100%", color=ORANGE, thickness=1.4, spaceBefore=4, spaceAfter=12)]
    for kind, text in blocks:
        story.append(Paragraph(strip_md(text), S[kind]))

    for t in tables:
        if t.get("title"):
            story.append(Paragraph(esc(t["title"]), S["h2"]))
        header = [Paragraph(esc(str(c)), S["cellb"]) for c in t["rows"][0]]
        body = [[Paragraph(strip_md(str(c)), S["cell"]) for c in r] for r in t["rows"][1:]]
        data = [header] + body
        cols = len(header)
        widths = t.get("widths") or [doc.width + 2 * doc.leftMargin - 2 * doc.leftMargin for _ in [1]] * 0 or None
        if not widths:
            widths = [(doc.width) / cols] * cols
        tbl = Table(data, colWidths=widths, repeatRows=1)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("GRID", (0, 0), (-1, -1), 0.4, GRID),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ]
        tbl.setStyle(TableStyle(style))
        story.append(tbl)
        story.append(Spacer(1, 10))
    if addl_story_builder:
        addl_story_builder(story)
    doc.build(story)


def md_to_pdf(md_path, pdf_path, code, title):
    text = open(md_path, encoding="utf-8").read()
    tables = md_table_rows(text)
    blocks = []
    in_table = False
    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("|"):
            in_table = True
            continue
        if in_table and not s.startswith("|"):
            in_table = False
        if s.startswith("# "):
            blocks.append(("h2", s[2:]))
        elif s.startswith("## "):
            blocks.append(("h2", s[3:]))
        elif s.startswith("### "):
            blocks.append(("h2", s[4:]))
        elif s.startswith(">"):
            blocks.append(("quote", s[1:]))
        elif s.startswith("- "):
            blocks.append(("bullet", "- " + s[2:]))
        elif s.startswith("---"):
            continue
        elif s:
            blocks.append(("body", s))
    subtitle_parts = [l for l in text.splitlines() if l and not l.startswith(("#", "|", ">", "-"))][:1]
    build_pdf(pdf_path, title, code, subtitle_parts[0] if subtitle_parts else "", blocks,
              [{"title": None, "rows": t} for t in tables])


# ---------- datasheet.docx (mirror of datasheet.md table) ----------
def write_datasheet_docx(path, md_path):
    text = open(md_path, encoding="utf-8").read()
    tables = md_table_rows(text)
    tbl = tables[0]
    doc = _docx_mod.Document()
    doc.add_heading("Technical Datasheet - VBF-T4R2-DSH-01", level=0)
    p = doc.add_paragraph()
    p.add_run("Extreme-cold equipment cell | finalist E3-porheadroom | Chen2020 base (NMC811-class/graphite) | 2026-08-26")
    p.runs[0].font.size = Pt(9)
    table = doc.add_table(rows=len(tbl), cols=3)
    table.style = "Table Grid"
    for i, row in enumerate(tbl):
        for j, cell in enumerate(row):
            table.cell(i, j).text = cell
    for i, w in enumerate([3.2, 9.0, 3.8]):
        for row in table.rows:
            row.cells[i].width = _docx_mod.shared.Inches(w)
    doc.save(path)


# ---------- delivery index ----------
idx_rows = [
    ("VBF-T4R2-DS-01", "Cell Design Specification", "PDF", "01", "deliverables/design_spec.pdf; source design_spec.md"),
    ("VBF-T4R2-BOM-01", "Bill of Materials", "XLSX", "01", "deliverables/bom.xlsx; PDF rendition bom.pdf"),
    ("VBF-T4R2-DSH-01", "Technical Datasheet", "DOCX", "01", "deliverables/datasheet.docx; source datasheet.md; PDF rendition datasheet.pdf"),
    ("VBF-T4R2-CALC-01", "Check / Calc Sheet", "XLSX", "01", "deliverables/calc.xlsx; PDF rendition calc.pdf"),
    ("VBF-T4R2-DVPR-01", "Design Verification Plan & Report", "PDF", "01", "deliverables/dvpr.pdf; source dvpr.md"),
    ("VBF-T4R2-DFMEA-01", "Design FMEA", "PDF", "01", "deliverables/dfmea.pdf; source dfmea.md"),
    ("VBF-T4R2-IDX-01", "Delivery Index", "PDF", "01", "deliverables/delivery_index.pdf (this document)"),
    ("VBF-T4R2-CAD-01", "Packaging & Geometry Drawing", "PDF", "-", "N/A: requires user clarification (zero-interaction rule) - skipped honestly"),
]

file_rows = [
    ("design_spec.md", "Cell Design Specification (source)", "md"),
    ("design_spec.pdf", "Cell Design Specification (release)", "pdf"),
    ("bom.xlsx", "Bill of Materials (native)", "xlsx"),
    ("bom.pdf", "Bill of Materials (release)", "pdf"),
    ("datasheet.md", "Technical Datasheet (source)", "md"),
    ("datasheet.docx", "Technical Datasheet (DOCX release)", "docx"),
    ("datasheet.pdf", "Technical Datasheet (PDF release)", "pdf"),
    ("calc.xlsx", "Check / Calc Sheet (native)", "xlsx"),
    ("calc.pdf", "Check / Calc Sheet (release)", "pdf"),
    ("dvpr.md", "Design Verification Plan & Report (source)", "md"),
    ("dvpr.pdf", "Design Verification Plan & Report (release)", "pdf"),
    ("dfmea.md", "Design FMEA (source)", "md"),
    ("dfmea.pdf", "Design FMEA (release)", "pdf"),
    ("delivery_index.md", "Delivery Index (this document)", "md"),
    ("delivery_index.pdf", "Delivery Index (release)", "pdf"),
    ("../report.html", "Case report (ancillary, rendered by /bda render)", "html"),
]


def write_index_md(path):
    present = [r for r in file_rows if os.path.exists(os.path.normpath(os.path.join(DEL, r[0])))]
    lines = [
        "# Design Delivery Index - VBF-T4R2-IDX-01",
        "Case t4_r2: extreme-cold environment equipment battery | 2026-08-26 | headless session",
        "",
        "| VBF code | Title | Format | Rev | Files |",
        "|---|---|---|---|---|",
    ]
    for code, title, fmt_, rev, files in idx_rows:
        lines.append(f"| {code} | {title} | {fmt_} | {rev} | {files} |")
    lines += [
        "",
        "## File list (files below all exist on disk at generation time)",
        "",
        "| File | Role | Format |",
        "|---|---|---|",
    ]
    for fname, role, fmt_ in present:
        lines.append(f"| {fname} | {role} | {fmt_} |")
    lines += [
        "",
        "## Signature block (headless: left blank per template)",
        "",
        "Prepared by: ____________________    Reviewed by: ____________________",
        "",
        "Approved by: ____________________    Date: ____________________",
        "",
        f"Generation: /bda render completed (report.html exists); {len(present)} files registered; "
        "note: CAD delivery not generated (requires user clarification, zero-interaction rule).",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def idx_pdf(path):
    pdfs_rows = [["VBF code", "Title", "Format", "Rev", "Files"]]
    for r in idx_rows:
        pdfs_rows.append([r[0], r[1], r[2], r[3], r[4]])
    files_tbl = [["File", "Role", "Format"]]
    for fname, role, fmt_ in file_rows:
        if os.path.exists(os.path.normpath(os.path.join(DEL, fname))):
            files_tbl.append([fname, role, fmt_])
    build_pdf(
        path, "Design Delivery Index", "VBF-T4R2-IDX-01",
        "Case t4_r2 - extreme-cold environment equipment battery - 2026-08-26 - headless session",
        [
            ("body", "This index registers the deliverable set of case t4_r2. Only files that exist on disk are listed. "
                     "Signature block left blank (headless session, no user present)."),
            ("body", "CAD packaging drawing (VBF-T4R2-CAD-01): N/A - requires user clarification; skipped per zero-interaction rule."),
        ],
        [{"title": "Numbering scheme", "rows": pdfs_rows, "widths": [3.1 * cm, 5.4 * cm, 1.7 * cm, 1.2 * cm, 7.0 * cm]},
         {"title": "File list", "rows": files_tbl, "widths": [4.0 * cm, 9.4 * cm, 1.6 * cm]}],
    )


def bom_pdf(path):
    rows = [["#", "Component", "Material / detail", "g/cell", "kg/kWh", "Basis / source"]]
    for r in BOM_ROWS:
        rows.append([str(r[0]), r[1], r[2],
                     "Not modeled" if r[0] == 11 else f"{r[3]:.2f}",
                     "Not modeled" if r[0] == 11 else f"{r[4]:.3f}", r[5]])
    build_pdf(path, "Bill of Materials", "VBF-T4R2-BOM-01",
              "Finalist E3-porheadroom | dual caliber g/cell (per cell) and kg/kWh (per 0.0181647 kWh) | 2026-08-26",
              [("body", "Binder/conductive-additive rows use the literature-default 96/2/2 wt% split of active mass - annotated, "
                        "because the Chen2020 parameter set has no binder/aditive keys. Enclosure/tabs/mandrel: Not modeled (no keys).")],
              [{"rows": rows, "widths": [0.9 * cm, 3.6 * cm, 4.9 * cm, 1.6 * cm, 1.5 * cm, 6.3 * cm]}],
              )


def calc_pdf(path):
    sheets = [
        ("Inputs", "Input parameters (finalist E3, params_E3.json)", ["Parameter", "Value", "Unit", "Source"], CALC_INPUTS),
        ("CapacityEnergy", "Capacity and energy", ["Quantity", "Formula", "Value", "Unit", "Source"], CALC_CAP),
        ("EnergyDensity", "Energy density vs criteria", ["Quantity", "Formula", "Value", "Unit", "Threshold / verdict", "Source"], CALC_ED),
        ("NPratioMass", "N/P ratio and mass", ["Quantity", "Formula", "Value", "Unit", "Source"], CALC_NP),
        ("Process", "Process design parameters", ["Parameter", "Formula", "Value", "Unit", "Notes"], CALC_PROC),
    ]
    def fmtv(v):
        if isinstance(v, float):
            return f"{v:.6g}" if abs(v) >= 1e4 or abs(v) < 1e-3 else f"{v:g}"
        return str(v)

    tables = []
    for name, _title, headers, data in sheets:
        rows = [headers]
        for r in data:
            rows.append([fmtv(v) for v in r])
        w = [3.4 * cm] + [4.8 * cm] * max(0, len(headers) - 3) + [2.2 * cm, 1.7 * cm, 6.3 * cm]
        w = (w + [3.0 * cm] * len(headers))[:len(headers)]
        tables.append({"title": _title, "rows": rows, "widths": w})
    build_pdf(path, "Check / Calc Sheet", "VBF-T4R2-CALC-01",
              "Finalist E3-porheadroom | formulas with sources, consistent with design_spec.md | 2026-08-26",
              [("body", "All values are mechanically taken from tool output JSONs under cell/ or computed by the stated formulas. "
                        "Compaction density carries the explicit /1000 kg/m3 -> g/cm3 unit conversion.")],
              tables)


def main():
    os.makedirs(DEL, exist_ok=True)
    write_bom(os.path.join(DEL, "bom.xlsx"))
    write_calc(os.path.join(DEL, "calc.xlsx"))
    write_datasheet_docx(os.path.join(DEL, "datasheet.docx"), os.path.join(DEL, "datasheet.md"))

    md_to_pdf(os.path.join(DEL, "design_spec.md"), os.path.join(DEL, "design_spec.pdf"),
              "VBF-T4R2-DS-01", "Cell Design Specification")
    bom_pdf(os.path.join(DEL, "bom.pdf"))
    md_to_pdf(os.path.join(DEL, "datasheet.md"), os.path.join(DEL, "datasheet.pdf"),
              "VBF-T4R2-DSH-01", "Technical Datasheet")
    calc_pdf(os.path.join(DEL, "calc.pdf"))
    md_to_pdf(os.path.join(DEL, "dvpr.md"), os.path.join(DEL, "dvpr.pdf"),
              "VBF-T4R2-DVPR-01", "Design Verification Plan & Report")
    md_to_pdf(os.path.join(DEL, "dfmea.md"), os.path.join(DEL, "dfmea.pdf"),
              "VBF-T4R2-DFMEA-01", "Design FMEA")

    write_index_md(os.path.join(DEL, "delivery_index.md"))
    idx_pdf(os.path.join(DEL, "delivery_index.pdf"))

    print("generated (size in bytes):")
    for f in sorted(os.listdir(DEL)):
        sz = os.path.getsize(os.path.join(DEL, f))
        print(f"  {f:22s} {sz:>7d}")
    for r in file_rows:
        p = os.path.normpath(os.path.join(DEL, r[0]))
        assert os.path.exists(p), f"missing {p}"
        assert os.path.getsize(p) > 1024, f"too small: {p}"
    print("ALL DELIVERABLE FILES PRESENT AND > 1024 bytes")


if __name__ == "__main__":
    main()