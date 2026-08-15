import pybamm

PROTOCOLS = {
    "1C_discharge": {"kind": "discharge", "C_rate": 1.0, "t_end_s": 3600.0, "T_amb_K": 298.15},
    "4C_charge_45C": {"kind": "charge", "C_rate": 4.0, "t_end_s": 900.0, "T_amb_K": 318.15},
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

    def _solve(model):
        sim = pybamm.Simulation(model, parameter_values=parameter_values)
        sim.solve([0, p["t_end_s"]])
        return sim.solution

    model_used = "DFN" if mode == "dfn" else "SPMe"
    try:
        sol = _solve(pybamm.lithium_ion.DFN() if mode == "dfn" else pybamm.lithium_ion.SPMe())
    except pybamm.SolverError:
        if mode == "dfn" and fallback:
            sol = _solve(pybamm.lithium_ion.SPMe())
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
