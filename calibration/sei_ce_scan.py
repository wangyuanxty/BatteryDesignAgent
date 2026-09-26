# -*- coding: utf-8 -*-
"""CE-vs-k scan -> inversion table. Same setup as bda run-pyamm aging_1C_100cyc (Chen2020, SPMe, 1C, isothermal)."""
import io, sys, numpy as np, pybamm
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
exp = pybamm.Experiment([("Discharge at 1C until 2.5 V", "Charge at 1C until 4.2 V")] * 100)

def run(k):
    pv = pybamm.ParameterValues('Chen2020')
    pv.update({"SEI kinetic rate constant [m.s-1]": k})
    pv.update({"Ambient temperature [K]": 298.15}, check_already_exists=False)
    m = pybamm.lithium_ion.SPMe(options={"SEI": "ec reaction limited", "thermal": "isothermal"})
    sol = pybamm.Simulation(m, experiment=exp, parameter_values=pv).solve()
    qd, loss = [], []
    for i in range(len(sol.cycles)):
        qd.append(float(np.asarray(sol.cycles[i]["Discharge capacity [A.h]"].entries).reshape(-1)[-1]))
        loss.append(float(np.asarray(sol.cycles[i]["Loss of capacity to negative SEI [A.h]"].entries).reshape(-1)[-1]))
    qd, loss = np.array(qd), np.array(loss)
    ce = qd / (qd + np.diff(loss, prepend=loss[0])) * 100.0
    L = float(np.asarray(sol.cycles[-1]["Negative SEI thickness [m]"].entries[-1]).max()) * 1e9
    return ce[9:].mean(), L

MULTS = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001, 0.0003, 0.0001]
res = []
for mu in MULTS:
    ce, L = run(1e-12 * mu)
    res.append((mu, ce, L))
    print(f"k x {mu:<9g}  SEI={L:8.2f} nm   CE(mean 10..100) = {ce:.4f}%")

base_ce = res[0][1]
print("\n-- CE-loss ratio (relative to baseline) --")
for mu, ce, L in res:
    print(f"k x {mu:<9g}  CE loss = {100-ce:.4f} pp   loss/loss_base = {(100-ce)/(100-base_ce):.4f}")
