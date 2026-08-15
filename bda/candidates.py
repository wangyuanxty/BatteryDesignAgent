from dataclasses import dataclass
from rdkit import Chem


def validate_smiles(smiles: str) -> bool:
    if not smiles:
        return False
    mol = Chem.MolFromSmiles(smiles)
    return mol is not None


@dataclass
class Candidate:
    smiles: str
    source: str  # "seed" | "llm"
    round: int
    status: str = "pending"  # pending | passed | disputed | rejected
