import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ddir = "runs/exp/t2_r1_mimo/deliverables"
MED_BLUE = HexColor("#1E5A8A")
styles = getSampleStyleSheet()
title_style = ParagraphStyle("Title2", parent=styles["Title"], fontSize=14, textColor=HexColor("#14283C"))
small_style = ParagraphStyle("Small", parent=styles["Normal"], fontSize=8)

def xlsx_to_pdf(xlsx_path, pdf_path, title):
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm,
                           topMargin=15*mm, bottomMargin=15*mm)
    story = [Paragraph(title, title_style), Spacer(1, 10)]

    data = []
    for row in ws.iter_rows(values_only=True):
        data.append([Paragraph(str(c or ""), small_style) for c in row])

    if data:
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), MED_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor("#F0F4F8")]),
        ]))
        story.append(t)

    doc.build(story)

xlsx_to_pdf(f"{ddir}/bom.xlsx", f"{ddir}/bom.pdf", "Bill of Materials")
xlsx_to_pdf(f"{ddir}/calc.xlsx", f"{ddir}/calc.pdf", "Design Calculation Sheet")

print("Created bom.pdf and calc.pdf")
