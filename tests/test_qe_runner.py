"""run-qe 周期 DFT 背书 runner 单测（输入生成/输出解析——不跑 pw.x）。"""
import pytest

from bda.simulators.qe_runner import parse_pw_output, write_inputs


def test_write_inputs_control_and_pseudo(tmp_path):
    from pymatgen.core import Lattice, Structure

    struct = Structure(Lattice.cubic(3.51), ["Li", "Li"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    write_inputs(struct, str(tmp_path), "li", relax_cell=True)
    text = (tmp_path / "li.in").read_text(encoding="utf-8")
    assert "calculation = 'vc-relax'" in text
    assert "ecutwfc = 50" in text
    assert "li_pbe_v1.4.uspp.F.UPF" in text  # Li 赝势自动映射
    assert "tstress" in text


def test_write_inputs_magnetic_nspin(tmp_path):
    from bda.simulators.comp_runner import build_doped_structure, NMC_BASE_FORMULA

    struct, _, _ = build_doped_structure(NMC_BASE_FORMULA)
    write_inputs(struct, str(tmp_path), "nmc", relax_cell=False)
    text = (tmp_path / "nmc.in").read_text(encoding="utf-8")
    assert "nspin = 2" in text  # Ni/Mn/Co 磁性
    assert "calculation = 'relax'" in text


def test_parse_pw_output_energy_and_convergence():
    text = (
        "some noise\n"
        "!    total energy              =    -123.45678912 Ry\n"
        "convergence has been achieved\n"
    )
    energy, converged = parse_pw_output(text)
    assert energy == pytest.approx(-123.45678912 * 13.605703976)
    assert converged is True
    with pytest.raises(RuntimeError):
        parse_pw_output("no energy line here")
