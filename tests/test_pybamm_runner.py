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
