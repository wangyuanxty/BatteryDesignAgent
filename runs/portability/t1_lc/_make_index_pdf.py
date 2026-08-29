from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

DEL = Path("runs/portability/t1_lc/deliverables")
DEEP = colors.HexColor("#14283C")
MID = colors.HexColor("#1E5A8A")


def sanitize(s):
    return (s.replace("≥", ">=").replace("≤", "<=").replace("✓", "[PASS]")
            .replace("→", "->").replace("°", " deg ").replace("µm", "um")
            .replace("×", "x").replace("−", "-"))


lines = (DEL / "delivery_index.md").read_text(encoding="utf-8").splitlines()
doc = SimpleDocTemplate(str(DEL / "delivery_index.pdf"), pagesize=A4,
                        leftMargin=18*mm, rightMargin=18*mm,
                        topMargin=16*mm, bottomMargin=16*mm)
styles = getSampleStyleSheet()
h1 = styles["Title"]; h1.textColor = colors.white; h1.fontSize = 15
h2 = styles["Heading2"]; h2.textColor = MID
body = styles["BodyText"]; body.fontSize = 8.5; body.leading = 11
story = []
header = Table([[Paragraph('<font color="white"><b>VBF-T1LC-IDX-01</b><br/>Delivery Index</font>', h1)]],
               colWidths=[174*mm])
header.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DEEP),
    ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(header)
story.append(Spacer(1, 4*mm))
for ln in lines:
    s = sanitize(ln.rstrip("\n"))
    if not s.strip():
        story.append(Spacer(1, 2))
    elif s.startswith("# "):
        story.append(Paragraph(f"<b>{s[2:]}</b>", h2))
    elif s.startswith("## "):
        story.append(Paragraph(f"<b>{s[3:]}</b>", h2))
    else:
        story.append(Paragraph(s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), body))
doc.build(story)
print("delivery_index.pdf written")
