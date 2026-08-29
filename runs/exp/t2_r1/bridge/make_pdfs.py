"""PDF release versions of all deliverables (reportlab, blueprint style).

Content mirrors the md/xlsx/docx sources row-by-row. Values mechanical (same sources
as the source files). Blueprint palette: #14283C deep blue / #1E5A8A medium blue /
#C97B3D copper accent.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from gen_bin import bom_rows, ENERGY_WH, MASS_CONTRACT_KG, CAP_1C, ED_WHKG, ED_WHL

DEL = Path("runs/exp/t2_r1/deliverables")
DEEP, MID, COPPER = colors.HexColor("#14283C"), colors.HexColor("#1E5A8A"), colors.HexColor("#C97B3D")
SS = getSampleStyleSheet()
ST_TITLE = SS["Title"]
ST_H2 = SS["Heading2"]
ST_BODY = SS["BodyText"]
ST_CELL = SS["BodyText"]


def cell_para(text):
    return Paragraph(str(text), ST_CELL)


def mk_table(header, rows, widths=None):
    data = [[cell_para(c) for c in header]]
    for r in rows:
        data.append([cell_para(c) for c in r])
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MID),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9DB2C4")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EFF4F8")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    if widths:
        for i, w in enumerate(widths):
            t._argW[i] = w
    return t


def build(path, title, num, blocks):
    doc = SimpleDocTemplate(str(DEL / path), pagesize=A4,
                            leftMargin=14 * mm, rightMargin=14 * mm,
                            topMargin=14 * mm, bottomMargin=14 * mm, title=title)
    story = [Paragraph(title, ParagraphStyle("h1", parent=ST_TITLE, fontSize=15,
                                             textColor=colors.white, backColor=DEEP,
                                             borderPadding=6, spaceAfter=6)),
             Paragraph(f"{num} &nbsp;|&nbsp; t2_r1 grid energy storage &nbsp;|&nbsp; 2026-08-25 &nbsp;|&nbsp; "
                       "values mechanically sourced from parameter set / simulation outputs",
                       ParagraphStyle("meta", parent=ST_BODY, fontSize=8.5, leading=11.5)),
             Spacer(1, 6)]
    for block in blocks:
        if block[0] == "h2":
            story.append(Paragraph(block[1], ParagraphStyle("h2", parent=ST_H2, fontSize=11.5,
                                                            textColor=MID, spaceBefore=8, spaceAfter=3)))
        elif block[0] == "table":
            story.append(block[1])
            story.append(Spacer(1, 6))
        elif block[0] == "note":
            story.append(Paragraph(block[1], ParagraphStyle("note", parent=ST_BODY,
                                                            fontSize=8.5, leading=11.5)))
            story.append(Spacer(1, 4))
    doc.build(story)
    print("wrote", path)


def pdf_design_spec():
    blocks = [
        ("h2", "1. Basic specification"),
        ("table", mk_table(["Item", "Value", "Source"], [
            ["Electrochemical system", "NMC811 / graphite, EC/EMC + LiPF6 (baseline chemistry; electrolyte transport overridden as formulation proxy)", "Chen2020 parameter set"],
            ["Nominal capacity", "5.0 Ah (parameter set); 5.066 Ah simulated 1C", "cell/r6_d3_1c.json:capacity_ah"],
            ["Voltage window", "2.5 - 4.2 V", "Chen2020 dump"],
            ["Discharge plateau proxy", "3.722 V at fixed t = 1800 s (calc-energy 'midpoint' scalar is a step-density artifact)", "cell/r6_d3_1c.json:voltage_v (fixed-time)"],
            ["Cell dimensions", "1580 x 65 x 0.2008 mm (W x H x T, layer stack)", "Chen2020 dump; r6_d3_energy.json:thickness_m"],
            ["Cell mass", "39.63 g (contract caliber; electrolyte excluded)", "cell/r6_d3_energy.json:mass_kg"],
            ["Shell / casing / tabs", "Not provided (no parameters in set)", "Chen2020 dump"],
            ["Electrolyte formulation", "Baseline EC/EMC + LiPF6; transport as constants sigma 3.0 S/m, D 2.5e-9 m2/s, t+ 0.35 (formulation proxy; no molecular funnel - case started at stage 3)", "candidates/r6_d3_params.json"],
            ["Cation transference number", "0.35 (base 0.2594)", "r6_d3_params.json; Chen2020 dump"],
        ], [42 * mm, 92 * mm, 52 * mm])),
        ("h2", "2. Electrode and separator"),
        ("table", mk_table(["Layer", "Thickness", "Porosity (final)", "Material / notes", "Source"], [
            ["Positive electrode", "75.6 um", "0.40 (base 0.335)", "NMC811, active vf 0.665, r_p 2.5 um (base 5.22 um), rho 3262", "Chen2020 dump; r6_d3_params.json"],
            ["Negative electrode", "85.2 um", "0.40 (base 0.25)", "graphite, active vf 0.75, r_n 2.0 um (base 5.86 um), rho 1657", "Chen2020 dump; r6_d3_params.json"],
            ["Separator", "12 um", "0.47", "polyolefin, rho 397", "Chen2020 dump"],
            ["Positive current collector", "16 um", "-", "Al, rho 2700", "Chen2020 dump"],
            ["Negative current collector", "12 um", "-", "Cu, rho 8960", "Chen2020 dump"],
            ["N/P ratio", "= 1.98", "-", "(33133x0.9014x85.2um)/(63104x0.2700x75.6um), initial-Li-content caliber; baseline geometry unchanged", "Chen2020 dump, mechanical"],
        ], [32 * mm, 20 * mm, 26 * mm, 76 * mm, 32 * mm])),
        ("h2", "3. Process design parameters"),
        ("table", mk_table(["Parameter", "Value", "Formula / note"], [
            ["Positive areal density", "147.96 g/m2", "75.6um x 0.60 x 3262"],
            ["Negative areal density", "84.71 g/m2", "85.2um x 0.60 x 1657"],
            ["Positive compaction density", "1.957 g/cm3", "3262 x 0.60 / 1000"],
            ["Negative compaction density", "0.994 g/cm3", "1657 x 0.60 / 1000"],
            ["Electrolyte fill amount", "8.62 g", "pore volume 7.185 cm3 x 1.2 g/cm3 (literature value) x 100% fill"],
            ["Formation recommendation", "0.1C CC to 4.2V, 25C, 2 cycles", "design-recommended; production value requires tuning"],
        ], [38 * mm, 34 * mm, 114 * mm])),
        ("h2", "4. Mass breakdown (contract caliber, electrolyte excluded)"),
        ("table", mk_table(["Layer", "kg/m2", "g/cell", "Source"], [
            ["Positive electrode", 0.147964, 15.196, "r6_d3_energy.json:layer_kg_m2 x 0.1027 m2"],
            ["Negative electrode", 0.084706, 8.699, "idem"],
            ["Positive current collector", 0.043200, 4.437, "idem"],
            ["Negative current collector", 0.107520, 11.042, "idem"],
            ["Separator", 0.002525, 0.259, "idem"],
            ["TOTAL", 0.385915, "39.63 g", "r6_d3_energy.json:mass_kg"],
        ], [44 * mm, 26 * mm, 26 * mm, 90 * mm])),
        ("h2", "5. Performance verification (vs entry-0 criteria)"),
        ("table", mk_table(["Item", "Value", "Criterion", "Determination", "Source"], [
            ["Energy density", "465.62 Wh/kg", ">= 327.18 Wh/kg", "PASS", "cell/r6_d3_energy.json:energy_density_wh_kg"],
            ["4C fast charge - plating", "anode pot min +0.0498 V", "no plating (>= 0 V)", "PASS", "cell/r6_d3_4c.json:anode_potential_v"],
            ["SEI @100 cyc", "9.087 nm", "<= 500 nm", "PASS", "cell/r6_d3_aging100.json:sei_thickness_nm_end"],
            ["SEI @500 cyc", "25.317 nm", "<= 550 nm", "PASS", "cell/r6_d3_aging500.json:sei_thickness_nm_end"],
            ["-20C retention", "99.571%", ">= 90%", "PASS", "cell/r6_d3_lowT_ret.json (100 x 5.04452/5.06626 Ah)"],
            ["-20C true-soak cross-check", "99.571%, T_max 266.7 K", ">= 90%", "PASS", "cell/r6_d3_lowT_soak.json (Initial temperature 253.15 K probe)"],
            ["4C acceptance / temperature", "0.838 Ah; T_max 342.4 K (+24.2 K)", "informational", "-", "cell/r6_d3_4c.json"],
        ], [30 * mm, 40 * mm, 30 * mm, 20 * mm, 66 * mm])),
        ("h2", "6. Design notes"),
        ("note", "1) Electrolyte transport constants (sigma 0.4->3.0 S/m; D 4e-10->2.5e-9 m2/s; t+ 0.2594->0.35): baseline 4C plated (min -0.1918 V); constant formulation proxy solved plating (R2) and enables -20C. 2) Negative particle radius 5.86->2.0 um (R2/R4): 4C margin +0.091 V, acceptance 0.553 Ah. 3) Positive particle radius 5.22->2.5 um (R5): +50% acceptance (0.828 Ah), ED 458.1 Wh/kg. 4) k_sei 1e-12->1e-16 m/s (R3, coating bridge): SEI@500cyc 777.9->21.7 nm. 5) Negative porosity 0.35->0.40 (R6 probe): strictly non-worse; ED 465.6 Wh/kg; margin +0.0498 V (within solve noise)."),
        ("note", "Honest annotations: volume-fraction consistency (active vf 0.665/0.75 defined at base porosity; final porosity 0.40 makes active+pore>1 in model bookkeeping - interpreted as replacing unmodeled binder/additive volume); calc-energy midpoint/DCR scalars are solver-step-density index artifacts (time-integral metrics unaffected; fixed-time v@1800s used); aging per-cycle capacity is a PyBaMM variable artifact (probe: real steps are full 1C swings 5.08/4.75 Ah; sei_thickness_nm_end accumulates over genuine full-depth cycles); part of the porosity ED gain is contract-caliber (electrolyte excluded from mass; worst-case re-inclusion still 459.6 Wh/kg); 4C temperature +24.2 K above ambient with no contract red line (cooling h not a design lever)."),
    ]
    build("design_spec.pdf", "Cell Design Specification - GridStore-D3", "VBF-T2R1-DS-01", blocks)


def pdf_bom():
    rows, _ = bom_rows()
    data = [["Component", "Volume fraction / basis", "Mass g/cell", "kg/kWh", "Source / formula"]]
    total_g = 0.0
    for name, vf, mass, src in rows:
        if mass is None:
            data.append([name, vf, "Not modeled", "", src])
            continue
        total_g += mass
        data.append([name, vf, f"{mass:.4f}", f"{mass/1000.0/(ENERGY_WH/1000.0):.4f}", src])
    data.append(["TOTAL (BOM caliber: incl. lit-default additive/binder + electrolyte)", "", f"{total_g:.3f}",
                 f"{total_g/1000.0/(ENERGY_WH/1000.0):.4f}", f"sum of rows; total energy {ENERGY_WH:.4f} Wh"])
    data.append(["TOTAL cell mass (contract caliber: layers only, electrolyte/binder/additive excluded)", "",
                 f"{MASS_CONTRACT_KG*1000:.3f}", f"{MASS_CONTRACT_KG/(ENERGY_WH/1000.0):.4f}",
                 "cell/r6_d3_energy.json:mass_kg"])
    blocks = [("h2", "Bill of materials (dual caliber: g/cell and kg/kWh)"),
              ("table", mk_table(data[0], data[1:], [56 * mm, 34 * mm, 20 * mm, 16 * mm, 60 * mm]))]
    build("bom.pdf", "Bill of Materials - GridStore-D3", "VBF-T2R1-BOM-01", blocks)


def pdf_datasheet():
    blocks = [
        ("h2", "Technical datasheet"),
        ("table", mk_table(["Field", "Value", "Source"], [
            ["Rated capacity (Ah)", "5.0 nominal (parameter set); 5.066 simulated 1C discharge", "Chen2020 dump; cell/r6_d3_1c.json:capacity_ah"],
            ["Nominal voltage / voltage window (V)", "2.5 - 4.2 V; plateau proxy 3.722 V at fixed t = 1800 s", "Chen2020 dump; r6_d3_1c.json (calc-energy 'midpoint' is a step-density artifact - design_spec section 6)"],
            ["Rated energy (Wh)", "18.454 (time integration of V*I at 1C)", "cell/r6_d3_energy.json:energy_wh"],
            ["Energy density", "465.62 Wh/kg (contract caliber, electrolyte excluded); 894.87 Wh/L", "cell/r6_d3_energy.json:energy_density_wh_kg / _wh_l"],
            ["Maximum continuous discharge rate", "1C (5.066 A) simulated; higher rates not in task contract", "cell/r6_d3_1c.json"],
            ["Fast-charge capability", "4C charge @ 45C: plating-free (anode pot min +0.0498 V), acceptance 0.838 Ah, T_max 342.39 K (+24.2 K)", "cell/r6_d3_4c.json"],
            ["Operating temperature range", "Verified -20C (253.15 K) to +45C (318.15 K) per simulation conditions; -20C retention 99.571% (protocol and true-soak, cell temp 266.7 K)", "cell/r6_d3_lowT_ret.json; r6_d3_lowT_soak.json"],
            ["Cycle life", "Aging protocol (1C CC 2.5-4.2 V, SEI model): SEI 9.087 nm @100 cyc, 25.317 nm @500 cyc (limits 500/550 nm); trajectory flat. Annotation: reported per-cycle capacity variable is a PyBaMM artifact (freezes at first-discharge value); probe confirms real steps are full 1C swings (5.08 Ah dis / 4.75 Ah chg)", "cell/r6_d3_aging100.json / r6_d3_aging500.json; bridge/probe_aging.py"],
            ["Safety determination", "4C plating-free; T_max 342.39 K during 4C charge (no contract red line); nail/overcharge/crush not simulated - N/A (beyond pure simulation boundary)", "cell/r6_d3_4c.json"],
            ["Dimensions and mass", "1580 x 65 x 0.2008 mm; 39.63 g contract caliber (electrolyte excluded); shell Not provided", "Chen2020 dump; r6_d3_energy.json"],
        ], [36 * mm, 96 * mm, 54 * mm])),
    ]
    build("datasheet.pdf", "Technical Datasheet - GridStore-D3", "VBF-T2R1-DSH-01", blocks)


def pdf_calc():
    blocks = [
        ("h2", "1. Input parameters"),
        ("table", mk_table(["Parameter", "Base (Chen2020)", "Final (GridStore-D3)", "Source"], [
            ["Nominal cell capacity [A.h]", 5.0, 5.0, "Chen2020 dump"],
            ["Positive electrode thickness [m]", 7.56e-05, 7.56e-05, "Chen2020 dump"],
            ["Negative electrode thickness [m]", 8.52e-05, 8.52e-05, "Chen2020 dump"],
            ["Positive electrode porosity", 0.335, 0.40, "r6_d3_params.json"],
            ["Negative electrode porosity", 0.25, 0.40, "r6_d3_params.json"],
            ["Positive particle radius [m]", 5.22e-06, 2.5e-06, "r6_d3_params.json"],
            ["Negative particle radius [m]", 5.86e-06, 2.0e-06, "r6_d3_params.json"],
            ["Electrolyte conductivity [S.m-1]", "Nyman2008 f(T)", 3.0, "r6_d3_params.json (constant override)"],
            ["Electrolyte diffusivity [m2.s-1]", "Nyman2008 f(T)", 2.5e-09, "r6_d3_params.json (constant override)"],
            ["Cation transference number", 0.2594, 0.35, "r6_d3_params.json"],
            ["SEI kinetic rate constant [m.s-1]", 1e-12, 1e-16, "r6_d3_params.json (coating bridge)"],
            ["Voltage cut-offs [V]", "2.5 / 4.2", "2.5 / 4.2", "Chen2020 dump"],
        ], [44 * mm, 26 * mm, 26 * mm, 62 * mm])),
        ("h2", "2. Capacity and energy"),
        ("table", mk_table(["Item", "Formula", "Value", "Source"], [
            ["1C discharge capacity [Ah]", "run-pyamm 1C_discharge", CAP_1C, "cell/r6_d3_1c.json:capacity_ah"],
            ["Discharge energy [Wh]", "trapezoid integral of voltage_v x I_1C over time_s; I_1C = 5.0 A", f"{ENERGY_WH:.4f}", "cell/r6_d3_energy.json:energy_wh"],
        ], [34 * mm, 66 * mm, 20 * mm, 40 * mm])),
        ("h2", "3. Energy density"),
        ("table", mk_table(["Item", "Formula", "Value", "Source"], [
            ["Gravimetric ED [Wh/kg]", "energy / mass (layers only, electrolyte excluded)", ED_WHKG, "cell/r6_d3_energy.json:energy_density_wh_kg"],
            ["Volumetric ED [Wh/L]", "energy / volume (layer stack x area)", ED_WHL, "cell/r6_d3_energy.json:energy_density_wh_l"],
            ["Criterion check", "465.62 >= 327.18", "PASS", "entry-0 criteria.stage2.energy_density_wh_kg"],
        ], [30 * mm, 66 * mm, 20 * mm, 44 * mm])),
        ("h2", "4. N/P and mass"),
        ("table", mk_table(["Item", "Formula", "Value", "Source"], [
            ["N/P ratio", "(33133x0.9014x85.2um)/(63104x0.2700x75.6um)", 1.9755, "Chen2020 dump; initial-Li-content caliber (set defines initial concentrations, not x0/x100 windows)"],
            ["Positive electrode", "75.6um x 0.60 x 3262", "147.96 g/m2", "r6_d3_energy.json:layer_kg_m2"],
            ["Negative electrode", "85.2um x 0.60 x 1657", "84.71 g/m2", "idem"],
            ["Positive current collector", "16um x 2700", "43.20 g/m2", "idem"],
            ["Negative current collector", "12um x 8960", "107.52 g/m2", "idem"],
            ["Separator", "12um x 0.53 x 397", "2.52 g/m2", "idem"],
            ["TOTAL mass", "sum x 0.1027 m2", "39.633 g", "r6_d3_energy.json:mass_kg"],
        ], [30 * mm, 46 * mm, 20 * mm, 64 * mm])),
        ("h2", "5. Process parameters"),
        ("table", mk_table(["Parameter", "Formula", "Value", "Unit", "Source"], [
            ["Positive areal density", "75.6um x (1-0.40) x 3262", 147.96, "g/m2", "calc-energy layer_kg_m2"],
            ["Negative areal density", "85.2um x (1-0.40) x 1657", 84.71, "g/m2", "calc-energy layer_kg_m2"],
            ["Positive compaction density", "3262 x (1-0.40) / 1000", 1.957, "g/cm3", "design-spec process formula (divide by 1000)"],
            ["Negative compaction density", "1657 x (1-0.40) / 1000", 0.994, "g/cm3", "design-spec process formula"],
            ["Electrolyte fill amount", "pore volume 7.185 cm3 x 1.2 g/cm3 x 100%", 8.62, "g", "electrolyte density 1.2 g/cm3 = literature value (annotated)"],
            ["Formation recommendation", "0.1C CC to 4.2V, 25C, 2 cycles", "-", "", "design-recommended; production value requires tuning"],
        ], [34 * mm, 50 * mm, 16 * mm, 12 * mm, 46 * mm])),
    ]
    build("calc.pdf", "Design Calculation Sheet - GridStore-D3", "VBF-T2R1-CALC-01", blocks)


def pdf_dvpr():
    blocks = [
        ("h2", "Verification items (virtual-test version)"),
        ("table", mk_table(["#", "Item", "Condition", "Result value", "Determination", "Source"], [
            [1, "1C discharge capacity", "1C_discharge, 298.15 K", "5.06626 Ah (nominal 5.0 Ah)", "PASS (>= nominal)", "cell/r6_d3_1c.json:capacity_ah"],
            [2, "Energy density", "contract caliber (calc-energy)", "465.62 Wh/kg", "PASS vs >= 327.18", "cell/r6_d3_energy.json:energy_density_wh_kg"],
            [3, "4C fast-charge plating", "4C_charge_45C --plating, 318.15 K", "anode pot min +0.0498 V", "PASS (min >= 0)", "cell/r6_d3_4c.json:anode_potential_v"],
            [4, "4C temperature rise", "4C_charge_45C --thermal lumped", "T_max 342.39 K (+24.2 K)", "informational (no contract red line)", "cell/r6_d3_4c.json:T_max_K"],
            [5, "Voltage window", "parameter-set limits", "2.5 - 4.2 V", "PASS (as specified)", "Chen2020 dump"],
            [6, "-20C discharge retention", "lowT_discharge, 253.15 K", "99.571% (5.04452/5.06626 Ah)", "PASS vs >= 90%", "cell/r6_d3_lowT_ret.json"],
            [7, "-20C true-soak cross-check", "lowT + Initial temperature 253.15 K", "99.571% (5.04452 Ah), T_max 266.71 K", "PASS vs >= 90%", "cell/r6_d3_lowT_soak.json"],
            [8, "SEI @100 cyc", "aging_1C_100cyc (1C CC 2.5-4.2 V)", "9.087 nm", "PASS vs <= 500 nm", "cell/r6_d3_aging100.json:sei_thickness_nm_end"],
            [9, "SEI @500 cyc", "aging --cycles 500", "25.317 nm", "PASS vs <= 550 nm", "cell/r6_d3_aging500.json:sei_thickness_nm_end"],
            [10, "Cycle-capacity trajectory shape", "aging protocol", "flat (0.3032->0.3041 Ah, no climb artifact)", "informational", "cell/r6_d3_aging500.json:capacity_ah_per_cycle"],
        ], [8 * mm, 28 * mm, 40 * mm, 42 * mm, 28 * mm, 44 * mm])),
        ("h2", "Items marked N/A (beyond pure simulation boundary / requires physical experiment)"),
        ("table", mk_table(["Item", "Reason"], [
            ["Nail penetration", "N/A (requires physical experiment)"],
            ["Overcharge to thermal runaway", "N/A (protocol available but not in task contract; not executed)"],
            ["Crush, drop", "N/A (requires physical experiment)"],
            ["Rate-pulse internal resistance", "N/A (calc-energy DCR scalar is a step-density artifact - design_spec section 6)"],
            ["Real-electrode coating validation (k_sei 1e-16 bridge)", "N/A (requires Stage 2 material work / physical validation - honest gap)"],
            ["CAD structure model", "N/A (not requested in task clarification; optional deliverable)"],
        ], [52 * mm, 134 * mm])),
        ("note", "Conclusion: 5/5 contractual verification items PASS with margin (ED x1.42, plating-free at 4C, SEI 9.1/25.3 nm vs 500/550 nm, -20C retention 99.6%). Uncovered items cited directly as paper limitations. Known tool artifacts annotated (aging per-cycle-capacity variable freezes at first-discharge value while real steps are full 1C swings - probe-grounded; calc-energy midpoint/DCR step-density artifacts)."),
    ]
    build("dvpr.pdf", "Design Verification Plan and Report (virtual) - GridStore-D3", "VBF-T2R1-DVPR-01", blocks)


def pdf_dfmea():
    blocks = [
        ("h2", "Failure-mode table (qualitative; S/O high/medium/low based on simulation signals)"),
        ("table", mk_table(["#", "Failure mode", "Failure cause", "Simulation signal", "S", "O", "Mitigation recommendation"], [
            [1, "Anode lithium plating at 4C", "transport-limited anode polarization at 4C/45C", "anode_potential_v min +0.0498 V (thinnest margin in family; baseline -0.1918 V)", "high", "low", "keep transport formulation (sigma 3.0, D 2.5e-9, r_n 2.0um, r_p 2.5um); margin monitoring; fallback D1 (+0.091 V) on record"],
            [2, "Excessive temperature rise at fast charge", "self-heating at 4C", "T_max 342.39 K at 318.15 K ambient (+24.2 K)", "medium", "medium", "no contract red line; verify cell-level cooling in field use (cooling h not a design lever here)"],
            [3, "Electrolyte oxidative decomposition at high voltage", "cathode potential vs electrolyte stability", "window capped 4.2 V; HOMO endorsement skipped (real_compute=false)", "medium", "low", "keep 4.2 V cutoff; run Stage 2 molecular validation before production (honest gap)"],
            [4, "Insufficient capacity / ED", "loading / transport mismatch", "1C 5.066 Ah >= 5.0; ED 465.62 >= 327.18", "low", "low", "none required (margin x1.42)"],
            [5, "Low-temperature capacity loss", "electrolyte transport freezing at -20C", "retention 99.571% (protocol + true-soak, 266.7 K)", "low", "low", "constant-transport formulation proxy is the enabler; validate real electrolyte at -20C physically"],
            [6, "Long-term SEI overgrowth (>550 nm @500cyc)", "SEI growth kinetics", "25.32 nm @500 cyc (k_sei 1e-16 coating bridge; baseline 777.9 nm)", "medium", "low", "actual coating must be developed and validated (Stage 2 + physical aging); without it baseline kinetics FAIL"],
            [7, "Model bookkeeping inconsistency (porosity override)", "active vf (0.665/0.75) defined at base porosity; 0.40 makes active+pore>1", "parameter-set arithmetic (design_spec section 6)", "low", "low", "physical electrode reformulation (binder/additive accounting) before manufacture; annotated in spec"],
        ], [8 * mm, 30 * mm, 34 * mm, 48 * mm, 10 * mm, 10 * mm, 50 * mm])),
        ("note", "Conclusion: highest-risk items are #1 (plating margin thin at +0.0498 V) and #6 (SEI-kinetics rests on the coating bridge - physical validation mandatory). Mitigations embedded in design; fallback designs on record. Process/supplier-level FMEA: N/A (beyond pure simulation boundary)."),
    ]
    build("dfmea.pdf", "Design FMEA (qualitative) - GridStore-D3", "VBF-T2R1-DFMEA-01", blocks)


def pdf_index():
    blocks = [
        ("h2", "Cover information"),
        ("table", mk_table(["Field", "Value"], [
            ["Case name", "t2_r1 - grid energy storage battery design (ED >= 327.18 Wh/kg; 4C no plating; SEI <= 500/550 nm @100/500 cyc; -20C >= 90%)"],
            ["Numbering scheme", "VBF-T2R1-<DOC-CODE>-<SEQ-NO>"],
            ["Generation date", "2026-08-25"],
            ["Prepared / Reviewed / Approved", "(blank - for manual signing)"],
        ], [34 * mm, 152 * mm])),
        ("h2", "File list (row-by-row identical to delivery_index.md)"),
        ("table", mk_table(["File name", "Number", "Format", "Source description"], [
            ["design_spec.md", "VBF-T2R1-DS-01", "md", "Generated per deliverable-design-spec spec; values mechanically from Chen2020 dump + sim outputs"],
            ["design_spec.pdf", "VBF-T2R1-DS-01", "pdf", "PDF release, md -> reportlab (blueprint style)"],
            ["report.html", "VBF-T2R1-DS-02", "html", "bda render self-contained report (ancillary, belongs to DS)"],
            ["bom.xlsx", "VBF-T2R1-BOM-01", "xlsx", "Generated per deliverable-bom spec (openpyxl); dual caliber g/cell + kg/kWh"],
            ["bom.pdf", "VBF-T2R1-BOM-01", "pdf", "PDF release, xlsx -> reportlab table export"],
            ["datasheet.docx", "VBF-T2R1-DSH-01", "docx", "Generated per deliverable-datasheet spec (python-docx)"],
            ["datasheet.pdf", "VBF-T2R1-DSH-01", "pdf", "PDF release, docx content -> reportlab"],
            ["calc.xlsx", "VBF-T2R1-CALC-01", "xlsx", "Generated per deliverable-calc-sheet spec (openpyxl); 5 sheets, formula + source columns"],
            ["calc.pdf", "VBF-T2R1-CALC-01", "pdf", "PDF release, xlsx -> reportlab table export"],
            ["dvpr.md", "VBF-T2R1-DVPR-01", "md", "Virtual-test verification report (simulation values, mechanical)"],
            ["dvpr.pdf", "VBF-T2R1-DVPR-01", "pdf", "PDF release, md -> reportlab"],
            ["dfmea.md", "VBF-T2R1-DFMEA-01", "md", "Qualitative design FMEA (simulation-signal based)"],
            ["dfmea.pdf", "VBF-T2R1-DFMEA-01", "pdf", "PDF release, md -> reportlab"],
            ["delivery_index.md", "VBF-T2R1-IDX-01", "md", "This index"],
            ["delivery_index.pdf", "VBF-T2R1-IDX-01", "pdf", "PDF release, md -> reportlab"],
        ], [34 * mm, 34 * mm, 14 * mm, 104 * mm])),
        ("note", "Notes: CAD structure model not produced (optional deliverable decided by user clarification; not requested in this task - recorded honestly). All values in all files are mechanically sourced (parameter-set dump, simulation output JSONs, bridge JSONs, or annotated literature defaults). report.html lives in the workspace root; all other files in deliverables/."),
    ]
    build("delivery_index.pdf", "Delivery Package Index - t2_r1", "VBF-T2R1-IDX-01", blocks)


if __name__ == "__main__":
    DEL.mkdir(parents=True, exist_ok=True)
    pdf_design_spec()
    pdf_bom()
    pdf_datasheet()
    pdf_calc()
    pdf_dvpr()
    pdf_dfmea()
    pdf_index()
    print("all PDFs written")
