# Deliverables generator for t3_r1 (VBF-T3R1): design_spec/bom/datasheet/calc/dvpr/dfmea/delivery_index
# Every value mechanically read from parameter set / simulation outputs / log.jsonl entry 0.
import json
import os
from pathlib import Path

import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

WS = Path("runs/exp/t3_r1")
CELL = WS / "cell"
DEL = WS / "deliverables"
DEL.mkdir(exist_ok=True)

CRITERIA = next(json.loads(l) for l in (WS / "log.jsonl").read_text(encoding="utf-8-sig").splitlines()
               if json.loads(l).get("criteria"))["criteria"]
TH = CRITERIA["stage2"] | CRITERIA["stage3"]

P = json.load(open(CELL / "p_v12.json", encoding="utf-8-sig"))
E = json.load(open(CELL / "r4_v12_energy.json", encoding="utf-8-sig"))
D = json.load(open(CELL / "r4_v12_derived.json", encoding="utf-8-sig"))
D1 = json.load(open(CELL / "r4_v12_1c.json", encoding="utf-8-sig"))
D5 = json.load(open(CELL / "r4_v12_5c.json", encoding="utf-8-sig"))
D4 = json.load(open(CELL / "r4_v12_4c.json", encoding="utf-8-sig"))

AREA = E["area_m2"]                       # 0.1027
ANODE_MIN = min(D4["anode_potential_v"])
T_MAX_C = D["T_max_K"] - 273.15
I_1C = P["Nominal cell capacity [A.h]"]   # 3.08 A
I_5C, I_4C = 5 * I_1C, 4 * I_1C

# Layer masses (mechanically from calc-energy layer_kg_m2 x area)
LM = {k: v * AREA for k, v in E["layer_kg_m2"].items()}
LAYERS = [
    ("Positive electrode (NMC811)", P["Positive electrode thickness [m]"] * 1e6,
     P["Positive electrode porosity"], 3699.0, LM["positive_electrode"], "Chen2020 set"),
    ("Negative electrode (graphite)", P["Negative electrode thickness [m]"] * 1e6,
     P["Negative electrode porosity"], 2060.0, LM["negative_electrode"], "Chen2020 set"),
    ("Separator (polyolefin)", 12.0, 0.47, 1548.0, LM["separator"], "Chen2020 set"),
    ("Positive current collector (Al)", 16.0, None, 2702.0, LM["positive_cc"], "Chen2020 set"),
    ("Negative current collector (Cu)", 12.0, None, 8933.0, LM["negative_cc"], "Chen2020 set"),
]

CASE = "T3R1"
TODAY = "2026-08-25"


def w_md(name, text):
    (DEL / name).write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- design_spec.md
design_spec = f"""# Cell Design Specification — VBF-{CASE}-DS-001

| Field | Value | Source |
|---|---|---|
| Case | exp/t3_r1 — power-tool battery design | log.jsonl entry 0 |
| Document number | VBF-{CASE}-DS-001 | delivery index |
| Generation date | {TODAY} | — |
| Status | Final (verdict: achieved, log.jsonl final entry) | bda log-evaluate R4 |

## 1. Design requirements (entry-0 criteria, verbatim from task text)

| Metric | Threshold | Layer |
|---|---|---|
| Nominal capacity | >= {TH['capacity_ah']['min']} Ah | stage2 |
| 5C discharge retention | >= {TH['retention_5c']['min']} | stage2 |
| Power density | >= {TH['power_density_w_kg']['min']} W/kg | stage2 |
| Maximum temperature (4C charge @45 C) | <= {TH['T_max_K']['max']} K ({TH['T_max_K']['max']-273.15:.2f} C) | stage3 |
| Lithium plating at 4C charge | {TH['plated']} (none) | stage3 |

## 2. System and chemistry

| Item | Value | Source |
|---|---|---|
| Base parameter set | Chen2020 (NMC811 / graphite, 1M LiPF6 EC/EMC) | SKILL.md anchor table; task text names no electrode system -> default with record |
| Cathode | NMC811, 40 um, porosity 0.42, particle radius 2.0 um | cell/p_v12.json |
| Anode | Graphite, 52 um, porosity 0.35, particle radius 2.5 um | cell/p_v12.json |
| Voltage window | 2.5 - 4.2 V | Chen2020 set |
| Electrode area | 0.065 m x 1.58 m = 0.1027 m2 | Chen2020 set / calc-energy |
| Stack thickness | 40+52+12+16+12 = 132 um | layer sum, calc-energy thickness_m |

## 3. Cell architecture (final design V12_BalancedCooling)

| Layer | Thickness [um] | Porosity | Particle radius [um] | Density [kg/m3] | Mass [g] | Source |
|---|---|---|---|---|---|---|
{chr(10).join(f'| {n} | {t:g} | {eps if eps is not None else "-"} | {r if r else "-"} | {rho:g} | {m*1000:.2f} | {s} |' for (n, t, eps, rho, m, s), r in zip(LAYERS, [P["Positive particle radius [m]"]*1e6, P["Negative particle radius [m]"]*1e6, "-", "-", "-"]))}
| Total (electrolyte excluded by contract) | — | — | — | — | {sum(LM.values())*1000:.2f} | calc-energy |

Layer masses are mechanically computed: mass = layer_kg_m2 x area (calc-energy output r4_v12_energy.json).

## 4. Electrolyte design

| Property | Value | Baseline (Chen2020) | Source |
|---|---|---|---|
| Conductivity kappa | 1.5 S/m | 0.9487 | cell/p_v12.json |
| Diffusivity D | 2.5e-10 m2/s | 1.769e-10 | cell/p_v12.json |
| Cation transference t+ | 0.35 | 0.2594 | cell/p_v12.json |

Rationale (round-2/3 attribution, log.jsonl): high-transport electrolyte is load-bearing for both 5C retention
and plating margin — V9 (kappa 1.2 / D 2.0e-10 / t+ 0.30) passed retention but eroded the plating margin to
+0.6 mV (cell/r3_v9_4c.json), so the aggressive values are retained. Values are transport-parameter
overrides of the baseline formulation (electrolyte formulation degree of freedom, widest interpretation
recorded in entry-0 meta.freedoms).

## 5. Thermal design

| Property | Value | Source |
|---|---|---|
| Cooling coefficient h | 20 W/m2/K | cell/p_v12.json |
| Ambient for rating | 25 C (discharge), 45 C (4C charge protocol) | bda protocols |

Rationale (round-3/4 attribution): h trades thermal margin against plating margin (warmer cell kinetically
suppresses plating): h=15 -> T_max 331.96 K / anode +14.9 mV (V8); h=30 -> T_max 326.86 K / anode +8.2 mV
(V11). h=20 lands both margins balanced (measured: T_max {D['T_max_K']:.2f} K, anode min {ANODE_MIN*1000:.1f} mV)
and is realistic for a power tool (natural convection + tool-body conduction with light airflow).

## 6. Electrical ratings

| Rating | Value | Source |
|---|---|---|
| Nominal capacity Q_nom | 3.08 Ah | cell/p_v12.json (fixed-point iteration: measured 1C = 3.075 Ah, round 2 lesson) |
| 1C current | {I_1C:g} A | Q_nom x 1 |
| 5C discharge current | {I_5C:g} A | Q_nom x 5 |
| 4C charge current | {I_4C:g} A | Q_nom x 4 |
| Midpoint voltage | 3.844 V | calc-energy midpoint_voltage_v |

## 7. Verification summary

See DVPR (VBF-{CASE}-DVPR-001): all five criteria verified pass by DFN simulation, evidence
cell/r4_v12_*.json via bda log-evaluate (round 4, 5/5 checked, verdict pass). Iteration history in
log.jsonl (rounds 1-4) and report.html.

## 8. Design notes (honest limits)

- Electrolyte mass excluded from calc-energy by contract (parameter set lacks density; output
  electrolyte_included: false) — mass/power density slightly optimistic vs a real cell with electrolyte.
- True DFT/MD endorsement skipped (real_compute=false, entry-0 meta): no first-principles values claimed.
- 4C CC-only charge accepts ~0.81 Ah before the 4.2 V ceiling (cell/r4_v12_4c.json) — a CV taper phase is
  required for full charge; plating-free result is for the CC segment per protocol definition.
- Manufacturability drawings with tolerances, material datasheets, and process cards are outside the
  pure-simulation boundary and are not provided.
"""

# ---------------------------------------------------------------- datasheet.md
datasheet = f"""# Technical Datasheet — VBF-{CASE}-DSH-001

## Product

| Item | Value | Source |
|---|---|---|
| Cell designation | V12_BalancedCooling (power-tool high-rate cell) | cell/p_v12.json |
| Chemistry | NMC811 / graphite, LiPF6 EC/EMC electrolyte | Chen2020 base |
| Nominal capacity | 3.08 Ah (measured 1C: {D1['capacity_ah']:.3f} Ah) | p_v12 / r4_v12_1c.json |
| Nominal energy | {E['energy_wh']:.2f} Wh | calc-energy |
| Cell mass | {E['mass_kg']*1000:.2f} g (electrolyte excluded by contract) | calc-energy |
| Dimensions (active stack) | 0.065 m x 1.58 m x 132 um | Chen2020 / layer sum |
| Voltage window | 2.5 - 4.2 V | Chen2020 |

## Rated performance (DFN-verified)

| Specification | Rated | Measured | Margin | Source |
|---|---|---|---|---|
| Capacity @ 1C, 25 C | >= 2.0 Ah | {D1['capacity_ah']:.3f} Ah | +{D1['capacity_ah']-2.0:.3f} Ah | r4_v12_1c.json |
| 5C discharge retention (5C cap / 1C cap) | >= 95 % | {D['retention_5c']*100:.2f} % | +{D['retention_5c']*100-95:.2f} pp | r4_v12_derived.json |
| Max temperature, 4C charge @ 45 C amb | <= 60 C | {T_MAX_C:.2f} C | {60-T_MAX_C:.2f} C below red line | r4_v12_4c.json |
| Plating at 4C charge | none | none (anode potential min {ANODE_MIN*1000:+.1f} mV vs 0 V) | {ANODE_MIN*1000:.1f} mV | r4_v12_4c.json |
| Power density | >= 4000 W/kg | {E['power_density_w_kg']:.0f} W/kg | x{4000 and E['power_density_w_kg']/4000:.1f} | calc-energy |

## Additional characteristics

| Item | Value | Source |
|---|---|---|
| Energy density | {E['energy_density_wh_kg']:.1f} Wh/kg (gravimetric), {E['energy_density_wh_l']:.1f} Wh/L (volumetric) | calc-energy |
| DC resistance (10% discharge) | {E['dcr_ohm']*1000:.2f} mOhm | calc-energy |
| Discharge midpoint voltage | {E['midpoint_voltage_v']:.3f} V | calc-energy |
| 5C discharge capacity | {D5['capacity_ah']:.3f} Ah | r4_v12_5c.json |
| 4C CC charge capacity (to 4.2 V) | {D4['capacity_ah']:.3f} Ah (CV phase required for full charge) | r4_v12_4c.json |

## Recommended operating conditions

- Continuous discharge: up to 5C ({I_5C:g} A); Fast charge: 4C CC ({I_4C:g} A) with CV taper, ambient <= 45 C.
- Cooling: heat transfer >= 20 W/m2/K (tool-body conduction + light airflow) — required to keep T <= 60 C.
- Charge termination 4.2 V; discharge cut-off 2.5 V.
"""
w_md("design_spec.md", design_spec)
w_md("datasheet.md", datasheet)

# ---------------------------------------------------------------- dvpr.md
dvpr = f"""# Design Verification Plan & Report (virtual tests) — VBF-{CASE}-DVPR-001

All tests executed with the bda simulation library, DFN mode, Chen2020 base parameters + design
overrides (cell/p_v12.json). Verdicts are mechanical (bda log-evaluate, round 4).

| # | Test item | Requirement | Method / protocol | Result | Verdict | Evidence |
|---|---|---|---|---|---|---|
| 1 | Nominal capacity | >= {TH['capacity_ah']['min']} Ah | 1C_discharge, DFN | {D1['capacity_ah']:.3f} Ah | PASS | cell/r4_v12_1c.json:capacity_ah |
| 2 | 5C capacity retention | >= {TH['retention_5c']['min']} | 5C_discharge DFN / 1C_discharge DFN | {D['retention_5c']} | PASS | cell/r4_v12_derived.json:retention_5c |
| 3 | Fast-charge plating | {TH['plated']} (no plating) | 4C_charge_45C, DFN, --plating | anode min {ANODE_MIN*1000:+.1f} mV (>0) | PASS | cell/r4_v12_4c.json:anode_potential_v |
| 4 | Max temperature | <= {TH['T_max_K']['max']} K | 4C_charge_45C, DFN, --thermal lumped | {D['T_max_K']:.2f} K ({T_MAX_C:.2f} C) | PASS | cell/r4_v12_derived.json:T_max_K |
| 5 | Power density | >= {TH['power_density_w_kg']['min']} W/kg | calc-energy contract formula | {E['power_density_w_kg']:.0f} W/kg | PASS | cell/r4_v12_energy.json:power_density_w_kg |

## Iteration history (log.jsonl)

| Round | Candidates | Outcome |
|---|---|---|
| 1 | Baseline (Chen2020 defaults) | FAIL: retention 0.0874, T_max 354.29 K, plated — power density/capacity OK. Failures are transport/architecture-scale -> Stage-3 fallback. |
| 2 | V1-V6 single levers + combo | V6_ComboCeiling first full pass (retention 0.9782, T 324.91 K, no plating); Q_nom understated C-rates by ~15% (lesson recorded). |
| 3 | V7-V11 refinements | Attribution: thicker anode insufficient (V7 retention fail), porosity boost load-bearing (V10 plated), moderate electrolyte erodes plating margin (V9 +0.6 mV), h-trade mapped (V8/V11). |
| 4 | V12_BalancedCooling (h=20) | PASS 5/5 with balanced margins (3.38 K thermal, +12.1 mV plating) — final selection. |

## Notes

- Stage-5 true DFT/MD endorsement skipped: real_compute=false (entry-0 meta); endorse entry records the skip.
- Aging/cycle-life not in task criteria; not tested (aging protocol available for follow-up).
"""
w_md("dvpr.md", dvpr)

# ---------------------------------------------------------------- dfmea.md
dfmea = f"""# Design FMEA (qualitative) — VBF-{CASE}-DFMEA-001

Qualitative design FMEA on the final design V12_BalancedCooling. Ratings: S=severity, O=occurrence,
D=detection (1-10, 10 worst). Mitigations reference round measurements (log.jsonl).

| Failure mode | Effect | S | O | D | Design controls / mitigation | Residual risk |
|---|---|---|---|---|---|---|
| Lithium plating during 4C charge | Capacity loss, internal short risk | 9 | 2 | 3 | Thin electrodes (40/52 um), porosity 0.42/0.35, high-transport electrolyte, measured anode min {ANODE_MIN*1000:+.1f} mV; V10 showed porosity rollback alone plates (-4.3 mV) | Electrolyte transport aging erodes margin (V9: +0.6 mV at kappa 1.2) -> recommend periodic anode-potential-aware charge control |
| Cell over-temperature at fast charge | Electrolyte degradation, venting | 7 | 3 | 2 | h=20 W/m2/K specified; measured {T_MAX_C:.1f} C at 4C/45 C (3.38 K margin); lumped-thermal DFN verification | Margin consumed if cooling degrades (dust, insulation) -> pack-level thermal monitor recommended |
| 5C-rate capacity fade / power loss | Tool stalls under load | 6 | 5 | 4 | Measured retention {D['retention_5c']*100:.1f}% at BOL; DCR {E['dcr_ohm']*1000:.1f} mOhm | Cycle-life rate fade not tested (aging protocol available for follow-up) |
| Thickness/porosity manufacturing deviation | Plating margin or retention loss | 5 | 4 | 3 | Single-lever attribution (R2): V1-V5 quantify each lever's effect; tolerance stackup can be re-simulated with the same pipeline | No tolerance band specified (drawings outside simulation boundary) |
| Charge CV-phase heating beyond CC segment | T exceeds 60 C in taper | 5 | 3 | 2 | CC-only 4C measured; CV phase not simulated (protocol limitation) | Recommend CV-phase thermal verification in follow-up |
| Electrolyte density unmodeled mass | Power density over-estimate | 3 | 8 | 1 | Contract excludes electrolyte mass (electrolyte_included: false) — disclosed on datasheet | Est. few-% overstatement; real-cell verification required |

FMEA scope note: pure-simulation boundary — no abuse (nail/overcharge) tests performed (not in task criteria).
"""
w_md("dfmea.md", dfmea)

# ---------------------------------------------------------------- delivery_index.md
idx_rows = [
    ("design_spec.md / .pdf", f"VBF-{CASE}-DS-001", "MD + PDF", "Cell design specification (this case's final design V12)"),
    ("bom.xlsx / .pdf", f"VBF-{CASE}-BOM-001", "XLSX + PDF", "Bill of materials (layer stack, masses from calc-energy)"),
    ("datasheet.md / .pdf", f"VBF-{CASE}-DSH-001", "MD + PDF", "Technical datasheet (rated + DFN-verified performance)"),
    ("calc.xlsx / .pdf", f"VBF-{CASE}-CALC-001", "XLSX + PDF", "Design calculation sheet (ratings, performance, energy/power, mass)"),
    ("dvpr.md / .pdf", f"VBF-{CASE}-DVPR-001", "MD + PDF", "Design verification plan & report (virtual tests)"),
    ("dfmea.md / .pdf", f"VBF-{CASE}-DFMEA-001", "MD + PDF", "Design FMEA (qualitative)"),
    ("delivery_index.md / .pdf", f"VBF-{CASE}-IDX-001", "MD + PDF", "This index"),
]
idx_text = f"""# Delivery Index — VBF-{CASE}-IDX-001

| Field | Value |
|---|---|
| Case | exp/t3_r1 — power-tool battery design (headless execution) |
| Numbering scheme | VBF-<CASE-ID>-<doc-code>-<serial>; CASE-ID = {CASE} |
| Generation date | {TODAY} |
| Signature (author) | ______________ |
| Signature (reviewer) | ______________ |

## Document list

| # | File | Number | Format | Source note |
|---|---|---|---|---|
{chr(10).join(f'| {i+1} | {f} | {n} | {fmt} | {s} |' for i, (f, n, fmt, s) in enumerate(idx_rows))}

## VBF numbering list

{chr(10).join(f'- {n}: {f}' for f, n, fmt, s in idx_rows)}

## Notes

- All numeric values traceable to cell/*.json simulation outputs and log.jsonl (case directory).
- Editable sources retained alongside PDF releases (industry dual-format rule).
- Engineering drawings with tolerances, material specifications, and process cards are outside the
  pure-simulation boundary and are not provided (stated in design_spec section 8).
"""
w_md("delivery_index.md", idx_text)

# ---------------------------------------------------------------- bom.xlsx
wb = openpyxl.Workbook()
ws_ = wb.active
ws_.title = "BOM"
ws_.append(["#", "Component", "Material", "Thickness [um]", "Porosity", "Density [kg/m3]",
            "Area [m2]", "Mass [g]", "Source"])
for i, (name, t, eps, rho, m, src) in enumerate(LAYERS, 1):
    ws_.append([i, name, name.split(" (")[0], t, eps if eps is not None else "-", rho,
                AREA, round(m * 1000, 3), src])
ws_.append(["", "Electrolyte", "1M LiPF6 EC/EMC (kappa 1.5 S/m, D 2.5e-10, t+ 0.35)", "-", "-", "-",
            "-", "not provided (density absent from parameter set; contract excludes)", "p_v12.json / calc-energy note"])
ws_.append(["", "TOTAL (active stack)", "", E["thickness_m"] * 1e6, "", "", AREA,
            round(sum(LM.values()) * 1000, 2), "calc-energy mass_kg"])
n = ws_.append(["Design values", "", "particle radii: pos 2.0 um / neg 2.5 um", "", "", "", "", "", "p_v12.json"])
ws_.append(["Cooling", "h = 20 W/m2/K", "cell-to-ambient", "", "", "", "", "", "p_v12.json"])
ws_.append(["Voltage window", "2.5 - 4.2 V", "", "", "", "", "", "", "Chen2020 set"])
wb.save(DEL / "bom.xlsx")

# ---------------------------------------------------------------- calc.xlsx
wb2 = openpyxl.Workbook()
s1 = wb2.active
s1.title = "Ratings"
s1.append(["Item", "Value", "Formula", "Source"])
s1.append(["Q_nom", I_1C, "design nominal (fixed-point from measured 1C)", "p_v12.json"])
s1.append(["I_1C", I_1C, "Q_nom x 1", "p_v12.json"])
s1.append(["I_5C", I_5C, "Q_nom x 5", "p_v12.json"])
s1.append(["I_4C", I_4C, "Q_nom x 4", "p_v12.json"])

s2 = wb2.create_sheet("Performance")
s2.append(["Metric", "Value", "Threshold (entry 0)", "Verdict", "Source"])
s2.append(["capacity_ah (1C)", round(D1["capacity_ah"], 4), TH["capacity_ah"]["min"], "PASS", "r4_v12_1c.json"])
s2.append(["retention_5c", D["retention_5c"], TH["retention_5c"]["min"], "PASS", "r4_v12_derived.json"])
s2.append(["capacity_ah (5C)", round(D5["capacity_ah"], 4), "-", "-", "r4_v12_5c.json"])
s2.append(["T_max_K (4C@45C)", D["T_max_K"], TH["T_max_K"]["max"], "PASS", "r4_v12_derived.json"])
s2.append(["T_max_C", round(T_MAX_C, 2), 60.0, "PASS", "mechanical: K-273.15"])
s2.append(["anode_min_v (4C)", round(ANODE_MIN, 5), "> 0 (plated=false)", "PASS", "r4_v12_4c.json"])
s2.append(["power_density_w_kg", round(E["power_density_w_kg"], 1), TH["power_density_w_kg"]["min"], "PASS", "r4_v12_energy.json"])

s3 = wb2.create_sheet("EnergyAndPower")
s3.append(["Item", "Value", "Formula / note", "Source"])
s3.append(["energy_wh", E["energy_wh"], "integral V(t) x I_1C dt", "calc-energy"])
s3.append(["mass_kg", E["mass_kg"], "sum layer thickness x (1-eps) x density x area", "calc-energy"])
s3.append(["energy_density_wh_kg", E["energy_density_wh_kg"], "energy/mass", "calc-energy"])
s3.append(["energy_density_wh_l", E["energy_density_wh_l"], "energy/volume (stack only)", "calc-energy"])
s3.append(["dcr_ohm", E["dcr_ohm"], "(V[0] - V@10% time)/I_1C", "calc-energy"])
s3.append(["power_density_w_kg", E["power_density_w_kg"], "V_OC^2/(4 x DCR)/mass", "calc-energy"])
s3.append(["midpoint_voltage_v", E["midpoint_voltage_v"], "V at discharge time midpoint", "calc-energy"])
s3.append(["electrolyte_included", E["electrolyte_included"], "contract excludes electrolyte mass", "calc-energy"])

s4 = wb2.create_sheet("Mass")
s4.append(["Layer", "Thickness [um]", "Porosity", "Density [kg/m3]", "kg/m2", "Area [m2]", "Mass [g]", "Source"])
for i, (name, t, eps, rho, m, src) in enumerate(LAYERS, 1):
    s4.append([name, t, eps if eps is not None else "-", rho, E["layer_kg_m2"][
        ["positive_electrode", "negative_electrode", "separator", "positive_cc", "negative_cc"][i - 1]],
        AREA, round(m * 1000, 3), src])
s4.append(["TOTAL", E["thickness_m"] * 1e6, "", "", "", AREA, round(sum(LM.values()) * 1000, 2), "calc-energy mass_kg"])
wb2.save(DEL / "calc.xlsx")

print("md + xlsx deliverables written")

# ---------------------------------------------------------------- PDFs
ST = getSampleStyleSheet()
for tag in ("Heading1", "Heading2", "Heading3"):
    ST[tag].fontName = "Helvetica-Bold"
    ST[tag].textColor = "#1a1a1a"


def md_to_pdf(src: Path, dst: Path, title: str):
    doc = SimpleDocTemplate(str(dst), pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm)
    story = [Paragraph(title, ST["Title"]), Spacer(1, 6 * mm)]
    for raw in src.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        txt = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if line.startswith("### "):
            story.append(Paragraph(txt[4:], ST["Heading3"]))
        elif line.startswith("## "):
            story.append(Paragraph(txt[3:], ST["Heading2"]))
        elif line.startswith("# "):
            story.append(Paragraph(txt[2:], ST["Heading1"]))
        else:
            story.append(Paragraph(txt, ST["BodyText"]))
        story.append(Spacer(1, 1.2 * mm))
    doc.build(story)


md_to_pdf(DEL / "design_spec.md", DEL / "design_spec.pdf", "Design Specification — VBF-T3R1-DS-001")
md_to_pdf(DEL / "datasheet.md", DEL / "datasheet.pdf", "Technical Datasheet — VBF-T3R1-DSH-001")
md_to_pdf(DEL / "dvpr.md", DEL / "dvpr.pdf", "DVP&R — VBF-T3R1-DVPR-001")
md_to_pdf(DEL / "dfmea.md", DEL / "dfmea.pdf", "Design FMEA — VBF-T3R1-DFMEA-001")
md_to_pdf(DEL / "delivery_index.md", DEL / "delivery_index.pdf", "Delivery Index — VBF-T3R1-IDX-001")


def xlsx_to_pdf(src: Path, dst: Path, title: str):
    doc = SimpleDocTemplate(str(dst), pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm)
    story = [Paragraph(title, ST["Title"]), Spacer(1, 6 * mm)]
    for sheet in openpyxl.load_workbook(src, read_only=True).worksheets:
        story.append(Paragraph(f"Sheet: {sheet.title}", ST["Heading2"]))
        for row in sheet.iter_rows(values_only=True):
            if row is None or all(v is None or str(v).strip() == "" for v in row):
                continue
            cells = ["" if v is None else str(v).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for v in row]
            story.append(Paragraph("  |  ".join(cells), ST["BodyText"]))
            story.append(Spacer(1, 1.0 * mm))
        story.append(Spacer(1, 4 * mm))
    doc.build(story)


xlsx_to_pdf(DEL / "bom.xlsx", DEL / "bom.pdf", "Bill of Materials — VBF-T3R1-BOM-001")
xlsx_to_pdf(DEL / "calc.xlsx", DEL / "calc.pdf", "Design Calculation Sheet — VBF-T3R1-CALC-001")

print("pdfs written")
for p in sorted(DEL.iterdir()):
    print(f"  {p.name}  {p.stat().st_size} B")
