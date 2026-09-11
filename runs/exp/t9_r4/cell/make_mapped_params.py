"""Build the mapped-cell parameter set for a layered finalist (custom JSON base, mirroring
the LNMO.json precedent + the contract's fixed mapping rule).

Contract mapping rule:
  - constant OCP = computed average voltage (scalar float, verified working in SPMe)
  - capacity = 0.9 x computed capacity  -> "Nominal cell capacity [A.h]"
  - SEI kinetics = Chen2020 baseline k0 -> SEI keys untouched (inherited from Chen2020)
  - upper voltage cut-off = 4.8 V (the declared charging-potential limit)

Material constants (all sourced/inferred, per-value provenance written into the JSON):
  - avg_voltage_v, capacity_mah_g: run-comp batch output (sourced)
  - density_g_cm3: CHGNet-relaxed cell density from comp/profile_voltage.py (sourced)
  - molar_mass_kg_mol = 0.7 * F/3.6 / capacity_mah_g  (inferred from the capacity definition)
  - c_max = density / MW (mol/m3, inferred); initial = 0.3 * c_max (top-of-charge x_Li = 0.3)
  - M_am = pos_thickness x eps_am x area x density (Chen2020 geometry, 5.162e-6 m3 x rho)

Transport properties (conductivity/diffusivity/reaction rate) inherited from Chen2020
(NMC811, same layered family) — no fabricated values.

IN: {"name": ..., "avg_voltage_v": ..., "capacity_mah_g": ..., "density_g_cm3": ...}
OUT: cell/params_<name>.json
"""
import json
import sys
from pathlib import Path

_F = 26801.481  # F/3.6 mAh/mol (run-comp capacity definition)
_AREA = 0.065 * 1.58  # m2, Chen2020 electrode height x width
_POS_THICK = 7.56e-5
_EPS_AM = 0.665
_V_AM = _POS_THICK * _AREA * _EPS_AM  # m3 active material (Chen2020 geometry)


def build(data: dict) -> dict:
    name = str(data["name"])
    v_avg = float(data["avg_voltage_v"])
    c_comp = float(data["capacity_mah_g"])
    rho_gcm3 = float(data["density_g_cm3"])
    rho = rho_gcm3 * 1000.0  # kg/m3
    mw = 0.7 * _F / c_comp  # kg/mol
    m_am = _V_AM * rho  # kg
    nominal_ah = 0.9 * c_comp * m_am  # Ah (0.9 x computed capacity)
    c_max = rho / mw  # mol/m3
    params = {
        "Lower voltage cut-off [V]": 2.5,
        "Upper voltage cut-off [V]": 4.8,
        "Positive electrode OCP [V]": v_avg,
        "Positive electrode OCP entropic change [V.K-1]": 0.0,
        "Positive electrode stoichiometry limits for reaction [0.0, 1.0]": [1.0, 0.3],
        "Positive electrode density [kg.m-3]": rho,
        "Positive electrode molar mass [kg.mol-1]": mw,
        "Positive electrode maximum concentration [mol.m-3]": c_max,
        "Initial concentration in positive electrode [mol.m-3]": 0.3 * c_max,
        "Positive electrode number of electrons transferred": 1.0,
        "Positive electrode active material volume fraction": _EPS_AM,
        "Nominal cell capacity [A.h]": nominal_ah,
        "_provenance": {
            "name": name,
            "avg_voltage_v_src": "run-comp batch output (comp/batch*_layered_out.json)",
            "capacity_mah_g_src": "run-comp batch output (capacity_mah_g)",
            "density_g_cm3_src": "comp/profile_voltage.py output (CHGNet-relaxed cell density)",
            "molar_mass_kg_mol": f"inferred: 0.7 x F/3.6 / capacity_mah_g = {mw:.6f}",
            "c_max": f"inferred: density / molar mass = {c_max:.1f} mol/m3",
            "nominal_capacity_ah": f"0.9 x capacity_mah_g x M_am (M_am = {m_am:.5f} kg) = {nominal_ah:.4f} Ah",
            "ed_active_wh_kg": f"ED_active = V x C x 0.9 = {v_avg:.4f} x {c_comp:.2f} x 0.9 = {v_avg * c_comp * 0.9:.1f}",
            "mapping_rule": "constant OCP = computed average voltage; capacity = 0.9 x computed capacity; SEI = Chen2020 baseline k0 (untouched)",
        },
    }
    return params


def main(in_path, out_path):
    data = json.loads(Path(in_path).read_text(encoding="utf-8"))
    params = build(data)
    Path(out_path).write_text(json.dumps(params, indent=2), encoding="utf-8")
    print(f"wrote {out_path}")
    for k, v in params["_provenance"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
