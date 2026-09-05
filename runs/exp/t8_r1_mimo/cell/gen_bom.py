import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()

# BOM sheet
ws_bom = wb.active
ws_bom.title = "BOM"

# Header style
header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="14283C", end_color="14283C", fill_type="solid")
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

# BOM headers
bom_headers = ["Item", "Component", "Material", "Thickness (µm)", "Area (m²)",
               "Density (kg/m³)", "Mass per m² (g/m²)", "Total Mass (g)", "Notes"]
for col, h in enumerate(bom_headers, 1):
    cell = ws_bom.cell(row=1, column=col, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', wrap_text=True)
    cell.border = thin_border

# BOM data
bom_data = [
    [1, "Positive electrode", "NMC811", 100, 0.1027, 3260, 221.8, 22.78, "Active material + binder"],
    [2, "Positive CC", "Aluminum", 10, 0.1027, 2700, 27.0, 2.77, "Current collector"],
    [3, "Separator", "PE", 15, 0.1027, 900, 2.38, 0.24, "Polyolefin"],
    [4, "Negative CC", "Copper", 5, 0.1027, 8960, 44.8, 4.60, "Current collector"],
    [5, "Negative electrode", "Graphite", 90, 0.1027, 1660, 107.4, 11.03, "Active material + binder"],
    [6, "TOTAL", "—", "—", "—", "—", "—", 41.42, "Formula-caliber mass (excl. electrolyte/casing)"],
]

for row_idx, row_data in enumerate(bom_data, 2):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws_bom.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border
        if row_idx == 7:  # Total row
            cell.font = Font(bold=True)

# Set column widths
widths = [6, 22, 12, 12, 10, 12, 14, 12, 30]
for i, w in enumerate(widths, 1):
    ws_bom.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

wb.save("runs/exp/t8_r1_mimo/deliverables/bom.xlsx")
print("BOM created")
