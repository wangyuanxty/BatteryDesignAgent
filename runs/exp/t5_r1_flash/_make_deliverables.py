# -*- coding: utf-8 -*-
"""Generate all closing deliverables for case t5_r1_flash (LNMO-R6 final design).
All values pulled mechanically from tool output JSONs; derived values computed here
with documented formulas. Sources annotated per line."""
import json, os, math
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.abspath(__file__))
DLV = os.path.join(ROOT, "deliverables")
os.makedirs(DLV, exist_ok=True)
CASE = "t5_r1_flash"
PREFIX = "VBF-T5R1FLASH"

def j(*p):
    return json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))

# ---------------------------------------------------------------- tool outputs
E   = j("cell", "r9_lnmo_r6_energy_dfn.json")      # calc-energy on DFN 1C (conclusion grade)
S   = j("cell", "r9_lnmo_r6_4c45_dfn.json")         # 4C charge 45C DFN (safety)
C1  = j("cell", "r9_lnmo_r6_1c_dfn.json")           # 1C discharge DFN
E_SP= j("cell", "r9_lnmo_r6_energy.json")           # calc-energy on SPMe 1C (cross-check)
P6  = j("entries", "params_lnmo_r6.json")           # final design parameters

cap      = E["capacity_ah"]            # 8.2629 Ah
energy   = E["energy_wh"]              # 35.162 Wh
mass     = E["mass_kg"]                # 0.058813 kg
ed       = E["energy_density_wh_kg"]   # 597.86 Wh/kg
edv      = E["energy_density_wh_l"]    # 1141.2 Wh/L
midv     = E["midpoint_voltage_v"]     # 4.235 V
dcr      = E["dcr_ohm"]                # ohm
area     = E["area_m2"]                # 0.1027 m2
thick    = E["thickness_m"]            # 300 um
layers   = E["layer_kg_m2"]
power_w  = E["power_density_w_kg"]     # W/kg

tmax     = S["T_max_K"]
tmax_c   = tmax - 273.15
anode_min= min(S["anode_potential_v"])
anode_min_mv = anode_min*1000.0
charge_ah= S["capacity_ah"]            # 2.0 Ah (protocol cap)
model4c  = S["model_used"]

# ---------------------------------------------------------------- derived
g = 1000.0
m_pos  = layers["positive_electrode"] * area * g   # g
m_neg  = layers["negative_electrode"] * area * g
m_al   = layers["positive_cc"] * area * g
m_cu   = layers["negative_cc"] * area * g
m_sep  = layers["separator"] * area * g
m_tot  = m_pos + m_neg + m_al + m_cu + m_sep

Lp, ep = P6["Positive electrode thickness [m]"], P6["Positive electrode porosity"]
Ln, en = P6["Negative electrode thickness [m]"], P6["Negative electrode porosity"]
Ls, es = P6["Separator thickness [m]"], P6["Separator porosity"]
pore_v_m3 = area * (Lp*ep + Ln*en + Ls*es)
pore_ml   = pore_v_m3 * 1e6            # mL
elec_g    = pore_ml * 1.2              # electrolyte mass @ 1.2 g/cm3 (lit, annotated)
m_with_elec = m_tot + elec_g
ed_inc_elec = energy / (m_with_elec/1000.0)

# N/P (active-material theoretical basis, formula documented)
rho_neg, a_neg, q_neg = 1657.0, 0.75, 372.0     # Chen2020 defaults + graphite theoretical
rho_pos, a_pos, q_pos = 4400.0, 0.665, 146.6    # LNMO.json + LNMO theoretical
np_ratio = (layers["negative_electrode"]*a_neg*q_neg) / (layers["positive_electrode"]*a_pos*q_pos)

comp_pos = rho_pos*(1-ep)/1000.0    # g/cm3
comp_neg = rho_neg*(1-en)/1000.0

i4c = 4*4.5                      # A (nominal capacity 4.5 Ah from LNMO.json)
i4c_am2 = i4c/area               # A/m2

num = {
 "case": CASE, "prefix": PREFIX,
 "cap": cap, "energy": energy, "mass_g": mass*1000, "ed": ed, "edv": edv,
 "midv": midv, "dcr_mohm": dcr*1000, "thick_um": thick*1e6, "area": area,
 "m_pos": m_pos, "m_neg": m_neg, "m_al": m_al, "m_cu": m_cu, "m_sep": m_sep,
 "m_tot": m_tot, "pore_ml": pore_ml, "elec_g": elec_g, "m_with_elec": m_with_elec,
 "ed_inc_elec": ed_inc_elec,
 "tmax": tmax, "tmax_c": tmax_c, "anode_min_mv": anode_min*1000, "charge_ah": charge_ah,
 "np": np_ratio, "comp_pos": comp_pos, "comp_neg": comp_neg,
 "i4c": i4c, "i4c_am2": i4c_am2, "power_w": power_w,
 "a_pos_frac": layers["positive_electrode"]*1000, "a_neg_frac": layers["negative_electrode"]*1000,
 "a_al_frac": layers["positive_cc"]*1000, "a_cu_frac": layers["negative_cc"]*1000,
 "a_sep_frac": layers["separator"]*1000,
}
def f(x, nd=2):
    return f"{x:.{nd}f}"

# standalone aliases used by markdown bodies
dcr_mohm   = dcr*1000.0
ed_inc_elec = ed_inc_elec  # noqa: from above
m_with_elec = m_with_elec  # noqa

# ---------------------------------------------------------------- markdown bodies
design_spec_md = f"""# Cell Design Specification — {CASE}

**Doc No. {PREFIX}-DS-01** · Design case: next-generation flagship-vehicle battery · Rev A (2026-08-25)
Requirement (task contract): energy density ≥ 500.94 Wh/kg · 4C fast charge without lithium plating · maximum temperature ≤ 60 °C (333.15 K).

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | LNMO (LiNi0.5Mn1.5O4, 4.7 V high-voltage spinel) / graphite | base parameter set LNMO.json + Chen2020 negative defaults (runner-injected) |
| Nominal capacity | 4.5 Ah (nominal, parameter set) / 8.26 Ah (simulated 1C, DFN) | LNMO.json `Nominal cell capacity [A.h]`; cell/r9_lnmo_r6_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.7 V | LNMO.json `Lower/Upper voltage cut-off [V]` |
| Cell dimensions | height × width × thickness = Not provided (area 0.1027 m², stack thickness 300 µm) | shell geometry not in parameter set; cell/r9_lnmo_r6_energy_dfn.json:thickness_m/area_m2 |
| Electrolyte formulation | HiTrans-class carbonate/LiFSI-like transport: σ 6 S/m, t⁺ 0.70, D 1.0e-9 m²/s (domain estimates, marked **estimate**, LiFSI-class literature; not yet true-MD-endorsed) + additive set FEC/VC/PES/DTD (funnel-passed, Stage 2) | params_lnmo_r6.json; funnel3 entry; values marked estimate in log |
| Cation transference number | 0.70 | params_lnmo_r6.json `Cation transference number` |

## 2. Electrode and separator

| Layer | Material | Thickness (µm) | Porosity | Active fraction | Source |
|---|---|---|---|---|---|
| Positive electrode | LNMO | 98 | 0.30 | 0.665 | params_lnmo_r6.json; LNMO.json active vol fraction |
| Negative electrode | Graphite | 180 | 0.32 | 0.75 | params_lnmo_r6.json; Chen2020 default active vol fraction |
| Separator | Not provided (default, ρ 397 kg/m³) | 9 | 0.55 | — | params_lnmo_r6.json |
| Positive current collector | Al | 8 | — | — | params_lnmo_r6.json |
| Negative current collector | Cu | 5 | — | — | params_lnmo_r6.json |
| Particles | pos 2.5 µm / neg 1.5 µm | — | — | — | params_lnmo_r6.json |

N/P ratio = (negative areal active capacity)/(positive areal active capacity)
= (m_neg·a_neg·q_neg)/(m_pos·a_pos·q_pos) = ({f(layers['negative_electrode'],4)}×0.75×372)/({f(layers['positive_electrode'],4)}×0.665×146.6) = **{f(np_ratio)}**
(q_neg 372 mAh/g graphite theoretical, q_pos 146.6 mAh/g LNMO theoretical — literature; audit round notes cited simplified estimates 1.78–2.14; deliverable value supersedes with explicit formula.)

## 3. Process design parameters

| Parameter | Value | Formula / source |
|---|---|---|
| Positive areal density | {f(num['a_pos_frac'],0)} g/m² | thickness×(1−ε)×ρ = 98 µm×0.70×4400 kg/m³ (calc-energy layer_kg_m2) |
| Negative areal density | {f(num['a_neg_frac'],0)} g/m² | 180 µm×0.68×1657 kg/m³ (calc-energy layer_kg_m2) |
| Positive compaction density | {f(comp_pos,2)} g/cm³ | electrode density×(1−porosity) ÷1000 |
| Negative compaction density | {f(comp_neg,2)} g/cm³ | 1657×0.68 ÷1000 |
| Electrolyte fill amount | {f(pore_ml,1)} mL / {f(elec_g,1)} g | pore volume×electrolyte density×fill factor (1.0); electrolyte density 1.2 g/cm³ literature value, parameter set missing (annotated) |
| Formation recommendation | 0.1C CC to 4.7 V, 25 °C, 2 cycles | design recommended value; production-line value requires tuning |

## 4. Mass breakdown (per cell)

| Component | Mass (g) | Source |
|---|---|---|
| Positive coating (LNMO composite) | {f(m_pos,2)} | calc-energy layer_kg_m2×area |
| Negative coating (graphite composite) | {f(m_neg,2)} | same |
| Positive CC (Al) | {f(m_al,2)} | same |
| Negative CC (Cu) | {f(m_cu,2)} | same |
| Separator | {f(m_sep,2)} | same |
| **Total (contract caliber, electrolyte excluded)** | **{f(m_tot,2)}** | calc-energy mass_kg |
| Electrolyte (informational, 1.2 g/cm³) | {f(elec_g,1)} | pore volume calc (annotated literature density) |
| Total incl. electrolyte | {f(m_with_elec,1)} | above |
| Enclosure / tabs | Not modeled | beyond pure simulation boundary |

Contract energy density excludes electrolyte per calc-energy contract (electrolyte_included=false); with electrolyte the cell would be {f(ed_inc_elec,0)} Wh/kg (informational).

## 5. Performance verification (conclusion-grade, DFN)

| Metric | Value | Threshold (entry 0) | Determination |
|---|---|---|---|
| Energy density (1C, DFN) | {f(ed,1)} Wh/kg | ≥ 500.94 | ✓ PASS |
| Max temperature (4C charge @45 °C ambient, DFN) | {f(tmax,2)} K = {f(tmax_c,1)} °C | ≤ 333.15 K (≤60 °C) | ✓ PASS |
| Lithium plating (4C, anode potential min) | +{f(anode_min_mv,1)} mV (> 0) | none (plated=false) | ✓ PASS (no plating) |
| 1C discharge capacity (DFN) | {f(cap,2)} Ah | — (informational) | reported |
| Midpoint voltage | {f(midv,3)} V | — (informational) | reported |
| DC resistance (calc-energy formula) | {f(dcr_mohm,1)} mΩ | — (informational) | reported |
| Volumetric energy density | {f(edv,0)} Wh/L | — (informational) | reported |

All conclusion-grade values: cell/r9_lnmo_r6_energy_dfn.json, cell/r9_lnmo_r6_4c45_dfn.json (see DVPR-01 for per-row sources).

## 6. Design notes

- Baseline Chen2020 (NMC811/graphite): ED 400.3 Wh/kg, 4C anode min −0.438 V → confirmed below target; **escalated to Stage 2 materials** (plan_update1): LNMO 4.7 V high-voltage system + HiTrans-class transport + mass-cut architecture (10→8 µm Al, 6→5 µm Cu, 12→9 µm sep).
- ED chain: 492.8 → 520.2 → 539.5 → 566.8 → 622.6 → 612.6 → **603.6 (SPMe) / 597.9 (DFN)** — all ≥ 500.94 from R4 on; final architecture keeps 97 Wh/kg margin.
- Plating chain (anode min, same protocol, same 2.0 Ah charge cap): −0.128 → −0.041 → −0.005 → **+0.015 V** via N/P increase (122→180 µm negative), negative porosity 0.22→0.32, electrolyte D 4e-10→1e-9 m²/s, σ 3.5→6 S/m, separator ε 0.45→0.55 (diagnosis in evaluate R6–R9 notes).
- T_max chain: 321–330 K across LNMO rounds, final 327.6 K at h=100 W/m²K cooling (5.6 K margin).
- Transport values (σ 6 S/m, t⁺ 0.7, D 1e-9 m²/s) are LiFSI-class **domain estimates** (marked estimate in audit; Stage 2 funnel passed the additive set; true DFT/MD endorsement skipped — real_compute=false, endorse entry records skip honestly).
"""

datasheet_md = f"""# Technical Datasheet — {CASE}

**Doc No. {PREFIX}-DSH-01** · Customer-facing summary · Rev A (2026-08-25)

| Field | Value | Source |
|---|---|---|
| Rated capacity | 4.5 Ah (nominal, parameter set) · 8.26 Ah (simulated 1C, DFN) | LNMO.json; cell/r9_lnmo_r6_1c_dfn.json |
| Nominal voltage / window | 4.24 V midpoint · 2.5–4.7 V | calc-energy midpoint_voltage_v; LNMO.json cut-offs |
| Rated energy | {f(energy,2)} Wh | calc-energy energy_wh (V·I integration) |
| Energy density | {f(ed,1)} Wh/kg (contract caliber, electrolyte excluded; with electrolyte {f(ed_inc_elec,0)} Wh/kg informational) | calc-energy + contract mass formula |
| Volumetric energy density | {f(edv,0)} Wh/L | calc-energy energy_density_wh_l |
| Maximum continuous discharge rate | 1C demonstrated (8.26 Ah); 5C not run in this case (N/A — not part of contract) | 1C_discharge protocol |
| Fast-charge capability | 4C @45 °C ambient: T_max {f(tmax,1)} °C (≤60 °C ✓), no lithium plating (anode min +{f(anode_min_mv,1)} mV) | 4C_charge_45C DFN |
| Operating temperature range | 25 °C nominal / 45 °C fast-charge ambient (simulated conditions only) | protocol conditions |
| Cycle life | **Not simulated (requires aging model)** — must not fabricate | — |
| Safety determination | PASS: plating-free 4C charge; T_max within limit | dvpr.md |
| Dimensions / mass | stack 300 µm × 0.1027 m² · {f(m_tot,1)} g (contract) | calc-energy |
| DC resistance | {f(dcr_mohm,1)} mΩ (formula caliber) | calc-energy dcr_ohm |
| Electrolyte | HiTrans-class transport (σ 6 S/m, t⁺ 0.7, D 1e-9 m²/s, estimate) + FEC/VC/PES/DTD additives | params; funnel3 |

**Limitations (honest):** cycle life, calendar aging, mechanical abuse (nail/crush/drop), overcharge-to-thermal-runaway, and low-temperature performance were not simulated — beyond the pure-simulation boundary of this case (see DVPR-01). Transport values are domain estimates pending true MD endorsement.
"""

dvpr_md = f"""# Design Verification Plan & Report (virtual test) — {CASE}

**Doc No. {PREFIX}-DVPR-01** · Rev A (2026-08-25) · Virtual-test version; all results from simulation (run-pyamm / calc-energy), conclusion-grade values DFN.

| # | Verification item | Condition | Result | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C CC discharge 4.7→2.5 V, 25 °C | {f(cap,2)} Ah | informational (no contract threshold) | cell/r9_lnmo_r6_1c_dfn.json:capacity_ah |
| 2 | Energy density | 1C discharge energy ÷ contract mass | {f(ed,1)} Wh/kg | ✓ PASS vs ≥500.94 | cell/r9_lnmo_r6_energy_dfn.json:energy_density_wh_kg |
| 3 | 4C fast-charge temperature | 4C charge, 45 °C ambient, lumped thermal, DFN | T_max {f(tmax,2)} K ({f(tmax_c,1)} °C) | ✓ PASS vs ≤333.15 K | cell/r9_lnmo_r6_4c45_dfn.json:T_max_K |
| 4 | 4C fast-charge plating | same, anode potential series | min +{f(anode_min_mv,1)} mV (>0) | ✓ PASS (plated=false) | cell/r9_lnmo_r6_4c45_dfn.json:anode_potential_v |
| 5 | Voltage window | parameter set limits | 2.5–4.7 V | — | LNMO.json |
| 6 | 4C charge acceptance | protocol cap | {f(charge_ah,1)} Ah accepted | informational | cell/r9_lnmo_r6_4c45_dfn.json:capacity_ah |
| 7 | DC resistance (formula) | calc-energy V²/4P formula | {f(dcr_mohm,1)} mΩ | informational | cell/r9_lnmo_r6_energy_dfn.json:dcr_ohm |
| 8 | Nail penetration | — | N/A (beyond pure simulation boundary, requires physical experiment) | — | — |
| 9 | Overcharge to thermal runaway | — | N/A (same) | — | — |
| 10 | Crush / drop / mechanical | — | N/A (same) | — | — |
| 11 | Cycle life | — | N/A (aging model not in scope of this case; no SEI aging protocol run) | — | — |
| 12 | Rate-pulse internal resistance | — | N/A (same) | — | — |

**Conclusion:** contract requirements **ACHIEVED** — energy density {f(ed,1)} ≥ 500.94 Wh/kg ✓, 4C no-plating ✓ (anode min +{f(anode_min_mv,1)} mV), T_max {f(tmax,1)} °C ≤ 60 °C ✓.
**Not covered (paper limitations):** mechanical abuse, overcharge, cycle life, low temperature, rate pulse — require physical experiments; electrolyte transport values are estimates pending true MD endorsement (real_compute=false).
"""

dfmea_md = f"""# Design FMEA (qualitative, simulation-signal based) — {CASE}

**Doc No. {PREFIX}-DFMEA-01** · Rev A (2026-08-25) · Qualitative caliber: severity/occurrence rated from simulation signal magnitude vs threshold; S/O ∈ high/medium/low; RPN = simplified S×O matrix (annotated qualitative).

| Failure mode | Failure cause | Simulation signal (detectability) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Negative-electrode Li plating (fast charge) | anode potential < 0 V at 4C: deep-charge lithiation + electrolyte depletion | anode_potential_v min = **+{f(anode_min_mv,1)} mV** (margin vs 0) | low (caught before onset; plating risk currently absent) | low | N/P 1.92 (180 µm negative), negative ε 0.32, D 1e-9/σ 6 (transport), sep ε 0.55 — R4→R9 chain −41→+15 mV |
| Thermal runaway risk (4C charge) | heat generation > dissipation at 4C | T_max {f(tmax,2)} K vs 333.15 K limit (margin {f(333.15-tmax,1)} K) | high (consequence if triggered) | low | h=100 W/m²K cooling; margin 5.6 K; transport gains cut ohmic heat |
| Electrolyte oxidative decomposition (4.7 V window) | high-voltage oxidation at 4.7 V cathode | Stage 2 funnel: additive set FEC/VC/PES/DTD passed elimination lines (HOMO < −6 eV threshold; HOMO −12.8…−12.0 eV); true DFT endorsement skipped (real_compute=false) | medium | low | 4.7 V-class LNMO system + film-forming additives (SEI/CEI) |
| Insufficient capacity / energy | electrode utilization loss | 1C capacity {f(cap,2)} Ah, ED {f(ed,1)} Wh/kg vs 500.94 (margin {f(ed-500.94,0)} Wh/kg) | medium | low | positive-limited design; stoich window 0.9→0.3 |
| Electrolyte transport degradation at low T | conductivity drop | not simulated (low-T out of scope) | medium | not evaluated | N/A (beyond simulation boundary) |

**Conclusion:** highest-risk items are high-consequence/low-occurrence (thermal) — mitigated by 5.6 K T_max margin and plating-free anode (+{f(anode_min_mv,1)} mV margin). All identified failure modes have design-side mitigations implemented in LNMO-R6. Complete FMEA incl. process/supplier failure modes: **N/A (beyond pure simulation boundary)**.
"""

delivery_index_md = f"""# Delivery Index — {CASE}

**Doc No. {PREFIX}-INDEX-01** · Generation date: 2026-08-25 · Numbering scheme: VBF-<CASE-UPPER>-<doc-code>-<serial> · Signature fields left blank for review.

| File | Doc No. | Format | Source note |
|---|---|---|---|
| design_spec.md / design_spec.pdf | {PREFIX}-DS-01 | Markdown / PDF (release) | parameter set + simulation (calc-energy/run-pyamm) |
| bom.xlsx / bom.pdf | {PREFIX}-BOM-01 | Excel / PDF (release) | calc-energy layer masses + composition estimates |
| datasheet.md / datasheet.pdf | {PREFIX}-DSH-01 | Markdown / PDF (release) | parameter set + simulation |
| calc.xlsx / calc.pdf | {PREFIX}-CALC-01 | Excel / PDF (release) | full calculation chain, formulas annotated |
| dvpr.md / dvpr.pdf | {PREFIX}-DVPR-01 | Markdown / PDF (release) | virtual tests (run-pyamm DFN) |
| dfmea.md / dfmea.pdf | {PREFIX}-DFMEA-01 | Markdown / PDF (release) | simulation signals, qualitative ratings |
| delivery_index.md / delivery_index.pdf | {PREFIX}-INDEX-01 | Markdown / PDF (release) | this index |

VBF numbering list: {PREFIX}-DS-01 · {PREFIX}-BOM-01 · {PREFIX}-DSH-01 · {PREFIX}-CALC-01 · {PREFIX}-DVPR-01 · {PREFIX}-DFMEA-01 · {PREFIX}-INDEX-01

**Case summary:** next-generation flagship-vehicle battery — LNMO/graphite 4.7 V system, HiTrans-class electrolyte transport, 4C fast charge without plating, T_max ≤ 60 °C.
**Final (conclusion-grade, DFN):** {f(ed,1)} Wh/kg (≥500.94) · 4C anode min +{f(anode_min_mv,1)} mV (no plating) · T_max {f(tmax,1)} °C (≤60 °C) — **ALL GATES PASS**, verdict: achieved (log.jsonl final entry).
Audit trail: runs/exp/{CASE}/log.jsonl (plan → propose R1–R9 → funnel → evaluate R1–R9 → endorse (skipped, real_compute=false) → final).
Signatures: ______ (design) · ______ (review) · ______ (approval)
"""

# ---------------------------------------------------------------- xlsx builders
HEAD_FILL = PatternFill("solid", fgColor="1E5A8A")
HEAD_FONT = Font(color="FFFFFF", bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")

def style_sheet(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for cell in ws[1]:
        cell.fill = HEAD_FILL; cell.font = HEAD_FONT
    for row in ws.iter_rows():
        for c in row:
            c.alignment = WRAP

# ---- bom.xlsx
wb = Workbook()
ws = wb.active; ws.title = "BOM"
ws.append(["Component", "Material / note", "Mass (g/cell)", "kg/kWh", "Formula", "Source"])
energy_kwh = energy/1000.0
bom_rows = [
 ("Positive active material", "LNMO LiNi0.5Mn1.5O4, vol frac 0.665", m_pos*0.665, "coating mass × active vol frac", "LNMO.json active vol fraction; calc-energy layer_kg_m2"),
 ("Positive conductive additive", "carbon black (lit. ρ 1900 kg/m³), est. 0.067 vol frac", m_pos*0.067, "coating mass × est. vol frac (lit. default)", "literature default (annotated: split 80/20 of residual 0.335)"),
 ("Positive binder", "PVDF (lit. ρ 1780 kg/m³), est. 0.268 vol frac", m_pos*0.268, "coating mass × est. vol frac (lit. default)", "literature default (annotated)"),
 ("Negative active material", "graphite, vol frac 0.75", m_neg*0.75, "coating mass × active vol frac", "Chen2020 default active vol fraction"),
 ("Negative conductive additive", "est. 0.05 vol frac (lit. default)", m_neg*0.05, "coating mass × est. vol frac", "literature default (annotated)"),
 ("Negative binder", "CMC/SBR, est. 0.20 vol frac (lit. default)", m_neg*0.20, "coating mass × est. vol frac", "literature default (annotated)"),
 ("Separator", "default sep. ρ 397 kg/m³", m_sep, "L×(1−ε)×ρ×area", "calc-energy layer_kg_m2"),
 ("Electrolyte", "HiTrans-class + FEC/VC/PES/DTD; ρ 1.2 g/cm³ (lit.)", elec_g, "pore volume × 1.2 g/cm³", "pore vol = area×Σ(L·ε); density literature (annotated)"),
 ("Positive current collector (Al)", "Al 8 µm", m_al, "L×ρ×area", "calc-energy layer_kg_m2"),
 ("Negative current collector (Cu)", "Cu 5 µm", m_cu, "L×ρ×area", "calc-energy layer_kg_m2"),
 ("Enclosure / tabs", "Not modeled", None, None, "beyond pure simulation boundary", "—"),
]
tot = 0.0
for r in bom_rows:
    ws.append([r[0], r[1], round(r[2],2) if r[2] is not None else "N/A",
               round(r[2]/1000/energy_kwh,3) if r[2] is not None else "N/A", r[3], r[4]])
    if r[2] is not None: tot += r[2]
ws.append(["TOTAL (without electrolyte)", "", round(m_tot,2), round(m_tot/1000/energy_kwh,3),
           "Σ layer masses (contract caliber)", "calc-energy mass_kg"])
ws.append(["TOTAL (with electrolyte)", "", round(m_with_elec,1), round(m_with_elec/1000/energy_kwh,3),
           "contract + electrolyte estimate", "pore-volume calc"])
ws.append(["Cell energy", "", round(energy,2), "Wh", "V·I integration", "cell/r9_lnmo_r6_energy_dfn.json:energy_wh"])
style_sheet(ws, [30, 38, 14, 12, 38, 42])
wb.save(os.path.join(DLV, "bom.xlsx"))

# ---- calc.xlsx
wb = Workbook()
ws = wb.active; ws.title = "Inputs"
ws.append(["Parameter", "Value", "Unit", "Source"])
for k, v, u, s in [
    ("Positive electrode thickness", Lp*1e6, "µm", "params_lnmo_r6.json"),
    ("Negative electrode thickness", Ln*1e6, "µm", "params_lnmo_r6.json"),
    ("Separator thickness", Ls*1e6, "µm", "params_lnmo_r6.json"),
    ("Positive CC thickness (Al)", 8e-6*1e6, "µm", "params_lnmo_r6.json"),
    ("Negative CC thickness (Cu)", 5e-6*1e6, "µm", "params_lnmo_r6.json"),
    ("Positive porosity", ep, "—", "params_lnmo_r6.json"),
    ("Negative porosity", en, "—", "params_lnmo_r6.json"),
    ("Separator porosity", es, "—", "params_lnmo_r6.json"),
    ("Electrolyte conductivity", 6.0, "S/m", "params_lnmo_r6.json (estimate, LiFSI-class)"),
    ("Cation transference number", 0.70, "—", "params_lnmo_r6.json"),
    ("Electrolyte diffusivity", 1.0e-9, "m²/s", "params_lnmo_r6.json (estimate)"),
    ("Cooling h", 100.0, "W/m²K", "params_lnmo_r6.json"),
    ("Positive particle radius", 2.5e-6*1e6, "µm", "params_lnmo_r6.json"),
    ("Negative particle radius", 1.5e-6*1e6, "µm", "params_lnmo_r6.json"),
    ("Cell area", area, "m²", "calc-energy area_m2"),
]:
    ws.append([k, v, u, s])
style_sheet(ws, [40, 16, 10, 40])
ws = wb.create_sheet("CapacityEnergy")
ws.append(["Quantity", "Value", "Unit", "Formula", "Source"])
for r in [
    ("Nominal capacity", 4.5, "Ah", "parameter set", "LNMO.json"),
    ("1C capacity (DFN)", cap, "Ah", "simulation", "cell/r9_lnmo_r6_1c_dfn.json:capacity_ah"),
    ("Discharge energy (1C, DFN)", energy, "Wh", "∫V·I dt", "cell/r9_lnmo_r6_energy_dfn.json:energy_wh"),
    ("Midpoint voltage", midv, "V", "E/cap", "cell/r9_lnmo_r6_energy_dfn.json:midpoint_voltage_v"),
    ("4C current (nominal basis)", i4c, "A", "4×4.5 Ah", "LNMO.json nominal capacity"),
    ("4C current density", i4c_am2, "A/m²", "I/area", "derived"),
]:
    ws.append([r[0], r[1], r[2], r[3], r[4]])
style_sheet(ws, [40, 16, 10, 30, 45])
ws = wb.create_sheet("EnergyDensity")
ws.append(["Quantity", "Value", "Unit", "Formula", "Source"])
for r in [
    ("Cell mass (contract)", mass*1000, "g", "Σ L×(1−ε)×ρ×area (electrolyte excluded)", "cell/r9_lnmo_r6_energy_dfn.json:mass_kg"),
    ("Energy density (gravimetric)", ed, "Wh/kg", "E/mass", "cell/r9_lnmo_r6_energy_dfn.json:energy_density_wh_kg"),
    ("Volume", E["volume_m3"]*1e6, "mL", "thickness×area", "cell/r9_lnmo_r6_energy_dfn.json:volume_m3"),
    ("Energy density (volumetric)", edv, "Wh/L", "E/volume", "cell/r9_lnmo_r6_energy_dfn.json:energy_density_wh_l"),
    ("DC resistance", dcr*1000, "mΩ", "formula (calc-energy)", "cell/r9_lnmo_r6_energy_dfn.json:dcr_ohm"),
    ("Power density (formula)", power_w/1000.0, "kW/kg", "V²/4R/m", "cell/r9_lnmo_r6_energy_dfn.json:power_density_w_kg"),
    ("ED incl. electrolyte (info)", ed_inc_elec, "Wh/kg", "E/(mass+electrolyte)", "derived; electrolyte ρ 1.2 g/cm³ lit."),
]:
    ws.append([r[0], r[1], r[2], r[3], r[4]])
style_sheet(ws, [40, 16, 10, 40, 45])
ws = wb.create_sheet("NPAndMass")
ws.append(["Quantity", "Value", "Unit", "Formula", "Source"])
for r in [
    ("Positive areal mass", layers["positive_electrode"]*1000, "g/m²", "L×(1−ε)×ρ", "calc-energy layer_kg_m2"),
    ("Negative areal mass", layers["negative_electrode"]*1000, "g/m²", "L×(1−ε)×ρ", "calc-energy layer_kg_m2"),
    ("N/P ratio", np_ratio, "—", "(m_neg·a_neg·q_neg)/(m_pos·a_pos·q_pos)", "a 0.75/0.665 param sets; q 372/146.6 mAh/g lit."),
    ("Layer masses", f"{m_pos:.1f} / {m_neg:.1f} / {m_al:.2f} / {m_cu:.2f} / {m_sep:.2f}", "g", "areal mass×area", "calc-energy layer_kg_m2×area"),
    ("Total mass (contract)", m_tot, "g", "Σ layers", "calc-energy mass_kg"),
    ("Electrolyte mass (info)", elec_g, "g", "pore vol×1.2 g/cm³", "pore vol = area×Σ(L·ε)"),
]:
    ws.append([r[0], r[1], r[2], r[3], r[4]])
style_sheet(ws, [40, 30, 10, 42, 45])
ws = wb.create_sheet("ProcessParams")
ws.append(["Parameter", "Value", "Unit", "Formula", "Source"])
for r in [
    ("Positive areal density", num['a_pos_frac'], "g/m²", "L×(1−ε)×ρ", "calc-energy"),
    ("Negative areal density", num['a_neg_frac'], "g/m²", "L×(1−ε)×ρ", "calc-energy"),
    ("Positive compaction density", comp_pos, "g/cm³", "ρ×(1−ε)÷1000", "derived"),
    ("Negative compaction density", comp_neg, "g/cm³", "ρ×(1−ε)÷1000", "derived"),
    ("Electrolyte fill", pore_ml, "mL", "pore vol; fill factor 1.0", "derived; ρ 1.2 g/cm³ lit. annotated"),
    ("Formation", "0.1C CC to 4.7 V, 25 °C, 2 cycles", "—", "design recommended value", "annotated: production-line value requires tuning"),
]:
    ws.append([r[0], r[1], r[2], r[3], r[4]])
style_sheet(ws, [40, 30, 10, 40, 45])
wb.save(os.path.join(DLV, "calc.xlsx"))

# ---------------------------------------------------------------- markdown write
for fn, md in [("design_spec.md", design_spec_md), ("datasheet.md", datasheet_md),
               ("dvpr.md", dvpr_md), ("dfmea.md", dfmea_md), ("delivery_index.md", delivery_index_md)]:
    with open(os.path.join(DLV, fn), "w", encoding="utf-8") as fh:
        fh.write(md)
print("md written; total mass check: %.3f g (calc %.3f)" % (m_tot, mass*1000))
print("ED %.2f | Tmax %.2f K | anode min %.4f V | N/P %.2f | elec %.1f g | with-elec ED %.0f"
      % (ed, tmax, anode_min, np_ratio, elec_g, ed_inc_elec))
