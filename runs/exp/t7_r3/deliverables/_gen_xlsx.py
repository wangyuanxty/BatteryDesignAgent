# -*- coding: utf-8 -*-
"""One-off deliverable generator: bom.xlsx + calc.xlsx for case t7_r3 (values mechanically
taken from bda outputs / Chen2020 parameter set; sources annotated per row)."""
import json
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

DEL = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t7_r3"

def load(name):
    return json.load(io.open(DEL + "/cell/" + name, encoding="utf-8"))

energy = load("r7_v19_final_energy.json")
aging = load("r7_v19_final_aging45c.json")
c4 = load("r7_v19_final_4c45c.json")
onec = load("r7_v19_final_1c.json")

AREA = energy["area_m2"]           # 0.1027 m2
LM = energy["layer_kg_m2"]
G_POS = LM["positive_electrode"] * AREA * 1000.0
G_NEG = LM["negative_electrode"] * AREA * 1000.0
G_AL = LM["positive_cc"] * AREA * 1000.0
G_CU = LM["negative_cc"] * AREA * 1000.0
G_SEP = LM["separator"] * AREA * 1000.0
G_EL = 7.21  # g: pore volume 6.004e-6 m3 x 1200 kg/m3 (literature 1.2 g/cm3)
E_WH = energy["energy_wh"]
KG_PER_KWH = 1000.0 / E_WH  # => kg/kWh = g * (1/1000) * (1000/E_WH) = g / E_WH

HDR_FILL = PatternFill("solid", fgColor="14283C")
HDR_FONT = Font(bold=True, color="FFFFFF")

# ---------------- bom.xlsx ----------------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
rows = [
    ["Component", "Mass g/cell", "kg/kWh", "Volume-fraction / basis", "Source"],
    ["Positive active material (NMC811)", G_POS, G_POS / E_WH, "active vol frac 0.665, layer 75.6 um",
     "r7_v19_final_energy.json layer_kg_m2 x area (contract mass caliber; model has no inactive phases)"],
    ["Positive conductive additive", "Not modeled", "Not modeled", "no parameter in Chen2020; industry rec. ~2 wt%",
     "parameter set gap (annotated)"],
    ["Positive binder (PVDF)", "Not modeled", "Not modeled", "no parameter; industry rec. ~2 wt%",
     "parameter set gap (annotated)"],
    ["Negative active material (graphite)", G_NEG, G_NEG / E_WH, "active vol frac 0.75, layer 110 um",
     "r7_v19_final_energy.json layer_kg_m2"],
    ["Negative conductive additive", "Not modeled", "Not modeled", "no parameter; industry rec. ~1 wt%",
     "parameter set gap (annotated)"],
    ["Negative binder (CMC/SBR)", "Not modeled", "Not modeled", "no parameter; industry rec. ~3 wt%",
     "parameter set gap (annotated)"],
    ["Separator", G_SEP, G_SEP / E_WH, "12 um x 0.53 (1-porosity 0.47)",
     "r7_v19_final_energy.json layer_kg_m2"],
    ["Electrolyte", G_EL, G_EL / E_WH, "pore volume 6.004 mL x 1.2 g/cm3 (literature density), fill 1.0",
     "derived: porosities x geometry; density = literature default (1.2 g/cm3)"],
    ["Positive current collector (Al)", G_AL, G_AL / E_WH, "16 um x 2700 kg/m3", "Chen2020 set"],
    ["Negative current collector (Cu)", G_CU, G_CU / E_WH, "12 um x 8960 kg/m3", "Chen2020 set"],
    ["Enclosure / tabs", "Not modeled", "Not modeled", "", "parameter set gap (annotated)"],
    ["TOTAL (contract, electrolyte excluded)", G_POS + G_NEG + G_AL + G_CU + G_SEP,
     (G_POS + G_NEG + G_AL + G_CU + G_SEP) / E_WH, "mass_kg 0.0466198 x1000", "energy.json:mass_kg"],
    ["TOTAL incl. electrolyte", G_POS + G_NEG + G_AL + G_CU + G_SEP + G_EL,
     (G_POS + G_NEG + G_AL + G_CU + G_SEP + G_EL) / E_WH, "", "derived (electrolyte excluded from contract)]"],
    ["Cell energy (Wh)", E_WH, "", "integral V x I_1C dt, I_1C = 6.28 A", "energy.json:energy_wh"],
]
for r in rows:
    ws.append(r)
for i, c in enumerate(ws[1], start=1):
    c.fill = HDR_FILL; c.font = HDR_FONT
for col, w in zip("ABCDE", (42, 16, 12, 52, 66)):
    ws.column_dimensions[col].width = w
wb.save(DEL + "/deliverables/bom.xlsx")

# ---------------- calc.xlsx ----------------
wb2 = openpyxl.Workbook()
def sheet(name, header, rows, widths):
    ws = wb2.create_sheet(name)
    ws.append(header)
    for r in rows:
        ws.append(r)
    for i, c in enumerate(ws[1], start=1):
        c.fill = HDR_FILL; c.font = HDR_FONT
    for col, w in zip("ABCDEF", widths):
        ws.column_dimensions[col].width = w

sheet("input_parameters",
      ["Parameter", "Value (final design)", "Unit", "Base (Chen2020)", "Changed by", "Source"],
      [
       ["Nominal cell capacity", 6.28, "Ah", 5.0, "yes (honest re-rating)", "r7_v19_final_params.json"],
       ["Positive electrode thickness", 75.6e-6, "m", 75.6e-6, "no", "Chen2020 set"],
       ["Negative electrode thickness", 110e-6, "m", 85.2e-6, "yes", "r7_v19_final_params.json"],
       ["Separator thickness", 12e-6, "m", 12e-6, "no", "Chen2020 set"],
       ["Positive particle radius", 2.0e-6, "m", 5.22e-6, "yes", "r7_v19_final_params.json"],
       ["Negative particle radius", 2.0e-6, "m", 5.86e-6, "yes", "r7_v19_final_params.json"],
       ["Positive porosity", 0.335, "-", 0.335, "no", "Chen2020 set"],
       ["Negative porosity", 0.25, "-", 0.25, "no", "Chen2020 set"],
       ["Positive active volume fraction", 0.665, "-", 0.665, "no", "Chen2020 set"],
       ["Cation transference number", 0.6, "-", 0.2594, "yes", "r7_v19_final_params.json"],
       ["Electrolyte conductivity", 1.5, "S/m", "Nyman2008 fn", "yes", "r7_v19_final_params.json"],
       ["Electrolyte diffusivity", 1.0e-9, "m2/s", "Nyman2008 fn", "yes", "r7_v19_final_params.json"],
       ["Upper / lower voltage cut-off", "4.2 / 2.5", "V", "same", "no", "Chen2020 set"],
       ["Electrode height x width", "0.065 x 1.58", "m", "same", "no", "Chen2020 set"],
       ["Ambient temp (charge/aging)", 45.0 + 273.15, "K", "-", "protocol", "aging_1C_100cyc_45C / 4C_charge_45C"],
      ], (40, 20, 12, 16, 22, 44))
sheet("capacity_energy",
      ["Quantity", "Formula", "Value", "Unit", "Source"],
      [
       ["1C discharge capacity (SPMe)", "protocol 1C_discharge, CC 6.28 A to 2.5 V", onec["capacity_ah"], "Ah", "r7_v19_final_1c.json:capacity_ah"],
       ["1C discharge capacity (DFN)", "protocol 1C_discharge DFN", 6.28, "Ah", "r6_v19_1c_dfn.json"],
       ["Rated energy", "integral V x I_1C dt / 3600, I_1C = 6.28 A", E_WH, "Wh", "energy.json:energy_wh"],
       ["Midpoint voltage", "V at 50% of discharge time", energy["midpoint_voltage_v"], "V", "energy.json"],
       ["DCR", "(V(t0) - V(t=10%)) / I_1C", energy["dcr_ohm"], "ohm", "energy.json:dcr_ohm"],
       ["Aging SEI end (100cyc@45C)", "SEI ec-reaction-limited model", aging["sei_thickness_nm_end"], "nm", "r7_v19_final_aging45c.json"],
       ["4C anode surface potential min", "DFN + plating, 25.12 A charge", min(c4["anode_potential_v"]), "V", "r7_v19_final_4c45c.json:anode_potential_v"],
       ["4C T_max", "lumped thermal", c4["T_max_K"], "K", "r7_v19_final_4c45c.json:T_max_K"],
      ], (40, 46, 18, 10, 60))
sheet("energy_density",
      ["Quantity", "Formula", "Value", "Unit", "Source"],
      [
       ["Contract mass (electrolyte excluded)", "sum layer thickness x (1-porosity) x density x area", energy["mass_kg"] * 1000, "g", "energy.json:mass_kg"],
       ["Energy density (contract caliber)", "E_Wh / mass_kg", energy["energy_density_wh_kg"], "Wh/kg", "energy.json:energy_density_wh_kg"],
       ["Threshold (task text)", "", 327.18, "Wh/kg", "log.jsonl entry 0 stage2"],
       ["Electrolyte mass add-on", "pore volume 6.004e-6 m3 x 1200 kg/m3 (lit.)", G_EL, "g", "derived (literature density 1.2 g/cm3)"],
       ["Energy density incl. electrolyte", "22.49098 / (0.0466198 + 0.00721)", E_WH / (0.0466198 + G_EL / 1000.0), "Wh/kg", "derived"],
       ["Volumetric energy density", "E_Wh / (stack thickness 225.6e-6 x area m3)", energy["energy_density_wh_l"], "Wh/L", "energy.json"],
       ["Power density (peak proxy)", "Voc^2 / (4 x DCR) / mass", energy["power_density_w_kg"], "W/kg", "energy.json:power_density_w_kg"],
      ], (44, 52, 20, 12, 48))
sheet("np_and_mass",
      ["Quantity", "Formula", "Value", "Unit", "Source"],
      [
       ["Positive areal Li capacity", "63104 x 0.665 x 75.6e-6", 3.1725, "mol/m2", "Chen2020 max conc + geometry"],
       ["Negative areal Li capacity", "33133 x 0.75 x 110e-6", 2.7335, "mol/m2", "Chen2020 max conc + geometry"],
       ["N/P ratio", "neg/pos areal capacity", 2.7335 / 3.1725, "-", "mechanical derivation"],
       ["Positive electrode mass", "164.0 g/m2 x 0.1027 m2", G_POS, "g", "energy.json layer_kg_m2 x area"],
       ["Negative electrode mass", "136.7 g/m2 x 0.1027 m2", G_NEG, "g", "energy.json layer_kg_m2 x area"],
       ["Al collector mass", "43.2 g/m2 x 0.1027 m2", G_AL, "g", "energy.json layer_kg_m2"],
       ["Cu collector mass", "107.5 g/m2 x 0.1027 m2", G_CU, "g", "energy.json layer_kg_m2"],
       ["Separator mass", "2.52 g/m2 x 0.1027 m2", G_SEP, "g", "energy.json layer_kg_m2"],
       ["Total contract mass", "sum of layers", (G_POS + G_NEG + G_AL + G_CU + G_SEP), "g", "energy.json:mass_kg x1000"],
      ], (34, 40, 16, 10, 46))
sheet("process_parameters",
      ["Process parameter", "Formula", "Value", "Unit", "Source"],
      [
       ["Positive areal density", "thickness x (1-porosity) x density", round(LM["positive_electrode"] * 1000, 1), "g/m2", "energy.json layer_kg_m2"],
       ["Negative areal density", "thickness x (1-porosity) x density", round(LM["negative_electrode"] * 1000, 1), "g/m2", "energy.json layer_kg_m2"],
       ["Positive compaction density", "3262 x (1-0.335) / 1000", 3262 * 0.665 / 1000, "g/cm3", "Chen2020 density x (1-porosity) / 1000"],
       ["Negative compaction density", "1657 x (1-0.25) / 1000", 1657 * 0.75 / 1000, "g/cm3", "Chen2020 density x (1-porosity) / 1000"],
       ["Electrolyte fill amount", "pore volume x 1200 kg/m3", G_EL, "g/cell", "6.004 mL x 1.2 g/cm3 (literature)"],
       ["Formation recommendation", "0.1C CC to 4.2 V, 25 C, 2 cycles", "-", "-", "design-recommended value; production requires tuning"],
      ], (34, 44, 16, 12, 60))
wb2.remove(wb2["Sheet"])
wb2.save(DEL + "/deliverables/calc.xlsx")
print("bom.xlsx + calc.xlsx written")
print("G: pos=%.2f neg=%.2f al=%.2f cu=%.2f sep=%.3f el=%.2f | kg/kWh tot-incl=%.3f" % (
    G_POS, G_NEG, G_AL, G_CU, G_SEP, G_EL, (G_POS + G_NEG + G_AL + G_CU + G_SEP + G_EL) / E_WH))