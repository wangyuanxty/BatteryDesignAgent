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
    # Real lumped-thermal coupling: the 4C-charge cell must heat above the 45 C ambient.
    assert out["T_max_K"] > 318.15 + 0.5

def test_plating_returns_anode_potential():
    out = run_simulation({}, protocol="4C_charge_45C", mode="spme", plating=True)
    assert "anode_potential_v" in out
    assert len(out["anode_potential_v"]) == len(out["time_s"])


def test_legacy_base_injects_thermal_defaults():
    """Legacy sets (Prada2013/Ramadass2004) lack lumped-thermal geometry params;
    the runner injects documented defaults (mirroring plating defaults) so system
    candidates can run stages 2/3, and records them for the audit trail."""
    for base in ("Prada2013", "Ramadass2004"):
        out = run_simulation({}, protocol="1C_discharge", base=base, mode="spme",
                             thermal="lumped", plating=True)
        assert out["model_used"] == "SPMe"
        assert len(out["time_s"]) == len(out["voltage_v"])
        assert out["capacity_ah"] > 0.0
        assert "T_max_K" in out
        assert "anode_potential_v" in out
        injected = out.get("injected_defaults") or {}
        assert "Cell volume [m3]" in injected


def test_modern_base_keeps_own_thermal_params():
    """ORegan2022 defines its own thermal params; nothing must be injected."""
    out = run_simulation({}, protocol="1C_discharge", base="ORegan2022", mode="spme",
                         thermal="lumped", plating=True)
    assert "injected_defaults" not in out
    assert "T_max_K" in out

def test_dfn_fallback_to_spme():
    # 极端薄电极使 DFN 数值刚性，通常触发求解困难；若未触发，跳过
    hard = {"Positive electrode thickness [m]": 1e-6}
    try:
        out = run_simulation(hard, protocol="1C_discharge", mode="dfn", fallback=True)
    except pybamm.SolverError:
        pytest.fail("fallback did not engage")
    assert out["model_used"] in ("DFN", "SPMe(fallback)")


def test_dfn_fallback_engages(monkeypatch):
    # Force the DFN solve to fail once; the SPMe rerun must engage and succeed.
    real_solve = pybamm.Simulation.solve
    calls = {"n": 0}

    def fake_solve(self, *args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise pybamm.SolverError("forced failure")
        return real_solve(self, *args, **kwargs)

    monkeypatch.setattr(pybamm.Simulation, "solve", fake_solve)
    out = run_simulation({}, protocol="1C_discharge", mode="dfn", fallback=True)
    assert calls["n"] == 2
    assert out["model_used"] == "SPMe(fallback)"


def test_dfn_no_fallback_reraises(monkeypatch):
    # With fallback disabled the DFN SolverError must propagate unchanged.
    def fake_solve(self, *args, **kwargs):
        raise pybamm.SolverError("forced failure")

    monkeypatch.setattr(pybamm.Simulation, "solve", fake_solve)
    with pytest.raises(pybamm.SolverError):
        run_simulation({}, protocol="1C_discharge", mode="dfn", fallback=False)
