# -*- coding: utf-8 -*-
"""t4_r2 deliverable-input extraction: parameter set keys + output-file scalars.
Mechanical only - every number printed here originates in the Chen2020 parameter
set (overridden by cell/params_E3.json) or in tool output JSONs. No hand-typed values.
"""
import json
import os
import pybamm

HERE = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t4_r2"

pset = pybamm.ParameterValues("Chen2020")
pset.update(json.load(open(os.path.join(HERE, "cell", "params_E3.json"), encoding="utf-8")))

S = pset  # shorthand
F = 96485.33212
KEYS = [
    "Nominal cell capacity [A.h]",
    "Upper voltage cut-off [V]",
    "Lower voltage cut-off [V]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator thickness [m]",
    "Separator porosity",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive electrode active material density [kg.m-3]",
    "Negative electrode active material density [kg.m-3]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell volume [m3]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Initial concentration in electrolyte [mol.m-3]",
]
print("== parameter set ==")
for k in KEYS:
    if k in S:
        print(f"{k} = {float(S[k])}")

def stoich_span(keys):
    for k in keys:
        if k in S:
            v = S[k]
            sub = v.evaluate() if hasattr(v, "evaluate") else v
            if hasattr(sub, "entries"):
                sub = sub.entries[0]
            if hasattr(sub, "left") and hasattr(sub, "right"):
                return float(sub.right() - sub.left())
            return float(sub)
    raise KeyError(keys)

try:
    spos = stoich_span([
        "Initial concentration in positive electrode [mol.m-3] / Maximum concentration in positive electrode [mol.m-3]",
        "Initial concentration in positive electrode [mol.m-3]",
    ])
except Exception as e:
    spos = None
    print("pos stoich span unavailable:", e)
try:
    sneg = stoich_span([
        "Initial concentration in negative electrode [mol.m-3] / Maximum concentration in negative electrode [mol.m-3]",
        "Initial concentration in negative electrode [mol.m-3]",
    ])
except Exception as e:
    sneg = None
    print("neg stoich span unavailable:", e)

cmax_pos = float(S["Maximum concentration in positive electrode [mol.m-3]"])
cmax_neg = float(S["Maximum concentration in negative electrode [mol.m-3]"])
t_pos = float(S["Positive electrode thickness [m]"])
t_neg = float(S["Negative electrode thickness [m]"])
area = float(S["Electrode height [m]"]) * float(S["Electrode width [m]"])
cap_dens_pos = cmax_pos * spos * F / 3600.0 * t_pos  # Ah/m2
cap_dens_neg = cmax_neg * sneg * F / 3600.0 * t_neg
print(f"pos stoich span {spos}, neg stoich span {sneg}")
print(f"cap_density_pos_ah_m2 = {cap_dens_pos}")
print(f"cap_density_neg_ah_m2 = {cap_dens_neg}")
print(f"NP_ratio = {cap_dens_neg/cap_dens_pos}")
print(f"area_m2 = {area}, stack_thickness_m = {t_pos+t_neg+float(S['Separator thickness [m]'])+float(S['Positive current collector thickness [m]'])+float(S['Negative current collector thickness [m]'])}")
pore_vol = (t_pos * float(S["Positive electrode porosity"]) + t_neg * float(S["Negative electrode porosity"]) + float(S["Separator thickness [m]"]) * float(S["Separator porosity"])) * area
print(f"pore_volume_m3 = {pore_vol}")
print(f"electrolyte_mass_kg_at_1200kgm3 = {pore_vol*1200.0}")

print("== outputs ==")
for tag in ["1c_dfn", "lowt_dfn", "4c_dfn2", "energy_dfn"]:
    p = os.path.join(HERE, "cell", f"r5_E3_{tag}.json")
    d = json.load(open(p, encoding="utf-8"))
    if tag == "energy_dfn":
        print(f"energy_dfn: energy_wh={d['energy_wh']}, mass_kg={d['mass_kg']}, w_kg={d['energy_density_wh_kg']}, w_l={d['energy_density_wh_l']}, vol_m3={d['volume_m3']}, thick_m={d['thickness_m']}, mid_V={d['midpoint_voltage_v']}, dcr={d['dcr_ohm']}, power_w_kg={d['power_density_w_kg']}, area={d['area_m2']}")
        print("layer_kg_m2:", json.dumps(d["layer_kg_m2"], ensure_ascii=False))
    if tag == "4c_dfn2":
        ap = d["anode_potential_v"]
        print(f"4c_dfn2: Tmax={d['T_max_K']}, cap={d['capacity_ah']}, ap_min={min(ap)}, neg_pts={sum(1 for x in ap if x<0)}/{len(ap)}, last={ap[-1]}")
    if tag in ("1c_dfn", "lowt_dfn"):
        print(f"{tag}: capacity_ah={d['capacity_ah']}, T_max_K={d.get('T_max_K')}")