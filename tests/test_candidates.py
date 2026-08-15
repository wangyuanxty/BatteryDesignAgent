from bda.candidates import Candidate, validate_smiles

def test_valid_smiles():
    assert validate_smiles("CCO") is True
    assert validate_smiles("O=C1OCCO1") is True  # EC
    assert validate_smiles("not-a-molecule") is False
    assert validate_smiles("") is False

def test_candidate_status_flow():
    c = Candidate(smiles="CCO", source="seed", round=1)
    assert c.status == "pending"
