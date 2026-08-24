"""calc-energy 合同口径能量密度计算测试。"""
import json

import pytest

from bda.energy import calc_energy


@pytest.fixture
def sim_json(tmp_path):
    """合成 1C 放电曲线：恒定电压 3.5V × 5A × 3600s = 17.5 Wh。"""
    n = 361
    t = [i * 10 for i in range(n)]  # 0..3600 s，间隔 10s
    v = [3.5] * n
    d = {"capacity_ah": 5.0, "time_s": t, "voltage_v": v}
    p = tmp_path / "sim.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    return str(p)


def test_energy_positive(sim_json):
    out = calc_energy("", sim_json, "OKane2022")
    assert out["energy_density_wh_kg"] > 0
    assert out["energy_wh"] > 0
    assert out["mass_kg"] > 0
    assert out["electrolyte_included"] is False


def test_energy_wh_approx(sim_json):
    """3.5V × I_1C × 1h（I_1C = 参数集 Nominal capacity；梯形积分恒压精确）。"""
    import pybamm

    i_1c = float(pybamm.ParameterValues("OKane2022")["Nominal cell capacity [A.h]"])
    out = calc_energy("", sim_json, "OKane2022")
    assert abs(out["energy_wh"] - 3.5 * i_1c) < 0.1


def test_thinner_electrode_higher_ed(sim_json, tmp_path):
    """减薄正极 → 质量下降 → ED 上升（合同公式敏感性）。"""
    base = calc_energy("", sim_json, "OKane2022")
    thin = {"Positive electrode thickness [m]": 5e-5}  # 默认 7.56e-5
    p = tmp_path / "thin.json"
    p.write_text(json.dumps(thin), encoding="utf-8")
    out = calc_energy(str(p), sim_json, "OKane2022")
    assert out["energy_density_wh_kg"] > base["energy_density_wh_kg"]


def test_unknown_base_raises(sim_json):
    with pytest.raises(ValueError):
        calc_energy("", sim_json, "ORegan202")
