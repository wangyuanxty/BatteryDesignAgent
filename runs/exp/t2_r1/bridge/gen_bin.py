"""Generate binary deliverables: bom.xlsx, calc.xlsx, datasheet.docx.

All values mechanically derived from Chen2020 parameter-set dump + simulation outputs
(r6_d3_*). Literature defaults annotated. No values from memory.
"""
from pathlib import Path

import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Pt

DEL = Path("runs/exp/t2_r1/deliverables")

# ---- shared mechanical values (sources annotated in the sheets themselves) ----
AREA = 0.1027            # Electrode height 0.065 x width 1.58 m (Chen2020 dump)
TH_POS, TH_NEG, TH_SEP = 75.6e-6, 85.2e-6, 12e-6
TH_PCC, TH_NCC = 16e-6, 12e-6
RHO_POS, RHO_NEG, RHO_SEP = 3262.0, 1657.0, 397.0
RHO_PCC, RHO_NCC = 2700.0, 8960.0
POR_POS, POR_NEG, POR_SEP = 0.40, 0.40, 0.47       # final design porosities (r6_d3)
AF_POS, AF_NEG = 0.665, 0.75                        # parameter-set active volume fractions
ENERGY_WH = 18.454205458102855                      # r6_d3_energy.json:energy_wh
MASS_CONTRACT_KG = 0.039633478716                   # r6_d3_energy.json:mass_kg
VOL_M3 = 2.0622160000000005e-05                     # r6_d3_energy.json:volume_m3
ED_WHKG = 465.62164250933915                        # r6_d3_energy.json
ED_WHL = 894.8725767864692                          # r6_d3_energy.json
CAP_1C = 5.066256277024658                          # r6_d3_1c.json:capacity_ah
C_MAX_N, C_MAX_P = 33133.0, 63104.0                 # Chen2020 dump
X0_N, X0_P = 29866.0 / C_MAX_N, 17038.0 / C_MAX_P   # initial stoichs (Chen2020 dump)
ELYT_DENS_G_CM3 = 1.2                               # literature value (annotated)

# ---- BOM ----
def bom_rows():
    m_pos_active = TH_POS * AREA * AF_POS * RHO_POS
    m_neg_active = TH_NEG * AREA * AF_NEG * RHO_NEG
    m_sep = TH_SEP * AREA * (1 - POR_SEP) * RHO_SEP
    m_pcc = TH_PCC * AREA * RHO_PCC
    m_ncc = TH_NCC * AREA * RHO_NCC
    pore_m3 = (TH_POS * POR_POS + TH_NEG * POR_NEG + TH_SEP * POR_SEP) * AREA
    m_elyte = pore_m3 * 1e6 * ELYT_DENS_G_CM3  # cm3 * g/cm3 = g
    # literature-default additive/binder (annotated): NMC811 92:4:4 wt, graphite 96:2:2 wt
    m_pos_cb = m_pos_active * 4 / 92
    m_pos_bd = m_pos_active * 4 / 92
    m_neg_cb = m_neg_active * 2 / 96
    m_neg_bd = m_neg_active * 2 / 96
    rows = [
        ("Positive electrode active material (NMC811)", "0.665 (param set)", m_pos_active,
         "th 75.6um x area 0.1027m2 x vf 0.665 x rho 3262 (Chen2020 dump)"),
        ("Positive electrode conductive additive (CB)", "4 wt% of active (lit. default, NMC811 92:4:4)", m_pos_cb,
         "literature default, annotated"),
        ("Positive electrode binder (PVDF)", "4 wt% of active (lit. default)", m_pos_bd,
         "literature default, annotated"),
        ("Negative electrode active material (graphite)", "0.75 (param set)", m_neg_active,
         "th 85.2um x area x vf 0.75 x rho 1657 (Chen2020 dump)"),
        ("Negative electrode conductive additive (CB)", "2 wt% of active (lit. default, graphite 96:2:2)", m_neg_cb,
         "literature default, annotated"),
        ("Negative electrode binder (CMC/SBR)", "2 wt% of active (lit. default)", m_neg_bd,
         "literature default, annotated"),
        ("Separator", "porosity 0.47", m_sep,
         "th 12um x area x (1-0.47) x rho 397 (Chen2020 dump)"),
        ("Electrolyte", "pore volume x 1.2 g/cm3 (lit. density)", m_elyte,
         f"pore volume {(pore_m3*1e6):.3f} cm3 x 1.2 g/cm3; fill factor 100%"),
        ("Positive current collector (Al)", "-", m_pcc,
         "th 16um x area x rho 2700 (Chen2020 dump)"),
        ("Negative current collector (Cu)", "-", m_ncc,
         "th 12um x area x rho 8960 (Chen2020 dump)"),
        ("Enclosure", "Not modeled", None, "beyond simulation boundary"),
        ("Tabs", "Not modeled", None, "beyond simulation boundary"),
    ]
    return rows, m_elyte

def write_bom():
    rows, m_elyte = bom_rows()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "BOM"
    ws.append(["Component", "Volume fraction / basis", "Mass g/cell", "kg/kWh", "Source / formula"])
    total_g = 0.0
    for name, vf, mass, src in rows:
        if mass is None:
            ws.append([name, vf, "Not modeled", "", src])
            continue
        total_g += mass
        ws.append([name, vf, round(mass, 4), round(mass / 1000.0 / (ENERGY_WH / 1000.0), 4), src])
    ws.append(["TOTAL (BOM caliber: incl. lit-default additive/binder + electrolyte)",
               "", round(total_g, 3), round(total_g / 1000.0 / (ENERGY_WH / 1000.0), 4),
               f"sum of rows; total energy {ENERGY_WH:.4f} Wh"])
    ws.append(["TOTAL cell mass (contract caliber: layers only, electrolyte/binder/additive excluded)",
               "", round(MASS_CONTRACT_KG * 1000.0, 3), round(MASS_CONTRACT_KG / (ENERGY_WH / 1000.0), 4),
               "cell/r6_d3_energy.json:mass_kg"])
    for col, w in zip("ABCDE", (48, 34, 14, 12, 60)):
        ws.column_dimensions[col].width = w
    wb.save(DEL / "bom.xlsx")
    print("bom.xlsx written")

# ---- CALC ----
def write_calc():
    wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = "input_parameters"
    ws.append(["Parameter", "Base (Chen2020)", "Final (GridStore-D3)", "Source"])
    for row in [
        ("Nominal cell capacity [A.h]", 5.0, 5.0, "Chen2020 dump"),
        ("Electrode height [m]", 0.065, 0.065, "Chen2020 dump"),
        ("Electrode width [m]", 1.58, 1.58, "Chen2020 dump"),
        ("Positive electrode thickness [m]", 7.56e-05, 7.56e-05, "Chen2020 dump"),
        ("Negative electrode thickness [m]", 8.52e-05, 8.52e-05, "Chen2020 dump"),
        ("Positive electrode porosity", 0.335, 0.40, "r6_d3_params.json"),
        ("Negative electrode porosity", 0.25, 0.40, "r6_d3_params.json"),
        ("Positive particle radius [m]", 5.22e-06, 2.5e-06, "r6_d3_params.json"),
        ("Negative particle radius [m]", 5.86e-06, 2.0e-06, "r6_d3_params.json"),
        ("Electrolyte conductivity [S.m-1]", "Nyman2008 f(T)", 3.0, "r6_d3_params.json (constant override)"),
        ("Electrolyte diffusivity [m2.s-1]", "Nyman2008 f(T)", 2.5e-09, "r6_d3_params.json (constant override)"),
        ("Cation transference number", 0.2594, 0.35, "r6_d3_params.json"),
        ("SEI kinetic rate constant [m.s-1]", 1e-12, 1e-16, "r6_d3_params.json (coating bridge)"),
        ("Positive electrode density [kg.m-3]", 3262.0, 3262.0, "Chen2020 dump"),
        ("Negative electrode density [kg.m-3]", 1657.0, 1657.0, "Chen2020 dump"),
        ("Upper voltage cut-off [V]", 4.2, 4.2, "Chen2020 dump"),
        ("Lower voltage cut-off [V]", 2.5, 2.5, "Chen2020 dump"),
    ]:
        ws.append(list(row))
    for col, w in zip("ABCD", (42, 20, 22, 34)):
        ws.column_dimensions[col].width = w

    ws = wb.create_sheet("capacity_and_energy")
    ws.append(["Item", "Formula", "Value", "Source"])
    ws.append(["1C discharge capacity [Ah]", "run-pyamm 1C_discharge", CAP_1C, "cell/r6_d3_1c.json:capacity_ah"])
    ws.append(["Discharge energy [Wh]", "trapezoid integral of voltage_v x I_1C over time_s; I_1C = nominal 5.0 A",
               ENERGY_WH, "cell/r6_d3_energy.json:energy_wh"])
    for col, w in zip("ABCD", (34, 60, 16, 40)):
        ws.column_dimensions[col].width = w

    ws = wb.create_sheet("energy_density")
    ws.append(["Item", "Formula", "Value", "Source"])
    ws.append(["Gravimetric ED [Wh/kg]", f"energy / mass = {ENERGY_WH:.4f} Wh / {MASS_CONTRACT_KG:.6f} kg", ED_WHKG,
               "cell/r6_d3_energy.json:energy_density_wh_kg"])
    ws.append(["Volumetric ED [Wh/L]", f"energy / volume = {ENERGY_WH:.4f} Wh / {VOL_M3:.6e} m3 x 1e-3", ED_WHL,
               "cell/r6_d3_energy.json:energy_density_wh_l"])
    ws.append(["Mass [kg]", "sum over layers: thickness x (1-porosity) x density x area (electrolyte excluded)", MASS_CONTRACT_KG,
               "cell/r6_d3_energy.json:mass_kg"])
    ws.append(["Criterion check", "465.62 >= 327.18", "PASS", "entry-0 criteria.stage2.energy_density_wh_kg"])
    for col, w in zip("ABCD", (30, 66, 14, 44)):
        ws.column_dimensions[col].width = w

    ws = wb.create_sheet("np_and_mass")
    ws.append(["Item", "Formula", "Value", "Source"])
    ws.append(["N/P ratio",
               f"(c_max_n x x0_n x th_n)/(c_max_p x x0_p x th_p) = ({C_MAX_N:.0f}x{X0_N:.4f}x85.2um)/({C_MAX_P:.0f}x{X0_P:.4f}x75.6um)",
               round((C_MAX_N * X0_N * TH_NEG) / (C_MAX_P * X0_P * TH_POS), 4),
               "Chen2020 dump; initial-lithium-content caliber (set defines initial concentrations, not x0/x100 windows)"])
    layer_rows = [
        ("Positive electrode", TH_POS, 1 - POR_POS, RHO_POS, 0.147964),
        ("Negative electrode", TH_NEG, 1 - POR_NEG, RHO_NEG, 0.084706),
        ("Positive current collector", TH_PCC, 1.0, RHO_PCC, 0.043200),
        ("Negative current collector", TH_NCC, 1.0, RHO_NCC, 0.107520),
        ("Separator", TH_SEP, 1 - POR_SEP, RHO_SEP, 0.002525),
    ]
    ws.append([])
    ws.append(["Layer", "thickness m", "(1-por)", "density kg/m3", "layer kg/m2"])
    for name, th, fpor, rho, lkg in layer_rows:
        ws.append([name, th, round(fpor, 4), rho, lkg])
    ws.append(["TOTAL kg/m2", "", "", "", sum(r[4] for r in layer_rows)])
    ws.append(["TOTAL mass g (x area 0.1027 m2)", "", "", "", MASS_CONTRACT_KG * 1000.0])
    for col, w in zip("ABCDE", (34, 66, 14, 16, 14)):
        ws.column_dimensions[col].width = w

    ws = wb.create_sheet("process_parameters")
    ws.append(["Parameter", "Formula", "Value", "Unit", "Source"])
    ws.append(["Positive areal density", "th 75.6um x (1-0.40) x 3262", round(TH_POS * (1 - POR_POS) * RHO_POS, 2), "g/m2",
               "calc-energy layer_kg_m2"])
    ws.append(["Negative areal density", "th 85.2um x (1-0.40) x 1657", round(TH_NEG * (1 - POR_NEG) * RHO_NEG, 2), "g/m2",
               "calc-energy layer_kg_m2"])
    ws.append(["Positive compaction density", "3262 x (1-0.40) / 1000", round(RHO_POS * (1 - POR_POS) / 1000.0, 3), "g/cm3",
               "design-spec process formula (divide by 1000)"])
    ws.append(["Negative compaction density", "1657 x (1-0.40) / 1000", round(RHO_NEG * (1 - POR_NEG) / 1000.0, 3), "g/cm3",
               "design-spec process formula"])
    pore_cm3 = (TH_POS * POR_POS + TH_NEG * POR_NEG + TH_SEP * POR_SEP) * AREA * 1e6
    ws.append(["Electrolyte fill amount", f"pore volume {pore_cm3:.3f} cm3 x 1.2 g/cm3 x 100%", round(pore_cm3 * 1.2, 3), "g",
               "electrolyte density 1.2 g/cm3 = literature value (annotated)"])
    ws.append(["Formation recommendation", "0.1C CC to 4.2V, 25C, 2 cycles", "", "",
               "design-recommended value; production-line value requires tuning (annotated)"])
    for col, w in zip("ABCDE", (32, 46, 14, 10, 48)):
        ws.column_dimensions[col].width = w

    wb.save(DEL / "calc.xlsx")
    print("calc.xlsx written")

# ---- DATASHEET (docx) ----
def write_datasheet():
    doc = Document()
    h = doc.add_heading("Technical Datasheet — GridStore-D3", level=1)
    doc.add_paragraph("Number: VBF-T2R1-DSH-01    Case: t2_r1 (grid energy storage)    Date: 2026-08-25")
    doc.add_paragraph("All values mechanically taken from simulation outputs / parameter set; sources per row.")
    rows = [
        ("Rated capacity (Ah)", "5.0 nominal (parameter set); 5.066 simulated 1C discharge",
         "Chen2020 dump; cell/r6_d3_1c.json:capacity_ah"),
        ("Nominal voltage / voltage window (V)", "2.5 – 4.2 V; discharge plateau proxy 3.722 V at fixed t = 1800 s of 1C",
         "Chen2020 dump; r6_d3_1c.json (calc-energy 'midpoint' scalar is a solver-step-density index artifact — see design_spec §6)"),
        ("Rated energy (Wh)", "18.454 (time integration of V·I at 1C)",
         "cell/r6_d3_energy.json:energy_wh"),
        ("Energy density", "465.62 Wh/kg (contract caliber, electrolyte excluded); 894.87 Wh/L",
         "cell/r6_d3_energy.json:energy_density_wh_kg / _wh_l"),
        ("Maximum continuous discharge rate", "1C (5.066 A) simulated; higher rates not in task contract (5C protocol not run)",
         "cell/r6_d3_1c.json"),
        ("Fast-charge capability", "4C charge @ 45 °C: plating-free (anode potential min +0.0498 V), acceptance 0.838 Ah to 4.2 V, T_max 342.39 K (+24.2 K above ambient)",
         "cell/r6_d3_4c.json:anode_potential_v / capacity_ah / T_max_K"),
        ("Operating temperature range", "Verified −20 °C (253.15 K) to +45 °C (318.15 K) per simulation conditions; −20 °C discharge retention 99.571% (protocol and true-soak, cell temp 266.7 K)",
         "cell/r6_d3_lowT_ret.json; cell/r6_d3_lowT_soak.json"),
        ("Cycle life", "Aging protocol (1C CC 2.5–4.2 V, SEI ec-reaction-limited, isothermal): SEI thickness 9.087 nm after 100 cycles, 25.317 nm after 500 cycles (contract limits 500/550 nm); capacity trajectory flat. Honest annotation: the reported per-cycle capacity variable is a PyBaMM artifact (freezes at first-discharge value); probe confirms real steps are full 1C swings (5.08 Ah discharge / 4.75 Ah charge per cycle)",
         "cell/r6_d3_aging100.json / r6_d3_aging500.json; bridge/probe_aging.py"),
        ("Safety determination", "4C fast charge plating-free; T_max 342.39 K during 4C charge (no contract red line); abuse scenarios (nail / overcharge / crush) not simulated — N/A (beyond pure simulation boundary)",
         "cell/r6_d3_4c.json"),
        ("Dimensions and mass", "1580 × 65 × 0.2008 mm (W × H × T, layer stack); 39.63 g contract caliber (electrolyte excluded); shell/casing Not provided",
         "Chen2020 dump; cell/r6_d3_energy.json:mass_kg / thickness_m"),
    ]
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    for j, txt in enumerate(("Field", "Value", "Source")):
        table.rows[0].cells[j].text = txt
    for field, val, src in rows:
        cells = table.add_row().cells
        cells[0].text = field
        cells[1].text = val
        cells[2].text = src
    doc.save(DEL / "datasheet.docx")
    print("datasheet.docx written")

if __name__ == "__main__":
    DEL.mkdir(parents=True, exist_ok=True)
    write_bom()
    write_calc()
    write_datasheet()
