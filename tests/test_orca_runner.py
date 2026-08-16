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
