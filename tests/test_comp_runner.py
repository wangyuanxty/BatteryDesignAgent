"""run-comp 组分筛选 runner 单测（结构构造/电压公式/计数取整——无需 GPU）。"""
import numpy as np
import pytest

from bda.simulators.comp_runner import (
    NMC_BASE_FORMULA,
    _largest_remainder,
    average_voltage,
    build_doped_structure,
    delithiate,
    _tm_fractions,
)


def test_largest_remainder_sums_exactly():
    counts = _largest_remainder({"Ni": 0.7, "Mn": 0.05, "Co": 0.05, "Si": 0.1, "Mg": 0.1}, 12)
    assert sum(counts.values()) == 12
    assert counts["Ni"] == 8  # 8.4 → 8（余数让给小数组分）


def test_tm_fractions_validation():
    assert _tm_fractions("Li(Ni0.8Mn0.1Co0.1)O2") == {"Ni": 0.8, "Mn": 0.1, "Co": 0.1}
    with pytest.raises(ValueError):
        _tm_fractions("Li(Ni0.9Mn0.2)O2")  # 和不等于 1


def test_base_structure_geometry():
    s, counts, tm_sites = build_doped_structure(NMC_BASE_FORMULA)
    assert len(s) == 48  # 2×2×1 超胞
    assert sum(1 for x in s if x.specie.symbol == "Li") == 12
    assert len(tm_sites) == 12
    assert sum(counts.values()) == 12
    d = s.distance_matrix
    assert d[d > 0].min() > 1.5  # 无原子重叠（Li-O ≈ 1.96 Å）


def test_delithiate_keeps_expected_lithium():
    s, _, _ = build_doped_structure(NMC_BASE_FORMULA)
    s2, keep = delithiate(s.copy(), 0.3, 42)
    assert keep == 4  # round(0.3 × 12)
    assert sum(1 for x in s2 if x.specie.symbol == "Li") == 4
    assert len(s2) == 40


def test_average_voltage_formula_lithium_reference():
    # 用自校准真实值验证公式（CHGNet: E_full=-290.97, E_del=-245.36, 8 Li removed, E_Li=-1.88）
    v = average_voltage(-290.97, -245.36, 8, -1.88)
    assert v == pytest.approx(3.80, abs=0.05)  # 文献 ≈3.8 V
    with pytest.raises(ValueError):
        average_voltage(-1, -2, 0, -1.9)
