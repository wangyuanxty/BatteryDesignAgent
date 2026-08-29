# -*- coding: utf-8 -*-
"""One-off PDF release generator for t7_r3 deliverables (reportlab; blueprint cover colors)."""
import io
import os
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

DEL = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
BLUE_D = colors.HexColor("#14283C")
BLUE_M = colors.HexColor("#1E5A8A")
COPPER = colors.HexColor("#C97B3D")

REPL = {"✓": "[PASS]", "✗": "[FAIL]", "〃": "same", "⁻": "-", "⁹": "9", "⁺": "+",
        "ε": "eps", "σ": "sigma", "∫": "int", "Σ": "SUM", "⋯": "...", "Ω": "ohm",
        "≈": "~", "—": "-", "“": '"', "”": '"', "・": ".", "（": "(", "）": ")",
        "；": ";", "：": ":", "→": "->", "←": "<-", "⌄": "", "｜": "|", "∈": "in",
        "≥": ">=", "≤": "<="}

def tmap(s):
    for k, v in REPL.items():
        s = s.replace(k, v)
    return s

TITLE = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=20, leading=26,
                       textColor=colors.white)
SUB = ParagraphStyle("sub", fontName="Helvetica", fontSize=11, leading=15,
                     textColor=colors.HexColor("#D8E4F0"))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=17,
                    textColor=BLUE_D, spaceAfter=6, spaceBefore=10)
BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13)
MONO = ParagraphStyle("mono", fontName="Courier", fontSize=7.6, leading=9.6)

def cover(title, number, extra=""):
    t = Table([[""]], colWidths=[160 * mm], rowHeights=[26 * mm], style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_D)]))
    numstyle = ParagraphStyle("num", parent=SUB, fontSize=13, textColor=COPPER)
    vnstyle = ParagraphStyle("vn", parent=SUB, fontSize=9)
    return [t, Spacer(1, 8 * mm), Paragraph(tmap(title), TITLE), Spacer(1, 3 * mm),
            Paragraph(tmap(number), numstyle), Spacer(1, 1.5 * mm),
            Paragraph(tmap(extra), SUB), Spacer(1, 40 * mm),
            Paragraph("Prepared: ____________    Reviewed: ____________    Approved: ____________",
                      SUB), Spacer(1, 4 * mm),
            Paragraph("Virtual design package - simulation caliber (no physical build)", vnstyle)]

def render_md(src, dst, title, number):
    lines = io.open(src, encoding="utf-8").read().splitlines()
    doc = SimpleDocTemplate(dst, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title=title, author="Virtual Battery Factory")
    els = cover(title, number)
    els.append(PageBreak())
    i = 0
    rows = []
    while i < len(lines):
        ln = lines[i]
        is_table = (ln.strip().startswith("|") and i + 1 < len(lines)
                    and lines[i + 1].strip().startswith("|"))
        if is_table:
            rows = [ln]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i]); i += 1
            cells_all = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            body_rows = [r for r in cells_all if not all(set(c) <= set("-: ") for c in r)]
            for r in body_rows:
                els.append(Paragraph(tmap("  " + " | ".join(r)), MONO))
            els.append(Spacer(1, 2.2 * mm))
            continue
        s = ln.strip()
        if s.startswith("### "):
            els.append(Paragraph(tmap(s[4:]), BODY))
        elif s.startswith("## "):
            els.append(Paragraph(tmap(s[3:]), H1))
        elif s.startswith("# "):
            els.append(Paragraph(tmap(s[2:]), ParagraphStyle("h0", parent=H1, fontSize=16,
                       textColor=BLUE_M)))
        elif s == "":
            els.append(Spacer(1, 1.6 * mm))
        else:
            els.append(Paragraph(tmap(s), BODY))
        i += 1
    doc.build(els)

def render_xlsx(src, dst, title, number):
    wb = openpyxl.load_workbook(src, read_only=True)
    doc = SimpleDocTemplate(dst, pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm, title=title)
    els = cover(title, number)
    els.append(PageBreak())
    for ws in wb.worksheets:
        rows = [[tmap(str(c.value)) if c.value is not None else "" for c in r] for r in ws.iter_rows()]
        if not rows:
            continue
        els.append(Paragraph(tmap("%s - %s" % (number, ws.title)), H1))
        data = rows[:22]
        colw = [170 * mm / max(1, len(data[0]))] * len(data[0])
        t = Table(data, colWidths=colw, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLUE_D),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 6.6),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AAFC4")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EFF3F8")]),
        ]))
        els.append(t)
        els.append(Spacer(1, 4 * mm))
        if rows and len(rows) > 22:
            els.append(Paragraph("(table truncated in PDF release; full data in xlsx source)",
                                 BODY))
        els.append(PageBreak())
    doc.build(els)

META = {
    "design_spec.md": ("design_spec.pdf", "Cell Design Specification - HEV Battery (virtual)",
                       "VBF-T7R3-DS-01", "Case t7_r3  |  2026-08-26"),
    "datasheet.md": ("datasheet.pdf", "Technical Datasheet - HEV Battery Cell (virtual)",
                     "VBF-T7R3-DSH-01", "Case t7_r3  |  2026-08-26"),
    "dvpr.md": ("dvpr.pdf", "Design Verification Plan & Report (virtual-test version)",
                "VBF-T7R3-DVPR-01", "Case t7_r3  |  2026-08-26"),
    "dfmea.md": ("dfmea.pdf", "Design FMEA (qualitative, simulation-signal basis)",
                 "VBF-T7R3-DFMEA-01", "Case t7_r3  |  2026-08-26"),
    "delivery_index.md": ("delivery_index.pdf", "Delivery Index",
                          "VBF-T7R3-IDX-01", "Case t7_r3  |  2026-08-26"),
    "bom.xlsx": ("bom.pdf", "Bill of Materials", "VBF-T7R3-BOM-01", "Case t7_r3  |  2026-08-26"),
    "calc.xlsx": ("calc.pdf", "Design Calculation Sheet", "VBF-T7R3-CALC-01",
                  "Case t7_r3  |  2026-08-26"),
}

for src, (dst, title, num, extra) in META.items():
    if src.endswith(".md"):
        render_md(os.path.join(DEL, src), os.path.join(DEL, dst), title, num + " " + extra)
    else:
        render_xlsx(os.path.join(DEL, src), os.path.join(DEL, dst), title, num + " " + extra)
    sz = os.path.getsize(os.path.join(DEL, dst))
    print("%-22s -> %-20s %6.1f KB" % (src, dst, sz / 1024.0))
    assert sz > 1024, "PDF too small: " + dst
print("all PDF releases written")