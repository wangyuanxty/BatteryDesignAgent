"""PDF release generation for all deliverables (reportlab, blueprint colors)."""
import re
import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

DLV = r"runs\exp\t5_r3\deliverables"
DEEP = colors.HexColor("#14283C")
MID = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")

def sanitize(s):
    s = str(s)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for a, b in [("→", "-&gt;"), ("←", "&lt;-"), ("≤", "&lt;="), ("≥", "&gt;="),
                 ("≈", "~"), ("✓", "(PASS) "), ("✗", "(FAIL)"), ("’", "'"), ("“", '"'), ("”", '"')]:
        s = s.replace(a, b)
    return s

ST = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, textColor=DEEP, spaceAfter=8, spaceBefore=6),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, textColor=MID, spaceAfter=6, spaceBefore=10),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10, textColor=COPPER, spaceAfter=4, spaceBefore=8),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9, leading=12, spaceAfter=4),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=7.5, leading=9),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=7.5, leading=9),
}

def md_to_pdf(src, dst):
    with open(f"{DLV}\\{src}", encoding="utf-8") as f:
        lines = f.read().splitlines()
    doc = SimpleDocTemplate(f"{DLV}\\{dst}", pagesize=A4, leftMargin=1.4 * cm,
                            rightMargin=1.4 * cm, topMargin=1.4 * cm, bottomMargin=1.4 * cm,
                            title=sanitize(src))
    story = []
    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        if not ln or ln == "---" or set(ln) <= {"-"}:
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(cells)
                i += 1
            header, body_rows = rows[0], rows[1:]
            data = [[Paragraph(sanitize(c), ST["cellb"]) if j == 0 and r == 0 else
                     Paragraph(sanitize(c), ST["cell"] if j == 0 else ST["cell"])
                     for j, c in enumerate(r)] for r in rows]
            ncol = max(len(r) for r in rows)
            avail = A4[0] - 2.8 * cm
            widths = [avail * 0.32] + [avail * 0.68 / max(1, ncol - 1)] * max(1, ncol - 1)
            for r in data:
                r.extend([""] * (ncol - len(r)))
            t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), MID),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9FB3C8")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EFF4F8")]),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
            continue
        if ln.startswith("### "):
            story.append(Paragraph(sanitize(ln[4:]), ST["h3"])); i += 1; continue
        if ln.startswith("## "):
            story.append(Paragraph(sanitize(ln[3:]), ST["h2"])); i += 1; continue
        if ln.startswith("# "):
            story.append(Paragraph(sanitize(ln[2:]), ST["h1"])); i += 1; continue
        if ln.startswith("- ") or ln.startswith("* "):
            txt = sanitize(ln[2:])
            story.append(Paragraph(f"<bullet>&bull;</bullet>{txt}", ParagraphStyle(
                "b", parent=ST["body"], leftIndent=14, bulletIndent=4, spaceAfter=2)))
            i += 1
            continue
        story.append(Paragraph(sanitize(ln), ST["body"]))
        i += 1
    doc.build(story)
    print("built", dst)

def xlsx_to_pdf(src, dst):
    wb = openpyxl.load_workbook(f"{DLV}\\{src}", read_only=True, data_only=True)
    doc = SimpleDocTemplate(f"{DLV}\\{dst}", pagesize=A4, leftMargin=1.3 * cm,
                            rightMargin=1.3 * cm, topMargin=1.3 * cm, bottomMargin=1.3 * cm,
                            title=sanitize(src))
    story = [Paragraph(sanitize(src.replace(".xlsx", "")), ST["h1"]), Spacer(1, 8)]
    for sh in wb.worksheets:
        rows = [[c for c in r] for r in sh.iter_rows(values_only=True)]
        rows = [r for r in rows if any(v not in (None, "") for v in r)]
        if not rows:
            continue
        story.append(Paragraph(sanitize(sh.title), ST["h2"]))
        data = [[Paragraph(sanitize(v), ST["cellb"]) if r == 0 or j == 0 else
                 Paragraph(sanitize(v), ST["cell"]) for j, v in enumerate(row)] for r, row in enumerate(rows)]
        ncol = max(len(r) for r in rows)
        avail = A4[0] - 2.6 * cm
        widths = [avail * 0.3] + [avail * 0.7 / max(1, ncol - 1)] * max(1, ncol - 1)
        for r in data:
            r.extend([""] * (ncol - len(r)))
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), MID),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9FB3C8")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EFF4F8")]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))
    doc.build(story)
    print("built", dst)

md_to_pdf("design_spec.md", "design_spec.pdf")
md_to_pdf("datasheet.md", "datasheet.pdf")
md_to_pdf("dvpr.md", "dvpr.pdf")
md_to_pdf("dfmea.md", "dfmea.pdf")
xlsx_to_pdf("bom.xlsx", "bom.pdf")
xlsx_to_pdf("calc.xlsx", "calc.pdf")
md_to_pdf("delivery_index.md", "delivery_index.pdf")
print("ALL PDFS DONE")