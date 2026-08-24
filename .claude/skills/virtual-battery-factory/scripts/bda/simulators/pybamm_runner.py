import numpy as np
import pybamm

PROTOCOLS = {
    "1C_discharge": {"kind": "discharge", "C_rate": 1.0, "t_end_s": 3600.0, "T_amb_K": 298.15},
    "4C_charge_45C": {"kind": "charge", "C_rate": 4.0, "t_end_s": 900.0, "T_amb_K": 318.15},
    # 倍率放电：5C 恒流放电（电动工具/混动场景）。容量保持率 = 5C 容量 ÷ 同参数 1C 容量，
    # 由 agent 机械计算后落盘供 log-evaluate 判定。
    "5C_discharge": {"kind": "discharge", "C_rate": 5.0, "t_end_s": 720.0, "T_amb_K": 298.15},
    # 低温放电：-20 ℃（253.15 K）1C 放电（极寒场景）。低温容量保持率 = -20℃ 容量 ÷ 25℃ 容量。
    "lowT_discharge": {"kind": "discharge", "C_rate": 1.0, "t_end_s": 3600.0, "T_amb_K": 253.15},
    # 过充协议：先 1C 放到下限，再以 C_rate 充电至 上限+0.5V（过充场景）。
    # 输出含 T_max_K 与过充段电压曲线；过充后是否热失控由 thermal_runaway 模块耦合判定。
    "overcharge": {"kind": "overcharge", "C_rate": 0.5, "t_end_s": 7200.0, "T_amb_K": 298.15, "cutoff_add_v": 0.5},
    # 老化协议：N 圈 1C 恒流充放（SEI ec reaction limited + isothermal）；
    # 电压上下限取参数集自身值。要求基参数集带 SEI 动力学参数（Chen2020/OKane2022 等）。
    # cycles 可通过 run-pyamm --cycles 覆盖（默认 100）。
    "aging_1C_100cyc": {"kind": "aging", "cycles": 100, "C_rate": 1.0, "T_amb_K": 298.15},
    # 高温老化：45 ℃（318.15 K）1C 循环（高温存储/循环场景，SEI 生长加速）。
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
    """老化协议：N 圈 1C 恒流充放（SEI ec reaction limited + isothermal）。

    输出 cycle_numbers / capacity_ah_per_cycle / sei_thickness_nm_end。
    基参数集无 SEI 动力学参数时报错（老化必须用老化体系，如 Chen2020/OKane2022）。
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
        # 自定义参数集（如高电压 LNMO）：Chen2020 基底 + JSON 覆盖键
        # （JSON 为扁平覆盖键集，见 data/LNMO.json；OCP 等函数键手动解析为 Python 函数）
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
        # 老化协议内部固定 isothermal + SEI，--thermal/--plating 不参与
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
        # Experiment 驱动：C_rate 真实生效（此前只影响 capacity 口径，4C 协议实际跑
        # 默认 1C 放电；agent 传负电流时与默认满电初始条件冲突，触发
        # "Maximum voltage non-positive at initial conditions"）。电压事件由实验处理。
        # 充电从空电开始：默认满电初始会让充电步骤立即不可行，故先 1C 放到 v_min 再充。
        v_min = float(parameter_values["Lower voltage cut-off [V]"])
        v_max = float(parameter_values["Upper voltage cut-off [V]"])
        if p["kind"] in ("charge", "overcharge"):
            # 过充协议：充电截止 = 上限 + cutoff_add_v（默认 +0.5 V）
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
        # 充电容量 = 最后一段（充电段）时长 × C_rate（恒流）
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
