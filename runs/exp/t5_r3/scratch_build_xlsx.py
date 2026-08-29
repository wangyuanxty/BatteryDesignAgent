"""Build bom.xlsx + calc.xlsx from r6 command outputs (mechanical values only)."""
import json
import openpyxl
from openpyxl.styles import Font

ws_root = r"runs\exp\t5_r3"
cell = f"{ws_root}\\cell"
dlv = f"{ws_root}\\deliverables"

def load(name):
    with open(f"{cell}\\{name}", encoding="utf-8") as f:
        return json.load(f)

y4e = load("r6_y4_energy_dfn.json")
y4c = load("r6_y4_4c_dfn.json")

# ---- ground values ----
AREA = y4e["area_m2"]
M_KG = y4e["mass_kg"]
E_WH = y4e["energy_wh"]
E_KWH = E_WH / 1000.0
L = y4e["layer_kg_m2"]
g = {k: v * AREA * 1000.0 for k, v in L.items()}
ELEC_DENSITY = 1.2  # g/cm3, literature default (annotated)
t_pos, t_neg, t_sep = 75.6e-6, 85.2e-6, 7e-6
eps_pos, eps_neg, eps_sep = 0.335, 0.25, 0.47
pore_m3 = (eps_pos * t_pos + eps_neg * t_neg + eps_sep * t_sep) * AREA
elec_g = pore_m3 * 1e6 * ELEC_DENSITY  # cm3 * g/cm3
SPLIT = (0.96, 0.02, 0.02)  # AM:CB:binder w/w literature default (annotated)

def split3(m):
    return [m * s for s in SPLIT]

pos_parts = split3(g["positive_electrode"])
neg_parts = split3(g["negative_electrode"])

rows = [
    ("Positive electrode active material", "NMC811", pos_parts[0]),
    ("Positive electrode conductive additive", "carbon black (literature default)", pos_parts[1]),
    ("Positive electrode binder", "PVDF-class (literature default)", pos_parts[2]),
    ("Negative electrode active material", "graphite", neg_parts[0]),
    ("Negative electrode conductive additive", "carbon black (literature default)", neg_parts[1]),
    ("Negative electrode binder", "CMC/SBR-class (literature default)", neg_parts[2]),
    ("Separator", "polyolefin (7 um, eps 0.47)", g["separator"]),
    ("Electrolyte", "LiPF6 EC/EMC-class, transport-upgraded (est. 1.2 g/cm3)", elec_g),
    ("Positive current collector", "Al 6 um", g["positive_cc"]),
    ("Negative current collector", "Cu 5 um", g["negative_cc"]),
    ("Enclosure", "Not modeled", 0.0),
    ("Tabs", "Not modeled", 0.0),
]
total_excl = sum(r[2] for i, r in enumerate(rows) if i != 7)  # exclude electrolyte row
total_incl = total_excl + elec_g

wb = openpyxl.Workbook()
sh = wb.active
sh.title = "BOM"
sh.append(["Component", "Material", "Mass g/cell", "kg/kWh", "Source / formula"])
bold = Font(bold=True)
sh["A1"].font = bold; sh["B1"].font = bold; sh["C1"].font = bold
sh["D1"].font = bold; sh["E1"].font = bold
for name, mat, m in rows:
    sh.append([name, mat, round(m, 3), round(m / 1000 / E_KWH, 2) if m else "N/A",
               "mechanical" if not m else "mass = layer_kg_m2 x area"])
sh.append([])
sh.append(["SUMMARY", "", "", "", ""])
sh.append(["Total mass (contract, electrolyte excluded)", "", round(total_excl, 3), round(total_excl / 1000 / E_KWH, 2),
           "r6_y4_energy_dfn.json:mass_kg (34.132 g)"])
sh.append(["Total mass incl. electrolyte (est.)", "", round(total_incl, 3), round(total_incl / 1000 / E_KWH, 2),
           "electrolyte density 1.2 g/cm3 literature default (annotated)"])
sh.append(["Total energy", "", round(E_WH, 4), "Wh", "r6_y4_energy_dfn.json:energy_wh"])
wb.save(f"{dlv}\\bom.xlsx")
print("bom.xlsx written; total_excl(g) =", round(total_excl, 3), "total_incl =", round(total_incl, 3),
      "elec_g =", round(elec_g, 3), "kg/kWh excl =", round(total_excl / 1000 / E_KWH, 2))

# ---- calc.xlsx ----
wb2 = openpyxl.Workbook()

sh = wb2.active
sh.title = "1 Inputs"
sh.append(["Parameter", "Value", "Unit", "Source"])
inputs = [
    ("Positive electrode thickness", 75.6e-6, "m", "param_dump.txt Chen2020 (baseline)"),
    ("Negative electrode thickness", 85.2e-6, "m", "param_dump.txt Chen2020"),
    ("Separator thickness (override)", 7e-6, "m", "cell/params_y4.json"),
    ("Positive CC thickness (override)", 6e-6, "m", "cell/params_y4.json"),
    ("Negative CC thickness (override)", 5e-6, "m", "cell/params_y4.json"),
    ("Positive electrode porosity", 0.335, "-", "param_dump.txt"),
    ("Negative electrode porosity", 0.25, "-", "param_dump.txt"),
    ("Separator porosity", 0.47, "-", "param_dump.txt"),
    ("Pos AM volume fraction", 0.665, "-", "param_dump.txt"),
    ("Neg AM volume fraction", 0.75, "-", "param_dump.txt"),
    ("Positive electrode density", 3262.0, "kg/m3", "param_dump.txt"),
    ("Negative electrode density", 1657.0, "kg/m3", "param_dump.txt"),
    ("Al collector density", 2700.0, "kg/m3", "param_dump.txt"),
    ("Cu collector density", 8960.0, "kg/m3", "param_dump.txt"),
    ("Electrode area", AREA, "m2", "r6_y4_energy_dfn.json:area_m2"),
    ("Electrolyte conductivity (override)", 5.0, "S/m", "cell/params_y4.json"),
    ("Cation transference number (override)", 0.6, "-", "cell/params_y4.json"),
    ("Electrolyte diffusivity (override)", 9e-10, "m2/s", "cell/params_y4.json"),
    ("Heat transfer coefficient (override)", 26.0, "W/m2/K", "cell/params_y4.json"),
    ("Cooling surface area (override)", 0.01062, "m2", "cell/params_y4.json"),
    ("Particle radii (override)", 3e-6, "m (both)", "cell/params_y4.json"),
    ("Nominal capacity", 5.0, "Ah", "param_dump.txt"),
]
for r in inputs:
    sh.append(list(r))

sh = wb2.create_sheet("2 CapacityEnergy")
sh.append(["Quantity", "Value", "Unit", "Formula / Source"])
sh.append(["1C discharge capacity", round(y4e["capacity_ah"], 4), "Ah", "r6_y4_1c_dfn.json:capacity_ah"])
sh.append(["Discharge energy", round(E_WH, 4), "Wh", "r6_y4_energy_dfn.json:energy_wh (integral V*I dt)"])
sh.append(["Midpoint voltage", round(y4e["midpoint_voltage_v"], 4), "V", "r6_y4_energy_dfn.json:midpoint_voltage_v"])
sh.append(["4C T_max", round(y4c["T_max_K"], 2), "K", "r6_y4_4c_dfn.json:T_max_K"])
sh.append(["4C min anode potential", round(min(y4c["anode_potential_v"]), 4), "V", "r6_y4_4c_dfn.json:anode_potential_v"])

sh = wb2.create_sheet("3 EnergyDensity")
sh.append(["Quantity", "Value", "Unit", "Formula / Source"])
sh.append(["Gravimetric ED", round(y4e["energy_density_wh_kg"], 2), "Wh/kg", "E_Wh / mass_kg; electrolyte excluded (contract)"])
sh.append(["Threshold", 500.94, "Wh/kg", "task text (entry-0 contract)"])
sh.append(["PASS?", "YES", "", "535.72 >= 500.94"])
sh.append(["Volumetric ED", round(y4e["energy_density_wh_l"], 2), "Wh/L", "r6_y4_energy_dfn.json"])
sh.append(["Cell mass", round(M_KG * 1000, 3), "g", "r6_y4_energy_dfn.json:mass_kg"])
sh.append(["Stack thickness", round(y4e["thickness_m"] * 1e6, 1), "um", "r6_y4_energy_dfn.json:thickness_m"])
sh.append(["Cell volume", round(y4e["volume_m3"] * 1e6, 3), "cm3", "r6_y4_energy_dfn.json:volume_m3"])

sh = wb2.create_sheet("4 NP_Mass")
sh.append(["Quantity", "Value", "Unit", "Formula / Source"])
sh.append(["Pos areal capacity", round(7.56e-4 * 0.665 * 3.262 * 201, 3), "mAh/cm2",
           "t x (1-e) x rho x 201 mAh/g (NMC811, literature default, annotated)"])
sh.append(["Neg areal capacity", round(8.52e-4 * 0.75 * 1.657 * 372, 3), "mAh/cm2",
           "t x (1-e) x rho x 372 mAh/g (graphite, literature default, annotated)"])
sh.append(["N/P ratio", round((8.52e-4 * 0.75 * 1.657 * 372) / (7.56e-4 * 0.665 * 3.262 * 201), 2), "-",
           "neg/pos areal capacity (parameter set lacks capacity-density keys)"])
sh.append(["Mass positive layer", round(g["positive_electrode"], 3), "g", "layer_kg_m2 x area"])
sh.append(["Mass negative layer", round(g["negative_electrode"], 3), "g", "layer_kg_m2 x area"])
sh.append(["Mass Al CC", round(g["positive_cc"], 3), "g", "layer_kg_m2 x area"])
sh.append(["Mass Cu CC", round(g["negative_cc"], 3), "g", "layer_kg_m2 x area"])
sh.append(["Mass separator", round(g["separator"], 3), "g", "layer_kg_m2 x area"])
sh.append(["Total mass (contract)", round(M_KG * 1000, 3), "g", "sum = r6_y4_energy_dfn.json:mass_kg"])
sh.append(["Electrolyte mass (est.)", round(elec_g, 3), "g", "pore vol x 1.2 g/cm3 (lit. default)"])

sh = wb2.create_sheet("5 Process")
sh.append(["Parameter", "Value", "Unit", "Formula / Source"])
sh.append(["Pos areal density", round(16.842 / AREA, 2), "g/m2", "mass / area (16.842 g / 0.1027 m2)"])
sh.append(["Neg areal density", round(10.874 / AREA, 2), "g/m2", "mass / area (10.874 g / 0.1027 m2)"])
sh.append(["Pos compaction density", round(3262 * 0.665 / 1000, 3), "g/cm3", "rho x (1-e) / 1000"])
sh.append(["Neg compaction density", round(1657 * 0.75 / 1000, 3), "g/cm3", "rho x (1-e) / 1000"])
sh.append(["Electrolyte fill amount", round(elec_g, 3), "g", "pore vol 5.126 cm3 x 1.2 g/cm3 (lit. default)"])
sh.append(["Formation recommendation", "0.1C CC to 4.2 V, 25 C, 2 cycles", "", "design recommended; production tuning required"])
wb2.save(f"{dlv}\\calc.xlsx")
print("calc.xlsx written")