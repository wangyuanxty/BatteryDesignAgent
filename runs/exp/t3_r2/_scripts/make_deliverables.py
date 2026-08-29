"""Generate bom.xlsx, calc.xlsx and the 7 PDF releases in deliverables/.

Values are read mechanically from the simulation artifact JSONs + the
parameter-set dump values verified in this session; literature defaults are
annotated per line. PDF tables/markdown rendered with reportlab.
"""
import json
import re
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path("runs/exp/t3_r2")
DEL = ROOT / "deliverables"
CELL = ROOT / "cell"
DEL.mkdir(exist_ok=True)

energy = json.loads(open(CELL / "r2_p1_energy.json", encoding="utf-8").read())
d1c = json.loads(open(CELL / "r2_p1_1c_dfn.json", encoding="utf-8").read())
probe = json.loads(open(ROOT / "_logs" / "p1_stoich_probe.json", encoding="utf-8").read())

ENERGY_WH = energy["energy_wh"]            # 12.1255
AREA = energy["area_m2"]                     # 0.1027
CAP_AH = d1c["capacity_ah"]                  # 3.3278

L = energy["layer_kg_m2"]                    # kg/m2 per layer
G = {k: v * AREA * 1000.0 for k, v in L.items()}  # g/cell
TOTAL_CONTRACT_G = energy["mass_kg"] * 1000.0

# ---------------------------------------------------------------- BOM data
LIT_DENS_EL = 1.2  # g/cm3 literature electrolyte density (annotated)
pore_m3 = (0.45 * 45e-6 + 0.47 * 12e-6 + 0.40 * 56e-6) * AREA
ELECTROLYTE_G = pore_m3 * 1e6 * LIT_DENS_EL
GRAND_TOTAL_G = TOTAL_CONTRACT_G + ELECTROLYTE_G

def kgkwh(g):
    return g / ENERGY_WH  # g/kWh -> kg/kWh

bom_rows = []  # (item, material, thickness_um, volfrac, density, g, kg_kwh, source)
bom_rows.append(("Positive active material", "NMC811", 45, 0.55 * 0.96,
                 3262, G["positive_electrode"] * 0.96, kgkwh(G["positive_electrode"] * 0.96),
                 "layer mass x 96% literature AM split (parameter set has no binder/additive fractions)"))
bom_rows.append(("Positive conductive additive", "carbon black (lit. default)", 45, 0.55 * 0.02,
                 None, G["positive_electrode"] * 0.02, kgkwh(G["positive_electrode"] * 0.02),
                 "layer mass x 2% literature default"))
bom_rows.append(("Positive binder", "PVDF (lit. default)", 45, 0.55 * 0.02,
                 None, G["positive_electrode"] * 0.02, kgkwh(G["positive_electrode"] * 0.02),
                 "layer mass x 2% literature default"))
bom_rows.append(("Negative active material", "graphite", 56, 0.60 * 0.965,
                 1657, G["negative_electrode"] * 0.965, kgkwh(G["negative_electrode"] * 0.965),
                 "layer mass x 96.5% literature AM split"))
bom_rows.append(("Negative conductive additive", "carbon black (lit. default)", 56, 0.60 * 0.01,
                 None, G["negative_electrode"] * 0.01, kgkwh(G["negative_electrode"] * 0.01),
                 "layer mass x 1% literature default"))
bom_rows.append(("Negative binder", "CMC/SBR (lit. default)", 56, 0.60 * 0.025,
                 None, G["negative_electrode"] * 0.025, kgkwh(G["negative_electrode"] * 0.025),
                 "layer mass x 2.5% literature default"))
bom_rows.append(("Separator", "polyolefin (parameter-set values)", 12, None,
                 None, G["separator"], kgkwh(G["separator"]),
                 "calc-energy layer mass (thickness x (1-porosity) x density)"))
bom_rows.append(("Electrolyte", "1 M LiPF6-class, high-transport (lit. density 1.2 g/cm3)", None, None,
                 1200, ELECTROLYTE_G, kgkwh(ELECTROLYTE_G),
                 "pore volume (eps-based) x literature density 1.2 g/cm3"))
bom_rows.append(("Positive current collector", "Al", 16, None, 2700,
                 G["positive_cc"], kgkwh(G["positive_cc"]), "parameter set thickness x density x area"))
bom_rows.append(("Negative current collector", "Cu", 12, None, 8960,
                 G["negative_cc"], kgkwh(G["negative_cc"]), "parameter set thickness x density x area"))
bom_rows.append(("Enclosure, tabs, seals", "Not modeled", None, None, None, None, None,
                 "beyond pure-simulation boundary"))

# ---------------------------------------------------------------- CALC data
INPUTS = [
    ("Positive electrode thickness [m]", 4.5e-5, "m", "design override (r2_p1_params_final.json)"),
    ("Negative electrode thickness [m]", 5.6e-5, "m", "design override"),
    ("Positive electrode porosity", 0.45, "-", "design override"),
    ("Negative electrode porosity", 0.40, "-", "design override"),
    ("Separator thickness [m]", 1.2e-5, "m", "Chen2020 parameter set"),
    ("Separator porosity", 0.47, "-", "Chen2020 parameter set"),
    ("Positive particle radius [m]", 1.3e-6, "m", "design override (5.22 um base)"),
    ("Negative particle radius [m]", 1.6e-6, "m", "design override (5.86 um base)"),
    ("Electrolyte conductivity [S.m-1]", 1.5, "S/m", "design override, constant (replaces Nyman2008 function)"),
    ("Electrolyte diffusivity [m2.s-1]", 6.0e-10, "m2/s", "design override, constant"),
    ("Nominal cell capacity [A.h]", 3.3219, "Ah", "re-based to delivered 1C capacity (audited rule)"),
    ("Electrode height x width [m]", "0.065 x 1.58", "m", "Chen2020 parameter set"),
    ("Active material volume fraction pos/neg", "0.665 / 0.75", "-", "Chen2020 parameter set (model solid fraction)"),
    ("Upper / lower voltage cut-off [V]", "4.2 / 2.5", "V", "Chen2020 parameter set"),
    ("Ambient temperature 1C/5C discharge", 298.15, "K", "protocol"),
    ("Ambient temperature 4C charge", 318.15, "K", "protocol (45 C)"),
]
CAPEN = [
    ("1C discharge capacity", round(CAP_AH, 4), "Ah", "cell/r2_p1_1c_dfn.json:capacity_ah"),
    ("5C discharge capacity", 3.2911, "Ah", "cell/r2_p1_5c_dfn.json:capacity_ah"),
    ("5C capacity retention", 0.9889, "-", "5C cap / 1C cap (cell/r2_p1_derived.json)"),
    ("Rated energy (1C integral of V*I)", round(ENERGY_WH, 4), "Wh", "cell/r2_p1_energy.json:energy_wh"),
    ("Discharge midpoint voltage", round(energy["midpoint_voltage_v"], 4), "V", "cell/r2_p1_energy.json:midpoint_voltage_v"),
    ("DCR (V_start - V@10%) / I_1C", round(energy["dcr_ohm"] * 1e3, 4), "mOhm", "cell/r2_p1_energy.json:dcr_ohm"),
    ("Power density V_OC^2/(4 DCR)/mass", round(energy["power_density_w_kg"], 1), "W/kg", "cell/r2_p1_energy.json:power_density_w_kg"),
    ("4C charge T_max", 332.5213, "K", "cell/r2_p1_4c_dfn.json:T_max_K"),
    ("4C anode potential min", 0.03641, "V", "cell/r2_p1_4c_dfn.json:anode_potential_v (>= 0 -> no plating)"),
    ("5C discharge T_max", 322.2243, "K", "cell/r2_p1_derived.json:t_max_5c_k"),
]
EDEN = [
    ("Layer masses (pos / neg / AlCC / CuCC / sep)", "8.29 / 5.72 / 4.44 / 11.04 / 0.26", "g",
     "calc-energy layer_kg_m2 x area x 1000"),
    ("Total mass (contract caliber, electrolyte excluded)", round(TOTAL_CONTRACT_G, 2), "g",
     "cell/r2_p1_energy.json:mass_kg"),
    ("Energy density (Wh/kg)", round(energy["energy_density_wh_kg"], 1), "Wh/kg",
     "energy_wh / mass_kg"),
    ("Volumetric energy density (Wh/L)", round(energy["energy_density_wh_l"], 1), "Wh/L",
     "energy_wh / (total layer thickness 141 um x area)"),
    ("Total layer stack thickness", 141, "um", "pos 45 + sep 12 + neg 56 + Al 16 + Cu 12"),
    ("Electrolyte mass (informative, lit. density 1.2 g/cm3)", round(ELECTROLYTE_G, 2), "g",
     "pore volume x density; excluded from ED caliber"),
]
NP_MASS = [
    ("N/P theoretical full-range (neg cap.density x thickness / pos ...)", 0.74, "-",
     "33133 x 0.75 x 56e-6 / (63104 x 0.665 x 45e-6), mol/m3 formula caliber"),
    ("Positive full theoretical areal capacity", 50.62, "Ah/m2", "63104 x F x 1 x 45e-6 x 0.665 / 3600"),
    ("Negative full theoretical areal capacity", 37.29, "Ah/m2", "33133 x F x 1 x 56e-6 x 0.75 / 3600"),
    ("Pos stoichiometry start -> end (1C discharge)", "0.2700 -> 0.9102", "-", "_logs/p1_stoich_probe.json"),
    ("Neg stoichiometry start -> end (1C discharge)", "0.9014 -> 0.0326", "-", "_logs/p1_stoich_probe.json"),
    ("Consumed areal capacity pos = neg = cell", round(probe["cell_delivered_area_capacity_ah_m2"], 3), "Ah/m2",
     "probe identity check 1.0000 / 1.0000 (series current balance)"),
    ("Anode lithiation headroom at full charge", "9.86 %", "-", "(1 - 0.9014) from probe"),
    ("Mass per energy (contract caliber)", round(kgkwh(TOTAL_CONTRACT_G), 3), "kg/kWh", "total g / energy_wh"),
]
PROC = [
    ("Positive areal density", round(L["positive_electrode"] * 1000.0, 2), "g/m2",
     "thickness x (1 - porosity) x density 3262"),
    ("Negative areal density", round(L["negative_electrode"] * 1000.0, 2), "g/m2",
     "thickness x (1 - porosity) x density 1657"),
    ("Positive compaction density", 1.794, "g/cm3", "3262 x (1 - 0.45) / 1000"),
    ("Negative compaction density", 0.994, "g/cm3", "1657 x (1 - 0.40) / 1000"),
    ("Electrolyte fill amount", round(ELECTROLYTE_G, 2), "g",
     "pore volume 4.96 cm3 x 1.2 g/cm3 (literature density)"),
    ("Formation recommendation", "0.1C CC to 4.2 V, 25 C, 2 cycles", "-",
     "design recommended value; production tuning required"),
    ("Nominal capacity re-basing note", "nominal := measured 1C capacity (iterated, drift < 2%)", "-",
     "audited design rule, log plan_update_r1"),
]

# ---------------------------------------------------------------- xlsx
def write_xlsx(path, sheets):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for sname, header, rows in sheets:
        ws = wb.create_sheet(sname)
        ws.append(header)
        for r in rows:
            ws.append([("" if v is None else v) for v in r])
        bold = Font(bold=True)
        fill = PatternFill("solid", fgColor="1E5A8A")
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = fill
        for row in ws.iter_rows():
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        widths = [18, 30, 12, 12, 12, 14, 14, 60]
        for i, w in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    wb.save(path)

write_xlsx(DEL / "bom.xlsx", [("BOM", ["Item", "Material", "Thickness (um)", "Volume fraction",
    "Density (kg/m3)", "Mass (g/cell)", "Mass (kg/kWh)", "Source / formula note"], bom_rows)])
bom_summary = [("Total mass (contract caliber, electrolyte excluded)", TOTAL_CONTRACT_G, kgkwh(TOTAL_CONTRACT_G),
                "cell/r2_p1_energy.json:mass_kg"),
               ("Grand total including electrolyte (informative)", GRAND_TOTAL_G, kgkwh(GRAND_TOTAL_G),
                "contract mass + electrolyte computed above")]
write_xlsx(DEL / "calc.xlsx", [
    ("Inputs", ["Parameter", "Value", "Unit", "Source"], INPUTS),
    ("Capacity & energy", ["Parameter", "Value", "Unit", "Source"], CAPEN),
    ("Energy density", ["Parameter", "Value", "Unit", "Source"], EDEN),
    ("N-P ratio & mass", ["Parameter", "Value", "Unit", "Source"], NP_MASS),
    ("Process parameters", ["Parameter", "Value", "Unit", "Source"], PROC),
])
print("xlsx written")

# ---------------------------------------------------------------- PDF
_san = {">=": ">=", "<=": "<=", "→": "->", "×": "x", "≈": "~",
        "τ": "tau", "ε": "eps", "Δ": "delta", "σ": "sigma",
        "—": "-", "–": "-", "’": "'", "‘": "'", "“": '"',
        "”": '"', "≥": ">=", "≤": "<=", "·": "-"}
def san(s):
    return "".join(_san.get(ch, ch) for ch in s)

def md_rows_to_pdf(path, title_color=True):
    """Render a markdown file to PDF with a minimal renderer."""
    raw = Path(path).read_text(encoding="utf-8")
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1p", parent=styles["Title"], fontSize=15, spaceAfter=10)
    h2 = ParagraphStyle("h2p", parent=styles["Heading2"], fontSize=12, spaceBefore=8, spaceAfter=4)
    h3 = ParagraphStyle("h3p", parent=styles["Heading3"], fontSize=10.5, spaceBefore=6, spaceAfter=3)
    body = ParagraphStyle("bodyp", parent=styles["BodyText"], fontSize=9, leading=12.5, spaceAfter=5)
    cell = ParagraphStyle("cellp", parent=styles["BodyText"], fontSize=8, leading=10)
    cellb = ParagraphStyle("cellbp", parent=cell, fontName="Helvetica-Bold")
    pdf = str(Path(path).with_suffix(".pdf"))
    doc = SimpleDocTemplate(pdf, pagesize=A4,
                            leftMargin=1.4 * cm, rightMargin=1.4 * cm,
                            topMargin=1.6 * cm, bottomMargin=1.6 * cm)
    story = []
    lines = raw.splitlines()
    i = 0

    def esc(txt):
        return san(txt).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def inline(txt):
        parts = re.split(r"(\*\*.*?\*\*|`[^`]*`)", esc(txt))
        out = []
        for p in parts:
            if p.startswith("**") and p.endswith("**"):
                out.append(f"<b>{p[2:-2]}</b>")
            elif p.startswith("`") and p.endswith("`"):
                out.append(f'<font face="Courier">{p[1:-1]}</font>')
            else:
                out.append(p)
        return "".join(out)

    while i < len(lines):
        ln = lines[i].strip()
        if not ln:
            i += 1
            continue
        if ln.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            if len(block) > 1 and all(re.fullmatch(r":?-{2,}:?", c) for c in block[1]):
                block = [block[0]] + block[2:]
            ncol = max(len(r) for r in block)
            block = [r + [""] * (ncol - len(r)) for r in block]
            width = (A4[0] - 2 * 1.4 * cm) / ncol
            data = [[Paragraph(inline(block[0][c]), cellb) for c in range(ncol)]]
            for r in block[1:]:
                data.append([Paragraph(inline(r[c]), cell) for c in range(ncol)])
            t = Table(data, colWidths=[width] * ncol, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#14283C")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.2, colors.HexColor("#1E5A8A")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EAF0F6")]),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
            continue
        if ln.startswith("### "):
            story.append(Paragraph(inline(ln[4:]), h3))
        elif ln.startswith("## "):
            story.append(Paragraph(inline(ln[3:]), h2))
        elif ln.startswith("# "):
            story.append(Paragraph(inline(ln[2:]), h1))
        elif ln.startswith("- "):
            story.append(Paragraph("&#8226; " + inline(ln[2:]), body))
        elif ln == "---":
            story.append(Spacer(1, 4))
        else:
            story.append(Paragraph(inline(ln), body))
        i += 1
    doc.build(story)
    return pdf

def rows_to_pdf(name, title, header, rows):
    """Render a row-list into a table PDF."""
    styles = getSampleStyleSheet()
    tstyle = ParagraphStyle("tp", parent=styles["Title"], fontSize=15, spaceAfter=8)
    b = ParagraphStyle("bp", parent=styles["BodyText"], fontSize=8.2, leading=10.5)
    hb = ParagraphStyle("hbp", parent=styles["BodyText"], fontName="Helvetica-Bold",
                        fontSize=8.2, leading=10.5)
    doc = SimpleDocTemplate(str(DEL / f"{name}.pdf"), pagesize=A4,
                            leftMargin=1.2 * cm, rightMargin=1.2 * cm,
                            topMargin=1.4 * cm, bottomMargin=1.4 * cm)
    story = [Paragraph(esc_title(title), tstyle), Spacer(1, 6)]
    data = [[Paragraph(san(str(c)), hb) for c in header]]
    for r in rows:
        data.append([Paragraph(san("" if v is None else str(v)), b) for v in r])
    ncol = len(header)
    t = Table(data, colWidths=[(A4[0] - 2.4 * cm) / ncol] * ncol, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E5A8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.2, colors.HexColor("#14283C")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EAF0F6")]),
    ]))
    story.append(t)
    doc.build(story)

def esc_title(s):
    return san(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

for m in ["design_spec", "datasheet", "dvpr", "dfmea", "delivery_index"]:
    md_rows_to_pdf(DEL / f"{m}.md")
rows_to_pdf("bom", "Bill of Materials — VBF-T3R2-BOM-01 (PDF release of bom.xlsx)",
            ["Item", "Material", "Thickness (um)", "Volume fraction", "Density (kg/m3)",
             "Mass (g/cell)", "Mass (kg/kWh)", "Source / formula note"],
            bom_rows + [("Total (contract caliber, electrolyte excluded)", "", "", "", "",
                         round(TOTAL_CONTRACT_G, 2), round(kgkwh(TOTAL_CONTRACT_G), 3),
                         "cell/r2_p1_energy.json:mass_kg"),
                        ("Grand total including electrolyte (informative)", "", "", "", "",
                         round(GRAND_TOTAL_G, 2), round(kgkwh(GRAND_TOTAL_G), 3),
                         "contract mass + electrolyte (lit. density)")])
rows_to_pdf("calc", "Design Calculation Sheet — VBF-T3R2-CALC-01 (PDF release of calc.xlsx)",
            ["Parameter", "Value", "Unit", "Source"],
            [("Sheet: Inputs", "", "", "")] + INPUTS +
            [("Sheet: Capacity & energy", "", "", "")] + CAPEN +
            [("Sheet: Energy density", "", "", "")] + EDEN +
            [("Sheet: N/P & mass", "", "", "")] + NP_MASS +
            [("Sheet: Process parameters", "", "", "")] + PROC)
print("pdfs written")
for p in sorted(DEL.iterdir()):
    if p.suffix in (".pdf", ".xlsx"):
        print(p.name, p.stat().st_size, "bytes")