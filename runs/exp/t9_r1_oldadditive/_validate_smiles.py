import json
from rdkit import Chem
from rdkit.Chem import AllChem

cands = [
    ("FVC", "O=C1OC=C(F)O1"),
    ("DFEC", "O=C1OC(F)C(F)O1"),
    ("FES", "O=S1OC(F)CO1"),
    ("VEC", "C=CC1COC(=O)O1"),
]
excl = ["C1OC(=O)OC1F", "FC1COC(=O)O1", "O=C1OC(F)CO1", "O=C1OC=CO1", "O=S1(=O)CCCO1", "O=S1(=O)OCCO1"]

excl_canon = set()
for s in excl:
    m = Chem.MolFromSmiles(s)
    excl_canon.add(Chem.MolToSmiles(m))

ok = True
for name, s in cands:
    m = Chem.MolFromSmiles(s)
    if m is None:
        print(f"{name}: INVALID SMILES {s}")
        ok = False
        continue
    canon = Chem.MolToSmiles(m)
    clash = canon in excl_canon
    if clash:
        ok = False
    print(f"{name}: {s} -> canonical {canon}  exclusion_clash={clash}  ring_atoms={m.GetNumAtoms()}")

print("ALL_OK" if ok else "HAS_PROBLEM")
