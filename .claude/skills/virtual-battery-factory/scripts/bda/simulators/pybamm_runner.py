import numpy as np
import pybamm

PROTOCOLS = {
    "1C_discharge": {"kind": "discharge", "C_rate": 1.0, "t_end_s": 3600.0, "T_amb_K": 298.15},
    "0.1C_discharge": {"kind": "discharge", "C_rate": 0.1, "t_end_s": 36000.0, "T_amb_K": 298.15},
    "4C_charge_45C": {"kind": "charge", "C_rate": 4.0, "t_end_s": 900.0, "T_amb_K": 318.15},
    # Rate discharge: 5C constant-current discharge (power-tool/hybrid scenarios). Capacity
    # retention = 5C capacity ÷ 1C capacity at the same parameters, computed mechanically by
    # the agent and written to disk for log-evaluate to judge.
    "5C_discharge": {"kind": "discharge", "C_rate": 5.0, "t_end_s": 720.0, "T_amb_K": 298.15},
    # Low-temperature discharge: 1C discharge at -20 ℃ (253.15 K) (extreme-cold scenario).
    # Low-temperature capacity retention = -20℃ capacity ÷ 25℃ capacity.
    "lowT_discharge": {"kind": "discharge", "C_rate": 1.0, "t_end_s": 3600.0, "T_amb_K": 253.15},
    # Overcharge protocol: first discharge at 1C to the lower limit, then charge at C_rate to
    # upper limit + 0.5V (overcharge scenario). The output contains T_max_K and the overcharge
    # segment voltage curve; whether thermal runaway follows the overcharge is determined by
    # coupling with the thermal_runaway module.
    "overcharge": {"kind": "overcharge", "C_rate": 0.5, "t_end_s": 7200.0, "T_amb_K": 298.15, "cutoff_add_v": 0.5},
    # Aging protocol: N cycles of 1C constant-current charge/discharge (SEI ec reaction
    # limited + isothermal); the voltage limits come from the parameter set itself. The base
    # parameter set must carry SEI kinetic parameters (Chen2020/OKane2022, etc.). cycles can
    # be overridden via run-pyamm --cycles (default 100).
    "aging_1C_100cyc": {"kind": "aging", "cycles": 100, "C_rate": 1.0, "T_amb_K": 298.15},
    # High-temperature aging: 1C cycling at 45 ℃ (318.15 K) (high-temperature storage/cycling
    # scenario, accelerated SEI growth).
    "aging_1C_100cyc_45C": {"kind": "aging", "cycles": 100, "C_rate": 1.0, "T_amb_K": 318.15},
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


def _run_aging(parameter_values: pybamm.ParameterValues, p: dict, mode: str) -> dict:
    """Aging protocol: N cycles of 1C constant-current charge/discharge (SEI ec reaction
    limited + isothermal).

    Outputs cycle_numbers / capacity_ah_per_cycle / sei_thickness_nm_end. Raises if the base
    parameter set has no SEI kinetic parameters (aging must use an aging-capable system, such
    as Chen2020/OKane2022).
    """
    sei_required = "SEI kinetic rate constant [m.s-1]"
    if sei_required not in parameter_values:
        raise ValueError(
            f"base parameter set has no '{sei_required}'; the aging protocol requires "
            "an aging-capable parameter set (e.g. Chen2020, OKane2022)"
        )
    v_min = float(parameter_values["Lower voltage cut-off [V]"])
    v_max = float(parameter_values["Upper voltage cut-off [V]"])
    exp = pybamm.Experiment(
        [(
            f"Discharge at {p['C_rate']:g}C until {v_min} V",
            f"Charge at {p['C_rate']:g}C until {v_max} V",
        )] * p["cycles"]
    )
    options = {"SEI": "ec reaction limited", "thermal": "isothermal"}
    model = (
        pybamm.lithium_ion.DFN(options=options)
        if mode == "dfn"
        else pybamm.lithium_ion.SPMe(options=options)
    )
    sol = pybamm.Simulation(model, experiment=exp, parameter_values=parameter_values).solve()
    caps = [
        float(sol.cycles[i]["Discharge capacity [A.h]"].entries[-1])
        for i in range(len(sol.cycles))
    ]
    sei_end = float(np.asarray(
        sol.cycles[-1]["Negative SEI thickness [m]"].entries[-1]
    ).max())
    return {
        "model_used": "DFN" if mode == "dfn" else "SPMe",
        "protocol": "aging",
        "cycle_numbers": list(range(1, len(caps) + 1)),
        "capacity_ah_per_cycle": caps,
        "sei_thickness_nm_end": sei_end * 1e9,
    }


def run_simulation(
    params: dict,
    protocol: str,
    base: str = "Chen2020",
    mode: str = "spme",
    fallback: bool = True,
    thermal: str = "lumped",
    plating: bool = False,
    cycles: int | None = None,
) -> dict:
    if protocol not in PROTOCOLS:
        raise ValueError(f"unknown protocol '{protocol}'; legal: {sorted(PROTOCOLS)}")
    if mode not in ("spme", "dfn"):
        raise ValueError(f"unknown mode '{mode}'; legal: spme, dfn")
    p = dict(PROTOCOLS[protocol])
    if cycles is not None and p["kind"] == "aging":
        p["cycles"] = cycles
    if base.endswith(".json"):
        # Custom parameter set (e.g. high-voltage LNMO): Chen2020 base plus JSON override keys
        # (the JSON is a flat set of override keys, see data/LNMO.json; function keys such as
        # the OCP are parsed into Python functions by hand)
        import json as _json
        from pathlib import Path as _Path

        from bda.simulators.lnmo_parameters import lnmo_ocp

        extra = _json.loads(_Path(base).read_text(encoding="utf-8"))
        for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
            if isinstance(extra.get(key), str):
                extra[key] = lnmo_ocp
        parameter_values = pybamm.ParameterValues("Chen2020")
        parameter_values.update(extra, check_already_exists=False)
    else:
        parameter_values = pybamm.ParameterValues(base)
    unknown_params = sorted(name for name in params if name not in parameter_values)
    if unknown_params:
        raise ValueError(f"unknown parameter name(s): {unknown_params}")
    parameter_values.update(params)
    parameter_values.update({"Ambient temperature [K]": p["T_amb_K"]}, check_already_exists=False)
    if p["kind"] == "aging":
        # The aging protocol fixes isothermal + SEI internally; --thermal/--plating do not apply
        return _run_aging(parameter_values, p, mode)
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
        # Experiment-driven: C_rate actually takes effect (previously it only affected the
        # capacity convention, and the 4C protocol really ran the default 1C discharge; when
        # the agent passed a negative current it conflicted with the default fully charged
        # initial condition, triggering "Maximum voltage non-positive at initial conditions").
        # Voltage events are handled by the experiment.
        # Charging starts from empty: the default fully charged initial state makes the charge
        # step immediately infeasible, so discharge at 1C to v_min first and then charge.
        v_min = float(parameter_values["Lower voltage cut-off [V]"])
        v_max = float(parameter_values["Upper voltage cut-off [V]"])
        if p["kind"] in ("charge", "overcharge"):
            # Overcharge protocol: charge cut-off = upper limit + cutoff_add_v (default +0.5 V)
            v_cut = v_max + p.get("cutoff_add_v", 0.0)
            exp = pybamm.Experiment(
                [
                    f"Discharge at 1C until {v_min} V",
                    f"Charge at {p['C_rate']:g}C until {v_cut:g} V",
                ]
            )
        else:
            exp = pybamm.Experiment([f"Discharge at {p['C_rate']:g}C until {v_min} V"])
        sim = pybamm.Simulation(model, experiment=exp, parameter_values=parameter_values)
        sim.solve()
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
        out["capacity_ah"] = float(sol.cycles[-1]["Discharge capacity [A.h]"].entries[-1])
    else:
        # Charge capacity = duration of the last (charge) segment × C_rate (constant current)
        cyc = sol.cycles[-1]
        t_cyc = cyc["Time [s]"].entries
        out["capacity_ah"] = float(t_cyc[-1] - t_cyc[0]) * p["C_rate"] / 3600.0
    if thermal != "isothermal":
        out["T_max_K"] = float(sol["Volume-averaged cell temperature [K]"].entries.max())
    if plating:
        out["anode_potential_v"] = sol[
            "Negative electrode surface potential difference at separator interface [V]"
        ].entries.tolist()
    return out
