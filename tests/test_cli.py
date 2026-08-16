import json
import subprocess
import sys

from bda.cli import main

PY = sys.executable

def test_unknown_command_fails_fast():
    r = subprocess.run([PY, "-m", "bda", "nonsense"], capture_output=True, text=True)
    assert r.returncode != 0
    assert "command" in r.stderr.lower() or "usage" in r.stderr.lower()

def test_bridge_roundtrip(tmp_path):
    props = tmp_path / "p.json"
    props.write_text(json.dumps({"D_electrolyte_m2_s": 3e-10}), encoding="utf-8")
    out = tmp_path / "o.json"
    r = subprocess.run([PY, "-m", "bda", "bridge", "--props", str(props), "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Electrolyte diffusivity [m2.s-1]"] == 3e-10

def test_bridge_bad_key_exit_1(tmp_path):
    props = tmp_path / "p.json"
    props.write_text(json.dumps({"bogus": 1.0}), encoding="utf-8")
    out = tmp_path / "o.json"
    r = subprocess.run([PY, "-m", "bda", "bridge", "--props", str(props), "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 1
    assert "bogus" in r.stderr


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
