# -*- coding: utf-8 -*-
"""One-off PDF release generator for case t8_r1 deliverables.

Reads the already-generated source files (md/xlsx/docx) and renders a PDF
release per document code with reportlab. md sources are parsed structurally
(headings/paragraphs/bullets/tables) so the PDF mirrors the source content.
"""
import re
from pathlib import Path

import openpyxl
from docx import Document as DocxDocument
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether,
)

CASE = Path(__file__).resolve().parent
OUT = CASE / "deliverables"

DEEP = colors.HexColor("#14283C")
MID = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")
LIGHT = colors.HexColor("#EAF0F6")

S_TITLE = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15, leading=19,
                         textColor=colors.white, spaceAfter=2)
S_SUB = ParagraphStyle("sub", fontName="Helvetica", fontSize=9, leading=12,
                       textColor=colors.HexColor("#D8E4F0"))
S_H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=14,
                      textColor=DEEP, spaceBefore=10, spaceAfter=4)
S_H3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10, leading=13,
                      textColor=MID, spaceBefore=8, spaceAfter=3)
S_P = ParagraphStyle("p", fontName="Helvetica", fontSize=9, leading=12, spaceAfter=4)
S_CELL = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.5, leading=9.5)
S_CELL_B = ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5)

PAGE_W, PAGE_H = A4


def esc(t: str) -> str:
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("\n", "<br/>"))


def cover(doc, case_label: str, code: str, title: str):
    """Blueprint-style cover band."""
    story = []
    band = Table(
        [[Paragraph(esc(title), S_TITLE)],
         [Paragraph(esc(f"VBF-T8R1-{code}-01 &nbsp;|&nbsp; Case t8_r1 — {case_label} &nbsp;|&nbsp; 2026-08-25"), S_SUB)]],
        colWidths=[PAGE_W - 24 * mm], rowHeights=[None, None])
    band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DEEP),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 1.4, COPPER),
    ]))
    story.append(band)
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Prepared: ________&nbsp;&nbsp;&nbsp;Reviewed: ________&nbsp;&nbsp;&nbsp;Approved: ________", S_P))
    story.append(HRFlowable(width="100%", thickness=0.7, color=MID))
    story.append(Spacer(1, 2 * mm))
    return story


def md_to_story(text: str) -> list:
    """Structural md parser for the simple md subset used in deliverables."""
    story = []
    lines = text.splitlines()
    i = 0
    in_table = False
    tbl_rows = []
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line.startswith("|"):
            # table row (header separator row is skipped, first row = header)
            cells = [c.strip() for c in line.strip("|").split("|")]
            cells = [re.sub(r"^-+$", "", c) for c in cells]
            if all(c == "" for c in cells):
                i += 1
                continue
            tbl_rows.append(cells)
            i += 1
            continue
        if in_table or tbl_rows:
            story.append(table_story(tbl_rows))
            tbl_rows = []
        if line.startswith("# "):
            story.append(Paragraph(esc(line[2:]), S_TITLE_MAIN))
        elif line.startswith("### "):
            story.append(Paragraph(esc(line[3:]), S_H3))
        elif line.startswith("## "):
            story.append(Paragraph(esc(line[2:]), S_H2))
        elif line.startswith("- "):
            story.append(Paragraph("•&nbsp;&nbsp;" + esc(line[2:]), S_P))
        else:
            story.append(Paragraph(esc(line), S_P))
        i += 1
    if tbl_rows:
        story.append(table_story(tbl_rows))
    return story


def table_story(rows):
    if not rows:
        return Spacer(1, 1)
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    # column widths: distribute proportionally with a cap
    total_w = PAGE_W - 24 * mm
    widths = [min(total_w / ncols, 62 * mm)] * ncols
    body = []
    for j, r in enumerate(rows):
        sty = S_CELL_B if j == 0 else S_CELL
        body.append([Paragraph(esc(c), sty) for c in r])
    t = Table(body, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MID),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9FB6CC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return KeepTogether([t, Spacer(1, 2.5 * mm)])


S_TITLE_MAIN = ParagraphStyle("titlemain", fontName="Helvetica-Bold", fontSize=13,
                              leading=16, textColor=DEEP, spaceAfter=4)


def render_md(src: str, code: str, title: str, case_label: str):
    text = (CASE / "deliverables" / src).read_text(encoding="utf-8")
    out = OUT / (Path(src).stem + ".pdf")
    doc = SimpleDocTemplate(str(out), pagesize=A4,
                            leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=10 * mm, bottomMargin=12 * mm)
    story = cover(doc, case_label, code, title)
    story.extend(md_to_story(text))
    doc.build(story)
    print("wrote", out.name, out.stat().st_size, "bytes")


def render_xlsx(src: str, code: str, title: str, case_label: str):
    wb = openpyxl.load_workbook(OUT / src, read_only=True)
    out = OUT / (Path(src).stem + ".pdf")
    doc = SimpleDocTemplate(str(out), pagesize=A4,
                            leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=10 * mm, bottomMargin=12 * mm)
    story = cover(doc, case_label, code, title)
    for ws in wb.worksheets:
        rows = [[c for c in row] for row in ws.iter_rows(values_only=True)]
        rows = [r for r in rows if any(v is not None and str(v).strip() != "" for v in r)]
        if not rows:
            continue
        story.append(Paragraph(esc(ws.title), S_H2))
        story.append(table_story([[("" if v is None else str(v)) for v in r] for r in rows]))
    doc.build(story)
    print("wrote", out.name, out.stat().st_size, "bytes")


def render_docx(src: str, code: str, title: str, case_label: str):
    d = DocxDocument(OUT / src)
    out = OUT / (Path(src).stem + ".pdf")
    doc = SimpleDocTemplate(str(out), pagesize=A4,
                            leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=10 * mm, bottomMargin=12 * mm)
    story = cover(doc, case_label, code, title)
    for p in d.paragraphs:
        if p.text.strip():
            story.append(Paragraph(esc(p.text), S_P))
    for t in d.tables:
        rows = [[cell.text for cell in row.cells] for row in t.rows]
        story.append(table_story(rows))
    doc.build(story)
    print("wrote", out.name, out.stat().st_size, "bytes")


if __name__ == "__main__":
    render_md("design_spec.md", "DS", "Cell Design Specification — T8-40g", "Long-endurance drone battery")
    render_xlsx("bom.xlsx", "BOM", "Bill of Materials — T8-40g", "Long-endurance drone battery")
    render_docx("datasheet.docx", "DSH", "Technical Datasheet — T8-40g", "Long-endurance drone battery")
    render_xlsx("calc.xlsx", "CALC", "Design Calculation Sheet — T8-40g", "Long-endurance drone battery")
    render_md("dvpr.md", "DVPR", "Design Verification Plan and Report — T8-40g", "Long-endurance drone battery")
    render_md("dfmea.md", "DFMEA", "Design FMEA (qualitative) — T8-40g", "Long-endurance drone battery")
    render_md("delivery_index.md", "IDX", "Delivery Package Index — t8_r1", "Long-endurance drone battery")
    print("all pdfs done")
