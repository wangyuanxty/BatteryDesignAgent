"""Molecular true-DFT endorsement (run-cp2k): CP2K PBE-D3(BJ) + GTH basis sets (native
Windows, MSYS2 package).

Output is isomorphic to run-orca (E_hartree/homo_ev/lumo_ev/ie_ev/ea_ev): neutral state
GEO_OPT, cation/anion states as vertical single points on the neutral optimized geometry
(IE/EA are vertical values, matching the run-orca convention). CPU minutes per small
molecule (a FEC-scale 10-atom molecule ≈ 15-40 minutes/molecule).

Environment: MSYS2 `pacman -S mingw-w64-ucrt-x86_64-cp2k` (cp2k.ssmp.exe; its 2MB stack
must be patched with pefile into cp2k_stack4g.exe); data files in C:\\cp2k-data
(BASIS_MOLOPT/GTH_POTENTIALS/dftd3.dat downloaded from cp2k/cp2k GitHub data/).
"""

import os
import shutil
import subprocess
import time

_HARTREE_EV = 27.211386245988
_CP2K_DATA_CANDIDATES = [
    os.environ.get("CP2K_DATA_DIR"),
    r"C:\cp2k-data",
]

# Common electrolyte molecule elements (DZVP-MOLOPT-SR-GTH short-range basis + GTH-PBE pseudopotential)
_KIND = {"H": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE"),
         "C": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE"),
         "O": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE"),
         "F": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE"),
         "N": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE"),
         "S": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE"),
         "P": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE"),
         "B": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE"),
         "Li": ("DZVP-MOLOPT-SR-GTH", "GTH-PBE")}


def cp2k_bin() -> str:
    for cand in (
        r"C:\msys64\ucrt64\bin\cp2k_stack4g.exe",  # pefile stack-patched build (4GB reserve)
        r"C:\msys64\ucrt64\bin\cp2k.ssmp.exe",  # stock MSYS2 build (2MB stack, overflows on large molecules)
    ):
        if os.path.isfile(cand):
            return cand
    raise RuntimeError(
        "cp2k not found; install: MSYS2 pacman -S mingw-w64-ucrt-x86_64-cp2k"
    )


def data_dir() -> str:
    for cand in _CP2K_DATA_CANDIDATES:
        if cand and os.path.isdir(cand) and os.path.isfile(os.path.join(cand, "BASIS_MOLOPT")):
            return cand
    raise RuntimeError(
        "CP2K data dir not found; download BASIS_MOLOPT/GTH_POTENTIALS/dftd3.dat "
        "from github.com/cp2k/cp2k/tree/master/data to C:\\cp2k-data"
    )


def smiles_to_xyz(smiles: str) -> list[str]:
    """SMILES → RDKit 3D → xyz lines (element x y z, Å)."""
    from rdkit import Chem
    from rdkit.Chem import AllChem

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"invalid SMILES: {smiles!r}")
    mol = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(mol, randomSeed=42) != 0:
        raise ValueError(f"failed to embed 3D structure for {smiles}")
    AllChem.MMFFOptimizeMolecule(mol)
    xyz = Chem.MolToXYZBlock(mol)
    return [line for line in xyz.splitlines()[2:] if line.strip()]


def build_input(coords: list[str], charge: int, multiplicity: int, geo_opt: bool,
                workdir: str, name: str) -> str:
    """CP2K input (isolated molecule in a 20 Å vacuum box; GEO_OPT or ENERGY)."""
    dd = data_dir().replace("\\", "/")
    kinds = "\n".join(
        f"      &KIND {el}\n"
        f"        BASIS_SET {_KIND[el][0]}\n"
        f"        POTENTIAL {_KIND[el][1]}\n"
        f"      &END KIND"
        for el in sorted({line.split()[0] for line in coords})
    )
    coord_block = "\n".join(f"      {line}" for line in coords)
    run_type = "GEO_OPT" if geo_opt else "ENERGY"
    return f"""&GLOBAL
  PROJECT {name}
  RUN_TYPE {run_type}
  PRINT_LEVEL LOW
&END GLOBAL
&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME {dd}/BASIS_MOLOPT
    POTENTIAL_FILE_NAME {dd}/GTH_POTENTIALS
    CHARGE {charge}
    MULTIPLICITY {multiplicity}
    &MGRID
      CUTOFF 400
      REL_CUTOFF 60
    &END MGRID
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
    &SCF
      EPS_SCF 1.0E-7
      MAX_SCF 120
    &END SCF
    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
      &VDW_POTENTIAL
        &PAIR_POTENTIAL
          TYPE DFTD3(BJ)
          PARAMETER_FILE_NAME {dd}/dftd3.dat
          REFERENCE_FUNCTIONAL PBE
        &END PAIR_POTENTIAL
      &END VDW_POTENTIAL
    &END XC
    &PRINT
      &MO
        EIGVALS
      &END MO
    &END PRINT
  &END DFT
  &SUBSYS
    &CELL
      ABC 20.0 20.0 20.0
      PERIODIC NONE
    &END CELL
    &COORD
{coord_block}
    &END COORD
{kinds}
  &END SUBSYS
&END FORCE_EVAL
"""


def _parse_energy(text: str) -> float:
    """CP2K output → total energy (hartree)."""
    lines = [l for l in text.splitlines() if "ENERGY| Total FORCE_EVAL" in l]
    if not lines:
        raise RuntimeError("cp2k produced no total energy")
    return float(lines[-1].split()[-1])


def _parse_homo_lumo(text: str) -> tuple[float | None, float | None]:
    """Last MO eigenvalue block → (HOMO eV, LUMO eV).

    The EIGVALS output of this build has no occupation column ('MO| Index au eV') — the
    HOMO/LUMO indices are determined from the 'Number of occupied orbitals:' line
    (HOMO = the N-th, LUMO = the N+1-th).
    """
    lines = text.splitlines()
    n_occ = None
    for l in lines:
        if "Number of occupied orbitals:" in l:
            try:
                n_occ = int(l.split(":")[-1].strip())
            except ValueError:
                pass
    if n_occ is None:
        return None, None
    block_start = None
    for i, l in enumerate(lines):
        if "EIGENVALUES AND OCCUPATION NUMBERS" in l:
            block_start = i
    if block_start is None:
        return None, None
    rows: dict[int, float] = {}
    for l in lines[block_start + 1 :]:
        parts = l.split()
        if not (l.strip().startswith("MO|") and len(parts) >= 4 and parts[1].lstrip("-").isdigit()):
            if rows:
                break
            continue
        try:
            rows[int(parts[1])] = float(parts[3])  # index → eV
        except ValueError:
            continue
    return (rows.get(n_occ), rows.get(n_occ + 1))


def _ensure_statm() -> None:
    """DBCSR reads /proc/self/statm when the SCF starts (gfortran talks to the Windows CRTL
    directly, with no path translation) — so place a static page-count file at
    C:\\proc\\self\\statm (32GB convention)."""
    p = r"C:\proc\self\statm"
    if not os.path.isfile(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write("8388608 2097152 0 0 0 2097152 0\n")


def run_cp2k(workdir: str, name: str) -> tuple[float, bool, float]:
    """Run cp2k.ssmp (through MSYS2 bash: DBCSR needs /proc/self/statm, which only MSYS2
    emulates) → (energy hartree, clean exit, elapsed seconds)."""
    t0 = time.time()
    _ensure_statm()
    bash = r"C:\msys64\usr\bin\bash.exe"
    # MSYS path: C:/x/y → /c/x/y
    in_win = os.path.join(workdir, f"{name}.in").replace("\\", "/")
    in_msys = "/" + in_win[0].lower() + in_win[2:]
    bin_msys = "/" + cp2k_bin().replace("\\", "/")[0].lower() + cp2k_bin().replace("\\", "/")[2:]
    cmd = f"{bin_msys} -i '{in_msys}'"
    env = dict(os.environ)
    env["OMP_NUM_THREADS"] = str(min(8, os.cpu_count() or 4))  # 32 threads easily exhausts memory and crashes
    env["OMP_STACKSIZE"] = "512M"
    out_file = os.path.join(workdir, f"{name}.out")
    with open(out_file, "w", encoding="utf-8") as out:
        subprocess.run(
            [bash, "-lc", cmd],
            stdout=out, stderr=subprocess.STDOUT, check=False, env=env, cwd=workdir,
        )
    wall = time.time() - t0
    text = open(out_file, encoding="utf-8", errors="replace").read()
    return _parse_energy(text), ("PROGRAM ENDED" in text or "PROGRAM RAN" in text), wall


def cp2k_endorsement(smiles: str) -> dict:
    """Single-molecule true-DFT endorsement: neutral GEO_OPT + vertical single points on the
    ionic states → E/HOMO/LUMO/IE/EA."""
    import tempfile

    from bda.simulators.orca_runner import _multiplicity_for

    coords = smiles_to_xyz(smiles)
    workdir = tempfile.mkdtemp(prefix="bda_cp2k_")
    try:
        mult0 = _multiplicity_for(smiles, 0)
        inp = build_input(coords, 0, mult0, geo_opt=True, workdir=workdir, name="neutral")
        open(os.path.join(workdir, "neutral.in"), "w", encoding="utf-8").write(inp)
        e0, ok0, t0 = run_cp2k(workdir, "neutral")
        text0 = open(os.path.join(workdir, "neutral.out"), encoding="utf-8", errors="replace").read()
        homo, lumo = _parse_homo_lumo(text0)
        # Optimized geometry (neutral): take the GEO_OPT converged configuration and rewrite
        # the vertical single points with it
        opt_xyz = _extract_opt_coords(text0, coords)
        ie = ea = None
        ok_ion = True
        if opt_xyz:
            for charge, tag in ((1, "cation"), (-1, "anion")):
                mult = _multiplicity_for(smiles, charge)
                inp = build_input(opt_xyz, charge, mult, geo_opt=False, workdir=workdir, name=tag)
                open(os.path.join(workdir, f"{tag}.in"), "w", encoding="utf-8").write(inp)
                e_ion, ok, _t = run_cp2k(workdir, tag)
                ok_ion = ok_ion and ok
                if charge == 1:
                    ie = (e_ion - e0) * _HARTREE_EV
                else:
                    ea = (e0 - e_ion) * _HARTREE_EV
        return {
            "E_hartree": e0,
            "homo_ev": homo,
            "lumo_ev": lumo,
            "ie_ev": ie,
            "ea_ev": ea,
            "converged": bool(ok0 and ok_ion),
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _extract_opt_coords(text: str, coords: list[str]) -> list[str] | None:
    """GEO_OPT output → optimized coordinates (take the last &COORD block that appears)."""
    blocks = text.split("&COORD")
    if len(blocks) < 2:
        return None
    tail = blocks[-1].split("&END COORD")[0]
    lines = [l for l in tail.splitlines() if l.strip() and not l.strip().startswith("!")]
    if len(lines) != len(coords):
        return None
    return lines


def run_cp2k_endorsement(in_data: dict) -> dict:
    """IN: {"candidates": [{"smiles"}]} → OUT: one endorsement per candidate (isomorphic to run-orca)."""
    cands = in_data.get("candidates", [])
    if not cands:
        raise ValueError("input must contain a non-empty 'candidates' list")
    out = []
    for c in cands:
        smiles = str(c.get("smiles") or "")
        try:
            out.append({"smiles": smiles, "endorsement": cp2k_endorsement(smiles)})
        except (ValueError, RuntimeError) as exc:
            out.append({"smiles": smiles, "error": str(exc)})
    return {"candidates": out}
