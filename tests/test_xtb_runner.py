import shutil
import pytest
from bda.simulators.xtb_runner import xtb_single_point

def test_invalid_smiles():
    with pytest.raises(ValueError, match="SMILES"):
        xtb_single_point("nope")

@pytest.mark.slow
def test_water_single_point():
    if shutil.which("xtb") is None:
        pytest.skip("xtb binary not installed")
    out = xtb_single_point("O")
    assert out["homo_ev"] < 0.0
    assert out["lumo_ev"] > out["homo_ev"]
