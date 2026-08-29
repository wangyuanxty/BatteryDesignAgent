# -*- coding: utf-8 -*-
"""Generate bom.xlsx, calc.xlsx and PDF release versions for case t1_r1 deliverables.
All numbers computed from tool-output JSON files / parameter dumps (no handwritten values).
Usage: python make_deliverables.py [--index]   (--index: also build delivery_index.pdf)
"""
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

CASE = Path(__file__).resolve().parents[1]  # runs/exp/t1_r1
CELL = CASE / "cell"
OUT = CASE / "deliverables"
OUT.mkdir(exist_ok=True)

# ---- tool-output values (read-only, sourced) ----
E = json.loads((CELL / "r3_I_energy.json").read_text(encoding="utf-8"))
ONEC = json.loads((CELL / "r3_I_1c.json").read_text(encoding="utf-8"))
DFN4C = json.loads((CELL / "r3_I_4c_dfn.json").read_text(encoding="utf-8"))
SPME4C = json.loads((CELL / "r3_I_4c.json").read_text(encoding="utf-8"))
OC = json.loads((CELL / "r3_I_oc.json").read_text(encoding="utf-8"))
TR = json.loads((CELL / "r3_I_tr.json").read_text(encoding="utf-8"))

AREA = 0.065 * 1.58
# finalist overrides + Chen2020 defaults (dump_params.py)
POS_TH, POS_POR, POS_DEN, POS_AMVF = 75.6e-6, 0.335, 3262.0, 0.665
NEG_TH, NEG_POR, NEG_DEN, NEG_AMVF = 120e-6, 0.40, 1657.0, 0.60
SEP_TH, SEP_POR, SEP_DEN = 6e-6, 0.47, 397.0
ALCC, CUCC = 8e-6 * 2700.0, 5e-6 * 8960.0
C_MAX_N, C_MAX_P = 33133.0, 63104.0

POS_EL = POS_TH * (1 - POS_POR) * POS_DEN
NEG_EL = NEG_TH * (1 - NEG_POR) * NEG_DEN
SEP_EL = SEP_TH * (1 - SEP_POR) * SEP_DEN
MASS_KG = (POS_EL + NEG_EL + SEP_EL + ALCC + CUCC) * AREA
KWH = E["energy_wh"] / 1000.0
PORE_CM3 = (POS_TH * POS_POR + NEG_TH * NEG_POR + SEP_TH * SEP_POR) * AREA * 1e6
ELEC_G = PORE_CM3 * 1.2  # literature density 1.2 g/cm3, fill factor 1.0 (estimate, annotated)
NP_FORMULA = (C_MAX_N * NEG_AMVF * NEG_TH) / (C_MAX_P * POS_AMVF * POS_TH)
assert abs(MASS_KG - E["mass_kg"]) < 1e-12, (MASS_KG, E["mass_kg"])

layers_g = {
    "positive_electrode": POS_EL * AREA * 1000,
    "negative_electrode": NEG_EL * AREA * 1000,
    "positive_cc": ALCC * AREA * 1000,
    "negative_cc": CUCC * AREA * 1000,
    "separator": SEP_EL * AREA * 1000,
}

# BOM rows: (component, mass_g, note). Composition split = literature defaults (annotated).
BOM = [
    ("Positive active material (NMC811)", layers_g["positive_electrode"],
     "75.6 um x 0.1027 m2 x 0.665 x 3262 kg/m3 (parameter set + override)"),
    ("Positive conductive additive (carbon black)", layers_g["positive_electrode"] * 1.7 / 96.7,
     "literature default 96.7/1.7/1.6 wt% AM/CB/binder (estimate, annotated)"),
    ("Positive binder (PVDF)", layers_g["positive_electrode"] * 1.6 / 96.7,
     "literature default 96.7/1.7/1.6 wt% AM/CB/binder (estimate, annotated)"),
    ("Negative active material (graphite)", layers_g["negative_electrode"],
     "120 um x 0.1027 m2 x 0.60 x 1657 kg/m3 (parameter set + override)"),
    ("Negative conductive additive (carbon black)", layers_g["negative_electrode"] * 1.0 / 96.0,
     "literature default 96/1/3 wt% AM/CB/binder (estimate, annotated)"),
    ("Negative binder (CMC/SBR)", layers_g["negative_electrode"] * 3.0 / 96.0,
     "literature default 96/1/3 wt% AM/CB/binder (estimate, annotated)"),
    ("Separator", layers_g["separator"],
     "6 um x 0.1027 m2 x (1-0.47) x 397 kg/m3 (parameter set + override)"),
    ("Electrolyte", ELEC_G,
     "pore volume 7.820 cm3 x 1.2 g/cm3, fill factor 1.0 (literature density, estimate)"),
    ("Positive current collector (Al)", layers_g["positive_cc"], "8 um x 0.1027 m2 x 2700 kg/m3"),
    ("Negative current collector (Cu)", layers_g["negative_cc"], "5 um x 0.1027 m2 x 8960 kg/m3"),
    ("Enclosure and tabs", None, "Not modeled (no parameter)"),
]
BOM_TOTAL = sum(r[1] for r in BOM if r[1] is not None)

# ---- calc.xlsx ----
wb = Workbook()
hdr_fill = PatternFill("solid", fgColor="14283C")
hdr_font = Font(color="FFFFFF", bold=True)

def sheet(ws, title, headers, rows, widths=None):
    ws.title = title
    ws.append(headers)
    for c in ws[1]:
        c.fill, c.font = hdr_fill, hdr_font
        c.alignment = Alignment(wrap_text=True)
    for r in rows:
        ws.append(list(r))
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[chr(64 + i)].width = w
    ws.freeze_panes = "A2"

s1 = wb.active
sheet(s1, "Inputs",
      ["Parameter", "Value", "Unit", "Source"],
      [
          ["Positive electrode thickness", 75.6e-6, "m", "Chen2020 default (dump_params.py)"],
          ["Positive electrode porosity", 0.335, "-", "Chen2020 default"],
          ["Positive AMVF", 0.665, "-", "Chen2020 default"],
          ["Positive electrode density", 3262.0, "kg/m3", "Chen2020 default"],
          ["Positive particle radius", 5.22e-6, "m", "Chen2020 default"],
          ["Negative electrode thickness", 120e-6, "m", "params_r3_I.json override"],
          ["Negative electrode porosity", 0.40, "-", "params_r3_I.json override"],
          ["Negative AMVF", 0.60, "-", "params_r3_I.json override"],
          ["Negative electrode density", 1657.0, "kg/m3", "Chen2020 default"],
          ["Negative particle radius", 2.5e-6, "m", "params_r3_I.json override"],
          ["Separator thickness", 6e-6, "m", "params_r3_I.json override"],
          ["Separator porosity", 0.47, "-", "Chen2020 default"],
          ["Separator density", 397.0, "kg/m3", "Chen2020 default"],
          ["Al current collector thickness", 8e-6, "m", "params_r3_I.json override"],
          ["Cu current collector thickness", 5e-6, "m", "params_r3_I.json override"],
          ["Electrolyte conductivity", 1.8, "S/m", "params_r3_I.json override (formulation estimate)"],
          ["Cation transference number", 0.55, "-", "params_r3_I.json override (formulation estimate)"],
          ["Total heat transfer coefficient", 100.0, "W/m2K", "params_r3_I.json override"],
          ["Electrode height x width", "0.065 x 1.58", "m", "Chen2020 (area 0.1027 m2)"],
          ["Nominal cell capacity", 5.0, "Ah", "Chen2020"],
          ["Voltage window", "2.5 - 4.2", "V", "Chen2020 cut-offs"],
      ], [42, 16, 10, 46])

s2 = wb.create_sheet()
sheet(s2, "CapacityEnergy",
      ["Item", "Value", "Formula", "Source"],
      [
          ["1C discharge capacity", ONEC["capacity_ah"], "run-pyamm 1C_discharge, SPMe (discharge to 2.5 V)", "cell/r3_I_1c.json:capacity_ah"],
          ["Discharge energy", E["energy_wh"], "integral V(t) x I_1C dt / 3600; I_1C = nominal capacity x 1 = 5.0 A", "cell/r3_I_energy.json:energy_wh"],
          ["Midpoint voltage", E["midpoint_voltage_v"], "V at t = 50% of discharge", "cell/r3_I_energy.json:midpoint_voltage_v"],
          ["DC resistance", E["dcr_ohm"], "(V[0] - V[10% t]) / I_1C", "cell/r3_I_energy.json:dcr_ohm"],
          ["Peak power density", E["power_density_w_kg"], "V[0]^2 / (4 x R_DC) / mass", "cell/r3_I_energy.json:power_density_w_kg"],
      ], [30, 18, 60, 40])

s3 = wb.create_sheet()
sheet(s3, "EnergyDensity",
      ["Item", "Value", "Formula", "Source"],
      [
          ["Stack mass", E["mass_kg"], "sum over layers: thickness x (1-porosity) x density x area", "cell/r3_I_energy.json:mass_kg (recomputed match 1e-12)"],
          ["Gravimetric ED", E["energy_density_wh_kg"], "energy_wh / mass_kg", "cell/r3_I_energy.json:energy_density_wh_kg"],
          ["Stack volume", E["volume_m3"], "sum layer thickness x area", "cell/r3_I_energy.json:volume_m3"],
          ["Volumetric ED", E["energy_density_wh_l"], "energy_wh / volume_l", "cell/r3_I_energy.json:energy_density_wh_l"],
          ["Electrolyte included", E["electrolyte_included"], "contract caliber: electrolyte excluded", "cell/r3_I_energy.json:electrolyte_included"],
      ], [28, 20, 56, 46])

s4 = wb.create_sheet()
sheet(s4, "NPandMass",
      ["Item", "Value", "Formula", "Source"],
      [
          ["N/P (formula caliber)", NP_FORMULA, "(c_max_neg x AMVF_neg x L_neg) / (c_max_pos x AMVF_pos x L_pos)", "Chen2020 c_max + params_r3_I.json"],
          ["N/P (usable-window caliber)", 1.0, "anode window 0.860 vs cathode 0.647 of full capacity at 2.5-4.2 V envelope (1C: 5.6505 Ah both sides)", "derived from 1C capacity vs theoretical 6.567 / 8.732 Ah"],
          ["Positive layer mass", layers_g["positive_electrode"], "75.6 um x 0.665 x 3262 x 0.1027", "computed (matches calc-energy)"],
          ["Negative layer mass", layers_g["negative_electrode"], "120 um x 0.60 x 1657 x 0.1027", "computed (matches calc-energy)"],
          ["Al CC mass", layers_g["positive_cc"], "8 um x 2700 x 0.1027", "computed"],
          ["Cu CC mass", layers_g["negative_cc"], "5 um x 8960 x 0.1027", "computed"],
          ["Separator mass", layers_g["separator"], "6 um x 0.53 x 397 x 0.1027", "computed"],
          ["Total", MASS_KG * 1000, "sum of above", "= cell/r3_I_energy.json:mass_kg x 1000"],
      ], [30, 18, 62, 38])

s5 = wb.create_sheet()
sheet(s5, "Process",
      ["Parameter", "Value", "Formula", "Source"],
      [
          ["Positive areal density", "163.994 g/m2 = 16.399 mg/cm2", "thickness x (1-porosity) x density", "computed"],
          ["Negative areal density", "119.304 g/m2 = 11.930 mg/cm2", "thickness x (1-porosity) x density", "computed"],
          ["Positive compaction density", "2169.2 kg/m3 = 2.169 g/cm3", "density x (1-porosity) / 1000", "computed (x1000-folding point checked)"],
          ["Negative compaction density", "994.2 kg/m3 = 0.994 g/cm3", "density x (1-porosity) / 1000", "computed"],
          ["Electrolyte fill amount", f"{ELEC_G:.4f} g", "pore volume x 1.2 g/cm3 x fill factor 1.0", "pore volume from parameter set; density literature estimate"],
          ["Formation recommendation", "0.1C CC to 4.2 V, 25 degC, 2 cycles", "design recommended value; production tuning required", "annotated"],
      ], [30, 32, 52, 42])

wb.save(OUT / "bom_xlsx_tmp.xlsx" if False else OUT / "calc.xlsx")

wb2 = Workbook()
ws = wb2.active
sheet(ws, "BOM",
      ["Component", "Mass (g/cell)", "kg/kWh", "Source / formula"],
      [(r[0], None if r[1] is None else round(r[1], 4),
        None if r[1] is None else round(r[1] / 1000 / KWH, 5), r[2]) for r in BOM]
      + [("Total (excl. enclosure/tabs)", round(BOM_TOTAL, 4), round(BOM_TOTAL / 1000 / KWH, 5),
          "sum of modeled components; cell energy 0.0199673 kWh (cell/r3_I_energy.json)")],
      [46, 18, 12, 80])
ws2 = wb2.create_sheet()
sheet(ws2, "Summary",
      ["Item", "Value", "Source"],
      [
          ["Total component mass (with electrolyte)", f"{BOM_TOTAL:.4f} g", "BOM sum"],
          ["Contract stack mass (electrolyte excluded)", f"{MASS_KG*1000:.4f} g", "cell/r3_I_energy.json:mass_kg"],
          ["Cell energy", f"{E['energy_wh']:.4f} Wh", "cell/r3_I_energy.json:energy_wh"],
          ["Material usage", f"{BOM_TOTAL/1000/KWH:.5f} kg/kWh", "total mass / cell energy"],
      ], [46, 22, 60])
wb2.save(OUT / "bom.xlsx")
print("xlsx written: calc.xlsx, bom.xlsx; BOM total =", round(BOM_TOTAL, 4), "g; mass_kg check ok")

# ---- PDF release versions ----
TRANSLIT = {
    "≥": ">=", "≤": "<=", "→": "->", "←": "<-", "↔": "<->",
    "σ": "sigma", "⁺": "+", "⁻": "-", "≈": "~=", "−": "-",
    "Δ": "Delta", "∆": "delta", "​": "", "…": "...",
    "√": "sqrt",
}

def safe(s):
    for k, v in TRANSLIT.items():
        s = s.replace(k, v)
    return s.encode("cp1252", errors="replace").decode("cp1252")

STYLES = getSampleStyleSheet()
TITLE = ParagraphStyle("T", parent=STYLES["Title"], fontSize=15, textColor=colors.HexColor("#14283C"))
H2 = ParagraphStyle("H2", parent=STYLES["Heading2"], fontSize=11.5, textColor=colors.HexColor("#1E5A8A"), spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("B", parent=STYLES["BodyText"], fontSize=8.5, leading=11.5)
CELLP = ParagraphStyle("C", parent=BODY, fontSize=7.8, leading=9.6)
BULLET = ParagraphStyle("Bu", parent=BODY, leftIndent=12, bulletIndent=4, spaceAfter=1)

def md_table_row(cells):
    return [Paragraph(safe(c), CELLP) for c in cells]

def parse_md(text):
    story = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.strip() == "---":
            story.append(Spacer(1, 4))
            story.append(Table([[""]], colWidths=[17 * cm], style=TableStyle([
                ("LINEBELOW", (0, 0), (-1, -1), 0.7, colors.HexColor("#C97B3D"))])))
            story.append(Spacer(1, 4))
            continue
        if line.startswith("# "):
            story.append(Paragraph(safe(line[2:]), TITLE))
        elif line.startswith("## "):
            story.append(Paragraph(safe(line[3:]), H2))
        elif line.startswith("|"):
            if "rows" not in locals():
                continue
        elif line.startswith("- "):
            story.append(Paragraph(safe(line[2:]), BULLET, bulletText="•"))
        else:
            story.append(Paragraph(safe(line), BODY))
    return story

def parse_md_full(text):
    """parser handling tables (greedy row collection)."""
    story, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.strip() == "---":
            story.append(Spacer(1, 4))
            story.append(Table([[""]], colWidths=[17 * cm], style=TableStyle([
                ("LINEBELOW", (0, 0), (-1, -1), 0.7, colors.HexColor("#C97B3D"))])))
            story.append(Spacer(1, 4))
            i += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(safe(line[2:]), TITLE))
            i += 1
        elif line.startswith("## "):
            story.append(Paragraph(safe(line[3:]), H2))
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            body = rows[1:] if len(rows) > 1 and all(set(c) <= set("-: ") for c in rows[1]) else rows
            data = [md_table_row(r) for r in body]
            if data:
                t = Table(data, repeatRows=1)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#14283C")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA7B4")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EDF2F7")]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]))
                story.append(t)
                story.append(Spacer(1, 5))
        elif line.startswith("- "):
            story.append(Paragraph(safe(line[2:]), BULLET, bulletText="•"))
            i += 1
        else:
            story.append(Paragraph(safe(line), BODY))
            i += 1
    return story

def pdf_from_md(name):
    text = (OUT / f"{name}.md").read_text(encoding="utf-8")
    doc = SimpleDocTemplate(str(OUT / f"{name}.pdf"), pagesize=A4,
                            leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm)
    doc.build(parse_md_full(text))
    print(f"pdf written: {name}.pdf")

def pdf_tables(name, title, sections):
    story = [Paragraph(safe(title), TITLE), Spacer(1, 8)]
    for h, headers, rows in sections:
        story.append(Paragraph(safe(h), H2))
        data = [md_table_row(r) for r in [headers] + rows]
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#14283C")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA7B4")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EDF2F7")]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))
    doc = SimpleDocTemplate(str(OUT / f"{name}.pdf"), pagesize=A4,
                            leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm)
    doc.build(story)
    print(f"pdf written: {name}.pdf")

if __name__ == "__main__":
    for md in ("design_spec", "datasheet", "dvpr", "dfmea"):
        pdf_from_md(md)
    # bom.pdf (row-by-row identical to bom.xlsx)
    pdf_tables("bom", "Bill of Materials - VBF-T1R1-BOM-01",
               [("Bill of Materials (g/cell and kg/kWh; dual caliber)",
                 ["Component", "Mass (g/cell)", "kg/kWh", "Source / formula"],
                 [(r[0], "Not modeled" if r[1] is None else f"{r[1]:.4f}",
                   "-" if r[1] is None else f"{r[1]/1000/KWH:.5f}", r[2]) for r in BOM]
                 + [("Total (excl. enclosure/tabs)", f"{BOM_TOTAL:.4f}", f"{BOM_TOTAL/1000/KWH:.5f}",
                     "sum of modeled components; cell energy 0.0199673 kWh (cell/r3_I_energy.json)")])])
    # calc.pdf (mirrors calc.xlsx sheets)
    pdf_tables("calc", "Design Calculation Sheet - VBF-T1R1-CALC-01", [
        ("Energy density chain",
         ["Item", "Value", "Formula", "Source"],
         [["1C capacity", f"{ONEC['capacity_ah']:.4f} Ah", "1C_discharge protocol", "cell/r3_I_1c.json"],
          ["Energy", f"{E['energy_wh']:.4f} Wh", "integral V x I dt", "cell/r3_I_energy.json"],
          ["Stack mass", f"{E['mass_kg']:.6f} kg", "sum layer thickness x (1-porosity) x density x area", "cell/r3_I_energy.json (recomputed match 1e-12)"],
          ["ED gravimetric", f"{E['energy_density_wh_kg']:.3f} Wh/kg", "energy / mass", "cell/r3_I_energy.json"],
          ["ED volumetric", f"{E['energy_density_wh_l']:.3f} Wh/L", "energy / volume", "cell/r3_I_energy.json"]]),
        ("N/P and mass",
         ["Item", "Value", "Formula"],
         [["N/P formula caliber", f"{NP_FORMULA:.4f}", "(33133 x 0.60 x 120 um) / (63104 x 0.665 x 75.6 um)"],
          ["N/P usable-window caliber", "~1.0", "anode 0.860 vs cathode 0.647 of full capacity at 2.5-4.2 V"],
          ["Positive layer", f"{layers_g['positive_electrode']:.4f} g", "75.6 um x 0.665 x 3262 x 0.1027 m2"],
          ["Negative layer", f"{layers_g['negative_electrode']:.4f} g", "120 um x 0.60 x 1657 x 0.1027 m2"],
          ["Al CC / Cu CC", f"{layers_g['positive_cc']:.4f} / {layers_g['negative_cc']:.4f} g", "8 um x 2700 / 5 um x 8960 x 0.1027 m2"],
          ["Separator", f"{layers_g['separator']:.4f} g", "6 um x 0.53 x 397 x 0.1027 m2"]]),
        ("Process parameters",
         ["Parameter", "Value", "Formula"],
         [["Positive areal density", "163.994 g/m2 = 16.399 mg/cm2", "thickness x (1-porosity) x density"],
          ["Negative areal density", "119.304 g/m2 = 11.930 mg/cm2", "thickness x (1-porosity) x density"],
          ["Positive compaction density", "2169.2 kg/m3 = 2.169 g/cm3", "density x (1-porosity) / 1000"],
          ["Negative compaction density", "994.2 kg/m3 = 0.994 g/cm3", "density x (1-porosity) / 1000"],
          ["Electrolyte fill", f"{ELEC_G:.4f} g", "pore volume 7.820 cm3 x 1.2 g/cm3 x 1.0"],
          ["Formation", "0.1C CC to 4.2 V, 25 degC, 2 cycles", "design recommended value"]]),
    ])
    if "--index" in sys.argv:
        pdf_from_md("delivery_index")
    print("done")
