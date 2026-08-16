import shutil
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from bda.simulators import md_runner
from bda.simulators.md_runner import run_diffusion_md


# ---------------------------------------------------------------------------
# Brief tests (verbatim from task brief)
# ---------------------------------------------------------------------------

def test_bad_engine():
    with pytest.raises(ValueError, match="engine"):
        run_diffusion_md({"molecules": {"EC": 100}}, engine="nope")


@pytest.mark.slow
def test_short_trajectory():
    if shutil.which("gmx") is None:
        pytest.skip("GROMACS not installed")
    out = run_diffusion_md({"molecules": {"EC": 50, "EMC": 50, "PF6": 4, "Li": 4}}, t_ns=0.1)
    assert "D_Li_m2_s" in out


# ---------------------------------------------------------------------------
# Focused non-slow tests (deterministic; gmx-independent)
# ---------------------------------------------------------------------------

def test_missing_gmx_raises(monkeypatch):
    monkeypatch.setattr(md_runner.shutil, "which", lambda name: None)
    with pytest.raises(RuntimeError, match="GROMACS not found"):
        run_diffusion_md({"molecules": {"EC": 10, "Li": 1}})


def test_no_lithium_raises(monkeypatch):
    monkeypatch.setattr(md_runner.shutil, "which", lambda name: "C:/fake/gmx.exe")
    with pytest.raises(ValueError, match="Li"):
        run_diffusion_md({"molecules": {"EC": 10}})


def _fake_opls(tmp_path: Path) -> Path:
    opls = tmp_path / "opls"
    opls.mkdir()
    for name in ("ec.itp", "emc.itp", "pf6.itp", "li.itp"):
        (opls / name).write_text(f"; fake {name}\n[ moleculetype ]\n", encoding="utf-8")
    return opls


def test_build_box_deterministic(tmp_path, monkeypatch):
    monkeypatch.setattr(md_runner, "_OPLS_DIR", _fake_opls(tmp_path))
    box = {"molecules": {"EC": 3, "EMC": 3, "PF6": 1, "Li": 1}}
    snapshots = []
    for i in range(2):
        wd = tmp_path / f"run{i}"
        wd.mkdir()
        md_runner._build_box(box, wd)
        snapshots.append({p.name: p.read_bytes() for p in sorted(wd.iterdir())})
    assert snapshots[0] == snapshots[1]
    topol = (tmp_path / "run0" / "topol.top").read_text(encoding="utf-8")
    for inc in ('#include "ec.itp"', '#include "emc.itp"', '#include "pf6.itp"', '#include "li.itp"'):
        assert inc in topol
    assert "EC 3" in topol and "EMC 3" in topol and "PF6 1" in topol and "Li 1" in topol
    gro = (tmp_path / "run0" / "conf.gro").read_text(encoding="utf-8")
    n_atoms = int(gro.splitlines()[1])
    assert n_atoms > 0
    mdp = (tmp_path / "run0" / "md.mdp").read_text(encoding="utf-8")
    assert "dt = 0.001" in mdp and "gen-seed = 42" in mdp


def test_build_box_missing_itp_raises(tmp_path, monkeypatch):
    empty = tmp_path / "no-itp"
    empty.mkdir()
    monkeypatch.setattr(md_runner, "_OPLS_DIR", empty)
    with pytest.raises(RuntimeError, match="README"):
        md_runner._build_box({"molecules": {"EC": 1, "Li": 1}}, tmp_path / "wd")


def test_build_box_empty_box_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(md_runner, "_OPLS_DIR", _fake_opls(tmp_path))
    with pytest.raises(ValueError, match="molecule"):
        md_runner._build_box({"molecules": {}}, tmp_path / "wd")


def _write_synthetic_li_traj(
    path: Path,
    n_li: int = 150,
    n_frames: int = 60,
    dt_frame_fs: float = 100.0,
    d_m2_s: float = 1e-10,
    seed: int = 7,
) -> None:
    """Brownian walkers with a known diffusivity (fixed seed, deterministic)."""
    from ase import Atoms
    from ase.io import write as ase_write

    rng = np.random.default_rng(seed)
    sigma_aa = np.sqrt(2.0 * d_m2_s * dt_frame_fs * 1e-15) / 1e-10  # per-axis, per frame, Å
    positions = np.zeros((n_li, 3))
    frames = []
    for k in range(n_frames):
        if k:
            positions = positions + rng.normal(0.0, sigma_aa, size=(n_li, 3))
        frames.append(Atoms("Li" * n_li, positions=positions.copy()))
    ase_write(str(path), frames, format="xyz")


def test_msd_diffusion_recovers_diffusivity(tmp_path):
    """Pins the MSD units: synthetic D=1e-10 m2/s walkers must come back out."""
    d_true = 1e-10
    _write_synthetic_li_traj(tmp_path / "traj.xyz", d_m2_s=d_true)
    d_fit = md_runner._msd_diffusion(tmp_path / "traj.xyz", n_li=150, dt_frame_fs=100.0)
    assert d_fit > 0.0
    assert d_fit == pytest.approx(d_true, rel=0.25)


def test_msd_diffusion_li_count_mismatch_raises(tmp_path):
    _write_synthetic_li_traj(tmp_path / "traj.xyz", n_li=10, n_frames=30)
    with pytest.raises(ValueError, match="Li atoms"):
        md_runner._msd_diffusion(tmp_path / "traj.xyz", n_li=11)


def test_msd_diffusion_too_short_raises(tmp_path):
    _write_synthetic_li_traj(tmp_path / "traj.xyz", n_li=5, n_frames=2)
    with pytest.raises(ValueError, match="too short"):
        md_runner._msd_diffusion(tmp_path / "traj.xyz", n_li=5)


def _write_fake_mdlog(path: Path, tail_energy: float, n_rows: int = 100) -> None:
    lines = ["   Step           Time         Total Energy"]
    for k in range(n_rows):
        energy = tail_energy if k >= int(n_rows * 0.8) else -1000.0
        lines.append(f"{k * 100:>10} {k * 0.1:>10.5f} {energy:>12.5f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_drift_check_stable_log_ok(tmp_path):
    _write_fake_mdlog(tmp_path / "md.log", tail_energy=-1000.0)
    ok, status = md_runner._energy_drift_ok(tmp_path / "md.log")
    assert ok is True
    assert status == "ok"


def test_drift_check_drifting_log_fails(tmp_path):
    # last 20% of frames sit 20% above the middle section -> drift flagged
    _write_fake_mdlog(tmp_path / "md.log", tail_energy=-800.0)
    ok, status = md_runner._energy_drift_ok(tmp_path / "md.log")
    assert ok is False
    assert status == "drift"


def test_drift_check_skipped_without_log(tmp_path):
    ok, status = md_runner._energy_drift_ok(tmp_path / "missing" / "md.log")
    assert ok is True
    assert status == "skipped"


def test_parse_log_energies_no_header():
    assert md_runner._parse_log_energies("no table here\njust words\n") == []


def test_drift_check_skipped_with_insufficient_rows(tmp_path):
    log = tmp_path / "md.log"
    log.write_text("   Step           Time         Total Energy\n" + "".join(
        f"{k * 100:>10} {k * 0.1:>10.5f} {-1000.0:>12.5f}\n" for k in range(5)
    ), encoding="utf-8")
    ok, status = md_runner._energy_drift_ok(log)
    assert ok is True
    assert status == "skipped"


def test_parse_log_energies_unparseable_columns():
    text = "   Step           Time         Total Energy\n"
    text += "".join(f"{k * 100:>10} {k * 0.1:>10.5f} nope\n" for k in range(30))
    assert md_runner._parse_log_energies(text) == []


def test_msd_diffusion_nonpositive_frame_interval_raises(tmp_path):
    _write_synthetic_li_traj(tmp_path / "traj.xyz", n_li=5, n_frames=30)
    with pytest.raises(ValueError, match="dt_frame_fs"):
        md_runner._msd_diffusion(tmp_path / "traj.xyz", n_li=5, dt_frame_fs=0.0)


def test_molecule_template_invalid_smiles_raises(monkeypatch):
    import rdkit.Chem as Chem

    monkeypatch.setattr(Chem, "MolFromSmiles", lambda smiles: None)
    with pytest.raises(ValueError, match="SMILES"):
        md_runner._molecule_template("EC")


def test_molecule_template_embed_failure_raises(monkeypatch):
    import rdkit.Chem.AllChem as AllChem

    monkeypatch.setattr(AllChem, "EmbedMolecule", lambda mol, **kwargs: -1)
    with pytest.raises(ValueError, match="embed"):
        md_runner._molecule_template("EC")


@pytest.fixture
def fake_gmx_env(tmp_path, monkeypatch):
    monkeypatch.setattr(md_runner, "_OPLS_DIR", _fake_opls(tmp_path))
    monkeypatch.setattr(md_runner.shutil, "which", lambda name: f"C:/fake/{name}.exe")
    return tmp_path


def _patch_subprocess(monkeypatch, mdrun_rc=0, trjconv_rc=0):
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append((list(cmd), kwargs))
        if "gmx" in cmd and cmd[cmd.index("gmx") + 1] == "mdrun":
            return SimpleNamespace(returncode=mdrun_rc, stdout="", stderr="simulation crashed")
        if "gmx" in cmd and cmd[cmd.index("gmx") + 1] == "trjconv":
            return SimpleNamespace(returncode=trjconv_rc, stdout="", stderr="conversion failed")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(md_runner.subprocess, "run", fake_run)
    return calls


def test_run_diffusion_md_orchestration(tmp_path, fake_gmx_env, monkeypatch):
    calls = _patch_subprocess(monkeypatch)
    monkeypatch.setattr(md_runner, "_msd_diffusion", lambda trj, n_li, dt_frame_fs=100.0: 1.5e-10)
    box = {"molecules": {"EC": 3, "EMC": 3, "PF6": 1, "Li": 1}}
    out = md_runner.run_diffusion_md(box, t_ns=0.001)
    assert out == {"D_Li_m2_s": 1.5e-10, "trajectory_ok": True, "drift_check": "skipped"}
    joined = [" ".join(c) for c, _ in calls]
    assert any("grompp" in j and "conf.gro" in j and "topol.top" in j for j in joined)
    assert any("mdrun" in j and "-nsteps 1000" in j for j in joined)
    assert any("trjconv" in j and "traj.xyz" in j for j in joined)


@pytest.mark.parametrize("which_fails", ["mdrun", "trjconv"])
def test_run_diffusion_md_subprocess_failure(tmp_path, fake_gmx_env, monkeypatch, which_fails):
    _patch_subprocess(monkeypatch, mdrun_rc=1 if which_fails == "mdrun" else 0,
                      trjconv_rc=1 if which_fails == "trjconv" else 0)
    box = {"molecules": {"EC": 3, "EMC": 3, "PF6": 1, "Li": 1}}
    with pytest.raises(RuntimeError, match="failed"):
        md_runner.run_diffusion_md(box, t_ns=0.001)
