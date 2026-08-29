# Build the 7 deliverable sources (md/xlsx) + 7 PDF releases for case t2_r1_noceiling.
# All numeric values are taken from tool outputs / log.jsonl evaluate entries only.
import json
from pathlib import Path

CASE = Path("runs/exp/t2_r1_noceiling")
DEL = CASE / "deliverables"
DEL.mkdir(exist_ok=True)
CID = "T2R1NOCEILING"

# ---------------------------------------------------------------- shared numbers
L = {
    "ed": 476.72, "ed_wh_l": 891.88, "cap": 4.9520, "energy_wh": 17.4766,
    "mass_kg": 0.036660, "area": 0.1027, "thick_um": 190.8, "vol_cm3": 19.60,
    "mid_v": 3.9474, "dcr": 0.19939, "pd": 558718.5,
    "anode_min": -0.3868, "tmax4c": 333.2, "charge_ah": 0.0461, "charge_s": 8.4,
    "sei100": 467.6, "sei500": 811.3, "lowT": 0.9944, "nominal": 4.9506,
}
LAYERS = [
    ("Positive electrode (NMC811)", 75.6, 0.335, 0.163994),
    ("Negative electrode (graphite)", 85.2, 0.350, 0.091765),
    ("Positive current collector (Al)", 10.0, None, 0.027000),
    ("Negative current collector (Cu)", 8.0, None, 0.071680),
    ("Separator", 12.0, 0.47, 0.002525),
]

# Comparison table from log.jsonl evaluate entries (tool-source values)
COMP = [
    ("Baseline Chen2020", "-", 400.3, 449.1, 777.9, 0.9943, -0.4385),
    ("A ThinCC", "R2", 456.4, 449.1, 777.9, 0.9943, -0.4386),
    ("B HiCond (sigma x2, D x1.7, t+ 0.4)", "R2", 404.1, 476.8, 829.8, 0.9945, -0.4494),
    ("C SmallNeg (r 3.5 um)", "R2", 407.0, 452.9, 771.4, 0.9944, -0.4368),
    ("D LowLoad (x0.728)", "R2", 355.6, 481.0, 836.8, 0.9940, -0.4067),
    ("E ThickNeg (N/P 1.5)", "R3", 478.6, 494.6, 865.6, 0.9999, -0.4643),
    ("F ThinSep (9 um / 0.55)", "R3", 458.6, 455.0, 787.9, 0.9943, -0.4348),
    ("G ThickNeg+ThinSep", "R3", 480.0, 496.2, 868.9, 0.9999, -0.4704),
    ("H ThickNeg2 (N/P 1.77)", "R3", 452.1, 540.0, 979.9, 1.0000, -0.5027),
    ("I Cool (h 100)", "R4", 454.1, 454.1, 786.4, 0.9919, -0.4337),
    ("J CathPartUp (12.5 um)", "R4", 376.4, 463.3, 856.7, 0.9999, -0.4455),
    ("K TransDown (degenerate)", "R4", 238.2, 68.0, 68.0, 1.0000, +0.1178),
    ("L AnPorUp (SELECTED)", "R4", 476.7, 467.6, 811.3, 0.9944, -0.3868),
]

# ---------------------------------------------------------------- 1. design_spec.md
ds = f"""# Design Specification - Grid Energy Storage Cell (Case {CID})

**Case**: t2_r1_noceiling | **Ablation**: ceiling_escalation OFF (no proactive material-design escalation)
**Status**: NEGATIVE RESULT - 3 of 5 criteria met; 2 criteria infeasible in the admissible design
space (evidence: 4 rounds, 14 evaluated designs, 10 lever axes, all mechanically evaluated via
`bda log-evaluate` against entry-0 criteria).

## 1. Task criteria (thresholds verbatim from task text, log.jsonl entry 0)

| Criterion | Threshold | Decision layer |
|---|---|---|
| Gravimetric energy density | >= 327.18 Wh/kg | stage2 |
| 4C fast charge, no lithium plating | plated = false (min anode surface potential difference at separator interface >= 0 V) | stage3 |
| Anode SEI thickness after 100 cycles of 1C cycling | <= 500 nm | stage2 |
| Discharge capacity retention at -20 C | >= 0.90 | stage2 |
| Anode SEI thickness after 500 cycles of 1C cycling | <= 550 nm | stage2 |

## 2. Selected design: L "AnPorUp" (best-effort)

Base parameter set: Chen2020 (NMC811/graphite teaching parameterization), SPMe, start_stage 3.
Degrees of freedom per entry 0: electrode_system locked, electrolyte_formulation adjustable,
electrode_modification locked, cell_architecture adjustable, thermal_management adjustable.

| Parameter | Baseline | Design L |
|---|---|---|
| Positive current collector thickness [m] | 1.6e-05 | 1.0e-05 |
| Negative current collector thickness [m] | 1.2e-05 | 8.0e-06 |
| Negative electrode porosity | 0.25 | 0.35 |
| Nominal cell capacity [A.h] | 5.0 | 4.9506 (measured 1C, honest C-rate bookkeeping) |

All other parameters at Chen2020 baseline: separator 12 um / porosity 0.47, negative electrode
85.2 um, positive electrode 75.6 um / porosity 0.335, particle radii 5.86 / 5.22 um, electrolyte
Nyman2008 transport functions, t+ 0.2594, cooling h 10 W/m2/K.

Design rationale: the thin current collectors are a pure energy-density bank (verified inert
w.r.t. plating/SEI, R2-A). The anode-porosity lever is the only admissible direction that moved
the 4C plating metric favorably (R4-L: +0.052 V vs R2-A) by relieving the anode-side electrolyte
potential drop at the metric point; it also lowers cell mass (active-material fraction) and DCR
to 0.199 mOhm, the lowest measured in this case.

## 3. Measured performance (all values from tool outputs under cell/)

| Criterion | Target | Measured | Verdict |
|---|---|---|---|
| Energy density | >= 327.18 Wh/kg | 476.72 Wh/kg | PASS |
| 4C no plating | anode min >= 0 V | -0.3868 V | FAIL |
| SEI 100 cycles | <= 500 nm | 467.6 nm | PASS |
| lowT retention | >= 0.90 | 0.9944 | PASS |
| SEI 500 cycles | <= 550 nm | 811.3 nm | FAIL |

Supporting cell values (calc-energy / protocol outputs): capacity 4.9520 Ah, energy 17.4766 Wh,
mass 36.660 g, area 0.1027 m2, stack thickness 190.8 um, volume 19.60 cm3, midpoint voltage
3.9474 V, DCR 0.199 mOhm, power density 558.7 kW/kg (tool formula V_OC^2/(4 DCR)/mass),
energy density (volumetric) 891.88 Wh/L. 4C charge acceptance at 19.80 A: 0.0461 Ah in 8.4 s
to the 4.2 V abort (~0.9% SOC), T_max 333.2 K.

## 4. Infeasibility evidence (the two failing criteria)

Full sweep (all 14 mechanically evaluated designs; values from log evaluate entries):

| Design | ED Wh/kg | SEI100 nm | SEI500 nm | lowT | anode min V |
|---|---|---|---|---|---|
""" + "\n".join(
    f"| {n} | {ed:.1f} | {s1:.1f} | {s5:.1f} | {lt:.4f} | {am:+.4f} |"
    for n, r, ed, s1, s5, lt, am in COMP
) + """

4C plating: the metric is pinned by (a) the protocol start state - the test first discharges the
cell at 1C to 2.5 V, leaving the anode deeply lithiated; (b) the SPMe surface response at ~195
A/m2; (c) the electrolyte potential drop at the separator interface. The 4C abort is a ~5 s
transport event. Lever outcomes: current collectors (no effect), electrolyte transport up/down
(B worse -0.4494 / K breaks the cell), anode particle size (neutral), electrode loading (D
+0.032), N/P thickness (monotonic WORSE: -0.4643 / -0.4704 / -0.5027), separator (neutral),
thermal cooling (dead, +0.005 - abort too fast for cell-level cooling), cathode particle size
(J worse), anode porosity (best, +0.052). Best measured: -0.3868 V (L); required >= 0 V.
Largest single-lever move across all rounds: 0.052 V.

SEI500: driven by the per-cycle 4.2 V charge-end depth (SEI ec-reaction-limited, isothermal
25 C aging). Best measured: 771.4 nm (C); required <= 550 nm. Admissible levers moved it only
-6.5 nm (C) to +208 nm (H). The levers that would reduce it - SEI kinetics (electrode
modification, locked) and charge cut-off (usage mode, excluded) - are outside the boundary.

## 5. Pareto alternates (documented, not selected)

- A ThinCC: best SEI500 among ED-strong designs (777.9 nm), ED 456.4, plating -0.4386.
- G ThickNeg+ThinSep: best ED 480.0, but SEI500 868.9 and plating -0.4704.
- C SmallNeg: best SEI500 overall (771.4), ED 407.0, plating -0.4368.
- D LowLoad: second-best plating (-0.4067), ED 355.6, SEI500 836.8.

## 6. Honest protocol annotations

- lowT_discharge (tool definition): 1C discharge, ambient 253.15 K (-20 C), lumped thermal from
  the parameter set's 25 C initial temperature; the cell cools during the test (T_max 298.15 K =
  initial). Retention is the ratio of this run's capacity to the same-rate 1C reference.
- Aging: isothermal 25 C, SEI ec-reaction-limited, 1C cycles between the parameter set's own
  voltage limits. PyBaMM "Discharge capacity [A.h]" per cycle is the NET (discharge - charge)
  integral; the climb-then-saturate trajectory is an artifact of the shrinking charge step -
  SEI thickness is the direct criterion used here.
- calc-energy contract formula; electrolyte excluded from mass (parameter set lacks density) -
  the reported ED is an overestimate of a fully-built cell (annotated in calc.xlsx).
- 4C test: 1C discharge to 2.5 V, then 4C charge to 4.2 V at 45 C ambient; plating judged by
  min "Negative electrode surface potential difference at separator interface" >= 0 V
  (plated = min < 0).

## 7. Verdict

NEGATIVE RESULT. Design L is the best-effort deliverable: ED, SEI100 and lowT pass with margin,
and it holds the best 4C plating margin and lowest DCR of all 14 evaluated designs. The 4C-plating
and SEI500 criteria are infeasible within the admissible design space (see final log entry,
escalation layers 1-3). Thresholds were not relaxed.
"""
(DEL / "design_spec.md").write_text(ds, encoding="utf-8")

# ---------------------------------------------------------------- 2. datasheet.md
dsh = f"""# Datasheet - Grid Energy Storage Cell L "AnPorUp" (VBF-{CID}-DSH-003)

Case t2_r1_noceiling | Chen2020 NMC811/graphite SPMe | Best-effort design (negative result case)

## Cell-level specifications (calc-energy output, 1C reference)

| Item | Value |
|---|---|
| Nominal capacity (measured 1C) | 4.9506 Ah |
| 1C discharge capacity (at nominal) | 4.9520 Ah |
| Discharge energy (1C) | 17.4766 Wh |
| Gravimetric energy density | 476.72 Wh/kg |
| Volumetric energy density | 891.88 Wh/L |
| Cell mass (layers, electrolyte excluded) | 36.660 g |
| Stack thickness | 190.8 um |
| Electrode area | 0.1027 m2 |
| Cell volume (stack x area) | 19.60 cm3 |
| Midpoint voltage (1C) | 3.9474 V |
| DC resistance (tool definition) | 0.199 mOhm |
| Power density (tool formula) | 558.7 kW/kg |

## Layer stack

| Layer | Thickness um | Porosity | Areal mass kg/m2 | Mass g |
|---|---|---|---|---|
""" + "\n".join(
    f"| {n} | {t} | {p if p is not None else '-'} | {m:.6f} | {m*0.1027*1000:.2f} |"
    for n, t, p, m in LAYERS
) + f"""
| **Total** | {L['thick_um']} | | | {L['mass_kg']*1000:.2f} |

Electrolyte: excluded from mass and volume (parameter set lacks density - tool note).

## Operating envelope (measured)

| Condition | Result |
|---|---|
| 1C discharge, 25 C | 4.9520 Ah to 2.5 V |
| 1C discharge, -20 C ambient (from 25 C initial) | 4.9242 Ah; retention 0.9944 vs 1C |
| 4C charge, 45 C ambient, after full 1C discharge | 0.0461 Ah in 8.4 s to 4.2 V abort; T_max 333.2 K; min anode surface potential difference -0.3868 V (plating risk: FAIL) |
| 1C cycling, 100 cycles, 25 C | SEI thickness 467.6 nm (<= 500 PASS) |
| 1C cycling, 500 cycles, 25 C | SEI thickness 811.3 nm (<= 550 FAIL) |

## Honest limitations

- 4C fast charge is NOT supported: the 4C charge terminates at 4.2 V after ~8.4 s (~0.9% SOC)
  and the anode surface potential difference goes negative (plating onset) - see DFMEA FM1.
- SEI at 500 cycles exceeds the 550 nm target - see DFMEA FM2.
- Energy density excludes electrolyte mass (overestimate vs a built cell).
"""
(DEL / "datasheet.md").write_text(dsh, encoding="utf-8")

# ---------------------------------------------------------------- 3. bom.xlsx
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
ws.append(["Item", "Layer / part", "Material", "Thickness um", "Porosity",
           "Areal mass kg/m2", "Mass g", "Note"])
for n, t, p, m in LAYERS:
    ws.append([f"{n.split(' ')[0]}", n, n.split('(')[-1].rstrip(')') if '(' in n else n,
               t, p if p is not None else "n/a", m, round(m * 0.1027 * 1000, 2),
               "porosity factor applied" if p is not None else "no porosity factor"])
ws.append(["Total", "Cell stack (5 layers)", "-", L["thick_um"], "-",
           sum(m for *_, m in LAYERS), round(L["mass_kg"] * 1000, 2),
           "electrolyte excluded (parameter set lacks density)"])
ws.append(["", "", "", "", "", "", "", ""])
ws.append(["Design note", "Baseline Chen2020 with: Al CC 16->10 um, Cu CC 12->8 um, anode porosity 0.25->0.35, nominal 4.9506 Ah (measured 1C)"])
wb.save(DEL / "bom.xlsx")

# ---------------------------------------------------------------- 4. calc.xlsx
en = json.loads((CASE / "cell/r4_L_energy.json").read_text(encoding="utf-8-sig"))
wb2 = openpyxl.Workbook()
ws2 = wb2.active
ws2.title = "L_calc_energy"
ws2.append(["Key", "Value"])
for k, v in en.items():
    if k == "layer_kg_m2" and isinstance(v, dict):
        ws2.append([k, json.dumps(v)])
        for lk, lv in v.items():
            ws2.append([f"layer_kg_m2.{lk}", lv])
    else:
        ws2.append([k, v if isinstance(v, (int, float, str, bool)) or v is None else json.dumps(v)])
ws3 = wb2.create_sheet("Comparison")
ws3.append(["Design", "Round", "ED Wh/kg", "SEI100 nm", "SEI500 nm", "lowT ret", "anode min V"])
for n, r, ed, s1, s5, lt, am in COMP:
    ws3.append([n, r, ed, s1, s5, lt, am])
ws4 = wb2.create_sheet("Criteria")
ws4.append(["Metric", "Threshold", "L measured", "Verdict"])
ws4.append(["energy_density_wh_kg", 327.18, 476.72, "PASS"])
ws4.append(["sei_100cyc_nm", 500, 467.6, "PASS"])
ws4.append(["sei_500cyc_nm", 550, 811.3, "FAIL"])
ws4.append(["lowT_retention", 0.9, 0.9944, "PASS"])
ws4.append(["plated (anode min >= 0 V)", False, -0.3868, "FAIL"])
wb2.save(DEL / "calc.xlsx")

# ---------------------------------------------------------------- 5. dvpr.md
dvpr = f"""# Design Verification Plan & Report - Case {CID}

Plan and mechanical results of every protocol run for the selected design L and the round sweep.
All results from tool outputs (cell/*.json) and log-evaluate entries.

## Verification matrix

| # | Criterion | Protocol (bda run-pyamm) | Output file (L) | Measured | Threshold | Verdict |
|---|---|---|---|---|---|---|
| 1 | Energy density | 1C_discharge + calc-energy | cell/r4_L_1c_spme.json + cell/r4_L_energy.json | 476.72 Wh/kg | >= 327.18 | PASS |
| 2 | 4C no plating | 4C_charge_45C --plating | cell/r4_L_4c45.json | anode min -0.3868 V | >= 0 V | FAIL |
| 3 | SEI 100 cyc | aging_1C_100cyc | cell/r4_L_aging100.json | 467.6 nm | <= 500 | PASS |
| 4 | lowT retention | lowT_discharge vs 1C ref | cell/r4_L_lowT.json / r4_L_1c_spme.json | 0.9944 | >= 0.90 | PASS |
| 5 | SEI 500 cyc | aging_1C_100cyc --cycles 500 | cell/r4_L_aging500.json | 811.3 nm | <= 550 | FAIL |

## Sweep coverage (14 designs, all mechanically evaluated)

Rounds: R1 baseline; R2 current collectors / electrolyte transport up / anode particle size /
electrode loading; R3 anode thickness (N/P dose-response) / separator; R4 thermal cooling /
cathode particle size / electrolyte transport down / anode porosity. Every propose round has a
same-round log-evaluate entry (verify-deliverables audit-chain check PASS).

## Per-criterion commentary

- ED: passes for 13/14 designs (327.18+); K fails (238.2, transport-down cell collapse).
- 4C plating: fails for 13/13 non-degenerate designs; best -0.3868 V (L). K's mechanical pass is
  an artifact (nominal collapse -> 4C = 4.64 A = 45 A/m2; charge never reached 4.2 V within the
  experiment window) and K fails ED anyway.
- SEI100: passes for 13/14; H fails (540.0, thick-anode direction).
- SEI500: fails for 13/13 non-degenerate designs (771.4..979.9); K's 68.0 nm is an artifact of
  the crippled cell barely cycling.
- lowT: passes for all 14 (0.9919..1.0000).

## Protocol honesty notes

- lowT_discharge: ambient 253.15 K with lumped thermal from 25 C initial (tool definition);
  T_max 298.15 K in all runs = initial temperature.
- Aging: isothermal 25 C (task text says "1C cycling" without temperature; 25 C standard used,
  protocol default).
- PyBaMM per-cycle "Discharge capacity [A.h]" is the net integral; capacity-trajectory climb is
  an artifact (lithium loss shifts the voltage window) - SEI thickness is the direct criterion.
- calc-energy: contract formula, electrolyte excluded (parameter set lacks density).

## Conclusion

3/5 criteria PASS (ED, SEI100, lowT). 4C-plating and SEI500 FAIL for every design in the
admissible space - negative result, documented with the full sweep as evidence.
"""
(DEL / "dvpr.md").write_text(dvpr, encoding="utf-8")

# ---------------------------------------------------------------- 6. dfmea.md
dfmea = f"""# DFMEA - Design L (Case {CID}, negative-result case)

Ranking: S = severity (1-10), O = occurrence (1-10), D = detection (1-10, 10 = undetectable at design time).

| # | Failure mode | Effect | Cause (tool-diagnosed) | S | O | D | RPN | Current design control | Action / status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 4C charge lithium plating | Dendrite risk, fast-charge function not delivered | 4C test start state (full 1C discharge leaves anode deeply lithiated) + SPMe surface response at ~195 A/m2 + electrolyte potential drop at separator interface; abort is a ~5 s event | 10 | 10 | 2 | 200 | None found in admissible space (10 lever axes swept, best -0.3868 V vs >= 0) | Out of scope: requires material system / electrode modification (locked) or test at far lower effective current |
| 2 | SEI overgrowth at 500 cyc (811.3 nm vs 550) | Impedance growth, lithium loss | Per-cycle 4.2 V charge-end depth drives ec-reaction-limited SEI; isothermal 25 C aging | 8 | 10 | 2 | 160 | None found (levers moved SEI500 only -6.5..+208 nm) | Out of scope: SEI kinetics (electrode modification, locked) or lower charge cut-off (usage mode, excluded) |
| 3 | SEI100 margin erosion with thick anodes | 100-cycle criterion failure (H: 540.0 nm) | Longer charge step per cycle with higher anode headroom | 7 | 3 | 1 | 21 | Thick-anode direction rejected (R3 dose-response) | Design rule: N/P 1.16 baseline; do not raise |
| 4 | Near-zero 4C charge acceptance (0.0461 Ah, 8.4 s, ~0.9% SOC) | Grid fast-charge function not delivered even absent plating | 4.2 V abort driven by cell polarization + cathode surface depletion at 4C | 7 | 10 | 2 | 140 | None (inherent to Chen2020 SPMe at 4C) | Documented as system-level limitation |
| 5 | lowT retention margin erosion with aggressive cooling | Retention drops (I: 0.9919) | h 100 cools the cell toward -20 C during the lowT test | 4 | 3 | 1 | 12 | h = 10 selected (thermal lever dead for plating anyway) | Keep h 10 |
| 6 | 4C test temperature rise (T_max 333.2 K) | Aging acceleration under fast-charge use | Ohmic + polarization heating in the 4C burst | 3 | 8 | 2 | 48 | None needed (below red line; test 45 C ambient) | Monitor only |
| 7 | Energy density overestimate (electrolyte excluded) | Real built-cell ED lower than reported | calc-energy contract formula excludes electrolyte mass (parameter set lacks density) | 4 | 10 | 1 | 40 | Annotated in calc.xlsx / datasheet | Re-calc when electrolyte density available |

Top risks FM1/FM2 are boundary-level (outside the admissible design space of this task) - the
negative-result conclusion of this case rests on them. See final log entry escalation layers.
"""
(DEL / "dfmea.md").write_text(dfmea, encoding="utf-8")

# ---------------------------------------------------------------- 7. delivery_index.md
idx = f"""# Delivery Index - Case {CID}

| # | VBF number | Deliverable | File | Status |
|---|---|---|---|---|
| 1 | VBF-{CID}-DS-001 | Design specification (best-effort design L, infeasibility evidence) | design_spec.md + pdf | Complete |
| 2 | VBF-{CID}-BOM-002 | Bill of materials (5-layer stack, masses) | bom.xlsx + pdf | Complete |
| 3 | VBF-{CID}-DSH-003 | Datasheet (cell-level specs, operating envelope) | datasheet.md + pdf | Complete |
| 4 | VBF-{CID}-CALC-004 | Energy-density calculation + full comparison | calc.xlsx + pdf | Complete |
| 5 | VBF-{CID}-DVPR-005 | Design verification plan & report (5 criteria, 14 designs) | dvpr.md + pdf | Complete |
| 6 | VBF-{CID}-DFMEA-006 | Design FMEA (7 failure modes, ranked) | dfmea.md + pdf | Complete |
| 7 | VBF-{CID}-IDX-007 | This index | delivery_index.md + pdf | Complete |
| 8 | VBF-{CID}-RPT-008 | HTML report (rendered from log.jsonl) | report.html | Complete |

Case summary: NEGATIVE RESULT. Best-effort design L passes energy density (476.72 Wh/kg),
SEI100 (467.6 nm) and lowT retention (0.9944); 4C plating (-0.3868 V vs >= 0) and SEI500
(811.3 nm vs <= 550) are infeasible in the admissible design space (14 designs, 10 lever axes,
4 rounds, all mechanically evaluated). real_compute = false: true DFT/MD endorsement skipped
(endorse entry in log.jsonl).
"""
(DEL / "delivery_index.md").write_text(idx, encoding="utf-8")
print("7 source deliverables written to", DEL)

# ---------------------------------------------------------------- PDF releases
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

st = getSampleStyleSheet()
stH1 = ParagraphStyle("H1x", parent=st["Heading1"], fontSize=15, spaceAfter=8)
stH2 = ParagraphStyle("H2x", parent=st["Heading2"], fontSize=12, spaceAfter=6, spaceBefore=6)
stP = ParagraphStyle("Px", parent=st["BodyText"], fontSize=9, leading=12, spaceAfter=4)
stB = ParagraphStyle("Bx", parent=st["BodyText"], fontSize=9, leading=12, leftIndent=10, spaceAfter=2)

def table_pdf(path, title, header, rows, widths=None, note=None):
    doc = SimpleDocTemplate(str(path), pagesize=A4, topMargin=15 * mm, bottomMargin=15 * mm)
    story = [Paragraph(title, stH1)]
    if note:
        story.append(Paragraph(note, stP))
    data = [header] + rows
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)
    doc.build(story)

def md_pdf(path, blocks):
    doc = SimpleDocTemplate(str(path), pagesize=A4, topMargin=15 * mm, bottomMargin=15 * mm)
    story = []
    for kind, payload in blocks:
        if kind == "h1":
            story.append(Paragraph(payload, stH1))
        elif kind == "h2":
            story.append(Paragraph(payload, stH2))
        elif kind == "p":
            story.append(Paragraph(payload, stP))
        elif kind == "bullets":
            for b in payload:
                story.append(Paragraph("&bull; " + b, stB))
        elif kind == "table":
            hdr, rows, w = payload
            t = Table([hdr] + rows, colWidths=w, repeatRows=1)
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
    doc.build(story)

W = [58, 52, 30, 30, 26, 26]
table_pdf(DEL / "design_spec.pdf", f"Design Specification - Case {CID}",
          ["Design", "Round", "ED Wh/kg", "SEI100 nm", "SEI500 nm", "lowT"],
          [[n, r, f"{ed:.1f}", f"{s1:.1f}", f"{s5:.1f}", f"{lt:.4f}"] for n, r, ed, s1, s5, lt, am in COMP],
          widths=W,
          note="Best-effort design L (AnPorUp). NEGATIVE RESULT: ED/SEI100/lowT PASS; 4C plating and SEI500 FAIL for every design in the admissible space. Full text: design_spec.md.")

table_pdf(DEL / "datasheet.pdf", f"Datasheet - Design L (Case {CID})",
          ["Item", "Value"],
          [["Nominal capacity (measured 1C)", "4.9506 Ah"],
           ["1C discharge capacity", "4.9520 Ah"],
           ["Discharge energy (1C)", "17.4766 Wh"],
           ["Gravimetric energy density", "476.72 Wh/kg"],
           ["Volumetric energy density", "891.88 Wh/L"],
           ["Cell mass (electrolyte excluded)", "36.660 g"],
           ["Stack thickness / area / volume", "190.8 um / 0.1027 m2 / 19.60 cm3"],
           ["Midpoint voltage (1C)", "3.9474 V"],
           ["DC resistance", "0.199 mOhm"],
           ["Power density (tool formula)", "558.7 kW/kg"],
           ["4C charge acceptance", "0.0461 Ah in 8.4 s to 4.2 V abort"],
           ["4C min anode surface potential diff.", "-0.3868 V (plating risk)"],
           ["SEI after 100 / 500 cycles 1C", "467.6 nm / 811.3 nm"],
           ["-20 C retention (tool protocol)", "0.9944"]],
          widths=[210, 300],
          note="Layer stack and limitations: see datasheet.md (electrolyte excluded from mass).")

table_pdf(DEL / "bom.pdf", f"Bill of Materials - Design L (Case {CID})",
          ["Layer", "Thickness um", "Porosity", "Areal mass kg/m2", "Mass g"],
          [[n, t, p if p is not None else "n/a", f"{m:.6f}", f"{m*0.1027*1000:.2f}"] for n, t, p, m in LAYERS]
          + [["Total (electrolyte excluded)", L["thick_um"], "-",
              f"{sum(m for *_, m in LAYERS):.6f}", f"{L['mass_kg']*1000:.2f}"]],
          widths=[170, 60, 50, 90, 60],
          note="Changes vs Chen2020 baseline: Al CC 16->10 um, Cu CC 12->8 um, anode porosity 0.25->0.35, nominal 4.9506 Ah.")

table_pdf(DEL / "calc.pdf", f"Energy-Density Calculation + Comparison (Case {CID})",
          ["Design", "Round", "ED Wh/kg", "SEI100 nm", "SEI500 nm", "lowT", "anode min V"],
          [[n, r, f"{ed:.1f}", f"{s1:.1f}", f"{s5:.1f}", f"{lt:.4f}", f"{am:+.4f}"] for n, r, ed, s1, s5, lt, am in COMP],
          widths=[86, 28, 42, 38, 38, 32, 40],
          note="calc-energy contract formula: ED = integral(V x I_1C)dt / sum(layer thickness x (1-porosity) x density x area); electrolyte excluded (parameter set lacks density). Selected design L highlighted in calc.xlsx.")

table_pdf(DEL / "dvpr.pdf", f"Design Verification Plan & Report (Case {CID})",
          ["Criterion", "Protocol", "Measured (L)", "Threshold", "Verdict"],
          [["Energy density", "1C_discharge + calc-energy", "476.72 Wh/kg", ">= 327.18", "PASS"],
           ["4C no plating", "4C_charge_45C --plating", "-0.3868 V", ">= 0 V", "FAIL"],
           ["SEI 100 cyc", "aging_1C_100cyc", "467.6 nm", "<= 500", "PASS"],
           ["lowT retention", "lowT_discharge vs 1C ref", "0.9944", ">= 0.90", "PASS"],
           ["SEI 500 cyc", "aging_1C_100cyc --cycles 500", "811.3 nm", "<= 550", "FAIL"]],
          widths=[60, 90, 70, 50, 34],
          note="Sweep: 14 designs, 4 rounds, 10 lever axes, every round mechanically evaluated (log-evaluate). Protocol honesty notes in dvpr.md.")

table_pdf(DEL / "dfmea.pdf", f"DFMEA - Design L (Case {CID})",
          ["FM", "Failure mode", "Effect / cause", "S O D", "RPN", "Status"],
          [["1", "4C lithium plating", "Test start state + SPMe surface response + electrolyte drop; ~5 s abort", "10 10 2", 200, "Out of admissible scope"],
           ["2", "SEI500 overgrowth (811 vs 550)", "Per-cycle 4.2 V charge-end depth", "8 10 2", 160, "Out of admissible scope"],
           ["3", "SEI100 erosion (thick anodes)", "H failed at 540.0 nm (R3)", "7 3 1", 21, "Direction rejected"],
           ["4", "Near-zero 4C acceptance", "0.0461 Ah in 8.4 s (~0.9% SOC)", "7 10 2", 140, "System-level limitation"],
           ["5", "lowT margin vs cooling", "h 100 -> 0.9919 (I)", "4 3 1", 12, "Keep h 10"],
           ["6", "4C thermal rise 333.2 K", "Ohmic heating in 4C burst", "3 8 2", 48, "Monitor"],
           ["7", "ED overestimate (no electrolyte)", "Contract formula excludes electrolyte", "4 10 1", 40, "Annotated"]],
          widths=[16, 80, 150, 30, 18, 56],
          note="Top risks FM1/FM2 are boundary-level (material system / electrode modification locked, escalation OFF).")

table_pdf(DEL / "delivery_index.pdf", f"Delivery Index - Case {CID}",
          ["#", "VBF number", "Deliverable", "Status"],
          [[1, f"VBF-{CID}-DS-001", "Design specification", "Complete"],
           [2, f"VBF-{CID}-BOM-002", "Bill of materials", "Complete"],
           [3, f"VBF-{CID}-DSH-003", "Datasheet", "Complete"],
           [4, f"VBF-{CID}-CALC-004", "Energy-density calculation + comparison", "Complete"],
           [5, f"VBF-{CID}-DVPR-005", "Design verification plan & report", "Complete"],
           [6, f"VBF-{CID}-DFMEA-006", "Design FMEA", "Complete"],
           [7, f"VBF-{CID}-IDX-007", "This index", "Complete"],
           [8, f"VBF-{CID}-RPT-008", "HTML report (report.html)", "Complete"]],
          widths=[18, 130, 180, 40],
          note="Case summary: NEGATIVE RESULT - best-effort design L passes ED/SEI100/lowT; 4C plating and SEI500 infeasible in the admissible space.")

print("7 PDF releases written")
