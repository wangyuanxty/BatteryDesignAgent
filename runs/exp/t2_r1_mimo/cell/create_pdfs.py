import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

ddir = "runs/exp/t2_r1_mimo/deliverables"

# Blueprint style colors
DEEP_BLUE = HexColor("#14283C")
MED_BLUE = HexColor("#1E5A8A")
COPPER = HexColor("#C97B3D")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=16, textColor=DEEP_BLUE)
heading_style = ParagraphStyle("CustomHeading", parent=styles["Heading2"], fontSize=12, textColor=MED_BLUE)
body_style = styles["Normal"]

def md_to_pdf(md_path, pdf_path):
    """Convert markdown table-style content to simple PDF."""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           leftMargin=20*mm, rightMargin=20*mm,
                           topMargin=20*mm, bottomMargin=20*mm)
    story = []

    for line in content.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
        elif line.startswith("# "):
            story.append(Paragraph(line[2:], title_style))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], heading_style))
        elif line.startswith("| ") and "---" not in line:
            # Table row
            cells = [c.strip() for c in line.split("|")[1:-1]]
            row = [Paragraph(c, body_style) for c in cells]
            story.append(row)
        elif line.startswith("**") and line.endswith("**"):
            story.append(Paragraph(line.replace("**", "<b>").replace("**", "</b>"), body_style))
        elif line.startswith("- "):
            story.append(Paragraph(f"• {line[2:]}", body_style))
        else:
            story.append(Paragraph(line, body_style))

    # Build with table styling
    doc.build(story)

# Create PDFs for each deliverable
for md_file in ["design_spec.md", "datasheet.md", "dvpr.md", "dfmea.md", "delivery_index.md"]:
    md_path = os.path.join(ddir, md_file)
    pdf_file = md_file.replace(".md", ".pdf")
    pdf_path = os.path.join(ddir, pdf_file)
    try:
        md_to_pdf(md_path, pdf_path)
        size = os.path.getsize(pdf_path)
        print(f"Created {pdf_file} ({size} bytes)")
    except Exception as e:
        print(f"FAILED {pdf_file}: {e}")

print("\nDone creating PDFs")
