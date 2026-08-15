from bda.candidates import validate_smiles


def relax_structure(smiles: str, model: str = "mace") -> dict:
    if not validate_smiles(smiles):
        raise ValueError(f"invalid SMILES: {smiles!r}")
    if model not in ("mace", "chgnet"):
        raise ValueError(f"unknown model '{model}'; legal: mace, chgnet")
    from rdkit import Chem
    from rdkit.Chem import AllChem

    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    if AllChem.EmbedMolecule(mol, randomSeed=42) != 0:
        raise ValueError(f"failed to embed 3D structure for {smiles}")
    AllChem.MMFFOptimizeMolecule(mol)
    from ase import Atoms
    from ase.io import read as ase_read
    from io import StringIO

    xyz = Chem.MolToXYZBlock(mol)
    atoms = ase_read(StringIO(xyz), format="xyz")
    if model == "mace":
        from mace.calculators import mace_mp

        calc = mace_mp(model="medium", device="cpu")
    else:
        from chgnet.model.model import CHGNet

        calc = CHGNet.load()
    atoms.calc = calc
    from ase.optimize import BFGS

    opt = BFGS(atoms)
    converged = bool(opt.run(fmax=0.05, steps=50))
    return {"energy_ev": float(atoms.get_potential_energy()), "converged": converged}
