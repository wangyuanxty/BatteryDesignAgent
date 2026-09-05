"""Convert markdown deliverables to PDF using reportlab."""
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

DELIVERABLES_DIR = r'D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_mimo\deliverables'

def md_table_to_data(md_text):
    """Parse a markdown table into a list of lists."""
    lines = [l.strip() for l in md_text.strip().split('\n') if l.strip()]
    data = []
    for line in lines:
        if line.startswith('|') and not set(line.replace('|','').replace('-','').replace(':','').strip()):
            continue  # skip separator line
        if line.startswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            data.append(cells)
    return data

def md_to_pdf(md_path, pdf_path):
    """Convert a markdown file to PDF."""
    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           topMargin=20*mm, bottomMargin=20*mm,
                           leftMargin=15*mm, rightMargin=15*mm)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=16, spaceAfter=12)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=13, spaceAfter=8, spaceBefore=12)
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=9, spaceAfter=4)
    small_style = ParagraphStyle('Small', parent=styles['Normal'], fontSize=8, spaceAfter=2)

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Title (# heading)
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))
            i += 1
            continue

        # Section heading (## or ###)
        if line.startswith('## ') or line.startswith('### '):
            text = line.lstrip('#').strip()
            story.append(Paragraph(text, heading_style))
            i += 1
            continue

        # Table
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            table_text = '\n'.join(table_lines)
            data = md_table_to_data(table_text)
            if data:
                # Limit column count to prevent overflow
                max_cols = max(len(row) for row in data)
                # Normalize rows to same column count
                normalized = []
                for row in data:
                    while len(row) < max_cols:
                        row.append('')
                    normalized.append(row[:min(max_cols, 6)])  # Max 6 columns

                col_width = (A4[0] - 30*mm) / min(max_cols, 6)
                t = Table(normalized, colWidths=[col_width]*min(max_cols, 6))
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTSIZE', (0, 0), (-1, -1), 7),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ]))
                story.append(t)
                story.append(Spacer(1, 6))
            continue

        # Horizontal rule
        if line.startswith('---'):
            story.append(Spacer(1, 8))
            i += 1
            continue

        # Bold text
        text = line
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)

        # Bullet points
        if line.startswith('- ') or line.startswith('* '):
            text = '• ' + line[2:]
            story.append(Paragraph(text, body_style))
            i += 1
            continue

        # Numbered list
        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if m:
            text = f'{m.group(1)}. {m.group(2)}'
            story.append(Paragraph(text, body_style))
            i += 1
            continue

        # Regular text
        story.append(Paragraph(text, body_style))
        i += 1

    doc.build(story)
    print(f'  Created: {os.path.basename(pdf_path)} ({os.path.getsize(pdf_path)} bytes)')

# Convert all deliverables
files = [
    ('design_spec.md', 'design_spec.pdf'),
    ('bom.md', 'bom.pdf'),
    ('datasheet.md', 'datasheet.pdf'),
    ('calc_sheet.md', 'calc_sheet.pdf'),
    ('dvpr.md', 'dvpr.pdf'),
    ('dfmea.md', 'dfmea.pdf'),
    ('delivery_index.md', 'delivery_index.pdf'),
]

for md_name, pdf_name in files:
    md_path = os.path.join(DELIVERABLES_DIR, md_name)
    pdf_path = os.path.join(DELIVERABLES_DIR, pdf_name)
    if os.path.exists(md_path):
        md_to_pdf(md_path, pdf_path)
    else:
        print(f'  SKIP: {md_name} not found')

print('\nAll PDFs generated.')
