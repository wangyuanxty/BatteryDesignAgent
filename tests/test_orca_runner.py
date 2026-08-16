import shutil
import pytest
from bda.simulators.orca_runner import orca_endorsement

def test_invalid_smiles():
    with pytest.raises(ValueError, match="SMILES"):
        orca_endorsement("nope")

@pytest.mark.slow
def test_water_endorsement():
    if shutil.which("orca") is None:
        pytest.skip("ORCA binary not installed")
    out = orca_endorsement("O")
    assert out["homo_ev"] < 0.0
    assert out["ie_ev"] > 0.0
    assert -40.0 < out["homo_ev"] < -1.0
    assert -40.0 < out["lumo_ev"] < 0.0

def test_retry_varies_seed_and_reraises(monkeypatch):
    import bda.simulators.orca_runner as r

    seeds = []

    def fake_write(workdir, name, smiles, charge, mult, functional, seed):
        seeds.append(seed)
        raise RuntimeError("forced")

    monkeypatch.setattr(r.shutil, "which", lambda name: "orca")
    monkeypatch.setattr(r, "_write_input", fake_write)
    with pytest.raises(RuntimeError, match="3 attempts"):
        r.orca_endorsement("O")
    assert seeds == [42, 43, 44]
    assert len(seeds) == 3


class _FakeCompletedProcess:
    returncode = 0
    stderr = ""


def _fake_run(*args, **kwargs):
    return _FakeCompletedProcess()


def test_run_and_parse_converts_au_to_ev(tmp_path, monkeypatch):
    import bda.simulators.orca_runner as r

    monkeypatch.setattr(r.subprocess, "run", _fake_run)
    (tmp_path / "neutral.out").write_text(
        "FINAL SINGLE POINT ENERGY      -76.1234567890\n"
        "E(HOMO)   =    -0.269345 a.u.\n"
        "E(LUMO)   =     0.067890 a.u.\n",
        encoding="utf-8",
    )
    out = r._run_and_parse(tmp_path, "neutral")
    assert out["homo_ev"] == pytest.approx(-0.269345 * 27.2114)
    assert out["lumo_ev"] == pytest.approx(0.067890 * 27.2114)


def test_run_and_parse_accepts_ev_units(tmp_path, monkeypatch):
    import bda.simulators.orca_runner as r

    monkeypatch.setattr(r.subprocess, "run", _fake_run)
    (tmp_path / "neutral.out").write_text(
        "FINAL SINGLE POINT ENERGY      -76.1234567890\n"
        "E(HOMO)   =    -7.328841 eV\n"
        "E(LUMO)   =     1.847318 eV\n",
        encoding="utf-8",
    )
    out = r._run_and_parse(tmp_path, "neutral")
    assert out["homo_ev"] == pytest.approx(-7.328841)
    assert out["lumo_ev"] == pytest.approx(1.847318)


def test_run_and_parse_rejects_missing_unit(tmp_path, monkeypatch):
    import bda.simulators.orca_runner as r

    monkeypatch.setattr(r.subprocess, "run", _fake_run)
    (tmp_path / "neutral.out").write_text(
        "FINAL SINGLE POINT ENERGY      -76.1234567890\n"
        "E(HOMO)   =    -0.269345\n",
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="cannot determine orbital energy unit"):
        r._run_and_parse(tmp_path, "neutral")
