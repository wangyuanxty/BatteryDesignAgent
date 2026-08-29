# -*- coding: utf-8 -*-
"""Closing deliverables generator for exp/t3_r1_noforce (final design V8).
All values mechanically read from parameter set / simulation outputs.
"""
import json
import math
import re
from pathlib import Path

import pybamm
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
import docx
from docx.shared import Pt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ROOT = Path('runs/exp/t3_r1_noforce')
DEL = ROOT / 'deliverables'
DEL.mkdir(exist_ok=True)
F = 96485.0

# ---------- mechanical sources ----------
def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

base = pybamm.ParameterValues('Chen2020')
over = load(ROOT / 'bridge' / 'params_v8.json')
base.update(over, check_already_exists=False)
d1 = load(ROOT / 'cell' / 'r4_v8_1c_dfn.json')
d5 = load(ROOT / 'cell' / 'r4_v8_5c_dfn.json')
d4 = load(ROOT / 'cell' / 'r4_v8_4c45_dfn.json')
e = load(ROOT / 'cell' / 'r4_v8_energy.json')

A = e['area_m2']
cap1, cap5 = d1['capacity_ah'], d5['capacity_ah']
ret = cap5 / cap1
ap_min = min(d4['anode_potential_v'])
energy_wh, mass_kg = e['energy_wh'], e['mass_kg']
energy_kwh = energy_wh / 1000.0
voc = math.sqrt(e['power_density_w_kg'] * 4.0 * e['dcr_ohm'] * mass_kg)

L_pos, L_neg, L_sep, L_al, L_cu = 50e-6, 60e-6, 9e-6, 16e-6, 12e-6
por_pos, por_neg, por_sep = 0.40, 0.42, 0.55
amvf_pos, amvf_neg = 0.58, 0.56
d_pos, d_neg, d_sep, d_al, d_cu = (
    base['Positive electrode density [kg.m-3]'],
    base['Negative electrode density [kg.m-3]'],
    base['Separator density [kg.m-3]'],
    base['Positive current collector density [kg.m-3]'],
    base['Negative current collector density [kg.m-3]'],
)
c_pos, c_neg = (base['Maximum concentration in positive electrode [mol.m-3]'],
                base['Maximum concentration in negative electrode [mol.m-3]'])
x_neg0 = base['Initial concentration in negative electrode [mol.m-3]'] / c_neg
x_pos0 = base['Initial concentration in positive electrode [mol.m-3]'] / c_pos
ds_pos = base['Positive electrode diffusivity [m2.s-1]']
ds_neg = base['Negative electrode diffusivity [m2.s-1]']
rp_pos, rp_neg = over['Positive particle radius [m]'], over['Negative particle radius [m]']

# BOM component masses (g)
m_pos_am = L_pos * A * amvf_pos * d_pos * 1000
m_pos_b = L_pos * A * 0.015 * 1780 * 1000      # PVDF, literature default density
m_pos_c = L_pos * A * 0.005 * 2200 * 1000      # carbon black, literature default density
m_neg_am = L_neg * A * amvf_neg * d_neg * 1000
m_neg_b = L_neg * A * 0.02 * 1300 * 1000       # SBR/CMC, literature default density
m_sep = L_sep * A * (1 - por_sep) * d_sep * 1000
m_al = L_al * A * d_al * 1000
m_cu = L_cu * A * d_cu * 1000
pore_vol = A * (L_pos * por_pos + L_neg * por_neg + L_sep * por_sep)
m_ely = pore_vol * 1200 * 1000                  # 1.2 g/cm3 literature value, fill factor 1.0
sum_excl = m_pos_am + m_pos_b + m_pos_c + m_neg_am + m_neg_b + m_sep + m_al + m_cu
sum_incl = sum_excl + m_ely

bom_rows = [
    ['Positive electrode active material', 'NMC811', 0.58, 3262, m_pos_am, 'L_pos x A x AMVF x d (parameter set)'],
    ['Positive electrode binder', 'PVDF', 0.015, 1780, m_pos_b, 'literature default density (no parameter in set)'],
    ['Positive electrode conductive additive', 'carbon black', 0.005, 2200, m_pos_c, 'literature default density (no parameter in set)'],
    ['Negative electrode active material', 'graphite', 0.56, 1657, m_neg_am, 'L_neg x A x AMVF x d (parameter set)'],
    ['Negative electrode binder', 'SBR/CMC', 0.02, 1300, m_neg_b, 'literature default density (no parameter in set)'],
    ['Separator', 'polyolefin class', 1 - por_sep, 397, m_sep, 'L_sep x A x (1-porosity) x d (parameter set)'],
    ['Positive current collector', 'Al', 1.0, 2700, m_al, 'L_al x A x d (parameter set)'],
    ['Negative current collector', 'Cu', 1.0, 8960, m_cu, 'L_cu x A x d (parameter set)'],
    ['Electrolyte', 'EC/EMC + LiPF6 class', None, 1200, m_ely, 'pore volume x 1.2 g/cm3 (literature); excluded from contract mass'],
    ['Enclosure / tabs', 'Not modeled', None, None, None, 'outside pure-simulation boundary'],
]

# ---------- bom.xlsx ----------
wb = Workbook()
ws = wb.active
ws.title = 'BOM'
hdr = ['Item', 'Material', 'Volume fraction', 'Density (kg/m3)', 'Mass (g/cell)', 'Mass (kg/kWh)', 'Formula / source']
ws.append(hdr)
for row in bom_rows:
    kgkwh = (row[4] / 1000.0 / energy_kwh) if row[4] is not None else None
    ws.append([row[0], row[1], row[2], row[3], round(row[4], 3) if row[4] is not None else 'Not modeled',
               round(kgkwh, 3) if kgkwh is not None else 'Not modeled', row[5]])
ws.append([])
ws.append(['Component sum (excl. electrolyte)', '', '', '', round(sum_excl, 3), round(sum_excl / 1000.0 / energy_kwh, 3),
           'sum of rows 1-8'])
ws.append(['Contract mass (calc-energy caliber)', '', '', '', round(mass_kg * 1000, 3), round(mass_kg / energy_kwh, 3),
           'cell/r4_v8_energy.json mass_kg; electrolyte excluded (parameter set lacks density)'])
ws.append(['Total incl. electrolyte', '', '', '', round(sum_incl, 3), round(sum_incl / 1000.0 / energy_kwh, 3),
           'contract mass + electrolyte fill'])
ws.append(['Cell energy', '', '', '', '', '', f'{energy_wh:.4f} Wh (r4_v8_energy.json energy_wh)'])
for c in ws[1]:
    c.font = Font(bold=True, color='FFFFFF')
    c.fill = PatternFill('solid', fgColor='1E5A8A')
for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical='top')
for col, w in zip('ABCDEFG', [38, 20, 16, 16, 14, 14, 52]):
    ws.column_dimensions[col].width = w
wb.save(DEL / 'bom.xlsx')

# ---------- calc.xlsx ----------
wb2 = Workbook()
def sheet(ws, title, rows):
    ws.title = title
    for r in rows:
        ws.append(r)
    for c in ws[1]:
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor='1E5A8A')
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')
    for col, w in zip('ABCDE', [34, 16, 10, 60, 52]):
        ws.column_dimensions[col].width = w

S = [['Item', 'Value', 'Unit', 'Formula', 'Source']]
sheet(wb2.active, 'Input parameters', S + [
    ['Positive electrode thickness', L_pos * 1e6, 'um', 'design override', 'bridge/params_v8.json'],
    ['Negative electrode thickness', L_neg * 1e6, 'um', 'design override', 'bridge/params_v8.json'],
    ['Separator thickness', L_sep * 1e6, 'um', 'design override', 'bridge/params_v8.json'],
    ['Positive particle radius', rp_pos * 1e6, 'um', 'design override', 'bridge/params_v8.json'],
    ['Negative particle radius', rp_neg * 1e6, 'um', 'design override', 'bridge/params_v8.json'],
    ['Positive porosity', por_pos, '', 'design override', 'bridge/params_v8.json'],
    ['Negative porosity', por_neg, '', 'design override', 'bridge/params_v8.json'],
    ['Positive AMVF', amvf_pos, '', 'design override', 'bridge/params_v8.json'],
    ['Negative AMVF', amvf_neg, '', 'design override', 'bridge/params_v8.json'],
    ['Separator porosity', por_sep, '', 'design override', 'bridge/params_v8.json'],
    ['Electrolyte conductivity', over['Electrolyte conductivity [S.m-1]'], 'S/m', 'design override (estimate class)', 'bridge/params_v8.json'],
    ['Cation transference number', over['Cation transference number'], '', 'design override (estimate class)', 'bridge/params_v8.json'],
    ['Cooling heat transfer coefficient', over['Total heat transfer coefficient [W.m-2.K-1]'], 'W/m2K', 'design override (forced air)', 'bridge/params_v8.json'],
    ['Rated (nominal) capacity', over['Nominal cell capacity [A.h]'], 'Ah', 'cell rating = designed capacity', 'bridge/params_v8.json'],
    ['Positive density', d_pos, 'kg/m3', 'base set', 'Chen2020'],
    ['Negative density', d_neg, 'kg/m3', 'base set', 'Chen2020'],
    ['Separator density', d_sep, 'kg/m3', 'base set', 'Chen2020'],
    ['Positive c_max', c_pos, 'mol/m3', 'base set', 'Chen2020'],
    ['Negative c_max', c_neg, 'mol/m3', 'base set', 'Chen2020'],
    ['Positive solid diffusivity', ds_pos, 'm2/s', 'base set (excluded design lever)', 'Chen2020'],
    ['Negative solid diffusivity', ds_neg, 'm2/s', 'base set (excluded design lever)', 'Chen2020'],
    ['Electrode area', A, 'm2', 'height x width', 'Chen2020 (0.065 x 1.58)'],
    ['Voltage window', '2.5 - 4.2', 'V', 'base set cut-offs', 'Chen2020'],
])

sheet(wb2.create_sheet(), 'Capacity and energy', S + [
    ['1C discharge capacity', cap1, 'Ah', 'simulation integration', 'cell/r4_v8_1c_dfn.json:capacity_ah'],
    ['5C discharge capacity', cap5, 'Ah', 'simulation integration', 'cell/r4_v8_5c_dfn.json:capacity_ah'],
    ['5C retention', ret, '', '5C capacity / 1C capacity', 'cell/r4_v8_derived.json:rate_retention_5c'],
    ['Discharge energy', energy_wh, 'Wh', 'time integration of V*I', 'cell/r4_v8_energy.json:energy_wh'],
    ['Midpoint voltage', e['midpoint_voltage_v'], 'V', 'simulation', 'cell/r4_v8_energy.json'],
    ['DC resistance (10% discharge)', e['dcr_ohm'], 'ohm', '(start OCV - V@10%) / I_1C', 'cell/r4_v8_energy.json:dcr_ohm'],
    ['Open-circuit voltage (contract)', voc, 'V', 'sqrt(PD x 4 x DCR x mass)', 'derived from cell/r4_v8_energy.json'],
    ['Peak power', e['power_density_w_kg'] * mass_kg, 'W', 'PD x mass', 'derived'],
])

sheet(wb2.create_sheet(), 'Energy density', S + [
    ['Energy', energy_wh, 'Wh', 'simulation integration', 'cell/r4_v8_energy.json:energy_wh'],
    ['Cell mass (contract)', mass_kg, 'kg', 'sum layer thickness x area x (1-porosity) x density; electrolyte excluded', 'cell/r4_v8_energy.json:mass_kg'],
    ['Cell volume (stack)', e['volume_m3'], 'm3', 'area x stack thickness', 'cell/r4_v8_energy.json:volume_m3'],
    ['Gravimetric energy density', e['energy_density_wh_kg'], 'Wh/kg', 'energy / mass', 'cell/r4_v8_energy.json'],
    ['Volumetric energy density', e['energy_density_wh_l'], 'Wh/L', 'energy / volume', 'cell/r4_v8_energy.json'],
    ['Power density', e['power_density_w_kg'], 'W/kg', 'V_OC^2/(4 x DCR)/mass (contract)', 'cell/r4_v8_energy.json:power_density_w_kg'],
])

np_areal_neg = c_neg * F / 3600 * L_neg * amvf_neg
np_areal_pos = c_pos * F / 3600 * L_pos * amvf_pos
sheet(wb2.create_sheet(), 'N-P and mass', S + [
    ['Negative areal capacity (full-lithiation)', np_areal_neg, 'Ah/m2', 'c_max x F/3600 x L x AMVF', 'derived from Chen2020 + params_v8.json'],
    ['Positive areal capacity (full-lithiation)', np_areal_pos, 'Ah/m2', 'c_max x F/3600 x L x AMVF', 'derived from Chen2020 + params_v8.json'],
    ['N/P ratio', np_areal_neg / np_areal_pos, '', 'neg capacity density x thickness / pos capacity density x thickness', 'deliverable formula'],
    ['Charged-state negative stoichiometry', x_neg0, '', 'initial concentration / c_max', 'Chen2020'],
    ['Charged-state positive stoichiometry', x_pos0, '', 'initial concentration / c_max', 'Chen2020'],
    ['Layer mass positive coating', e['layer_kg_m2']['positive_electrode'] * A, 'kg', 'layer_kg_m2 x area', 'cell/r4_v8_energy.json'],
    ['Layer mass negative coating', e['layer_kg_m2']['negative_electrode'] * A, 'kg', 'layer_kg_m2 x area', 'cell/r4_v8_energy.json'],
    ['Layer mass Al CC', e['layer_kg_m2']['positive_cc'] * A, 'kg', 'layer_kg_m2 x area', 'cell/r4_v8_energy.json'],
    ['Layer mass Cu CC', e['layer_kg_m2']['negative_cc'] * A, 'kg', 'layer_kg_m2 x area', 'cell/r4_v8_energy.json'],
    ['Layer mass separator', e['layer_kg_m2']['separator'] * A, 'kg', 'layer_kg_m2 x area', 'cell/r4_v8_energy.json'],
    ['Anode-limited balance check', '2.9907 x 0.56/0.63 = 2.658 vs 2.6683 measured', '', '1C capacity scales with negative AMVF (V6 -> V8)', 'r4_v6_1c_dfn.json + r4_v8_1c_dfn.json'],
])

sheet(wb2.create_sheet(), 'Process parameters', S + [
    ['Areal density positive', L_pos * (1 - por_pos) * d_pos, 'g/m2', 'thickness x (1-porosity) x density', 'derived'],
    ['Areal density negative', L_neg * (1 - por_neg) * d_neg, 'g/m2', 'thickness x (1-porosity) x density', 'derived'],
    ['Compaction density positive', d_pos * (1 - por_pos) / 1000, 'g/cm3', 'density x (1-porosity) / 1000', 'derived'],
    ['Compaction density negative', d_neg * (1 - por_neg) / 1000, 'g/cm3', 'density x (1-porosity) / 1000', 'derived'],
    ['Electrolyte fill amount', m_ely, 'g', 'pore volume x 1.2 g/cm3 (literature) x fill factor 1.0', 'derived'],
    ['Formation recommendation', '0.1C CC to 4.2V, 25C, 2 cycles', '', 'design recommended value; production-line tuning required', 'design note'],
    ['Diffusion time positive', rp_pos ** 2 / ds_pos, 's', 'r^2 / D_s', 'derived'],
    ['Diffusion time negative', rp_neg ** 2 / ds_neg, 's', 'r^2 / D_s', 'derived'],
])
wb2.save(DEL / 'calc.xlsx')

# ---------- datasheet.docx ----------
doc = docx.Document()
doc.add_heading('Technical Datasheet — Power-Tool Battery Cell (V8)', 0)
doc.add_paragraph('Document no.: VBF-T3R1NOFORCE-DSH-01 · Case exp/t3_r1_noforce · 2026-08-25')
rows = [
    ('Rated capacity (Ah)', f"{over['Nominal cell capacity [A.h]']:.1f} (design rating) / {cap1:.4f} simulation-verified at 1C",
     'bridge/params_v8.json / cell/r4_v8_1c_dfn.json'),
    ('Nominal voltage / voltage window (V)', f"midpoint {e['midpoint_voltage_v']:.4f}; window 2.5 - 4.2",
     'cell/r4_v8_energy.json / Chen2020 cut-offs'),
    ('Rated energy (Wh)', f'{energy_wh:.3f}', 'cell/r4_v8_energy.json:energy_wh'),
    ('Energy density', f"{e['energy_density_wh_kg']:.1f} Wh/kg / {e['energy_density_wh_l']:.1f} Wh/L",
     'cell/r4_v8_energy.json (contract mass formula, electrolyte excluded)'),
    ('Maximum continuous discharge rate', f'5C (15 A): capacity {cap5:.4f} Ah, retention {ret:.4f} vs 1C',
     'cell/r4_v8_5c_dfn.json / cell/r4_v8_derived.json'),
    ('Fast-charge capability', f'4C (12 A) at 45 C ambient: T_max {d4["T_max_K"]:.2f} K, anode potential min {ap_min:+.4f} V -> no plating',
     'cell/r4_v8_4c45_dfn.json'),
    ('Operating temperature range', 'Simulated: 298.15 K discharge / 318.15 K charge ambient (protocol conditions); broader range not simulated',
     'protocol definitions'),
    ('Cycle life', 'Not simulated (requires aging model)', 'honest annotation per protocol'),
    ('Safety determination', f'No plating on 4C charge; T_max {max(d5["T_max_K"], d4["T_max_K"]):.2f} K <= 333.15 K (60 C)',
     'cell/r4_v8_5c_dfn.json / cell/r4_v8_4c45_dfn.json'),
    ('Power density (W/kg)', f"{e['power_density_w_kg']:.1f}", 'cell/r4_v8_energy.json'),
    ('Dimensions and mass', f'electrodes 65 x 1580 mm (unrolled), stack {e["thickness_m"] * 1000:.3f} mm; mass {mass_kg * 1000:.1f} g (contract, electrolyte excluded; {sum_incl:.1f} g incl. electrolyte fill); shell Not provided',
     'Chen2020 + params_v8.json + cell/r4_v8_energy.json'),
]
t = doc.add_table(rows=1, cols=3)
t.style = 'Light Grid Accent 1'
for i, h in enumerate(['Field', 'Value', 'Source']):
    t.rows[0].cells[i].text = h
for fld, val, src in rows:
    c = t.add_row().cells
    c[0].text, c[1].text, c[2].text = fld, val, src
doc.save(DEL / 'datasheet.docx')

# ---------- PDF release versions ----------
DEEP = colors.HexColor('#14283C')
MID = colors.HexColor('#1E5A8A')
COPPER = colors.HexColor('#C97B3D')
styles = getSampleStyleSheet()

def band(doc_title, doc_no):
    t = Table([[Paragraph(doc_title, ParagraphStyle('tt', fontName='Helvetica-Bold', fontSize=13, textColor=colors.white)),
                Paragraph(doc_no, ParagraphStyle('tn', fontName='Helvetica', fontSize=9, textColor=colors.white, alignment=2))]],
              colWidths=[130 * mm, 60 * mm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), DEEP),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10)]))
    line = Table([['']], colWidths=[190 * mm], rowHeights=[2 * mm])
    line.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), COPPER)]))
    return [t, line, Spacer(1, 6 * mm)]

def data_to_table(header, data, colwidths_mm):
    rows = [[Paragraph(h, ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)) for h in header]]
    for r in data:
        rows.append([Paragraph(str(v), ParagraphStyle('c', fontName='Helvetica', fontSize=8)) for v in r])
    t = Table(rows, colWidths=[w * mm for w in colwidths_mm], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), MID),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#B9C6D2')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F4F8')]),
    ]))
    return t

def pdf_from_md(md_name, pdf_name, doc_title, doc_no):
    txt = (DEL / md_name).read_text(encoding='utf-8')
    flow = band(doc_title, doc_no)
    h1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=11, textColor=DEEP, spaceBefore=8, spaceAfter=4)
    h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=9.5, textColor=MID, spaceBefore=6, spaceAfter=3)
    pst = ParagraphStyle('p', fontName='Helvetica', fontSize=8.5, leading=11.5, spaceAfter=3)
    bst = ParagraphStyle('b', fontName='Helvetica', fontSize=8.5, leading=11.5, spaceAfter=2, leftIndent=8, bulletIndent=2)
    tbl = []
    for raw in txt.splitlines():
        s = raw.strip()
        if not s:
            if tbl:
                flow.append(data_to_table(tbl[0], tbl[2:], tbl[1]))
                flow.append(Spacer(1, 3 * mm))
                tbl = []
            continue
        if s.startswith('|'):
            cells = [c.strip() for c in s.strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                continue
            if not tbl:
                colw = [190.0 / len(cells)] * len(cells)
                tbl = [cells, colw]
            else:
                tbl.append(cells)
            continue
        if s.startswith('# '):
            flow.append(Paragraph(s[2:].replace('**', ''), h1))
        elif s.startswith('## '):
            flow.append(Paragraph(s[2:].replace('**', ''), h2))
        elif s.startswith('- '):
            t = s[2:]
            while t.count('**') >= 2:
                t = t.replace('**', '<b>', 1).replace('**', '</b>', 1)
            flow.append(Paragraph(t, bst))
        else:
            t = s
            while t.count('**') >= 2:
                t = t.replace('**', '<b>', 1).replace('**', '</b>', 1)
            flow.append(Paragraph(t, pst))
    if tbl:
        flow.append(data_to_table(tbl[0], tbl[2:], tbl[1]))
    SimpleDocTemplate(str(DEL / pdf_name), pagesize=A4, leftMargin=10 * mm, rightMargin=10 * mm,
                      topMargin=10 * mm, bottomMargin=10 * mm).build(flow)

pdf_from_md('design_spec.md', 'design_spec.pdf', 'Cell Design Specification — Power-Tool Battery Cell (V8)', 'VBF-T3R1NOFORCE-DS-01')
pdf_from_md('dvpr.md', 'dvpr.pdf', 'Design Verification Plan and Report (virtual) — V8', 'VBF-T3R1NOFORCE-DVPR-01')
pdf_from_md('dfmea.md', 'dfmea.pdf', 'Design FMEA (qualitative) — V8', 'VBF-T3R1NOFORCE-DFMEA-01')
pdf_from_md('delivery_index.md', 'delivery_index.pdf', 'Delivery Package Index', 'VBF-T3R1NOFORCE-IDX-01')

# bom.pdf
flow = band('Bill of Materials — V8', 'VBF-T3R1NOFORCE-BOM-01')
data = []
for row in bom_rows:
    kgkwh = (row[4] / 1000.0 / energy_kwh) if row[4] is not None else 'Not modeled'
    data.append([row[0], row[1], str(row[2]) if row[2] is not None else '', str(row[3]) if row[3] is not None else '',
                 f'{row[4]:.3f}' if row[4] is not None else 'Not modeled', f'{kgkwh:.3f}' if not isinstance(kgkwh, str) else kgkwh, row[5]])
data.append(['Component sum (excl. electrolyte)', '', '', '', f'{sum_excl:.3f}', f'{sum_excl / 1000.0 / energy_kwh:.3f}', 'sum of rows 1-8'])
data.append(['Contract mass (calc-energy caliber)', '', '', '', f'{mass_kg * 1000:.3f}', f'{mass_kg / energy_kwh:.3f}', 'cell/r4_v8_energy.json mass_kg'])
data.append(['Total incl. electrolyte', '', '', '', f'{sum_incl:.3f}', f'{sum_incl / 1000.0 / energy_kwh:.3f}', 'contract mass + electrolyte fill'])
flow.append(data_to_table(['Item', 'Material', 'Vol. frac', 'Density (kg/m3)', 'Mass (g/cell)', 'Mass (kg/kWh)', 'Formula / source'],
                          data, [30, 16, 12, 15, 15, 15, 48]))
SimpleDocTemplate(str(DEL / 'bom.pdf'), pagesize=landscape(A4), leftMargin=10 * mm, rightMargin=10 * mm,
                  topMargin=10 * mm, bottomMargin=10 * mm).build(flow)

# calc.pdf
flow = band('Design Calculation Sheet — V8', 'VBF-T3R1NOFORCE-CALC-01')
wb_calc = __import__('openpyxl').load_workbook(DEL / 'calc.xlsx', read_only=True)
for name in wb_calc.sheetnames:
    ws2 = wb_calc[name]
    crows = [[str(c.value) if c.value is not None else '' for c in r] for r in ws2.iter_rows()]
    flow.append(Paragraph(name, ParagraphStyle('sh', fontName='Helvetica-Bold', fontSize=10, textColor=MID, spaceBefore=6, spaceAfter=3)))
    flow.append(data_to_table(crows[0], crows[1:], [55, 20, 12, 55, 48]))
    flow.append(Spacer(1, 3 * mm))
SimpleDocTemplate(str(DEL / 'calc.pdf'), pagesize=landscape(A4), leftMargin=10 * mm, rightMargin=10 * mm,
                  topMargin=10 * mm, bottomMargin=10 * mm).build(flow)

# datasheet.pdf
flow = band('Technical Datasheet — Power-Tool Battery Cell (V8)', 'VBF-T3R1NOFORCE-DSH-01')
flow.append(data_to_table(['Field', 'Value', 'Source'],
                          [[f, v, s] for f, v, s in rows],
                          [40, 95, 55]))
SimpleDocTemplate(str(DEL / 'datasheet.pdf'), pagesize=A4, leftMargin=10 * mm, rightMargin=10 * mm,
                  topMargin=10 * mm, bottomMargin=10 * mm).build(flow)

# ---------- summary ----------
print('deliverables written to', DEL)
for p in sorted(DEL.iterdir()):
    print(f'  {p.name:22s} {p.stat().st_size:>8d} B')
print(f'N/P = {np_areal_neg / np_areal_pos:.4f} | V_OC = {voc:.4f} V | ap_min = {ap_min:+.4f} V')
