"""Generate PDF release versions for all 7 deliverable categories (reportlab).

md sources: rendered line-by-line as wrapped paragraphs. xlsx sources: each sheet
rendered as a grid table. Non-Latin-1 characters sanitized for Helvetica/WinAnsi.
"""
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

SAN = {"→": "->", "≤": "<=", "≥": ">=", "×": "x", "φ": "phi",
       "–": "-", "—": "-", "−": "-", "✓": "[PASS]", "✗": "[FAIL]",
       "“": '"', "”": '"', "’": "'", "σ": "sigma", "μ": "u",
       "…": "...", "≠": "!=", "≈": "~"}

def san(s):
    s = str(s)
    for k, v in SAN.items():
        s = s.replace(k, v)
    return "".join(ch if ord(ch) < 256 else "?" for ch in s)

title_style = ParagraphStyle("t", fontSize=13, leading=16, spaceAfter=8)
body_style = ParagraphStyle("b", fontSize=7.5, leading=10, spaceAfter=2)
cell_style = ParagraphStyle("c", fontSize=6.5, leading=8)

def md_to_pdf(src, dst, title):
    with open(src, encoding="utf-8-sig") as f:
        lines = [l.rstrip() for l in f.read().splitlines()]
    story = [Paragraph(san(title), title_style), Spacer(1, 4)]
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 3))
            continue
        if line.startswith("#"):
            story.append(Paragraph(san(line.lstrip("# ")), title_style))
        else:
            story.append(Paragraph(san(line), body_style))
    doc = SimpleDocTemplate(dst, pagesize=A4, topMargin=14 * mm, bottomMargin=14 * mm,
                            leftMargin=12 * mm, rightMargin=12 * mm, title=title)
    doc.build(story)
    print("pdf:", dst)

def xlsx_to_pdf(src, dst, title):
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
    story = [Paragraph(san(title), title_style), Spacer(1, 4)]
    for ws in wb.worksheets:
        story.append(Paragraph(san(f"Sheet: {ws.title}"), title_style))
        rows = []
        for row in ws.iter_rows(values_only=True):
            rows.append([Paragraph(san(c) if c is not None else "", cell_style) for c in row])
        if rows:
            t = Table(rows, repeatRows=1, colWidths=[32 * mm] * len(rows[0]) if rows else None)
            t.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(t)
        story.append(Spacer(1, 6))
    doc = SimpleDocTemplate(dst, pagesize=A4, topMargin=14 * mm, bottomMargin=14 * mm,
                            leftMargin=12 * mm, rightMargin=12 * mm, title=title)
    doc.build(story)
    print("pdf:", dst)

base = "deliverables/"
md_to_pdf(base + "design_spec.md", base + "design_spec.pdf", "VBF-T2R1NOFORCE-DS-001 - Cell Design Specification (F1)")
xlsx_to_pdf(base + "bom.xlsx", base + "bom.pdf", "VBF-T2R1NOFORCE-BOM-001 - Bill of Materials (F1)")
md_to_pdf(base + "datasheet.md", base + "datasheet.pdf", "VBF-T2R1NOFORCE-DSH-001 - Technical Datasheet (F1)")
xlsx_to_pdf(base + "calc.xlsx", base + "calc.pdf", "VBF-T2R1NOFORCE-CALC-001 - Design Calculation Sheet (F1)")
md_to_pdf(base + "dvpr.md", base + "dvpr.pdf", "VBF-T2R1NOFORCE-DVPR-001 - Design Verification Report (F1)")
md_to_pdf(base + "dfmea.md", base + "dfmea.pdf", "VBF-T2R1NOFORCE-DFMEA-001 - Design FMEA (F1)")
md_to_pdf(base + "delivery_index.md", base + "delivery_index.pdf", "VBF-T2R1NOFORCE-IDX-001 - Delivery Index")
print("all pdfs written")
