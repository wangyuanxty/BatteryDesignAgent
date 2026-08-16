import shutil
import subprocess
import tempfile
from pathlib import Path
from bda.candidates import validate_smiles

INPUT_TEMPLATE = "! {functional}\n%pal nprocs 4 end\n* xyz {charge} {mult}\n{xyz}\n*\n"


def _write_input(workdir: Path, name: str, smiles: str, charge: int, mult: int, functional: str) -> None:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(mol, randomSeed=42)
    AllChem.MMFFOptimizeMolecule(mol)
    conf = mol.GetConformer()
    lines = [str(mol.GetNumAtoms()), ""]
    for atom in mol.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        lines.append(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}")
    xyz_block = "\n".join(lines)
    (workdir / f"{name}.inp").write_text(
        INPUT_TEMPLATE.format(functional=functional, charge=charge, mult=mult, xyz=xyz_block),
        encoding="utf-8",
    )


def _run_and_parse(workdir: Path, name: str) -> dict:
    proc = subprocess.run(["orca", f"{name}.inp"], cwd=workdir, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ORCA failed: {proc.stderr[-300:]}")
    out_text = (workdir / f"{name}.out").read_text(encoding="utf-8")
    E, homo, lumo = None, None, None
    for line in out_text.splitlines():
        if "FINAL SINGLE POINT ENERGY" in line:
            E = float(line.split()[-1])
        if "E(HOMO)" in line:
            homo = float(line.split()[-2])
        if "E(LUMO)" in line:
            lumo = float(line.split()[-2])
    if E is None or homo is None or lumo is None:
        raise RuntimeError("failed to parse ORCA output")
    return {"E_hartree": E, "homo_ev": homo, "lumo_ev": lumo}


def orca_endorsement(smiles: str, charge: int = 0, mult: int = 1, functional: str = "r2SCAN-3c") -> dict:
    if not validate_smiles(smiles):
        raise ValueError(f"invalid SMILES: {smiles!r}")
    if shutil.which("orca") is None:
        raise RuntimeError("ORCA binary not found; download academic Windows build from the ORCA forum")
    last_err = None
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        for attempt in range(3):
            try:
                _write_input(workdir, "neutral", smiles, charge, mult, functional)
                neutral = _run_and_parse(workdir, "neutral")
                _write_input(workdir, "cation", smiles, charge + 1, 1, functional)
                cation = _run_and_parse(workdir, "cation")
                _write_input(workdir, "anion", smiles, charge - 1, 1, functional)
                anion = _run_and_parse(workdir, "anion")
                return {
                    "E_hartree": neutral["E_hartree"],
                    "homo_ev": neutral["homo_ev"],
                    "lumo_ev": neutral["lumo_ev"],
                    "ie_ev": (cation["E_hartree"] - neutral["E_hartree"]) * 27.2114,
                    "ea_ev": (neutral["E_hartree"] - anion["E_hartree"]) * 27.2114,
                }
            except RuntimeError as e:
                last_err = e
        raise RuntimeError(f"ORCA failed after 3 attempts for {smiles} (DFT not converged): {last_err}")
