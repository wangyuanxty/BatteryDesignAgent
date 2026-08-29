"""Gather all final-design (V4) values mechanically for deliverables."""
import json
import pybamm

BASE = "runs/exp/t8_r1_flash"
OUT = {}

# --- simulation outputs ---
def load(name):
    return json.load(open(f"{BASE}/cell/{name}", encoding="utf-8"))

d1c, d5c, e4, r4, c4, ag, ov, tr = (
    load("r1_v4_1c.json"), load("r1_v4_5c.json"), load("r1_v4_energy.json"),
    load("r1_v4_retention.json"), load("r1_v4_4c.json"), load("r1_v4_aging.json"),
    load("r1_v4_ovc.json"), load("r1_v4_tr.json"),
)
OUT["sim"] = {
    "cap_1c_ah": d1c["capacity_ah"], "cap_5c_ah": d5c["capacity_ah"],
    "retention_5c": r4["capacity_retention_5c"],
    "energy_wh": e4["energy_wh"], "mass_kg": e4["mass_kg"],
    "ed_wh_kg": e4["energy_density_wh_kg"], "ed_wh_l": e4["energy_density_wh_l"],
    "thickness_m": e4["thickness_m"], "midpoint_v": e4["midpoint_voltage_v"],
    "dcr_ohm": e4["dcr_ohm"], "power_density_w_kg": e4["power_density_w_kg"],
    "area_m2": e4["area_m2"], "layer_kg_m2": e4["layer_kg_m2"],
    "tmax_5c_K": d5c["T_max_K"], "tmax_4c_K": c4["T_max_K"],
    "anode_min_v": min(c4["anode_potential_v"]),
    "sei_end_nm": ag["sei_thickness_nm_end"],
    "aging_cap_max": max(ag["capacity_ah_per_cycle"]),
    "ovc_tmax_K": ov["T_max_K"], "tr_triggered": tr["triggered"],
    "model_5c": d5c["model_used"], "model_4c": c4["model_used"],
}

# --- parameter set (V4 = Chen2020 + params_r1_v4.json) ---
pv = pybamm.ParameterValues("Chen2020")
ovp = json.load(open(f"{BASE}/params_r1_v4.json", encoding="utf-8"))
pv.update(ovp)
P = {}
keys = [
    "Electrode height [m]", "Electrode width [m]", "Nominal cell capacity [A.h]",
    "Upper voltage cut-off [V]", "Lower voltage cut-off [V]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Separator thickness [m]", "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Cation transference number", "Cell cooling surface area [m2]", "Cell volume [m3]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]", "Negative electrode diffusivity [m2.s-1]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
]
for k in keys:
    v = pv[k]
    P[k] = float(v) if isinstance(v, (int, float)) else (list(v) if isinstance(v, (list, tuple)) else str(v)[:60])

# maximum concentrations (correct PyBaMM names) for N/P
P["pos_cmax"] = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
P["neg_cmax"] = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
OUT["params"] = P

# N/P = (neg areal capacity) / (pos areal capacity) = L(1-eps)cmax*deltax ratios
# deltax from literature stoich windows: NMC811 0.99->0.24 (0.75), graphite ->LiC6 (0.86)
# (Chen2020 set does not expose stoich-limit keys in this PyBaMM version; window lives
#  inside OCP functions -> literature windows marked approximate)
DX_POS, DX_NEG = 0.75, 0.86
np_ratio = (
    (P["Negative electrode thickness [m]"] * (1 - P["Negative electrode porosity"]) * P["neg_cmax"] * DX_NEG)
    / (P["Positive electrode thickness [m]"] * (1 - P["Positive electrode porosity"]) * P["pos_cmax"] * DX_POS)
)
OUT["np_ratio"] = np_ratio
OUT["np_note"] = "literature stoich windows dx_pos=0.75 (NMC811 0.99->0.24), dx_neg=0.86 (graphite->LiC6); approximate, set does not expose stoich-limit keys"

# process parameters
rho_pos = P["Positive electrode density [kg.m-3]"] * (1 - P["Positive electrode porosity"])
rho_neg = P["Negative electrode density [kg.m-3]"] * (1 - P["Negative electrode porosity"])
OUT["process"] = {
    "areal_density_pos_g_m2": P["Positive electrode thickness [m]"] * (1 - P["Positive electrode porosity"]) * P["Positive electrode density [kg.m-3]"] * 1000,
    "areal_density_neg_g_m2": P["Negative electrode thickness [m]"] * (1 - P["Negative electrode porosity"]) * P["Negative electrode density [kg.m-3]"] * 1000,
    "compaction_pos_g_cm3": rho_pos / 1000,
    "compaction_neg_g_cm3": rho_neg / 1000,
    "electrolyte_vol_m3": (
        P["Positive electrode thickness [m]"] * P["Positive electrode porosity"]
        + P["Negative electrode thickness [m]"] * P["Negative electrode porosity"]
        + P["Separator thickness [m]"] * P["Separator porosity"]
    ) * P["Electrode height [m]"] * P["Electrode width [m]"],
    "electrolyte_mass_g": None,  # = vol * 1.2 g/cm3 * fill factor, computed at render
}

json.dump(OUT, open(f"{BASE}/final_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, dict) else "dict") for k, v in OUT["sim"].items()}, indent=1))
print("N/P:", round(OUT["np_ratio"], 3))
print("process:", json.dumps(OUT["process"], indent=1))
