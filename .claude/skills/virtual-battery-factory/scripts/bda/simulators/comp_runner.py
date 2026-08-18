"""电极组分候选筛选（run-comp）：NMC811 层状原型 + 位点替换 → CHGNet 弛豫（满锂/去锂两态）
→ 相对稳定性 + 平均电压 + 容量代理。

口径（如实声明）：
- 结构：NMC811 层状 R-3m 原型（六方 a≈2.87 Å, c≈14.19 Å；Li 3b / TM 3a / O 6c z≈0.241），
  4×4×1 超胞（64 原子、16 个 TM 位点）；掺杂组分按最大余数法取整，实际实现组分写入输出。
- 能量/电压：CHGNet 代理（筛选口径，误差 0.1-0.3 V 量级）；周期 DFT 真背书缺工具（如实标注）。
- 去锂态：x_Li=0.3 随机去锂（种子由 formula 哈希决定，可复现）。
"""

import hashlib
import json

import numpy as np
from pymatgen.core import Composition, Lattice, Structure

_A, _C, _O_Z = 2.87, 14.19, 0.241  # NMC811 层状 R-3m 文献晶格参数
_SUPERCELL = (2, 2, 1)
_X_FULL, _X_DELITH = 1.0, 0.3  # 满锂 / 去锂态的 Li 占位
_F = 26801.481  # 法拉第常数折算：F/3.6 (mAh·mol⁻¹)

NMC_BASE_FORMULA = "Li(Ni0.8Mn0.1Co0.1)O2"


def _seed(formula: str) -> int:
    return int(hashlib.sha256(formula.encode("utf-8")).hexdigest()[:8], 16)


def _base_structure() -> Structure:
    """NMC811 层状 R-3m 原型 2×2×1 超胞（每六方晶胞 3 个化学式单元 = 12 原子；
    超胞 48 原子：12 Li / 12 TM / 24 O）。Wyckoff 位点：
    Li 3b (0,0,1/2)(1/3,2/3,5/6)(2/3,1/3,1/6)；TM 3a (0,0,0)(1/3,2/3,1/3)(2/3,1/3,2/3)；
    O 6c (0,0,±z)(1/3,2/3,1/3±z)(2/3,1/3,2/3±z)。"""
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
    """组分分数 → 整数计数（最大余数法，和恰为 n）。"""
    counts = {sym: int(f * n) for sym, f in fractions.items()}
    rest = n - sum(counts.values())
    order = sorted(fractions, key=lambda s: (fractions[s] * n - counts[s]), reverse=True)
    for i in range(rest):
        counts[order[i % len(order)]] += 1
    return counts


def build_doped_structure(formula: str) -> tuple[Structure, dict[str, int], list[int]]:
    """按组分在原型上替换 TM 位点 → (结构, 实现计数, TM 位点下标列表)。"""
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


def delithiate(struct: Structure, x_li: float, seed: int) -> tuple[Structure, int]:
    """随机去锂至 x_li 占位（种子可复现）→ (结构, 保留 Li 数)。"""
    li_sites = [i for i, site in enumerate(struct) if site.specie.symbol == "Li"]
    keep = int(round(x_li * len(li_sites)))
    rng = np.random.default_rng(seed)
    drop = rng.choice(li_sites, size=len(li_sites) - keep, replace=False)
    struct.remove_sites(drop)
    return struct, keep


def relax_energy(struct: Structure) -> tuple[float, bool]:
    """CHGNet 原生 StructOptimizer（FIRE）+ GPU 弛豫 → (能量 eV, 是否收敛)。"""
    from chgnet.model import CHGNet
    from chgnet.model.dynamics import AseAtomsAdaptor
    from chgnet.model.dynamics import FIRE
    from chgnet.model.dynamics import StructOptimizer

    atoms = AseAtomsAdaptor().get_atoms(struct)
    relaxer = StructOptimizer(model=CHGNet.load(), optimizer_class=FIRE)
    result = relaxer.relax(atoms, fmax=0.1, steps=300, relax_cell=True, verbose=False)
    traj = result.get("trajectory")
    # chgnet 0.4.x：TrajectoryObserver 对象（.trajectory 帧列表）或帧列表
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
    """超胞所含化学式单元数（按 Li 数定：满锂态 Li 数 = 12 → n_fu = 12/1）。"""
    return 12  # 2×2×1 超胞：12 个 Li


def average_voltage(e_full: float, e_delith: float, n_removed: int, e_li: float) -> float:
    """平均电压（vs Li 金属）：V = −[E(Li_x2) − E(Li_x1) − n_removed·E_Li] / n_removed。"""
    if n_removed <= 0:
        raise ValueError("n_removed must be positive")
    return -(e_full - e_delith - n_removed * e_li) / n_removed


def screen_candidate(formula: str, base_energy_fu: float | None, e_li: float) -> dict:
    """单个组分候选：满锂/去锂弛豫 → 相对稳定性 + 平均电压 + 容量代理。

    平均电压（vs Li 金属）：V = −[E(Li_x2MO2) − E(Li_x1MO2) − n_removed·E_Li] / n_removed
    （E_Li 为 CHGNet 的 bcc Li 金属参考能量，每轮基线计算一次）。
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
    """bcc Li 金属参考能量（每原子 eV，CHGNet 弛豫 2 原子胞）。"""
    from pymatgen.core import Lattice as _Lattice

    li = Structure(_Lattice.cubic(3.51), ["Li", "Li"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    e, _conv = relax_energy(li)
    return e / 2.0


def run_composition_screen(in_data: dict) -> dict:
    """IN: {"candidates": [{"formula": "...", "name": "..."}]} → OUT: 每候选 metrics + 基线。"""
    cands = in_data.get("candidates", [])
    if not cands:
        raise ValueError("input must contain a non-empty 'candidates' list")
    base_e_fu = None
    # 基线 NMC811 + bcc Li 金属参考能量
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
            "NMC811 基线自校准：文献平均电压 ≈3.8 V、理论容量 ≈194 mAh/g（x∈[0.3,1] 窗口）"
            "——若基线预测显著偏离，说明本批结果不可信（如实标注）。"
        ),
    }
