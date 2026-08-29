# -*- coding: utf-8 -*-
"""PDF release generator for t2_r3 deliverables.

Reads the editable sources in deliverables/ (md tables / xlsx / docx) and renders
row-by-row identical PDF releases with the engineering-blueprint palette
#14283C / #1E5A8A / #C97B3D (reportlab, installed in .venv).
"""
import re
from pathlib import Path

import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

OUT = Path(__file__).resolve().parent / "deliverables"
NAVY = colors.HexColor("#14283C")
BLUE = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")

PAGE_W = A4[0] - 2 * 14 * mm          # margins 14 mm
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=16, textColor=colors.white, leading=20)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#DCE6F0"), leading=12)
SEC = ParagraphStyle("sec", fontName="Helvetica-Bold", fontSize=11, textColor=BLUE, leading=14, spaceBefore=8, spaceAfter=3)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=7, leading=9, textColor=colors.HexColor("#1A1A1A"))
CELLB = ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=colors.white)
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=colors.HexColor("#222222"), spaceAfter=4)


def esc(s):
    """ASCII-only, XML-escaped cell text (reportlab built-in fonts are latin-1)."""
    s = str(s)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for a, b in [("µm", "um"), ("μ", "u"), ("²", "^2"), ("³", "^3"), ("⁺", "^+"), ("⁻", "^-"),
                 ("×", "x"), ("−", "-"), ("–", "-"), ("≥", ">="), ("≤", "<="), ("≈", "~"),
                 ("✓", "[PASS]"), ("✗", "[FAIL]"), ("→", "->"), ("°", " deg "), ("Δ", "dT"),
                 ("ρ", "rho "), ("σ", "sigma "), ("π", "pi "), ("τ", "tau "), ("·", "*"),
                 ("÷", "/"), ("—", "--"), ("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'"),
                 ("±", "+/-"), ("é", "e"), ("・", "-"), ("　", " ")]:
        s = s.replace(a, b)
    s = s.encode("latin-1", "replace").decode("latin-1")
    return s


def cover(doc_title, subtitle, title, num):
    return [
        Table([[Paragraph(esc(title), HEAD), Paragraph(esc(subtitle), SUB)]],
              colWidths=[PAGE_W], rowHeights=None,
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                  ("LINEBELOW", (0, 0), (-1, 0), 2.2, COPPER),
                  ("TOPPADDING", (0, 0), (-1, -1), 10),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                  ("LEFTPADDING", (0, 0), (-1, -1), 8),
              ])),
        Spacer(1, 8),
        Paragraph("Document: %s | %s&nbsp;&nbsp;Generation date: 2026-08-26"
                  % (esc(doc_title), esc(num)), BODY),
        Spacer(1, 2),
    ]


def md_tables(text):
    """Yield (kind, payload) for headings, plain paragraphs and pipe tables of an md file."""
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            if rows:
                yield ("table", rows)
                rows = []
            continue
        if s.startswith("|") and s.count("|") >= 2:
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue
            rows.append(cells)
            continue
        if rows:
            yield ("table", rows)
            rows = []
        if s.startswith("#"):
            yield ("head", s.lstrip("#").strip())
        elif s.startswith((">", "- ")):
            yield ("para", s.lstrip("> -"))
        else:
            yield ("para", s)
    if rows:
        yield ("table", rows)


def table_flow(rows, max_w=PAGE_W):
    n = len(rows[0])
    widths = [max_w / n] * n
    data = []
    for i, r in enumerate(rows):
        data.append([Paragraph(esc(c), CELLB if i == 0 else CELL) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EDF2F7")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def md_to_pdf(src, pdf, doc_title, subtitle, title, num):
    text = (OUT / src).read_text(encoding="utf-8")
    story = cover(doc_title, subtitle, title, num)
    for kind, payload in md_tables(text):
        if kind == "head":
            story.append(Paragraph(esc(payload), SEC))
        elif kind == "para":
            story.append(Paragraph(esc(payload), BODY))
        else:
            story.append(table_flow(payload))
            story.append(Spacer(1, 6))
    SimpleDocTemplate(str(OUT / pdf), pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
                      topMargin=10 * mm, bottomMargin=10 * mm, title=esc(doc_title)).build(story)


def xlsx_to_pdf(src, pdf, doc_title, subtitle, title, num):
    wb = openpyxl.load_workbook(OUT / src, read_only=True)
    story = cover(doc_title, subtitle, title, num)
    first = True
    for ws in wb.worksheets:
        rows = [list(row) for row in ws.iter_rows(values_only=True)]
        rows = [r for r in rows if any(v is not None and str(v).strip() != "" for v in r)]
        if not rows:
            continue
        story.append(Paragraph("Sheet: %s" % esc(ws.title), SEC))
        story.append(table_flow(rows))
        story.append(Spacer(1, 8))
        first = False
    SimpleDocTemplate(str(OUT / pdf), pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
                      topMargin=10 * mm, bottomMargin=10 * mm, title=esc(doc_title)).build(story)


def docx_to_pdf(src, pdf, doc_title, subtitle, title, num):
    import docx
    d = docx.Document(OUT / src)
    story = cover(doc_title, subtitle, title, num)
    for obj in d.paragraphs:
        story.append(Paragraph(esc(obj.text), BODY))
    story.append(Spacer(1, 4))
    for tbl in d.tables:
        rows = [[cell.text for cell in row.cells] for row in tbl.rows]
        story.append(table_flow(rows))
        story.append(Spacer(1, 8))
    SimpleDocTemplate(str(OUT / pdf), pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
                      topMargin=10 * mm, bottomMargin=10 * mm, title=esc(doc_title)).build(story)


SUB_COMMON = ("Mechanically generated from simulation outputs under runs/exp/t2_r3/cell/ "
              "(r7_final_*_dfn.json, r6_combo-v5-final_aging*_spme.json, calc-energy). "
              "Values carry per-line sources; true-compute endorsement skipped "
              "(real_compute=false, see log endorse entry).")

md_to_pdf("design_spec.md", "design_spec.pdf",
          "Cell Design Specification", SUB_COMMON, "Cell Design Specification - combo-v5-final", "VBF-T2R3-DS-01")
xlsx_to_pdf("bom.xlsx", "bom.pdf",
            "Bill of Materials", SUB_COMMON + " Dual calibre: g/cell and kg/kWh.", "Bill of Materials - combo-v5-final", "VBF-T2R3-BOM-01")
docx_to_pdf("datasheet.docx", "datasheet.pdf",
            "Technical Datasheet", SUB_COMMON, "Technical Datasheet - combo-v5-final", "VBF-T2R3-DSH-01")
xlsx_to_pdf("calc.xlsx", "calc.pdf",
            "Design Calculation Sheet", SUB_COMMON + " Contract calibre consistent with design_spec.", "Design Calculation Sheet - combo-v5-final", "VBF-T2R3-CALC-01")
md_to_pdf("dvpr.md", "dvpr.pdf",
          "Design Verification Plan and Report", SUB_COMMON + " Virtual-test calibre; N/A items annotated.",
          "Design Verification Plan and Report (virtual) - combo-v5-final", "VBF-T2R3-DVPR-01")
md_to_pdf("dfmea.md", "dfmea.pdf",
          "Design FMEA", SUB_COMMON + " Qualitative calibre (S/O from simulation signals).",
          "Design FMEA (qualitative) - combo-v5-final", "VBF-T2R3-DFMEA-01")
md_to_pdf("delivery_index.md", "delivery_index.pdf",
          "Delivery Package Index", "Cover + controlled list of all deliverables actually generated for VBF case t2_r3.",
          "Delivery Package Index - VBF Case t2_r3", "VBF-T2R3-IDX-01")

print("PDFs written:", ", ".join(sorted(p.name for p in OUT.glob("*.pdf"))))
for p in sorted(OUT.glob("*.pdf")):
    print(" ", p.name, p.stat().st_size, "bytes")