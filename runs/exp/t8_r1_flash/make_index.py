"""Generate delivery_index.md + delivery_index.pdf (blueprint cover style)."""
import json

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

BASE = "runs/exp/t8_r1_flash"
DD = f"{BASE}/deliverables"
D = json.load(open(f"{BASE}/final_data.json", encoding="utf-8"))
S = D["sim"]
CASE_ID = "T8R1FLASH"
DATE = "2026-08-25"

rows = [
    ("design_spec.md", "VBF-T8R1FLASH-DS-01", "md", "generated per deliverable-design-spec spec; values from parameter set + cell/r1_v4_*.json (mechanical)"),
    ("design_spec.pdf", "VBF-T8R1FLASH-DS-01", "pdf", "md -> pdf release (reportlab)"),
    ("report.html", "VBF-T8R1FLASH-DS-02", "html", "bda render from log.jsonl (audit report, seven sections)"),
    ("delivery_index.md", "VBF-T8R1FLASH-DS-03", "md", "package cover + controlled file list (this file)"),
    ("delivery_index.pdf", "VBF-T8R1FLASH-DS-03", "pdf", "md -> pdf release, blueprint cover style (reportlab)"),
    ("bom.xlsx", "VBF-T8R1FLASH-BOM-01", "xlsx", "openpyxl from final_data.json (g/cell + kg/kWh, per-line source column)"),
    ("bom.pdf", "VBF-T8R1FLASH-BOM-01", "pdf", "xlsx -> pdf release (reportlab)"),
    ("datasheet.md", "VBF-T8R1FLASH-DSH-01", "md", "generated per deliverable-datasheet spec; simulation-verified values"),
    ("datasheet.pdf", "VBF-T8R1FLASH-DSH-01", "pdf", "md -> pdf release (reportlab)"),
    ("calc.xlsx", "VBF-T8R1FLASH-CALC-01", "xlsx", "openpyxl: inputs/capacity&energy/ED/N-P&mass/process sheets, formula+source columns"),
    ("calc.pdf", "VBF-T8R1FLASH-CALC-01", "pdf", "xlsx -> pdf release (reportlab)"),
    ("dvpr.md", "VBF-T8R1FLASH-DVPR-01", "md", "virtual-test verification report; per-row source to cell/r1_v4_*.json"),
    ("dvpr.pdf", "VBF-T8R1FLASH-DVPR-01", "pdf", "md -> pdf release (reportlab)"),
    ("dfmea.md", "VBF-T8R1FLASH-DFMEA-01", "md", "qualitative FMEA from simulation risk signals"),
    ("dfmea.pdf", "VBF-T8R1FLASH-DFMEA-01", "pdf", "md -> pdf release (reportlab)"),
]
# CAD model: skipped (headless zero-interaction; user clarification not available)

md = f"""# Delivery Index — VBF-{CASE_ID}

**Case name**: t8_r1_flash — long-endurance drone battery (energy density ≥ 446.18 Wh/kg, 5C discharge retention ≥ 90%, cell mass ≤ 40 g)
**Design**: V4 Thermal-tuned — NMC811/graphite, nano particles, high-transport electrolyte, thin collectors, flatter-pouch cooling
**Key results**: ED {S['ed_wh_kg']:.1f} Wh/kg | 5C retention {S['retention_5c']*100:.1f} % | mass {S['mass_kg']*1000:.1f} g | 4C-charge T_max {S['tmax_4c_K']:.2f} K | no plating | **verdict: achieved**
**Generation date**: {DATE}
**Numbering scheme**: VBF-{CASE_ID}-<DOC-CODE>-<SEQ-NO> (uppercase case ID, non-alphanumerics removed)

| File | Number | Format | Source description |
|---|---|---|---|
""" + "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows) + """

**Notes**
- CAD structure model: not generated (optional deliverable requiring user clarification; headless run — honestly skipped).
- Signature block: prepared / reviewed / approved — left blank for manual signing.
- Official release format = PDF; editable sources retained (md/xlsx).
"""
open(f"{DD}/delivery_index.md", "w", encoding="utf-8").write(md)

# -------- PDF (blueprint cover) --------
DEEP, MID, COPPER = colors.HexColor("#14283C"), colors.HexColor("#1E5A8A"), colors.HexColor("#C97B3D")
st_t = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=20, textColor=colors.white, leading=24)
st_sub = ParagraphStyle("s", fontName="Helvetica", fontSize=10, textColor=colors.white, leading=13)
st_h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=12, textColor=MID, spaceBefore=10, spaceAfter=4)
st_c = ParagraphStyle("c", fontName="Helvetica", fontSize=7.5, leading=9)

doc = SimpleDocTemplate(f"{DD}/delivery_index.pdf", pagesize=A4, leftMargin=14*mm, rightMargin=14*mm,
                        topMargin=14*mm, bottomMargin=14*mm)
story = []
cover = Table([[Paragraph(f"VBF Delivery Package — {CASE_ID}", st_t)],
               [Paragraph(f"Long-endurance drone battery · V4 Thermal-tuned · {DATE}", st_sub)],
               [Paragraph(f"ED {S['ed_wh_kg']:.1f} Wh/kg · 5C retention {S['retention_5c']*100:.1f}% · mass {S['mass_kg']*1000:.1f} g · 4C T_max {S['tmax_4c_K']:.1f} K · verdict: achieved", st_sub)]],
              colWidths=[182*mm])
cover.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), DEEP),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("LINEBELOW", (0, -1), (-1, -1), 2, COPPER),
]))
story += [cover, Spacer(1, 8), Paragraph("File list (VBF numbering)", st_h)]
data = [[Paragraph(c, st_c) for c in ("File", "Number", "Format", "Source")]]
for a, b, c, d in rows:
    data.append([Paragraph(a, st_c), Paragraph(b, st_c), Paragraph(c, st_c), Paragraph(d, st_c)])
t = Table(data, colWidths=[38*mm, 40*mm, 16*mm, 88*mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), MID),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9DB4C4")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF3F7")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(t)
story.append(Spacer(1, 8))
story.append(Paragraph("Signature: prepared ______ / reviewed ______ / approved ______ (left blank for manual signing)", st_c))
doc.build(story)
print("delivery_index.md + delivery_index.pdf OK")
