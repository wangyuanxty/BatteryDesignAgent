# -*- coding: utf-8 -*-
"""Shared deliverable data for t6_r1_noceiling (design ED-Compact B-p).

All conclusion-grade numbers are mechanical values from tool output files
(cell/r2_bp_*.json, cell/r4_bp_aging.json) or the Chen2020 parameter set.
No numbers written from memory.
"""
from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parent
DELIV = CASE_ROOT / "deliverables"
CASE_NAME = "exp/t6_r1_noceiling"
CASE_ID = "T6R1NOCEILING"
GEN_DATE = "2026-08-25"

# --- simulation outputs (cell/r2_bp_energy.json) ---
ENERGY_WH = 18.601222347864425
ENERGY_KWH = ENERGY_WH / 1000.0
MASS_KG = 0.03965656259500001
MASS_G = MASS_KG * 1000.0
VOLUME_M3 = 1.9287060000000004e-05
ED_WH_L = 964.4405289279143
ED_WH_KG = 469.0578590442357
MIDPOINT_V = 3.921427550822483
DCR_OHM = 0.0003636012830776636
POWER_DENSITY_W_KG = 283313.20463461475
AREA_M2 = 0.1027
LAYER_KG_M2 = {
    "positive_electrode": 0.17262503999999998,
    "negative_electrode": 0.11294111999999999,
    "positive_cc": 0.027000000000000003,
    "negative_cc": 0.07168,
    "separator": 0.00189369,
}

# --- other simulation outputs ---
CAPACITY_AH_1C = 5.322205945840946          # cell/r2_bp_1c.json
CAPACITY_AH_NOMINAL = 5.6                    # design nominal (parameter-set reconciliation)
TMAX_4C_K = 351.004                          # cell/r2_bp_4c.json
ANODE_MIN_4C_V = -0.2566                     # cell/r2_bp_4c.json
CAP_4C_AH = 0.096                            # cell/r2_bp_4c.json
SEI_END_NM = 417.743                         # cell/r4_bp_aging.json
AGING_CAP_START_AH = 1.798                   # cell/r4_bp_aging.json (artifact-annotated)
AGING_CAP_END_AH = 2.151                     # cell/r4_bp_aging.json (artifact-annotated)
TMAX_B_H25_K = 338.657                       # cell/r3_bh25_4c.json (family datum, h=25)

# --- parameter set values (Chen2020 + params_r2_bp.json) ---
THICKNESS_UM = {"pos": 75.6, "neg": 85.2, "sep": 9.0, "al": 10.0, "cu": 8.0}
POROSITY = {"pos": 0.30, "neg": 0.20, "sep": 0.47}
ACTIVE_FRAC = {"pos": 0.70, "neg": 0.80}
DENSITY = {"pos": 3262.0, "neg": 1657.0, "sep": 397.0, "al": 2700.0, "cu": 8960.0}
RADIUS_UM = {"pos": 5.22, "neg": 4.0}
CMAX = {"pos": 63104.0, "neg": 33133.0}
DELTA_X = {"pos": 0.73, "neg": 0.90}         # dischargeable window (OCP window basis)
ELECTRODE_H_MM = 65.0                        # Electrode height [mm]
ELECTRODE_W_MM = 1580.0                      # Electrode width [mm]
V_LOW = 2.5
V_HIGH = 4.2
T_PLUS = 0.2594
H_COOLING = 10.0                             # contract default cooling
COOLING_AREA_M2 = 0.00531                    # parameter-set wound-cell value (locked)
STACK_UM = sum(THICKNESS_UM.values())        # 187.8 um
F_AMOUNT_AH = 26.8                           # Ah/mol for the areal-capacity computation

# --- derived ---
def comp_mass_g(key):
    return LAYER_KG_M2[key] * AREA_M2 * 1000.0

MASS_POS_G = comp_mass_g("positive_electrode")
MASS_NEG_G = comp_mass_g("negative_electrode")
MASS_AL_G = comp_mass_g("positive_cc")
MASS_CU_G = comp_mass_g("negative_cc")
MASS_SEP_G = comp_mass_g("separator")

PORE_VOL_CM3 = (sum(THICKNESS_UM[k] * 1e-6 * POROSITY[k] for k in ("pos", "neg", "sep"))
                * AREA_M2) * 1e6              # cm^3
ELEC_DENSITY_G_CM3 = 1.2                     # literature value (annotated)
MASS_ELEC_G = PORE_VOL_CM3 * ELEC_DENSITY_G_CM3

# binder / conductive additive: literature defaults (parameter set has no such params)
MASS_POS_BINDER_G = MASS_POS_G * 0.02        # PVDF 2 wt% of coating solid
MASS_POS_CARBON_G = MASS_POS_G * 0.02        # 2 wt%
MASS_NEG_BINDER_G = MASS_NEG_G * 0.02        # CMC+SBR 2 wt%
MASS_NEG_CARBON_G = MASS_NEG_G * 0.01        # 1 wt%
MASS_GRAND_TOTAL_G = (MASS_G + MASS_ELEC_G + MASS_POS_BINDER_G + MASS_POS_CARBON_G
                      + MASS_NEG_BINDER_G + MASS_NEG_CARBON_G)

def g_to_kg_kwh(g):
    return g / ENERGY_WH                       # kg/kWh = g/Wh numerically

# N/P ratio (areal discharge capacity ratio)
NEG_AREAL_AH_M2 = CMAX["neg"] * ACTIVE_FRAC["neg"] * THICKNESS_UM["neg"] * 1e-6 * DELTA_X["neg"] * F_AMOUNT_AH
POS_AREAL_AH_M2 = CMAX["pos"] * ACTIVE_FRAC["pos"] * THICKNESS_UM["pos"] * 1e-6 * DELTA_X["pos"] * F_AMOUNT_AH
NP_RATIO = NEG_AREAL_AH_M2 / POS_AREAL_AH_M2

# compaction density
COMPACTION_POS_G_CM3 = DENSITY["pos"] * ACTIVE_FRAC["pos"] / 1000.0
COMPACTION_NEG_G_CM3 = DENSITY["neg"] * ACTIVE_FRAC["neg"] / 1000.0

# areal density
AREAL_POS_G_M2 = MASS_POS_G / AREA_M2
AREAL_NEG_G_M2 = MASS_NEG_G / AREA_M2

# --- BOM rows: (component, g/cell, kg/kWh, annotation) ---
BOM_ROWS = [
    ("Positive electrode active material (NMC811)", MASS_POS_G, g_to_kg_kwh(MASS_POS_G),
     "thickness 75.6 um x area x volume fraction 0.70 x density 3262 kg/m3 (parameter set + params_r2_bp.json)"),
    ("Positive electrode conductive additive (carbon)", MASS_POS_CARBON_G, g_to_kg_kwh(MASS_POS_CARBON_G),
     "literature default 2 wt% of coating solid (parameter set has no additive params - annotated); addition requires active-fraction rebalance"),
    ("Positive electrode binder (PVDF)", MASS_POS_BINDER_G, g_to_kg_kwh(MASS_POS_BINDER_G),
     "literature default 2 wt% of coating solid (annotated); addition requires active-fraction rebalance"),
    ("Negative electrode active material (graphite)", MASS_NEG_G, g_to_kg_kwh(MASS_NEG_G),
     "thickness 85.2 um x area x volume fraction 0.80 x density 1657 kg/m3 (parameter set + params_r2_bp.json)"),
    ("Negative electrode conductive additive (carbon)", MASS_NEG_CARBON_G, g_to_kg_kwh(MASS_NEG_CARBON_G),
     "literature default 1 wt% of coating solid (annotated); addition requires active-fraction rebalance"),
    ("Negative electrode binder (CMC+SBR)", MASS_NEG_BINDER_G, g_to_kg_kwh(MASS_NEG_BINDER_G),
     "literature default 2 wt% of coating solid (annotated); addition requires active-fraction rebalance"),
    ("Separator", MASS_SEP_G, g_to_kg_kwh(MASS_SEP_G),
     "thickness 9 um x area x density 397 kg/m3; porosity 0.47 (parameter set)"),
    ("Electrolyte", MASS_ELEC_G, g_to_kg_kwh(MASS_ELEC_G),
     "pore volume 4.514 cm3 x electrolyte density 1.2 g/cm3 (literature value - annotated)"),
    ("Positive current collector (Al)", MASS_AL_G, g_to_kg_kwh(MASS_AL_G),
     "thickness 10 um x area x density 2700 kg/m3 (params_r2_bp.json)"),
    ("Negative current collector (Cu)", MASS_CU_G, g_to_kg_kwh(MASS_CU_G),
     "thickness 8 um x area x density 8960 kg/m3 (params_r2_bp.json)"),
    ("Enclosure", None, None, "Not modeled (beyond parameter set) - honest"),
    ("Tabs", None, None, "Not modeled (beyond parameter set) - honest"),
]

# --- calc.xlsx sheet chain ---
CALC_SHEETS = [
    ("Inputs", [
        ("Electrode strip height", "parameter set", 65.0, "mm", "Chen2020 Electrode height [mm]"),
        ("Electrode strip width", "parameter set", 1580.0, "mm", "Chen2020 Electrode width [mm]"),
        ("Electrode area", "height x width", 0.1027, "m2", "calc-energy output area_m2"),
        ("Positive thickness", "parameter set", 75.6, "um", "params_r2_bp.json"),
        ("Negative thickness", "parameter set", 85.2, "um", "params_r2_bp.json"),
        ("Separator thickness", "parameter set", 9.0, "um", "params_r2_bp.json"),
        ("Al collector thickness", "parameter set", 10.0, "um", "params_r2_bp.json"),
        ("Cu collector thickness", "parameter set", 8.0, "um", "params_r2_bp.json"),
        ("Stack thickness", "sum of 5 layers", STACK_UM, "um", "computed"),
        ("Positive porosity", "parameter set", 0.30, "-", "params_r2_bp.json"),
        ("Negative porosity", "parameter set", 0.20, "-", "params_r2_bp.json"),
        ("Positive active volume fraction", "parameter set", 0.70, "-", "params_r2_bp.json"),
        ("Negative active volume fraction", "parameter set", 0.80, "-", "params_r2_bp.json"),
        ("Positive density (NMC811)", "parameter set", 3262.0, "kg/m3", "Chen2020"),
        ("Negative density (graphite)", "parameter set", 1657.0, "kg/m3", "Chen2020"),
        ("Positive particle radius", "parameter set", 5.22, "um", "Chen2020"),
        ("Negative particle radius", "parameter set", 4.0, "um", "params_r2_bp.json"),
        ("Cooling coefficient h", "design lever (10-25)", 10.0, "W/m2K", "contract default"),
        ("Nominal capacity (design)", "loading-reconciled", 5.6, "Ah", "params_r2_bp.json"),
    ]),
    ("Capacity & Energy", [
        ("1C discharge capacity", "run-pyamm 1C_discharge (SPMe)", CAPACITY_AH_1C, "Ah", "cell/r2_bp_1c.json:capacity_ah"),
        ("Discharge current (1C)", "nominal capacity / 1h", 5.6, "A", "protocol definition"),
        ("Discharge energy", "integral V x I dt over 1C discharge", ENERGY_WH, "Wh", "cell/r2_bp_energy.json:energy_wh"),
        ("Voltage window", "parameter set cut-offs", "2.5 - 4.2", "V", "Chen2020 Lower/Upper voltage cut-off"),
        ("Discharge-time midpoint voltage", "V at discharge-time midpoint", MIDPOINT_V, "V", "cell/r2_bp_energy.json:midpoint_voltage_v"),
        ("DC resistance", "10%-discharge definition", DCR_OHM, "ohm", "cell/r2_bp_energy.json:dcr_ohm"),
        ("Power density", "DCR-based (calc-energy definition)", POWER_DENSITY_W_KG, "W/kg", "cell/r2_bp_energy.json:power_density_w_kg"),
    ]),
    ("Energy Density", [
        ("Stack volume", "stack thickness x area", VOLUME_M3, "m3", "calc-energy output volume_m3 (= 19.29 cm3)"),
        ("Volumetric energy density", "energy / volume (contract: electrolyte excluded)", ED_WH_L, "Wh/L", "cell/r2_bp_energy.json:energy_density_wh_l"),
        ("Cell mass (contract)", "electrodes + CCs + separator", MASS_KG, "kg", "calc-energy output mass_kg (39.66 g)"),
        ("Gravimetric energy density", "energy / mass", ED_WH_KG, "Wh/kg", "cell/r2_bp_energy.json:energy_density_wh_kg"),
        ("Criterion ED", "energy_density_wh_l >= 950", "PASS (964.44)", "-", "log entry 0 + log-evaluate"),
    ]),
    ("N-P & Mass", [
        ("Positive areal discharge capacity", "c_max x active frac x thickness x delta_x x 26.8 Ah/mol", POS_AREAL_AH_M2, "Ah/m2", "computed from parameter set"),
        ("Negative areal discharge capacity", "c_max x active frac x thickness x delta_x x 26.8 Ah/mol", NEG_AREAL_AH_M2, "Ah/m2", "computed from parameter set"),
        ("N/P ratio", "negative areal capacity / positive areal capacity", NP_RATIO, "-", "negative-limited design (Chen2020 characteristic kept)"),
        ("Positive active mass", "layer_kg_m2 x area", MASS_POS_G, "g", "cell/r2_bp_energy.json:layer_kg_m2"),
        ("Negative active mass", "layer_kg_m2 x area", MASS_NEG_G, "g", "cell/r2_bp_energy.json:layer_kg_m2"),
        ("Al collector mass", "layer_kg_m2 x area", MASS_AL_G, "g", "cell/r2_bp_energy.json:layer_kg_m2"),
        ("Cu collector mass", "layer_kg_m2 x area", MASS_CU_G, "g", "cell/r2_bp_energy.json:layer_kg_m2"),
        ("Separator mass", "layer_kg_m2 x area", MASS_SEP_G, "g", "cell/r2_bp_energy.json:layer_kg_m2"),
        ("Total mass (contract)", "sum of the 5 layers", MASS_G, "g", "calc-energy output mass_kg x 1000"),
    ]),
    ("Process Params", [
        ("Positive areal density", "thickness x (1-porosity) x density", AREAL_POS_G_M2, "g/m2", "cell/r2_bp_energy.json:layer_kg_m2"),
        ("Negative areal density", "thickness x (1-porosity) x density", AREAL_NEG_G_M2, "g/m2", "cell/r2_bp_energy.json:layer_kg_m2"),
        ("Positive compaction density", "density x active fraction / 1000", COMPACTION_POS_G_CM3, "g/cm3", "computed (3262 x 0.70 / 1000 = 2.28)"),
        ("Negative compaction density", "density x active fraction / 1000", COMPACTION_NEG_G_CM3, "g/cm3", "computed (1657 x 0.80 / 1000 = 1.33)"),
        ("Electrolyte pore volume", "sum(thickness x porosity) x area", PORE_VOL_CM3, "cm3", "computed from parameter set"),
        ("Electrolyte fill amount", "pore volume x electrolyte density (1.2 g/cm3 literature)", MASS_ELEC_G, "g", "annotated literature value"),
        ("Formation recommendation", "-", "0.1C CC to 4.2 V, 25 C, 2 cycles", "-", "design recommended value; production tuning required"),
        ("Binder / conductive additive", "-", "see BOM (literature defaults, annotated)", "-", "parameter set has no inert-volume params; production must rebalance active fraction"),
    ]),
]

# --- datasheet fields: (field, value) ---
DATASHEET_FIELDS = [
    ("Product / electrochemical system",
     "ED-Compact B-p smartphone cell: NMC811 positive / graphite negative (Chen2020 parameter set). "
     "Electrolyte: EC:EMC + LiPF6 (parameter-set formulation; transport: Nyman2008 functions); cation transference number 0.2594."),
    ("Rated capacity (Ah)",
     "5.6 Ah nominal (design value, loading-reconciled in params_r2_bp.json); 1C simulation-verified 5.3222 Ah "
     "(cell/r2_bp_1c.json:capacity_ah)."),
    ("Nominal voltage / voltage window (V)",
     "Discharge-time midpoint 3.9214 V (cell/r2_bp_energy.json:midpoint_voltage_v); window 2.5 - 4.2 V (parameter set cut-offs)."),
    ("Rated energy (Wh)",
     "18.6012 Wh (1C discharge integration, cell/r2_bp_energy.json:energy_wh)."),
    ("Energy density (Wh/L / Wh/kg)",
     "964.44 Wh/L; 469.06 Wh/kg (contract caliber: electrodes + current collectors + separator; electrolyte excluded - "
     "calc-energy definition)."),
    ("Maximum continuous discharge rate",
     "1C (5.6 A) simulated (SPMe, 25 C). Higher rates not verified - honest."),
    ("Fast-charge capability",
     "4C NOT supported: at 4C charge from empty, 45 C ambient (DFN, lumped thermal, h = 10 W/m2K) the anode potential "
     "minimum reaches -0.2566 V -> lithium plating (cell/r2_bp_4c.json:anode_potential_v), T_max 351.0 K (same file), "
     "4C charge acceptance 0.096 Ah before the 4.2 V limit. Design-side recommendation: derate charge to <= 2C "
     "(qualitative, not simulation-verified)."),
    ("Operating temperature range",
     "Simulated at 25 C ambient (1C discharge, 1C aging) and 45 C ambient (4C charge). T_max at 4C/45 C exceeds the 50 C "
     "limit -> 4C operation not permitted. Honest operating statement: <= 45 C ambient with derated charge."),
    ("Cycle life",
     "Aging simulated (aging_1C_100cyc, isothermal 25 C): anode SEI 417.74 nm after 100 cycles - within the 500 nm limit "
     "(cell/r4_bp_aging.json:sei_thickness_nm_end). Capacity trajectory 1.798 -> 2.151 Ah shows the climb-then-saturate "
     "artifact (lithium-loss window shift; Chen2020 set starts discharged) - annotated, NOT treated as normal degradation. "
     "Cycle life to 80% capacity: Not simulated (beyond the aging protocol)."),
    ("Safety determination",
     "4C plating: FAIL (plated). 4C/45 C temperature: FAIL (351.0 K > 323.15 K). Anode SEI after 100 cycles: PASS "
     "(417.74 nm <= 500 nm). Mechanical verdicts from log-evaluate (batch r4)."),
    ("Dimensions and mass",
     "Electrode strip 1580 mm x 65 mm; stack thickness 187.8 um (pos 75.6 / neg 85.2 / sep 9 / Al 10 / Cu 8 um); "
     "contract volume 19.29 cm3; mass 39.66 g (contract caliber, electrolyte excluded) + electrolyte 5.42 g (pore volume "
     "4.514 cm3 x 1.2 g/cm3 literature density)."),
    ("DC resistance",
     "0.364 mohm (10%-discharge definition, cell/r2_bp_energy.json:dcr_ohm)."),
    ("Power density",
     "283313 W/kg (DCR-based, cell/r2_bp_energy.json:power_density_w_kg)."),
    ("Voltage plateau vs spec",
     "3.9214 V vs >= 4.1 V criterion -> FAIL (NMC811 cathode OCP ceiling ~4.0 V; recorded in log final.escalation)."),
]

# --- performance verification table (design_spec section 5 / dvpr) ---
PERF_ROWS = [
    ("1C discharge capacity", "(reporting)", "5.3222 Ah (nominal 5.6)", "within 5% of nominal",
     "cell/r2_bp_1c.json:capacity_ah"),
    ("Volumetric energy density", ">= 950 Wh/L", "964.44 Wh/L", "PASS", "cell/r2_bp_energy.json:energy_density_wh_l"),
    ("Gravimetric energy density", "(reporting)", "469.06 Wh/kg", "-", "cell/r2_bp_energy.json:energy_density_wh_kg"),
    ("Voltage plateau", ">= 4.1 V", "3.9214 V", "FAIL", "cell/r2_bp_energy.json:midpoint_voltage_v"),
    ("4C fast charge - plating", "plated = false", "plated = true (anode min -0.2566 V)", "FAIL", "cell/r2_bp_4c.json:anode_potential_v"),
    ("4C fast charge - temperature", "<= 50 C (323.15 K)", "T_max 351.004 K (h=10); h=25 family datum 338.7 K", "FAIL",
     "cell/r2_bp_4c.json:T_max_K; cell/r3_bh25_4c.json"),
    ("4C charge acceptance", "(reporting)", "0.096 Ah before 4.2 V limit", "poor fast-charge support", "cell/r2_bp_4c.json:capacity_ah"),
    ("Anode SEI after 100 cycles (1C)", "<= 500 nm", "417.74 nm", "PASS", "cell/r4_bp_aging.json:sei_thickness_nm_end"),
]
