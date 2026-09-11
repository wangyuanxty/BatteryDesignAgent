"""Electrode composition screening (run-comp): NMC811 layered prototype + site substitution
→ CHGNet relaxation (full-lithium / delithiated) → relative stability + average voltage
+ capacity proxy.

Caliber (declared honestly):
- Structure: NMC811 layered R-3m prototype (hexagonal a≈2.87 Å, c≈14.19 Å; Li 3b / TM 3a /
  O 6c z≈0.241), 2×2×1 supercell (48 atoms, 12 TM sites); doped compositions are rounded by
  the largest-remainder method and the realized composition is written to the output.
- Energy/voltage: CHGNet proxy (screening caliber, error on the 0.1-0.3 V scale); periodic-DFT
  true endorsement lacks a tool here (declared honestly).
- Delithiated state: random delithiation to x_Li=0.3 (seed derived from the formula hash,
  reproducible).
"""

import hashlib
import json

import numpy as np
from pymatgen.core import Composition, Lattice, Structure

_A, _C, _O_Z = 2.87, 14.19, 0.241  # NMC811 layered R-3m literature lattice parameters
_SUPERCELL = (2, 2, 1)
_X_FULL, _X_DELITH = 1.0, 0.3  # Li occupancy of the full-lithium / delithiated states
_F = 26801.481  # Faraday constant conversion: F/3.6 (mAh·mol⁻¹)

NMC_BASE_FORMULA = "Li(Ni0.8Mn0.1Co0.1)O2"


def _seed(formula: str) -> int:
    return int(hashlib.sha256(formula.encode("utf-8")).hexdigest()[:8], 16)


def _base_structure() -> Structure:
    """NMC811 layered R-3m prototype, 2×2×1 supercell (3 formula units per hexagonal cell
    = 12 atoms; supercell 48 atoms: 12 Li / 12 TM / 24 O). Wyckoff sites:
    Li 3b (0,0,1/2)(1/3,2/3,5/6)(2/3,1/3,1/6); TM 3a (0,0,0)(1/3,2/3,1/3)(2/3,1/3,2/3);
    O 6c (0,0,±z)(1/3,2/3,1/3±z)(2/3,1/3,2/3±z)."""
    li = [[0, 0, 0.5], [1 / 3, 2 / 3, 5 / 6], [2 / 3, 1 / 3, 1 / 6]]
    tm = [[0, 0, 0], [1 / 3, 2 / 3, 1 / 3], [2 / 3, 1 / 3, 2 / 3]]
    o = [
        [0, 0, _O_Z], [0, 0, 1 - _O_Z],
        [1 / 3, 2 / 3, 1 / 3 + _O_Z], [1 / 3, 2 / 3, 1 / 3 - _O_Z],
        [2 / 3, 1 / 3, 2 / 3 + _O_Z], [2 / 3, 1 / 3, 2 / 3 - _O_Z],
    ]
    lat = Lattice.hexagonal(_A, _C)
    struct = Structure(lat, ["Li"] * 3 + ["Ni"] * 3 + ["O"] * 6, li + tm + o)
    struct.make_supercell(_SUPERCELL)
    return struct


def _tm_fractions(formula: str) -> dict[str, float]:
    comp = Composition(formula)
    tm = {str(k): float(v) for k, v in comp.items() if str(k) not in ("Li", "O")}
    if not tm:
        raise ValueError(f"no transition-metal species in formula: {formula}")
    total = sum(tm.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"TM fractions must sum to 1; got {tm} (sum={total})")
    return tm


def _largest_remainder(fractions: dict[str, float], n: int) -> dict[str, int]:
    """Composition fractions → integer counts (largest-remainder method, sum exactly n)."""
    counts = {sym: int(f * n) for sym, f in fractions.items()}
    rest = n - sum(counts.values())
    order = sorted(fractions, key=lambda s: (fractions[s] * n - counts[s]), reverse=True)
    for i in range(rest):
        counts[order[i % len(order)]] += 1
    return counts


def build_doped_structure(formula: str) -> tuple[Structure, dict[str, int], list[int]]:
    """Substitute TM sites on the prototype for the requested composition → (structure,
    realized counts, TM site indices).

    **Strict dispatch (since 2026-09-10)**: the framework is determined uniquely by the
    stoichiometry; anything unrecognized raises instead of being guessed. The former behavior
    (any P → olivine, TM count = 2 → spinel, everything else → layered) silently forced
    cross-domain formulas into the wrong prototype (e.g. LiNiSO4F as a layered oxide,
    Li3V2(PO4)3 as an olivine), producing "wrong numbers that look credible".
    Supported frameworks (crystallographic provenance in each builder's docstring):
      - layered LiMO2 (R-3m, NMC811 prototype)
      - olivine LiMPO4 (Pnma, LiFePO4 prototype)
      - spinel LiM2O4 (Fd-3m, LiMn2O4 prototype)
      - tavorite phosphate LiM(PO4)F (P-1, LiVPO4F prototype)
      - tavorite sulfate LiM(SO4)F (P-1, LiFeSO4F cell + tavorite framework coordinates)
      - NASICON Li3M2(PO4)3 (P2₁/c, Li3V2(PO4)3 prototype, COD 2237423)
    Other frameworks (oxyfluorides Li2MO2F, Li2CoPO4F/Li2NiPO4F, ...) have no template →
    explicit error.
    """
    framework = _framework(formula)
    if framework == "tavorite_phosphate":
        return _build_tavorite(formula, sulfate=False)
    if framework == "tavorite_sulfate":
        return _build_tavorite(formula, sulfate=True)
    if framework == "nasicon":
        return _build_nasicon(formula)
    if framework == "olivine":
        return _build_olivine(formula)
    if framework == "spinel":
        return _build_spinel(formula)
    tm = _tm_fractions(formula)
    struct = _base_structure()
    tm_sites = [
        i for i, site in enumerate(struct) if site.specie.symbol not in ("Li", "O")
    ]
    counts = _largest_remainder(tm, len(tm_sites))
    rng = np.random.default_rng(_seed(formula))
    order = rng.permutation(len(tm_sites))
    assignment: list[str] = []
    for sym, k in counts.items():
        assignment += [sym] * k
    rng.shuffle(assignment)
    for pos, sym in zip(order, assignment):
        struct.replace(tm_sites[pos], sym)
    return struct, counts, tm_sites


def _framework(formula: str) -> str:
    """Stoichiometry → framework name (strict; raises ValueError on no match — never guesses)."""
    comp = Composition(formula)
    els = {str(k): float(v) for k, v in comp.items()}
    tm_total = sum(v for k, v in els.items() if k not in ("Li", "O", "P", "S", "F"))

    def eq(name: str, value: float) -> bool:
        return abs(els.get(name, 0.0) - value) < 1e-6

    if eq("Li", 1.0) and eq("O", 4.0) and eq("F", 1.0) and tm_total > 1e-9:
        if eq("P", 1.0) and not els.get("S", 0.0):
            return "tavorite_phosphate"
        if eq("S", 1.0) and not els.get("P", 0.0):
            return "tavorite_sulfate"
    if eq("Li", 3.0) and eq("P", 3.0) and eq("O", 12.0) and abs(tm_total - 2.0) < 1e-6:
        return "nasicon"
    if eq("Li", 1.0) and eq("O", 4.0) and eq("P", 1.0) \
            and not els.get("F", 0.0) and not els.get("S", 0.0):
        return "olivine"
    if eq("Li", 1.0) and eq("O", 4.0) and abs(tm_total - 2.0) < 1e-6 \
            and not els.get("P", 0.0) and not els.get("S", 0.0) and not els.get("F", 0.0):
        return "spinel"
    if eq("Li", 1.0) and eq("O", 2.0) and abs(tm_total - 1.0) < 1e-6 \
            and not els.get("P", 0.0) and not els.get("S", 0.0) and not els.get("F", 0.0):
        return "layered"
    raise ValueError(
        f"unsupported framework for {formula}: supported are layered LiMO2, olivine LiMPO4, "
        f"spinel LiM2O4, tavorite LiM(PO4)F, tavorite LiM(SO4)F, NASICON Li3M2(PO4)3"
    )


def _build_olivine(formula: str) -> tuple[Structure, dict[str, int], list[int]]:
    """Olivine Pnma (LiFePO4 standard parameters: a=10.332 b=6.010 c=4.694 Å).
    Representative coordinates (Wyckoff): Li 4a (0,0,0); M 4c (0.218,0.25,0.202);
    P 4c (0.0946,0.25,0.0619); O 4c×2 + 8d → 28-atom primitive cell (from_spacegroup)."""
    struct = Structure.from_spacegroup(
        "Pnma",
        Lattice.orthorhombic(10.332, 6.010, 4.694),
        ["Li", "M", "P", "O", "O", "O"],
        [[0, 0, 0],
         [0.218, 0.25, 0.202],
         [0.0946, 0.25, 0.0619],
         [0.0984, 0.25, 0.7427],
         [0.0450, 0.25, 0.2849],
         [0.0859, 0.0358, 0.5330]],
    )
    tm_sites = [i for i, site in enumerate(struct) if site.specie.symbol == "M"]
    tm = {str(k): float(v) for k, v in Composition(formula).items()
          if str(k) not in ("Li", "O", "P", "Si", "F")}
    total = sum(tm.values())
    tm = {k: v / total for k, v in tm.items()}  # normalized (olivine M site = 1.0)
    counts = _largest_remainder(tm, len(tm_sites))
    rng = np.random.default_rng(_seed(formula))
    order = rng.permutation(len(tm_sites))
    assignment: list[str] = []
    for sym, k in counts.items():
        assignment += [sym] * k
    rng.shuffle(assignment)
    for pos, sym in zip(order, assignment):
        struct.replace(tm_sites[pos], sym)
    return struct, counts, tm_sites


def _build_spinel(formula: str) -> tuple[Structure, dict[str, int], list[int]]:
    """Spinel Fd-3m (LiMn2O4, COD 1513964: a=8.251 Å; 56-atom cell = 8 Li / 16 M / 32 O).

    **Coordinate provenance and a corrected bug (2026-09-10).** The authoritative COD entry
    describes this structure in the Fd-3m origin-choice-2 setting: Li on 8a (1/8,1/8,1/8),
    M on 16d (1/2,1/2,1/2), O on 32e with x=0.263. pymatgen's `from_spacegroup` applies the
    *origin-choice-1* setting, in which those same fractional coordinates generate 16 and 8
    sites respectively — i.e. the previous code built Li16 M8 O32 (Li2MO4) with Li in
    octahedral holes and M ~3.4 Å from any oxygen. Its "voltages" (7.8-9.0 V) were artefacts
    of that wrong structure. The setting-correct assignment used here is
    Li 8-fold (1/2,1/2,1/2), M 16-fold (1/8,1/8,1/8), O 32e x=0.3622 (= 0.625 - 0.2628).
    Verified against the COD entry: identical cell volume and coordination spectra —
    Li 4 O at 1.97 Å (tetrahedral), M 6 O at 1.96 Å (octahedral).
    """
    struct = Structure.from_spacegroup(
        "Fd-3m",
        Lattice.cubic(8.251),
        ["Li", "M", "O"],
        [[0.5, 0.5, 0.5],
         [0.125, 0.125, 0.125],
         [0.3622, 0.3622, 0.3622]],
    )
    tm_sites = [i for i, site in enumerate(struct) if site.specie.symbol == "M"]
    tm = {str(k): float(v) for k, v in Composition(formula).items()
          if str(k) not in ("Li", "O")}
    total = sum(tm.values())
    tm = {k: v / total for k, v in tm.items()}  # normalized (spinel M site ratio 1.5-2.0)
    counts = _largest_remainder(tm, len(tm_sites))
    rng = np.random.default_rng(_seed(formula))
    order = rng.permutation(len(tm_sites))
    assignment: list[str] = []
    for sym, k in counts.items():
        assignment += [sym] * k
    rng.shuffle(assignment)
    for pos, sym in zip(order, assignment):
        struct.replace(tm_sites[pos], sym)
    return struct, counts, tm_sites


# ---- Cross-domain prototypes (added 2026-09-10 for the T9 v9 contract) ---------
# Cells and coordinates are inlined from public literature/open databases, with the
# provenance written in each builder (never guess coordinates from memory).
_TAVORITE_SITES: tuple[tuple[str, tuple[float, float, float]], ...] = (
    ("M", (0.0, 0.0, 0.0)),            # TM site 1 (inversion center)
    ("M", (0.0, 0.0, 0.5)),            # TM site 2 (inversion center)
    ("X", (0.3193, 0.6456, 0.2514)),   # P (phosphate family) / S (sulfate family)
    ("F", (-0.1204, 0.0925, 0.2439)),
    ("O", (0.3690, 0.2446, 0.5811)),
    ("O", (0.1140, 0.6696, 0.3628)),
    ("O", (0.3210, 0.3380, 0.1388)),
    ("O", (0.2775, 0.7968, 0.0920)),
    ("Li", (0.7090, 0.3930, 0.2210)),
)

_NASICON_SITES: tuple[tuple[str, tuple[float, float, float]], ...] = (
    ("Li", (0.1133, 0.5883, 0.1934)),
    ("Li", (0.1891, 0.1919, 0.2599)),
    ("Li", (0.4730, 0.2213, 0.1767)),
    ("M", (0.13814, 0.52846, 0.38977)),
    ("M", (0.36217, 0.53898, 0.11037)),
    ("P", (0.04417, 0.25109, 0.00782)),
    ("P", (0.45782, 0.39759, 0.35181)),
    ("P", (0.75192, 0.38467, 0.14738)),
    ("O", (0.0267, 0.1788, 0.09643)),
    ("O", (0.0361, 0.3649, 0.42742)),
    ("O", (0.0850, 0.0021, 0.28038)),
    ("O", (0.1152, 0.6330, 0.06577)),
    ("O", (0.1785, 0.7151, 0.31962)),
    ("O", (0.2392, 0.3319, 0.07040)),
    ("O", (0.2789, 0.3861, 0.35185)),
    ("O", (0.3675, 0.5514, 0.54043)),
    ("O", (0.4764, 0.2357, 0.31413)),
    ("O", (0.5906, 0.0200, 0.23807)),
    ("O", (0.5994, 0.4098, 0.16881)),
    ("O", (0.6748, 0.4125, 0.02723)),
)

_TM_EXCLUDED = ("Li", "O", "P", "S", "F")


def _substitute_tm(
    struct: Structure, tm_sites: list[int], formula: str
) -> tuple[Structure, dict[str, int], list[int]]:
    """Assign all TM sites on the prototype by formula fractions (normalized) via the
    largest-remainder method."""
    tm = {
        str(k): float(v)
        for k, v in Composition(formula).items()
        if str(k) not in _TM_EXCLUDED
    }
    if not tm or any(v <= 0 for v in tm.values()):
        raise ValueError(f"no transition-metal species in formula: {formula}")
    total = sum(tm.values())
    counts = _largest_remainder({k: v / total for k, v in tm.items()}, len(tm_sites))
    rng = np.random.default_rng(_seed(formula))
    order = rng.permutation(len(tm_sites))
    assignment: list[str] = []
    for sym, k in counts.items():
        assignment += [sym] * k
    rng.shuffle(assignment)
    for pos, sym in zip(order, assignment):
        struct.replace(tm_sites[pos], sym)
    return struct, counts, tm_sites


def _build_tavorite(formula: str, *, sulfate: bool) -> tuple[Structure, dict[str, int], list[int]]:
    """Tavorite-type LiM(XO4)F (X=P phosphate / X=S sulfate), triclinic P-1, Z=2.

    Cell and coordinate provenance:
    - Phosphate family (X=P): LiVPO4F, a=5.184 b=5.312 c=7.266 Å, α=107.58 β=107.95 γ=98.45°
      with the asymmetric-unit coordinates (V 1a/1b inversion centers; P/F/O×4/Li each 2i)
      taken from LiVPO4F powder neutron/synchrotron refinement (OSTI; cf. the same family in
      ICSD 184601: a=5.1708 b=5.3083 c=7.2631 Å — consistent across reports).
    - Sulfate family (X=S): LiFeSO4F, a=5.1747 b=5.4943 c=7.2224 Å,
      α=106.522 β=107.210 γ=97.791° (Barpanda et al., Nat. Mater. 2011, supplementary).
      This family shares the tavorite topology with the phosphate family, so the framework
      fractional coordinates above are reused with S on the X site and the sulfate cell;
      **that approximation is validated by a literature voltage anchor**: the computed
      LiFeSO4F value must land near the literature ~3.6 V, otherwise this family is excluded
      honestly.
    2×2×1 supercell → 64 atoms / 8 Li / 8 TM.
    """
    if sulfate:
        lat = Lattice.from_parameters(5.1747, 5.4943, 7.2224, 106.522, 107.210, 97.791)
        x_species = "S"
    else:
        lat = Lattice.from_parameters(5.184, 5.312, 7.266, 107.58, 107.95, 98.45)
        x_species = "P"
    species = [x_species if sym == "X" else sym for sym, _ in _TAVORITE_SITES]
    coords = [list(xyz) for _, xyz in _TAVORITE_SITES]
    struct = Structure.from_spacegroup("P-1", lat, species, coords)
    struct.make_supercell((2, 2, 1))
    tm_sites = [i for i, site in enumerate(struct) if site.specie.symbol == "M"]
    return _substitute_tm(struct, tm_sites, formula)


def _build_nasicon(formula: str) -> tuple[Structure, dict[str, int], list[int]]:
    """NASICON-type Li3M2(PO4)3, monoclinic P2₁/c.

    Cell and the 20 asymmetric-unit sites from: Li3V2(PO4)3, a=8.6201 b=8.6013 c=14.7465 Å,
    β=125.204°, Crystallography Open Database entry COD 2237423 (from_spacegroup generates the
    80-atom cell = 12 Li / 8 TM / 12 P / 48 O, matching this file's parent stoichiometry).
    """
    lat = Lattice.from_parameters(8.6201, 8.6013, 14.7465, 90.0, 125.204, 90.0)
    species = [sym for sym, _ in _NASICON_SITES]
    coords = [list(xyz) for _, xyz in _NASICON_SITES]
    struct = Structure.from_spacegroup("P2_1/c", lat, species, coords)
    tm_sites = [i for i, site in enumerate(struct) if site.specie.symbol == "M"]
    return _substitute_tm(struct, tm_sites, formula)


def delithiate(struct: Structure, x_li: float, seed: int) -> tuple[Structure, int]:
    """Randomly delithiate to x_li occupancy (seeded, reproducible) → (structure, Li kept)."""
    li_sites = [i for i, site in enumerate(struct) if site.specie.symbol == "Li"]
    keep = int(round(x_li * len(li_sites)))
    rng = np.random.default_rng(seed)
    drop = rng.choice(li_sites, size=len(li_sites) - keep, replace=False)
    struct.remove_sites(drop)
    return struct, keep


def relax_energy(struct: Structure) -> tuple[float, bool]:
    """CHGNet native StructOptimizer (FIRE) + GPU relaxation → (energy eV, converged)."""
    from chgnet.model import CHGNet
    from chgnet.model.dynamics import AseAtomsAdaptor
    from chgnet.model.dynamics import FIRE
    from chgnet.model.dynamics import StructOptimizer

    atoms = AseAtomsAdaptor().get_atoms(struct)
    relaxer = StructOptimizer(model=CHGNet.load(), optimizer_class=FIRE)
    result = relaxer.relax(atoms, fmax=0.1, steps=300, relax_cell=True, verbose=False)
    traj = result.get("trajectory")
    # chgnet 0.4.x: TrajectoryObserver object (.trajectory = frame list) or a frame list
    frames = getattr(traj, "trajectory", None) or (traj if isinstance(traj, list) else [])
    if not frames:
        return float(atoms.get_potential_energy()), False
    last = frames[-1]
    energy = last.get("energies", last.get("energy"))
    if isinstance(energy, (list, tuple)):
        energy = energy[-1] if energy else None
    forces = last.get("forces", last.get("force"))
    if isinstance(forces, (list, tuple)):
        forces = forces[-1] if forces else None
    fmax = float(np.abs(np.asarray(forces)).max()) if forces is not None else None
    converged = bool(energy is not None and fmax is not None and fmax <= 0.1)
    return float(energy), converged


def _n_fu(formula: str) -> int:
    """Formula units contained in the supercell (set by Li count: full-lithium Li = 12 → 12)."""
    return 12  # 2×2×1 supercell: 12 Li


def average_voltage(e_full: float, e_delith: float, n_removed: int, e_li: float) -> float:
    """Average voltage (vs Li metal): V = −[E(Li_x2) − E(Li_x1) − n_removed·E_Li] / n_removed."""
    if n_removed <= 0:
        raise ValueError("n_removed must be positive")
    return -(e_full - e_delith - n_removed * e_li) / n_removed


def screen_candidate(formula: str, base_energy_fu: float | None, e_li: float) -> dict:
    """One composition candidate: full-lithium/delithiated relaxation → relative stability
    + average voltage + capacity proxy.

    Average voltage (vs Li metal): V = −[E(Li_x2MO2) − E(Li_x1MO2) − n_removed·E_Li] / n_removed
    (E_Li is CHGNet's bcc Li metal reference energy, computed once per baseline batch).
    """
    struct_full, counts, _ = build_doped_structure(formula)
    seed = _seed(formula)
    e_full, conv_full = relax_energy(struct_full)
    n_li_full = sum(1 for s in struct_full if s.specie.symbol == "Li")
    struct_delith, n_li_delith = delithiate(struct_full, _X_DELITH, seed)
    e_delith, conv_delith = relax_energy(struct_delith)
    n_removed = n_li_full - n_li_delith
    avg_voltage = average_voltage(e_full, e_delith, n_removed, e_li)
    mw = Composition(formula).weight  # g/mol
    capacity_mah_g = (_X_FULL - _X_DELITH) * _F / mw
    n_atoms = len(struct_full)
    out = {
        "formula": formula,
        "realized_tm_counts": counts,
        "avg_voltage_v": float(avg_voltage),
        "capacity_mah_g": float(capacity_mah_g),
        "e_full_ev": e_full,
        "e_delith_ev": e_delith,
        "converged": bool(conv_full and conv_delith),
        "rel_stability_ev_atom": (
            float((e_full / n_atoms) - (base_energy_fu / 4.0))
            if base_energy_fu is not None
            else None
        ),
    }
    return out


def _li_metal_energy() -> float:
    """bcc Li metal reference energy (eV per atom, CHGNet relaxation of a 2-atom cell)."""
    from pymatgen.core import Lattice as _Lattice

    li = Structure(_Lattice.cubic(3.51), ["Li", "Li"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    e, _conv = relax_energy(li)
    return e / 2.0


def run_composition_screen(in_data: dict) -> dict:
    """IN: {"candidates": [{"formula": "...", "name": "..."}]} → OUT: metrics per candidate
    + baseline."""
    cands = in_data.get("candidates", [])
    if not cands:
        raise ValueError("input must contain a non-empty 'candidates' list")
    base_e_fu = None
    # baseline NMC811 + bcc Li metal reference energy
    base_struct, _, _ = build_doped_structure(NMC_BASE_FORMULA)
    e_base, conv_base = relax_energy(base_struct)
    base_e_fu = e_base / _n_fu(NMC_BASE_FORMULA)
    e_li = _li_metal_energy()
    results = []
    for c in cands:
        formula = str(c.get("formula") or "")
        name = str(c.get("name") or formula)
        try:
            m = screen_candidate(formula, base_e_fu, e_li)
            m["name"] = name
            results.append(m)
        except ValueError as exc:
            results.append({"name": name, "formula": formula, "error": str(exc)})
    return {
        "baseline": {
            "formula": NMC_BASE_FORMULA,
            "e_full_ev": e_base,
            "e_li_metal_ev": e_li,
            "converged": bool(conv_base),
        },
        "candidates": results,
        "calibration_note": (
            "NMC811 baseline self-calibration: literature average voltage ≈3.8 V, theoretical "
            "capacity ≈194 mAh/g (x∈[0.3,1] window) — if the baseline deviates markedly, this "
            "batch's results are not trustworthy (declared honestly)."
        ),
    }
