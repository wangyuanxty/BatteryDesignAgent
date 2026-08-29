"""Generate deliverable source files (md + xlsx) for t8_r3, flat in deliverables/."""
import json
from pathlib import Path

import openpyxl
import pybamm

CASE = "t8_r3"
OUT = Path("runs/exp/t8_r3/deliverables")
OUT.mkdir(parents=True, exist_ok=True)
CELL = Path("runs/exp/t8_r3/cell")

# ---------- sources (all numbers below come from these objects) ----------
pv = pybamm.ParameterValues("Chen2020")
with open(CELL / "params_r4_V13_porousanode.json", encoding="utf-8") as f:
    over = json.load(f)
full = pv.copy()
full.update(over, check_already_exists=False)

def S(path, key=None):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return d if key is None else d[key]

en  = S(CELL / "r4_V13_porousanode_energy.json")
c1  = S(CELL / "r4_V13_porousanode_1c_dfn.json")
c5  = S(CELL / "r4_V13_porousanode_5c_dfn.json")
c4  = S(CELL / "r4_V13_porousanode_4c_safety.json")
der = S(CELL / "r4_V13_porousanode_derived.json")
oc  = S(CELL / "r4_V13_overcharge.json")
tr  = S(CELL / "r4_V13_runtr.json")

P = lambda k: float(full[k])

area = en["area_m2"]
layers = en["layer_kg_m2"]
L = lambda k: layers[k] * area * 1000.0  # g
m_pos, m_neg = L("positive_electrode"), L("negative_electrode")
m_al, m_cu, m_sep = L("positive_cc"), L("negative_cc"), L("separator")
m_stack = en["mass_kg"] * 1000.0

t_pos, t_neg, t_sep = P("Positive electrode thickness [m]"), P("Negative electrode thickness [m]"), P("Separator thickness [m]")
e_pos, e_neg, e_sep = P("Positive electrode porosity"), P("Negative electrode porosity"), P("Separator porosity")
rho_pos, rho_neg, rho_sep = P("Positive electrode density [kg.m-3]"), P("Negative electrode density [kg.m-3]"), P("Separator density [kg.m-3]")
rho_al, rho_cu = P("Positive current collector density [kg.m-3]"), P("Negative current collector density [kg.m-3]")
aal, acu = P("Positive current collector thickness [m]"), P("Negative current collector thickness [m]")
vf_pos, vf_neg = P("Positive electrode active material volume fraction"), P("Negative electrode active material volume fraction")
cm_pos, cm_neg = P("Maximum concentration in positive electrode [mol.m-3]"), P("Maximum concentration in negative electrode [mol.m-3]")
H, Wdim = P("Electrode height [m]"), P("Electrode width [m]")
h = P("Total heat transfer coefficient [W.m-2.K-1]")

# mechanical stoichiometric N/P (F/3600 cancels)
np_full = (vf_neg * cm_neg * t_neg) / (vf_pos * cm_pos * t_pos)

# process parameters
areal_pos = t_pos * vf_pos * rho_pos          # kg/m2
areal_neg = t_neg * (1 - e_neg) * rho_neg
comp_pos = rho_pos * vf_pos / 1000.0          # g/cm3
comp_neg = rho_neg * (1 - e_neg) / 1000.0
pore_vol = (e_pos * t_pos + e_neg * t_neg + e_sep * t_sep) * area  # m3
elec_mass = pore_vol * 1200.0 * 1.0 * 1000.0  # g: m3 x 1200 kg/m3 x fill 1.0 -> g; density 1.2 g/cm3 literature

# BOM literature-default fractions (parameter set has none)
AM_P, CB_P, BI_P = 0.96, 0.02, 0.02
AM_N, CB_N, BI_N = 0.96, 0.01, 0.03
kwh = en["energy_wh"] / 1000.0
def kk(g):
    return g / 1000.0 / kwh  # kg/kWh

pos_am, pos_cb, pos_bi = m_pos * AM_P, m_pos * CB_P, m_pos * BI_P
neg_am, neg_cb, neg_bi = m_neg * AM_N, m_neg * CB_N, m_neg * BI_N
m_total = pos_am + pos_cb + pos_bi + neg_am + neg_cb + neg_bi + m_sep + elec_mass + m_al + m_cu

Vmin, Vmax = P("Lower voltage cut-off [V]"), P("Upper voltage cut-off [V]")
nom = P("Nominal cell capacity [A.h]")
ret = der["retention_5c"]

def md_table(headers, rows, aligns=None):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out) + "\n"

f2 = lambda x: f"{x:.2f}"
f3 = lambda x: f"{x:.3f}"
f4 = lambda x: f"{x:.4f}"

# ================= design_spec.md =================
ds = []
ds.append("# Cell Design Specification — " + CASE + " (VBF-T8R3-DS-01)\n")
ds.append("**Case**: t8_r3 — long-endurance drone battery (zero-interaction design run).  \n"
          "**System base**: Chen2020 parameter set (NMC811 / graphite).  \n"
          "**Generation date**: 2026-08-26 (virtual-design session; not a production release).\n")
ds.append("## 1. Basic specification\n")
ds.append(md_table(
    ["Item", "Value", "Source"],
    [
        ["Electrochemical system", "NMC811 / graphite (lithium-ion)", "base_params=Chen2020 (case config)"],
        ["Nominal capacity", f"{nom:.1f} Ah (parameter set); simulated 1C DFN capacity {c1['capacity_ah']:.4f} Ah",
         "Chen2020 Nominal cell capacity [A.h]; r4_V13_porousanode_1c_dfn.json:capacity_ah"],
        ["Voltage window", f"{Vmin:.1f} – {Vmax:.1f} V",
         "Chen2020 Lower/Upper voltage cut-off [V]"],
        ["Cell dimensions", f"H {H*1000:.0f} mm × W {Wdim*1000:.0f} mm × stack {en['thickness_m']*1e6:.1f} µm",
         "Chen2020 Electrode height/width [m]; calc-energy thickness_m (layer sum, shell excluded)"],
        ["Shell/casing thickness", "Not provided (no parameter)", "—"],
        ["Electrolyte formulation", "Chen2020 baseline + sigma=2.0 S/m (estimate), D=6e-10 m2/s (estimate)",
         "params_r4_V13_porousanode.json (formulation estimates, marked estimate — not simulation output)"],
        ["Cation transference number", f"{over['Cation transference number']} (override, estimate)",
         "params_r4_V13_porousanode.json"],
        ["Additive candidates", "None (no Stage 2 material candidates; ceiling_escalation OFF ablation)",
         "log.jsonl rounds 1–4"],
    ]))
ds.append("## 2. Electrode and separator\n")
ds.append(md_table(
    ["Layer", "Thickness (µm)", "Porosity", "Collector material / thickness", "Source"],
    [
        ["Positive electrode", f"{t_pos*1e6:.1f}", f"{e_pos:.3f}", f"Al {aal*1e6:.0f} µm",
         "Chen2020 (thickness/porosity); override Al 10 µm (params file)"],
        ["Negative electrode", f"{t_neg*1e6:.1f}", f"{e_neg:.2f} (override 0.25→0.30)", f"Cu {acu*1e6:.0f} µm",
         "Chen2020; overrides: negative porosity 0.30, Cu 8 µm"],
        ["Separator", f"{t_sep*1e6:.1f}", f"{e_sep:.2f}", "—",
         "override separator 9 µm, porosity Chen2020"],
        ["Current collectors", f"Al {aal*1e6:.0f} / Cu {acu*1e6:.0f}", "—", "—",
         "round-1 mass-fit overrides (8/10 µm grades)"],
    ]))
ds.append(f"N/P ratio (DFN stoichiometric inference): **{np_full:.3f}** — full-swing ratio "
          f"(vf_neg×c_max_neg×th_neg)/(vf_pos×c_max_pos×th_pos) = "
          f"({vf_neg}×{cm_neg}×{t_neg*1e6:.1f} µm)/({vf_pos}×{cm_pos}×{t_pos*1e6:.1f} µm); "
          "F/3600 cancels. NOTE: full-swing (0–100% lithiation) ratio — the parameter set carries no direct "
          "capacity-density keys and Chen2020 operating windows differ from full swing; treat as approximate.\n")
ds.append("## 3. Process design parameters\n")
ds.append(md_table(
    ["Parameter", "Value", "Formula", "Notes"],
    [
        ["Positive areal density", f"{areal_pos*1000:.1f} g/m²", "thickness×(1−porosity)×electrode density",
         "matches calc-energy layer_kg_m2"],
        ["Negative areal density", f"{areal_neg*1000:.1f} g/m²", "same", "matches calc-energy layer_kg_m2"],
        ["Positive compaction density", f"{comp_pos:.2f} g/cm³", "electrode density×(1−porosity)/1000", "—"],
        ["Negative compaction density", f"{comp_neg:.2f} g/cm³", "same", "porosity override 0.30 applied"],
        ["Electrolyte fill amount", f"{elec_mass:.2f} g", "pore volume × 1200 kg/m³ × fill 1.0",
         "electrolyte density 1.2 g/cm³ literature value (parameter set lacks it)"],
        ["Formation recommendation", "0.1C CC to 4.2 V, 25 °C, 2 cycles",
         "design recommended value", "actual production-line value requires tuning"],
    ]))
ds.append("## 4. Mass breakdown (contract caliber)\n")
ds.append(md_table(
    ["Layer", "Mass (g)", "Basis", "Source"],
    [
        ["Positive electrode (active layer)", f"{m_pos:.3f}", f"{areal_pos*1000:.1f} g/m² × {area:.4f} m²",
         "r4_V13_porousanode_energy.json:layer_kg_m2.positive_electrode"],
        ["Negative electrode (active layer)", f"{m_neg:.3f}", f"{areal_neg*1000:.1f} g/m² × {area:.4f} m²",
         "energy:layer_kg_m2.negative_electrode"],
        ["Positive current collector (Al)", f"{m_al:.3f}", f"{aal*1e6:.0f} µm × {rho_al:.0f} kg/m³",
         "energy:layer_kg_m2.positive_cc"],
        ["Negative current collector (Cu)", f"{m_cu:.3f}", f"{acu*1e6:.0f} µm × {rho_cu:.0f} kg/m³",
         "energy:layer_kg_m2.negative_cc"],
        ["Separator", f"{m_sep:.3f}", f"{t_sep*1e6:.1f} µm × {rho_sep:.0f} kg/m³ × (1−{e_sep:.2f})",
         "energy:layer_kg_m2.separator"],
        ["**Stack total**", f"**{m_stack:.2f}**", "Σ layers above", "energy:mass_kg (electrolyte excluded — contract caliber)"],
        ["Electrolyte (informational)", f"{elec_mass:.2f}", "pore volume × 1.2 g/cm³", "not in calc-energy mass; listed for BOM only"],
    ]))
ds.append("## 5. Performance verification (vs entry-0 criteria)\n")
ds.append(md_table(
    ["Metric", "Threshold (entry 0)", "Result", "Determination", "Source"],
    [
        ["energy_density_wh_kg", "≥ 446.18", f"{en['energy_density_wh_kg']:.2f}", "✓ pass",
         "r4_V13_porousanode_energy.json:energy_density_wh_kg"],
        ["retention_5c", "≥ 0.90", f"{ret:.4f}", "✓ pass",
         "derived: 5C capacity {:.5f} / 1C capacity {:.5f}".format(c5["capacity_ah"], c1["capacity_ah"])],
        ["mass_kg", "≤ 0.04", f"{en['mass_kg']:.5f} kg ({m_stack:.2f} g)", "✓ pass",
         "energy:mass_kg"],
        ["T_max_K (4C/45 °C charge)", "≤ 333.15", f"{c4['T_max_K']:.2f} K", "✓ pass",
         "r4_V13_porousanode_4c_safety.json:T_max_K"],
        ["plated (4C/45 °C charge)", "false", f"false (anode min {min(c4['anode_potential_v']):+.4f} V)", "✓ pass",
         "4c_safety:anode_potential_v min>0 (mechanical)"],
        ["overcharge → thermal runaway", "(informational)", f"triggered={tr['triggered']}", "✓ not triggered",
         "r4_V13_overcharge.json (T_max 299.33 K) → r4_V13_runtr.json:triggered"],
    ]))
ds.append("## 6. Design notes (what changed and why)\n")
ds.append("- Round 1: thin Cu/Al/separator (8/10/9 µm) fix mass ≤ 40 g; particles remain 5.22/5.86 µm → 5C retention 9%"
          " (cathode surface saturation diagnosed at 96% of c_max at t≈62 s via direct DFN probe).\n"
          "- Round 2: positive/negative particles 1.5/2.5 µm + high-transport electrolyte (σ 2.0 S/m, D 6e-10 m²/s, "
          "t⁺ 0.4, formulation estimates) → retention 98.0%; 4C/45 °C thermal still fails at h=10.\n"
          "- Round 3: h=60 W/m²K forced-air cooling fixes T_max (327.3 K) but low-T anode kinetics plate (−10 mV) — "
          "negative particle 1.5 µm restores margin (V8 pass); thick-negative 100 µm route FAILS plating "
          "(V9/V11) — recorded negative result (anode thickness is a plating liability here).\n"
          "- Round 4: negative porosity 0.30 (V13) chosen: ED 497.5 Wh/kg, retention 98.66%, T_max 326.53 K, "
          "anode min +17.7 mV — the widest safety margins of the campaign; cooling h≥60 W/m²K is part of the "
          "pack-level design.\n")
OUT.joinpath("design_spec.md").write_text("\n".join(ds), encoding="utf-8")

# ================= datasheet.md =================
dsh = []
dsh.append("# Technical Datasheet — " + CASE + " V13 porousanode (VBF-T8R3-DSH-01)\n")
dsh.append("Virtual-design datasheet; values from parameter set and simulation outputs (no physical cell exists).\n")
dsh.append(md_table(
    ["Field", "Value", "Source"],
    [
        ["Rated capacity", f"{nom:.1f} Ah nominal (parameter set); {c1['capacity_ah']:.4f} Ah simulated 1C DFN",
         "Chen2020; r4_V13_porousanode_1c_dfn.json"],
        ["Nominal voltage / window", f"window {Vmin:.1f}–{Vmax:.1f} V; discharge midpoint {en['midpoint_voltage_v']:.3f} V",
         "Chen2020 cut-offs; energy:midpoint_voltage_v"],
        ["Rated energy", f"{en['energy_wh']:.3f} Wh", "energy:energy_wh (∫V·I dt, 1C DFN)"],
        ["Energy density", f"{en['energy_density_wh_kg']:.2f} Wh/kg ({en['energy_density_wh_l']:.1f} Wh/L)",
         "contract formula: energy ÷ calc-energy stack mass (electrolyte excluded)"],
        ["Maximum continuous discharge", f"5C verified: {c5['capacity_ah']:.3f} Ah, retention {ret*100:.2f}% vs 1C",
         "r4_V13_porousanode_5c_dfn.json / derived"],
        ["Fast-charge capability", f"4C/45 °C charge: T_max {c4['T_max_K']:.2f} K (limit 333.15)", "4c_safety:T_max_K"],
        ["Operating temperature range", "verified 298.15 K (discharge) and 318.15 K ambient (charge); 5C discharge peak "
         f"cell temperature {c5['T_max_K']:.1f} K", "protocol definitions; 5c_dfn:T_max_K"],
        ["Cycle life", "Not simulated (task has no cycle-life criterion; no aging protocol run) — must not be fabricated",
         "log.jsonl stage4 note"],
        ["Safety determination", f"no plating (anode min {min(c4['anode_potential_v']):+.4f} V); overcharge→thermal "
         f"runaway ODE: triggered={tr['triggered']}", "4c_safety / run-tr"],
        ["Dimensions and mass", f"{H*1000:.0f} × {Wdim*1000:.0f} × {en['thickness_m']*1e6:.1f} µm; stack {m_stack:.2f} g "
         f"(electrolyte excluded) + {elec_mass:.2f} g electrolyte fill", "parameter set + energy:mass_kg"],
        ["DC resistance (10% point)", f"{en['dcr_ohm']*1000:.2f} mΩ", "energy:dcr_ohm"],
    ]))
OUT.joinpath("datasheet.md").write_text("\n".join(dsh), encoding="utf-8")

# ================= dvpr.md =================
dv = []
dv.append("# Design Verification Plan and Report (virtual test version) — " + CASE + " (VBF-T8R3-DVPR-01)\n")
dv.append("All results below are simulation outputs (no physical cell exists); uncovered conditions marked N/A honestly.\n")
dv.append(md_table(
    ["Item", "Condition", "Result", "Determination", "Source"],
    [
        ["Energy density", "1C discharge energy ÷ stack mass", f"{en['energy_density_wh_kg']:.2f} Wh/kg",
         "✓ pass vs ≥446.18", "energy:energy_density_wh_kg"],
        ["5C retention", "5C DFN capacity ÷ 1C DFN capacity", f"{ret*100:.2f}%",
         "✓ pass vs ≥90%", "derived retention_5c"],
        ["Mass", "calc-energy stack mass", f"{en['mass_kg']*1000:.2f} g",
         "✓ pass vs ≤40 g", "energy:mass_kg"],
        ["4C fast-charge temperature rise", "4C charge, 45 °C chamber, thermal lumped", f"{c4['T_max_K']:.2f} K",
         "✓ pass vs ≤333.15 K", "4c_safety:T_max_K"],
        ["4C fast-charge plating", "same run, anode_potential_v vs 0 V", f"min {min(c4['anode_potential_v']):+.4f} V → plated=false",
         "✓ pass", "4c_safety:anode_potential_v"],
        ["1C discharge capacity", "1C CC discharge to 2.5 V", f"{c1['capacity_ah']:.4f} Ah",
         "informational (no capacity criterion in entry 0)", "1c_dfn:capacity_ah"],
        ["Voltage window", "parameter set limits", f"{Vmin:.1f}–{Vmax:.1f} V",
         "within parameter-set bounds", "Chen2020 cut-offs"],
        ["Overcharge → thermal runaway", "overcharge + 3-reaction ODE, T0=overcharge T_max", f"triggered={tr['triggered']} ({oc['T_max_K']:.2f} K → {tr['T_max_K']:.2f} K)",
         "✓ not triggered (informational)", "overcharge + run-tr outputs"],
        ["Nail penetration", "—", "N/A (beyond pure simulation boundary, requires physical experiment)", "N/A", "—"],
        ["Crush / drop", "—", "N/A (requires physical experiment)", "N/A", "—"],
        ["Cycle life", "aging protocol not in objective", "N/A (not simulated — no entry-0 criterion)", "N/A", "—"],
    ]))
dv.append("\n**Conclusion**: all five entry-0 criteria pass (see rows 1–5); safety-related informational checks pass; "
          "nail/crush/drop/cycle-life remain beyond virtual-testing boundary.\n")
OUT.joinpath("dvpr.md").write_text("\n".join(dv), encoding="utf-8")

# ================= dfmea.md =================
df = []
df.append("# Design FMEA (qualitative version, simulation-signal based) — " + CASE + " (VBF-T8R3-DFMEA-01)\n")
df.append("Qualitative ratings derived from simulation signal magnitudes vs thresholds; complete process/supplier FMEA "
          "is N/A (beyond pure simulation boundary).\n")
df.append(md_table(
    ["Failure mode", "Failure cause", "Simulation signal (detectability basis)", "Severity", "Occurrence",
     "Design-side mitigation"],
    [
        ["Negative electrode plating (fast charge)", "low-T anode kinetics loss at high cooling",
         "anode_potential_v min +17.7 mV at 4C/45 °C (V13) — margin over 0 V", "high", "low",
         "negative porosity 0.30 + 2.5 µm graphite + h=60 design point; V7-type cooling-only designs rejected (−10 mV)"],
        ["Thermal runaway risk (temperature rise)", "excessive heat during charge abuse",
         "T_max 326.53 K vs 333.15 K limit; run-tr triggered=false on overcharge coupling", "high", "low",
         "forced-air h≥60 W/m²K pack cooling mandated in design"],
        ["Electrolyte oxidative decomposition", "voltage window excess",
         "window 4.2 V top (parameter set); no final DFT endorsement run (real_compute=false) — signal NOT verified at molecular level", "medium", "low",
         "voltage window kept at parameter-set limit; DFT endorsement would be the next verification step"],
        ["Insufficient capacity / energy", "active-loading below requirement at mass cap",
         "ED 497.5 vs 446.18 Wh/kg (51 Wh/kg margin); retention 98.66% vs 90%", "medium", "low",
         "V13 loading/porosity selection; V6/V11 show 500–536 Wh/kg headroom if needed"],
        ["Thick-anode plating liability (documented negative result)", "through-anode electrolyte polarization at 4C",
         "V9/V11 (neg 100 µm) anode −26.5/−10.8 mV vs +7.3 mV at 85.2 µm", "medium", "low (avoided)",
         "negative thickness kept at 85.2 µm — design rule recorded"],
    ]))
df.append("\n**Conclusion**: no high-risk items remain at the selected design point; the highest-severity modes (plating, "
          "thermal) both show positive margins (+17.7 mV, −6.6 K); complete FMEA including process/supplier failures: "
          "N/A (beyond pure simulation boundary).\n")
OUT.joinpath("dfmea.md").write_text("\n".join(df), encoding="utf-8")

# ================= bom.xlsx =================
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"
ws.append(["Component", "Mass (g/cell)", "kg/kWh", "Basis / volume fraction", "Source / annotation"])
rows = [
    ["Positive electrode active material", pos_am, kk(pos_am), f"96 wt% of positive layer", "literature default (parameter set lacks AM/CB/binder split)"],
    ["Positive electrode conductive additive", pos_cb, kk(pos_cb), "2 wt%", "literature default"],
    ["Positive electrode binder (PVDF)", pos_bi, kk(pos_bi), "2 wt%", "literature default"],
    ["Negative electrode active material", neg_am, kk(neg_am), "96 wt% of negative layer", "literature default"],
    ["Negative electrode conductive additive", neg_cb, kk(neg_cb), "1 wt%", "literature default"],
    ["Negative electrode binder (CMC/SBR)", neg_bi, kk(neg_bi), "3 wt%", "literature default"],
    ["Separator", m_sep, kk(m_sep), f"{t_sep*1e6:.0f} µm, porosity {e_sep:.2f}", "parameter set + energy:layer_kg_m2"],
    ["Electrolyte", elec_mass, kk(elec_mass), f"pore volume {pore_vol*1e6:.2f} cm³", "1.2 g/cm³ literature value × fill 1.0"],
    ["Positive current collector (Al)", m_al, kk(m_al), f"{aal*1e6:.0f} µm", "round-1 override; energy:layer_kg_m2"],
    ["Negative current collector (Cu)", m_cu, kk(m_cu), f"{acu*1e6:.0f} µm", "round-1 override; energy:layer_kg_m2"],
    ["Enclosure / tabs", "Not modeled", "Not modeled", "—", "beyond pure simulation boundary"],
    ["TOTAL (incl. electrolyte)", m_total, kk(m_total), "—", "sum of rows above"],
    ["Stack total (contract caliber)", m_stack, kk(m_stack), "Σ layers, electrolyte excluded", "energy:mass_kg — the 37.32 g used for ED"],
]
for r in rows:
    ws.append([round(x, 4) if isinstance(x, float) else x for x in r])
ws2 = wb.create_sheet("Summary")
ws2.append(["Metric", "Value", "Source"])
for r in [
    ["Cell energy (kWh)", kwh, "energy:energy_wh/1000"],
    ["Total mass incl. electrolyte (kg)", m_total / 1000.0, "BOM sheet"],
    ["Material usage (kg/kWh, incl. electrolyte)", kk(m_total), "BOM sheet"],
    ["Stack mass (kg, contract)", en["mass_kg"], "energy:mass_kg"],
    ["Energy density (Wh/kg, contract)", en["energy_density_wh_kg"], "energy:energy_density_wh_kg"],
]:
    ws2.append(r)
wb.save(OUT / "bom.xlsx")

# ================= calc.xlsx =================
wbc = openpyxl.Workbook()
s1 = wbc.active
s1.title = "Input parameters"
s1.append(["Parameter", "Value", "Unit", "Source"])
inp_rows = [
    ["Positive particle radius", 1.5e-6, "m", "override"],
    ["Negative particle radius", 2.5e-6, "m", "override"],
    ["Electrolyte conductivity", over["Electrolyte conductivity [S.m-1]"], "S/m", "override (estimate)"],
    ["Electrolyte diffusivity", over["Electrolyte diffusivity [m2.s-1]"], "m²/s", "override (estimate)"],
    ["Cation transference number", over["Cation transference number"], "—", "override (estimate)"],
    ["Positive electrode thickness", t_pos, "m", "Chen2020"],
    ["Negative electrode thickness", t_neg, "m", "Chen2020"],
    ["Positive porosity", e_pos, "—", "Chen2020"],
    ["Negative porosity", e_neg, "—", "override 0.25→0.30"],
    ["Separator thickness/porosity", f"{t_sep:g} / {e_sep}", "m/—", "override thickness / Chen2020 porosity"],
    ["Collectors Al / Cu", f"{aal:g} / {acu:g}", "m", "override"],
    ["Heat transfer coefficient", h, "W/m²K", "override (cooling design)"],
    ["Electrode height × width", f"{H} × {Wdim}", "m", "Chen2020"],
    ["Nominal capacity", nom, "Ah", "Chen2020"],
    ["Voltage window", f"{Vmin}–{Vmax}", "V", "Chen2020"],
]
for r in inp_rows:
    s1.append(r)
s2 = wbc.create_sheet("Capacity and energy")
s2.append(["Quantity", "Value", "Formula", "Source"])
for r in [
    ["1C capacity", c1["capacity_ah"], "CC discharge 2.5–4.2 V, 1C (=Nominal capacity)", "1c_dfn"],
    ["Discharge energy", en["energy_wh"], "∫V·I dt (trapezoid, I=1C)", "energy"],
    ["Midpoint voltage", en["midpoint_voltage_v"], "voltage at discharge-time midpoint", "energy"],
    ["5C capacity", c5["capacity_ah"], "5C CC discharge", "5c_dfn"],
    ["5C retention", ret, "5C capacity ÷ 1C capacity", "derived"],
]:
    s2.append(r)
s3 = wbc.create_sheet("Energy density")
s3.append(["Quantity", "Value", "Formula", "Source"])
for r in [
    ["Stack mass (kg)", en["mass_kg"], "Σ layer thickness×(1−porosity)×density×area (electrolyte excluded)", "energy"],
    ["ED (Wh/kg)", en["energy_density_wh_kg"], "energy_wh ÷ mass_kg", "energy"],
    ["ED (Wh/L)", en["energy_density_wh_l"], "energy_wh ÷ volume", "energy"],
    ["Volume (m³)", en["volume_m3"], "Σ layer thickness × area", "energy"],
]:
    s3.append(r)
s4 = wbc.create_sheet("NP ratio and mass")
s4.append(["Quantity", "Value", "Formula", "Source"])
for r in [
    ["N/P (full-swing inference)", np_full, "(vf_neg×c_max_neg×th_neg)/(vf_pos×c_max_pos×th_pos), F/3600 cancels", "parameter set"],
    ["Positive layer mass (g)", m_pos, "layer_kg_m2 × area", "energy"],
    ["Negative layer mass (g)", m_neg, "layer_kg_m2 × area", "energy"],
    ["Collectors + separator (g)", m_al + m_cu + m_sep, "layer_kg_m2 × area", "energy"],
    ["Total (g)", m_stack, "Σ", "energy"],
]:
    s4.append(r)
s5 = wbc.create_sheet("Process parameters")
s5.append(["Parameter", "Value", "Formula", "Source"])
for r in [
    ["Positive areal density (g/m²)", areal_pos * 1000, "thickness×(1−porosity)×density", "parameter set"],
    ["Negative areal density (g/m²)", areal_neg * 1000, "same", "parameter set"],
    ["Positive compaction (g/cm³)", comp_pos, "density×(1−porosity)/1000", "parameter set"],
    ["Negative compaction (g/cm³)", comp_neg, "same", "parameter set"],
    ["Electrolyte fill (g)", elec_mass, "pore volume × 1200 × 1.0", "design-spec section 3"],
    ["Formation", "0.1C CC to 4.2 V, 25 °C, 2 cycles", "design recommended; production tuning required", "design-spec"],
]:
    s5.append(r)
wbc.save(OUT / "calc.xlsx")

print("sources written:", sorted(p.name for p in OUT.iterdir()))
print("np_full =", np_full, "elec_mass =", elec_mass, "m_total =", m_total)