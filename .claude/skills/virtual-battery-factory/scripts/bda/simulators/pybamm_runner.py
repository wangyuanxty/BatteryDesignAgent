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

# Legacy parameter sets (Prada2013, Ramadass2004) lack the cell-level geometry and
# collector parameters required by the lumped thermal model, so system candidates
# cannot run stage 2/3 without them. Inject standard defaults (constant
# approximation of the Chen2020/ORegan2022 cell-level values) only when the chosen
# set does not define the parameter itself — mirroring PLATING_PARAM_DEFAULTS.
# "Cell volume [m3]" is NOT taken as a constant: it is derived mechanically from
# each set's own electrode geometry (see _cell_volume_default).
THERMAL_PARAM_DEFAULTS = {
    "Cell cooling surface area [m2]": 0.00531,
    "Total heat transfer coefficient [W.m-2.K-1]": 10.0,
    "Positive current collector conductivity [S.m-1]": 36914000.0,
    "Negative current collector conductivity [S.m-1]": 58411000.0,
    "Positive current collector thickness [m]": 1.6e-05,
    "Negative current collector thickness [m]": 1.2e-05,
    "Positive current collector density [kg.m-3]": 2702.0,
    "Negative current collector density [kg.m-3]": 8933.0,
    "Positive current collector specific heat capacity [J.kg-1.K-1]": 897.0,
    "Negative current collector specific heat capacity [J.kg-1.K-1]": 385.0,
    # Electrode/separator densities and specific heats feed the lumped model's
    # effective heat capacity. These are NMC811/graphite/polyolefin constants from
    # ORegan2022 (densities) and Chen2020 (specific heats, 700 J/kg/K); for sets
    # with other chemistries (e.g. Prada2013 LFP) they are approximations and the
    # run output records them under "injected_defaults".
    "Positive electrode density [kg.m-3]": 3699.0,
    "Negative electrode density [kg.m-3]": 2060.0,
    "Separator density [kg.m-3]": 1548.0,
    "Positive electrode specific heat capacity [J.kg-1.K-1]": 700.0,
    "Negative electrode specific heat capacity [J.kg-1.K-1]": 700.0,
    "Separator specific heat capacity [J.kg-1.K-1]": 700.0,
}


def _cell_volume_default(parameter_values: pybamm.ParameterValues) -> float | None:
    """Mechanical cell volume proxy for sets lacking "Cell volume [m3]":
    electrode height x width x (positive + separator + negative layer thickness).
    Returns None when any geometric parameter is missing."""
    names = (
        "Electrode height [m]",
        "Electrode width [m]",
        "Positive electrode thickness [m]",
        "Separator thickness [m]",
        "Negative electrode thickness [m]",
    )
    try:
        height, width, l_pos, l_sep, l_neg = (float(parameter_values[n]) for n in names)
    except Exception:
        return None
    return height * width * (l_pos + l_sep + l_neg)


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
    injected_defaults: dict = {}
    if thermal != "isothermal":
        # Missing-only injection: sets that define their own values keep them.
        for name, value in THERMAL_PARAM_DEFAULTS.items():
            if name not in parameter_values:
                injected_defaults[name] = value
                parameter_values.update({name: value}, check_already_exists=False)
        if "Cell volume [m3]" not in parameter_values:
            volume = _cell_volume_default(parameter_values)
            if volume is None:
                raise ValueError(
                    "base parameter set lacks 'Cell volume [m3]' and the electrode "
                    "geometry needed to derive it; lumped thermal model cannot run"
                )
            injected_defaults["Cell volume [m3]"] = volume
            parameter_values.update({"Cell volume [m3]": volume}, check_already_exists=False)

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
    if injected_defaults:
        # Audit trail: which standard defaults the runner injected for this run
        # (legacy parameter sets lacking lumped-thermal geometry/collector params).
        out["injected_defaults"] = injected_defaults
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
