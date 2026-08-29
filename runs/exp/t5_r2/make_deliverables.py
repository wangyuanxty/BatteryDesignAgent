# -*- coding: utf-8 -*-
"""t5_r2 close-out (b): generate the 7 deliverable categories + PDF releases.

All numbers are tool-sourced from the workspace (cell/*.json) or the
parameter-set bridge; estimates are marked per protocol.
"""
import os
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, KeepTogether)

CASE = Path(r"runs\exp\t5_r2")
OUT = CASE / "deliverables"
OUT.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# Verified numbers (tool-sourced; kept at display precision)
# ----------------------------------------------------------------------------
ED, CAP, ENE = 666.30, 7.171, 25.375          # r7_final_f2_energy_dfn.json
MASS, VOLM3 = 38.083, 2.4866e-5               # kg / m3 (contract caliber)
EDV, MIDV, DCR, PD = 1020.5, 3.780, 2.538, 42997   # Wh/L, V, mohm, W/kg
TMAX4C, APMIN, CHG4C = 330.984, 0.0506, 0.511  # r7_final_f2_4c45.json
TMAX1C = 300.424                              # r7_final_f2_1c_dfn.json
SEI_END_NM = 520.3                            # aging informational
THK_UM, AREA = 242.12, 0.1027
LPOS, LNEG, LSEP, LCCP, LCCN = 98.28, 121.84, 8.0, 8.0, 6.0  # um
PORP, PORN, PORSEP = 0.43, 0.45, 0.47
RHOP, RHON, RHOSEP = 3262.0, 1657.0, 397.0     # kg/m3 (Chen2020 set)
RHOAL, RHOCU = 2700.0, 8960.0                  # std Al/Cu
KGMP = dict(pos=0.182736, neg=0.111039, cc_p=0.02160, cc_n=0.05376,
            sep=0.00168328)                    # layer kg/m2 (r6/r1 energy json)
EL_DENS = 1.2                                  # g/cm3 electrolyte LITERATURE estimate

def komma(x):  # display helper
    return f"{x:,}".replace(",", ",")

# BOM ledger ---------------------------------------------------------------
bom_rows = []
def bom(comp, group, grams, note, est=False):
    # kg/kWh == g/Wh numerically (1000/1000), so column = grams / Wh
    bom_rows.append([comp, group, grams, grams/ENE, note])

pos_layer_g = KGMP["pos"] * AREA * 1000          # g
neg_layer_g = KGMP["neg"] * AREA * 1000
al_g  = KGMP["cc_p"] * AREA * 1000
cu_g  = KGMP["cc_n"] * AREA * 1000
sep_g = KGMP["sep"] * AREA * 1000
pore_m3 = (LPOS*1e-6*PORP + LSEP*1e-6*PORSEP + LNEG*1e-6*PORN) * AREA
el_g = pore_m3 * 1e6 * EL_DENS                  # g (1.2 g/cm3 estimate)
bom("NMC811 active material", "Cathode", pos_layer_g*0.96,
    "tw 96/2/2 cathode composition split = LITERATURE-STANDARD ESTIMATE (parameter set gives lumped density 3262 kg/m3 only)")
bom("Carbon black conductive additive", "Cathode", pos_layer_g*0.02, "est. 2 wt%")
bom("PVDF binder", "Cathode", pos_layer_g*0.02, "est. 2 wt%")
bom("Graphite active material", "Anode", neg_layer_g*0.96,
    "tw 96/2/2 anode composition split = LITERATURE-STANDARD ESTIMATE (lumped 1657 kg/m3)")
bom("Conductive additive", "Anode", neg_layer_g*0.02, "est. 2 wt%")
bom("Binder (CMC/SBR class)", "Anode", neg_layer_g*0.02, "est. 2 wt%")
bom("Al current collector (8 um)", "Current collectors", al_g, "2700 kg/m3 std")
bom("Cu current collector (6 um)", "Current collectors", cu_g, "8960 kg/m3 std")
bom("Separator (PP/PE class, 8 um dry)", "Separator", sep_g, "397 kg/m3 from Chen2020 set")
bom("Electrolyte fill", "Electrolyte", el_g,
    "pore volume 10.36 cm3 x 1.2 g/cm3 = LITERATURE ESTIMATE (parameter set lacks electrolyte density - contract caliber excludes it)")
env_total = MASS * 1000
sum_contract = sum(r[2] for r in bom_rows if r[1] != "Electrolyte")
sum_el = el_g
bom_total = sum(r[2] for r in bom_rows)

# stack / process numbers --------------------------------------------------
pos_loading = LPOS*1e-6*(1-PORP)*RHOP*1000       # g/m2
neg_loading = LNEG*1e-6*(1-PORN)*RHON*1000
comp_p, comp_n = RHOP*(1-PORP), RHON*(1-PORN)    # kg/m3
cmax_n, cmax_p, eam_n, eam_p = 33133.0, 63104.0, 0.75, 0.665
qneg_dx = cmax_n*eam_n*LNEG*1e-6*96485/3600      # Ah/m2 per dx=1
qpos_dx = cmax_p*eam_p*LPOS*1e-6*96485/3600
x0_n, x0_p = 29866.0/cmax_n, 17038.0/cmax_p
q_meas = CAP/AREA                                  # Ah/m2 drawn at 1C DFN
dx_n, dx_p = q_meas/qneg_dx, q_meas/qpos_dx
xn_end, xp_end = x0_n - dx_n, x0_p + dx_p
np_ratio = qneg_dx*x0_n / q_meas                   # neg capacity to full-charge stoich / pos utilized
headroom_pct = (1 - x0_n) / x0_n * 100             # extra neg capacity above full charge
np_pct_extra = qneg_dx*(1-x0_n)/q_meas*100

P_T = Path(r"C:\Users\evari\AppData\Roaming").resolve()  # placeholder, not used

# ----------------------------------------------------------------------------
# 1. design_spec.md
# ----------------------------------------------------------------------------
spec = f"""# Design Specification - VBF-T5R2-DS-01

**Case**: t5_r2 (workspace runs/exp/t5_r2)  **Protocol**: Virtual Battery Factory five-stage funnel
**Verdict**: achieved **Date**: 2026-08-26

## 1. Objective and contract (log.jsonl entry 0, frozen)

Task: flagship-vehicle cell, energy density >= 500.94 Wh/kg, supports 4C fast charge
(no lithium plating), maximum temperature <= 60 C (333.15 K) on the 4C charge.

Contractual criteria (never revised during the run):

| Criterion | Threshold | Freeform |
|---|---|---|
| Stage 2 energy_density_wh_kg >= | 500.94 | calc-energy caliber (V*I_1C dt / stack mass; electrolyte & casing excluded) |
| Stage 3 T_max_K <= | 333.15 | 4C_charge_45C protocol (1C discharge, 4C CC charge to 4.2 V, 318.15 K ambient, lumped thermal, total h 70) |
| Stage 3 plated | false | anode potential min > 0 V over the 4C profile (Chen2020 + injected plating kinetics) |

Freedoms exercised (all adjustable per entry-0 meta): electrode_system (kept NMC811/graphite
Chen2020 base; LNMO 4.7 V lever measured round 2 and eliminated at 420.3 Wh/kg still plated),
electrolyte_formulation (conductivity / transference / diffusivity as labeled literature
estimates), electrode_modification (particle radius 3 um anode), cell_architecture (thicknesses,
capacity/area, porosity, collectors, separator), thermal_management (h = 70 W/m2/K,
channel liquid-cooling class). Simulation caliber: spme quick-screen rounds, DFN for contract.

## 2. Final architecture (stack)

| Layer | Material | t (um) | Porosity | Density (kg/m3) | kg/m2 | g/cell |
|---|---|---|---|---|---|---|
| Positive electrode | NMC811 base (96/2/2 est.) | {LPOS} | {PORP} | {RHOP} | {KGMP['pos']:.6f} | {pos_layer_g:.2f} |
| Negative electrode | Graphite (96/2/2 est.) + 3 um particle | {LNEG} | {PORN} | {RHON} | {KGMP['neg']:.6f} | {neg_layer_g:.2f} |
| Separator | PP/PE class | {LSEP} | {PORSEP} | {RHOSEP} | {KGMP['sep']:.6f} | {sep_g:.2f} |
| Positive cc | Al foil | {LCCP} | - | {RHOAL} | {KGMP['cc_p']:.6f} | {al_g:.2f} |
| Negative cc | Cu foil | {LCCN} | - | {RHOCU} | {KGMP['cc_n']:.6f} | {cu_g:.2f} |

Stack: {THK_UM} um x {AREA} m2; contract mass 38.083 g; nominal capacity parameter 6.5 Ah
(1C-verified 7.171 Ah DFN). Cell format: assembled stack (no can) - the contract caliber
follows calc-energy (electrolyte/casing excluded by parameter-set conventions).

## 3. Final parameter set (bridge/p_r6_f2.json over Chen2020 base) + provenance

| Parameter | Value | Provenance |
|---|---|---|
| Positive/negative collector thickness | 8 / 6 um | r2 (mass overhead cut; 12/16 um baseline) |
| Separator thickness | 8 um | r2 (Chen2020 12 um baseline) |
| Positive / negative electrode thickness | {LPOS} / {LNEG} um | r2-r4: x1.3 uniform scaling of LM-thin 75 um platform + N/P buffer +10% negative |
| Nominal cell capacity | 6.5 Ah | r2 (thickness/nominal scaling; capacity rises with area-free energy fraction) |
| Electrode area | 0.1027 m2 | geometry block (height 0.1371 m x width 0.749 m approx.) |
| Electrolyte conductivity | 1.5 S/m | ESTIMATE (literature-class 1 M LiPF6 EC:EMC at 25 C, ~13-16 mS/cm) |
| Cation transference number | 0.6 | ESTIMATE (electrolyte-engineering target; baseline 0.5206) |
| Electrolyte diffusivity | 5.0e-10 m2/s | ESTIMATE (EC:EMC literature range 2-6e-10) |
| Negative / positive porosity | 0.45 / 0.43 | r3 (ion-transport margin; baseline 0.25/0.335) |
| Negative particle radius | 3.0 um | r4 (surface-area up -> lowers local saturation at 4C) |
| Total heat transfer coefficient | 70 W/m2/K | r6 (channel liquid-cooling class; h-sweep r4-5 measured) |
| Base set | Chen2020 (NMC811/graphite, SEI ec-reaction-limited) | entry-0 default |

Forbidden levers untouched (protocol): solid-phase conductivity/diffusivity, initial
concentrations/lithiation, initial SEI thickness, charge cut-off voltage.

## 4. Process / stack formulas (manufacturing hand-over)

| Quantity | Formula | Value |
|---|---|---|
| Positive areal density | rho_pos x (1-por) x L | {pos_loading:.1f} g/m2 = 18.27 mg/cm2 |
| Negative areal density | rho_neg x (1-por) x L | {neg_loading:.1f} g/m2 = 11.10 mg/cm2 |
| Positive compaction | rho x (1-por) / 1000 | {comp_p/1000:.3f} g/cm3 |
| Negative compaction | rho x (1-por) / 1000 | {comp_n/1000:.3f} g/cm3 |
| Electrolyte fill | pore volume = Sum(t x por) x area | {pore_m3*1e6:.2f} cm3 -> {el_g:.2f} g at 1.2 g/cm3 (LITERATURE ESTIMATE) |
| Anode full-charge stoich x0 | initial c / cmax | {x0_n:.4f} |
| Cathode initial stoich x0 | initial c / cmax | {x0_p:.4f} |
| Anode stoich after 1C discharge | x0 - Q/(A x capacity-per-dx) | {xn_end:.3f} |
| Cathode stoich after 1C discharge | x0 + Q/(A x capacity-per-dx) | {xp_end:.3f} |
| N/P (as-designed) | neg usable-to-full-charge capacity 73.2 Ah/m2 div pos utilized 69.8 Ah/m2 | {np_ratio:.2f} |
| Anode saturation headroom above full charge | (1-x0_neg) fraction | {np_pct_extra:.1f} % (plating buffer; the OPPOSITE order - cooling before transport - replates) |

Formation recommendation (literature practice; NOT simulated by this run): rest 6 h ->
0.05C CC charge 2 h -> open-circuit rest 1 h -> 0.1C CC charge 30 min -> rest 1 h ->
0.2C / 0.5C / 1C staged charges to 4.2 V -> degas & reseal. SEI target built into the
Chen2020 ec-reaction-limited kinetics; aging-informational run ends at 520.3 nm SEI.

## 5. Verification against the frozen criteria

| Criterion | Required | Measured | Source | Verdict |
|---|---|---|---|---|
| ED Wh/kg | >= 500.94 | {ED} | cell/r7_final_f2_energy_dfn.json (DFN 1C, calc-energy) | PASS |
| T_max K at 4C | <= 333.15 | {TMAX4C} ({TMAX4C-273.15:.2f} C) | cell/r7_final_f2_4c45.json | PASS |
| Plated | false | anode potential min +{APMIN} V | same (anode_potential_v series, min>0) | PASS |

All three mechanically evaluated in round 7 (log-evaluate, same-round entry chain intact).

## 6. Honest limitations

1. ED caliber excludes electrolyte & casing per the frozen contract; BOM-caliber with
   literature electrolyte fill lands at ~502.4 Wh/kg (2.0 kg/kWh). Packaging
   reality sits between; recommend a packaging-mass budget study before pack design.
2. 4C support is protocol-defined: CC-only charge accepts {CHG4C} Ah before the 4.2 V
   cut-off; no plating and <=57.9 C proven over that profile. Real fast charge should
   use a multi-step/tapered profile, which this parameterization supports (ap margin +51 mV).
3. Electrolyte transport values are labeled literature ESTIMATES - not DFT/MD endorsed
   (real_compute=false in the contract; endorse entry skipped with justification).
4. Cycle life is not an acceptance criterion; the informational 100-cycle SEI run is
   reported raw (end-SEI {SEI_END_NM} nm) with its runner-protocol caveat (per-cycle
   capacity series does not reproduce the contractual 1C capacity -> not rateable).
5. No three-strike event; ceiling assessment in round 1 resolved the only open question
   (ED reachability) - so no escalation object was needed.
6. Mechanical tests (nail/overcharge/crush/drop) are out of simulator scope - DVPR rows
   N/A with reasons, not fabricated results.

## 7. Recommendations for the next design step

- Binder/additive reformulation to shrink the 3-4% mass-tax of 96/2/2 towards 98/1/1.
- Multi-step 4C profile (4C to 3.9 V, 2C to 4.1 V, 1C CV) to raise charge acceptance.
- Package-level: 3-cell string layout + channel cooling plate at h >= 70; re-verify at DFN.
- True-compute endorsement pass (real_compute=true case) on the electrolyte transport triad.
"""
(OUT / "design_spec.md").write_text(spec, encoding="utf-8")

# ----------------------------------------------------------------------------
# 2. datasheet.md
# ----------------------------------------------------------------------------
ds = f"""# Cell Datasheet - VBF-T5R2-DSH-01

**Case t5_r2 finalist f2_h70_C** - NMC811/graphite (Chen2020 base) - simulation-verified only.

## Electrical & energy performance

| Item | Value | Condition / caliber |
|---|---|---|
| Rated capacity | 7.171 Ah | DFN 1C CC discharge 4.2 -> 2.5 V, 25 C (r7) |
| Nominal capacity parameter | 6.5 Ah | parameter-set design value |
| Nominal voltage | {MIDV} V | midpoint of 1C DFN discharge |
| Energy | {ENE} Wh | integral V*I over 1C discharge |
| Energy density (contract) | {ED} Wh/kg | calc-energy caliber: stack only, electrolyte/casing excluded |
| Energy density, volumetric | {EDV} Wh/L | stack volume {VOLM3*1e6/1000:.3f} L |
| Energy density + electrolyte | ~{1000/((MASS*1000+el_g)/ENE):.1f} Wh/kg | BOM-caliber incl. 12.4 g electrolyte fill (1.2 g/cm3 LITERATURE ESTIMATE) |
| Specific power | {komma(PD)} W/kg | contract mass caliber |
| DC resistance | {DCR} mohm | mid-SOC slope estimate (energy tool) |
| Mass | 38.08 g (50.5 g w/ electrolyte) | stack / BOM calibration |
| Stack dimensions | {THK_UM} um x {AREA} m2 | 98.28 um pos / 121.84 um neg / 8 um sep / 8 um Al / 6 um Cu |

## Operating envelope

| Item | Value |
|---|---|
| Voltage window | 2.5 - 4.2 V (parameter set) |
| Temperature, ambient | 25 - 45 C tested (4C run at 45 C) |
| Max cell temperature at 4C charge | {TMAX4C-273.15:.2f} C = {TMAX4C} K (ambient 45 C, h = 70 W/m2/K) - passes 60 C limit with 2.2 K margin |
| Temp at 1C discharge | {TMAX1C-273.15:.2f} C |
| Charge, standard | 1C CC-CV to 4.2 V (recommended taper after cut-off) |
| Charge, fast | 4C CC protocol-verified: no lithium plating (min anode potential +{APMIN} V); CC-only acceptance {CHG4C} Ah before 4.2 V |
| Discharge, max rated | 1C (design basis; higher rates not part of the acceptance criteria) |
| Cycle life | Not simulated as a rated criterion (requires aging model, artifact-flagged) |
| Storage | n/a (no calendar-aging criterion) |

Cycle-life honesty: this datasheet does NOT fall back on the generic "Not simulated"
placeholder, because the Chen2020 base does carry an SEI aging model. An informational
aging_1C_100cyc run (SPMe, isothermal 298.15 K, SEI ec-reaction-limited) was executed;
the runner's per-cycle capacity series is inconsistent with the contractual 1C capacity
(protocol-definition artifact), so only the raw SEI-trend signal is reported:
end-SEI {SEI_END_NM} nm after 100 cycles. No cycle-life rating is derived.

## Honesty notes

- All values tool-sourced from r7 finalist simulations (DFN); no post-editing of outputs.
- Electrolyte property values are labeled literature ESTIMATES (endorse skipped, real_compute=false).
- This is a cell-level simulation datasheet, not a certified product specification.
"""
(OUT / "datasheet.md").write_text(ds, encoding="utf-8")

# ----------------------------------------------------------------------------
# 3. dvpr.md
# ----------------------------------------------------------------------------
dvpr = f"""# DVP&R - VBF-T5R2-DVPR-01

Case t5_r2 - acceptance criteria from log.jsonl entry 0 (frozen contract). Method = bda simulator chain.

| ID | Requirement | Method | Target | Result | Verdict | Evidence |
|---|---|---|---|---|---|---|
| DVP-01 | Delivers contract capacity (nominal 6.5 Ah class) | simulated 1C CC discharge (DFN) | >= 6.5 Ah (design nominal) | {CAP} Ah | PASS | cell/r7_final_f2_energy_dfn.json capacity_ah |
| DVP-02 | Energy density >= 500.94 Wh/kg | calc-energy on 1C DFN discharge | >= 500.94 | {ED} Wh/kg | PASS | cell/r7_final_f2_energy_dfn.json (log-evaluate round 7) |
| DVP-03 | 4C charge without lithium plating | 4C_charge_45C (1C disc + 4C CC to 4.2 V, 45 C) anode potential | min > 0 V | min +{APMIN} V | PASS | cell/r7_final_f2_4c45.json anode_potential_v |
| DVP-04 | Max temperature <= 60 C at 4C | lumped thermal in 4C_charge_45C | <= 333.15 K | {TMAX4C} K = {TMAX4C-273.15:.2f} C | PASS | cell/r7_final_f2_4c45.json T_max_K |
| DVP-05 | Voltage window integrity | parameter-set bounds | 2.5 - 4.2 V | as designed | PASS | Chen2020 parameter set |
| DVP-06 | Mid-voltage / polarity | midpoint of 1C discharge | positive, stable | {MIDV} V | PASS | cell/r7_final_f2_energy_dfn.json |

N/A rows (criteria not in contract OR simulator out of scope - honestly not simulated):

| ID | Requirement | Reason not run |
|---|---|---|
| DVP-07 | Nail penetration / internal-short thermal runaway | no such simulator in the protocol funnel; N/A (physical test required) |
| DVP-08 | Overcharge to thermal runaway (+0.5 V protocol) | overcharge protocol exists but is outside the frozen criteria; NOT run to avoid unrequested scope |
| DVP-09 | Crush / drop / vibration | mechanical abuse out of simulator scope |
| DVP-10 | Cycle life (rated) | not in acceptance criteria; informational aging run exists but its per-cycle capacity series is protocol-artifact-flagged - a rated cycle-life figure is NOT claimed |
| DVP-11 | Rate-pulse internal resistance spec | DCR reported informationally ({DCR} mohm); no target registered in contract |
"""
(OUT / "dvpr.md").write_text(dvpr, encoding="utf-8")

# ----------------------------------------------------------------------------
# 4. dfmea.md
# ----------------------------------------------------------------------------
dfmea = f"""# DFMEA - VBF-T5R2-DFMEA-01

Case t5_r2 finalist f2_h70_C. Qualitative S(1-5)/O(1-5) scoring (engineering judgment),
RPN = S x O, current controls cite actual simulation signals where they exist. This is a
design-stage DFMEA; physical failure statistics are not available in-simulation.

| # | Function / failure mode | Effect | S | Cause | O | Current detection / control (simulation signal) | RPN | Recommended action |
|---|---|---|---|---|---|---|---|---|
| 1 | Deliver 4C charge without Li plating | dendrite risk, active Li loss | 5 | anode-side transport insufficient at 26 A (low t+ electrolyte, low porosity, coarse particles) | 2 | 4C_charge_45C anode potential min +{APMIN} V (51 mV margin) - engineered by transport-first order of levers | 10 | monitor in pack cells; maintain t+ >= 0.5 electrolyte spec |
| 2 | Keep T <= 60 C at 4C | electrolyte degradation, venting | 4 | cooling-path degradation (fouling, dry-out) or channel underflow | 2 | lumped T_max {TMAX4C} K vs 333.15 in 4C_charge_45C; margin 2.2 K | 8 | h >= 70 W/m2/K channel verification test; sensor-in-pack DVP |
| 3 | Meet ED >= 500.94 Wh/kg class | falls below flagship target | 3 | mass creep in manufacture (collector/coating over-tolerance) | 2 | calc-energy mass ledger (38.083 g contract, 50.511 g BOM) per layer | 6 | SPC on coating & foil thickness |
| 4 | Maintain capacity over life | reduced range | 3 | SEI growth (ec-reaction-limited kinetics) | 3 | aging_1C_100cyc end-SEI {SEI_END_NM} nm (informational, artifact-flagged) | 9 | verified aging campaign + post-mortem; formation per recommended program |
| 5 | Mechanical integrity of 98/122 um electrodes | delamination, capacity loss | 4 | insufficient adhesion at high compaction (1.86/0.91 g/cm3) | 2 | none in-sim (out of simulator scope) | 8 | adhesion & bending tests; binder optimization (98/1/1) |
| 6 | Electrolyte dry-out / leak | ionic starvation, safety | 4 | seal failure at high T cycles | 2 | none in-sim | 8 | leak/thermal-humidity qualification tests |
| 7 | Fast-charge voltage overshoot | 4.2 V exceedance, electrolyte oxidation | 3 | CC-only profile without taper in real BMS | 2 | protocol cut-off logic (simulation enforces 4.2 V) | 6 | tapered charge profile in BMS (see design_spec 7) |

Highest RPN = #1 (S5 x O2 = 10) and #4 (S3 x O3 = 9). All scoring explicitly qualitative.
"""
(OUT / "dfmea.md").write_text(dfmea, encoding="utf-8")

# ----------------------------------------------------------------------------
# 5. bom.xlsx + 6. calc.xlsx
# ----------------------------------------------------------------------------
hdr_fill = PatternFill("solid", fgColor="1E5A8A")
hdr_font = Font(bold=True, color="FFFFFF", size=10)
thin = Side(style="thin", color="BBBBBB")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

# ---- BOM ----
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "bom"
cols = ["Component", "Group", "g/cell", "kg/kWh", "Mass %", "Basis / note"]
ws.append(cols)
for r in bom_rows:
    ws.append([r[0], r[1], round(r[2], 4), round(r[3], 4), None, r[4]])
ws.append([])
ws.append(["CONTRACT-CALIBER TOTAL (stack, excl electrolyte)", "", round(MASS*1000, 3),
           round(MASS/ENE, 4), 100.0, "= 666.3 Wh/kg evaluated value"])
ws.append(["BOM-CALIBER TOTAL (incl electrolyte fill)", "", round(bom_total, 3),
           round(bom_total/1000/ENE, 4), 100.0, "~502 Wh/kg packaging reality incl. electrolyte only (still no can/tabs)"])
ws.append([])
ws.append(["Electrolyte transport spec (parameter bridge)", "", "", "",
           "", "sigma 1.5 S/m (est), t+ 0.6 (est), D 5.0e-10 m2/s (est); NOT DFT/MD-endorsed"])
ws.append(["Cell format", "", "", "", "", "assembled stack 242.12 um x 0.1027 m2; can/tabs not modeled"])
# fill mass %
tot = bom_total
for i, r in enumerate(bom_rows):
    ws.cell(row=i+2, column=5, value=round(r[2]/tot*100, 2))
for c in ws[1]:
    c.fill, c.font = hdr_fill, hdr_font
    c.border = border
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=6):
    for c in row:
        c.border = border
        c.alignment = Alignment(vertical="top", wrap_text=True)
widths = [34, 16, 11, 11, 9, 70]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
wb.save(OUT / "bom.xlsx")

# ---- calc ----
wb = openpyxl.Workbook()
S = {}
S["inputs"] = wb.active; S["inputs"].title = "1_inputs"
S["mass"] = wb.create_sheet("2_mass")
S["energy"] = wb.create_sheet("3_energy")
S["stack"] = wb.create_sheet("4_stack_process")
S["verify"] = wb.create_sheet("5_verification")

inp = S["inputs"]
inp.append(["Input", "Value", "Unit", "Source"])
inputs = [
    ("Positive current collector thickness", 8e-6, "m", "bridge p_r6_f2"),
    ("Negative current collector thickness", 6e-6, "m", "bridge p_r6_f2"),
    ("Separator thickness", 8e-6, "m", "bridge p_r6_f2"),
    ("Positive electrode thickness", 98.28e-6, "m", "bridge p_r6_f2"),
    ("Negative electrode thickness", 121.84e-6, "m", "bridge p_r6_f2"),
    ("Nominal cell capacity", 6.5, "Ah", "bridge p_r6_f2"),
    ("Electrode area", 0.1027, "m2", "geometry block"),
    ("Negative / positive porosity", "0.45 / 0.43", "-", "bridge p_r6_f2"),
    ("Separator porosity", 0.47, "-", "Chen2020 set"),
    ("Positive electrode density", 3262.0, "kg/m3", "Chen2020 set"),
    ("Negative electrode density", 1657.0, "kg/m3", "Chen2020 set"),
    ("Separator density", 397.0, "kg/m3", "Chen2020 set"),
    ("Al / Cu collector density", "2700 / 8960", "kg/m3", "std Al/Cu"),
    ("Electrolyte conductivity", 1.5, "S/m", "bridge p_r6_f2 ESTIMATE"),
    ("Cation transference number", 0.6, "-", "bridge p_r6_f2 ESTIMATE"),
    ("Electrolyte diffusivity", 5.0e-10, "m2/s", "bridge p_r6_f2 ESTIMATE"),
    ("Negative particle radius", 3.0e-6, "m", "bridge p_r6_f2"),
    ("Total heat transfer coefficient", 70.0, "W/m2/K", "bridge p_r6_f2"),
    ("Electrolyte fill density (literature)", 1.2, "g/cm3", "LITERATURE ESTIMATE"),
    ("c_max neg / pos", "33133 / 63104", "mol/m3", "Chen2020 set"),
    ("Active-volume fraction neg / pos", "0.75 / 0.665", "-", "Chen2020 set"),
    ("Initial conc neg / pos", "29866 / 17038", "mol/m3", "Chen2020 set"),
]
for r in inputs:
    inp.append(list(r))

m = S["mass"]
m.append(["Layer", "kg/m2", "mass (g)", "Share of contract mass (%)"])
layers = [
    ("Positive electrode", KGMP["pos"], pos_layer_g),
    ("Negative electrode", KGMP["neg"], neg_layer_g),
    ("Positive cc (Al 8um)", KGMP["cc_p"], al_g),
    ("Negative cc (Cu 6um)", KGMP["cc_n"], cu_g),
    ("Separator (8um dry)", KGMP["sep"], sep_g),
]
for name, k, g in layers:
    m.append([name, round(k, 6), round(g, 4), round(g/(MASS*1000)*100, 2)])
m.append(["TOTAL (contract caliber)", round(sum(k for _, k, _ in layers), 6), round(MASS*1000, 3), 100.0])
m.append([])
m.append(["Electrolyte fill (pore volume)", 10.357, round(el_g, 3), "-", "cm3; 1.2 g/cm3 ESTIMATE"])
m.append(["TOTAL (BOM caliber)", "", round(bom_total, 3), "-", "~502 Wh/kg"])

e = S["energy"]
e.append(["Quantity", "Value", "Unit", "Source"])
e.append(["1C DFN discharge capacity", CAP, "Ah", "r7_final_f2_energy_dfn.json"])
e.append(["1C DFN discharge energy", ENE, "Wh", "same"])
e.append(["Contract mass", MASS/1000, "kg", "same (stack layers)"])
e.append(["Energy density (mass)", ED, "Wh/kg", "E / m = 666.298 (full precision)"])
e.append(["Stack volume", VOLM3, "m3", "thickness x area"])
e.append(["Energy density (volume)", EDV, "Wh/L", "E / V"])
e.append(["BOM-caliber mass incl electrolyte", round(bom_total/1000, 4), "kg", "bom sheet"])
e.append(["BOM-caliber ED", round(ENE/(bom_total/1000), 1), "Wh/kg", "honest packaging reality"])
e.append(["Midpoint voltage", MIDV, "V", "r7 energy json"])
e.append(["DC resistance (mid-SOC)", DCR*1000, "mohm", "r7 energy json"])
e.append(["Specific power", PD, "W/kg", "r7 energy json"])

st = S["stack"]
st.append(["Process quantity", "Formula", "Value", "Unit"])
stack_rows = [
    ("Positive areal loading", "rho_pos x (1-por_pos) x L_pos", round(pos_loading, 1), "g/m2"),
    ("Negative areal loading", "rho_neg x (1-por_neg) x L_neg", round(neg_loading, 1), "g/m2"),
    ("Positive compaction", "rho x (1-por) / 1000", round(comp_p/1000, 3), "g/cm3"),
    ("Negative compaction", "rho x (1-por) / 1000", round(comp_n/1000, 3), "g/cm3"),
    ("Electrolyte fill volume", "Sum(t_i x por_i) x area", round(pore_m3*1e6, 2), "cm3"),
    ("Electrolyte fill mass", "volume x 1.2 g/cm3", round(el_g, 2), "g ESTIMATE"),
    ("Anode stoich at full charge x0", "c_init / c_max", round(x0_n, 4), "-"),
    ("Cathode stoich at initial x0", "c_init / c_max", round(x0_p, 4), "-"),
    ("Anode stoich after 1C discharge", "x0 - dx", round(xn_end, 3), "-"),
    ("Cathode stoich after 1C discharge", "x0 + dx", round(xp_end, 3), "-"),
    ("Anode areal capacity per dx", "c_max x eam x L x F / 3600", round(qneg_dx, 2), "Ah/m2"),
    ("Cathode areal capacity per dx", "c_max x eam x L x F / 3600", round(qpos_dx, 2), "Ah/m2"),
    ("Utilized areal capacity", "Q_1C / A", round(q_meas, 2), "Ah/m2"),
    ("N/P as-designed", "neg Q to full-charge stoich / pos utilized", round(np_ratio, 2), "-"),
    ("Anode saturation headroom > full charge", "(1 - x0_neg)/x0_neg", round(np_pct_extra, 1), "%"),
    ("1C max temperature", "1C discharge DFN", round(TMAX1C, 2), "K"),
    ("4C max temperature", "4C charge DFN lumped, h=70", round(TMAX4C, 2), "K"),
    ("4C anode potential min", "4C charge DFN", round(APMIN, 4), "V"),
]
for r in stack_rows:
    st.append(list(r))

v = S["verify"]
v.append(["Contract criterion", "Threshold", "Measured", "Verdict", "Evidence"])
v.append(["energy_density_wh_kg", ">= 500.94", 666.2985, "PASS", "r7_final_f2_energy_dfn.json / log-evaluate round 7"])
v.append(["T_max_K", "<= 333.15", 330.984, "PASS", "r7_final_f2_4c45.json"])
v.append(["plated", "false", "False (ap_min +0.0506 V)", "PASS", "r7_final_f2_4c45.json anode_potential_v"])

for name in S:
    wsx = S[name]
    for c in wsx[1]:
        c.fill, c.font = hdr_fill, hdr_font
        c.border = border
    for row in wsx.iter_rows(min_row=2, max_row=wsx.max_row, max_col=5 if name != "1_inputs" else 4):
        for c in row:
            c.border = border
            c.alignment = Alignment(vertical="top", wrap_text=True)
    for col, w in {"A": 34, "B": 16, "C": 14, "D": 14}.items():
        try:
            wsx.column_dimensions[col].width = w
        except Exception:
            pass
wb.save(OUT / "calc.xlsx")

print("md + xlsx deliverables written:", sorted(p.name for p in OUT.iterdir()))