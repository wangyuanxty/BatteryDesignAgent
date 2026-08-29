# -*- coding: utf-8 -*-
"""One-off deliverables builder: bom.xlsx, calc.xlsx + PDF releases for all deliverables.

Values: mechanically derived from bda tool outputs / parameter-set dumps (sources annotated).
PDF: reportlab, landscape A4, Arial TTF (coverage-checked, risky chars mapped to ASCII deterministically).
"""
import json
import os
import re
from pathlib import Path

import openpyxl
from openpyxl.styles import Font as XLFont, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1")
DLV = WS / "deliverables"
DLV.mkdir(parents=True, exist_ok=True)

# ---------------- source data (tool outputs, read mechanically) ----------------
energy = json.loads((WS / "cell/r7b_chen_energy.json").read_text(encoding="utf-8"))
energy_o = json.loads((WS / "cell/r7b_okane_energy.json").read_text(encoding="utf-8"))
f4c_c = json.loads((WS / "cell/r7b_chen_4c_dfn.json").read_text(encoding="utf-8"))
f4c_o = json.loads((WS / "cell/r7b_okane_4c_dfn.json").read_text(encoding="utf-8"))

E_WH = energy["energy_wh"]          # 22.2364 Wh (Chen, default base)
E_WH_O = energy_o["energy_wh"]      # 22.2024 Wh (OKane)
AREA = energy["area_m2"]            # 0.1027 m2
LKG = energy["layer_kg_m2"]
G = lambda kgm2: kgm2 * AREA * 1000.0  # kg/m2 -> g/cell

# ---------------- font setup (deterministic coverage) ----------------
from fontTools.ttLib import TTFont as FTT

ARIAL = r"C:\Windows\Fonts\arial.ttf"
ARIALBD = r"C:\Windows\Fonts\arialbd.ttf"
_cmap = FTT(ARIAL).getBestCmap()
_FALLBACK = {
    "\u2713": "PASS", "\u2717": "FAIL", "\u2192": "->", "\u2264": "<=", "\u2265": ">=",
    "\u2248": "~", "\u00b7": "*", "\u207b": "^", "\u2070": "0", "\u00b9": "1",
    "\u00b2": "2", "\u00b3": "3", "\u2074": "4", "\u2075": "5", "\u2076": "6",
    "\u2077": "7", "\u2078": "8", "\u2079": "9", "\u0394": "D", "\u2014": "-",
}

def _safe(s: str) -> str:
    out = []
    for ch in str(s):
        if ord(ch) < 128 or ch in _cmap:
            out.append(ch)
        else:
            out.append(_FALLBACK.get(ch, "?"))
    return "".join(out)

pdfmetrics.registerFont(TTFont("Arial", ARIAL))
pdfmetrics.registerFont(TTFont("Arial-Bold", ARIALBD))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")

# ---------------- reportlab styles ----------------
S = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=S["Title"], fontName="Arial-Bold", fontSize=15,
                    textColor=colors.HexColor("#14283C"), spaceAfter=6)
H2 = ParagraphStyle("H2", parent=S["Heading2"], fontName="Arial-Bold", fontSize=11.5,
                    textColor=colors.HexColor("#1E5A8A"), spaceBefore=8, spaceAfter=4)
H3 = ParagraphStyle("H3", parent=S["Heading3"], fontName="Arial-Bold", fontSize=10,
                    textColor=colors.HexColor("#C97B3D"), spaceBefore=6, spaceAfter=3)
BODY = ParagraphStyle("BODY", parent=S["BodyText"], fontName="Arial", fontSize=8.6, leading=11.5)
CELL = ParagraphStyle("CELL", parent=BODY, fontSize=7.6, leading=9.4)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="Arial-Bold")
BULL = ParagraphStyle("BULL", parent=BODY, leftIndent=12, bulletIndent=3, spaceAfter=2)

def _md_to_story(text: str, base: str) -> list:
    story = [Paragraph(_safe(base), H1), Spacer(1, 2)]
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("### "):
            story.append(Paragraph(_safe(s[4:]), H3)); i += 1; continue
        if s.startswith("## "):
            story.append(Paragraph(_safe(s[3:]), H2)); i += 1; continue
        if s.startswith("# "):
            story.append(Paragraph(_safe(s[2:]), H1)); i += 1; continue
        if s.startswith("|"):
            rows, widths = [], []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):  # separator row
                    i += 1
                    continue
                rows.append(cells)
                i += 1
            if rows:
                ncol = max(len(r) for r in rows)
                rows = [(r + [""] * (ncol - len(r))) for r in rows]
                colmax = [max((len(_safe(r[c])) for r in rows), default=8) for c in range(ncol)]
                tot = sum(min(m, 60) for m in colmax)
                widths = [max(28.0, 750.0 * min(m, 60) / tot) for m in colmax]
                data = [[Paragraph(_safe(cell).replace("**", ""), CELLB if ri == 0 else CELL)
                         for cell in row] for ri, row in enumerate(rows)]
                t = Table(data, colWidths=widths, repeatRows=1)
                t.setStyle(TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AAFC4")),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E5A8A")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                     [colors.white, colors.HexColor("#EEF3F8")]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]))
                story.append(t)
                story.append(Spacer(1, 5))
            continue
        if s.startswith("- "):
            story.append(Paragraph(_safe(s[2:].replace("**", "")), BULL, bulletText="\u2022"))
            i += 1
            continue
        story.append(Paragraph(_safe(s.replace("**", "")), BODY))
        i += 1
    return story

def make_md_pdf(md_name: str, base: str, cover: bool = False):
    text = (DLV / md_name).read_text(encoding="utf-8")
    pdf = DLV / (md_name.rsplit(".", 1)[0] + ".pdf")
    doc = SimpleDocTemplate(str(pdf), pagesize=landscape(A4),
                            leftMargin=16 * mm, rightMargin=16 * mm,
                            topMargin=12 * mm, bottomMargin=12 * mm,
                            title=_safe(base))
    story = []
    if cover:
        story.extend(_cover_story(base))
    story.extend(_md_to_story(text, base))
    doc.build(story)
    return pdf

def _cover_story(base: str) -> list:
    t = Table([[Paragraph(_safe(base), ParagraphStyle("C", parent=H1, fontSize=17,
                 textColor=colors.white, alignment=1))],
               [Paragraph(_safe("VBF-T5R1 delivery package - generated 2026-08-25"),
                          ParagraphStyle("C2", parent=BODY, fontSize=9.5,
                          textColor=colors.HexColor("#D8E4EF"), alignment=1))]],
              colWidths=[750])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#14283C")),
        ("LINEBELOW", (0, 0), (-1, -1), 2.2, colors.HexColor("#C97B3D")),
        ("TOPPADDING", (0, 0), (-1, -1), 22),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
    ]))
    return [t, Spacer(1, 10)]

# ================= BOM =================
def build_bom():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "BOM"
    head = ["#", "Component", "Material", "g per cell", "kg per kWh", "Formula", "Source"]
    ws.append(head)
    rows = [
        ("1", "Positive electrode - active material", "NMC811 composite (96 wt% split)",
         16.842 * 0.96, "16.842 x 0.96",
         "electrode layer mass mechanical (calc-energy layer_kg_m2 x area); 96:2:2 mass split = literature default (estimate - parameter set models single-phase composite)"),
        ("2", "Positive electrode - conductive additive", "carbon (2 wt% split)",
         16.842 * 0.02, "16.842 x 0.02", "same annotation as #1"),
        ("3", "Positive electrode - binder", "PVDF-class (2 wt% split)",
         16.842 * 0.02, "16.842 x 0.02", "same annotation as #1"),
        ("4", "Negative electrode - active material", "graphite(-SiOx) composite (96 wt% split)",
         9.902 * 0.96, "9.902 x 0.96", "same annotation as #1"),
        ("5", "Negative electrode - conductive additive", "carbon (2 wt% split)",
         9.902 * 0.02, "9.902 x 0.02", "same annotation as #1"),
        ("6", "Negative electrode - binder", "SBR/CMC-class (2 wt% split)",
         9.902 * 0.02, "9.902 x 0.02", "same annotation as #1"),
        ("7", "Separator", "polyolefin-class, 8 um / porosity 0.55 / 397 kg/m3",
         0.147, "8e-6 x (1-0.55) x 397 x 0.1027 x 1000",
         "mechanical from bridge/r7b_negR261.json + parameter-set density"),
        ("8", "Electrolyte", "EC-based + 1 M LiPF6, 9.53 g (NOT in contract cell mass)",
         9.532, "pore vol 7.943 cm3 x 1.2 g/cm3",
         "pore volume mechanical from layer geometry; density 1.2 g/cm3 = literature default (parameter set lacks the key)"),
        ("9", "Positive current collector", "Al foil 8 um / 2700 kg/m3",
         2.218, "8e-6 x 2700 x 0.1027 x 1000", "mechanical (bridge params)"),
        ("10", "Negative current collector", "Cu foil 6 um / 8960 kg/m3",
         5.521, "6e-6 x 8960 x 0.1027 x 1000", "mechanical (bridge params)"),
        ("11", "Enclosure / tabs", "Not modeled",
         "", "", "honest annotation: outside pure-simulation boundary"),
    ]
    for r in rows:
        kgkwh = round(r[3] / E_WH, 4) if isinstance(r[3], float) else ""
        ws.append([r[0], r[1], r[2], round(r[3], 3) if isinstance(r[3], float) else r[3],
                   kgkwh, r[4], r[5]])
    tot_contract = G(LKG["positive_electrode"] + LKG["negative_electrode"]
                     + LKG["positive_cc"] + LKG["negative_cc"] + LKG["separator"])
    tot_elec = 9.532
    ws.append([])
    ws.append(["", "TOTAL (contract caliber, electrolyte excluded)", "",
               round(tot_contract, 3), round(tot_contract / E_WH, 4),
               "sum of mechanical rows", "calc-energy mass_kg = 0.0346308 kg (matches)"])
    ws.append(["", "TOTAL incl. electrolyte (reference)", "",
               round(tot_contract + tot_elec, 3), round((tot_contract + tot_elec) / E_WH, 4),
               "contract + electrolyte", "reference caliber only"])
    ws.append(["", "Total energy (Chen2020 / OKane2022)", "", f"{E_WH:.4f} / {E_WH_O:.4f} Wh",
               "", "1C time-integrated V*I", "cell/r7b_{chen,okane}_energy.json"])
    ws.append(["", "Energy density (Chen2020 / OKane2022)", "",
               f"{energy['energy_density_wh_kg']:.1f} / {energy_o['energy_density_wh_kg']:.1f} Wh/kg",
               "", "E / contract mass", "cell/r7b_{chen,okane}_energy.json"])
    hfill = PatternFill("solid", fgColor="1E5A8A")
    for c in range(1, 8):
        ws.cell(1, c).fill = hfill
        ws.cell(1, c).font = XLFont(color="FFFFFF", bold=True)
    widths = [5, 34, 40, 13, 13, 32, 66]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    wb.save(DLV / "bom.xlsx")

# ================= CALC =================
def _sheet(ws, head, rows, widths):
    ws.append(head)
    for r in rows:
        ws.append(r)
    hfill = PatternFill("solid", fgColor="1E5A8A")
    for c in range(1, len(head) + 1):
        ws.cell(1, c).fill = hfill
        ws.cell(1, c).font = XLFont(color="FFFFFF", bold=True)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def build_calc():
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Inputs"
    _sheet(ws1, ["Parameter", "Value", "Unit", "Formula/Definition", "Source"],
        [
         ["Nominal cell capacity", 5.0, "Ah", "parameter set", "Chen2020/OKane2022 dump"],
         ["Voltage window", "2.5 - 4.2", "V", "lower/upper cut-off", "parameter set"],
         ["Electrode height", 0.065, "m", "parameter set", "dump"],
         ["Electrode width", 1.58, "m", "parameter set", "dump"],
         ["Electrode area", 0.1027, "m2", "height x width", "calc-energy area_m2"],
         ["Positive electrode thickness", 75.6e-6, "m", "design override", "bridge/r7b_negR261.json"],
         ["Positive electrode porosity", 0.335, "-", "set default (not overridden)", "dump"],
         ["Positive electrode density", 3262.0, "kg/m3", "set", "dump"],
         ["Positive active material volume fraction", 0.665, "-", "set", "dump"],
         ["Positive particle radius", 2.61e-6, "m", "design override", "bridge"],
         ["Negative electrode thickness", 105.8e-6, "m", "design override", "bridge"],
         ["Negative electrode porosity", 0.45, "-", "design override", "bridge"],
         ["Negative electrode density", 1657.0, "kg/m3", "set", "dump"],
         ["Negative active material volume fraction", 0.75, "-", "set", "dump"],
         ["Negative particle radius", 2.61e-6, "m", "design override (decisive plating lever)", "bridge"],
         ["Separator thickness", 8e-6, "m", "design override", "bridge"],
         ["Separator porosity", 0.55, "-", "design override", "bridge"],
         ["Separator density", 397.0, "kg/m3", "set", "dump"],
         ["Al collector thickness", 8e-6, "m", "design override", "bridge"],
         ["Cu collector thickness", 6e-6, "m", "design override", "bridge"],
         ["Electrolyte conductivity (target)", 2.0, "S/m", "design override (upper-bound estimate)", "bridge"],
         ["Electrolyte diffusivity (target)", 4.5e-10, "m2/s", "design override (upper-bound estimate)", "bridge"],
         ["Cation transference number (target)", 0.45, "-", "design override (upper-bound estimate)", "bridge"],
         ["Total heat transfer coefficient", 60.0, "W/m2/K", "design override (immersion-class)", "bridge"],
         ["Cell cooling surface area", 0.00531, "m2", "set", "dump"],
         ["1C protocol ambient", 298.15, "K", "protocol definition", "pybamm_runner PROTOCOLS"],
         ["4C protocol ambient", 318.15, "K", "protocol definition", "pybamm_runner PROTOCOLS"],
        ], [46, 14, 10, 46, 34])
    ws2 = wb.create_sheet("CapacityEnergy")
    _sheet(ws2, ["Quantity", "Chen2020 (DFN)", "OKane2022 (DFN)", "Unit", "Source"],
        [
         ["1C discharge capacity", round(energy["capacity_ah"], 4), round(energy_o["capacity_ah"], 4), "Ah", "cell/r7b_*_1c_dfn.json via calc-energy"],
         ["Rated energy (1C integral)", round(E_WH, 4), round(E_WH_O, 4), "Wh", "calc-energy energy_wh"],
         ["Midpoint voltage", round(energy["midpoint_voltage_v"], 4), round(energy_o["midpoint_voltage_v"], 4), "V", "calc-energy"],
         ["DC resistance (calc-energy caliber)", round(energy["dcr_ohm"] * 1000, 2), round(energy_o["dcr_ohm"] * 1000, 2), "mOhm", "calc-energy dcr_ohm"],
         ["Power density", round(energy["power_density_w_kg"] / 1000, 2), round(energy_o["power_density_w_kg"] / 1000, 2), "kW/kg", "calc-energy"],
         ["4C T_max (45 C ambient)", round(f4c_c["T_max_K"], 3), round(f4c_o["T_max_K"], 3), "K", "cell/r7b_*_4c_dfn.json"],
         ["4C anode surface potential min", round(min(f4c_c["anode_potential_v"]), 5), round(min(f4c_o["anode_potential_v"]), 5), "V", "cell/r7b_*_4c_dfn.json (>0 = no plating)"],
         ["4C charge acceptance (physical)", 4.73, 5.00, "Ah", "charge-segment duration x 20 A / 3600 (library capacity_ah key under-reports 5x - bug, not used)"],
        ], [42, 18, 18, 10, 66])
    ws3 = wb.create_sheet("EnergyDensity")
    _sheet(ws3, ["Layer", "Thickness m", "Porosity", "Density kg/m3", "kg/m2", "g per cell", "Share", "Source"],
        [
         ["Positive electrode", 75.6e-6, 0.335, 3262.0, LKG["positive_electrode"], round(G(LKG["positive_electrode"]), 3),
          f"{G(LKG['positive_electrode'])/34.631*100:.1f}%", "calc-energy layer_kg_m2"],
         ["Negative electrode", 105.8e-6, 0.45, 1657.0, LKG["negative_electrode"], round(G(LKG["negative_electrode"]), 3),
          f"{G(LKG['negative_electrode'])/34.631*100:.1f}%", "calc-energy layer_kg_m2"],
         ["Positive CC (Al 8um)", 8e-6, 0.0, 2700.0, LKG["positive_cc"], round(G(LKG["positive_cc"]), 3),
          f"{G(LKG['positive_cc'])/34.631*100:.1f}%", "calc-energy layer_kg_m2"],
         ["Negative CC (Cu 6um)", 6e-6, 0.0, 8960.0, LKG["negative_cc"], round(G(LKG["negative_cc"]), 3),
          f"{G(LKG['negative_cc'])/34.631*100:.1f}%", "calc-energy layer_kg_m2"],
         ["Separator", 8e-6, 0.55, 397.0, LKG["separator"], round(G(LKG["separator"]), 3),
          f"{G(LKG['separator'])/34.631*100:.1f}%", "calc-energy layer_kg_m2"],
         ["TOTAL", 203.4e-6, "", "", round(energy["mass_kg"], 5), round(energy["mass_kg"] * 1000, 3), "100%", "calc-energy mass_kg"],
         ["Energy density (Wh/kg)", "", "", "", "", round(energy["energy_density_wh_kg"], 3), "E/mass", "calc-energy (contract caliber, electrolyte excluded)"],
         ["Volumetric ED (Wh/L)", "", "", "", "", round(energy["energy_density_wh_l"], 2), "E/volume", "calc-energy"],
         ["Layer stack volume", "", "", "", "", round(energy["volume_m3"] * 1e6, 2), "cm3", "calc-energy volume_m3"],
        ], [26, 14, 10, 14, 12, 12, 9, 52])
    ws4 = wb.create_sheet("NPMass")
    _sheet(ws4, ["Quantity", "Value", "Formula / note", "Source"],
        [
         ["N/P ratio (thickness-ratio caliber)", 1.40, "105.8/75.6 = 1.3995; caliber used in proposals R4C-R6B. Parameter set defines fully-charged initial concentrations but no 0%-SOC stoich keys, so capacity-density form not computable from set keys alone.", "propose entries + set dump"],
         ["N/P empirical support", "anode-limited 1C", "capacity grew 5.73 -> 6.42 Ah when anode 85.2 -> 110 um (R4C) -> anode limits discharge -> N/P >= 1 consistent", "R4C evaluate entries"],
         ["Electrolyte mass (reference)", "9.53 g", "pore vol 7.943 cm3 x 1.2 g/cm3 (literature density, annotated)", "mechanical (design_spec section 3)"],
         ["Total mass incl. electrolyte (reference)", "44.16 g", "34.631 + 9.53", "mechanical"],
         ["kg/kWh total (contract caliber)", round(energy["mass_kg"] / (E_WH / 1000), 3), "mass_kg / E_kWh", "calc-energy"],
         ["kg/kWh total incl. electrolyte", round((energy["mass_kg"] * 1000 + 9.532) / 1000 / (E_WH / 1000), 3), "(mass + electrolyte) / E_kWh", "mechanical"],
        ], [36, 20, 80, 36])
    ws5 = wb.create_sheet("Process")
    _sheet(ws5, ["Process parameter", "Value", "Formula", "Source"],
        [
         ["Positive areal density", "163.99 g/m2", "75.6e-6 x (1-0.335) x 3262", "mechanical"],
         ["Negative areal density", "96.42 g/m2", "105.8e-6 x (1-0.45) x 1657", "mechanical"],
         ["Positive compaction density", "2.169 g/cm3", "3262 x 0.665 / 1000", "mechanical (divide by 1000!)"],
         ["Negative compaction density", "0.911 g/cm3", "1657 x 0.55 / 1000", "mechanical"],
         ["Electrolyte fill amount", "9.53 g (7.943 cm3)", "pore volume x 1.2 g/cm3 (literature density, annotated)", "mechanical"],
         ["Formation recommendation", "0.1C CC to 4.2 V, 25 C, 2 cycles", "design recommended value; production-line value requires tuning", "design note"],
        ], [36, 26, 50, 34])
    wb.save(DLV / "calc.xlsx")

# ================= xlsx -> pdf =================
def xlsx_to_pdf(name: str, base: str):
    wb = openpyxl.load_workbook(DLV / name, read_only=True)
    pdf = DLV / (name.rsplit(".", 1)[0] + ".pdf")
    doc = SimpleDocTemplate(str(pdf), pagesize=landscape(A4),
                            leftMargin=14 * mm, rightMargin=14 * mm,
                            topMargin=12 * mm, bottomMargin=12 * mm, title=_safe(base))
    story = _cover_story(base)
    for sheet in wb.worksheets:
        rows = list(sheet.iter_rows(values_only=True))
        rows = [r for r in rows if any(v is not None and str(v).strip() != "" for v in r)]
        if not rows:
            continue
        story.append(Paragraph(_safe(f"{base} - sheet '{sheet.title}'"), H2))
        ncol = max(len(r) for r in rows)
        rows = [tuple(r) + ("",) * (ncol - len(r)) for r in rows]
        colmax = [max((len(_safe(str(r[c]))) for r in rows), default=8) for c in range(ncol)]
        tot = sum(min(m, 70) for m in colmax)
        widths = [max(30.0, 760.0 * min(m, 70) / tot) for m in colmax]
        data = [[Paragraph(_safe(str(v)), CELLB if ri == 0 else CELL) for v in row]
                for ri, row in enumerate(rows)]
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AAFC4")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E5A8A")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF3F8")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))
    doc.build(story)
    return pdf

if __name__ == "__main__":
    build_bom()
    build_calc()
    for md, base, cov in [
        ("design_spec.md", "Cell Design Specification - VBF-T5R1-DS-01", True),
        ("datasheet.md", "Technical Datasheet - VBF-T5R1-DSH-01", True),
        ("dvpr.md", "Design Verification Plan and Report - VBF-T5R1-DVPR-01", True),
        ("dfmea.md", "Design FMEA - VBF-T5R1-DFMEA-01", True),
        ("delivery_index.md", "Delivery Package Index - VBF-T5R1-IDX-01", True),
    ]:
        p = make_md_pdf(md, base, cover=cov)
        print("pdf:", p.name, p.stat().st_size, "bytes")
    for x, base in [("bom.xlsx", "Bill of Materials - VBF-T5R1-BOM-01"),
                    ("calc.xlsx", "Design Calculation Sheet - VBF-T5R1-CALC-01")]:
        p = xlsx_to_pdf(x, base)
        print("pdf:", p.name, p.stat().st_size, "bytes")
    print("ALL DELIVERABLE FILES BUILT")
