# PDF release generation for t2_r3 deliverables (reportlab, engineering-blueprint style)
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
import html as _html
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak)

D = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t2_r3")
DEL = D / "deliverables"
NAVY = HexColor("#14283C"); MID = HexColor("#1E5A8A"); COPPER = HexColor("#C97B3D")

def esc(s):
    return _html.escape(str(s))

ss = getSampleStyleSheet()
st_title = ParagraphStyle("t", parent=ss["Title"], fontSize=15, leading=19, textColor=white)
st_sub = ParagraphStyle("s", parent=ss["Normal"], fontSize=8, leading=10, textColor=HexColor("#9FB3C8"))
st_h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=12, leading=15, textColor=MID, spaceAfter=4, spaceBefore=8)
st_h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=10, leading=13, textColor=NAVY, spaceAfter=2, spaceBefore=6)
st_p = ParagraphStyle("p", parent=ss["Normal"], fontSize=8.5, leading=11.5, spaceAfter=3)
st_q = ParagraphStyle("q", parent=ss["Normal"], fontSize=8, leading=11, textColor=MID, spaceAfter=4, leftIndent=4)
st_cell = ParagraphStyle("c", parent=ss["Normal"], fontSize=6.8, leading=8.6)
st_cell_b = ParagraphStyle("cb", parent=st_cell, fontName="Helvetica-Bold")

def header(doc, doc_code, title, subtitle):
    story = []
    t = Table(
        [[Paragraph(title, st_title)],
         [Paragraph(subtitle, st_sub)]],
        colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBELOW", (0, 0), (-1, -1), 1.2, COPPER),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 3 * mm))
    return story

def md_story(md_path, doc_code, title):
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    story = header(doc_code, doc_code, title, f"VBF Case t2_r3 | {doc_code} | Virtual simulation calibre | Generated 2026-08-26")
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("# "):
            story.append(Paragraph(esc(ln[2:]), st_h1)); i += 1; continue
        if ln.startswith("## "):
            story.append(Paragraph(esc(ln[2:]), st_h2)); i += 1; continue
        if ln.startswith(">"):
            story.append(Paragraph(esc(ln.lstrip("> ")), st_q)); i += 1; continue
        if ln.startswith("|"):
            j = i
            rows = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                row = lines[j].strip()
                if not all(c in "|-: " for c in row):
                    cells = [c.strip() for c in row.strip("|").split("|")]
                    rows.append([Paragraph(esc(c), st_cell) for c in cells])
                j += 1
            if rows:
                ncol = max(len(r) for r in rows)
                w = 170 * mm / ncol
                tbl = Table(rows, colWidths=[w] * ncol, repeatRows=0)
                tbl.setStyle(TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#B8C6D4")),
                    ("BACKGROUND", (0, 0), (-1, 0), MID),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                ]))
                def white_first(cell, txt):
                    pass
                for r in range(len(rows)):
                    for c in range(ncol):
                        if r == 0:
                            rows[r][c].style = st_cell_b
                            rows[r][c].textColor = white
                story.append(tbl)
                story.append(Spacer(1, 2 * mm))
            i = j; continue
        if ln.strip() == "":
            story.append(Spacer(1, 1.2 * mm)); i += 1; continue
        story.append(Paragraph(esc(ln), st_p)); i += 1
    return story

def xlsx_story(xlsx_path, doc_code, title, max_cols=4, drop_col=None):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    story = header(doc_code, doc_code, title, f"VBF Case t2_r3 | {doc_code} | Virtual simulation calibre | Generated 2026-08-26")
    for ws in wb.worksheets:
        rows = []
        for row in ws.iter_rows(values_only=True):
            if all(v is None or str(v).strip() == "" for v in row):
                continue
            cells = list(row)[:max_cols]
            if drop_col is not None:
                cells = [cells[i] for i in range(len(cells)) if i != drop_col]
            rows.append([Paragraph(esc(v) if v is not None else "", st_cell) for v in cells])
        if not rows:
            continue
        story.append(Paragraph(f"Sheet: {esc(ws.title)}", st_h2))
        ncol = max(len(r) for r in rows)
        w = 170 * mm / ncol
        tbl = Table(rows, colWidths=[w] * ncol)
        tbl.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#B8C6D4")),
            ("BACKGROUND", (0, 0), (-1, 0), MID),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 1.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ]))
        for r in range(len(rows)):
            for c in range(ncol):
                if r == 0:
                    rows[r][c].style = st_cell_b
                    rows[r][c].textColor = white
        story.append(tbl)
        story.append(Spacer(1, 2 * mm))
        story.append(PageBreak())
    return story

def build(pdf_name, story):
    out = DEL / pdf_name
    doc = SimpleDocTemplate(str(out), pagesize=A4,
                            leftMargin=14 * mm, rightMargin=14 * mm, topMargin=12 * mm, bottomMargin=14 * mm,
                            title=pdf_name)
    doc.build(story)
    print(pdf_name, out.stat().st_size, "bytes")

build("design_spec.pdf", md_story(DEL / "design_spec.md", "VBF-T2R3-DS-01", "Cell Design Specification — combo-v5-final (t2_r3)"))
build("dvpr.pdf", md_story(DEL / "dvpr.md", "VBF-T2R3-DVPR-01", "Design Verification Plan and Report (virtual)"))
build("dfmea.pdf", md_story(DEL / "dfmea.md", "VBF-T2R3-DFMEA-01", "Design FMEA (qualitative, simulation-signal based)"))
build("bom.pdf", xlsx_story(DEL / "bom.xlsx", "VBF-T2R3-BOM-01", "Bill of Materials", drop_col=4))
build("calc.pdf", xlsx_story(DEL / "calc.xlsx", "VBF-T2R3-CALC-01", "Design Calculation Sheet"))
build("datasheet.pdf", md_story(DEL / "datasheet_docx_content.md", "VBF-T2R3-DSH-01", "Technical Datasheet — Grid Energy Storage Cell"))
build("delivery_index.pdf", md_story(DEL / "delivery_index.md", "VBF-T2R3-IDX-01", "Delivery Package Index"))
print("ALL PDFs done")