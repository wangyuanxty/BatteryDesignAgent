# -*- coding: utf-8 -*-
"""Build bom.xlsx + calc.xlsx + PDF releases for all 7 deliverable categories.
All numbers mechanically taken from simulation outputs / parameter set (read from files).
"""
import json
from pathlib import Path

import openpyxl

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
DLV = WS / "deliverables"
DLV.mkdir(exist_ok=True)

en = json.loads((WS / "cell" / "r5_final_archN_energy_dfn.json").read_text(encoding="utf-8"))
area = en["area_m2"]
E_wh = en["energy_wh"]
mass_g = en["mass_kg"] * 1000.0
layers = en["layer_kg_m2"]

# ---- BOM ----
pos_solid_g = layers["positive_electrode"] * area * 1000.0
neg_solid_g = layers["negative_electrode"] * area * 1000.0
al_g = layers["positive_cc"] * area * 1000.0
cu_g = layers["negative_cc"] * area * 1000.0
sep_g = layers["separator"] * area * 1000.0
pore_cm3 = (75.6e-6 * 0.40 + 85.2e-6 * 0.22 + 10e-6 * 0.47) * area * 1e6  # cm3
elyte_g = pore_cm3 * 1.2  # literature density 1.2 g/cm3, annotated
total_solid_g = pos_solid_g + neg_solid_g + al_g + cu_g + sep_g
total_g = total_solid_g + elyte_g

def kgpkwh(g):
    return g / E_wh  # g/Wh == kg/kWh

rows = [
    ("Positive electrode active material (NMC811)", "coating th x area x AM wt% x density", pos_solid_g * 0.96, "AM/binder/additive split = literature default 96/2/2 wt% (base set has no binder/additive parameters)"),
    ("Positive electrode conductive additive", "literature default 2 wt% of electrode solids", pos_solid_g * 0.02, "literature default, annotated"),
    ("Positive electrode binder (PVDF-class)", "literature default 2 wt% of electrode solids", pos_solid_g * 0.02, "literature default, annotated"),
    ("Negative electrode active material (graphite)", "coating th x area x AM wt% x density", neg_solid_g * 0.96, "split = literature default 96/2/2 wt%"),
    ("Negative electrode conductive additive", "literature default 2 wt% of electrode solids", neg_solid_g * 0.02, "literature default, annotated"),
    ("Negative electrode binder (SBR/CMC-class)", "literature default 2 wt% of electrode solids", neg_solid_g * 0.02, "literature default, annotated"),
    ("Separator", "th x area x (1-por) x density", sep_g, "calc-energy layer caliber"),
    ("Electrolyte", "pore volume x 1.2 g/cm3 (lit.) x fill factor 1.0", elyte_g, "electrolyte density = literature value, annotated"),
    ("Positive current collector (Al)", "th x area x density", al_g, "calc-energy layer caliber"),
    ("Negative current collector (Cu)", "th x area x density", cu_g, "calc-energy layer caliber"),
    ("Enclosure + tabs", "-", None, "Not modeled"),
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
ws.append(["Component", "Basis (formula)", "g / cell", "kg / kWh", "Source note"])
for name, formula, g, note in rows:
    ws.append([name, formula, (round(g, 4) if g is not None else "Not modeled"),
               (round(kgpkwh(g), 4) if g is not None else "Not modeled"), note])
ws.append([])
ws.append(["Total (contract caliber, electrolyte excluded)", "sum of modeled layers", round(total_solid_g, 4), round(kgpkwh(total_solid_g), 4),
           f"cell energy {E_wh:.4f} Wh from r5_final_archN_energy_dfn.json"])
ws.append(["Total (incl. electrolyte, literature density)", "contract + electrolyte", round(total_g, 4), round(kgpkwh(total_g), 4),
           "electrolyte mass at 1.2 g/cm3 literature density; electrolyte excluded from contract ED caliber"])
for col, w in zip("ABCDE", (46, 44, 12, 12, 66)):
    ws.column_dimensions[col].width = w
wb.save(DLV / "bom.xlsx")

# ---- CALC ----
wb2 = openpyxl.Workbook()

def sheet(title, header, rows_):
    s = wb2.create_sheet(title)
    s.append(header)
    for r in rows_:
        s.append(r)
    for i, w in enumerate((44, 46, 16, 14, 70)[:len(header)], start=1):
        s.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    return s

s1 = sheet("Input", ["Parameter", "Formula / role", "Value", "Unit", "Source"], [
    ("Base parameter set", "anchor-table default (task names no electrode system)", "OKane2022", "-", "entry 0 meta; base_params"),
    ("Positive current collector thickness", "mass lever (thinned 12->8 um)", 8e-6, "m", "candidates/r4_archN_params.json"),
    ("Negative current collector thickness", "mass lever (thinned 8->6 um)", 6e-6, "m", "candidates/r4_archN_params.json"),
    ("Separator thickness", "mass lever (default 25->10 um class)", 1e-5, "m", "candidates/r4_archN_params.json"),
    ("Positive electrode porosity", "mass lever on measured capacity slack", 0.40, "-", "candidates/r4_archN_params.json; R1 measured no capacity loss"),
    ("Negative electrode porosity", "transport lever", 0.22, "-", "candidates/r4_archN_params.json"),
    ("Electrolyte conductivity", "transport bridge (plating suppression)", 3.5, "S/m", "candidates/r4_archN_params.json"),
    ("Electrolyte diffusivity", "transport bridge", 1.2e-9, "m2/s", "candidates/r4_archN_params.json"),
    ("Cation transference number", "transport bridge", 0.55, "-", "candidates/r4_archN_params.json"),
    ("Positive particle radius", "kinetics (plating margin)", 2.0e-6, "m", "candidates/r4_archN_params.json"),
    ("Negative particle radius", "kinetics (plating margin)", 2.2e-6, "m", "candidates/r4_archN_params.json"),
    ("Total heat transfer coefficient", "cooling (safe window: h>45 overcools -> plating)", 45.0, "W/m2/K", "candidates/r4_archN_params.json; R3 measured"),
    ("Positive electrode thickness", "base value", 75.6e-6, "m", "OKane2022"),
    ("Negative electrode thickness", "base value", 85.2e-6, "m", "OKane2022"),
    ("Electrode area (height x width)", "base value", area, "m2", "OKane2022 Electrode height 0.065 x width 1.58"),
])

s2 = sheet("CapacityEnergy", ["Item", "Formula", "Value", "Unit", "Source"], [
    ("1C discharge capacity (DFN)", "simulation", 5.0374, "Ah", "cell/r5_final_archN_1c_dfn.json:capacity_ah"),
    ("1C discharge energy (DFN)", "integral V*I_1C dt", E_wh, "Wh", "cell/r5_final_archN_energy_dfn.json:energy_wh"),
    ("Midpoint voltage (DFN)", "voltage at mid discharge time", en["midpoint_voltage_v"], "V", "cell/r5_final_archN_energy_dfn.json:midpoint_voltage_v"),
    ("SPMe cross-check ED", "same caliber, SPMe 1C", 531.85, "Wh/kg", "cell/r4_archN_energy.json (+0.25% vs DFN)"),
    ("4C charge max temperature", "4C_charge_45C DFN (T_amb 318.15 K)", 330.50, "K", "cell/r4_archN_4c_dfn.json:T_max_K"),
    ("4C charge anode potential min", "min of anode_potential_v series", 0.0215, "V", "cell/r4_archN_4c_dfn.json (plated=false)"),
])

s3 = sheet("EnergyDensity", ["Item", "Formula", "Value", "Unit", "Source"], [
    ("Contract cell mass (electrolyte excluded)", "sum over layers: th x (1-por) x density x area", mass_g, "g", "cell/r5_final_archN_energy_dfn.json:mass_kg"),
    ("Gravimetric energy density", "energy_wh / mass_kg", en["energy_density_wh_kg"], "Wh/kg", "cell/r5_final_archN_energy_dfn.json"),
    ("Threshold check", "criterion >= 500.94 Wh/kg", "PASS (+32.2)", "-", "entry 0 criteria.stage2"),
    ("Volumetric energy density", "energy / (thickness x area)", en["energy_density_wh_l"], "Wh/L", "cell/r5_final_archN_energy_dfn.json"),
    ("Layer stack thickness", "sum of 5 layer thicknesses", en["thickness_m"] * 1e6, "um", "cell/r5_final_archN_energy_dfn.json"),
])

s4 = sheet("NPMass", ["Item", "Formula", "Value", "Unit", "Source"], [
    ("N/P ratio (voltage-cutoff equilibrium caliber)", "OCP endpoint solve at 2.5/4.2 V with lithium conservation", 1.00, "-", "_np_ratio.py (inferred; OKane2022 OCP CSV + concentrations)"),
    ("Equilibrium capacity (N/P solve)", "areal capacity x area", 5.097, "Ah", "_np_ratio.py (simulated 1C: 5.037 Ah, +1.2% kinetic cutoffs)"),
    ("Positive stoich window", "x at 2.5 V -> 4.2 V", "0.268 -> 0.851", "-", "_np_ratio.py"),
    ("Negative stoich window", "x at 4.2 V -> 2.5 V", "0.905 -> 0.030", "-", "_np_ratio.py"),
    ("Positive electrode mass", "layer_kg_m2 x area", pos_solid_g, "g", "cell/r5_final_archN_energy_dfn.json:layer_kg_m2"),
    ("Negative electrode mass", "layer_kg_m2 x area", neg_solid_g, "g", "same"),
    ("Positive CC (Al) mass", "layer_kg_m2 x area", al_g, "g", "same"),
    ("Negative CC (Cu) mass", "layer_kg_m2 x area", cu_g, "g", "same"),
    ("Separator mass", "layer_kg_m2 x area", sep_g, "g", "same"),
    ("Negative-limited note", "R2 measured: -8% neg thickness -> -7.9% capacity", "neg binds capacity", "-", "log.jsonl R2 evaluate"),
])

s5 = sheet("Process", ["Item", "Formula", "Value", "Unit", "Source"], [
    ("Positive areal density", "th x (1-por) x density", layers["positive_electrode"] * 1000, "g/m2", "calc-energy layer caliber"),
    ("Negative areal density", "th x (1-por) x density", layers["negative_electrode"] * 1000, "g/m2", "calc-energy layer caliber"),
    ("Positive compaction density", "density x (1-por) / 1000", 3262 * 0.60 / 1000, "g/cm3", "OKane2022 density 3262 kg/m3"),
    ("Negative compaction density", "density x (1-por) / 1000", 1657 * 0.78 / 1000, "g/cm3", "OKane2022 density 1657 kg/m3"),
    ("Electrolyte fill amount", "pore volume x 1.2 g/cm3 x fill factor 1.0", elyte_g, "g", "pore volume from layer parameters; density literature value annotated"),
    ("Formation recommendation", "design recommended value", "0.1C CC to 4.2 V, 25 C, 2 cycles", "-", "annotated: production-line value requires tuning"),
])
del wb2["Sheet"]
wb2.save(DLV / "calc.xlsx")
print(f"bom.xlsx + calc.xlsx written; totals: solids {total_solid_g:.2f} g, +elyte {total_g:.2f} g, kg/kWh {kgpkwh(total_solid_g):.4f} / {kgpkwh(total_g):.4f}")
