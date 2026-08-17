def relax_structure(smiles: str, model: str = "mace") -> dict:
    if model not in ("mace", "chgnet"):
        raise ValueError(f"unknown model '{model}'; legal: mace, chgnet")
    from rdkit import Chem
    from rdkit.Chem import AllChem

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"invalid SMILES: {smiles!r}")
    mol = Chem.AddHs(mol)
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
        # CHGNet 需周期性晶格（pymatgen 结构转换要求非奇异晶胞）：置于 20 Å 真空盒
        atoms.cell = [20.0, 20.0, 20.0]
        atoms.pbc = True
        atoms.center()
        from chgnet.model.dynamics import CHGNetCalculator

        calc = CHGNetCalculator()
    atoms.calc = calc
    from ase.optimize import BFGS

    opt = BFGS(atoms)
    converged = bool(opt.run(fmax=0.05, steps=50))
    return {"energy_ev": float(atoms.get_potential_energy()), "converged": converged}
