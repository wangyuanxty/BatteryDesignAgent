"""Generate PDF releases (reportlab) for all deliverables + copy report.html + delivery_index.md."""
import shutil
from pathlib import Path

import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

CASE = "t8_r3"
OUT = Path("runs/exp/t8_r3/deliverables")
BLUE, COPPER = colors.HexColor("#1E5A8A"), colors.HexColor("#C97B3D")

styles = getSampleStyleSheet()
h1 = styles["Title"]; h2 = styles["Heading2"]; body = styles["BodyText"]


def md_to_pdf(md_path: Path, pdf_path: Path, title):
    text = md_path.read_text(encoding="utf-8").splitlines()
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            title=title, author="Virtual Battery Factory")
    story = [Paragraph(title, h1), Spacer(1, 4 * mm)]
    i = 0
    while i < len(text):
        line = text[i].rstrip()
        if not line:
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(text) and set(text[i + 1].replace("|", "").strip()) <= {"-", ":"}:
            rows = []
            j = i
            while j < len(text) and text[j].strip().startswith("|"):
                if set(text[j].replace("|", "").strip()) <= {"-", ":", " "}:
                    j += 1
                    continue
                cells = [c.strip() for c in text[j].strip().strip("|").split("|")]
                rows.append(cells)
                j += 1
            if rows:
                t = Table(rows, repeatRows=1)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EAF1F7")]),
                ]))
                story.append(t)
                story.append(Spacer(1, 2 * mm))
            i = j
            continue
        if line.startswith("#"):
            lvl = line.count("#", 0, 4)
            story.append(Paragraph(line.lstrip("# "), h2 if lvl <= 2 else styles["Heading3"]))
            story.append(Spacer(1, 1.5 * mm))
        elif line.startswith(("- ", "* ")):
            story.append(Paragraph(line[2:], body))
        else:
            story.append(Paragraph(line, body))
        i += 1
    doc.build(story)


def xlsx_to_pdf(xlsx_path: Path, pdf_path: Path, title):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, title=title,
                            author="Virtual Battery Factory")
    story = [Paragraph(title, h1), Spacer(1, 4 * mm)]
    for ws in wb.worksheets:
        story.append(Paragraph(f"Sheet: {ws.title}", h2))
        rows = list(ws.iter_rows(values_only=True))
        if rows:
            t = Table([[str(c) if c is not None else "" for c in r] for r in rows], repeatRows=1)
            wmax = max(len(r) for r in rows)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), COPPER),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(t)
        story.append(Spacer(1, 3 * mm))
    doc.build(story)


# report.html ancillary copy
shutil.copy("runs/exp/t8_r3/report.html", OUT / "report.html")
print("copied report.html")

pairs = [
    ("design_spec.md", "design_spec.pdf", "Cell Design Specification — t8_r3 (VBF-T8R3-DS-01)"),
    ("bom.xlsx", "bom.pdf", "Bill of Materials — t8_r3 (VBF-T8R3-BOM-01)"),
    ("datasheet.md", "datasheet.pdf", "Technical Datasheet — t8_r3 V13 porousanode (VBF-T8R3-DSH-01)"),
    ("calc.xlsx", "calc.pdf", "Design Calculation Sheet — t8_r3 (VBF-T8R3-CALC-01)"),
    ("dvpr.md", "dvpr.pdf", "Design Verification Plan and Report — t8_r3 (VBF-T8R3-DVPR-01)"),
    ("dfmea.md", "dfmea.pdf", "Design FMEA — t8_r3 (VBF-T8R3-DFMEA-01)"),
]
for src, dst, title in pairs:
    p = OUT / src
    if p.suffix == ".md":
        md_to_pdf(p, OUT / dst, title)
    else:
        xlsx_to_pdf(p, OUT / dst, title)
    print("pdf:", dst, (OUT / dst).stat().st_size, "bytes")

# ---------- delivery_index.md (written once all files incl. index pdf slot exist except itself) ----------
idx_rows = [
    ["design_spec.md", "VBF-T8R3-DS-01", "md", "generated per deliverable-design-spec spec (values from Chen2020 parameter set + r4 sim outputs)"],
    ["design_spec.pdf", "VBF-T8R3-DS-01", "pdf", "md→pdf via reportlab release"],
    ["report.html", "VBF-T8R3-DS-02", "html", "bda render log.jsonl audience report (copied into deliverables/)"],
    ["bom.xlsx", "VBF-T8R3-BOM-01", "xlsx", "openpyxl; component masses from calc-energy layer_kg_m2 + parameter set; AM/CB/binder split literature defaults"],
    ["bom.pdf", "VBF-T8R3-BOM-01", "pdf", "xlsx→pdf via reportlab release"],
    ["datasheet.md", "VBF-T8R3-DSH-01", "md", "generated per deliverable-datasheet spec"],
    ["datasheet.pdf", "VBF-T8R3-DSH-01", "pdf", "md→pdf via reportlab release"],
    ["calc.xlsx", "VBF-T8R3-CALC-01", "xlsx", "openpyxl; 5 sheets: inputs / capacity-energy / energy density / NP-mass / process"],
    ["calc.pdf", "VBF-T8R3-CALC-01", "pdf", "xlsx→pdf via reportlab release"],
    ["dvpr.md", "VBF-T8R3-DVPR-01", "md", "generated per deliverable-dvpr spec (virtual version); N/A items stated"],
    ["dvpr.pdf", "VBF-T8R3-DVPR-01", "pdf", "md→pdf via reportlab release"],
    ["dfmea.md", "VBF-T8R3-DFMEA-01", "md", "generated per deliverable-dfmea spec (qualitative)"],
    ["dfmea.pdf", "VBF-T8R3-DFMEA-01", "pdf", "md→pdf via reportlab release"],
    ["delivery_index.md", "VBF-T8R3-IDX-01", "md", "this file (cover + controlled file list)"],
    ["delivery_index.pdf", "VBF-T8R3-IDX-01", "pdf", "md→pdf via reportlab release"],
]
idx = []
idx.append("# Delivery Package Index — t8_r3 (VBF-T8R3-IDX-01)\n")
idx.append("| Field | Value |")
idx.append("|---|---|")
idx.append(f"| Case name | {CASE} |")
idx.append("| Numbering scheme | VBF-&lt;CASE-ID-UPPER&gt;-&lt;DOC-CODE&gt;-&lt;SEQ&gt; → VBF-T8R3-DS-01 style |")
idx.append("| Generation date | 2026-08-26 |")
idx.append("| Prepared / Reviewed / Approved | (blank) / (blank) / (blank) — left for manual signing |\n")
idx.append("## Document code reference\n")
idx.append("| Code | Meaning | File |")
idx.append("|---|---|---|")
for code, meaning, fname in [
    ("DS", "Specification", "design_spec.md"),
    ("BOM", "Bill of Materials", "bom.xlsx"),
    ("DSH", "Datasheet", "datasheet.md"),
    ("CALC", "Calculation sheet", "calc.xlsx"),
    ("DVPR", "Design verification report", "dvpr.md"),
    ("DFMEA", "Failure analysis", "dfmea.md"),
    ("IDX", "Delivery index", "delivery_index.md"),
]:
    idx.append(f"| {code} | {meaning} | {fname} |")
idx.append("\nCAD (cell_model.stl): not requested (zero-interaction session, no structure-model clarification) — not produced, not registered.\n")
idx.append("## File list\n")
idx.append("| File | Number | Format | Source |")
idx.append("|---|---|---|---|")
for r in idx_rows:
    idx.append("| " + " | ".join(r) + " |")
idx_text = "\n".join(idx) + "\n"
(OUT / "delivery_index.md").write_text(idx_text, encoding="utf-8")

# index pdf
md_to_pdf(OUT / "delivery_index.md", OUT / "delivery_index.pdf",
          "Delivery Package Index — t8_r3 (VBF-T8R3-IDX-01)")
print("delivery_index.md/pdf written")
print("final deliverables:", sorted(p.name for p in OUT.iterdir()))