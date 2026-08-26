"""GROMACS diffusion runner with MSD analysis (Task 14).

Produces ``run_diffusion_md(box, engine="gromacs", t_ns=10.0) -> dict`` returning
``{"D_Li_m2_s": float, "trajectory_ok": bool, "drift_check": str,
"achieved_density_g_cm3": float}``.

Rulings applied (controller preflight review, binding):
1. The brief's flow assumed conf.gro/topol.top/md.mdp/traj.xyz already exist; no
   component generated them. This module therefore implements a deterministic
   box builder ``_build_box`` (ASE-free: RDKit fixed-seed 3D templates placed on
   a fixed-seed grid; packmol is not required -- the default path is fully
   deterministic and needs only rdkit/numpy).
2. OPLS-AA .itp templates are NOT shipped (LigParGen is an interactive website,
   ilff parameters need manual conversion). ``bda/simulators/data/opls/README.md``
   documents the exact steps; the builder copies any present .itp into the run
   directory and includes them in topol.top, and fails fast with a pointer to the
   README when a required .itp is missing (no impact on the slow test, which
   skips earlier at the GROMACS check).
3. ``trajectory_ok`` follows the brief's drift semantics: mean of the trailing
   20% of Total-Energy samples vs the middle section; relative drift > 5% ->
   False. The energy table is read from ``run.log`` (``gmx mdrun -deffnm run``
   writes it there; ``md.log`` is the default name only for mdrun without
   -deffnm and carries no table for our runs). Only when neither log yields a
   usable table is the check skipped and the trajectory accepted by default
   (``"drift_check": "skipped"``).

Unit notes (documented deviations from the brief):
* The brief's MSD conversion ``slope * 1e-12 / 6`` silently assumed frame index
  == femtoseconds. This module instead fits msd over real time (frames spaced
  by ``dt_frame_fs`` fs), so the slope is in A^2/fs and D = slope * 1e-5 / 6
  (1 A^2/fs = 1e-5 m^2/s) -- correct for any output cadence and consistent with
  the "slope/6" contract.
* GROMACS internal coordinates are nm and trjconv .xyz output follows the same
  convention, but the .xyz format carries no unit metadata. ``_xyz_unit_scale``
  sniffs the first frame's coordinate spread against the conf.gro box side (nm)
  and rescales nm coordinates to A before the MSD fit, so D is unit-correct
  whichever convention trjconv uses.
* The box builder sizes grid cells as max(vdW-contact floor, density-derived
  spacing), so the achieved density lands near the 1.2 g/cm3 target (reported
  as ``achieved_density_g_cm3``) instead of the ~0.14 g/cm3 the old
  bounding-box-only grid produced, which would systematically overestimate
  Li+ diffusion. At liquid-like density the rotated rigid templates can
  partially overlap, so a real production run should start with energy
  minimization/equilibration (see README in bda/simulators/data/opls/).
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Box-builder constants (fixed seed => deterministic output for identical input)
# ---------------------------------------------------------------------------

_SEED = 42
_NSTXOUT = 100  # trajectory output interval in steps (1 fs/step -> 100 fs/frame)

# Species order is fixed; it fixes residue ordering in conf.gro and the
# [molecules] section of topol.top, so repeated builds are byte-identical.
_SPECIES = ("EC", "EMC", "PF6", "Li")

# Starting geometries come from fixed-seed RDKit embedding of these SMILES.
# PF6- and Li+ are treated as separate species (counter-ion pair added by count).
_SMILES = {
    "EC": "C1COC(=O)O1",
    "EMC": "CCOC(=O)OC",
    "PF6": "F[P-](F)(F)(F)(F)F",
}

# Expected .itp template file names inside the opls data dir (see README.md there).
_ITP_FILES = {"EC": "ec.itp", "EMC": "emc.itp", "PF6": "pf6.itp", "Li": "li.itp"}

# Approximate molar masses (g/mol) for the density-based box sizing.
_MASSES_G_MOL = {"EC": 88.06, "EMC": 104.10, "PF6": 144.96, "Li": 6.94}

_DENSITY_G_CM3 = 1.2  # approximate EC/EMC blend density used for box volume
# vdW-contact floor between grid cells (heavy-atom contact distance, C...C ~
# 3.4 A): tighter cells would place atomic cores of neighbouring molecules at
# sub-contact distance. For realistic electrolyte compositions the
# density-derived spacing exceeds this floor, so the density branch wins and
# the achieved density lands near _DENSITY_G_CM3.
_MIN_SPACING_AA = 3.0
_PADDING_FRAC = 0.05  # extra box padding beyond the grid extent
_JITTER_FRAC = 0.05  # max positional jitter as fraction of the grid cell
_AVOGADRO = 6.02214076e23

_OPLS_DIR = Path(__file__).parent / "data" / "opls"

# ---------------------------------------------------------------------------
# Deterministic box builder
# ---------------------------------------------------------------------------


def _molecule_template(name: str) -> tuple[list[str], np.ndarray]:
    """Return (symbols, positions[A]) for one species from a fixed-seed RDKit embed."""
    if name == "Li":
        return ["Li"], np.zeros((1, 3))
    from rdkit import Chem
    from rdkit.Chem import AllChem

    mol = Chem.MolFromSmiles(_SMILES[name])
    if mol is None:
        raise ValueError(f"failed to parse SMILES for {name}")
    mol = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(mol, randomSeed=_SEED) != 0:
        raise ValueError(f"failed to embed 3D structure for {name}")
    AllChem.MMFFOptimizeMolecule(mol)
    conf = mol.GetConformer()
    symbols = [atom.GetSymbol() for atom in mol.GetAtoms()]
    return symbols, np.array(conf.GetPositions(), dtype=float)


def _random_rotation(rng: np.random.Generator) -> np.ndarray:
    alpha, beta, gamma = rng.uniform(0.0, 2.0 * np.pi, size=3)
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    cg, sg = np.cos(gamma), np.sin(gamma)
    rz = np.array([[cg, -sg, 0.0], [sg, cg, 0.0], [0.0, 0.0, 1.0]])
    ry = np.array([[cb, 0.0, sb], [0.0, 1.0, 0.0], [-sb, 0.0, cb]])
    rx = np.array([[1.0, 0.0, 0.0], [0.0, ca, -sa], [0.0, sa, ca]])
    return rz @ ry @ rx


def _place_molecules(
    molecules: dict[str, int],
) -> tuple[list[dict], float, float]:
    """Grid-place all molecules deterministically.

    Returns ``(atoms, box_length_A, achieved_density_g_cm3)``.

    Cell spacing is ``max(_MIN_SPACING_AA, density_spacing)``: the vdW-contact
    floor keeps neighbouring grid cells above the heavy-atom contact distance,
    and the density spacing derives the per-cell volume from the target density
    and the total species mass, so the achieved density lands near
    ``_DENSITY_G_CM3`` whenever the density branch wins (which it does for every
    realistic electrolyte composition). The box is additionally padded so the
    outermost jittered, rotated template always fits inside it, even when the
    cells are smaller than the largest template diameter.
    """
    molecules = {name: int(molecules.get(name, 0)) for name in _SPECIES}
    rng = np.random.default_rng(_SEED)
    templates = {name: _molecule_template(name) for name in _SPECIES}
    max_diameter = max(
        float(
            (templates[name][1].max(axis=0) - templates[name][1].min(axis=0)).max()
        )
        for name in _SPECIES
    )
    n_mol = sum(molecules.values())
    grid_n = max(1, int(np.ceil(n_mol ** (1.0 / 3.0))))
    total_mass = sum(molecules[name] * _MASSES_G_MOL[name] for name in _SPECIES)
    target_volume_aa3 = total_mass / (_DENSITY_G_CM3 * _AVOGADRO) * 1e24
    density_spacing = (target_volume_aa3 / float(grid_n**3)) ** (1.0 / 3.0)
    cell = max(_MIN_SPACING_AA, density_spacing)
    jitter_amp = _JITTER_FRAC * cell
    radius = max_diameter / 2.0
    length = grid_n * cell * (1.0 + _PADDING_FRAC)
    # Containment: the outermost atom extent (offset + (grid_n-0.5)*cell +
    # jitter + radius) must stay inside [0, length]; solved for length.
    length = max(length, grid_n * cell + 2.0 * (radius + jitter_amp - cell / 2.0))
    offset = (length - grid_n * cell) / 2.0
    atoms: list[dict] = []
    slot = 0
    for name in _SPECIES:
        symbols, positions = templates[name]
        for _ in range(molecules[name]):
            gi = slot // (grid_n * grid_n)
            rem = slot % (grid_n * grid_n)
            gj = rem // grid_n
            gk = rem % grid_n
            slot += 1
            center = (
                np.array([gi + 0.5, gj + 0.5, gk + 0.5]) * cell
                + offset
                + rng.uniform(-jitter_amp, jitter_amp, size=3)
            )
            rotated = positions @ _random_rotation(rng).T
            for a, (symbol, pos) in enumerate(zip(symbols, rotated)):
                atoms.append(
                    {
                        "symbol": symbol,
                        "pos": pos + center,
                        "resid": slot,
                        "resname": name,
                        "atomname": f"{symbol}{a + 1}",
                    }
                )
    volume_cm3 = length**3 * 1e-24  # A^3 -> cm^3
    achieved_density = total_mass / (_AVOGADRO * volume_cm3)
    return atoms, length, achieved_density


def _write_gro(atoms: list[dict], length_aa: float, path: Path) -> None:
    lines = ["bda md_runner deterministic box", str(len(atoms))]
    for n, atom in enumerate(atoms, start=1):
        x, y, z = atom["pos"] / 10.0  # A -> nm
        lines.append(
            f"{atom['resid']:5d}{atom['resname']:<5s}{atom['atomname']:>5s}"
            f"{n:5d}{x:8.3f}{y:8.3f}{z:8.3f}"
        )
    side = length_aa / 10.0
    lines.append(f"{side:10.5f}{side:10.5f}{side:10.5f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_topol(molecules: dict[str, int], opls_dir: Path, path: Path) -> None:
    """Write topol.top, copying the required .itp templates into the run dir.

    Fails fast when a template is missing: with gmx installed the run could not
    proceed anyway, and the error points at the generation steps in
    bda/simulators/data/opls/README.md.
    """
    present = [name for name in _SPECIES if molecules.get(name, 0) > 0]
    missing = [
        _ITP_FILES[name]
        for name in present
        if not (opls_dir / _ITP_FILES[name]).is_file()
    ]
    if missing:
        raise RuntimeError(
            "missing OPLS-AA .itp template(s): "
            + ", ".join(missing)
            + "; generate via LigParGen/ilff and place them in "
            "bda/simulators/data/opls/ (see README.md there)"
        )
    lines = [
        "; Deterministic topology written by bda.simulators.md_runner._build_box",
        "; .itp templates copied from bda/simulators/data/opls/ (see README.md there)",
    ]
    for name in present:
        itp = _ITP_FILES[name]
        shutil.copyfile(opls_dir / itp, path.parent / itp)
        lines.append(f'#include "{itp}"')
    lines += [
        "",
        "[system]",
        "; EC/EMC/LiPF6 electrolyte box built by bda md_runner",
        "",
        "[molecules]",
    ]
    lines += [f"{name} {molecules[name]}" for name in present]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_mdp(steps: int, path: Path) -> None:
    content = f"""; Deterministic md.mdp template written by bda.simulators.md_runner._build_box
; Single-stage NVT production run, 1 fs timestep, fixed velocity seed.
integrator = md
dt = 0.001
nsteps = {steps}
nstlist = 10
cutoff-scheme = Verlet
rvdw = 1.0
rcoulomb = 1.0
pbc = xyz
tcoupl = v-rescale
tc-grps = System
tau-t = 0.1
ref-t = 298.15
gen-vel = yes
gen-temp = 298.15
gen-seed = {_SEED}
nstlog = 1000
nstenergy = 1000
nstxout = {_NSTXOUT}
nstxout-compressed = 10000
"""
    path.write_text(content, encoding="utf-8")


def _build_box(box: dict, workdir: Path) -> tuple[float, float]:
    """Deterministic GROMACS box: conf.gro + topol.top + md.mdp in workdir.

    ``box`` is ``{"molecules": {"EC": n, "EMC": n, "PF6": n, "Li": n}}`` plus an
    optional ``t_ns`` used only to size md.mdp (mdrun -nsteps overrides it at
    runtime). Same input => byte-identical output (fixed seed, fixed species
    order, no external programs).

    Returns ``(achieved_density_g_cm3, box_nm)``.
    """
    molecules = {name: int(box.get("molecules", {}).get(name, 0)) for name in _SPECIES}
    if sum(molecules.values()) < 1:
        raise ValueError("box must contain at least 1 molecule")
    steps = int(box.get("t_ns", 10.0) * 1e6)
    _write_topol(molecules, _OPLS_DIR, workdir / "topol.top")
    atoms, length_aa, achieved_density = _place_molecules(molecules)
    _write_gro(atoms, length_aa, workdir / "conf.gro")
    _write_mdp(steps, workdir / "md.mdp")
    return achieved_density, length_aa / 10.0  # A -> nm box side


# ---------------------------------------------------------------------------
# MSD analysis
# ---------------------------------------------------------------------------


def _xyz_unit_scale(trj_xyz: Path, box_nm: float) -> float:
    """Factor converting the trjconv xyz coordinates to A (10.0 or 1.0).

    GROMACS internal coordinates are nm and trjconv writes .xyz in the same
    units, but the .xyz format carries no unit metadata, so the convention is
    verified at runtime: if the first frame's max coordinate spread is
    consistent with the conf.gro box side (nm), the coordinates are nm and must
    be scaled by 10 to A; a spread ~10x the box side means the writer already
    emitted A (ASE's assumption) and the factor is 1.
    """
    if box_nm <= 0.0:
        raise ValueError("box_nm must be positive")
    from ase.io import read

    first = read(str(trj_xyz), index="0", format="xyz")
    spread = float(np.max(first.positions.max(axis=0) - first.positions.min(axis=0)))
    return 10.0 if spread <= 3.0 * box_nm else 1.0


def _gro_box_nm(gro: Path) -> float:
    """Box side in nm from the last line of a .gro file (first vector component)."""
    for line in reversed(
        gro.read_text(encoding="utf-8", errors="ignore").splitlines()
    ):
        tokens = line.split()
        if tokens:
            try:
                return float(tokens[0])
            except ValueError:
                continue
    raise ValueError(f"no box vector found in {gro}")


def _msd_diffusion(
    trj_xyz: Path,
    n_li: int,
    dt_frame_fs: float = _NSTXOUT,
    box_nm: float | None = None,
) -> float:
    """D (m^2/s) from the linear part of the unwrapped Li+ MSD: msd(t) = 6 D t.

    The slope is fitted over the second half of the curve with time in fs and
    positions in A, so D = slope[A^2/fs] * 1e-5 / 6 (1 A^2/fs = 1e-5 m^2/s).
    When ``box_nm`` (the conf.gro box side in nm) is given, the xyz units are
    sniffed against it and nm coordinates are rescaled to A first.
    """
    if dt_frame_fs <= 0.0:
        raise ValueError("dt_frame_fs must be positive")
    from ase.io import read

    frames = read(str(trj_xyz), index=":", format="xyz")
    if box_nm is not None:
        scale = _xyz_unit_scale(trj_xyz, box_nm)
        if scale != 1.0:
            for frame in frames:
                frame.set_positions(frame.positions * scale)
    li_idx = [i for i, atom in enumerate(frames[0]) if atom.symbol == "Li"]
    if len(li_idx) != n_li:
        raise ValueError(f"trajectory has {len(li_idx)} Li atoms, expected {n_li}")
    if len(frames) < 10:
        raise ValueError(f"trajectory too short for MSD fit ({len(frames)} frames)")
    msd, ts_fs = [], []
    for k, frame in enumerate(frames):
        disp = np.mean(
            [
                np.sum((frame.positions[i] - frames[0].positions[i]) ** 2)
                for i in li_idx
            ]
        )
        msd.append(disp)
        ts_fs.append(k * dt_frame_fs)
    ts_fs = np.array(ts_fs)
    msd = np.array(msd)
    half = len(ts_fs) // 2
    slope = np.polyfit(ts_fs[half:], msd[half:], 1)[0]
    return float(slope) * 1e-5 / 6.0


# ---------------------------------------------------------------------------
# Energy drift check (trajectory_ok)
# ---------------------------------------------------------------------------


def _parse_log_energies(text: str) -> list[float]:
    """Collect per-step Total-Energy samples from a GROMACS md.log table.

    md.log prints a per-nstlog table whose header contains the tokens "Step",
    "Total" and "Energy"; the numeric column is taken from the first candidate
    column ("Energy", then "Total") that parses as floats for >= 20 rows.
    """
    header = None
    for line in text.splitlines():
        tokens = line.split()
        if "Step" in tokens and "Total" in tokens and "Energy" in tokens:
            header = tokens
            break
    if header is None:
        return []
    candidates = [header.index(label) for label in ("Energy", "Total") if label in header]
    for col in candidates:
        values: list[float] = []
        for line in text.splitlines():
            tokens = line.split()
            if len(tokens) > col and tokens[0].isdigit():
                try:
                    values.append(float(tokens[col]))
                except ValueError:
                    continue
        if len(values) >= 20:
            return values
    return []


def _drift_from_values(values: list[float]) -> tuple[bool, str]:
    """(ok, status): mean of trailing 20% vs middle section, drift > 5% -> False.

    Shared by the GROMACS log path and the MACE-MP per-frame energies. Fewer
    than 20 samples -> check skipped and the trajectory accepted by default.
    """
    n = len(values)
    if n < 20:
        return True, "skipped"
    arr = np.asarray(values, dtype=float)
    mid = float(np.mean(arr[int(n * 0.25) : int(n * 0.75)]))
    tail = float(np.mean(arr[int(n * 0.8) :]))
    denom = abs(mid)
    drift = abs(tail - mid) / denom if denom > 1e-9 else abs(tail - mid)
    ok = drift <= 0.05
    return ok, "ok" if ok else "drift"


def _energy_drift_ok(workdir: Path) -> tuple[bool, str]:
    """(ok, status) from the GROMACS per-step energy table in the run logs.

    ``gmx mdrun -deffnm run`` writes the per-step energy table to ``run.log``;
    ``md.log`` is the default log name only for mdrun without -deffnm and never
    carries the table for our runs. Try ``run.log`` first, then ``md.log``; only
    when neither yields a parseable table is the check skipped and the
    trajectory accepted by default (status "skipped").
    """
    for name in ("run.log", "md.log"):
        log = workdir / name
        if not log.is_file():
            continue
        values = _parse_log_energies(log.read_text(encoding="utf-8", errors="ignore"))
        if len(values) >= 20:
            return _drift_from_values(values)
    return True, "skipped"


# ---------------------------------------------------------------------------
# MACE-MP engine (spec decision 12): ASE + MACE-MP Langevin NVT in the same
# fixed-seed box, reusing the same MSD analysis as the GROMACS path.
# ---------------------------------------------------------------------------


def _mace_calculator():
    """MACE-MP-0 medium calculator (CUDA when available, else CPU; separate
    factory so tests can mock)."""
    import torch
    from mace.calculators import mace_mp

    return mace_mp(model="medium", device="cuda" if torch.cuda.is_available() else "cpu")


def _run_mace_md(box: dict, t_ns: float) -> dict:
    from ase import Atoms, units
    from ase.io import write as ase_write
    from ase.md.langevin import Langevin

    molecules = {name: int(box.get("molecules", {}).get(name, 0)) for name in _SPECIES}
    if sum(molecules.values()) < 1:
        raise ValueError("box must contain at least 1 molecule")
    n_li = molecules.get("Li", 0)
    if n_li < 1:
        raise ValueError("box must contain at least 1 Li")
    atom_dicts, length_aa, achieved_density = _place_molecules(molecules)
    atoms = Atoms(
        symbols=[a["symbol"] for a in atom_dicts],
        positions=[a["pos"] for a in atom_dicts],
        cell=[length_aa] * 3,
        pbc=True,
    )
    try:
        atoms.calc = _mace_calculator()
    except ImportError as e:  # pragma: no cover - only when mace-torch is absent
        raise RuntimeError(
            "mace engine requires mace-torch; install via `pip install mace-torch`"
        ) from e
    if t_ns <= 0.0:
        raise ValueError("t_ns must be positive")
    steps = int(t_ns * 1e6)  # 1 fs/step
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        frames: list[Atoms] = []
        energies: list[float] = []
        dyn = Langevin(atoms, timestep=1.0 * units.fs, temperature_K=298.15, friction=0.01)
        dyn.attach(lambda: frames.append(atoms.copy()), interval=_NSTXOUT)
        dyn.attach(lambda: energies.append(atoms.get_potential_energy()), interval=_NSTXOUT)
        # chunked run with progress reporting (10% granularity, ETA) — observability
        import time as _time

        _t0 = _time.time()
        chunk = max(1, steps // 10)
        done = 0
        while done < steps:
            n = min(chunk, steps - done)
            dyn.run(n)
            done += n
            elapsed = _time.time() - _t0
            eta = elapsed / done * (steps - done)
            print(
                f"[md] {done / steps * 100:5.1f}%  {done}/{steps} steps  "
                f"elapsed={elapsed / 3600:.2f}h  eta={eta / 3600:.2f}h",
                flush=True,
            )
        trj = workdir / "traj.xyz"
        ase_write(str(trj), frames, format="xyz")
        # MACE trajectory positions are plain A and unwrapped (no trjconv step),
        # so the MSD fit runs with box_nm=None (no nm rescaling).
        d_li = _msd_diffusion(trj, n_li, dt_frame_fs=float(_NSTXOUT), box_nm=None)
    trajectory_ok, drift_check = _drift_from_values(energies)
    return {
        "D_Li_m2_s": d_li,
        "trajectory_ok": trajectory_ok,
        "drift_check": drift_check,
        "achieved_density_g_cm3": achieved_density,
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_diffusion_md(box: dict, engine: str = "gromacs", t_ns: float = 10.0) -> dict:
    """Run an NVT trajectory and return Li+ diffusivity from MSD.

    box: {"molecules": {"EC": int, "EMC": int, "PF6": int, "Li": int}}
    engine: "gromacs" (needs gmx + OPLS .itp templates) or "mace"
    (ASE + MACE-MP Langevin, needs mace-torch only).
    Returns {"D_Li_m2_s": float, "trajectory_ok": bool, "drift_check": str,
    "achieved_density_g_cm3": float}.
    """
    if engine not in ("gromacs", "mace"):
        raise ValueError(f"unknown engine '{engine}'; legal: gromacs, mace")
    if engine == "mace":
        return _run_mace_md(box, t_ns)
    if shutil.which("gmx") is None:
        raise RuntimeError(
            "GROMACS not found; install via winget install GROMACS.GROMACS or conda"
        )
    n_li = int(box.get("molecules", {}).get("Li", 0))
    if n_li < 1:
        raise ValueError("box must contain at least 1 Li")
    steps = int(t_ns * 1e6)  # 1 fs/step
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        achieved_density, _ = _build_box({**box, "t_ns": t_ns}, workdir)
        subprocess.run(
            [
                "gmx",
                "grompp",
                "-f",
                "md.mdp",
                "-c",
                "conf.gro",
                "-p",
                "topol.top",
                "-o",
                "run.tpr",
            ],
            cwd=workdir,
            check=True,
        )
        proc = subprocess.run(
            ["gmx", "mdrun", "-deffnm", "run", "-nsteps", str(steps)],
            cwd=workdir,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"gmx mdrun failed: {proc.stderr[-300:]}")
        conv = subprocess.run(
            [
                "gmx",
                "trjconv",
                "-f",
                "run.trr",
                "-s",
                "run.tpr",
                "-o",
                "traj.xyz",
                "-pbc",
                "nojump",
            ],
            cwd=workdir,
            capture_output=True,
            text=True,
            input="0\n",  # write out the whole System group
        )
        if conv.returncode != 0:
            raise RuntimeError(f"gmx trjconv failed: {conv.stderr[-300:]}")
        d_li = _msd_diffusion(
            workdir / "traj.xyz",
            n_li,
            box_nm=_gro_box_nm(workdir / "conf.gro"),
        )
        trajectory_ok, drift_check = _energy_drift_ok(workdir)
        return {
            "D_Li_m2_s": d_li,
            "trajectory_ok": trajectory_ok,
            "drift_check": drift_check,
            "achieved_density_g_cm3": achieved_density,
        }
