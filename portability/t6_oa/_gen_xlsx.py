import json
from pathlib import Path
import openpyxl

D = Path("runs/portability/t6_oa")
OUT = D / "deliverables"
OUT.mkdir(parents=True, exist_ok=True)

def rd(p):
    return json.load(open(D / "cell" / p, encoding="utf-8"))

energy = rd("r5_d11_energy.json")
area = energy["area_m2"]
mass_kg = energy["mass_kg"]
energy_kwh = energy["energy_wh"] / 1000.0
lk = energy["layer_kg_m2"]

m_pos_active = lk["positive_electrode"] * area * 1000
m_neg_active = lk["negative_electrode"] * area * 1000
m_pos_cc = lk["positive_cc"] * area * 1000
m_neg_cc = lk["negative_cc"] * area * 1000
m_sep = lk["separator"] * area * 1000

m_pos_cb = m_pos_active * 3 / 94
m_pos_binder = m_pos_active * 3 / 94
m_neg_cb = m_neg_active * 1 / 96
m_neg_binder = m_neg_active * 3 / 96

pore_cm3 = (75.6e-6*0.335 + 108e-6*0.25 + 7e-6*0.47) * area * 1e6
m_elyte = pore_cm3 * 1.2

def kgkwh(g):
    return g / 1000 / energy_kwh

# ---------------- BOM ----------------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
ws.append(["Component", "Mass (g/cell)", "Mass (kg/kWh)", "Source"])
rows = [
    ("Positive active material (LNMO)", m_pos_active, kgkwh(m_pos_active), "calc-energy layer_kg_m2.positive_electrode x area"),
    ("Positive conductive additive (carbon black, 3wt%)", m_pos_cb, kgkwh(m_pos_cb), "literature default (no parameter), annotated"),
    ("Positive binder (PVDF, 3wt%)", m_pos_binder, kgkwh(m_pos_binder), "literature default (no parameter), annotated"),
    ("Negative active material (graphite)", m_neg_active, kgkwh(m_neg_active), "calc-energy layer_kg_m2.negative_electrode x area"),
    ("Negative conductive additive (carbon black, 1wt%)", m_neg_cb, kgkwh(m_neg_cb), "literature default (no parameter), annotated"),
    ("Negative binder (CMC/SBR, 3wt%)", m_neg_binder, kgkwh(m_neg_binder), "literature default (no parameter), annotated"),
    ("Separator", m_sep, kgkwh(m_sep), "calc-energy layer_kg_m2.separator x area"),
    ("Electrolyte", m_elyte, kgkwh(m_elyte), "pore volume x 1.2 g/cm3 (literature density, annotated)"),
    ("Positive current collector (Al)", m_pos_cc, kgkwh(m_pos_cc), "calc-energy layer_kg_m2.positive_cc x area"),
    ("Negative current collector (Cu)", m_neg_cc, kgkwh(m_neg_cc), "calc-energy layer_kg_m2.negative_cc x area"),
    ("Enclosure / tabs", "Not modeled", "", "Not provided"),
]
for r in rows:
    ws.append(list(r))
total_all = m_pos_active + m_pos_cb + m_pos_binder + m_neg_active + m_neg_cb + m_neg_binder + m_sep + m_elyte + m_pos_cc + m_neg_cc
ws.append(["Total (incl. electrolyte, excl. casing)", total_all, kgkwh(total_all), "sum"])
ws.append(["Total (contract-caliber, electrolyte/casing excluded)", mass_kg*1000, kgkwh(mass_kg*1000), "calc-energy mass_kg"])
ws.append(["Cell energy (kWh)", energy_kwh, "", "calc-energy energy_wh"])
wb.save(OUT / "bom.xlsx")

# ---------------- CALC ----------------
wb2 = openpyxl.Workbook()
wb2.remove(wb2.active)

def sheet(title, header, rows):
    s = wb2.create_sheet(title)
    s.append(header)
    for r in rows:
        s.append(list(r))
    return s

sheet("Inputs",
      ["Parameter", "Value", "Unit", "Source"],
      [
       ("Positive electrode thickness", 75.6, "um", "parameter set"),
       ("Negative electrode thickness", 108, "um", "design override"),
       ("Separator thickness", 7, "um", "design override"),
       ("Positive current collector thickness", 8, "um", "design override"),
       ("Negative current collector thickness", 6, "um", "design override"),
       ("Positive porosity", 0.335, "-", "parameter set"),
       ("Negative porosity", 0.25, "-", "parameter set"),
       ("Positive density (LNMO)", 4400, "kg/m3", "LNMO.json"),
       ("Negative density (graphite)", 1657, "kg/m3", "parameter set"),
       ("Electrode area", area, "m2", "calc-energy"),
       ("Nominal capacity", 4.5, "Ah", "LNMO.json"),
      ])

sheet("Capacity_Energy",
      ["Quantity", "Value", "Unit", "Formula/Source"],
      [
       ("1C discharge capacity", energy["capacity_ah"], "Ah", "run-pyamm 1C_discharge"),
       ("Discharge energy", energy["energy_wh"], "Wh", "integral V*I dt"),
       ("Cell mass (contract)", energy["mass_kg"], "kg", "sum layer (1-porosity)*density*area"),
       ("Cell volume", energy["volume_m3"], "m3", "sum layer thickness*area"),
       ("Midpoint voltage", energy["midpoint_voltage_v"], "V", "calc-energy"),
      ])

sheet("Energy_Density",
      ["Quantity", "Value", "Unit", "Formula/Source"],
      [
       ("Gravimetric energy density", energy["energy_density_wh_kg"], "Wh/kg", "energy/mass"),
       ("Volumetric energy density", energy["energy_density_wh_l"], "Wh/L", "energy/volume (electrolyte excluded)"),
      ])

s_np = sheet("NP_Mass",
      ["Layer", "Areal mass (kg/m2)", "Mass (g)", "Source"],
      [
       ("Positive electrode", lk["positive_electrode"], m_pos_active, "calc-energy layer_kg_m2"),
       ("Negative electrode", lk["negative_electrode"], m_neg_active, "calc-energy layer_kg_m2"),
       ("Positive CC", lk["positive_cc"], m_pos_cc, "calc-energy layer_kg_m2"),
       ("Negative CC", lk["negative_cc"], m_neg_cc, "calc-energy layer_kg_m2"),
       ("Separator", lk["separator"], m_sep, "calc-energy layer_kg_m2"),
      ])
np = (0.895*33133*108e-6*0.75) / (energy["capacity_ah"]/area)
s_np.append(["N/P ratio (negative/positive areal capacity)", np, "", "0.895*c_max_neg*L*eps_am / (cap/area)"])

sheet("Process",
      ["Parameter", "Value", "Unit", "Formula/Source"],
      [
       ("Positive areal density", 75.6e-6*(1-0.335)*4400*1000, "g/m2", "t*(1-por)*density"),
       ("Negative areal density", 108e-6*(1-0.25)*1657*1000, "g/m2", "t*(1-por)*density"),
       ("Positive compaction density", 4400*(1-0.335)/1000, "g/cm3", "density*(1-por)/1000"),
       ("Negative compaction density", 1657*(1-0.25)/1000, "g/cm3", "density*(1-por)/1000"),
       ("Electrolyte fill amount", m_elyte, "g", "pore volume x 1.2 g/cm3 (literature)"),
       ("Formation recommendation", "0.1C CC to 4.7V, 25C, 2 cycles", "-", "design-recommended (annotated)"),
      ])

wb2.save(OUT / "calc.xlsx")
print("bom.xlsx + calc.xlsx written")
print("total_all g =", round(total_all, 2), " electrolyte g =", round(m_elyte, 2), " N/P =", round(np, 3))
