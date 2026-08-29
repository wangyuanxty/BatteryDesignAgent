# -*- coding: utf-8 -*-
"""Generate bom.xlsx and calc.xlsx for t3_r1_flash from V4 simulation outputs."""
import json, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

WS = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_flash"
OUT = os.path.join(WS, "deliverables")
os.makedirs(OUT, exist_ok=True)

def load(name):
    with open(os.path.join(WS, "cell", name), encoding="utf-8") as f:
        return json.load(f)

eng = load("r2_v4_energy.json")
cc4 = load("r2_v4_4c_dfn.json")
der = load("r2_v4_derived.json")
with open(os.path.join(WS, "cell", "params_r2_v4.json"), encoding="utf-8") as f:
    par = json.load(f)

HDR = PatternFill("solid", fgColor="1F4E79")
HDRF = Font(bold=True, color="FFFFFF", size=11)
THIN = Border(*[Side(style="thin", color="BBBBBB")] * 4)
WRAP = Alignment(wrap_text=True, vertical="top")

def style_sheet(ws, widths, nrows, ncols):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for r in range(1, nrows + 1):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.border = THIN
            if r == 1:
                cell.fill = HDR
                cell.font = HDRF
                cell.alignment = Alignment(vertical="center")
            else:
                cell.alignment = WRAP

# ---------------------------------------------------------------- bom.xlsx
wb = Workbook()
ws = wb.active
ws.title = "BOM"
rows = [
    ["#", "Component", "Material", "Mass (g/cell)", "Mass (kg/kWh)", "Note / source"],
    [1, "Positive electrode coating", "NMC-type (Chen2020)", 8.44, 0.679,
     "layer_kg_m2 0.08220 x area 0.1027 m2; binder/conductive fractions not in parameter set"],
    [2, "Negative electrode coating", "Graphite (Chen2020)", 6.12, 0.492,
     "layer_kg_m2 0.05959 x area 0.1027 m2"],
    [3, "Positive current collector", "Al (2700 kg/m3)", 4.44, 0.357,
     "16 um x 0.1027 m2 x 2700; density from parameter set"],
    [4, "Negative current collector", "Cu (8960 kg/m3)", 11.04, 0.889,
     "12 um x 0.1027 m2 x 8960; density from parameter set"],
    [5, "Separator", "PP/PE-class (Chen2020)", 0.26, 0.021,
     "layer_kg_m2 0.002525 x area 0.1027 m2"],
    [6, "Electrolyte (fill estimate)", "EC/EMC LiPF6-class, sigma 2.4 S/m", 5.48, 0.441,
     "pore volume 4.57 mL x 1.2 g/cm3 (literature, annotated estimate); not in contract mass"],
    ["", "Subtotal (contract layer mass)", "", 30.30, 2.439,
     "sum of rows 1-5; equals calc-energy mass_kg 0.0302999"],
    ["", "Subtotal (with electrolyte estimate)", "", 35.78, 2.880, "rows 1-6"],
    [7, "Enclosure / casing / tabs", "Not modeled", "N/A", "N/A",
     "no casing parameter in Chen2020 set; honest N/A"],
    ["", "Cell energy", "", 12.42, "", "r2_v4_energy.json:energy_wh (Wh)"],
    ["", "kg/kWh basis", "", "mass(g)/1000 / (12.423 Wh/1000)", "", "per component"],
]
for r in rows:
    ws.append(r)
style_sheet(ws, [4, 28, 26, 16, 16, 70], len(rows), 6)
wb.save(os.path.join(OUT, "bom.xlsx"))
print("bom.xlsx written")

# --------------------------------------------------------------- calc.xlsx
wb = Workbook()
ws = wb.active
ws.title = "Input Parameters"
rows = [
    ["Parameter", "Value", "Unit", "Source"],
    ["Positive electrode thickness", par["Positive electrode thickness [m]"], "m", "params_r2_v4.json"],
    ["Negative electrode thickness", par["Negative electrode thickness [m]"], "m", "params_r2_v4.json"],
    ["Positive electrode porosity", par["Positive electrode porosity"], "-", "params_r2_v4.json"],
    ["Negative electrode porosity", par["Negative electrode porosity"], "-", "params_r2_v4.json"],
    ["Positive particle radius", par["Positive particle radius [m]"], "m", "params_r2_v4.json"],
    ["Negative particle radius", par["Negative particle radius [m]"], "m", "params_r2_v4.json"],
    ["Electrolyte conductivity", par["Electrolyte conductivity [S.m-1]"], "S/m", "params_r2_v4.json (design override)"],
    ["Electrolyte diffusivity", par["Electrolyte diffusivity [m2.s-1]"], "m2/s", "params_r2_v4.json (design override)"],
    ["Cation transference number", par["Cation transference number"], "-", "params_r2_v4.json (design override)"],
    ["Total heat transfer coefficient", par["Total heat transfer coefficient [W.m-2.K-1]"], "W/m2/K", "params_r2_v4.json (forced-air cooling)"],
    ["Electrode height", 0.065, "m", "parameter set"],
    ["Electrode width", 1.58, "m", "parameter set"],
    ["Positive solid density", 3262.0, "kg/m3", "parameter set"],
    ["Negative solid density", 1657.0, "kg/m3", "parameter set"],
    ["Positive CC density (Al)", 2700.0, "kg/m3", "parameter set"],
    ["Negative CC density (Cu)", 8960.0, "kg/m3", "parameter set"],
    ["Electrolyte density (estimate)", 1.2, "g/cm3", "literature estimate, annotated"],
]
for r in rows:
    ws.append(r)
style_sheet(ws, [40, 24, 14, 55], len(rows), 4)

ws = wb.create_sheet("Capacity and Energy")
rows = [
    ["Quantity", "Value", "Unit", "Formula / source"],
    ["1C discharge capacity", eng["capacity_ah"], "Ah", "run-pyamm 1C_discharge, DFN, 25 C (r2_v4_1c_dfn.json)"],
    ["5C discharge capacity", der["capacity_ah_5c"], "Ah", "run-pyamm 5C_discharge, DFN, 25 C (r2_v4_5c_dfn.json)"],
    ["5C capacity retention", der["retention_5c"], "-", "5C / 1C"],
    ["4C CC-phase charge accepted", cc4["capacity_ah"], "Ah", "run-pyamm 4C_charge_45C, DFN, to 4.2 V cutoff"],
    ["Energy (1C full discharge)", eng["energy_wh"], "Wh", "integral V*I dt over 1C discharge"],
    ["Midpoint voltage", eng["midpoint_voltage_v"], "V", "voltage at 50% DOD"],
    ["DCR (1C, first 10% time)", eng["dcr_ohm"], "ohm", "(V@t0 - V@10%time)/I_1C"],
]
for r in rows:
    ws.append(r)
style_sheet(ws, [38, 22, 12, 70], len(rows), 4)

ws = wb.create_sheet("Energy Density and Power")
rows = [
    ["Quantity", "Value", "Unit", "Formula / source"],
    ["Cell mass (contract layer mass)", eng["mass_kg"] * 1000, "g", "sum(layer thickness x (1-porosity) x density x area); electrolyte excluded"],
    ["Stack thickness", eng["thickness_m"] * 1e6, "um", "sum of layer thicknesses"],
    ["Electrode area", eng["area_m2"], "m2", "height x width"],
    ["Gravimetric energy density", eng["energy_density_wh_kg"], "Wh/kg", "energy / mass (contract caliber)"],
    ["Volumetric energy density", eng["energy_density_wh_l"], "Wh/L", "energy / (thickness x area)"],
    ["Power density (theoretical peak)", eng["power_density_w_kg"], "W/kg", "V_OC^2 / (4 x DCR) / mass"],
    ["Layer mass positive", eng["layer_kg_m2"]["positive_electrode"], "kg/m2", "calc-energy output"],
    ["Layer mass negative", eng["layer_kg_m2"]["negative_electrode"], "kg/m2", "calc-energy output"],
    ["Layer mass pos CC", eng["layer_kg_m2"]["positive_cc"], "kg/m2", "calc-energy output"],
    ["Layer mass neg CC", eng["layer_kg_m2"]["negative_cc"], "kg/m2", "calc-energy output"],
    ["Layer mass separator", eng["layer_kg_m2"]["separator"], "kg/m2", "calc-energy output"],
]
for r in rows:
    ws.append(r)
style_sheet(ws, [42, 24, 10, 75], len(rows), 4)

ws = wb.create_sheet("N-P and Process")
rows = [
    ["Quantity", "Value", "Unit", "Formula / source"],
    ["Positive capacity density", 63104.0, "Ah/m3", "parameter set (per m3 active material)"],
    ["Negative capacity density", 33133.0, "Ah/m3", "parameter set (per m3 active material)"],
    ["Positive max stoichiometry", 0.60, "-", "parameter set"],
    ["Negative max stoichiometry", 0.62, "-", "parameter set"],
    ["N/P ratio (full-range capacity density)", 0.75, "-", "neg cap dens x thick / pos cap dens x thick; see design_spec"],
    ["Positive areal density", 82.2, "g/m2", "thickness x (1-porosity) x density"],
    ["Negative areal density", 59.6, "g/m2", "thickness x (1-porosity) x density"],
    ["Positive compaction density", 1957, "kg/m3", "density x (1-porosity)"],
    ["Negative compaction density", 1027, "kg/m3", "density x (1-porosity)"],
    ["Pore volume", 4.57, "mL", "sum(porosity x thickness x area) incl. separator"],
    ["Electrolyte fill (estimate)", 5.5, "g", "pore volume x 1.2 g/cm3 (literature density, annotated)"],
]
for r in rows:
    ws.append(r)
style_sheet(ws, [42, 24, 14, 70], len(rows), 4)

wb.save(os.path.join(OUT, "calc.xlsx"))
print("calc.xlsx written")
