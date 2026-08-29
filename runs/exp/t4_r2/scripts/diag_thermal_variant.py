# -*- coding: utf-8 -*-
"""t4_r2 diagnostic: replicate runner 1C DFN exactly (lumped) vs isothermal."""
import json
import os
import pybamm
from bda.simulators.pybamm_runner import _cell_volume_default  # noqa: F401  (not needed)

HERE = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t4_r2"
E3 = json.load(open(os.path.join(HERE, "cell", "params_E3.json"), encoding="utf-8"))


def run(options, tag):
    pv = pybamm.ParameterValues("Chen2020")
    pv.update(E3)
    pv.update({"Ambient temperature [K]": 298.15}, check_already_exists=False)
    sim = pybamm.Simulation(
        pybamm.lithium_ion.DFN(options=options),
        experiment=pybamm.Experiment(["Discharge at 1C until 2.5 V"]),
        parameter_values=pv,
    )
    sol = sim.solve()
    vv = sol["Terminal voltage [V]"].entries
    xt = sol["Time [s]"].entries
    xn = sol["Negative electrode stoichiometry"].entries
    xp = sol["Positive electrode stoichiometry"].entries
    print(f"{tag}: t_end {xt[-1]:.1f}s cap {xt[-1]*5/3600:.4f} v0 {vv[0]:.4f} vN {vv[-1]:.4f} xn {xn[0]:.4f}->{xn[-1]:.4f} xp {xp[0]:.4f}->{xp[-1]:.4f}")
    return sol


run({}, "isothermal")
run({"thermal": "lumped"}, "lumped")