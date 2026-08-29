import json
from pathlib import Path

import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Preformatted,
)

WS = Path('runs/portability/t6_lc')
DEL = WS / 'deliverables'
DEL.mkdir(exist_ok=True)

pdfmetrics.registerFont(TTFont('Segoe', 'C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))

def sanitize(s):
    s = str(s)
    repl = {
        '℃': ' degC ', '✓': '[PASS]', '✗': '[FAIL]', '≥': '>=', '≤': '<=',
        '×': 'x', '⁻': '^-', '¹': '1', '²': '2', '³': '3', '⁴': '4',
        '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁰': '0',
        'µ': 'um', '→': '->', '—': '-', '–': '-', '·': '-',
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    return s

# ---------------- numeric data ----------------
area = 0.1027
pos_t, pos_af, pos_por, pos_dens = 57e-6, 0.665, 0.335, 4400.0
neg_t, neg_af, neg_por, neg_dens = 110e-6, 0.75, 0.25, 1657.0
sep_t, sep_por, sep_dens = 8e-6, 0.47, 1548.0
pos_cc_t, pos_cc_dens = 10e-6, 2702.0
neg_cc_t, neg_cc_dens = 8e-6, 8933.0

energy_wh = 19.935444566583183
kwh = energy_wh / 1000.0

def g(kg): return kg * 1000.0

pos_active = pos_t * area * pos_af * pos_dens
neg_active = neg_t * area * neg_af * neg_dens
sep_mass = sep_t * area * (1 - sep_por) * sep_dens
pos_cc_mass = pos_cc_t * area * pos_cc_dens
neg_cc_mass = neg_cc_t * area * neg_cc_dens
pore_vol = (pos_t * area * pos_por + neg_t * area * neg_por + sep_t * area * sep_por)
electrolyte_mass = pore_vol * 1200.0  # kg, 1.2 g/cm3 = 1200 kg/m3

# binder/conductive: literature defaults 2 wt% each vs active (annotated estimate)
pos_binder = pos_active * 2 / 96
pos_cond = pos_active * 2 / 96
neg_binder = neg_active * 2 / 96
neg_cond = neg_active * 2 / 96

total_stack_kg = pos_active + neg_active + sep_mass + pos_cc_mass + neg_cc_mass
total_with_electrolyte_kg = total_stack_kg + electrolyte_mass + pos_binder + pos_cond + neg_binder + neg_cond

def kg_per_kwh(kg): return kg / kwh

# ---------------- BOM.xlsx ----------------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'BOM'
bom_rows = [
    ['Component', 'Material', 'Mass (g/cell)', 'kg/kWh', 'Source note'],
    ['Positive active material', 'LNMO LiNi0.5Mn1.5O4', round(g(pos_active), 2), round(kg_per_kwh(pos_active), 3),
     'parameter set: thickness x area x volume fraction x density'],
    ['Positive conductive additive', 'carbon black (lit. 2 wt%)', round(g(pos_cond), 2), round(kg_per_kwh(pos_cond), 3),
     'literature default (not modeled in parameter set)'],
    ['Positive binder', 'PVDF (lit. 2 wt%)', round(g(pos_binder), 2), round(kg_per_kwh(pos_binder), 3),
     'literature default (not modeled in parameter set)'],
    ['Negative active material', 'graphite', round(g(neg_active), 2), round(kg_per_kwh(neg_active), 3),
     'parameter set'],
    ['Negative conductive additive', 'carbon black (lit. 2 wt%)', round(g(neg_cond), 2), round(kg_per_kwh(neg_cond), 3),
     'literature default (not modeled)'],
    ['Negative binder', 'SBR/CMC (lit. 2 wt%)', round(g(neg_binder), 2), round(kg_per_kwh(neg_binder), 3),
     'literature default (not modeled)'],
    ['Separator', 'polyolefin', round(g(sep_mass), 3), round(kg_per_kwh(sep_mass), 4),
     'parameter set: thickness x area x (1-porosity) x density'],
    ['Electrolyte', 'EC/EMC + LiPF6', round(g(electrolyte_mass), 2), round(kg_per_kwh(electrolyte_mass), 3),
     'pore volume x 1.2 g/cm3 (literature density)'],
    ['Positive current collector', 'Al 10 um', round(g(pos_cc_mass), 2), round(kg_per_kwh(pos_cc_mass), 3),
     'parameter set'],
    ['Negative current collector', 'Cu 8 um', round(g(neg_cc_mass), 2), round(kg_per_kwh(neg_cc_mass), 3),
     'parameter set'],
    ['Enclosure', 'pouch/housing', 'Not modeled', 'Not modeled', 'outside pure-simulation boundary'],
    ['Tabs', 'Al/Ni/Cu', 'Not modeled', 'Not modeled', 'outside pure-simulation boundary'],
    ['Total (stack, excl. electrolyte/additives)', '', round(g(total_stack_kg), 2), round(kg_per_kwh(total_stack_kg), 3), 'calc-energy mass_kg caliber'],
    ['Total (incl. electrolyte + binder/conductive)', '', round(g(total_with_electrolyte_kg), 2), round(kg_per_kwh(total_with_electrolyte_kg), 3), 'annotated'],
]
for r in bom_rows:
    ws.append(r)
for col, w in zip('ABCDE', [30, 26, 16, 12, 52]):
    ws.column_dimensions[col].width = w
wb.save(DEL / 'bom.xlsx')

# ---------------- calc.xlsx ----------------
wb2 = openpyxl.Workbook()
s_in = wb2.active; s_in.title = 'Inputs'
for r in [
    ['Parameter', 'Value', 'Source'],
    ['Positive electrode thickness [m]', 5.7e-5, 'params_final_h45.json'],
    ['Negative electrode thickness [m]', 1.10e-4, 'params_final_h45.json'],
    ['Separator thickness [m]', 8.0e-6, 'params_final_h45.json'],
    ['Positive current collector thickness [m]', 1.0e-5, 'params_final_h45.json'],
    ['Negative current collector thickness [m]', 8.0e-6, 'params_final_h45.json'],
    ['Electrode area [m2]', area, 'Electrode height x width (0.065 x 1.58)'],
    ['Positive porosity', 0.335, 'Chen2020'],
    ['Negative porosity', 0.25, 'Chen2020'],
    ['Separator porosity', 0.47, 'Chen2020'],
    ['Positive density [kg/m3]', 4400, 'LNMO.json'],
    ['Negative density [kg/m3]', 1657, 'Chen2020'],
    ['Total heat transfer coefficient [W/m2/K]', 45.0, 'params_final_h45.json'],
    ['SEI kinetic rate constant [m/s]', 1e-15, 'params_final_h45.json'],
]:
    s_in.append(r)

s_ce = wb2.create_sheet('CapacityEnergy')
for r in [
    ['Metric', 'Value', 'Source'],
    ['1C discharge capacity [Ah]', 4.804, 'final_1c_dfn_h45.json:capacity_ah'],
    ['Discharge energy [Wh]', 19.935, 'final_1c_energy_dfn_h45.json:energy_wh'],
    ['Voltage plateau (midpoint) [V]', 4.115, 'final_1c_energy_dfn_h45.json:midpoint_voltage_v'],
    ['T_max 4C/45C [K]', 322.59, 'final_4c_safety_h45_dfn.json:T_max_K'],
    ['Anode potential min [V]', 0.0894, 'final_4c_safety_h45_dfn.json:anode_potential_v'],
    ['SEI thickness 100cyc (DFN) [nm]', 9.46, 'final_aging_dfn_h45.json:sei_thickness_nm_end'],
]:
    s_ce.append(r)

s_ed = wb2.create_sheet('EnergyDensity')
for r in [
    ['Metric', 'Value', 'Formula / source'],
    ['Volume [m3]', 1.982e-5, 'total thickness x area'],
    ['Total thickness [m]', 0.000193, 'sum of 5 layers'],
    ['Volumetric ED [Wh/L]', 1005.77, 'energy_wh / volume_m3 / 1000'],
    ['Mass (stack) [kg]', 0.041475, 'calc-energy mass_kg'],
    ['Gravimetric ED [Wh/kg]', 480.66, 'energy_wh / mass_kg'],
]:
    s_ed.append(r)

s_np = wb2.create_sheet('NPRatio')
pos_cap = pos_t * pos_af * 43000.0
neg_cap = neg_t * neg_af * 33133.0
for r in [
    ['Quantity', 'Value', 'Source'],
    ['Positive areal capacity density (th x af x Cmax)', pos_cap, '57um x 0.665 x 43000 mol/m3'],
    ['Negative areal capacity density (th x af x Cmax)', neg_cap, '110um x 0.75 x 33133 mol/m3'],
    ['N/P ratio', round(neg_cap / pos_cap, 3), 'negative / positive'],
    ['Stack mass [kg]', 0.041475, 'calc-energy'],
]:
    s_np.append(r)

s_pr = wb2.create_sheet('Process')
for r in [
    ['Parameter', 'Value', 'Formula / source'],
    ['Positive areal density [g/m2]', 166.8, '57um x (1-0.335) x 4400 kg/m3'],
    ['Negative areal density [g/m2]', 136.7, '110um x (1-0.25) x 1657 kg/m3'],
    ['Positive compaction density [g/cm3]', 2.926, '4400 x (1-0.335)/1000'],
    ['Negative compaction density [g/cm3]', 1.243, '1657 x (1-0.25)/1000'],
    ['Electrolyte fill [g]', round(g(electrolyte_mass), 2), 'pore volume x 1.2 g/cm3'],
    ['Formation', '0.1C CC to 4.2V, 25C, 2 cycles', 'design recommended value'],
]:
    s_pr.append(r)
wb2.save(DEL / 'calc.xlsx')

# ---------------- PDF generation ----------------
styles = getSampleStyleSheet()
body = ParagraphStyle('body', fontName='Segoe', fontSize=9, leading=12)
title_st = ParagraphStyle('title', fontName='Segoe', fontSize=14, leading=18, spaceAfter=8)

def md_table_to_platypus(lines):
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        rows.append(cells)
    if not rows:
        return []
    header = rows[0]
    data = [r for r in rows[1:] if not all(set(c) <= set('-: ') and c for c in r)]
    tbl_data = [header] + data
    t = Table([[sanitize(c) for c in row] for row in tbl_data], repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Segoe'),
        ('FONTNAME', (0, 1), (-1, -1), 'Segoe'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E5A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#9BB3C6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    return [t, Spacer(1, 6)]

def md_to_pdf(md_path, pdf_path, title=None):
    text = Path(md_path).read_text(encoding='utf-8')
    lines = text.splitlines()
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=12*mm, rightMargin=12*mm, topMargin=14*mm, bottomMargin=14*mm)
    story = []
    if title:
        story.append(Paragraph(sanitize(title), title_st))
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('|'):
            j = i
            block = []
            while j < len(lines) and lines[j].strip().startswith('|'):
                block.append(lines[j]); j += 1
            story.extend(md_table_to_platypus(block))
            i = j
            continue
        s = ln.strip()
        if not s:
            i += 1; continue
        if s.startswith('#'):
            s = s.lstrip('#').strip()
            story.append(Paragraph('<b>%s</b>' % sanitize(s), body))
        elif s.startswith('- '):
            story.append(Paragraph('&bull; ' + sanitize(s[2:]), body))
        else:
            story.append(Paragraph(sanitize(s), body))
        i += 1
    doc.build(story)

def xlsx_to_pdf(xlsx_path, pdf_path, title):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=12*mm, rightMargin=12*mm, topMargin=14*mm, bottomMargin=14*mm)
    story = [Paragraph(sanitize(title), title_st)]
    for sh in wb.worksheets:
        story.append(Paragraph('<b>%s</b>' % sanitize(sh.title), body))
        rows = [[sanitize(c.value) for c in row] for row in sh.iter_rows()]
        if rows:
            t = Table(rows, repeatRows=1)
            t.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Segoe'),
                ('FONTSIZE', (0, 0), (-1, -1), 7.5),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14283C')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#9BB3C6')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(t)
        story.append(Spacer(1, 8))
    doc.build(story)

md_to_pdf(DEL / 'design_spec.md', DEL / 'design_spec.pdf', 'Cell Design Specification - VBF-T6LC-DS-01')
md_to_pdf(DEL / 'datasheet.md', DEL / 'datasheet.pdf', 'Technical Datasheet - VBF-T6LC-DSH-01')
md_to_pdf(DEL / 'dvpr.md', DEL / 'dvpr.pdf', 'Design Verification Plan & Report - VBF-T6LC-DVPR-01')
md_to_pdf(DEL / 'dfmea.md', DEL / 'dfmea.pdf', 'Design FMEA - VBF-T6LC-DFMEA-01')
md_to_pdf(DEL / 'delivery_index.md', DEL / 'delivery_index.pdf', 'Delivery Package Index - VBF-T6LC-IDX-01')
xlsx_to_pdf(DEL / 'bom.xlsx', DEL / 'bom.pdf', 'Bill of Materials - VBF-T6LC-BOM-01')
xlsx_to_pdf(DEL / 'calc.xlsx', DEL / 'calc.pdf', 'Design Calculation Sheet - VBF-T6LC-CALC-01')

print('deliverables generated')
for p in sorted(DEL.iterdir()):
    print(p.name, p.stat().st_size)
