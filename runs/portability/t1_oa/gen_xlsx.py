# -*- coding: utf-8 -*-
"""Generate bom.xlsx, calc.xlsx, and PDF releases for all deliverables."""
import json
import re
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

HERE = Path(__file__).resolve().parent
DLV = HERE / "deliverables"
DLV.mkdir(exist_ok=True)

# ---- Key numbers (from simulation outputs, tool-derived) ----
ENERGY_WH = 18.550374911992808       # cell/T10_energy_dfn.json:energy_wh
MASS_KG = 0.0434545275216            # cell/T10_energy_dfn.json:mass_kg
ED_WH_KG = 426.8916490409877
CAPACITY_AH = 5.056773637159709
AREA_M2 = 0.10270000000000001
LAYERS = {
    "positive_electrode": 0.163993788,
    "negative_electrode": 0.10588229999999998,
    "positive_cc": 0.043199999999999995,
    "negative_cc": 0.10752,
    "separator": 0.00252492,
}
POS_TH = 75.6e-6
NEG_TH = 85.2e-6
SEP_TH = 12e-6
POS_POR = 0.335
NEG_POR = 0.25
SEP_POR = 0.47
POS_DEN = 3262.0
NEG_DEN = 1657.0
POS_CC_TH = 16e-6
NEG_CC_TH = 12e-6
POS_CC_DEN = 2700.0
NEG_CC_DEN = 8960.0

# mass per layer in grams
pos_el_g = LAYERS["positive_electrode"] * AREA_M2 * 1000
neg_el_g = LAYERS["negative_electrode"] * AREA_M2 * 1000
pos_cc_g = LAYERS["positive_cc"] * AREA_M2 * 1000
neg_cc_g = LAYERS["negative_cc"] * AREA_M2 * 1000
sep_g = LAYERS["separator"] * AREA_M2 * 1000

# electrolyte mass: pore volume * 1.2 g/cm3
pore_cm3 = (POS_TH * POS_POR + NEG_TH * NEG_POR + SEP_TH * SEP_POR) * AREA_M2 * 1e6
elyte_g = pore_cm3 * 1.2

# ===================== BOM =====================
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
header = ["Component", "Mass (g/cell)", "Mass (kg/kWh)", "Source note"]
ws.append(header)

bom_rows = [
    ("Positive electrode active material (NMC811)", pos_el_g, pos_el_g/1000/ (ENERGY_WH/1000), "thickness*(1-porosity)*density*area (layer_kg_m2)"),
    ("Positive conductive additive (carbon black, 2 wt%)", pos_el_g*0.02, pos_el_g*0.02/1000/(ENERGY_WH/1000), "literature default (no parameter)"),
    ("Positive binder (PVDF, 2 wt%)", pos_el_g*0.02, pos_el_g*0.02/1000/(ENERGY_WH/1000), "literature default (no parameter)"),
    ("Negative electrode active material (graphite+SiOx)", neg_el_g, neg_el_g/1000/(ENERGY_WH/1000), "thickness*(1-porosity)*density*area"),
    ("Negative conductive additive (carbon black, 1 wt%)", neg_el_g*0.01, neg_el_g*0.01/1000/(ENERGY_WH/1000), "literature default"),
    ("Negative binder (SBR/CMC, 3 wt%)", neg_el_g*0.03, neg_el_g*0.03/1000/(ENERGY_WH/1000), "literature default"),
    ("Separator (polyolefin)", sep_g, sep_g/1000/(ENERGY_WH/1000), "thickness*(1-porosity)*density*area"),
    ("Electrolyte (1.2 g/cm3)", elyte_g, elyte_g/1000/(ENERGY_WH/1000), "pore volume * 1.2 g/cm3 (literature density)"),
    ("Positive current collector (Al)", pos_cc_g, pos_cc_g/1000/(ENERGY_WH/1000), "thickness*density*area"),
    ("Negative current collector (Cu)", neg_cc_g, neg_cc_g/1000/(ENERGY_WH/1000), "thickness*density*area"),
    ("Enclosure / tabs", None, None, "Not modeled"),
]
for r in bom_rows:
    ws.append([r[0], round(r[1], 3) if r[1] is not None else "Not modeled",
               round(r[2], 3) if r[2] is not None else "Not modeled", r[3]])

total_g = sum(r[1] for r in bom_rows if r[1] is not None)
total_kgkwh = sum(r[2] for r in bom_rows if r[2] is not None)
ws.append(["Total (excl. enclosure)", round(total_g, 3), round(total_kgkwh, 3),
           "cell energy %.4f kWh (energy_wh/1000)" % (ENERGY_WH/1000)])
for c in ws[1]:
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor="14283C")
    c.font = Font(bold=True, color="FFFFFF")
wb.save(DLV / "bom.xlsx")

# ===================== CALC =====================
wb2 = openpyxl.Workbook()
ws2 = wb2.active
ws2.title = "Input"
ws2.append(["Parameter", "Value", "Unit", "Source"])
calc_input = [
    ("Positive electrode thickness", POS_TH*1e6, "um", "parameter set OKane2022"),
    ("Negative electrode thickness", NEG_TH*1e6, "um", "parameter set"),
    ("Separator thickness", SEP_TH*1e6, "um", "parameter set"),
    ("Positive porosity", POS_POR, "-", "parameter set"),
    ("Negative porosity", NEG_POR, "-", "parameter set"),
    ("Positive density", POS_DEN, "kg/m3", "parameter set"),
    ("Negative density", NEG_DEN, "kg/m3", "parameter set"),
    ("Electrode area (h x w)", AREA_M2, "m2", "0.065 x 1.58"),
    ("Nominal capacity", 5.0, "Ah", "parameter set"),
    ("Electrolyte conductivity (override)", 3.0, "S/m", "design (estimate)"),
    ("Cation transference number (override)", 0.6, "-", "design (estimate)"),
    ("Cooling coefficient h (override)", 80.0, "W/m2/K", "design (liquid cooling)"),
]
for r in calc_input:
    ws2.append(list(r))

ws3 = wb2.create_sheet("Capacity-Energy")
ws3.append(["Item", "Value", "Unit", "Formula / source"])
ws3.append(["1C discharge capacity", CAPACITY_AH, "Ah", "cell/T10_1c_dfn.json"])
ws3.append(["Discharge energy", ENERGY_WH, "Wh", "integral(V*I)dt / 3600"])
ws3.append(["Cell mass (electrolyte excl.)", MASS_KG*1000, "g", "sum(layer thickness*(1-porosity)*density*area)"])
ws3.append(["Gravimetric energy density", ED_WH_KG, "Wh/kg", "energy_wh / mass_kg"])

ws4 = wb2.create_sheet("Mass-NP")
ws4.append(["Layer", "kg/m2", "g/cell"])
for k, v in LAYERS.items():
    ws4.append([k, v, round(v*AREA_M2*1000, 3)])
ws4.append(["Total", MASS_KG/AREA_M2, round(MASS_KG*1000, 3)])
ws4.append([])
ws4.append(["N/P ratio", 0.667, "-", "(0.75*85.2um*33133)/(0.665*75.6um*63104)"])

ws5 = wb2.create_sheet("Process")
ws5.append(["Parameter", "Positive", "Negative", "Formula"])
ws5.append(["Areal density (g/m2)", round(POS_TH*(1-POS_POR)*POS_DEN,2), round(NEG_TH*(1-NEG_POR)*NEG_DEN,2), "thickness*(1-porosity)*density"])
ws5.append(["Compaction density (g/cm3)", round(POS_DEN*(1-POS_POR)/1000,3), round(NEG_DEN*(1-NEG_POR)/1000,3), "density*(1-porosity)/1000"])
ws5.append(["Electrolyte fill (g/cell)", round(elyte_g,3), "", "pore volume * 1.2 g/cm3"])
wb2.save(DLV / "calc.xlsx")

print("xlsx written: bom.xlsx, calc.xlsx")
print("pos_el_g=%.3f neg_el_g=%.3f pos_cc_g=%.3f neg_cc_g=%.3f sep_g=%.3f elyte_g=%.3f total_excl_enc=%.3f" %
      (pos_el_g, neg_el_g, pos_cc_g, neg_cc_g, sep_g, elyte_g, total_g))
