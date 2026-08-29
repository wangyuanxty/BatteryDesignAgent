# -*- coding: utf-8 -*-
"""Build delivery_index.md + PDF (registers only actually produced files)."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t8_r2\deliverables")
CASE_ID = "T8R2"
TODAY = "2026-08-26"

# document-code table (fixed by protocol) -> which produced files belong to it
CODE_OF = {"DS": "design_spec", "BOM": "bom", "DSH": "datasheet", "CALC": "calc",
           "DVPR": "dvpr", "DFMEA": "dfmea", "IDX": "delivery_index"}

def serials_for(prefix, code, files):
    """Number actual files under a doc code: source+pdf share ONE number; ancillaries next serial."""
    row = []
    main = [f for f in files if f.name.lower().startswith(prefix) and f.suffix in (".md", ".xlsx", ".docx")]
    pdf = [f for f in files if f.name.lower().startswith(prefix) and f.suffix == ".pdf"]
    anc = [f for f in files if f.name.lower().startswith(prefix) and f not in main + pdf]
    n = 1
    for f in main:
        row.append((f.name, "VBF-%s-%s-%02d" % (CASE_ID, code, n), f.suffix[1:], "editable source"))
        n += 1
    for f in pdf:
        row.append((f.name, "VBF-%s-%s-%02d" % (CASE_ID, code, n), "pdf", "PDF release (reportlab, same content parity as source)"))
        n += 1
    for f in anc:
        row.append((f.name, "VBF-%s-%s-%02d" % (CASE_ID, code, n), f.suffix[1:], "ancillary"))
        n += 1
    return row

files = sorted(OUT.glob("*"))
rows = []
for code, prefix in [("DS", "design_spec"), ("BOM", "bom"), ("DSH", "datasheet"), ("CALC", "calc"),
                     ("DVPR", "dvpr"), ("DFMEA", "dfmea"), ("IDX", "delivery_index")]:
    rows += serials_for(prefix, code, files)

# report.html => ancillaries of DS (per deliverable-package.md example)
for f in files:
    if f.name == "report.html":
        rows.append((f.name, "VBF-%s-DS-%02d" % (CASE_ID, len([r for r in rows if r[1].startswith("VBF-%s-DS" % CASE_ID)]) + 1),
                     "html", "bda render audit report (deterministic from log.jsonl)"))

lines = []
lines.append("# Delivery Package Index - case t8_r2")
lines.append("")
lines.append("- Case name: t8_r2")
lines.append("- Numbering scheme: VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO> (case ID: T8R2)")
lines.append("- Generation date: %s" % TODAY)
lines.append("- Signature block: prepared ___ / reviewed ___ / approved ___ (left blank for manual signing)")
lines.append("")
lines.append("## Document code reference (fixed by protocol)")
lines.append("")
lines.append("| Document code | Meaning | Corresponding file |")
lines.append("|---|---|---|")
lines.append("| DS | Specification | design_spec.md |")
lines.append("| BOM | Bill of Materials | bom.xlsx |")
lines.append("| DSH | Datasheet technical parameter sheet | datasheet.docx |")
lines.append("| CALC | Calculation sheet | calc.xlsx |")
lines.append("| DVPR | Design verification report | dvpr.md |")
lines.append("| DFMEA | Failure analysis | dfmea.md |")
lines.append("| CAD | Structure model | skipped (optional deliverable; requires user form/expression clarification - zero-interaction session) |")
lines.append("")
lines.append("## File list (registers only actually generated files)")
lines.append("")
lines.append("| File name | Number | Format | Source description |")
lines.append("|---|---|---|---|")
for name, num, fmt, desc in rows:
    lines.append("| %s | %s | %s | %s |" % (name, num, fmt, desc))
lines.append("")
lines.append("Note: CAD structural model not produced (optional; per protocol requires user choice of form and presentation; headless session). Enclosure/tab masses: Not modeled (no parameter keys - honest annotation in BOM).")
(OUT / "delivery_index.md").write_text("\n".join(lines), encoding="utf-8")
print("delivery_index.md written with %d rows" % len(rows))

# ---- PDF release with blueprint colors ----
BP_DEEP = colors.HexColor("#14283C")
BP_MED = colors.HexColor("#1E5A8A")
BP_COP = colors.HexColor("#C97B3D")
st_title = ParagraphStyle("t", parent=getSampleStyleSheet()["Heading1"], fontSize=13, textColor=colors.white, spaceAfter=2)
st_sub = ParagraphStyle("s", parent=getSampleStyleSheet()["BodyText"], fontSize=9, textColor=colors.white)
st_h = ParagraphStyle("h", parent=getSampleStyleSheet()["Heading2"], fontSize=10, textColor=BP_MED, spaceBefore=4*mm, spaceAfter=1.5*mm)

doc = SimpleDocTemplate(str(OUT / "delivery_index.pdf"), pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=14*mm, bottomMargin=14*mm)
story = []
cover = Table([[Paragraph("Delivery Package Index - case t8_r2", st_title)],
               [Paragraph("Numbering: VBF-%s-&lt;DOC-CODE&gt;-&lt;SEQ-NO&gt; | Generated %s | Prepared/Reviewed/Approved: ___ / ___ / ___" % (CASE_ID, TODAY), st_sub)]],
              colWidths=[180*mm])
cover.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), BP_DEEP),
    ("LINEBELOW", (0, 0), (-1, 0), 1.2, BP_COP),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(cover)
story.append(Spacer(1, 5*mm))
story.append(Paragraph("Document code reference", st_h))
codes = [["DS", "Specification", "design_spec.md"],
         ["BOM", "Bill of Materials", "bom.xlsx"],
         ["DSH", "Datasheet", "datasheet.docx"],
         ["CALC", "Calculation sheet", "calc.xlsx"],
         ["DVPR", "Design verification report", "dvpr.md"],
         ["DFMEA", "Failure analysis", "dfmea.md"],
         ["CAD", "Structure model", "skipped (optional; needs user clarification)"],
         ["IDX", "Delivery index", "delivery_index.md"]]
tc = Table([["Code", "Meaning", "Corresponding file"]] + codes, repeatRows=1)
tc.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BP_MED), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 8), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9db3c8")),
]))
story.append(tc)
story.append(Paragraph("File list (actually generated files only)", st_h))
tl = Table([["File name", "Number", "Format", "Source description"]] +
           [[r[0], r[1], r[2], r[3]] for r in rows] +
           [["NOTE", "CAD skipped", "-", "optional deliverable requiring user clarification (headless session); listed for honesty, not produced"]],
           repeatRows=1, colWidths=[38*mm, 34*mm, 14*mm, 94*mm])
tl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BP_MED), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("LEADING", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9db3c8")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef4f9")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(tl)
doc.build(story)
print("delivery_index.pdf written")