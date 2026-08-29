# PDF release versions of all deliverables + delivery_index.md/pdf
# Minimal markdown -> PDF renderer (headings / tables / paragraphs / bold), CJK via STSong-Light CID font.
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

ROOT = Path(__file__).parent
OUT = ROOT / "deliverables"

H1 = ParagraphStyle("h1", fontName="STSong-Light", fontSize=16, leading=22, spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="STSong-Light", fontSize=13, leading=18, spaceBefore=8, spaceAfter=4)
H3 = ParagraphStyle("h3", fontName="STSong-Light", fontSize=11, leading=15, spaceBefore=6, spaceAfter=3)
BODY = ParagraphStyle("body", fontName="STSong-Light", fontSize=9.5, leading=14, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="STSong-Light", fontSize=8.5, leading=11)
HEAD = ParagraphStyle("head", fontName="STSong-Light", fontSize=8.5, leading=11)

def inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`]+)`", r"<font face='Courier'>\1</font>", s)
    return s

def md_to_flowables(text):
    flow = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in row):
                    tbl.append(row)
                i += 1
            if tbl:
                ncol = max(len(r) for r in tbl)
                data = [[Paragraph(inline((r[c] if c < len(r) else "")), HEAD if ri == 0 else CELL) for c in range(ncol)] for ri, r in enumerate(tbl)]
                t = Table(data, repeatRows=1, hAlign="LEFT")
                t.setStyle(TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDEBF7")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]))
                flow.append(t)
                flow.append(Spacer(1, 4))
            continue
        if ln.startswith("### "):
            flow.append(Paragraph(inline(ln[4:]), H3)); i += 1; continue
        if ln.startswith("## "):
            flow.append(Paragraph(inline(ln[3:]), H2)); i += 1; continue
        if ln.startswith("# "):
            flow.append(Paragraph(inline(ln[2:]), H1)); i += 1; continue
        if ln.strip() == "---":
            i += 1; continue
        if ln.lstrip().startswith("- "):
            flow.append(Paragraph(inline("• " + ln.strip()[2:]), BODY)); i += 1; continue
        flow.append(Paragraph(inline(ln), BODY)); i += 1
    return flow

def md_to_pdf(md_path, pdf_path):
    text = Path(md_path).read_text(encoding="utf-8")
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title=md_path.stem)
    doc.build(md_to_flowables(text))

# ---------- delivery index ----------
files = [
    ("design_spec.md", "VBF-T7R1FLASH-DS-001", "Markdown（可编辑源）", "电芯设计规格书：体系/电极/工艺/质量/性能验证（值取自参数集与仿真输出，逐行标注来源）"),
    ("datasheet.md", "VBF-T7R1FLASH-DSH-001", "Markdown（可编辑源）", "技术数据表：容量/能量/密度/快充/安全判定（循环寿命如实标注 Not simulated）"),
    ("dvpr.md", "VBF-T7R1FLASH-DVPR-001", "Markdown（可编辑源）", "设计验证计划与报告（虚拟测试版）：12 项验证，7 项仿真覆盖 + 4 项 N/A 如实标注"),
    ("dfmea.md", "VBF-T7R1FLASH-DFMEA-001", "Markdown（可编辑源）", "设计 FMEA（定性版，基于仿真信号）：5 项失效模式 + 缓解措施"),
    ("bom.xlsx", "VBF-T7R1FLASH-BOM-001", "Excel（可编辑源）", "物料清单：双口径 g/电芯 与 kg/kWh；导电剂/粘结剂配比文献默认并标注"),
    ("calc.xlsx", "VBF-T7R1FLASH-CALC-001", "Excel（可编辑源）", "设计计算书：输入参数/容量能量/能量密度/NP与质量/工艺参数，逐格来源列"),
    ("design_spec.pdf", "VBF-T7R1FLASH-DS-001", "PDF（发布版）", "design_spec.md 的发布版"),
    ("datasheet.pdf", "VBF-T7R1FLASH-DSH-001", "PDF（发布版）", "datasheet.md 的发布版"),
    ("dvpr.pdf", "VBF-T7R1FLASH-DVPR-001", "PDF（发布版）", "dvpr.md 的发布版"),
    ("dfmea.pdf", "VBF-T7R1FLASH-DFMEA-001", "PDF（发布版）", "dfmea.md 的发布版"),
    ("bom.pdf", "VBF-T7R1FLASH-BOM-001", "PDF（发布版）", "bom.xlsx 的发布版（数据同源）"),
    ("calc.pdf", "VBF-T7R1FLASH-CALC-001", "PDF（发布版）", "calc.xlsx 的发布版（数据同源）"),
]
idx = """# 交付物索引 Delivery Index

**案例**: VBF-T7-R1-FLASH · **生成日期**: 2026-08-25 · **版本**: 1.0

**封面信息**: 案例名 HEV 电池设计（虚拟电池工厂 VBF 协议，case t7_r1_flash）；编号方案 VBF-<CASE-ID-UPPER>-<doc-code>-<serial>；签名栏留空（虚拟测试版）。

## 文件清单

| 文件名 | 编号 | 格式 | 来源说明 |
|---|---|---|---|
""" + "\n".join(f"| {f} | {n} | {fmt} | {src} |" for f, n, fmt, src in files) + """

## 结论摘要

FC-4a 通过全部 4 项合同指标（机械判定，值均来自仿真输出文件）：
- 能量密度 **427.04 Wh/kg** ≥ 327.18 ✓（r3_fc4a_energy.json）
- 4C 快充无析锂 **+28.5 mV** ≥ 0 ✓（r3_fc4a_4c_dfn.json, DFN）
- SEI 100 圈 45 °C **496.9 nm** ≤ 550 ✓（r3_fc4a_aging45.json）
- 针刺 10 W 无热失控 **triggered=false**（T_max 309.2 / 322.7 K）✓（r3_fc4a_nail.json / _hot.json）

报告与审计链：`../report.html`（七节 HTML 报告，由 log.jsonl 确定性渲染）；`../log.jsonl`（全部审计条目）。
"""
(OUT / "delivery_index.md").write_text(idx, encoding="utf-8")

# ---------- generate PDFs ----------
for name in ("design_spec", "datasheet", "dvpr", "dfmea", "delivery_index"):
    md_to_pdf(OUT / f"{name}.md", OUT / f"{name}.pdf")

# xlsx -> PDF (data-same-source render)
import openpyxl
for xlsx_name, pdf_name in (("bom.xlsx", "bom.pdf"), ("calc.xlsx", "calc.pdf")):
    wb = openpyxl.load_workbook(OUT / xlsx_name)
    pages = []
    for ws in wb.worksheets:
        rows = [[c.value for c in row] for row in ws.iter_rows() if any(c.value is not None for c in row)]
        if not rows:
            continue
        data = [[Paragraph(inline(str(c)) if c is not None else "", HEAD if ri == 0 else CELL) for c in r] for ri, r in enumerate(rows)]
        t = Table(data, hAlign="LEFT", repeatRows=1)
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDEBF7")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        pages.append(Paragraph(f"Sheet: {ws.title}", H2))
        pages.append(t)
        pages.append(Spacer(1, 8))
    doc = SimpleDocTemplate(str(OUT / pdf_name), pagesize=A4,
                            leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=15 * mm, bottomMargin=15 * mm, title=pdf_name)
    doc.build(pages)

print("PDFs + index written:", sorted(p.name for p in OUT.iterdir()))
for p in sorted(OUT.glob("*.pdf")):
    print(" ", p.name, p.stat().st_size, "bytes")
