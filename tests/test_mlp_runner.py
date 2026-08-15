import pytest
from bda.simulators.mlp_runner import relax_structure


def test_invalid_smiles_fails_fast():
    with pytest.raises(ValueError, match="SMILES"):
        relax_structure("not-a-molecule")


@pytest.mark.slow
def test_water_relaxation():
    out = relax_structure("O", model="mace")
    assert "energy_ev" in out
    assert out["converged"] is True
