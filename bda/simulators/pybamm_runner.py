import pybamm

PROTOCOLS = {
    "1C_discharge": {"kind": "discharge", "C_rate": 1.0, "t_end_s": 3600.0, "T_amb_K": 298.15},
    "4C_charge_45C": {"kind": "charge", "C_rate": 4.0, "t_end_s": 900.0, "T_amb_K": 318.15},
}

# Standard lithium plating parameter values (constant approximation of PyBaMM's
# OKane2022 set). The default Chen2020 parameter set has no plating parameters, so
# they must be supplied whenever the plating option is enabled.
PLATING_PARAM_DEFAULTS = {
    "Initial plated lithium concentration [mol.m-3]": 0.0,
    "Typical plated lithium concentration [mol.m-3]": 1000.0,
    "Lithium plating transfer coefficient": 0.65,
    "Exchange-current density for plating [A.m-2]": 0.001,
    "Exchange-current density for stripping [A.m-2]": 0.001,
}


def run_simulation(
    params: dict,
    protocol: str,
    base: str = "Chen2020",
    mode: str = "spme",
    fallback: bool = True,
    thermal: str = "lumped",
    plating: bool = False,
) -> dict:
    if protocol not in PROTOCOLS:
        raise ValueError(f"unknown protocol '{protocol}'; legal: {sorted(PROTOCOLS)}")
    if mode not in ("spme", "dfn"):
        raise ValueError(f"unknown mode '{mode}'; legal: spme, dfn")
    p = PROTOCOLS[protocol]
    parameter_values = pybamm.ParameterValues(base)
    unknown_params = sorted(name for name in params if name not in parameter_values)
    if unknown_params:
        raise ValueError(f"unknown parameter name(s): {unknown_params}")
    parameter_values.update(params)
    parameter_values.update({"Ambient temperature [K]": p["T_amb_K"]}, check_already_exists=False)
    if plating:
        parameter_values.update(PLATING_PARAM_DEFAULTS, check_already_exists=False)

    options = {}
    if thermal != "isothermal":
        options["thermal"] = "lumped"
    if plating:
        options["lithium plating"] = "irreversible"

    def _solve(model):
        sim = pybamm.Simulation(model, parameter_values=parameter_values)
        sim.solve([0, p["t_end_s"]])
        return sim.solution

    model_used = "DFN" if mode == "dfn" else "SPMe"
    try:
        sol = _solve(
            pybamm.lithium_ion.DFN(options=options)
            if mode == "dfn"
            else pybamm.lithium_ion.SPMe(options=options)
        )
    except pybamm.SolverError:
        if mode == "dfn" and fallback:
            sol = _solve(pybamm.lithium_ion.SPMe(options=options))
            model_used = "SPMe(fallback)"
        else:
            raise

    out = {
        "model_used": model_used,
        "time_s": sol["Time [s]"].entries.tolist(),
        "voltage_v": sol["Terminal voltage [V]"].entries.tolist(),
    }
    if p["kind"] == "discharge":
        out["capacity_ah"] = float(sol["Discharge capacity [A.h]"].entries[-1])
    else:
        out["capacity_ah"] = float(sol["Time [s]"].entries[-1]) * p["C_rate"] / 3600.0
    if thermal != "isothermal":
        out["T_max_K"] = float(sol["Volume-averaged cell temperature [K]"].entries.max())
    if plating:
        out["anode_potential_v"] = sol[
            "Negative electrode surface potential difference at separator interface [V]"
        ].entries.tolist()
    return out
