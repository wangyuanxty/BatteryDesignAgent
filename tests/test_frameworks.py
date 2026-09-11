"""Framework construction regression tests for run-comp (no GPU needed).

Why this file exists: the spinel builder silently mixed up the Li and M site
multiplicities (pymatgen applies the Fd-3m origin-choice-1 setting, while the literature/COD
description uses origin choice 2), producing Li2MO4 with Li in octahedral holes and M ~3.4 A
from any oxygen — yet still returning plausible-looking "voltages" (7.8-9.0 V). Site counts
and coordination numbers are therefore asserted explicitly, so a wrong-prototype structure
cannot pass unnoticed again.
"""
import pytest

from bda.simulators.comp_runner import _framework, build_doped_structure

# formula, framework, total atoms, Li sites, TM sites
FRAMEWORK_CASES = [
    ("Li(Ni0.8Mn0.1Co0.1)O2", "layered", 48, 12, 12),
    ("LiFePO4", "olivine", 28, 4, 4),
    ("LiMn2O4", "spinel", 56, 8, 16),
    ("LiVPO4F", "tavorite_phosphate", 64, 8, 8),
    ("LiFeSO4F", "tavorite_sulfate", 64, 8, 8),
    ("Li3V2(PO4)3", "nasicon", 80, 12, 8),
]


@pytest.mark.parametrize("formula,framework,n_atoms,n_li,n_tm", FRAMEWORK_CASES)
def test_framework_dispatch_and_site_counts(formula, framework, n_atoms, n_li, n_tm):
    assert _framework(formula) == framework
    struct, counts, tm_sites = build_doped_structure(formula)
    assert len(struct) == n_atoms
    assert sum(1 for s in struct if s.specie.symbol == "Li") == n_li
    assert len(tm_sites) == n_tm
    assert sum(counts.values()) == n_tm


@pytest.mark.parametrize("formula,framework,n_atoms,n_li,n_tm", FRAMEWORK_CASES)
def test_no_atom_overlap(formula, framework, n_atoms, n_li, n_tm):
    struct, _, _ = build_doped_structure(formula)
    d = struct.distance_matrix
    assert d[d > 0].min() > 1.0  # closest contact must be a real bond, not an overlap


def test_spinel_coordination_is_physical():
    """Regression: Li must sit tetrahedrally (4 O) and M octahedrally (6 O) in the spinel."""
    struct, _, tm_sites = build_doped_structure("LiMn2O4")
    li_idx = [i for i, s in enumerate(struct) if s.specie.symbol == "Li"][0]
    tm_idx = tm_sites[0]
    li_o = sorted(struct.get_distance(li_idx, j) for j in range(len(struct))
                  if struct[j].specie.symbol == "O")
    tm_o = sorted(struct.get_distance(tm_idx, j) for j in range(len(struct))
                  if struct[j].specie.symbol == "O")
    assert 1.8 < li_o[0] < 2.1 and li_o[3] < 2.2 and li_o[4] > 2.5  # 4 O neighbours
    assert 1.8 < tm_o[0] < 2.1 and tm_o[5] < 2.2 and tm_o[6] > 2.5  # 6 O neighbours


@pytest.mark.parametrize("formula", [
    "Li2CuO2",        # Li-rich layered: needs an O2 stoichiometry rule we do not implement
    "Li2CoPO4F",      # Li2MPO4F framework: no template
    "Li2MnO2F",       # oxyfluoride: no template
    "LiNi0.5Mn1.5O3",  # oxygen-deficient spinel: unsupported ratio
])
def test_unsupported_frameworks_raise(formula):
    """Unknown frameworks must fail loudly — never be force-fitted into a prototype."""
    with pytest.raises(ValueError, match="unsupported framework"):
        _framework(formula)
