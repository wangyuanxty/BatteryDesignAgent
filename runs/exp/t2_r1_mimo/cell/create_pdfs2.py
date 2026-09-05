import os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ddir = "runs/exp/t2_r1_mimo/deliverables"

DEEP_BLUE = HexColor("#14283C")
MED_BLUE = HexColor("#1E5A8A")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=16, textColor=DEEP_BLUE)
heading_style = ParagraphStyle("CustomHeading", parent=styles["Heading2"], fontSize=12, textColor=MED_BLUE)
body_style = styles["Normal"]
small_style = ParagraphStyle("Small", parent=body_style, fontSize=8)

def md_to_pdf(md_path, pdf_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           leftMargin=15*mm, rightMargin=15*mm,
                           topMargin=15*mm, bottomMargin=15*mm)
    story = []

    table_rows = []
    in_table = False

    def flush_table():
        nonlocal table_rows, in_table
        if table_rows:
            # Filter out separator rows
            data_rows = [r for r in table_rows if not all(hasattr(c, 'text') and c.text.strip().replace("-","") == "" for c in r)]
            if data_rows:
                t = Table(data_rows, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), MED_BLUE),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor("#F0F4F8")]),
                ]))
                story.append(t)
            table_rows = []
            in_table = False

    for line in lines:
        line = line.rstrip("\n")
        stripped = line.strip()

        if not stripped:
            flush_table()
            story.append(Spacer(1, 4))
        elif stripped.startswith("# "):
            flush_table()
            story.append(Paragraph(stripped[2:], title_style))
        elif stripped.startswith("## "):
            flush_table()
            story.append(Paragraph(stripped[3:], heading_style))
        elif stripped.startswith("### "):
            flush_table()
            story.append(Paragraph(stripped[4:], heading_style))
        elif stripped.startswith("| "):
            cells = [re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', c.strip()) for c in stripped.split("|")[1:-1]]
            row = [Paragraph(c, small_style) for c in cells]
            table_rows.append(row)
            in_table = True
        elif stripped.startswith("- "):
            flush_table()
            story.append(Paragraph(f"• {stripped[2:]}", body_style))
        else:
            flush_table()
            text = stripped
            import re
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            story.append(Paragraph(text, body_style))

    flush_table()
    doc.build(story)

for md_file in ["design_spec.md", "datasheet.md", "dvpr.md", "dfmea.md", "delivery_index.md"]:
    md_path = os.path.join(ddir, md_file)
    pdf_file = md_file.replace(".md", ".pdf")
    pdf_path = os.path.join(ddir, pdf_file)
    try:
        md_to_pdf(md_path, pdf_path)
        size = os.path.getsize(pdf_path)
        print(f"OK {pdf_file} ({size} bytes)")
    except Exception as e:
        print(f"FAIL {pdf_file}: {e}")

print("Done")
