# -*- coding: utf-8 -*-
"""Generate PDF releases (reportlab, blueprint style) for t6_r1_noceiling deliverables.

Renders the markdown sources (design_spec/dvpr/dfmea/delivery_index) row-by-row,
and the bom/datasheet/calc PDFs from deliverable_data (same data as the xlsx/docx).
"""
import sys
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_noceiling")

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, HRFlowable)

from deliverable_data import DELIV, BOM_ROWS, CALC_SHEETS, DATASHEET_FIELDS, ENERGY_WH, MASS_G, MASS_ELEC_G

DEEP = colors.HexColor("#14283C")
MED = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")
GRID = colors.HexColor("#9DB2C8")
PAGE = A4
MARGIN = 1.35 * 28.3465
USABLE = PAGE[0] - 2 * MARGIN

REPL = {
    "\u2713": "PASS ", "\u2714": "PASS ", "\u2717": "FAIL ", "\u2718": "FAIL ",
    "\u2264": "<=", "\u2265": ">=", "\u2248": "~", "\u2192": "->", "\u2190": "<-",
    "\u2212": "-", "\u0394": "Delta", "\u03A3": "Sum", "\u207a": "+", "\u207b": "-",
    "\u00b2": "^2", "\u00b3": "^3", "\u03a9": "ohm", "\u03c3": "sigma", "\u201c": '"',
    "\u201d": '"', "\u2018": "'", "\u2019": "'", "\u2013": "-", "\u2014": "-",
}


def sanitize(s):
    for k, v in REPL.items():
        s = s.replace(k, v)
    return s.encode("latin-1", errors="replace").decode("latin-1")


def parse_md(path):
    blocks = []
    cur_table = None
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.rstrip()
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            if cur_table is None:
                cur_table = []
            cur_table.append(cells)
            continue
        if cur_table is not None:
            blocks.append(("table", cur_table))
            cur_table = None
        if not line.strip():
            continue
        if line.startswith("### "):
            blocks.append(("h3", line[4:]))
        elif line.startswith("## "):
            blocks.append(("h2", line[3:]))
        elif line.startswith("# "):
            blocks.append(("h1", line[2:]))
        elif line.startswith("- "):
            blocks.append(("bullet", line[2:]))
        else:
            blocks.append(("p", line))
    if cur_table is not None:
        blocks.append(("table", cur_table))
    return blocks


def clean_inline(s):
    s = s.replace("**", "")
    s = s.replace("`", "")
    return s


def col_widths(n):
    weights = {2: [0.38, 0.62], 3: [0.24, 0.46, 0.30], 4: [0.26, 0.26, 0.24, 0.24],
               5: [0.20, 0.13, 0.24, 0.10, 0.33], 6: [0.15, 0.13, 0.13, 0.17, 0.15, 0.27],
               7: [1.0 / 7.0] * 7}
    w = weights.get(n, [1.0 / n] * n)
    return [USABLE * x for x in w]


def build_story(blocks):
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15,
                        textColor=DEEP, spaceBefore=4, spaceAfter=6, leading=18)
    h2 = ParagraphStyle("h2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12,
                        textColor=MED, spaceBefore=10, spaceAfter=4, leading=15)
    h3 = ParagraphStyle("h3x", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=10.5,
                        textColor=COPPER, spaceBefore=6, spaceAfter=2, leading=13)
    body = ParagraphStyle("bodyx", parent=styles["Normal"], fontName="Helvetica", fontSize=9,
                          leading=12.5, alignment=TA_LEFT, spaceAfter=4)
    bullet = ParagraphStyle("bulletx", parent=body, leftIndent=14, bulletIndent=4, spaceAfter=2)
    cell = ParagraphStyle("cellx", parent=styles["Normal"], fontName="Helvetica", fontSize=7.5,
                          leading=9.5, alignment=TA_LEFT)
    story = []
    for kind, payload in blocks:
        if kind == "h1":
            story.append(Paragraph(sanitize(clean_inline(payload)), h1))
        elif kind == "h2":
            story.append(Paragraph(sanitize(clean_inline(payload)), h2))
        elif kind == "h3":
            story.append(Paragraph(sanitize(clean_inline(payload)), h3))
        elif kind == "bullet":
            story.append(Paragraph(sanitize(clean_inline(payload)), bullet, bulletText="\u2022"))
        elif kind == "p":
            story.append(Paragraph(sanitize(clean_inline(payload)), body))
        elif kind == "table":
            rows = [[Paragraph(sanitize(clean_inline(c)), cell) for c in r] for r in payload]
            tbl = Table(rows, colWidths=col_widths(len(payload[0])), repeatRows=1)
            style = [
                ("BACKGROUND", (0, 0), (-1, 0), MED),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 7.5),
                ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F7")]),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]
            tbl.setStyle(TableStyle(style))
            story.append(tbl)
            story.append(Spacer(1, 5))
    return story


def data_table(headers, rows, widths, body_size=7.5):
    cell = ParagraphStyle("cellx", fontName="Helvetica", fontSize=body_size, leading=body_size + 2.2)
    data = [[Paragraph(sanitize(str(h)), ParagraphStyle("hdr", fontName="Helvetica-Bold",
                                                        fontSize=7.5, textColor=colors.white)) for h in headers]]
    for r in rows:
        data.append([Paragraph(sanitize(str(c)), cell) for c in r])
    tbl = Table(data, colWidths=[USABLE * x for x in widths], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MED),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F7")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return tbl


def cover(docnum, title, subtitle):
    styles = getSampleStyleSheet()
    t = ParagraphStyle("covt", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.white)
    s = ParagraphStyle("covs", fontName="Helvetica", fontSize=10, leading=13,
                       textColor=colors.HexColor("#D8E2EE"))
    n = ParagraphStyle("covn", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=COPPER)
    inner = Table([[Paragraph(sanitize(title), t)],
                   [Paragraph(sanitize(subtitle), s)],
                   [Paragraph(sanitize(docnum), n)]],
                  colWidths=[USABLE - 40], style=TableStyle([
                      ("BACKGROUND", (0, 0), (-1, -1), DEEP),
                      ("LEFTPADDING", (0, 0), (-1, -1), 20),
                      ("RIGHTPADDING", (0, 0), (-1, -1), 20),
                      ("TOPPADDING", (0, 0), (-1, -1), 14),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                      ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return [inner, Spacer(1, 8), HRFlowable(width="100%", thickness=1.4, color=COPPER), Spacer(1, 10)]


def render_pdf(pdf_name, docnum, title, subtitle, flowables):
    pdf_path = str(DELIV / pdf_name)

    def footer(canv, doc):
        canv.saveState()
        canv.setStrokeColor(GRID)
        canv.setLineWidth(0.4)
        canv.line(MARGIN, MARGIN - 8, PAGE[0] - MARGIN, MARGIN - 8)
        canv.setFont("Helvetica", 7)
        canv.setFillColor(colors.HexColor("#5A6B7E"))
        canv.drawString(MARGIN, MARGIN - 18, "t6_r1_noceiling deliverables - virtual battery factory")
        canv.drawRightString(PAGE[0] - MARGIN, MARGIN - 18, "%s - page %d" % (docnum, doc.page))
        canv.restoreState()

    doc = BaseDocTemplate(pdf_path, pagesize=PAGE, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=MARGIN, bottomMargin=MARGIN + 16,
                          title=docnum, author="virtual-battery-factory")
    frame = Frame(MARGIN, MARGIN + 16, USABLE, PAGE[1] - 2 * MARGIN - 16, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])
    doc.build(flowables)
    print("wrote", pdf_name)


def md_pdf(pdf_name, docnum, title, subtitle, md_path):
    blocks = parse_md(md_path)
    story = build_story(blocks)
    render_pdf(pdf_name, docnum, title, subtitle, cover(docnum, title, subtitle) + story)


def bom_pdf():
    rows = []
    for comp, g, kgkwh, note in BOM_ROWS:
        rows.append([comp, "Not modeled" if g is None else "%.4f" % g,
                     "Not modeled" if kgkwh is None else "%.4f" % kgkwh, note])
    rows.append(["TOTAL (contract caliber, electrolyte excluded)", "%.4f" % MASS_G,
                 "%.4f" % (MASS_G / ENERGY_WH), "electrodes + CCs + separator (calc-energy mass_kg)"])
    rows.append(["Cell energy", "%.6f kWh" % (ENERGY_WH / 1000.0), "-",
                 "calc-energy output energy_wh / 1000 (18.6012 Wh)"])
    story = cover("VBF-T6R1NOCEILING-BOM-01",
                  "Bill of Materials - VBF-T6R1NOCEILING-BOM-01",
                  "ED-Compact B-p smartphone cell. Dual caliber g/cell and kg/kWh; literature defaults annotated.")
    story.append(Paragraph(sanitize("Binder / conductive additive use literature defaults (annotated): the parameter "
                                    "set has no inert-volume parameters; production formulation must rebalance the "
                                    "active fraction. Enclosure and tabs: Not modeled."),
                           ParagraphStyle("n", fontName="Helvetica", fontSize=9, leading=12)))
    story.append(Spacer(1, 6))
    story.append(data_table(["Component", "g/cell", "kg/kWh", "Annotation / source"], rows, [0.30, 0.10, 0.10, 0.50]))
    render_pdf("bom.pdf", "VBF-T6R1NOCEILING-BOM-01", "Bill of Materials",
               "ED-Compact B-p smartphone cell (NMC811/graphite, Chen2020)", story)


def dsh_pdf():
    story = cover("VBF-T6R1NOCEILING-DSH-01",
                  "Technical Datasheet - VBF-T6R1NOCEILING-DSH-01",
                  "ED-Compact B-p smartphone cell. Values mechanically taken from parameter set / simulation outputs "
                  "and annotated line by line; missing items honestly stated.")
    story.append(data_table(["Field", "Value (with source)"], DATASHEET_FIELDS, [0.22, 0.78], body_size=8))
    render_pdf("datasheet.pdf", "VBF-T6R1NOCEILING-DSH-01", "Technical Datasheet",
               "ED-Compact B-p smartphone cell (NMC811/graphite, Chen2020)", story)


def calc_pdf():
    story = cover("VBF-T6R1NOCEILING-CALC-01",
                  "Calculation Sheet - VBF-T6R1NOCEILING-CALC-01",
                  "Sheet chain: Inputs -> Capacity & Energy -> Energy Density -> N-P & Mass -> Process Params. "
                  "All conclusion-grade values from tool outputs / parameter set.")
    styles = getSampleStyleSheet()
    for name, rows in CALC_SHEETS:
        story.append(Paragraph(sanitize("Sheet: %s" % name),
                               ParagraphStyle("sh", parent=styles["Heading2"], fontName="Helvetica-Bold",
                                              fontSize=11, textColor=MED, spaceBefore=8, spaceAfter=4)))
        story.append(data_table(["Quantity", "Expression", "Value", "Unit", "Source"], rows,
                                [0.22, 0.34, 0.12, 0.07, 0.25]))
        story.append(Spacer(1, 4))
    render_pdf("calc.pdf", "VBF-T6R1NOCEILING-CALC-01", "Calculation Sheet",
               "ED-Compact B-p smartphone cell (NMC811/graphite, Chen2020)", story)


def main():
    DELIV.mkdir(exist_ok=True)
    d = DELIV
    md_pdf("design_spec.pdf", "VBF-T6R1NOCEILING-DS-01", "Cell Design Specification",
           "ED-Compact B-p smartphone cell (NMC811/graphite, Chen2020) - case exp/t6_r1_noceiling",
           d / "design_spec.md")
    bom_pdf()
    dsh_pdf()
    calc_pdf()
    md_pdf("dvpr.pdf", "VBF-T6R1NOCEILING-DVPR-01", "Design Verification Plan and Report (virtual test version)",
           "ED-Compact B-p smartphone cell - case exp/t6_r1_noceiling", d / "dvpr.md")
    md_pdf("dfmea.pdf", "VBF-T6R1NOCEILING-DFMEA-01", "Design FMEA (qualitative version)",
           "ED-Compact B-p smartphone cell - case exp/t6_r1_noceiling", d / "dfmea.md")
    idx_md = d / "delivery_index.md"
    if idx_md.exists():
        md_pdf("delivery_index.pdf", "VBF-T6R1NOCEILING-IDX-01", "Delivery Package Index",
               "Case exp/t6_r1_noceiling - controlled design package cover + file list", idx_md)
    else:
        print("delivery_index.md not present yet - IDX pdf skipped (run again after index is written)")


if __name__ == "__main__":
    main()
