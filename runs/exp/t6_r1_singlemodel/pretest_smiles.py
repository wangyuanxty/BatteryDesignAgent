"""Pre-test RDKit parsing + embedding of funnel SMILES (validation only, not the funnel run)."""
from rdkit import Chem
from rdkit.Chem import AllChem

SMILES = {
    "FEC": "O=C1OC(F)CO1",
    "VC": "O=C1OC=CO1",
    "LiDFOB": "[Li+].[B-]1(F)(F)OC(=O)C(=O)O1",
    "PS": "O=S1(=O)CCCO1",
}
for name, smi in SMILES.items():
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(name, "PARSE FAIL")
        continue
    mol = Chem.AddHs(mol)
    rc = AllChem.EmbedMolecule(mol, randomSeed=42)
    print(name, "embed rc =", rc)
