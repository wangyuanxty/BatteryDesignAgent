import shutil
import subprocess
import tempfile
from pathlib import Path
from bda.candidates import validate_smiles


def xtb_single_point(smiles: str) -> dict:
    if not validate_smiles(smiles):
        raise ValueError(f"invalid SMILES: {smiles!r}")
    if shutil.which("xtb") is None:
        raise RuntimeError(
            "xtb binary not found; install from https://github.com/grimme-lab/xtb/releases "
            "and put xtb.exe on PATH"
        )
    from rdkit import Chem
    from rdkit.Chem import AllChem
    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    if AllChem.EmbedMolecule(mol, randomSeed=42) != 0:
        raise RuntimeError(f"failed to embed 3D structure for {smiles}")
    AllChem.MMFFOptimizeMolecule(mol)
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        conf = mol.GetConformer()
        lines = [str(mol.GetNumAtoms()), ""]
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            lines.append(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}")
        (workdir / "mol.xyz").write_text("\n".join(lines), encoding="utf-8")
        proc = subprocess.run(
            ["xtb", "mol.xyz", "--gfn", "2"],
            cwd=workdir, capture_output=True, text=True, encoding="utf-8",
        )
        if proc.returncode != 0:
            raise RuntimeError(f"xtb failed: {proc.stderr[-500:]}")
        out_text = (workdir / "xtb.out").read_text(encoding="utf-8")
    homo, lumo = None, None
    total_e = None
    for line in out_text.splitlines():
        if "HOMO/LUMO" in line:
            parts = line.replace("HOMO/LUMO", "").replace("eV", "").split()
            if len(parts) >= 2:
                homo, lumo = float(parts[0]), float(parts[1])
        if "TOTAL ENERGY" in line:
            total_e = float(line.split()[-3])
    if homo is None or lumo is None:
        raise RuntimeError("failed to parse HOMO/LUMO from xtb output")
    if total_e is None:
        raise RuntimeError("failed to parse total energy from xtb output")
    return {"homo_ev": homo, "lumo_ev": lumo, "total_energy_ev": total_e}
