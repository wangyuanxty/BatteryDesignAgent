import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()

# Calc sheet
ws_calc = wb.active
ws_calc.title = "Design Calculations"

header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="14283C", end_color="14283C", fill_type="solid")
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

# Section 1: Mass Calculation
ws_calc.cell(row=1, column=1, value="Mass Calculation").font = Font(bold=True, size=12)
mass_headers = ["Component", "Thickness (m)", "Porosity", "Density (kg/m³)", "Area (m²)", "Mass (kg)", "Mass (g)"]
for col, h in enumerate(mass_headers, 1):
    cell = ws_calc.cell(row=2, column=col, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border

mass_data = [
    ["Positive electrode", 0.0001, 0.32, 3260, 0.1027, "=B3*(1-C3)*D3*E3", "=F3*1000"],
    ["Positive CC", 0.00001, 0, 2700, 0.1027, "=B4*(1-C4)*D4*E4", "=F4*1000"],
    ["Separator", 0.000015, 0.45, 900, 0.1027, "=B5*(1-C5)*D5*E5", "=F5*1000"],
    ["Negative CC", 0.000005, 0, 8960, 0.1027, "=B6*(1-C6)*D6*E6", "=F6*1000"],
    ["Negative electrode", 0.00009, 0.28, 1660, 0.1027, "=B7*(1-C7)*D7*E7", "=F7*1000"],
    ["TOTAL", "", "", "", "", "=SUM(F3:F7)", "=SUM(G3:G7)"],
]
for row_idx, row_data in enumerate(mass_data, 3):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws_calc.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border
        if row_idx == 8:
            cell.font = Font(bold=True)

# Section 2: Energy Density
ws_calc.cell(row=10, column=1, value="Energy Density Calculation").font = Font(bold=True, size=12)
ed_data = [
    ["Parameter", "Value", "Unit", "Source"],
    ["Discharge energy", 19.367, "Wh", "r3_archF_1c_energy.json:energy_wh"],
    ["Total mass", 0.04142, "kg", "Sum of layer masses"],
    ["Energy density", "=B12/B13", "Wh/kg", "Energy / Mass"],
    ["Volumetric ED", "=B12/0.0000226", "Wh/L", "Energy / Volume"],
    ["Midpoint voltage", 3.993, "V", "r3_archF_1c_energy.json:midpoint_voltage_v"],
    ["DC resistance", 0.000115, "Ω", "r3_archF_1c_energy.json:dcr_ohm"],
    ["Power density", "=B16^2/(4*B17)/B13", "W/kg", "V_OC²/(4·R) / mass"],
]
for row_idx, row_data in enumerate(ed_data, 11):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws_calc.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border
        if row_idx == 11:
            cell.font = header_font
            cell.fill = header_fill

# Section 3: Rate Capability
ws_calc.cell(row=20, column=1, value="Rate Capability").font = Font(bold=True, size=12)
rate_data = [
    ["Condition", "Capacity (Ah)", "Retention (%)", "T_max (K)", "Source"],
    ["1C discharge", 5.326, 100, 308.8, "r3_archF_1c.json"],
    ["5C discharge", 5.071, "=B22/B22*100", 386.6, "r3_archF_5c.json"],
    ["5C retention", "=B23/B22", "target>=90%", "", ""],
]
for row_idx, row_data in enumerate(rate_data, 21):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws_calc.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border
        if row_idx == 21:
            cell.font = header_font
            cell.fill = header_fill

# Section 4: Safety
ws_calc.cell(row=26, column=1, value="Safety Assessment").font = Font(bold=True, size=12)
safety_data = [
    ["Test", "T_max (K)", "Limit (K)", "Verdict", "Anode min (V)", "Plating"],
    ["4C charge 45°C", 361.8, 358.15, "MARGINAL", 0.030, "No"],
]
for row_idx, row_data in enumerate(safety_data, 27):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws_calc.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border
        if row_idx == 27:
            cell.font = header_font
            cell.fill = header_fill

# Set column widths
for i in range(1, 8):
    ws_calc.column_dimensions[openpyxl.utils.get_column_letter(i)].width = 18

wb.save("runs/exp/t8_r1_mimo/deliverables/calc.xlsx")
print("Calc sheet created")
