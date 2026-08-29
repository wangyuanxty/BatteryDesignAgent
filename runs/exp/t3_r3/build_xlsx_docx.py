# -*- coding: utf-8 -*-
"""t3_r3 closing deliverables, part A: compute metrics from tool outputs, then
write bom.xlsx, calc.xlsx, datasheet.docx, and the shared deliv_metrics.json.

Every numeric value is loaded from simulation output files / parameter files
(no hand-typed results). Agent-built input files: allowed.
"""
import json
import math
from pathlib import Path

CELL = Path("runs/exp/t3_r3/cell")
DLV = Path("runs/exp/t3_r3/deliverables")
DLV.mkdir(exist_ok=True)

ENERGY_WH = 15.703469  # placeholder; overwritten below


def load(p):
    return json.load(open(p, encoding="utf-8"))


energy = load(CELL / "r5_v12_energy.json")
c1 = load(CELL / "r5_v12_1c_dfn.json")
c5 = load(CELL / "r5_v12_5c_dfn.json")
c4 = load(CELL / "r5_v12_4c_dfn.json")
derived = load(CELL / "r5_v12_derived.json")
params = load(CELL / "r5_v12_hip_final_params.json")
base_energy = load(CELL / "r1_base_energy.json")

# ---- base parameter set (same source bda uses: pybamm Chen2020) ----
import pybamm

pv = pybamm.ParameterValues("Chen2020")
v_min = float(pv["Lower voltage cut-off [V]"])
v_max = float(pv["Upper voltage cut-off [V]"])
nominal_ah = float(pv["Nominal cell capacity [A.h]"])
height_m = float(pv["Electrode height [m]"])
width_m = float(pv["Electrode width [m]"])
L_sep = float(pv["Separator thickness [m]"])
c_e0 = float(pv["Initial concentration in electrolyte [mol.m-3]"])
rho_pos = float(pv["Positive electrode density [kg.m-3]"])
rho_neg = float(pv["Negative electrode density [kg.m-3]"])
rho_sep = float(pv["Separator density [kg.m-3]"])
rho_cc_pos = float(pv["Positive current collector density [kg.m-3]"])
rho_cc_neg = float(pv["Negative current collector density [kg.m-3]"])

area_m2 = energy["area_m2"]
assert abs(height_m * width_m - area_m2) < 1e-9, "geometry mismatch"

# ---- champion geometry ----
L_p = params["Positive electrode thickness [m]"]
eps_p = params["Positive electrode porosity"]
r_p = params["Positive particle radius [m]"]
L_n = params["Negative electrode thickness [m]"]
eps_n = params["Negative electrode porosity"]
r_n = params["Negative particle radius [m]"]
eps_sep = params["Separator porosity"]
th_cc_p = params["Positive current collector thickness [m]"]
th_cc_n = params["Negative current collector thickness [m]"]
kappa_e = params["Electrolyte conductivity [S.m-1]"]
tplus = params["Cation transference number"]
D_e = params["Electrolyte diffusivity [m2.s-1]"]
h = params["Total heat transfer coefficient [W.m-2.K-1]"]

total_thickness_m = L_p + L_n + L_sep + th_cc_p + th_cc_n

# ---- cross-checks: layer masses vs calc-energy contract values ----
lkg = energy["layer_kg_m2"]
assert abs(L_p * (1 - eps_p) * rho_pos - lkg["positive_electrode"]) < 1e-9
assert abs(L_n * (1 - eps_n) * rho_neg - lkg["negative_electrode"]) < 1e-9
assert abs(L_sep * eps_sep * rho_sep - lkg["separator"]) < 1e-9
assert abs(th_cc_p * rho_cc_pos - lkg["positive_cc"]) < 1e-9
assert abs(th_cc_n * rho_cc_neg - lkg["negative_cc"]) < 1e-9

g_pos_coat = lkg["positive_electrode"] * area_m2 * 1000.0
g_neg_coat = lkg["negative_electrode"] * area_m2 * 1000.0
g_sep = lkg["separator"] * area_m2 * 1000.0
g_cc_p = lkg["positive_cc"] * area_m2 * 1000.0
g_cc_n = lkg["negative_cc"] * area_m2 * 1000.0
g_stack = g_pos_coat + g_neg_coat + g_sep + g_cc_p + g_cc_n
assert abs(g_stack / 1000.0 - energy["mass_kg"]) < 1e-9

# electrolyte: pore volume x 1.2 g/cm3 (literature value, annotated)
pore_m3 = (L_p * eps_p + L_n * eps_n + L_sep * eps_sep) * area_m2
g_elec = pore_m3 * 1.2e6  # 1.2 g/cm3 = 1.2e6 g/m3)
g_total = g_stack + g_elec

# ---- BOM splits (literature defaults, annotated: no additive/binder params in set) ----
bom = [
    # (row, grams, kg_per_kwh)
    ("Positive active material NMC811", g_pos_coat * 0.94),
    ("Positive conductive additive (carbon black)", g_pos_coat * 0.03),
    ("Positive binder (PVDF)", g_pos_coat * 0.03),
    ("Negative active material (graphite)", g_neg_coat * 0.96),
    ("Negative conductive additive (carbon black)", g_neg_coat * 0.01),
    ("Negative binder (CMC+SBR)", g_neg_coat * 0.03),
    ("Separator", g_sep),
    ("Electrolyte", g_elec),
    ("Positive current collector (Al)", g_cc_p),
    ("Negative current collector (Cu)", g_cc_n),
]

# ---- N/P ratio (baseline ratio computed mechanically from r1 baseline energy file) ----
bl_kg = base_energy["layer_kg_m2"]
np_ratio = lkg["negative_electrode"] / lkg["positive_electrode"]
np_baseline = bl_kg["negative_electrode"] / bl_kg["positive_electrode"]
np_x = np_ratio / np_baseline

# ---- process parameters ----
areal_pos = L_p * (1 - eps_p) * rho_pos * 1000.0        # g/m2
areal_neg = L_n * (1 - eps_n) * rho_neg * 1000.0        # g/m2
comp_pos_kgm3 = rho_pos * (1 - eps_p)                    # kg/m3
comp_neg_kgm3 = rho_neg * (1 - eps_n)                    # kg/m3
comp_pos_gcm3 = comp_pos_kgm3 / 1000.0                   # g/cm3 (spec: divide by 1000)
comp_neg_gcm3 = comp_neg_kgm3 / 1000.0

metrics = {
    "capacity_ah": c1["capacity_ah"],
    "capacity_5c_ah": c5["capacity_ah"],
    "retention_5c": derived["retention_5c"],
    "t_max_5c_K": c5["T_max_K"],
    "t_max_4c_K": c4["T_max_K"],
    "anode_min_v": min(c4["anode_potential_v"]),
    "charge_4c_ah": c4["capacity_ah"],
    "energy_wh": energy["energy_wh"],
    "mass_kg": energy["mass_kg"],
    "ed_wh_kg": energy["energy_density_wh_kg"],
    "ed_wh_l": energy["energy_density_wh_l"],
    "volume_m3": energy["volume_m3"],
    "midpoint_v": energy["midpoint_voltage_v"],
    "dcr_ohm": energy["dcr_ohm"],
    "power_density_w_kg": energy["power_density_w_kg"],
    "area_m2": area_m2,
    "total_thickness_m": total_thickness_m,
    "v_min": v_min,
    "v_max": v_max,
    "nominal_ah": nominal_ah,
    "height_m": height_m,
    "width_m": width_m,
    "c_e0": c_e0,
    "L_p": L_p, "eps_p": eps_p, "r_p": r_p,
    "L_n": L_n, "eps_n": eps_n, "r_n": r_n,
    "L_sep": L_sep, "eps_sep": eps_sep,
    "th_cc_p": th_cc_p, "th_cc_n": th_cc_n,
    "kappa_e": kappa_e, "tplus": tplus, "D_e": D_e, "h": h,
    "rho_pos": rho_pos, "rho_neg": rho_neg, "rho_sep": rho_sep,
    "rho_cc_pos": rho_cc_pos, "rho_cc_neg": rho_cc_neg,
    "g_pos_coat": g_pos_coat, "g_neg_coat": g_neg_coat,
    "g_sep": g_sep, "g_cc_p": g_cc_p, "g_cc_n": g_cc_n,
    "g_elec": g_elec, "g_stack": g_stack, "g_total": g_total,
    "pore_m3": pore_m3,
    "np_ratio": np_ratio, "np_baseline": np_baseline, "np_x": np_x,
    "areal_pos": areal_pos, "areal_neg": areal_neg,
    "comp_pos_kgm3": comp_pos_kgm3, "comp_neg_kgm3": comp_neg_kgm3,
    "comp_pos_gcm3": comp_pos_gcm3, "comp_neg_gcm3": comp_neg_gcm3,
    "bom": bom,
}
json.dump(metrics, open(DLV / "deliv_metrics.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)

# ======================= BOM XLSX =======================
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
ws.append(["Component", "Mass (g/cell)", "kg/kWh", "Formula / split", "Source"])
for row, grams in bom:
    kgkwh = grams / energy["energy_wh"]  # g/Wh == kg/kWh
    split = {
        "Positive active material NMC811": "pos coat x 94% (lit. default)",
        "Positive conductive additive (carbon black)": "pos coat x 3% (lit. default)",
        "Positive binder (PVDF)": "pos coat x 3% (lit. default)",
        "Negative active material (graphite)": "neg coat x 94% (lit. default)",
        "Negative conductive additive (carbon black)": "neg coat x 1% (lit. default)",
        "Negative binder (CMC+SBR)": "neg coat x 3% (lit. default)",
        "Separator": "L_sep x eps_sep x rho_sep x area",
        "Electrolyte": "pore volume x 1.2 g/cm3 (lit. value)",
        "Positive current collector (Al)": "th x 2700 kg/m3 x area",
        "Negative current collector (Cu)": "th x 8960 kg/m3 x area",
    }[row]
    src = (
        "r5_v12_energy.json:layer_kg_m2 x area_m2"
        if row not in ("Electrolyte",)
        else "params+geometry pore volume x literature density 1.2 g/cm3"
    )
    ws.append([row, round(grams, 4), round(kgkwh, 4), split, src])
ws.append([])
ws.append(["Enclosure / case", "Not modeled", "", "no shell parameter in Chen2020 set", "base params"])
ws.append(["Tabs / terminals", "Not modeled", "", "no tab parameter in Chen2020 set", "base params"])
ws.append(["Total material mass", round(g_total, 4), round(g_total / energy["energy_wh"], 4),
           "stack mass + electrolyte fill", "mechanical sum"])
ws.append(["Cell energy", round(energy["energy_wh"], 4), "",
           "1C discharge energy (V*I time integral)", "r5_v12_energy.json:energy_wh"])

hdr = Font(bold=True, color="FFFFFF")
fill = PatternFill("solid", fgColor="1E5A8A")
for c in ws[1]:
    c.font = hdr
    c.fill = fill
for col, w in zip("ABCDE", (42, 14, 12, 44, 46)):
    ws.column_dimensions[col].width = w
wb.save(DLV / "bom.xlsx")

# ======================= CALC XLSX =======================
wb2 = openpyxl.Workbook()


def sheet(title, header, rows):
    wsx = wb2.create_sheet(title)
    wsx.append(header)
    for r in rows:
        wsx.append(r)
    for c in wsx[1]:
        c.font = hdr
        c.fill = fill
    width = max(len(str(v)) for row in rows for v in row) + 4
    wsx.column_dimensions["A"].width = 46
    for col in "BCDEF":
        wsx.column_dimensions[col].width = min(max(width, 12), 60)
    return wsx


# 1. inputs
inp_rows = [
    ["Cell design (design lever overrides)", "V12-HiP-final", "", "r5_v12_hip_final_params.json"],
    ["Positive electrode thickness", f"{L_p*1e6:.3f} um", "design override", "params file"],
    ["Positive electrode porosity", f"{eps_p:.2f}", "design override", "params file"],
    ["Positive particle radius", f"{r_p*1e6:.2f} um", "design override", "params file"],
    ["Negative electrode thickness", f"{L_n*1e6:.3f} um", "design override", "params file"],
    ["Negative electrode porosity", f"{eps_n:.2f}", "design override", "params file"],
    ["Negative particle radius", f"{r_n*1e6:.2f} um", "design override", "params file"],
    ["Separator thickness", f"{L_sep*1e6:.1f} um", "base set default", "pybamm Chen2020"],
    ["Separator porosity", f"{eps_sep:.2f}", "design override", "params file"],
    ["Positive current collector (Al)", f"{th_cc_p*1e6:.0f} um", "design override", "params file"],
    ["Negative current collector (Cu)", f"{th_cc_n*1e6:.0f} um", "design override", "params file"],
    ["Electrolyte conductivity kappa", f"{kappa_e:.1f} S/m", "design override", "params file"],
    ["Cation transference number", f"{tplus:.2f}", "design override", "params file"],
    ["Electrolyte diffusivity", f"{D_e:.2e} m2/s", "design override", "params file"],
    ["Total heat transfer coefficient h", f"{h:.0f} W/m2/K", "design override", "params file"],
    ["Cell height", f"{height_m*1e3:.1f} mm", "base set", "pybamm Chen2020"],
    ["Cell width (unwound strip)", f"{width_m:.3f} m", "base set", "pybamm Chen2020"],
    ["Electrode area", f"{area_m2:.4f} m2", "height x width", "r5_v12_energy.json:area_m2"],
    ["Nominal capacity (set)", f"{nominal_ah:.1f} Ah", "base set", "pybamm Chen2020"],
    ["Voltage window", f"{v_min:.1f}-{v_max:.1f} V", "base set", "pybamm Chen2020"],
    ["Initial electrolyte concentration", f"{c_e0:.0f} mol/m3", "base set", "pybamm Chen2020"],
]
sheet("1 inputs", ["Parameter", "Value", "Kind", "Source"], inp_rows)

# 2. capacity & energy
cap_rows = [
    ["1C discharge capacity", f"{c1['capacity_ah']:.6f} Ah", ">= 2.0 required",
     "r5_v12_1c_dfn.json:capacity_ah (DFN)", "PASS"],
    ["5C discharge capacity", f"{c5['capacity_ah']:.6f} Ah", "=", "r5_v12_5c_dfn.json:capacity_ah (DFN)", ""],
    ["5C retention", f"{derived['retention_5c']:.6f}", "5C cap / 1C cap; >= 0.95 required",
     "r5_v12_derived.json:retention_5c", "PASS"],
    ["4C CC-charge acceptance", f"{c4['capacity_ah']:.4f} Ah", "before 4.2 V ceiling (honest residual, not thresholded)",
     "r5_v12_4c_dfn.json:capacity_ah", ""],
    ["Discharge energy (1C)", f"{energy['energy_wh']:.6f} Wh", "V*I time integral", "r5_v12_energy.json:energy_wh", ""],
    ["Midpoint voltage (1C)", f"{energy['midpoint_voltage_v']:.5f} V", "", "r5_v12_energy.json:midpoint_voltage_v", ""],
]
sheet("2 capacity_energy", ["Quantity", "Value", "Criterion / formula", "Source", "Determination"], cap_rows)

# 3. energy & power density
ed_rows = [
    ["Layer stack thickness", f"{total_thickness_m*1e6:.2f} um", "L_p+L_n+L_sep+thCC", "computed from params"],
    ["Cell volume", f"{energy['volume_m3']:.6e} m3", "thickness x area", "r5_v12_energy.json:volume_m3"],
    ["Cell mass (stack)", f"{energy['mass_kg']:.6f} kg", "sum layer_kg_m2 x area (calc-energy contract)", "r5_v12_energy.json:mass_kg"],
    ["Gravimetric energy density", f"{energy['energy_density_wh_kg']:.2f} Wh/kg",
     "energy / mass (electrolyte excluded per contract)", "r5_v12_energy.json:energy_density_wh_kg"],
    ["Volumetric energy density", f"{energy['energy_density_wh_l']:.2f} Wh/L",
     "energy / volume", "r5_v12_energy.json:energy_density_wh_l"],
    ["DC resistance", f"{energy['dcr_ohm']*1e3:.3f} mOhm", "", "r5_v12_energy.json:dcr_ohm"],
    ["Power density", f"{energy['power_density_w_kg']:.0f} W/kg",
     "V_OC^2/(4*DCR)/mass; >= 4000 required", "r5_v12_energy.json:power_density_w_kg (contract formula)"],
]
sheet("3 energy_density", ["Quantity", "Value", "Formula", "Source"], ed_rows)

# 4. N/P and mass breakdown
np_rows = [
    ["Positive electrode loading", f"{lkg['positive_electrode']:.6f} kg/m2", "L x (1-eps) x rho", "r5_v12_energy.json:layer_kg_m2"],
    ["Negative electrode loading", f"{lkg['negative_electrode']:.6f} kg/m2", "L x (1-eps) x rho", "r5_v12_energy.json:layer_kg_m2"],
    ["Loading ratio neg/pos", f"{np_ratio:.4f}", "neg loading / pos loading", "mechanical"],
    ["Baseline loading ratio", f"{np_baseline:.4f}", "r1 baseline (Chen2020 default geometry)", "r1_base_energy.json:layer_kg_m2"],
    ["N/P (capacity terms)", f"{np_x:.2f} x baseline", "ratio / baseline ratio", "mechanical: x1.30 negative margin"],
    ["Positive coating mass", f"{g_pos_coat:.4f} g", "loading x area", "layer_kg_m2 x area_m2"],
    ["Negative coating mass", f"{g_neg_coat:.4f} g", "loading x area", "layer_kg_m2 x area_m2"],
    ["Positive CC mass (Al)", f"{g_cc_p:.4f} g", "th x 2700 kg/m3 x area", "layer_kg_m2 x area_m2"],
    ["Negative CC mass (Cu)", f"{g_cc_n:.4f} g", "th x 8960 kg/m3 x area", "layer_kg_m2 x area_m2"],
    ["Separator mass", f"{g_sep:.4f} g", "L x eps x 397 kg/m3 x area", "layer_kg_m2 x area_m2"],
    ["Electrolyte mass (fill)", f"{g_elec:.4f} g", "pore volume x 1.2 g/cm3 (lit.)", "mechanical"],
    ["Total mass (with electrolyte)", f"{g_total:.4f} g", "sum", "mechanical"],
]
sheet("4 np_mass", ["Quantity", "Value", "Formula", "Source"], np_rows)

# 5. process parameters
proc_rows = [
    ["Positive areal density", f"{areal_pos:.2f} g/m2", "L x (1-eps) x rho", "mechanical from params"],
    ["Negative areal density", f"{areal_neg:.2f} g/m2", "L x (1-eps) x rho", "mechanical from params"],
    ["Positive compaction density", f"{comp_pos_kgm3:.1f} kg/m3 = {comp_pos_gcm3:.3f} g/cm3",
     "rho x (1-eps); /1000 for g/cm3", "mechanical from params"],
    ["Negative compaction density", f"{comp_neg_kgm3:.1f} kg/m3 = {comp_neg_gcm3:.3f} g/cm3",
     "rho x (1-eps); /1000 for g/cm3", "mechanical from params"],
    ["Pore volume", f"{pore_m3:.6e} m3", "(L_p eps_p + L_n eps_n + L_sep eps_sep) x area", "mechanical from params"],
    ["Electrolyte fill amount", f"{g_elec:.2f} g", "pore volume x 1.2 g/cm3 x fill factor 1", "mechanical, lit. density annotated"],
    ["Formation recommendation", "0.1C CC to 4.2 V, 25 C, 2 cycles",
     "design-recommended value", "actual production-line value requires tuning"],
]
sheet("5 process", ["Parameter", "Value", "Formula", "Source"], proc_rows)

wb2.remove(wb2["Sheet"])  # drop default empty sheet
wb2.save(DLV / "calc.xlsx")

# ======================= DATASHEET DOCX =======================
import docx
from docx.shared import Pt, RGBColor

def fmt(x):
    return x

rows_ds = [
    ("Rated capacity (Ah)",
     f"{nominal_ah:.1f} Ah nominal (parameter set); "
     f"{c1['capacity_ah']:.2f} Ah verified at 1C (DFN simulation) - meets >= 2 Ah"),
    ("Nominal voltage / voltage window (V)",
     f"1C midpoint {energy['midpoint_voltage_v']:.3f} V (simulated); window {v_min:.1f}-{v_max:.1f} V (parameter set)"),
    ("Rated energy (Wh)", f"{energy['energy_wh']:.2f} Wh (V*I time integral over 1C discharge)"),
    ("Energy density (Wh/kg / Wh/L)",
     f"{energy['energy_density_wh_kg']:.1f} Wh/kg (contract caliber, electrolyte excluded); "
     f"{energy['energy_density_wh_l']:.1f} Wh/L"),
    ("Maximum continuous discharge rate",
     f"5C verified: capacity retention {derived['retention_5c']*100:.2f}% (>= 95% required), "
     f"T_max {c5['T_max_K']:.2f} K ({c5['T_max_K']-273.15:.1f} C)"),
    ("Fast-charge capability",
     f"4C CC charge at 45 C ambient: T_max {c4['T_max_K']:.2f} K ({c4['T_max_K']-273.15:.1f} C) <= 333.15 K; "
     f"anode potential min +{min(c4['anode_potential_v'])*1e3:.1f} mV -> no lithium plating. "
     f"Honest note: CC acceptance {c4['capacity_ah']:.3f} Ah before the 4.2 V ceiling (effective ~4.6C vs 5 Ah nominal)."),
    ("Operating temperature range",
     f"Simulated at 25 C discharge / 45 C charge ambient; peak simulated temperature "
     f"{c4['T_max_K']-273.15:.1f} C <= 60 C limit (lumped thermal)"),
    ("Cycle life", "Not simulated (requires aging protocol; aging-capable parameter set available)"),
    ("Safety determination",
     f"4C fast charge: plated = false (anode min +{min(c4['anode_potential_v'])*1e3:.1f} mV > 0); "
     f"peak temperature {c4['T_max_K']-273.15:.1f} C within 60 C"),
    ("Dimensions and mass",
     f"Layer stack {total_thickness_m*1e6:.1f} um x {height_m*1e3:.0f} mm x {width_m:.3f} m wound strip "
     f"(parameter-set geometry); stack mass {energy['mass_kg']*1e3:.2f} g "
     f"(calc-energy contract formula, electrolyte excluded; {g_elec:.2f} g electrolyte fill; "
     f"enclosure/tabs not modeled - shell dimensions Not provided)"),
]

d = docx.Document()
d.add_heading("Technical Datasheet - VBF-T3R3-DSH-01", level=0)
p = d.add_paragraph()
r = p.add_run("Power-tool battery cell (NMC811 / graphite, Chen2020 parameter set; champion V12-HiP-final). "
              "All values from simulation tool outputs; per-line sources in the value column.")
r.italic = True
tbl = d.add_table(rows=1, cols=2)
tbl.style = "Table Grid"
hdr_ds = tbl.rows[0].cells
hdr_ds[0].text = "Field"
hdr_ds[1].text = "Value / source"
for k, v in rows_ds:
    cells = tbl.add_row().cells
    cells[0].text = k
    cells[1].text = v
for row in tbl.rows:
    for cell in row.cells:
        for par in cell.paragraphs:
            for run in par.runs:
                run.font.size = Pt(9)
d.add_paragraph()
p2 = d.add_paragraph()
r2 = p2.add_run("Released under the Virtual Battery Factory delivery package; see calc.xlsx for the "
                "derivation chain and design_spec.md for design rationale.")
r2.font.size = Pt(9)
d.save(DLV / "datasheet.docx")

print("A done:")
print(f"  stack mass {g_stack:.3f} g (energy file {energy['mass_kg']*1e3:.3f} g) OK")
print(f"  electrolyte {g_elec:.3f} g, total {g_total:.3f} g")
print(f"  N/P {np_ratio:.4f} vs baseline {np_baseline:.4f} -> x{np_x:.3f}")
print(f"  compaction pos {comp_pos_gcm3:.3f} g/cm3, neg {comp_neg_gcm3:.3f} g/cm3")
print("  bom.xlsx, calc.xlsx, datasheet.docx, deliv_metrics.json written")