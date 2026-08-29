# -*- coding: utf-8 -*-
"""N/P ratio: mechanical derivation from parameter-set OCP functions at the voltage cutoffs.

Q_i unit areal capacity [Ah/m2 per stoich-unit] = c_max_i * volfrac_i * th_i * F / 3600
Lithium conservation between initial state and each endpoint:
    x_n(x_p) = x_n0 - (x_p - x_p0) * Qp_unit / Qn_unit
Endpoint equilibrium (no overpotential, marked inferred):
    OCP_p(x_p) - OCP_n(x_n) = V_target   (4.2 V charge end / 2.5 V discharge end)
"""
import csv
import json
from pathlib import Path

import numpy as np
import pybamm
from scipy.optimize import brentq

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
pv = pybamm.ParameterValues("OKane2022")
ov = json.loads((WS / "candidates" / "r4_archN_params.json").read_text(encoding="utf-8-sig"))
pv.update(ov)

F = 96485.3

def _ocp_csv(path):
    xs, ys = [], []
    with open(path, newline="") as fh:
        for row in csv.reader(fh):
            if not row or not row[0].strip() or row[0].strip()[0] in "#abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                continue
            xs.append(float(row[0])); ys.append(float(row[1]))
    xa, ya = np.asarray(xs), np.asarray(ys)
    return lambda x: float(np.interp(x, xa, ya))

ocp_p = _ocp_csv(r"D:\research\degradation_prognostics\Battery_Design_Agent\.venv\Lib\site-packages\pybamm\input\parameters\lithium_ion\data\nmc_LGM50_ocp_Chen2020.csv")
ocp_n = _ocp_csv(r"D:\research\degradation_prognostics\Battery_Design_Agent\.venv\Lib\site-packages\pybamm\input\parameters\lithium_ion\data\graphite_LGM50_ocp_Chen2020.csv")

c_p = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
c_n = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
x_p0 = float(pv["Initial concentration in positive electrode [mol.m-3]"]) / c_p
x_n0 = float(pv["Initial concentration in negative electrode [mol.m-3]"]) / c_n
th_p = float(pv["Positive electrode thickness [m]"])
th_n = float(pv["Negative electrode thickness [m]"])
vf_p = float(pv["Positive electrode active material volume fraction"])
vf_n = float(pv["Negative electrode active material volume fraction"])
Qp_unit = c_p * vf_p * th_p * F / 3600.0
Qn_unit = c_n * vf_n * th_n * F / 3600.0

def x_n_of(x_p):
    return x_n0 - (x_p - x_p0) * Qp_unit / Qn_unit

def f(x_p, v):
    return ocp_p(x_p) - ocp_n(x_n_of(x_p)) - v

print(f"x_p0={x_p0:.4f} x_n0={x_n0:.4f}  equil V at initial = {ocp_p(x_p0) - ocp_n(x_n0):.4f}")
print(f"Qp_unit={Qp_unit:.2f} Ah/m2 per x-unit, Qn_unit={Qn_unit:.2f} Ah/m2 per x-unit")

for vname, v in (("4.2V charge end", 4.2), ("2.5V discharge end", 2.5)):
    # bracket search
    lo, hi = 0.001, 0.999
    while f(lo, v) * f(hi, v) > 0 and hi - lo > 1e-6:
        if f(lo, v) > f(hi, v):  # decreasing in x_p -> shrink top
            hi -= 0.02
        else:
            lo += 0.02
    try:
        x_p = brentq(lambda x: f(x, v), lo, hi)
    except ValueError:
        print(f"{vname}: no root in bracket; f(0.001)={f(0.001,v):.4f} f(0.999)={f(0.999,v):.4f}")
        continue
    print(f"{vname}: x_p={x_p:.4f}  x_n={x_n_of(x_p):.4f}  Qp at this endpoint vs init = {(x_p-x_p0)*Qp_unit:.3f} Ah/m2")

# usable ranges via the two endpoint solves above are collected manually; compute here directly
def solve(v):
    lo, hi = 0.001, 0.999
    fl, fh = f(lo, v), f(hi, v)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        fm = f(mid, v)
        if fl * fm <= 0:
            hi, fh = mid, fm
        else:
            lo, fl = mid, fm
    return 0.5 * (lo + hi)

x_p_hi, x_p_lo = solve(4.2), solve(2.5)
x_n_hi, x_n_lo = x_n_of(x_p_lo), x_n_of(x_p_hi)
dQp = (x_p_hi - x_p_lo) * Qp_unit
dQn = (x_n_hi - x_n_lo) * Qn_unit
area = float(pv["Electrode height [m]"]) * float(pv["Electrode width [m]"])
print(f"\nusable ranges: x_p {x_p_lo:.4f}->{x_p_hi:.4f} (dQ={dQp:.2f} Ah/m2, {dQp*area:.3f} Ah)")
print(f"usable ranges: x_n {x_n_hi:.4f}->{x_n_lo:.4f} (dQ={dQn:.2f} Ah/m2, {dQn*area:.3f} Ah)")
print(f"N/P = neg/pos = {dQn/dQp:.4f}")
