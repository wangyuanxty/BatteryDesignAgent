import re
from pathlib import Path
import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle)

D = Path("runs/portability/t6_oa/deliverables")

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Title"], fontSize=15, spaceAfter=8, textColor=colors.HexColor("#14283C"))
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, spaceAfter=6, textColor=colors.HexColor("#1E5A8A"))
BODY = ParagraphStyle("BODY", parent=styles["BodyText"], fontSize=8.5, leading=11, spaceAfter=4)
BULLET = ParagraphStyle("BULLET", parent=BODY, leftIndent=12, bulletIndent=4)
QUOTE = ParagraphStyle("QUOTE", parent=BODY, textColor=colors.HexColor("#C97B3D"))

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render_md(src, dst):
    lines = src.read_text(encoding="utf-8-sig").splitlines()
    story = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            continue
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("### "):
            story.append(Paragraph(esc(s[4:]), H2)); i += 1; continue
        if s.startswith("## "):
            story.append(Paragraph(esc(s[3:]), H2)); i += 1; continue
        if s.startswith("# "):
            story.append(Paragraph(esc(s[2:]), H1)); i += 1; continue
        if s.startswith("|"):
            # table block
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not any(re.fullmatch(r":?-{2,}:?", c or "") for c in row):
                    tbl.append([esc(c) for c in row])
                i += 1
            if tbl:
                t = Table(tbl, repeatRows=1)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1E5A8A")),
                    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                    ("FONTSIZE", (0,0), (-1,-1), 7),
                    ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#9AA7B5")),
                    ("VALIGN", (0,0), (-1,-1), "TOP"),
                ]))
                story.append(t); story.append(Spacer(1, 6))
            continue
        if s.startswith("- "):
            story.append(Paragraph("• " + esc(s[2:]), BULLET)); i += 1; continue
        if s.startswith("> "):
            story.append(Paragraph(esc(s[2:]), QUOTE)); i += 1; continue
        story.append(Paragraph(esc(s), BODY)); i += 1
    doc = SimpleDocTemplate(str(dst), pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
    doc.build(story)

def render_xlsx(src, dst):
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
    story = [Paragraph(esc(src.stem), H1)]
    for ws in wb.worksheets:
        story.append(Paragraph("Sheet: " + esc(ws.title), H2))
        data = []
        for row in ws.iter_rows(values_only=True):
            data.append([("" if c is None else esc(str(c))) for c in row])
        if not data:
            continue
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#14283C")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTSIZE", (0,0), (-1,-1), 6.5),
            ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#9AA7B5")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(t); story.append(Spacer(1, 8))
    doc = SimpleDocTemplate(str(dst), pagesize=A4, leftMargin=12*mm, rightMargin=12*mm, topMargin=15*mm, bottomMargin=15*mm)
    doc.build(story)

for name in ["design_spec", "datasheet", "dvpr", "dfmea", "delivery_index"]:
    render_md(D / f"{name}.md", D / f"{name}.pdf")
    print("pdf:", name)

for name in ["bom", "calc"]:
    render_xlsx(D / f"{name}.xlsx", D / f"{name}.pdf")
    print("pdf:", name)
print("done")
