import pytest
import pybamm

from bda.simulators.pybamm_runner import run_simulation

def test_1c_discharge_returns_curves():
    out = run_simulation({}, protocol="1C_discharge", mode="spme")
    assert out["model_used"] == "SPMe"
    assert len(out["time_s"]) == len(out["voltage_v"])
    assert out["capacity_ah"] > 0.0

def test_bad_protocol_fails_fast():
    import pytest
    with pytest.raises(ValueError, match="protocol"):
        run_simulation({}, protocol="nonsense", mode="spme")

def test_unknown_param_fails_fast():
    import pytest
    with pytest.raises(ValueError, match="unknown parameter name"):
        run_simulation({"Bogus parameter name [x]": 1.0}, protocol="1C_discharge", mode="spme")

def test_thermal_returns_tmax():
    out = run_simulation({}, protocol="4C_charge_45C", mode="spme", thermal="lumped")
    assert "T_max_K" in out
    assert out["T_max_K"] > 300.0

def test_plating_returns_anode_potential():
    out = run_simulation({}, protocol="4C_charge_45C", mode="spme", plating=True)
    assert "anode_potential_v" in out
    assert len(out["anode_potential_v"]) == len(out["time_s"])

def test_dfn_fallback_to_spme():
    # 极端薄电极使 DFN 数值刚性，通常触发求解困难；若未触发，跳过
    hard = {"Positive electrode thickness [m]": 1e-6}
    try:
        out = run_simulation(hard, protocol="1C_discharge", mode="dfn", fallback=True)
    except pybamm.SolverError:
        pytest.fail("fallback did not engage")
    assert out["model_used"] in ("DFN", "SPMe(fallback)")
