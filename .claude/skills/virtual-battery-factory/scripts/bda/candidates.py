from rdkit import Chem


def validate_smiles(smiles: str) -> bool:
    if not smiles:
        return False
    mol = Chem.MolFromSmiles(smiles)
    return mol is not None
