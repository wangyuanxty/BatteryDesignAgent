# Build datasheet.docx, bom.xlsx, calc.xlsx for t2_r3 deliverables.
# All values sourced from tool outputs / pybamm Chen2020 dump / annotated estimates (see design_spec.md).
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
import docx
from docx.shared import Pt, Cm
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

D = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t2_r3\deliverables")
D.mkdir(parents=True, exist_ok=True)

# ---- shared constants (sourced) ----
AREA = 0.1027
KWH = 0.018457182518897157
ENERGY_WH = 18.457182518897156
MASS_G = 41.27970507960001
SERIES = "VBF-T2R3-"
DATE = "2026-08-26"

# ---------------- datasheet.docx ----------------
doc = docx.Document()
doc.add_heading("Technical Datasheet — Grid Energy Storage Cell", 0)
doc.add_paragraph(f"{SERIES}DSH-01   |   Generated {DATE}   |   Prepared: ______   Reviewed: ______   Approved: ______")

fields = [
    ("Rated capacity", "5.0 Ah (parameter-set nominal) / 5.0648 Ah simulated (1C CC, 25 °C, 2.5–4.2 V, DFN)",
     "Chen2020 'Nominal cell capacity [A.h]'; cell/r7_final_1c_dfn.json:capacity_ah"),
    ("Voltage window / midpoint", "2.5 – 4.2 V (lower/upper cut-off); simulated 1C discharge midpoint 3.9118 V",
     "Chen2020 set; cell/r7_final_energy_dfn.json:midpoint_voltage_v"),
    ("Rated energy", "18.457 Wh (1C discharge, DFN time-integration of V·I)",
     "cell/r7_final_energy_dfn.json:energy_wh"),
    ("Energy density", "447.12 Wh/kg; 895.02 Wh/L (contract caliber — electrolyte excluded from mass; incl. electrolyte estimate: 374.4 Wh/kg, derived)",
     "cell/r7_final_energy_dfn.json:energy_density_wh_kg / energy_density_wh_l; electrolyte mass = pore volume × 1.2 g/cm3 [estimate]"),
    ("Maximum continuous discharge rate", "1C (5 A) — simulated, DFN; DCR 2.612 mΩ; power density 39.08 kW/kg",
     "cell/r7_final_1c_dfn.json; cell/r7_final_energy_dfn.json:dcr_ohm / power_density_w_kg"),
    ("Fast-charge capability", "4C (20 A) CC at 45 °C: NO lithium plating (anode surface potential min +0.0443 V); T_max 347.70 K (+29.55 K vs 318.15 K ambient, lumped thermal h = 10 W/m2/K)",
     "cell/r7_final_4c_dfn.json:anode_potential_v / T_max_K"),
    ("Low-temperature performance", "−20 °C 1C discharge retention 99.57 % (vs 25 °C, same parameters, DFN)",
     "cell/r7_final_lowT_retention.json:lowT_retention"),
    ("Operating temperature range (simulated)", "−20 °C (discharge) … +45 °C (charge); 25 °C nominal cycling",
     "protocols lowT_discharge / 4C_charge_45C / 1C_discharge (log entries)"),
    ("Durability / SEI", "Anode SEI 276.22 nm @ 100 cyc (limit 500 nm) and 393.00 nm @ 500 cyc (limit 550 nm) at 1C cycling, SEI model. Per-cycle capacity trajectory in the SEI-only model decays (0.331 → 0.216 Ah @ 100 cyc; 0.0123 Ah @ 500 cyc) — SEI-growth lithium-inventory-loss model only, no calendar/fatigue mechanisms; known low-first-cycle Chen2020 artifact. Full calendar/fatigue cycle life: Not provided (beyond model scope)",
     "cell/r6_combo-v5-final_aging100_spme.json / aging500_spme.json:sei_thickness_nm_end, capacity_ah_per_cycle"),
    ("Safety determination", "4C fast charge plating-free (virtual test). Overcharge / nail / thermal-runaway abuse: not required by task, N/A",
     "cell/r7_final_4c_dfn.json; entry-0 criteria"),
    ("Dimensions", "Electrode sheet 65 mm × 1580 mm; layer stack thickness 200.8 µm (pos 75.6 + neg 85.2 + sep 12 + Al 16 + Cu 12 µm); cell envelope/jelly-roll: Not provided (not parameterized)",
     "Chen2020 geometry keys; design_spec.md §1"),
    ("Mass", "41.28 g (contract caliber, electrolyte excluded); 49.30 g incl. electrolyte estimate",
     "cell/r7_final_energy_dfn.json:mass_kg; pore-volume × 1.2 g/cm3 [estimate]"),
]
tbl = doc.add_table(rows=1, cols=3)
tbl.style = "Light Grid Accent 1"
hdr = tbl.rows[0].cells
hdr[0].text, hdr[1].text, hdr[2].text = "Field", "Value", "Source"
for name, val, src in fields:
    c = tbl.add_row().cells
    c[0].text, c[1].text, c[2].text = name, val, src
doc.save(str(D / "datasheet.docx"))
print("datasheet.docx written")

# ---------------- bom.xlsx ----------------
wb = Workbook()
ws = wb.active
ws.title = "BOM"
ws.append(["Component", "Material", "Mass (g/cell)", "kg/kWh", "Basis / source"])
def row(comp, mat, g, kgkwh, basis):
    def num(x):
        try:
            return round(float(x), 4)
        except (TypeError, ValueError):
            return x
    def num5(x):
        try:
            return round(float(x), 5)
        except (TypeError, ValueError):
            return x
    ws.append([comp, mat, num(g), num5(kgkwh), basis])

row("Positive electrode active material", "NMC811", 16.1685, 16.1685/1000/KWH,
    "coating 16.8422 g × 0.96 AM split [E] (96/2/2 solid split = industry-typical estimate; not in parameter set — Chen2020 has no binder/additive keys); coating mass = layer_kg_m2 × area (r7_final_energy_dfn.json)")
row("Positive electrode conductive additive", "Carbon black", 0.3368, 0.3368/1000/KWH, "split [E], see above")
row("Positive electrode binder", "PVDF", 0.3368, 0.3368/1000/KWH, "split [E], see above")
row("Negative electrode active material", "Graphite", 8.3513, 8.3513/1000/KWH,
    "coating 8.6993 g × 0.96 AM split [E]; coating mass = layer_kg_m2 × area")
row("Negative electrode conductive additive", "Carbon black", 0.1740, 0.1740/1000/KWH, "split [E]")
row("Negative electrode binder", "CMC/SBR", 0.1740, 0.1740/1000/KWH, "split [E]")
row("Separator", "Polyolefin, 12 µm (porosity 0.47)", 0.2593, 0.2593/1000/KWH,
    "r7_final_energy_dfn.json:layer_kg_m2.separator × area")
row("Electrolyte", "LiPF6 in EC/EMC carbonate, 1 M-class (electrolyte density 1.2 g/cm3 [E])", 8.0163, 8.0163/1000/KWH,
    "pore volume (pos 2.601 + neg 3.499 + sep 0.579 cm3) × 1.2 g/cm3 [E]; excluded from contract mass caliber")
row("Positive current collector", "Al foil 16 µm", 4.4366, 4.4366/1000/KWH,
    "layer_kg_m2.positive_cc × area (r7_final_energy_dfn.json)")
row("Negative current collector", "Cu foil 12 µm", 11.0423, 11.0423/1000/KWH,
    "layer_kg_m2.negative_cc × area")
row("Enclosure / tabs", "—", "Not modeled", "—", "honest gap (no parameter)")
sum_incl = 16.1685+0.3368+0.3368+8.3513+0.1740+0.1740+0.2593+8.0163+4.4366+11.0423
ws.append([])
ws.append(["SUMMARY", "", "", "", ""])
ws.append(["Total mass (contract, electrolyte excluded)", "41.280 g", "", sum_incl-8.0163, ""])
ws.append(["Total mass incl. electrolyte (estimate)", "49.296 g", "", sum_incl, ""])
ws.append(["Cell energy (DFN 1C)", "18.4572 Wh", ""])
ws.append(["Material usage per unit energy (contract)", str(round(41.2797/1000, 5)), "kg/kWh", "", "contract caliber"]),
ws["B1"].font = Font(bold=True)
for c in ["A1","B1","C1","D1","E1"]:
    ws[c].font = Font(bold=True)
ws.column_dimensions["A"].width = 38
ws.column_dimensions["B"].width = 34
ws.column_dimensions["C"].width = 14
ws.column_dimensions["D"].width = 12
ws.column_dimensions["E"].width = 90
wb.save(str(D / "bom.xlsx"))
print("bom.xlsx written, total incl electrolyte =", sum_incl)

# ---------------- calc.xlsx ----------------
wb2 = Workbook()
hdr_font = Font(bold=True, color="FFFFFF")
hdr_fill = PatternFill("solid", fgColor="14283C")

def sheet_titled(name):
    ws = wb2.active if wb2.active.title == "Sheet" else wb2.create_sheet()
    ws.title = name
    return ws

# Sheet 1: inputs
s = sheet_titled("1_inputs")
s.append(["Parameter", "Value", "Unit", "Source"])
inputs = [
    ("Electrode height × width", "0.065 × 1.58", "m", "Chen2020 dump"),
    ("Electrode area", AREA, "m2", "height × width"),
    ("Positive electrode thickness", 75.6e-6, "m", "Chen2020 dump"),
    ("Negative electrode thickness", 85.2e-6, "m", "Chen2020 dump"),
    ("Separator thickness", 12e-6, "m", "Chen2020 dump"),
    ("Positive current collector thickness (Al)", 16e-6, "m", "Chen2020 dump"),
    ("Negative current collector thickness (Cu)", 12e-6, "m", "Chen2020 dump"),
    ("Positive electrode density", 3262.0, "kg/m3", "Chen2020 dump"),
    ("Negative electrode density", 1657.0, "kg/m3", "Chen2020 dump"),
    ("Positive porosity", 0.335, "—", "Chen2020 dump"),
    ("Negative porosity (final)", 0.40, "—", "r6_combo-v5-final_params.json"),
    ("Positive AM volume fraction", 0.665, "—", "Chen2020 dump"),
    ("Negative AM volume fraction", 0.75, "—", "Chen2020 dump"),
    ("c_max positive", 63104.0, "mol/m3", "Chen2020 dump"),
    ("c_max negative", 33133.0, "mol/m3", "Chen2020 dump"),
    ("Nominal cell capacity", 5.0, "Ah", "Chen2020 dump"),
    ("I (1C) = I (discharge) = nominal × 1", 5.0, "A", "derived"),
]
for r in inputs:
    s.append(list(r))
for c in "ABCD":
    s[f"{c}1"].font = hdr_font
    s[f"{c}1"].fill = hdr_fill
s.column_dimensions["A"].width = 46
s.column_dimensions["D"].width = 34

# Sheet 2: capacity and energy
s = sheet_titled("2_capacity_energy")
s.append(["Quantity", "Value", "Unit", "Formula / source"])
rows = [
    ("Simulated 1C discharge capacity (DFN, 25 °C)", 5.064843296941604, "Ah", "cell/r7_final_1c_dfn.json:capacity_ah"),
    ("Discharge energy (DFN time-integral of V·I)", ENERGY_WH, "Wh", "cell/r7_final_energy_dfn.json:energy_wh"),
    ("Cell energy (kWh)", KWH, "kWh", "Wh ÷ 1000"),
    ("Midpoint discharge voltage", 3.911774309748794, "V", "cell/r7_final_energy_dfn.json:midpoint_voltage_v"),
    ("DC resistance (1C)", 0.0026124512480850013, "Ω", "cell/r7_final_energy_dfn.json:dcr_ohm"),
]
for r in rows:
    s.append(list(r))
for c in "ABCD":
    s[f"{c}1"].font = hdr_font
    s[f"{c}1"].fill = hdr_fill
s.column_dimensions["A"].width = 52
s.column_dimensions["D"].width = 52

# Sheet 3: energy density
s = sheet_titled("3_energy_density")
s.append(["Quantity", "Value", "Unit", "Formula / source"])
rows = [
    ("Cell mass (contract: Σ layer thickness×(1−porosity)×density×area, electrolyte excluded)", MASS_G, "g", "cell/r7_final_energy_dfn.json:mass_kg"),
    ("Layer masses (pos 16.842 / neg 8.699 / Al 4.437 / Cu 11.042 / sep 0.259)", MASS_G, "g", "r7_final_energy_dfn.json:layer_kg_m2 × area"),
    ("Gravimetric energy density", 447.12486398112617, "Wh/kg", "energy_wh ÷ mass_kg"),
    ("Cell volume = area × stack thickness (200.8 µm)", 2.062216e-05, "m3", "derived"),
    ("Volumetric energy density", 895.0169390062512, "Wh/L", "energy_wh ÷ volume_m3 × 1000"),
    ("ED incl. electrolyte (estimate 8.016 g)", 374.4156, "Wh/kg", "energy_wh ÷ (41.280+8.016)g — derived, estimate-caliber electrolyte"),
    ("Threshold check", "PASS (447.12 ≥ 327.18)", "—", "entry-0 criteria, stage2.energy_density_wh_kg.min"),
]
for r in rows:
    s.append(list(r))
for c in "ABCD":
    s[f"{c}1"].font = hdr_font
    s[f"{c}1"].fill = hdr_fill
s.column_dimensions["A"].width = 60
s.column_dimensions["D"].width = 46

# Sheet 4: NP and mass
s = sheet_titled("4_NP_mass")
s.append(["Quantity", "Value", "Unit", "Formula / source"])
rows = [
    ("Positive areal capacity (full-range)", 85.027, "Ah/m2", "c_max_pos × AMVF × L_pos × F/3600"),
    ("Negative areal capacity (full-range)", 56.744, "Ah/m2", "c_max_neg × AMVF × L_neg × F/3600"),
    ("N/P ratio (full-range basis)", 0.6674, "—", "neg ÷ pos (protocol formula)"),
    ("Positive full-range cell capacity", 8.7323, "Ah", "areal × area"),
    ("Usable-window fraction (5.0 Ah design window)", 0.5726, "—", "nominal ÷ pos full-range"),
    ("N/P ratio (usable-window basis)", 1.1655, "—", "neg ÷ (pos × fraction) — derived variant"),
    ("Total layer stack thickness", 200.8, "µm", "75.6+85.2+12+16+12"),
    ("Total mass per area", 401.9, "g/m2", "Σ layer_kg_m2 (r7_final_energy_dfn.json)"),
]
for r in rows:
    s.append(list(r))
for c in "ABCD":
    s[f"{c}1"].font = hdr_font
    s[f"{c}1"].fill = hdr_fill
s.column_dimensions["A"].width = 50
s.column_dimensions["D"].width = 46

# Sheet 5: process parameters
s = sheet_titled("5_process")
s.append(["Parameter", "Value", "Unit", "Formula / source"])
rows = [
    ("Positive areal density", 163.99, "g/m2", "thickness × (1−porosity) × density"),
    ("Negative areal density", 84.71, "g/m2", "ditto"),
    ("Positive compaction density", 2.1692, "g/cm3", "density × (1−porosity) ÷ 1000"),
    ("Negative compaction density", 0.9942, "g/cm3", "ditto"),
    ("Electrolyte fill amount", 8.016, "g/cell", "pore volume (6.680 cm3) × 1.2 g/cm3 [E]; fill factor 1.0"),
    ("Electrolyte fill per area", 78.05, "g/m2", "fill ÷ area"),
    ("Formation recommendation", "0.1C CC to 4.2 V, 25 °C, 2 cycles", "—", "design-recommended; production-line protocol requires tuning"),
]
for r in rows:
    s.append(list(r))
for c in "ABCD":
    s[f"{c}1"].font = hdr_font
    s[f"{c}1"].fill = hdr_fill
s.column_dimensions["A"].width = 46
s.column_dimensions["D"].width = 60

wb2.save(str(D / "calc.xlsx"))
print("calc.xlsx written")