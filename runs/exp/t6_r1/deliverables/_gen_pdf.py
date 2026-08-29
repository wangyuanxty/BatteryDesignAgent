# One-off PDF release generator (reportlab). Parses the deliverables/*.md tables and
# deliverables/*.xlsx sheets into PDF releases. No content lives here - all values come
# from the source files.
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak)

import openpyxl

OUT = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1\deliverables")
NAVY = colors.HexColor("#14283C")
MIDBLUE = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], fontSize=15, leading=18,
                    textColor=MIDBLUE, spaceBefore=10, spaceAfter=6)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], fontSize=11.5, leading=14,
                    textColor=NAVY, spaceBefore=8, spaceAfter=4)
BODY = ParagraphStyle("Bodyx", parent=styles["BodyText"], fontSize=8.5, leading=11)
CELL = ParagraphStyle("Cellx", parent=styles["BodyText"], fontSize=7.6, leading=9.6)
HEAD = ParagraphStyle("Headx", parent=styles["BodyText"], fontSize=7.8, leading=9.8,
                      textColor=colors.white, fontName="Helvetica-Bold")


def clean(s: str) -> str:
    s = s.replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    return s


def md_flowables(text: str):
    out = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            out.append(Paragraph(clean(line[2:]), H1))
        elif line.startswith("## "):
            out.append(Paragraph(clean(line[3:]), H2))
        elif line.startswith("|"):
            cells = [clean(c.strip()) for c in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
                continue  # separator row
            out.append(Table([[Paragraph(c, CELL) for c in cells]],
                             repeatRows=0, style=TableStyle([
                                 ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                                 ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                                 ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 3),
                                 ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                             ])))
        elif line.startswith(("- ", "* ")):
            out.append(Paragraph("• " + clean(line[2:]), BODY))
        else:
            out.append(Paragraph(clean(line), BODY))
    return out


def xlsx_flowables(path: Path, landscape_mode=False):
    out = []
    wb = openpyxl.load_workbook(path, read_only=True)
    for ws in wb.worksheets:
        rows = [[c if c is not None else "" for c in r] for r in ws.iter_rows(values_only=True)]
        rows = [r for r in rows if any(str(v).strip() for v in r)]
        if not rows:
            continue
        out.append(Paragraph(f"{path.stem} — sheet: {ws.title}", H2))
        data = []
        for i, r in enumerate(rows):
            st = HEAD if i == 0 else CELL
            data.append([Paragraph(clean(str(v)), st) for v in r])
        out.append(Table(data, repeatRows=1, style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), MIDBLUE),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ])))
        out.append(Spacer(1, 4 * mm))
    return out


def build_md_pdf(src: Path, cover_color=None, cover_title=None):
    text = src.read_text(encoding="utf-8")
    doc = SimpleDocTemplate(str(OUT / (src.stem + ".pdf")), pagesize=A4,
                            leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=12 * mm, bottomMargin=12 * mm)
    story = []
    if cover_color is not None:
        t = Table([[Paragraph(cover_title, ParagraphStyle("cv", parent=H1,
                     fontSize=17, textColor=colors.white, alignment=1))],
                   [Paragraph("Virtual Battery Factory — design package (simulation fidelity: DFN)",
                              ParagraphStyle("cv2", parent=BODY, textColor=colors.white, alignment=1))]],
                  colWidths=[186 * mm], style=TableStyle([
                      ("BACKGROUND", (0, 0), (-1, -1), cover_color),
                      ("TOPPADDING", (0, 0), (-1, 0), 14),
                      ("BOTTOMPADDING", (0, -1), (-1, -1), 14),
                      ("BOX", (0, 0), (-1, -1), 1.2, COPPER),
                  ]))
        story += [t, Spacer(1, 6 * mm)]
    story += md_flowables(text)
    doc.build(story)


def build_xlsx_pdf(src: Path):
    doc = SimpleDocTemplate(str(OUT / (src.stem + ".pdf")), pagesize=landscape(A4),
                            leftMargin=10 * mm, rightMargin=10 * mm,
                            topMargin=10 * mm, bottomMargin=10 * mm)
    story = xlsx_flowables(src)
    doc.build(story)


for f in ["design_spec.md", "datasheet.md", "dvpr.md", "dfmea.md"]:
    build_md_pdf(OUT / f)
build_md_pdf(OUT / "delivery_index.md",
             cover_color=NAVY, cover_title="Delivery Package — VBF-T6R1")
for f in ["bom.xlsx", "calc.xlsx"]:
    build_xlsx_pdf(OUT / f)
print("7 PDFs written")
