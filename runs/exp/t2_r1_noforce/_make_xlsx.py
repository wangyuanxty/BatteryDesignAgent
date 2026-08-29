"""Generate bom.xlsx and calc.xlsx (openpyxl) for the t2_r1_noforce deliverables.
All values from tool outputs / parameter set (extracted via _spec_numbers.py).
"""
import openpyxl
from openpyxl.styles import Font

def sheet(ws, rows):
    for r in rows:
        ws.append(r)

# ---------------- BOM ----------------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
ws.append(["Component", "Mass (g/cell)", "kg/kWh", "Source / note"])
bom_rows = [
    ["Positive electrode active material (NMC811)", 16.842, 0.9436,
     "layer_kg_m2.positive_electrode 0.16399 kg/m2 x 0.1027 m2 (calc-energy, electrolyte excluded)"],
    ["Negative electrode active material (graphite, ceramic-coated)", 8.409, 0.4711,
     "layer_kg_m2.negative_electrode 0.08188 kg/m2 x 0.1027 m2; coating = ALD Al2O3/TiO2 class, k_SEI 4e-13"],
    ["Positive current collector (Al, 16 um)", 4.437, 0.2486,
     "layer_kg_m2.positive_cc x area; density 2700 kg/m3 (parameter set)"],
    ["Negative current collector (Cu, 12 um)", 11.042, 0.6187,
     "layer_kg_m2.negative_cc x area; density 8960 kg/m3 (parameter set)"],
    ["Separator (12 um, porosity 0.47)", 0.259, 0.0145,
     "layer_kg_m2.separator x area; density 397 kg/m3 (parameter set)"],
    ["Electrolyte (EC/EMC + LiPF6)", 8.226, 0.4609,
     "pore volume 6.855 cm3 x 1.2 g/cm3 (literature density, annotated; not in parameter set)"],
    ["Positive conductive additive / binder", "Not modeled", "Not modeled",
     "parameter set has no binder/additive volume (volfrac 0.665 + porosity 0.335 = 1.0)"],
    ["Negative conductive additive / binder", "Not modeled", "Not modeled",
     "same as positive (volfrac 0.75 + porosity 0.42 = 1.17 > 1: porosity design change; note)"],
    ["Enclosure / tabs", "Not modeled", "Not modeled", "beyond pure-simulation boundary"],
    ["TOTAL (electrolyte excluded, contract caliber)", 40.990, 2.2965,
     "calc-energy mass_kg 0.0409897 kg; energy 17.8485 Wh"],
    ["TOTAL (electrolyte included, annotated)", 49.216, 2.7574,
     "sum of rows above; energy 17.8485 Wh (r5_f1_energy.json)"],
]
sheet(ws, bom_rows)
ws.column_dimensions["A"].width = 48
ws.column_dimensions["D"].width = 78
for c in ws[1]:
    c.font = Font(bold=True)
wb.save("deliverables/bom.xlsx")
print("bom.xlsx written")

# ---------------- CALC ----------------
wb2 = openpyxl.Workbook()
ws = wb2.active
ws.title = "Inputs"
ws.append(["Parameter", "Value", "Source"])
inputs = [
    ["Base parameter set", "Chen2020", "entry 0 meta (anchor-table default; no electrode system in task text)"],
    ["Design overrides (F1)", "Negative particle radius 3e-6 m; Negative electrode porosity 0.42; SEI kinetic rate constant 4e-13", "cell/params_f1.json"],
    ["Positive electrode thickness / porosity / density", "75.6 um / 0.335 / 3262 kg/m3", "parameter set"],
    ["Negative electrode thickness / porosity (F1) / density", "85.2 um / 0.42 / 1657 kg/m3", "parameter set + params_f1.json"],
    ["Separator thickness / porosity / density", "12 um / 0.47 / 397 kg/m3", "parameter set"],
    ["CC thickness Al / Cu", "16 um / 12 um (2700 / 8960 kg/m3)", "parameter set"],
    ["Electrode height x width (area)", "0.065 m x 1.58 m (0.1027 m2)", "parameter set"],
    ["Nominal cell capacity", "5.0 Ah", "parameter set Nominal cell capacity [A.h]"],
    ["Voltage window", "2.5 - 4.2 V", "parameter set cut-offs"],
    ["Cation transference number", "0.2594", "parameter set"],
]
sheet(ws, inputs)
ws.column_dimensions["A"].width = 46
ws.column_dimensions["B"].width = 52
ws.column_dimensions["C"].width = 40
for c in ws[1]:
    c.font = Font(bold=True)

ws = wb2.create_sheet("Capacity & Energy")
ws.append(["Quantity", "Formula", "Value", "Source"])
cap_energy = [
    ["1C discharge capacity (25 C)", "CC discharge at 5 A to 2.5 V", "5.0282 Ah", "cell/r5_f1_1c_spme.json:capacity_ah"],
    ["-20 C discharge capacity", "CC discharge at 5 A, 253.15 K ambient + initial temp (cold-start fix)", "5.0003 Ah", "cell/r5_f1_lowT_spme.json:capacity_ah"],
    ["-20 C retention", "100 x cap_lowT / cap_25C", "99.45 %", "derived/r5_f1_retention.json (mechanical)"],
    ["Discharge energy (1C)", "trapezoidal integral of voltage_v x I_1C dt / 3600", "17.8485 Wh", "cell/r5_f1_energy.json:energy_wh"],
    ["Midpoint voltage", "voltage at discharge-time midpoint", "3.9794 V", "cell/r5_f1_energy.json:midpoint_voltage_v"],
]
sheet(ws, cap_energy)
for c in ws[1]:
    c.font = Font(bold=True)
for col, w in zip("ABCD", [36, 58, 16, 52]):
    ws.column_dimensions[col].width = w

ws = wb2.create_sheet("Energy Density")
ws.append(["Quantity", "Formula", "Value", "Source"])
ed_rows = [
    ["Layer masses", "layer_kg_m2 x area (pos 0.16399, neg 0.08188, AlCC 0.0432, CuCC 0.10752, sep 0.002525) kg/m2 x 0.1027 m2", "16.842 + 8.409 + 4.437 + 11.042 + 0.259 g", "cell/r5_f1_energy.json:layer_kg_m2"],
    ["Cell mass (electrolyte excluded)", "sum of layer masses", "40.990 g", "cell/r5_f1_energy.json:mass_kg"],
    ["Gravimetric energy density", "energy_wh / mass_kg", "435.44 Wh/kg (criterion >= 327.18: PASS)", "cell/r5_f1_energy.json:energy_density_wh_kg"],
    ["Volumetric energy density", "energy_wh / (thickness x area)", "865.50 Wh/L", "cell/r5_f1_energy.json:energy_density_wh_l"],
    ["DCR / power density", "V_OC at t0 - V at 10% DOD over I_1C; V_OC^2/(4 DCR)/mass", "0.2036 mOhm; 497.31 kW/kg", "cell/r5_f1_energy.json:dcr_ohm,power_density_w_kg"],
]
sheet(ws, ed_rows)
for c in ws[1]:
    c.font = Font(bold=True)
for col, w in zip("ABCD", [30, 72, 44, 52]):
    ws.column_dimensions[col].width = w

ws = wb2.create_sheet("N-P & Mass")
ws.append(["Quantity", "Formula", "Value", "Source"])
np_rows = [
    ["Negative theoretical areal capacity", "c_max 33133 mol/m3 x F/3600 x volfrac 0.75 x (1-0.42) x 85.2 um", "32.91 Ah/m2", "parameter set + params_f1.json"],
    ["Positive theoretical areal capacity", "c_max 63104 mol/m3 x F/3600 x volfrac 0.665 x (1-0.335) x 75.6 um", "56.54 Ah/m2", "parameter set"],
    ["N/P (theoretical, deliverable formula)", "neg areal cap / pos areal cap", "0.582 (baseline 0.753)", "computed above"],
    ["N/P (practical, reversible)", "measured cell cap 5.0282 Ah / cathode practical ~5.74 Ah (R1)", "~0.88 (anode-limited by design)", "r5_f1_1c_spme.json + R1 computation"],
    ["Cell thickness", "sum of layer thicknesses", "200.8 um", "cell/r5_f1_energy.json:thickness_m"],
]
sheet(ws, np_rows)
for c in ws[1]:
    c.font = Font(bold=True)
for col, w in zip("ABCD", [34, 62, 40, 52]):
    ws.column_dimensions[col].width = w

ws = wb2.create_sheet("Process")
ws.append(["Parameter", "Formula", "Value", "Note"])
proc_rows = [
    ["Positive areal density", "thickness x (1-porosity) x density", "164.0 g/m2", "75.6e-6 x 0.665 x 3262"],
    ["Negative areal density", "85.2e-6 x 0.58 x 1657", "81.9 g/m2", "porosity 0.42 (F1)"],
    ["Positive compaction density", "density x (1-porosity) / 1000", "2.169 g/cm3", "divide by 1000"],
    ["Negative compaction density", "1657 x 0.58 / 1000", "0.961 g/cm3", "divide by 1000"],
    ["Electrolyte fill amount", "pore volume x 1.2 g/cm3 x fill factor 1.0", "8.23 g", "pore volume 6.855 cm3; literature density annotated"],
    ["Formation recommendation", "design recommended value", "0.1C CC to 4.2 V, 25 C, 2 cycles", "production value requires tuning"],
]
sheet(ws, proc_rows)
for c in ws[1]:
    c.font = Font(bold=True)
for col, w in zip("ABCD", [34, 44, 22, 46]):
    ws.column_dimensions[col].width = w

wb2.save("deliverables/calc.xlsx")
print("calc.xlsx written")
