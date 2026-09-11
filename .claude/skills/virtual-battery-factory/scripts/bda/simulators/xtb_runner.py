import shutil
import subprocess
import tempfile
from pathlib import Path

HARTREE_TO_EV = 27.2114


def _embed_mol_xyz(smiles: str, workdir: Path) -> None:
    """RDKit conformer embedding; writes workdir/mol.xyz (hydrogens included, MMFF
    pre-optimized)."""
    from rdkit import Chem
    from rdkit.Chem import AllChem

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"invalid SMILES: {smiles!r}")
    mol = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(mol, randomSeed=42) != 0:
        raise RuntimeError(f"failed to embed 3D structure for {smiles}")
    AllChem.MMFFOptimizeMolecule(mol)
    conf = mol.GetConformer()
    lines = [str(mol.GetNumAtoms()), ""]
    for atom in mol.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        lines.append(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}")
    (workdir / "mol.xyz").write_text("\n".join(lines), encoding="utf-8")


def _parse_output_text(text: str) -> tuple[float | None, float | None, float | None]:
    """Parse HOMO/LUMO and the total energy from xtb output text.

    Handles two formats:
    - xtb >= 6.5: all output goes to stdout, orbital lines carry a `(HOMO)`/`(LUMO)`
      suffix (the energy is the preceding column);
    - older xtb.out: a combined `HOMO/LUMO ... eV` line plus a `TOTAL ENERGY ... Eh` line.
    """
    homo: float | None = None
    lumo: float | None = None
    total_e: float | None = None
    for line in text.splitlines():
        if "TOTAL ENERGY" in line:
            parts = line.split()
            if len(parts) >= 4:
                total_e = float(parts[-3])
        if "(HOMO)" in line and homo is None:
            parts = line.split()
            idx = parts.index("(HOMO)")
            if idx >= 1:
                homo = float(parts[idx - 1])
        if "(LUMO)" in line and lumo is None:
            parts = line.split()
            idx = parts.index("(LUMO)")
            if idx >= 1:
                lumo = float(parts[idx - 1])
        if "HOMO/LUMO" in line:
            parts = line.replace("HOMO/LUMO", "").replace("eV", "").split()
            if len(parts) >= 2:
                homo, lumo = float(parts[0]), float(parts[1])
    return homo, lumo, total_e


def xtb_single_point(smiles: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        # RDKit parse in _embed_mol_xyz raises ValueError on invalid SMILES
        # before the xtb binary check, matching the former guard's ordering.
        _embed_mol_xyz(smiles, workdir)
        if shutil.which("xtb") is None:
            raise RuntimeError(
                "xtb binary not found; install from https://github.com/grimme-lab/xtb/releases "
                "and put xtb.exe on PATH"
            )
        proc = subprocess.run(
            ["xtb", "mol.xyz", "--gfn", "2"],
            cwd=workdir, capture_output=True, text=True, encoding="utf-8",
        )
        if proc.returncode != 0:
            raise RuntimeError(f"xtb failed: {proc.stderr[-500:]}")
        out_text = proc.stdout or ""
        # Older xtb rewrites xtb.out when stdout is redirected: fall back to reading the
        # file if stdout is empty
        if not out_text and (workdir / "xtb.out").exists():
            out_text = (workdir / "xtb.out").read_text(encoding="utf-8")
    homo, lumo, total_e = _parse_output_text(out_text)
    if homo is None or lumo is None:
        raise RuntimeError("failed to parse HOMO/LUMO from xtb output")
    if total_e is None:
        raise RuntimeError("failed to parse total energy from xtb output")
    # _parse_output_text returns the TOTAL ENERGY in Eh (as printed by xtb);
    # the exported key is named *_ev, so convert here.
    return {"homo_ev": homo, "lumo_ev": lumo, "total_energy_ev": total_e * HARTREE_TO_EV}
