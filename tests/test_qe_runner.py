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


def test_cp2k_parsers():
    """CP2K 输出解析：能量行 + HOMO（占据轨道数定序号；LUMO 如实 None）。"""
    from bda.simulators.cp2k_runner import _parse_energy, _parse_homo_lumo

    text = (
        " Number of occupied orbitals:                                                 20\n"
        " MO| EIGENVALUES AND OCCUPATION NUMBERS AFTER SCF STEP 8\n"
        " MO|  Index      Eigenvalue [a.u.]        Eigenvalue [eV]             Occupation\n"
        " MO|      1              -1.165432             -31.713025                2.000\n"
        " MO|     19              -0.300000              -8.160000                2.000\n"
        " MO|     20              -0.262000              -7.135000                2.000\n"
        " ENERGY| Total FORCE_EVAL ( a.u. )               -91.158695\n"
    )
    assert _parse_energy(text) == -91.158695
    homo, lumo = _parse_homo_lumo(text)
    assert homo == -7.135
    assert lumo is None  # 本构建 EIGVALS 无虚轨道——如实 None（IE/EA 为电压窗口主指标）


def test_cp2k_input_contains_mt_solver(tmp_path):
    """CP2K 输入：PERIODIC NONE + PSOLVER MT（孤立分子必需）。"""
    from bda.simulators.cp2k_runner import build_input

    inp = build_input(["F  0.0 0.0 0.0", "C  0.5 0.5 0.5"], 0, 2, geo_opt=False,
                      workdir=str(tmp_path), name="t")
    assert "PSOLVER MT" in inp
    assert "PERIODIC NONE" in inp
    assert "CHARGE 0" in inp and "MULTIPLICITY 2" in inp
