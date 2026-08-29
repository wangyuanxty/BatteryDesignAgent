# -*- coding: utf-8 -*-
"""t1_r3 — PDF release exports (reportlab): md->pdf and xlsx->pdf."""
import re
import sys
from pathlib import Path

import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable, ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

DEL = Path("runs/exp/t1_r3/deliverables")
PAGE_W, PAGE_H = A4
M = 18 * mm
AVAIL = PAGE_W - 2 * M

BLUEPRINT = colors.HexColor("#14283C")
MIDBLUE = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")

styles = getSampleStyleSheet()
S_BODY = ParagraphStyle("body", parent=styles["Normal"], fontSize=8.5, leading=12, spaceAfter=4)
S_H1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=15, leading=19, spaceBefore=8, spaceAfter=6,
                      textColor=MIDBLUE)
S_H2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=11.5, leading=15, spaceBefore=7, spaceAfter=4,
                      textColor=BLUEPRINT)
S_H3 = ParagraphStyle("h3", parent=styles["Heading3"], fontSize=10, leading=13, spaceBefore=5, spaceAfter=3,
                      textColor=MIDBLUE)
S_CELL = ParagraphStyle("cell", parent=styles["Normal"], fontSize=7.5, leading=9.5)
S_CELLH = ParagraphStyle("cellh", parent=S_CELL, textColor=colors.white)


def _clean(txt: str) -> str:
    txt = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", txt)
    return txt


def _cell(text: str, header: bool = False) -> Paragraph:
    return Paragraph(_clean(text), S_CELLH if header else S_CELL)


def _table(lines_rows: list[list[str]], header: bool, widths=None) -> Table:
    data = [[_cell(c, header and i == 0) for c in row] for i, row in enumerate(lines_rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA7B5")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    if header:
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), BLUEPRINT)]))
    return t


def md_to_pdf(md_path: Path, pdf_path: Path, title_override: str | None = None):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    bullets = []
    first_h1 = None

    def flush_bullets():
        nonlocal bullets
        if bullets:
            story.append(ListFlowable([ListItem(Paragraph(_clean(b), S_BODY)) for b in bullets],
                                      bulletType="bullet", start="-", leftIndent=10))
            bullets = []

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush_bullets()
            i += 1
            continue
        if line.strip() == "---":
            flush_bullets()
            story.append(HRFlowable(width="100%", thickness=0.8, color=MIDBLUE, spaceAfter=6))
            i += 1
            continue
        if line.startswith("### "):
            flush_bullets()
            story.append(Paragraph(_clean(line[4:]), S_H3))
            i += 1
            continue
        if line.startswith("## "):
            flush_bullets()
            story.append(Paragraph(_clean(line[3:]), S_H2))
            i += 1
            continue
        if line.startswith("# "):
            flush_bullets()
            txt = _clean(line[2:])
            if first_h1 is None:
                first_h1 = txt
            story.append(Paragraph(txt, S_H1))
            i += 1
            continue
        if line.startswith("- ") or line.startswith("* "):
            bullets.append(line[2:])
            i += 1
            continue
        if re.match(r"^\d+\.\s", line):
            bullets.append(re.sub(r"^\d+\.\s", "", line))
            i += 1
            continue
        if "|" in line:
            flush_bullets()
            raw = [[c.strip() for c in row.strip().strip("|").split("|")] for row in [line]]
            i += 1
            header = False
            while i < len(lines) and lines[i].lstrip().startswith("|") and \
                    re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i]):
                i += 1
                header = True
            while i < len(lines) and "|" in lines[i]:
                raw.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            n = max(len(r) for r in raw)
            raw = [r + [""] * (n - len(r)) for r in raw]
            w = AVAIL / n
            story.append(_table(raw, header, widths=[w] * n))
            story.append(Spacer(1, 4))
            continue
        flush_bullets()
        story.append(Paragraph(_clean(line), S_BODY))
        i += 1
    flush_bullets()

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=M, rightMargin=M, topMargin=14 * mm, bottomMargin=14 * mm,
                            title=title_override or first_h1 or md_path.stem)

    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#5A6B7D"))
        canvas.drawString(M, 9 * mm, "VBF-EXPT1R3 — t1_r3 virtual battery factory deliverables")
        canvas.drawRightString(PAGE_W - M, 9 * mm, f"page {doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"  {pdf_path.name} ({pdf_path.stat().st_size} bytes)")


def xlsx_to_pdf(xlsx_path: Path, pdf_path: Path):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    story = [Paragraph(_clean(f"PDF release of {xlsx_path.name}"), S_H1)]
    for ws in wb.worksheets:
        story.append(Paragraph(_clean(f"Sheet: {ws.title}"), S_H2))
        rows = list(ws.iter_rows(values_only=True))
        rows = [list(r) for r in rows if any(v is not None for v in r)]
        if not rows:
            story.append(Paragraph("(empty sheet)", S_BODY))
            continue
        n = max(len(r) for r in rows)
        data = []
        for r_i, r in enumerate(rows):
            r = list(r) + [""] * (n - len(r))
            data.append([_cell(str(v) if v is not None else "", header=r_i == 0) for v in r])
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA7B5")),
            ("BACKGROUND", (0, 0), (-1, 0), BLUEPRINT),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(t)
        story.append(PageBreak())
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=M, rightMargin=M, topMargin=14 * mm, bottomMargin=14 * mm,
                            title=f"{xlsx_path.stem} PDF release")
    doc.build(story)
    print(f"  {pdf_path.name} ({pdf_path.stat().st_size} bytes)")


def index_pdf(md_path: Path, pdf_path: Path):
    """delivery_index.pdf with blueprint-style cover band."""
    lines = md_path.read_text(encoding="utf-8").splitlines()
    # cover band
    cover = Table(
        [[Paragraph('VIRTUAL BATTERY FACTORY<br/><font size=9 color="#C97B3D">DESIGN DELIVERY PACKAGE</font>',
                    ParagraphStyle("cov", fontSize=17, leading=22, textColor=colors.white))],
         [Paragraph("Case: t1_r3 — next-generation pure electric sedan battery<br/>"
                    "ED >= 392.61 Wh/kg · 4C no plating · T_max <= 60 C · 4.7 V overcharge without TR<br/>"
                    f"<font size=8>Generation date: 2026-08-26 · prepared/reviewed/approved: (blank for manual signing)</font>",
                    ParagraphStyle("cov2", fontSize=9, leading=12.5, textColor=colors.white))]],
        colWidths=[AVAIL])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUEPRINT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEBELOW", (0, 0), (-1, -1), 3, COPPER),
    ]))

    story = [cover, Spacer(1, 10)]
    # reuse md renderer for the body but skip nothing — rebuild story by parsing from line 1
    i = 1
    bullets = []

    def flush():
        nonlocal bullets
        if bullets:
            story.append(ListFlowable([ListItem(Paragraph(_clean(b), S_BODY)) for b in bullets],
                                      bulletType="bullet", start="-", leftIndent=10))
            bullets = []

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush(); i += 1; continue
        if line.startswith("### "):
            flush(); story.append(Paragraph(_clean(line[4:]), S_H3)); i += 1; continue
        if line.startswith("## "):
            flush(); story.append(Paragraph(_clean(line[3:]), S_H2)); i += 1; continue
        if line.startswith("# "):
            flush(); story.append(Paragraph(_clean(line[2:]), S_H1)); i += 1; continue
        if line.startswith("- ") or line.startswith("* "):
            bullets.append(line[2:]); i += 1; continue
        if re.match(r"^\d+\.\s", line):
            bullets.append(re.sub(r"^\d+\.\s", "", line)); i += 1; continue
        if "|" in line:
            flush()
            raw = [[c.strip() for c in row.strip().strip("|").split("|")] for row in [line]]
            i += 1
            header = False
            while i < len(lines) and lines[i].lstrip().startswith("|") and \
                    re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i]):
                i += 1; header = True
            while i < len(lines) and "|" in lines[i]:
                raw.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            n = max(len(r) for r in raw)
            raw = [r + [""] * (n - len(r)) for r in raw]
            w = AVAIL / n
            story.append(_table(raw, header, widths=[w] * n))
            story.append(Spacer(1, 4))
            continue
        flush(); story.append(Paragraph(_clean(line), S_BODY)); i += 1
    flush()

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=M, rightMargin=M, topMargin=14 * mm, bottomMargin=14 * mm,
                            title="Delivery Package Index t1_r3")
    doc.build(story)
    print(f"  {pdf_path.name} ({pdf_path.stat().st_size} bytes)")


def main() -> int:
    for md_name in ("design_spec", "datasheet", "dvpr", "dfmea"):
        md_to_pdf(DEL / f"{md_name}.md", DEL / f"{md_name}.pdf")
    for xlsx_name in ("bom", "calc"):
        xlsx_to_pdf(DEL / f"{xlsx_name}.xlsx", DEL / f"{xlsx_name}.pdf")
    index_pdf(DEL / "delivery_index.md", DEL / "delivery_index.pdf")
    print("all PDFs written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
