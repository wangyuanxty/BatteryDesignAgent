"""Extract all deliverable numbers mechanically from outputs + parameter set.

Reads only: cell/*.json outputs, params_r3.json, Chen2020 parameter set.
Writes: cell/deliverable_numbers.json (single source for deliverable generation).
"""
import json
from pathlib import Path

import pybamm

CELL = Path("runs/exp/t2_r1_singlemodel/cell")
LOG = Path("runs/exp/t2_r1_singlemodel/log.jsonl")

entries = [json.loads(l) for l in LOG.read_text(encoding="utf-8-sig").splitlines()]
criteria = entries[0]["criteria"]

pv = pybamm.ParameterValues("Chen2020")
params = json.loads((CELL / "params_r3.json").read_text(encoding="utf-8-sig"))
pv.update(params)


def load(name):
    return json.loads((CELL / name).read_text(encoding="utf-8-sig"))


def P(key):
    return float(pv[key])


energy = load("r3_energy.json")
one_c = load("r3_1c_dfn.json")
lowt = load("r3_lowT.json")
c4_45 = load("r3_4c45.json")
c4_25 = load("r3_4c25_conservative.json")
aging100 = load("r3_aging100.json")
ret = load("derived_retention_lowT_r3.json")
tr = load("r3_tr.json")
tr_nail = load("r3_tr_nail.json")

# aging500: prefer the final-params file if it has 500 complete cycles
aging500 = load("r3_aging500.json")
aging500_source = "cell/r3_aging500.json"
if len(aging500["cycle_numbers"]) < 500:
    alt = load("r3_aging500_d1e19.json")
    if len(alt["cycle_numbers"]) >= 500:
        aging500 = alt
        aging500_source = "cell/r3_aging500_d1e19.json"

# derived 500-cycle SEI (mechanical key-copy per entry-0 notes)
sei500 = {
    "sei_thickness_nm_end_500cyc": aging500["sei_thickness_nm_end"],
    "cycles_completed": len(aging500["cycle_numbers"]),
    "source_file": aging500_source,
    "formula": "sei_thickness_nm_end of aging-500 output, max over x at last completed cycle",
}
(CELL / "derived_sei_500cyc_r3.json").write_text(json.dumps(sei500, indent=1), encoding="utf-8")

n = {
    "criteria": criteria["stage2"],
    "capacity_ah_1C": one_c["capacity_ah"],
    "capacity_ah_lowT": lowt["capacity_ah"],
    "retention_lowT_pct": ret["retention_lowT_pct"],
    "energy_wh": energy["energy_wh"],
    "energy_density_wh_kg": energy["energy_density_wh_kg"],
    "energy_density_wh_l": energy["energy_density_wh_l"],
    "mass_kg": energy["mass_kg"],
    "midpoint_voltage_v": energy["midpoint_voltage_v"],
    "dcr_ohm": energy["dcr_ohm"],
    "power_density_w_kg": energy["power_density_w_kg"],
    "area_m2": energy["area_m2"],
    "layer_kg_m2": energy["layer_kg_m2"],
    "t_max_1C": one_c["T_max_K"],
    "t_max_lowT": lowt["T_max_K"],
    "t_max_4C45": c4_45["T_max_K"],
    "ap_min_4C45": min(c4_45["anode_potential_v"]),
    "ap_min_4C25": min(c4_25["anode_potential_v"]),
    "sei_100_nm": aging100["sei_thickness_nm_end"],
    "sei_500_nm": aging500["sei_thickness_nm_end"],
    "aging500_cycles": len(aging500["cycle_numbers"]),
    "aging500_source": aging500_source,
    "aging500_cap_last_ah": aging500["capacity_ah_per_cycle"][-1],
    "tr_triggered": tr["triggered"],
    "tr_t_max_k": tr["T_max_K"],
    "tr_nail_triggered": tr_nail["triggered"],
    "tr_nail_t_max_k": tr_nail["T_max_K"],
    "tr_nail_trigger_time_s": tr_nail.get("trigger_time_s"),
    # parameter set
    "v_min": P("Lower voltage cut-off [V]"),
    "v_max": P("Upper voltage cut-off [V]"),
    "nominal_capacity_ah": P("Nominal cell capacity [A.h]"),
    "l_pos_m": P("Positive electrode thickness [m]"),
    "l_neg_m": P("Negative electrode thickness [m]"),
    "l_sep_m": P("Separator thickness [m]"),
    "por_pos": P("Positive electrode porosity"),
    "por_neg": P("Negative electrode porosity"),
    "por_sep": P("Separator porosity"),
    "rho_pos": P("Positive electrode density [kg.m-3]"),
    "rho_neg": P("Negative electrode density [kg.m-3]"),
    "l_cc_pos_m": P("Positive current collector thickness [m]"),
    "l_cc_neg_m": P("Negative current collector thickness [m]"),
    "rho_cc_pos": P("Positive current collector density [kg.m-3]"),
    "rho_cc_neg": P("Negative current collector density [kg.m-3]"),
    "height_m": P("Electrode height [m]"),
    "width_m": P("Electrode width [m]"),
    "t_plus": P("Cation transference number"),
    "c_e0": P("Initial concentration in electrolyte [mol.m-3]"),
    "eps_pos_am": P("Positive electrode active material volume fraction"),
    "eps_neg_am": P("Negative electrode active material volume fraction"),
    "r_pos_m": P("Positive particle radius [m]"),
    "r_neg_m": P("Negative particle radius [m]"),
    "h_conv": P("Total heat transfer coefficient [W.m-2.K-1]"),
    "k_sei": P("SEI kinetic rate constant [m.s-1]"),
    "j0_sei": P("SEI reaction exchange current density [A.m-2]"),
    "d_ec": P("EC diffusivity [m2.s-1]"),
    "r_sei_ohm_m": P("SEI resistivity [Ohm.m]"),
    "neg_i0": P("Negative electrode exchange-current density [A.m-2]"),
    "t_init_4C45": 318.15,
    "t_init_4C25": 298.15,
    "t_lowT": 253.15,
}

(CELL / "deliverable_numbers.json").write_text(json.dumps(n, indent=1), encoding="utf-8")
print("wrote cell/deliverable_numbers.json + derived_sei_500cyc_r3.json")
print("aging500 source:", aging500_source, "cycles:", len(aging500["cycle_numbers"]),
      "SEI500:", round(aging500["sei_thickness_nm_end"], 2))
print("SEI100:", round(aging100["sei_thickness_nm_end"], 2))
