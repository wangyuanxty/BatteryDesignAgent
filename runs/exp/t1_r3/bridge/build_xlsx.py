# -*- coding: utf-8 -*-
"""t1_r3 — build bom.xlsx and calc.xlsx deliverables (openpyxl).

All values mechanically taken from simulation outputs / parameter set.
"""
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

OUT = Path("runs/exp/t1_r3/deliverables")

# --- mechanically fixed numbers (source: outputs read during closing) ---
ENERGY_WH = 18.622174183550765      # r5_v11_energy.json:energy_wh
MASS_KG = 0.030763443214400006      # r5_v11_energy.json:mass_kg
ED_WH_KG = 605.3345216842939        # r5_v11_energy.json:energy_density_wh_kg
ED_WH_L = 981.200981695033          # r5_v11_energy.json:energy_density_wh_l
CAP_1C = 5.084876616106298          # r5_v11_1c_spme.json:capacity_ah
CAP_4C = 0.9197                     # r5_v11_4c.json:capacity_ah (C-h)
NOMINAL = 5.085                     # r5_v11_final.json
AN_MIN = 0.0425                     # r5_v11_4c.json:anode_potential_v min
TMAX_4C = 321.2                     # r5_v11_4c.json:T_max_K
TMAX_OC = 298.57                    # r5_v11_oc.json:T_max_K
AREA = 0.1027                       # Chen2020 height x width
LAYER = {  # r5_v11_energy.json:layer_kg_m2
    "pos_elec": 0.13563396, "neg_elec": 0.081882312,
    "pos_cc": 0.027, "neg_cc": 0.05376, "sep": 0.0012703999999999999,
}
# Chen2020 + r5_v11_final.json geometry
D_POS, D_NEG, D_SEP, D_PCC, D_NCC = 75.6e-6, 85.2e-6, 8e-6, 10e-6, 6e-6
RHO_POS, RHO_NEG, RHO_SEP, RHO_AL, RHO_CU = 3262.0, 1657.0, 397.0, 2700.0, 8960.0
EPS_POS, EPS_NEG, EPS_SEP = 0.45, 0.42, 0.60
CMAX_POS, CMAX_NEG = 63104.0, 33133.0   # pybamm Chen2020 set (read mechanically)
F = 96485.0
RHO_ELEC = 1.2  # g/cm3, literature value, annotated

pore_m3 = AREA * (D_POS * EPS_POS + D_NEG * EPS_NEG + D_SEP * EPS_SEP)
elec_g = pore_m3 * 1e6 * RHO_ELEC  # cm3 * g/cm3

rows_bom = [
    ("Component", "Mass (g/cell)", "kg/kWh", "Formula", "Source"),
    ("Positive active material", 13.9296, 13.9296 / ENERGY_WH,
     "d_pos*(1-e_pos)*rho_pos*A = 75.6um*0.55*3262*0.1027",
     "r5_v11_energy.json:layer_kg_m2 x area"),
    ("Positive conductive additive (2 wt% of active, literature default)", 0.2786, 0.2786 / ENERGY_WH,
     "13.9296 g x 0.02", "literature default, annotated"),
    ("Positive binder (2 wt% PVDF, literature default)", 0.2786, 0.2786 / ENERGY_WH,
     "13.9296 g x 0.02", "literature default, annotated"),
    ("Negative active material", 8.4093, 8.4093 / ENERGY_WH,
     "d_neg*(1-e_neg)*rho_neg*A = 85.2um*0.58*1657*0.1027",
     "r5_v11_energy.json:layer_kg_m2 x area"),
    ("Negative conductive additive (1 wt% of active, literature default)", 0.0841, 0.0841 / ENERGY_WH,
     "8.4093 g x 0.01", "literature default, annotated"),
    ("Negative binder (2 wt% CMC/SBR, literature default)", 0.1682, 0.1682 / ENERGY_WH,
     "8.4093 g x 0.02", "literature default, annotated"),
    ("Separator", 0.1305, 0.1305 / ENERGY_WH,
     "d_sep*(1-e_sep)*rho_sep*A = 8um*0.4*397*0.1027",
     "r5_v11_energy.json:layer_kg_m2.separator x area"),
    ("Electrolyte (1.2 g/cm3 literature density, fill factor 1.0)", 9.1944, 9.1944 / ENERGY_WH,
     "pore volume x 1.2 = 7.662 cm3 x 1.2",
     "pore volume from geometry; density literature value"),
    ("Positive current collector (Al 10 um)", 2.7729, 2.7729 / ENERGY_WH,
     "10um x 2700 x 0.1027", "r5_v11_energy.json:layer_kg_m2.positive_cc x area"),
    ("Negative current collector (Cu 6 um)", 5.5212, 5.5212 / ENERGY_WH,
     "6um x 8960 x 0.1027", "r5_v11_energy.json:layer_kg_m2.negative_cc x area"),
    ("Enclosure", "Not modeled", "Not modeled", "—", "honest omission"),
    ("Tabs", "Not modeled", "Not modeled", "—", "honest omission"),
    ("TOTAL (contract caliber, electrolyte excluded)", 30.7634, 30.7634 / ENERGY_WH,
     "sum of layer masses", "r5_v11_energy.json:mass_kg"),
    ("TOTAL incl. electrolyte + additives/binders", 40.7666, 40.7666 / ENERGY_WH,
     "sum of all rows above", "mechanical sum"),
    ("Cell energy (reference)", f"{ENERGY_WH:.4f} Wh", "—", "V*I integral, 1C",
     "r5_v11_energy.json:energy_wh"),
]

rows_calc_inputs = [
    ("Parameter", "Value", "Unit", "Source"),
    ("Positive electrode thickness", 75.6e-6, "m", "Chen2020 (unchanged)"),
    ("Negative electrode thickness", 85.2e-6, "m", "Chen2020 (unchanged)"),
    ("Positive electrode porosity", 0.45, "—", "r5_v11_final.json"),
    ("Negative electrode porosity", 0.42, "—", "r5_v11_final.json"),
    ("Separator thickness / porosity", "8e-6 / 0.60", "m / —", "r5_v11_final.json"),
    ("Positive / negative particle radius", "0.8e-6 / 0.8e-6", "m", "r5_v11_final.json"),
    ("Electrolyte conductivity", 1.8, "S/m", "r5_v11_final.json (constant, replaces Nyman2008 fn)"),
    ("Electrolyte diffusivity", 6.0e-10, "m2/s", "r5_v11_final.json"),
    ("Cation transference number", 0.55, "—", "r5_v11_final.json"),
    ("Current collectors Al / Cu", "10e-6 / 6e-6", "m", "r5_v11_final.json"),
    ("Total heat transfer coefficient", 120.0, "W/m2/K", "r5_v11_final.json"),
    ("Nominal cell capacity", 5.085, "Ah", "r5_v11_final.json (R5: = measured 1C cap)"),
    ("Electrode area (height x width)", 0.1027, "m2", "Chen2020: 0.065 x 1.58"),
    ("Voltage window", "2.5 - 4.2", "V", "Chen2020"),
    ("Positive max concentration", 63104.0, "mol/m3", "pybamm Chen2020"),
    ("Negative max concentration", 33133.0, "mol/m3", "pybamm Chen2020"),
]

rows_calc_ce = [
    ("Quantity", "Value", "Unit", "Formula", "Source"),
    ("1C discharge capacity", CAP_1C, "Ah", "CC 5.085 A to 2.5 V event", "r5_v11_1c_spme.json:capacity_ah"),
    ("4C charge accepted", f"{CAP_4C} C-h x {NOMINAL} = {CAP_4C*NOMINAL:.4f}", "Ah",
     "charge capacity_ah = duration x C/3600; true Ah = reported x nominal",
     "r5_v11_4c.json:capacity_ah"),
    ("4C acceptance fraction", f"{CAP_4C*NOMINAL/CAP_1C*100:.1f}", "% of 1C capacity",
     "accepted / 1C capacity", "mechanical derivation"),
    ("Discharge energy (1C)", ENERGY_WH, "Wh", "integral V*I dt", "r5_v11_energy.json:energy_wh"),
    ("Midpoint voltage", 4.1299, "V", "energy / capacity", "r5_v11_energy.json:midpoint_voltage_v"),
]

rows_calc_ed = [
    ("Quantity", "Value", "Unit", "Formula", "Source"),
    ("Energy density (mass)", ED_WH_KG, "Wh/kg", "18.6222 Wh / 0.0307634 kg", "r5_v11_energy.json"),
    ("Energy density (volume)", ED_WH_L, "Wh/L", "18.6222 Wh / 1.8979e-5 m3", "r5_v11_energy.json"),
    ("Criterion", ">= 392.61", "Wh/kg", "entry 0 stage2", "log.jsonl entry 0"),
    ("Verdict", "PASS (605.33 >= 392.61)", "—", "mechanical compare", "log-evaluate R5"),
]

rows_calc_np = [
    ("Layer", "Mass (g)", "Formula", "Source"),
    ("Positive electrode", 13.9296, "75.6um*0.55*3262*0.1027", "r5_v11_energy.json:layer_kg_m2"),
    ("Negative electrode", 8.4093, "85.2um*0.58*1657*0.1027", "r5_v11_energy.json:layer_kg_m2"),
    ("Positive CC (Al)", 2.7729, "10um*2700*0.1027", "r5_v11_energy.json:layer_kg_m2"),
    ("Negative CC (Cu)", 5.5212, "6um*8960*0.1027", "r5_v11_energy.json:layer_kg_m2"),
    ("Separator", 0.1305, "8um*0.4*397*0.1027", "r5_v11_energy.json:layer_kg_m2"),
    ("Total", 30.7634, "sum", "r5_v11_energy.json:mass_kg"),
    ("Geometric N/P", 0.624, "(0.58*33133*85.2um)/(0.55*63104*75.6um)",
     "parameter-set keys; caveat: Chen2020 neg OCP saturates above stoich 0.90 -> practical N/P verified by plating-free 4C sim instead"),
]

rows_calc_proc = [
    ("Parameter", "Value", "Unit", "Formula", "Source"),
    ("Positive areal density", 135.63, "g/m2", "75.6um x 0.55 x 3262", "layer_kg_m2 x 1000"),
    ("Negative areal density", 81.88, "g/m2", "85.2um x 0.58 x 1657", "layer_kg_m2 x 1000"),
    ("Positive compaction density", 1.79, "g/cm3", "3262 x 0.55 / 1000", "derived (note: /1000)"),
    ("Negative compaction density", 0.96, "g/cm3", "1657 x 0.58 / 1000", "derived (note: /1000)"),
    ("Electrolyte fill amount", 9.19, "g", "7.662 cm3 x 1.2 g/cm3 x 1.0 fill", "literature density 1.2, annotated"),
    ("Formation recommendation", "0.1C CC to 4.2V, 25C, 2 cycles", "—",
     "design recommended value; production tuning required", "annotated"),
]


def _write_sheet(wb, title, rows, widths):
    ws = wb.create_sheet(title)
    for r_i, row in enumerate(rows, start=1):
        for c_i, val in enumerate(row, start=1):
            cell = ws.cell(row=r_i, column=c_i, value=val)
            if r_i == 1:
                cell.font = Font(bold=True)
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


wb = openpyxl.Workbook()
wb.remove(wb.active)
_write_sheet(wb, "BOM", rows_bom, [58, 14, 10, 46, 40])
wb.save(OUT / "bom.xlsx")

wb2 = openpyxl.Workbook()
wb2.remove(wb2.active)
_write_sheet(wb2, "Inputs", rows_calc_inputs, [46, 18, 12, 46])
_write_sheet(wb2, "CapacityEnergy", rows_calc_ce, [30, 26, 16, 40, 40])
_write_sheet(wb2, "EnergyDensity", rows_calc_ed, [30, 26, 16, 40, 40])
_write_sheet(wb2, "NP_Mass", rows_calc_np, [30, 14, 42, 60])
_write_sheet(wb2, "Process", rows_calc_proc, [34, 26, 10, 42, 46])
wb2.save(OUT / "calc.xlsx")
print("bom.xlsx + calc.xlsx written")
