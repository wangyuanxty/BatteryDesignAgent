# -*- coding: utf-8 -*-
"""Generate PDF releases for all deliverables using reportlab."""
from pathlib import Path
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak)

import openpyxl

HERE = Path(__file__).resolve().parent
DLV = HERE / "deliverables"

DEEP = colors.HexColor("#14283C")
MED = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")


def style_md_table(rows):
    data = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        data.append(cells)
    if not data:
        return None
    ncol = max(len(r) for r in data)
    data = [r + [""] * (ncol - len(r)) for r in data]
    return data


def render_md_to_pdf(md_path, pdf_path, title):
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1x", parent=styles["Heading1"], fontSize=16, textColor=DEEP)
    h2 = ParagraphStyle("h2x", parent=styles["Heading2"], fontSize=12, textColor=MED)
    body = ParagraphStyle("bodyx", parent=styles["BodyText"], fontSize=8.5, leading=11)
    cell = ParagraphStyle("cellx", parent=styles["BodyText"], fontSize=7, leading=9)

    lines = md_path.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.strip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            data = style_md_table(block)
            # markdown separator row (---) -> skip
            data = [r for r in data if not all(re.fullmatch(r"-{2,}", c) or c == "" for c in r)]
            tdata = [[Paragraph(c, cell) for c in r] for r in data]
            t = Table(tdata, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), DEEP),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F6")]),
            ]))
            story.append(t)
            story.append(Spacer(1, 4))
            continue
        if line.startswith("# "):
            story.append(Paragraph(line[2:], h1))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], h2))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], h2))
        elif line.startswith("> "):
            story.append(Paragraph(line[2:], ParagraphStyle("q", parent=body, textColor=COPPER)))
        elif line.strip().startswith("- "):
            story.append(Paragraph("• " + line.strip()[2:], body))
        else:
            story.append(Paragraph(line, body))
        i += 1

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=14*mm, rightMargin=14*mm, topMargin=14*mm, bottomMargin=14*mm,
                            title=title)
    doc.build(story)


def render_xlsx_to_pdf(xlsx_path, pdf_path, title):
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1x", parent=styles["Heading1"], fontSize=15, textColor=DEEP)
    cell = ParagraphStyle("cellx", parent=styles["BodyText"], fontSize=7, leading=9)
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    story = [Paragraph(title, h1), Spacer(1, 6)]
    for sheet in wb.worksheets:
        story.append(Paragraph(sheet.title, ParagraphStyle("s", parent=styles["Heading2"], fontSize=11, textColor=MED)))
        rows = []
        for row in sheet.iter_rows(values_only=True):
            if row is None or all(v is None for v in row):
                continue
            rows.append(["" if v is None else str(v) for v in row])
        if not rows:
            continue
        tdata = [[Paragraph(c, cell) for c in r] for r in rows]
        t = Table(tdata, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DEEP),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F6")]),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=12*mm, rightMargin=12*mm, topMargin=12*mm, bottomMargin=12*mm,
                            title=title)
    doc.build(story)


jobs = [
    ("design_spec.md", "design_spec.pdf", "Cell Design Specification VBF-T1OA-DS-01"),
    ("datasheet.md", "datasheet.pdf", "Technical Datasheet VBF-T1OA-DSH-01"),
    ("dvpr.md", "dvpr.pdf", "Design Verification Plan & Report VBF-T1OA-DVPR-01"),
    ("dfmea.md", "dfmea.pdf", "Design FMEA VBF-T1OA-DFMEA-01"),
    ("delivery_index.md", "delivery_index.pdf", "Delivery Package Index VBF-T1OA-IDX-01"),
]
for src, dst, title in jobs:
    render_md_to_pdf(DLV / src, DLV / dst, title)
    print("pdf:", dst)

render_xlsx_to_pdf(DLV / "bom.xlsx", DLV / "bom.pdf", "Bill of Materials VBF-T1OA-BOM-01")
render_xlsx_to_pdf(DLV / "calc.xlsx", DLV / "calc.pdf", "Design Calculation Sheet VBF-T1OA-CALC-01")
print("pdf: bom.pdf, calc.pdf")
