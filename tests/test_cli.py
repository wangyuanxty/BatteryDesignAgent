import json
import subprocess
import sys

import pytest

from bda.cli import main

PY = sys.executable

def test_unknown_command_fails_fast():
    r = subprocess.run([PY, "-m", "bda", "nonsense"], capture_output=True, text=True)
    assert r.returncode != 0
    assert "command" in r.stderr.lower() or "usage" in r.stderr.lower()


# ---------------------------------------------------------------------------
# In-process handler tests (bda.cli.main): cover the CLI boundary directly.
# ---------------------------------------------------------------------------

def test_run_pyamm_base_flag_passed_through(tmp_path, monkeypatch):
    """CRITICAL regression: base_params from the case config must reach
    run_simulation; --base defaults to Chen2020."""
    import bda.simulators.pybamm_runner as pr

    seen = {}

    def fake_run(params, protocol, base="Chen2020", mode="spme", fallback=True,
                 thermal="lumped", plating=False):
        seen.update(params=params, protocol=protocol, base=base, mode=mode,
                    thermal=thermal, plating=plating)
        return {"model_used": "SPMe", "time_s": [0.0, 1.0],
                "voltage_v": [4.2, 3.5], "capacity_ah": 1.0}

    monkeypatch.setattr(pr, "run_simulation", fake_run)
    params = tmp_path / "p.json"
    params.write_text(json.dumps({"Electrolyte diffusivity [m2.s-1]": 3e-10}),
                      encoding="utf-8")
    out = tmp_path / "o.json"
    rc = main(["run-pyamm", "--params", str(params), "--protocol", "1C_discharge",
               "--base", "ORegan2022", "--out", str(out)])
    assert rc == 0
    assert seen["base"] == "ORegan2022"
    assert seen["protocol"] == "1C_discharge"
    assert json.loads(out.read_text(encoding="utf-8"))["capacity_ah"] == 1.0


def test_run_pyamm_base_defaults_to_chen2020(tmp_path, monkeypatch):
    import bda.simulators.pybamm_runner as pr

    seen = {}

    def fake_run(params, protocol, base="Chen2020", mode="spme", fallback=True,
                 thermal="lumped", plating=False):
        seen["base"] = base
        return {"model_used": "SPMe", "time_s": [0.0, 1.0],
                "voltage_v": [4.2, 3.5], "capacity_ah": 1.0}

    monkeypatch.setattr(pr, "run_simulation", fake_run)
    params = tmp_path / "p.json"
    params.write_text(json.dumps({}), encoding="utf-8")
    out = tmp_path / "o.json"
    rc = main(["run-pyamm", "--params", str(params), "--protocol", "1C_discharge",
               "--out", str(out)])
    assert rc == 0
    assert seen["base"] == "Chen2020"


# ---------------------------------------------------------------------------
# Spec 5.2 invariant 3: same params -> cache hit, no recompute.
# Workspace root for caching = directory of the --out file.
# ---------------------------------------------------------------------------

def _run_pyamm_cli(tmp_path, monkeypatch, params_file):
    import bda.simulators.pybamm_runner as pr
    calls = []

    def fake_run(params, protocol, base="Chen2020", mode="spme", fallback=True,
                 thermal="lumped", plating=False):
        calls.append((params, protocol, base, mode, thermal, plating))
        return {"model_used": "SPMe", "time_s": [0.0, 1.0],
                "voltage_v": [4.2, 3.5], "capacity_ah": 1.0}

    monkeypatch.setattr(pr, "run_simulation", fake_run)
    out = tmp_path / "o.json"
    argv = ["run-pyamm", "--params", str(params_file), "--protocol", "1C_discharge",
            "--out", str(out)]
    return calls, out, argv


def test_run_pyamm_reuses_cache_for_same_params(tmp_path, monkeypatch):
    params = tmp_path / "p.json"
    params.write_text(json.dumps({"Electrolyte diffusivity [m2.s-1]": 3e-10}),
                      encoding="utf-8")
    calls, out, argv = _run_pyamm_cli(tmp_path, monkeypatch, params)
    assert main(argv) == 0
    assert main(argv) == 0
    assert len(calls) == 1  # second invocation short-circuits on the cache


def test_run_pyamm_cache_key_covers_base(tmp_path, monkeypatch):
    params = tmp_path / "p.json"
    params.write_text(json.dumps({}), encoding="utf-8")
    calls, out, argv = _run_pyamm_cli(tmp_path, monkeypatch, params)
    assert main(argv + ["--base", "Chen2020"]) == 0
    assert main(argv + ["--base", "ORegan2022"]) == 0
    assert len(calls) == 2  # different base -> different key -> recompute


def test_run_pyamm_cache_key_covers_plating_flag(tmp_path, monkeypatch):
    params = tmp_path / "p.json"
    params.write_text(json.dumps({}), encoding="utf-8")
    calls, out, argv = _run_pyamm_cli(tmp_path, monkeypatch, params)
    assert main(argv) == 0
    assert main(argv + ["--plating"]) == 0
    assert len(calls) == 2


def test_run_pyamm_corrupt_cache_recomputes(tmp_path, monkeypatch):
    params = tmp_path / "p.json"
    params.write_text(json.dumps({}), encoding="utf-8")
    calls, out, argv = _run_pyamm_cli(tmp_path, monkeypatch, params)
    assert main(argv) == 0
    cache_dir = tmp_path / "cache"
    cache_file = next(cache_dir.glob("*.json"))
    cache_file.write_text("{corrupt", encoding="utf-8")
    assert main(argv) == 0
    assert len(calls) == 2  # corrupt cache file -> miss -> recompute + overwrite


def test_run_mlp_reuses_cache_per_candidate(tmp_path, monkeypatch):
    import bda.simulators.mlp_runner as mlp

    calls = []

    def fake_relax(smiles, model="mace"):
        calls.append((smiles, model))
        return {"energy_ev": -123.0, "converged": True}

    monkeypatch.setattr(mlp, "relax_structure", fake_relax)
    in_file = tmp_path / "in.json"
    in_file.write_text(json.dumps({"candidates": [{"smiles": "CCO"}, {"smiles": "FEC"}]}),
                       encoding="utf-8")
    out = tmp_path / "o.json"
    argv = ["run-mlp", "--in", str(in_file), "--out", str(out)]
    assert main(argv) == 0
    assert main(argv) == 0
    assert len(calls) == 2  # one call per candidate, then fully cached
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data["candidates"]) == 2
    assert data["candidates"][0]["metrics"]["energy_ev"] == -123.0


def test_run_xtb_handler_in_process_with_cache(tmp_path, monkeypatch):
    import bda.simulators.xtb_runner as xtb

    calls = []

    def fake_xtb(smiles):
        calls.append(smiles)
        return {"homo_ev": -8.1, "lumo_ev": 0.4, "total_energy_ev": -100.0}

    monkeypatch.setattr(xtb, "xtb_single_point", fake_xtb)
    in_file = tmp_path / "in.json"
    in_file.write_text(json.dumps({"candidates": [{"smiles": "CCO"}]}), encoding="utf-8")
    out = tmp_path / "o.json"
    argv = ["run-xtb", "--in", str(in_file), "--out", str(out)]
    assert main(argv) == 0
    assert main(argv) == 0
    assert calls == ["CCO"]  # second run served from cache
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["candidates"][0]["metrics"]["homo_ev"] == -8.1


def test_run_orca_handler_in_process_with_cache(tmp_path, monkeypatch):
    import bda.simulators.orca_runner as orca

    calls = []

    def fake_orca(smiles, charge=0, functional="r2SCAN-3c"):
        calls.append(smiles)
        return {"E_hartree": -76.0, "homo_ev": -7.0, "lumo_ev": 1.0,
                "ie_ev": 12.0, "ea_ev": -2.0}

    monkeypatch.setattr(orca, "orca_endorsement", fake_orca)
    in_file = tmp_path / "in.json"
    in_file.write_text(json.dumps({"candidates": [{"smiles": "O"}]}), encoding="utf-8")
    out = tmp_path / "o.json"
    argv = ["run-orca", "--in", str(in_file), "--out", str(out)]
    assert main(argv) == 0
    assert main(argv) == 0
    assert calls == ["O"]
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["candidates"][0]["endorsement"]["ie_ev"] == 12.0


def test_run_orca_invalid_smiles_returns_1(capsys, tmp_path):
    """Invalid SMILES must fail with the documented bda error (exit 1), not an
    rdkit traceback, even though the cache key derivation parses the molecule."""
    in_file = tmp_path / "in.json"
    in_file.write_text(json.dumps({"candidates": [{"smiles": "nope"}]}), encoding="utf-8")
    out = tmp_path / "o.json"
    rc = main(["run-orca", "--in", str(in_file), "--out", str(out)])
    assert rc == 1
    assert "SMILES" in capsys.readouterr().err


def test_run_md_handler_in_process_with_cache_and_engine(tmp_path, monkeypatch):
    import bda.simulators.md_runner as md

    calls = []

    def fake_md(box, engine="gromacs", t_ns=10.0):
        calls.append((box, engine, t_ns))
        return {"D_Li_m2_s": 1.5e-10, "trajectory_ok": True, "drift_check": "ok",
                "achieved_density_g_cm3": 1.1}

    monkeypatch.setattr(md, "run_diffusion_md", fake_md)
    box = tmp_path / "box.json"
    box.write_text(json.dumps({"molecules": {"EC": 3, "Li": 1}}), encoding="utf-8")
    out = tmp_path / "o.json"
    argv = ["run-md", "--box", str(box), "--engine", "mace", "--t-ns", "0.001",
            "--out", str(out)]
    assert main(argv) == 0
    assert main(argv) == 0
    assert calls == [({"molecules": {"EC": 3, "Li": 1}}, "mace", 0.001)]  # cached
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["D_Li_m2_s"] == 1.5e-10


def test_handler_error_returns_1_and_prints(capsys, tmp_path):
    """Parameter/validation errors must exit 1 with the documented bda error
    on stderr, not a traceback (unknown protocol vehicle for the error path)."""
    params = tmp_path / "p.json"
    params.write_text(json.dumps({}), encoding="utf-8")
    out = tmp_path / "o.json"
    rc = main(["run-pyamm", "--params", str(params), "--protocol", "bogus",
               "--out", str(out)])
    assert rc == 1
    err = capsys.readouterr().err
    assert "bogus" in err


def test_run_pyamm_handler_in_process_fast_protocol(tmp_path):
    """Real (not mocked) SPMe solve through the CLI boundary."""
    params = tmp_path / "p.json"
    params.write_text(json.dumps({}), encoding="utf-8")
    out = tmp_path / "o.json"
    rc = main(["run-pyamm", "--params", str(params), "--protocol", "1C_discharge",
               "--out", str(out)])
    assert rc == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["model_used"] == "SPMe"
    assert len(data["time_s"]) == len(data["voltage_v"])
    assert data["capacity_ah"] > 0.0


def test_render_handler_in_process_on_tmp_fixture(tmp_path):
    from bda.store import append_entry
    from bda.store import CaseWorkspace

    ws = CaseWorkspace("case1", root=str(tmp_path))
    append_entry(ws, {"criteria": {"T_max_C": 60}})
    append_entry(ws, {"action": "propose", "candidates": ["FEC"]})
    append_entry(ws, {"action": "final", "verdict": "达标", "recommendation": "FEC"})
    rc = main(["render", "--case-dir", str(ws.path), "--out", "report.html"])
    assert rc == 0
    html = (ws.path / "report.html").read_text(encoding="utf-8")
    assert "<html" in html and "FEC" in html


def test_module_entrypoint_runs(monkeypatch, tmp_path):
    import runpy

    import bda.simulators.pybamm_runner as pr

    def fake_run(params, protocol, base="Chen2020", mode="spme", fallback=True,
                 thermal="lumped", plating=False):
        return {"model_used": "SPMe", "time_s": [0.0, 1.0],
                "voltage_v": [4.2, 3.5], "capacity_ah": 1.0}

    monkeypatch.setattr(pr, "run_simulation", fake_run)
    params = tmp_path / "p.json"
    params.write_text(json.dumps({}), encoding="utf-8")
    out = tmp_path / "o.json"
    monkeypatch.setattr(sys, "argv", ["bda", "run-pyamm", "--params", str(params),
                                      "--protocol", "1C_discharge", "--out", str(out)])
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("bda", run_name="__main__")
    assert exc.value.code == 0
    assert out.exists()
