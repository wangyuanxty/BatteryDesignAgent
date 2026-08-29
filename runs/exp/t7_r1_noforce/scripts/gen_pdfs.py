"""Generate PDF releases for all deliverables (reportlab platypus)."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

DELIV = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_noforce/deliverables")
BLUE_D = colors.HexColor("#14283C")
BLUE_M = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")

styles = getSampleStyleSheet()
h1 = ParagraphStyle("h1x", parent=styles["Heading1"], textColor=BLUE_D, fontSize=15, spaceAfter=8)
h2 = ParagraphStyle("h2x", parent=styles["Heading2"], textColor=BLUE_M, fontSize=11, spaceAfter=4)
cell = ParagraphStyle("cellx", parent=styles["BodyText"], fontSize=7.5, leading=9)
cellb = ParagraphStyle("cellbx", parent=cell, fontName="Helvetica-Bold")

def make_table(header, rows, widths, max_h=380):
    data = [[Paragraph(h, cellb) for h in header]] + [
        [Paragraph(str(c), cell) for c in r] for r in rows
    ]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE_M),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F6")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

def doc(name, title, story, landscape_=False):
    out = DELIV / name
    SimpleDocTemplate(str(out), pagesize=landscape(A4) if landscape_ else A4,
                      topMargin=14 * mm, bottomMargin=14 * mm, leftMargin=12 * mm, rightMargin=12 * mm,
                      title=title).build(story)
    assert out.stat().st_size > 1024, f"{name} too small"
    print(f"{name}: {out.stat().st_size} bytes")

# ---------- design_spec.pdf ----------
rows = [
    ["System", "NMC811 (positive) / graphite (negative), Chen2020 baseline", "parameter set"],
    ["Nominal / 1C capacity", "5.0 Ah / 5.0065 Ah", "param set / r5_slim_1c_dfn.json"],
    ["Voltage window / midpoint", "2.5–4.2 V / 3.826 V", "param set / calc-energy"],
    ["Dimensions", "65 x 1580 mm (unfolded); stack 186.8 um; volume 19.18 cm3", "param set / calc-energy"],
    ["Electrolyte", "LiPF6/carbonate (Chen2020); design transport: sigma 2.5 S/m, D 5e-10 m2/s, t+ 0.5 (bridge estimates)", "params_r5_slim.json"],
    ["Positive electrode", "75.6 um NMC811, porosity 0.335, rho 3262 kg/m3 (unchanged)", "Chen2020"],
    ["Negative electrode", "85.2 um graphite, porosity 0.25, rho 1657 kg/m3, particles 4.0 um, Al2O3 ALD coating (SEI k 7.5e-13 m/s)", "params_r5_slim.json"],
    ["Separator / CC", "10 um (eps 0.47, rho 397) / Al 10 um, Cu 6 um", "params_r5_slim.json"],
    ["N/P", "0.667 (spec formula: neg 56.74 Ah/m2 / pos 85.03 Ah/m2); usable-window 1.00 by charge balance", "calc.xlsx sheet 4"],
    ["Mass", "36.226 g (contract caliber, electrolyte excluded); 42.55 g incl. electrolyte est.", "calc-energy / sec.3"],
    ["Areal density pos / neg / sep", "163.99 / 105.88 / 2.10 g/m2", "calc-energy layer_kg_m2"],
    ["Compaction pos / neg", "2.169 / 1.243 g/cm3 (x(1-eps) / 1000)", "formula"],
    ["Electrolyte fill", "5.27 cm3 pore volume -> 6.33 g @1.2 g/cm3 (lit), fill factor 1.0 assumed", "sec.3"],
    ["Formation", "0.1C CC to 4.2 V, 25 C, 2 cycles (design recommended; production needs tuning)", "sec.3"],
    ["ED / criterion", "491.47 Wh/kg (928.06 Wh/L) vs >=327.18  ->  PASS", "r5_slim_energy.json"],
    ["4C @45C plating / criterion", "anode min +0.0153 V -> plated=false  ->  PASS", "r5_slim_4c45.json"],
    ["SEI 100cyc @45C / criterion", "510.51 nm vs <=550  ->  PASS (+39.5 nm)", "r5_slim_aging45.json"],
    ["Nail 10 W / criterion", "triggered=false (T_final 317.0 K)  ->  PASS", "r5_slim_nail.json"],
    ["DCR / power density", "2.6415 mOhm / 43.24 kW/kg", "calc-energy"],
]
doc("design_spec.pdf", "Design Specification DS-01", [
    Paragraph("Cell Design Specification — VBF-T7R1NOFORCE-DS-01", h1),
    Paragraph("Case t7_r1_noforce (HEV battery) — 2026-08-25. PDF release of design_spec.md; values from parameter set / tool outputs.", styles["BodyText"]),
    Spacer(1, 6),
    make_table(["Field", "Value", "Source"], rows, [52 * mm, 150 * mm, 52 * mm]),
])

# ---------- bom.pdf ----------
rows = [
    ["Positive AM (NMC811)", "16.168", "0.908", "coating x 0.96 wt (lit default 96/2/2)"],
    ["Positive CB", "0.337", "0.019", "coating x 0.02 wt (lit default)"],
    ["Positive binder PVDF", "0.337", "0.019", "coating x 0.02 wt (lit default)"],
    ["Negative AM (graphite)", "10.417", "0.585", "coating x 0.958 wt (lit default 95.8/1.2/3.0)"],
    ["Negative CB", "0.130", "0.007", "coating x 0.012 wt (lit default)"],
    ["Negative binder CMC/SBR", "0.326", "0.018", "coating x 0.03 wt (lit default)"],
    ["Separator", "0.216", "0.012", "thickness x area x (1-eps) x 397 kg/m3 (tool caliber)"],
    ["Electrolyte", "6.326", "0.355", "pore vol 5.27 cm3 x 1.2 g/cm3 (lit)"],
    ["Al current collector", "2.773", "0.156", "10 um x area x 2700 kg/m3"],
    ["Cu current collector", "5.521", "0.310", "6 um x area x 8960 kg/m3"],
    ["Enclosure / tabs", "Not modeled", "—", "—"],
    ["TOTAL", "42.552", "2.390", "36.226 g contract (no electrolyte) + 6.326 g est."],
]
doc("bom.pdf", "Bill of Materials BOM-01", [
    Paragraph("Bill of Materials — VBF-T7R1NOFORCE-BOM-01", h1),
    Paragraph("Case t7_r1_noforce — 2026-08-25. Dual caliber g/cell and kg/kWh (cell energy 17.804 Wh). Additive/binder split uses literature weight fractions (parameter set has no additive/binder parameters).", styles["BodyText"]),
    Spacer(1, 6),
    make_table(["Component", "g/cell", "kg/kWh", "Formula note"], rows, [55 * mm, 25 * mm, 25 * mm, 95 * mm]),
])

# ---------- datasheet.pdf ----------
rows = [
    ["Rated capacity", "5.0 Ah nominal; 5.0065 Ah (1C sim)"],
    ["Voltage window", "2.5 – 4.2 V (midpoint 3.826 V)"],
    ["Rated energy", "17.804 Wh"],
    ["Energy density", "491.47 Wh/kg; 928.06 Wh/L"],
    ["Fast charge", "4C @45C: no plating (anode min +0.0153 V), T_max 325.54 K"],
    ["Max continuous discharge", "1C verified (5.0065 Ah, T_max 299.43 K); higher not simulated"],
    ["Operating temperature", "25–45 °C verified by simulation"],
    ["Cycle life", "Not determined (100-cyc 45C SEI simulated: 510.5 nm)"],
    ["Safety", "4C no plating PASS; nail 10 W triggered=false (T_final 317.0 K) PASS"],
    ["Dimensions", "65 mm x 1580 mm (unfolded); stack 186.8 um"],
    ["Mass", "36.23 g (no electrolyte) / ~42.6 g incl. electrolyte est."],
    ["DCR / power density", "2.6415 mOhm / 43.24 kW/kg"],
    ["Cooling requirement", "h >= 100 W/m2/K — load-bearing design element"],
]
doc("datasheet.pdf", "Technical Datasheet DSH-01", [
    Paragraph("Technical Datasheet — VBF-T7R1NOFORCE-DSH-01", h1),
    Paragraph("Case t7_r1_noforce (HEV cell, NMC811/graphite) — 2026-08-25. PDF release of datasheet.md.", styles["BodyText"]),
    Spacer(1, 6),
    make_table(["Field", "Value"], rows, [50 * mm, 200 * mm]),
])

# ---------- calc.pdf ----------
rows = [
    ["1C discharge capacity", "5.0065 Ah", "r5_slim_1c_dfn.json"],
    ["Rated energy", "17.8042 Wh", "r5_slim_energy.json"],
    ["ED gravimetric", "491.471 Wh/kg = 17.8042 / 0.0362264", "r5_slim_energy.json"],
    ["ED volumetric", "928.06 Wh/L = 17.8042 / 0.019184", "r5_slim_energy.json"],
    ["Mass (contract)", "36.2264 g (electrolyte excluded)", "r5_slim_energy.json"],
    ["Neg capacity density", "666,017 Ah/m3 = 33133 x 0.75 x 96485/3600", "Chen2020"],
    ["Pos capacity density", "1,124,723 Ah/m3 = 63104 x 0.665 x 96485/3600", "Chen2020"],
    ["N/P", "0.667 = (666017 x 85.2e-6) / (1124723 x 75.6e-6); usable-window 1.00", "formula"],
    ["Pos areal density", "163.99 g/m2 = 75.6e-6 x 0.665 x 3262", "calc-energy"],
    ["Neg areal density", "105.88 g/m2 = 85.2e-6 x 0.75 x 1657", "calc-energy"],
    ["Compaction pos", "2.169 g/cm3 = 3262 x 0.665 / 1000", "formula"],
    ["Compaction neg", "1.243 g/cm3 = 1657 x 0.75 / 1000", "formula"],
    ["Electrolyte fill", "6.33 g = 5.27 cm3 x 1.2 g/cm3 x 1.0", "formula (lit density)"],
]
doc("calc.pdf", "Design Calculation Sheet CALC-01", [
    Paragraph("Design Calculation Sheet — VBF-T7R1NOFORCE-CALC-01", h1),
    Paragraph("Case t7_r1_noforce — 2026-08-25. PDF summary of calc.xlsx (5 sheets: inputs → capacity/energy → energy density → N/P & mass → process parameters).", styles["BodyText"]),
    Spacer(1, 6),
    make_table(["Quantity", "Value", "Source"], rows, [45 * mm, 130 * mm, 55 * mm]),
])

# ---------- dvpr.pdf ----------
rows = [
    ["1", "1C discharge capacity", "1C CC, 25 C ambient", "5.0065 Ah", "PASS (vs 5.0 nominal)", "r5_slim_1c_dfn.json"],
    ["2", "4C charge temp rise", "4C @45C, lumped thermal, h=100", "T_max 325.54 K (+7.39 K)", "PASS (< 573 K red line)", "r5_slim_4c45.json"],
    ["3", "4C charge plating", "same run, anode potential", "min +0.0153 V", "PASS (plated=false)", "r5_slim_4c45.json"],
    ["4", "Voltage window", "parameter set", "2.5 – 4.2 V", "informational", "Chen2020"],
    ["5", "Energy density", "calc-energy caliber", "491.47 Wh/kg", "PASS (>= 327.18)", "r5_slim_energy.json"],
    ["6", "SEI @45C 100 cyc", "ec-reaction-limited aging", "510.51 nm", "PASS (<= 550)", "r5_slim_aging45.json"],
    ["7", "Nail 10 W thermal runaway", "t_init 325.54 K, amb 298.15 K, hA 0.531 W/K", "triggered=false; T_final 317.0 K", "PASS", "r5_slim_nail.json"],
    ["8", "DC internal resistance", "calc-energy", "2.6415 mOhm", "informational", "r5_slim_energy.json"],
]
doc("dvpr.pdf", "Design Verification Plan and Report DVPR-01", [
    Paragraph("Design Verification Plan and Report — VBF-T7R1NOFORCE-DVPR-01", h1),
    Paragraph("Case t7_r1_noforce — 2026-08-25. Virtual test version. N/A items (physical nail/overcharge/crush/drop, cycle life EOL, true DFT/MD endorsement): see dvpr.md limitations list.", styles["BodyText"]),
    Spacer(1, 6),
    make_table(["#", "Item", "Condition", "Result", "Verdict", "Source"],
               rows, [7 * mm, 38 * mm, 55 * mm, 55 * mm, 42 * mm, 48 * mm], max_h=340),
])

# ---------- dfmea.pdf ----------
rows = [
    ["1", "Anode plating @4C", "anode kinetics/transport", "R1 -0.192 V FAIL -> R5 +0.0153 V PASS", "High", "Low (design)", "4 um particles; transport electrolyte; cooling"],
    ["2", "Thermal runaway (nail)", "insufficient heat rejection", "R1 triggered 70-72 s (no cooling) -> R5 triggered=false", "High", "Low w/ cooling", "Liquid cooling h=100 mandatory"],
    ["3", "SEI growth @45C", "solvent-diffusion-limited", "R4 551.97 nm FAIL -> R5 510.5 nm (+39.5 margin)", "Medium", "Medium", "thin negative 85.2 um; ALD coating"],
    ["4", "Electrolyte oxidative decomp.", "HOMO vs window", "no molecular HOMO value (start_stage=3, real_compute=false)", "Medium", "Low (qual.)", "4.2 V cut-off; DFT follow-up listed"],
    ["5", "Insufficient capacity", "low loading", "5.0065 Ah vs 5.0 nominal", "Medium", "Low", "baseline loading"],
    ["6", "4C thermal overshoot", "rate heat vs cooling", "T_max 325.54 K vs 573 K", "High", "Low", "h=100 cooling"],
]
doc("dfmea.pdf", "Design FMEA DFMEA-01", [
    Paragraph("Design FMEA — VBF-T7R1NOFORCE-DFMEA-01", h1),
    Paragraph("Case t7_r1_noforce — 2026-08-25. Qualitative version, based on simulation signals (S/O three-level; RPN = qualitative S x O). Complete FMEA incl. process/supplier: N/A (beyond pure simulation boundary).", styles["BodyText"]),
    Spacer(1, 6),
    make_table(["#", "Failure mode", "Cause", "Simulation signal", "Sev", "Occ", "Mitigation (implemented)"],
               rows, [7 * mm, 32 * mm, 30 * mm, 62 * mm, 14 * mm, 18 * mm, 62 * mm], max_h=340),
])

# ---------- delivery_index.pdf ----------
story = [
    Paragraph("VIRTUAL BATTERY FACTORY", ParagraphStyle("cap", parent=styles["BodyText"], textColor=COPPER, fontSize=9, spaceAfter=2)),
    Paragraph("Delivery Package Index", ParagraphStyle("big", parent=styles["Heading1"], textColor=colors.white, fontSize=22)),
    Paragraph("Case: t7_r1_noforce — HEV battery design (NMC811/graphite)", ParagraphStyle("sub", parent=styles["BodyText"], textColor=colors.HexColor("#D7E3EF"), fontSize=10, spaceAfter=10)),
    Paragraph("Verdict: ACHIEVED — ED 491.47 Wh/kg; 4C @45C no plating; SEI 510.51 nm @100cyc/45C; nail 10 W no thermal runaway (log-evaluate R5: pass)", ParagraphStyle("sub2", parent=styles["BodyText"], textColor=colors.HexColor("#D7E3EF"), fontSize=9, spaceAfter=14)),
    Paragraph("Numbering scheme: VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO> (case ID t7_r1_noforce -> T7R1NOFORCE)", cell),
    Paragraph("Generation date: 2026-08-25", cell),
    Paragraph("Signature block — Prepared: ________   Reviewed: ________   Approved: ________", cell),
    Spacer(1, 8),
    make_table(["File name", "Number", "Format", "Source description"], [
        ["design_spec.md", "VBF-T7R1NOFORCE-DS-01", "md", "spec per deliverable-design-spec"],
        ["design_spec.pdf", "VBF-T7R1NOFORCE-DS-01", "pdf", "PDF release"],
        ["report.html", "VBF-T7R1NOFORCE-DS-02", "html", "bda render case report"],
        ["bom.xlsx", "VBF-T7R1NOFORCE-BOM-01", "xlsx", "BOM per deliverable-bom (openpyxl)"],
        ["bom.pdf", "VBF-T7R1NOFORCE-BOM-01", "pdf", "PDF release"],
        ["datasheet.md", "VBF-T7R1NOFORCE-DSH-01", "md", "datasheet per deliverable-datasheet"],
        ["datasheet.docx", "VBF-T7R1NOFORCE-DSH-01", "docx", "docx release (python-docx)"],
        ["datasheet.pdf", "VBF-T7R1NOFORCE-DSH-01", "pdf", "PDF release"],
        ["calc.xlsx", "VBF-T7R1NOFORCE-CALC-01", "xlsx", "calc sheet per deliverable-calc-sheet"],
        ["calc.pdf", "VBF-T7R1NOFORCE-CALC-01", "pdf", "PDF release"],
        ["dvpr.md", "VBF-T7R1NOFORCE-DVPR-01", "md", "DVPR per deliverable-dvpr (virtual)"],
        ["dvpr.pdf", "VBF-T7R1NOFORCE-DVPR-01", "pdf", "PDF release"],
        ["dfmea.md", "VBF-T7R1NOFORCE-DFMEA-01", "md", "DFMEA per deliverable-dfmea (qualitative)"],
        ["dfmea.pdf", "VBF-T7R1NOFORCE-DFMEA-01", "pdf", "PDF release"],
        ["delivery_index.md", "VBF-T7R1NOFORCE-IDX-01", "md", "this index (editable source)"],
        ["delivery_index.pdf", "VBF-T7R1NOFORCE-IDX-01", "pdf", "PDF release (blueprint cover style)"],
    ], [48 * mm, 62 * mm, 16 * mm, 74 * mm], max_h=330),
    Spacer(1, 8),
    Paragraph("CAD structure model: not produced — optional deliverable requiring user clarification (headless session, not requested); no CAD number registered.", cell),
]
out = DELIV / "delivery_index.pdf"
t = SimpleDocTemplate(str(out), pagesize=A4, topMargin=14 * mm, bottomMargin=14 * mm, leftMargin=12 * mm, rightMargin=12 * mm)
def cover(canvas, doc_):
    canvas.saveState()
    canvas.setFillColor(BLUE_D)
    canvas.rect(0, doc_.pagesize[1] - 46 * mm, doc_.pagesize[0], 46 * mm, stroke=0, fill=1)
    canvas.restoreState()
t.build(story, onFirstPage=cover, onLaterPages=cover)
assert out.stat().st_size > 1024
print(f"delivery_index.pdf: {out.stat().st_size} bytes")
print("all PDFs written")
