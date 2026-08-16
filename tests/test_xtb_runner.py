import shutil
import pytest
from bda.simulators.xtb_runner import _parse_output_text, xtb_single_point

def test_invalid_smiles():
    with pytest.raises(ValueError, match="SMILES"):
        xtb_single_point("nope")


MODERN_OUTPUT = """\
      4        2.0000           -0.4475057             -12.1773 (HOMO)
      5                          0.0908697               2.4727 (LUMO)
      -------------------------------------------------------------
                  HL-Gap            0.5383754 Eh           14.6499 eV
       :: HOMO-LUMO gap             14.649939784554 eV    ::
        | TOTAL ENERGY               -5.070369670927 Eh   |
"""


def test_parse_output_modern_xtb_6_6_format():
    homo, lumo, total = _parse_output_text(MODERN_OUTPUT)
    assert homo == pytest.approx(-12.1773)
    assert lumo == pytest.approx(2.4727)
    assert total == pytest.approx(-5.070369670927)


def test_parse_output_legacy_homo_lumo_line():
    homo, lumo, total = _parse_output_text(
        "   HOMO/LUMO    -8.12  0.41 eV\n"
        "| TOTAL ENERGY               -123.45 Eh   |\n"
    )
    assert homo == pytest.approx(-8.12)
    assert lumo == pytest.approx(0.41)
    assert total == pytest.approx(-123.45)


def test_parse_output_missing_markers_returns_nones():
    assert _parse_output_text("no chemistry here") == (None, None, None)


def test_single_point_stdout_only(monkeypatch, tmp_path):
    """xtb 6.6.x 输出全部走 stdout（不写 xtb.out）——解析 stdout 即可。"""
    import bda.simulators.xtb_runner as xtb_mod

    class FakeProc:
        returncode = 0
        stdout = MODERN_OUTPUT
        stderr = "normal termination of xtb\n"

    monkeypatch.setattr(xtb_mod.shutil, "which", lambda name: "xtb.exe")
    monkeypatch.setattr(xtb_mod.subprocess, "run", lambda *a, **k: FakeProc())
    monkeypatch.setattr(
        xtb_mod,
        "_embed_mol_xyz",
        lambda smiles, workdir: (workdir / "mol.xyz").write_text(
            "3\n\nO 0 0 0", encoding="utf-8"
        ),
    )
    out = xtb_single_point("O")
    assert out["homo_ev"] == pytest.approx(-12.1773)
    assert out["lumo_ev"] == pytest.approx(2.4727)
    assert out["total_energy_ev"] == pytest.approx(-5.070369670927)


@pytest.mark.slow
def test_water_single_point():
    if shutil.which("xtb") is None:
        pytest.skip("xtb binary not installed")
    out = xtb_single_point("O")
    assert out["homo_ev"] < 0.0
    assert out["lumo_ev"] > out["homo_ev"]
    assert out["total_energy_ev"] is not None
