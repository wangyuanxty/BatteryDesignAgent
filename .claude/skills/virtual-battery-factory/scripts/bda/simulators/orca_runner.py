import shutil
import subprocess
import tempfile
from pathlib import Path

INPUT_TEMPLATE = "! {functional} OPT\n%output Print[ P_MOs ] 1 end\n* xyzfile {charge} {mult} {name}.xyz\n"

HARTREE_TO_EV = 27.2114

DEFAULT_FUNCTIONAL = "r2SCAN-3c"


def _multiplicity_for(smiles: str, charge: int) -> int:
    """Spin multiplicity consistent with the electron count of the charge state.

    ORCA rejects mult 1 for odd-electron species, so every charge state must
    carry its own parity-derived multiplicity: even electron count -> singlet,
    odd -> doublet (the smallest safe choice).
    """
    from rdkit import Chem

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"invalid SMILES: {smiles!r}")
    mol = Chem.AddHs(mol)
    n_electrons = sum(atom.GetAtomicNum() for atom in mol.GetAtoms()) - charge
    return 1 if n_electrons % 2 == 0 else 2


def _parse_orbital_energies(text: str) -> tuple[float | None, float | None]:
    """ORCA 6 'ORBITAL ENERGIES' 块（P_OrbEnergies 输出）→ (HOMO eV, LUMO eV)。

    行格式：NO  OCC  E(Eh)  E(eV)——HOMO=占据数 ≥1.5 的最后一个，LUMO=下一个。
    """
    lines = text.splitlines()
    start = None
    for i, l in enumerate(lines):
        if l.strip() == "ORBITAL ENERGIES":
            start = i
            break
    if start is None:
        return None, None
    rows = []
    for l in lines[start + 1 : start + 400]:
        parts = l.split()
        if len(parts) >= 4 and parts[0].lstrip("-").isdigit():
            try:
                rows.append((float(parts[3]), float(parts[1])))  # (eV, occ)
            except ValueError:
                continue
        elif rows:
            break
    if not rows:
        return None, None
    homo = lumo = None
    for ev, occ in rows:
        if occ >= 1.5:
            homo = ev
            lumo = None
        elif homo is not None and lumo is None:
            lumo = ev
            break
    return (homo if homo is not None else None, lumo if lumo is not None else None)


def _orbital_energy_ev(tokens: list) -> float:
    """Convert one ORCA E(HOMO)/E(LUMO) summary line to eV, honoring the printed unit."""
    unit = tokens[-1] if tokens else ""
    if unit not in ("a.u.", "Eh", "eV"):
        raise RuntimeError("cannot determine orbital energy unit in ORCA output")
    try:
        value = float(tokens[-2])
    except (IndexError, ValueError):
        raise RuntimeError("cannot determine orbital energy unit in ORCA output") from None
    if unit == "eV":
        return value
    return value * HARTREE_TO_EV


def _write_input(
    workdir: Path, name: str, smiles: str, charge: int, mult: int, functional: str, seed: int
) -> None:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(mol, randomSeed=seed)
    AllChem.MMFFOptimizeMolecule(mol)
    conf = mol.GetConformer()
    # ORCA 6：坐标用外部 .xyz 文件（* xyzfile 语法；旧 * xyz 内联块已移除）
    lines = [str(mol.GetNumAtoms()), name]
    for atom in mol.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        lines.append(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}")
    (workdir / f"{name}.xyz").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (workdir / f"{name}.inp").write_text(
        INPUT_TEMPLATE.format(functional=functional, charge=charge, mult=mult, name=name),
        encoding="utf-8",
    )


def _run_and_parse(workdir: Path, name: str) -> dict:
    import os

    env = dict(os.environ)
    extra = []
    orca_dir = os.path.dirname(shutil.which("orca") or "")
    mpi_dir = r"C:\Program Files\Microsoft MPI\Bin"  # MS-MPI 的 mpiexec（%pal 需要）
    if os.path.isdir(mpi_dir):
        extra.append(mpi_dir)
    if orca_dir:
        extra.append(orca_dir)
    env["PATH"] = os.pathsep.join(extra + [env.get("PATH", "")])
    proc = subprocess.run(["orca", f"{name}.inp"], cwd=workdir, capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"ORCA failed: {proc.stderr[-300:]}")
    # ORCA 6.1 输出走 stdout，不写 .out 文件（已实测）
    out_text = proc.stdout
    E = None
    for line in out_text.splitlines():
        if "FINAL SINGLE POINT ENERGY" in line:
            E = float(line.split()[-1])
    homo, lumo = _parse_orbital_energies(out_text)
    if E is None or homo is None or lumo is None:
        raise RuntimeError("failed to parse ORCA output")
    return {"E_hartree": E, "homo_ev": homo, "lumo_ev": lumo}


def orca_endorsement(smiles: str, charge: int = 0, functional: str = DEFAULT_FUNCTIONAL) -> dict:
    # _multiplicity_for parses the SMILES via RDKit and raises ValueError on
    # invalid input; computing the three multiplicities up front keeps that
    # validation ahead of the ORCA binary check.
    mults = [_multiplicity_for(smiles, q) for q in (charge, charge + 1, charge - 1)]
    if shutil.which("orca") is None:
        raise RuntimeError("ORCA binary not found; download academic Windows build from the ORCA forum")
    last_err = None
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        for attempt in range(3):
            try:
                _write_input(workdir, "neutral", smiles, charge,
                             mults[0], functional, seed=42 + attempt)
                neutral = _run_and_parse(workdir, "neutral")
                _write_input(workdir, "cation", smiles, charge + 1,
                             mults[1], functional, seed=42 + attempt)
                cation = _run_and_parse(workdir, "cation")
                _write_input(workdir, "anion", smiles, charge - 1,
                             mults[2], functional, seed=42 + attempt)
                anion = _run_and_parse(workdir, "anion")
                return {
                    "E_hartree": neutral["E_hartree"],
                    "homo_ev": neutral["homo_ev"],
                    "lumo_ev": neutral["lumo_ev"],
                    "ie_ev": (cation["E_hartree"] - neutral["E_hartree"]) * HARTREE_TO_EV,
                    "ea_ev": (neutral["E_hartree"] - anion["E_hartree"]) * HARTREE_TO_EV,
                }
            except RuntimeError as e:
                last_err = e
        raise RuntimeError(f"ORCA failed after 3 attempts for {smiles} (DFT not converged): {last_err}")
