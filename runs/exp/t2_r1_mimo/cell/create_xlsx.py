import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

ddir = "runs/exp/t2_r1_mimo/deliverables"

# === bom.xlsx ===
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"

# Header style
header_font = Font(bold=True, color="FFFFFF", size=11)
header_fill = PatternFill(start_color="1E5A8A", end_color="1E5A8A", fill_type="solid")
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

headers = ["Item", "Component", "Material", "Quantity", "Unit Mass (g)", "Total Mass (g)", "Source"]
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border

bom_data = [
    ["1", "Positive electrode active layer", "NMC811", "1", "16.8", "16.8", "calc-energy layer_kg_m2"],
    ["2", "Negative electrode active layer", "Graphite", "1", "10.9", "10.9", "calc-energy layer_kg_m2"],
    ["3", "Positive current collector", "Aluminum (16µm)", "1", "4.4", "4.4", "calc-energy layer_kg_m2"],
    ["4", "Negative current collector", "Copper (12µm)", "1", "11.0", "11.0", "calc-energy layer_kg_m2"],
    ["5", "Separator", "PP/PE (25µm)", "1", "0.26", "0.26", "calc-energy layer_kg_m2"],
    ["6", "Electrolyte", "EC/EMC + LiPF6", "1", "N/A", "N/A", "Not in param set"],
    ["", "", "", "", "TOTAL", "33.4", "Excl. electrolyte"],
]

for row_idx, row_data in enumerate(bom_data, 2):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border

# Auto-width
for col in ws.columns:
    max_len = max(len(str(c.value or "")) for c in col)
    ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 30)

wb.save(f"{ddir}/bom.xlsx")
print("Created bom.xlsx")

# === calc.xlsx ===
wb2 = openpyxl.Workbook()
ws2 = wb2.active
ws2.title = "Calculations"

calc_headers = ["Parameter", "Value", "Unit", "Formula/Source"]
for col, h in enumerate(calc_headers, 1):
    cell = ws2.cell(row=1, column=col, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border

calc_data = [
    ["Nominal capacity", "3.28", "Ah", "Simulation: r5_Q_1c.json"],
    ["1C current", "3.28", "A", "= Nominal capacity × 1"],
    ["Discharge energy", "11.84", "Wh", "= ∫V·I₁C dt / 3600 (trapezoidal)"],
    ["Cell mass (excl. electrolyte)", "33.4", "g", "= Σ layer thickness×(1−ε)×density×area"],
    ["Energy density (gravimetric)", "378.69", "Wh/kg", "= 11.84 Wh / 0.0334 kg"],
    ["Midpoint voltage", "3.61", "V", "= Voltage at discharge midpoint"],
    ["DC resistance", "0.35", "mΩ", "= (OCV_start − V_10%) / I₁C"],
    ["Power density", "269.7", "W/kg", "= V_OC²/(4·DCR) / mass"],
    ["Positive electrode thickness", "40", "µm", "Parameter override"],
    ["Negative electrode thickness", "60", "µm", "Parameter override"],
    ["N/P ratio", "1.5", "—", "= 60/40"],
    ["Positive particle radius", "2", "µm", "Parameter override"],
    ["Negative particle radius", "5", "µm", "Parameter override"],
    ["Electrolyte diffusivity", "2.0e-9", "m²/s", "Parameter override (estimate)"],
    ["Electrolyte conductivity", "2.5", "S/m", "Parameter override (estimate)"],
    ["Cation transference number", "0.38", "—", "Parameter override (estimate)"],
    ["SEI kinetic rate constant", "7e-15", "m/s", "Parameter override (estimate)"],
    ["4C charge T_max", "344.95", "K", "Simulation: r5_Q_4c.json"],
    ["4C min anode potential", "0.0006", "V", "Simulation: r5_Q_4c.json"],
    ["Low-T (-20°C) retention", "99.99", "%", "= cap_lowT / cap_1C × 100"],
    ["SEI thickness @100 cyc", "205.9", "nm", "Simulation: r5_Q_aging100.json"],
    ["SEI thickness @500 cyc", "518.1", "nm", "Simulation: r5_Q_aging500.json"],
]

for row_idx, row_data in enumerate(calc_data, 2):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border

for col in ws2.columns:
    max_len = max(len(str(c.value or "")) for c in col)
    ws2.column_dimensions[col[0].column_letter].width = min(max_len + 2, 40)

wb2.save(f"{ddir}/calc.xlsx")
print("Created calc.xlsx")

print("Done")
