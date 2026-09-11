"""calc-energy: contract-conforming energy density calculation (all tasks share this one
formula, so no task can copy another task's precedent).

ED = ∫V·I_1C dt / Σ(layer thickness×(1−porosity)×density×area)
- I_1C = Nominal cell capacity × 1 (constant current)
- area = Electrode height × width
- layers: positive/negative active layers (porosity included), positive/negative current
  collectors (no porosity factor), separator
- the electrolyte is not counted toward the mass (the parameter set has no density for it;
  stated as-is)
"""
import json
from pathlib import Path

import numpy as np
import pybamm


def _layer(th: float, por: float, den: float) -> float:
    return th * (1 - por) * den  # kg/m²


def calc_energy(params_json: str, discharge_json: str, base: str) -> dict:
    if base.endswith(".json"):
        # Custom parameter set (high-voltage LNMO, etc.): Chen2020 base plus JSON
        # override keys (the OCP symbolic function is bound by hand)
        import json as _json
        from pathlib import Path as _Path

        from bda.simulators.lnmo_parameters import lnmo_ocp

        extra = _json.loads(_Path(base).read_text(encoding="utf-8"))
        for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
            if isinstance(extra.get(key), str):
                extra[key] = lnmo_ocp
        pv = pybamm.ParameterValues("Chen2020")
        pv.update(extra, check_already_exists=False)
    else:
        pv = pybamm.ParameterValues(base)
    if params_json:
        ov = json.loads(Path(params_json).read_text(encoding="utf-8-sig"))
        pv.update(ov)
    area = float(pv["Electrode height [m]"]) * float(pv["Electrode width [m]"])
    i_1c = float(pv["Nominal cell capacity [A.h]"]) * 1.0
    dis = json.loads(Path(discharge_json).read_text(encoding="utf-8-sig"))
    v = np.asarray(dis["voltage_v"])
    t = np.asarray(dis["time_s"])
    # Compatible with numpy 2 (np.trapezoid) and 1.x (the old np.trapz name)
    _trapz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    energy_wh = float(_trapz(v * i_1c, t) / 3600.0)
    pos_el = _layer(
        float(pv["Positive electrode thickness [m]"]),
        float(pv["Positive electrode porosity"]),
        float(pv["Positive electrode density [kg.m-3]"]),
    )
    neg_el = _layer(
        float(pv["Negative electrode thickness [m]"]),
        float(pv["Negative electrode porosity"]),
        float(pv["Negative electrode density [kg.m-3]"]),
    )
    pos_cc = float(pv["Positive current collector thickness [m]"]) * float(
        pv["Positive current collector density [kg.m-3]"]
    )
    neg_cc = float(pv["Negative current collector thickness [m]"]) * float(
        pv["Negative current collector density [kg.m-3]"]
    )
    sep = _layer(
        float(pv["Separator thickness [m]"]),
        float(pv["Separator porosity"]),
        float(pv["Separator density [kg.m-3]"]),
    )
    mass_kg = (pos_el + neg_el + pos_cc + neg_cc + sep) * area
    # Volume (contract convention: Σ layer thickness × area, porosity included; same layer
    # set as the mass — electrodes/separator/current collectors, electrolyte excluded)
    thickness_m = (
        float(pv["Positive electrode thickness [m]"])
        + float(pv["Negative electrode thickness [m]"])
        + float(pv["Separator thickness [m]"])
        + float(pv["Positive current collector thickness [m]"])
        + float(pv["Negative current collector thickness [m]"])
    )
    volume_m3 = thickness_m * area
    volume_l = volume_m3 * 1000.0  # 1 m³ = 1000 L
    # Voltage plateau (mechanically derived): the voltage at the mid-point of the
    # discharge time (constant-current discharge, so the time midpoint ≈ capacity midpoint)
    mid_idx = int(len(t) * 0.5)
    midpoint_voltage_v = float(v[mid_idx])
    # DC internal resistance (mechanically derived): voltage difference between the start
    # of discharge (OCV) and the 10% discharge time, divided by I_1C (constant current)
    idx = max(1, int(len(t) * 0.1))
    dcr_ohm = (v[0] - v[idx]) / i_1c
    # Power density (approximate theoretical peak): P_max = V_OC²/(4·R_DC), normalized
    # per unit mass
    power_density_w_kg = (v[0] ** 2) / (4.0 * dcr_ohm) / mass_kg if dcr_ohm > 0 else float("nan")
    return {
        "capacity_ah": dis["capacity_ah"],
        "energy_wh": energy_wh,
        "mass_kg": mass_kg,
        "energy_density_wh_kg": energy_wh / mass_kg,
        "volume_m3": volume_m3,
        "energy_density_wh_l": energy_wh / volume_l,
        "thickness_m": thickness_m,
        "midpoint_voltage_v": midpoint_voltage_v,
        "dcr_ohm": dcr_ohm,
        "power_density_w_kg": power_density_w_kg,
        "layer_kg_m2": {
            "positive_electrode": pos_el,
            "negative_electrode": neg_el,
            "positive_cc": pos_cc,
            "negative_cc": neg_cc,
            "separator": sep,
        },
        "area_m2": area,
        "electrolyte_included": False,
        "note": "electrolyte is not counted toward mass or volume (parameter set has no density)",
    }


def cmd_calc_energy(args) -> int:
    import sys

    try:
        out = calc_energy(args.params, args.sim, args.base)
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        print(f"bda error: {e}", file=sys.stderr)
        return 1
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return 0
