import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import re

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           leftMargin=20*mm, rightMargin=20*mm,
                           topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=16, spaceAfter=12)
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, spaceAfter=8)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14)

    def safe_para(text):
        """Escape XML entities and strip markdown bold markers."""
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Convert **text** to bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        return text

    lines = content.split('\n')
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            t = Table(table_rows)
            style_cmds = [
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#14283C')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f0f0')]),
            ]
            t.setStyle(TableStyle(style_cmds))
            story.append(t)
            story.append(Spacer(1, 6))
            table_rows = []
            in_table = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('# ') and not stripped.startswith('## '):
            flush_table()
            story.append(Paragraph(safe_para(stripped[2:]), title_style))
        elif stripped.startswith('## '):
            flush_table()
            story.append(Paragraph(safe_para(stripped[3:]), h2_style))
        elif stripped.startswith('### '):
            flush_table()
            story.append(Paragraph(safe_para(stripped[4:]), h2_style))
        elif stripped.startswith('|') and '|' in stripped[1:]:
            cells = [safe_para(c.strip()) for c in stripped.split('|')[1:-1]]
            if all(c.replace('-','').replace(' ','') == '' for c in cells):
                continue
            table_rows.append(cells)
            in_table = True
        elif stripped.startswith('- ') or stripped.startswith('* '):
            flush_table()
            story.append(Paragraph(safe_para(f"• {stripped[2:]}"), body_style))
        elif stripped:
            flush_table()
            story.append(Paragraph(safe_para(stripped), body_style))

    flush_table()
    doc.build(story)
    print(f"  Generated: {pdf_path}")

base = "runs/exp/t8_r1_mimo/deliverables"
files = {
    "design_spec.md": "design_spec.pdf",
    "datasheet.md": "datasheet.pdf",
    "dvpr.md": "dvpr.pdf",
    "dfmea.md": "dfmea.pdf",
    "delivery_index.md": "delivery_index.pdf",
}

for md_name, pdf_name in files.items():
    md_path = os.path.join(base, md_name)
    pdf_path = os.path.join(base, pdf_name)
    if os.path.exists(md_path):
        md_to_pdf(md_path, pdf_path)

# Generate PDFs from xlsx
for xlsx_name in ["bom.xlsx", "calc.xlsx"]:
    xlsx_path = os.path.join(base, xlsx_name)
    pdf_name = xlsx_name.replace(".xlsx", ".pdf")
    pdf_path = os.path.join(base, pdf_name)
    if os.path.exists(xlsx_path):
        import openpyxl
        wb = openpyxl.load_workbook(xlsx_path)
        doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                               leftMargin=15*mm, rightMargin=15*mm,
                               topMargin=15*mm, bottomMargin=15*mm)
        styles = getSampleStyleSheet()
        story = []
        for ws_name in wb.sheetnames:
            ws = wb[ws_name]
            story.append(Paragraph(ws_name, styles['Heading1']))
            data = []
            for row in ws.iter_rows(values_only=True):
                data.append([str(c) if c is not None else "" for c in row])
            if data:
                t = Table(data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#14283C')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                    ('FONTSIZE', (0,0), (-1,-1), 8),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ]))
                story.append(t)
            story.append(Spacer(1, 10))
        doc.build(story)
        print(f"  Generated: {pdf_path}")

print("All PDFs generated successfully")
