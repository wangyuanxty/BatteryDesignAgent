"""Minimal markdown -> PDF converter (reportlab) for VBF deliverables."""
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted
)

BASE = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_flash\deliverables")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=15, spaceAfter=8, textColor=colors.HexColor("#1a1a2e"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12.5, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor("#16213e"))
H3 = ParagraphStyle("H3", parent=ss["Heading3"], fontSize=11, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#0f3460"))
BODY = ParagraphStyle("BODY", parent=ss["BodyText"], fontSize=9.5, leading=13, spaceAfter=5)
CODE = ParagraphStyle("CODE", parent=ss["Code"], fontSize=8, leading=10, backColor=colors.HexColor("#f4f4f4"))
LI = ParagraphStyle("LI", parent=BODY, leftIndent=14, bulletIndent=4, spaceAfter=2)


def esc(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    return t


def parse_table(rows):
    headers = [c.strip() for c in rows[0]]
    data = [[Paragraph(esc(c), BODY) for c in headers]]
    for r in rows[1:]:
        data.append([Paragraph(esc(c), BODY) for c in r])
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16213e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def convert(md_path: Path, pdf_path: Path):
    lines = md_path.read_text(encoding="utf-8-sig").splitlines()
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=16*mm, rightMargin=16*mm,
                            topMargin=14*mm, bottomMargin=14*mm,
                            title=md_path.stem)
    story = []
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    i += 1
                    continue
                rows.append(cells)
                i += 1
            story.append(parse_table(rows))
            story.append(Spacer(1, 5))
            continue
        m = re.match(r"^(#{1,3})\s+(.*)", ln)
        if m:
            level, txt = len(m.group(1)), m.group(2)
            story.append(Paragraph(esc(txt), {1: H1, 2: H2, 3: H3}[level]))
            i += 1
            continue
        if re.match(r"^\s*[-*]\s+", ln):
            story.append(Paragraph("&bull; " + esc(re.sub(r"^\s*[-*]\s+", "", ln)), LI))
            i += 1
            continue
        if re.match(r"^\s*\d+\.\s+", ln):
            story.append(Paragraph("&bull; " + esc(re.sub(r"^\s*\d+\.\s+", "", ln)), LI))
            i += 1
            continue
        if ln.startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            story.append(Preformatted("\n".join(code), CODE))
            continue
        story.append(Paragraph(esc(ln), BODY))
        i += 1
    doc.build(story)
    print(f"PDF: {pdf_path.name} ({pdf_path.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    for md in BASE.glob("*.md"):
        if md.name == "README.md":
            continue
        convert(md, md.with_suffix(".pdf"))
    print("done")
