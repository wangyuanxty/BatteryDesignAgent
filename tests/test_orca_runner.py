import shutil
import pytest
from bda.simulators.orca_runner import orca_endorsement

def test_invalid_smiles():
    with pytest.raises(ValueError, match="SMILES"):
        orca_endorsement("nope")

def test_multiplicity_for_parity_of_electrons():
    import bda.simulators.orca_runner as r
    # H2O: 10 electrons -> even -> singlet for all three charge states would be
    # wrong for the ions: 9 (cation) and 11 (anion) electrons are odd -> doublet.
    assert r._multiplicity_for("O", 0) == 1
    assert r._multiplicity_for("O", 1) == 2
    assert r._multiplicity_for("O", -1) == 2
    # CH3 radical: 9 electrons -> doublet even at charge 0.
    assert r._multiplicity_for("[CH3]", 0) == 2

def test_write_input_embeds_charge_and_mult(tmp_path):
    import bda.simulators.orca_runner as r
    r._write_input(tmp_path, "cation", "O", 1, 2, "r2SCAN-3c", 42)
    text = (tmp_path / "cation.inp").read_text(encoding="utf-8")
    assert "* xyzfile 1 2 cation.xyz" in text

def test_input_template_requests_geometry_optimization(tmp_path):
    """Spec decision 11: gas-phase geometry optimization, not a bare single point."""
    import bda.simulators.orca_runner as r
    r._write_input(tmp_path, "neutral", "O", 0, 1, "r2SCAN-3c", 42)
    text = (tmp_path / "neutral.inp").read_text(encoding="utf-8")
    assert text.splitlines()[0] == "! r2SCAN-3c OPT"

def test_orca_endorsement_uses_spin_consistent_multiplicities(monkeypatch):
    """The three states written for one molecule must carry (charge, mult) pairs
    consistent with the electron parity: neutral (0, 1), cation (+1, 2), anion
    (-1, 2) for water. Testable without the ORCA binary."""
    import bda.simulators.orca_runner as r

    seen = {}

    def fake_run_and_parse(workdir, name):
        text = (workdir / f"{name}.inp").read_text(encoding="utf-8")
        line = next(ln for ln in text.splitlines() if ln.startswith("* xyz"))
        seen[name] = tuple(int(x) for x in line.split()[2:4])
        return {"E_hartree": -76.0, "homo_ev": -7.0, "lumo_ev": 1.0}

    monkeypatch.setattr(r.shutil, "which", lambda name: "orca")
    monkeypatch.setattr(r, "_run_and_parse", fake_run_and_parse)
    out = r.orca_endorsement("O")
    assert seen == {"neutral": (0, 1), "cation": (1, 2), "anion": (-1, 2)}
    assert "ie_ev" in out and "ea_ev" in out

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
    stdout = ""


def _fake_run(*args, **kwargs):
    p = _FakeCompletedProcess()
    cwd = kwargs.get("cwd")
    if cwd is not None:
        from pathlib import Path
        out_file = Path(cwd) / "neutral.out"
        p.stdout = out_file.read_text(encoding="utf-8") if out_file.exists() else ""
    return p


def test_run_and_parse_orbital_energies_block(tmp_path, monkeypatch):
    """ORCA 6 解析：FINAL SINGLE POINT ENERGY + ORBITAL ENERGIES 块（eV 列）。"""
    import bda.simulators.orca_runner as r

    monkeypatch.setattr(r.subprocess, "run", _fake_run)
    (tmp_path / "neutral.out").write_text(
        "FINAL SINGLE POINT ENERGY      -76.1234567890\n"
        "ORBITAL ENERGIES\n"
        "  NO   OCC          E(Eh)            E(eV)\n"
        "   0   2.0000      -15.606757      -424.6795\n"
        "   4   2.0000       -0.269345        -7.3288\n"
        "   5   0.0000        0.067890         1.8473\n",
        encoding="utf-8",
    )
    out = r._run_and_parse(tmp_path, "neutral")
    assert out["E_hartree"] == pytest.approx(-76.1234567890)
    assert out["homo_ev"] == pytest.approx(-7.3288)
    assert out["lumo_ev"] == pytest.approx(1.8473)


def test_run_and_parse_rejects_missing_orbital_block(tmp_path, monkeypatch):
    import bda.simulators.orca_runner as r

    monkeypatch.setattr(r.subprocess, "run", _fake_run)
    (tmp_path / "neutral.out").write_text(
        "FINAL SINGLE POINT ENERGY      -76.1234567890\n",
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="failed to parse ORCA output"):
        r._run_and_parse(tmp_path, "neutral")


def test_parse_orbital_energies_homo_lumo():
    """ORCA 6 ORBITAL ENERGIES 块：占据 2.0 边界定 HOMO/LUMO。"""
    from bda.simulators.orca_runner import _parse_orbital_energies

    text = (
        "ORBITAL ENERGIES\n"
        "  NO   OCC          E(Eh)            E(eV)\n"
        "   0   2.0000      -15.606757      -424.6795\n"
        "   9   2.0000       -0.437206       -11.8970\n"
        "  10   0.0000       -0.201234        -5.4759\n"
    )
    homo, lumo = _parse_orbital_energies(text)
    assert homo == -11.8970
    assert lumo == -5.4759
    assert _parse_orbital_energies("no block here") == (None, None)


def test_input_template_serial_no_pal(tmp_path):
    """ORCA 6 适配：串行（无 %pal，MS-MPI 启动不可靠）+ xyzfile + P_OrbEnergies。"""
    import bda.simulators.orca_runner as r

    r._write_input(tmp_path, "neutral", "O", 0, 1, "r2SCAN-3c", 42)
    text = (tmp_path / "neutral.inp").read_text(encoding="utf-8")
    assert "%pal" not in text  # 串行（本机 %pal 4 启动不稳定，已实测）
    assert "P_MOs" in text
    xyz = (tmp_path / "neutral.xyz").read_text(encoding="utf-8")
    assert xyz.splitlines()[0] == "3"  # 原子数行（水 = 3 原子）
