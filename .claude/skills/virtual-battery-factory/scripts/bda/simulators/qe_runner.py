"""周期 DFT 真背书（run-qe）：组分 → QE vc-relax → 相对稳定性 + 平均电压（含 QE Li 金属参考）。

环境：pw.x（conda-forge q-e 包）+ SSSP efficiency 赝势（conda-forge sssp 包）。
口径：
- ecutwfc=50 Ry / ecutrho=400 Ry（SSSP efficiency 标准）；nspin=2（Ni/Mn/Co 磁性，铁磁初猜）；
- 满锂态 vc-relax（晶胞+离子）；去锂态固定弛豫后晶胞、仅离子 relax（节省成本，如实标注）；
- 电压公式与 run-comp 一致：V = −[E_full − E_delith − n_removed·E_Li]/n_removed。
- 运行时间：12 原子原胞 ~1 小时/态；48 原子超胞小时级（CPU 挂夜）。
"""

import os
import shutil
import subprocess
import time

from pymatgen.core import Lattice, Structure

# 赝势探测顺序：环境变量 > py312 conda 环境 sssp 目录
_PSEUDO_CANDIDATES = [
    os.environ.get("QE_PSEUDO_DIR"),
    r"D:\anaconda\envs\py312\share\sssp\efficiency",
    r"D:\anaconda\share\sssp\efficiency",
]

# SSSP efficiency 赝势文件名（本案例元素；缺失元素报错提示）
_PSEUDO_FILES = {
    "Li": "li_pbe_v1.4.uspp.F.UPF",
    "Ni": "ni_pbe_v1.4.uspp.F.UPF",
    "Mn": "mn_pbe_v1.5.uspp.F.UPF",
    "Co": "Co_pbe_v1.2.uspp.F.UPF",
    "O": "O.pbe-n-kjpaw_psl.0.1.UPF",
    "Si": "Si.pbe-n-rrkjus_psl.1.0.0.UPF",
    "Mg": "Mg.pbe-n-kjpaw_psl.0.3.0.UPF",
}

_MAGNETIC = {"Ni", "Mn", "Co"}  # 需要 nspin=2 与初始磁矩的元素


def pseudo_dir() -> str:
    for cand in _PSEUDO_CANDIDATES:
        if cand and os.path.isdir(cand):
            return cand
    raise RuntimeError(
        "QE pseudopotential dir not found; set QE_PSEUDO_DIR or install conda-forge 'sssp' package"
    )


def pw_bin() -> str:
    for name in ("pw.x", "pw.exe", "pw.x.exe"):  # MSYS2 包内为 pw.exe
        found = shutil.which(name)
        if found:
            return found
    for cand in (
        # MSYS2 原版 pw.exe 栈保留仅 2MB（计算初始化即栈溢出 0xC00000FD）；
        # pw_stack4g.exe = pefile 打过补丁的副本（栈保留 4GB），优先使用
        r"C:\msys64\ucrt64\bin\pw_stack4g.exe",
        r"C:\msys64\ucrt64\bin\pw.exe",  # MSYS2 mingw-w64-ucrt-x86_64-quantum-espresso
        r"C:\msys64\mingw64\bin\pw.x.exe",
        r"D:\anaconda\envs\py312\Library\bin\pw.x",
        r"D:\anaconda\Library\bin\pw.x",
    ):
        if os.path.isfile(cand):
            return cand
    raise RuntimeError(
        "pw.x not found; install MSYS2 quantum-espresso: "
        "winget install MSYS2.MSYS2 && pacman -S mingw-w64-ucrt-x86_64-quantum-espresso"
    )


def _magnetization(structure: Structure) -> dict[str, float]:
    """磁性元素初始磁矩（铁磁初猜，筛选口径）。"""
    return {el: 0.6 for el in {s.specie.symbol for s in structure} if el in _MAGNETIC}


def write_inputs(structure: Structure, workdir: str, prefix: str, relax_cell: bool) -> None:
    """pymatgen → pw.x 输入文件（vc-relax 或 relax）。"""
    from pymatgen.io.pwscf import PWInput

    pseudo = {}
    for el in {s.specie.symbol for s in structure}:
        if el not in _PSEUDO_FILES:
            raise ValueError(f"no SSSP efficiency pseudopotential entry for element {el}")
        pseudo[el] = _PSEUDO_FILES[el]
    mag = _magnetization(structure)
    control = {
        "calculation": "vc-relax" if relax_cell else "relax",
        "prefix": prefix,
        "pseudo_dir": pseudo_dir(),
        "outdir": os.path.join(workdir, "out"),
        "tstress": relax_cell,
        "tprnfor": True,
        "etot_conv_thr": 1.0e-4,
        "forc_conv_thr": 1.0e-3,
        "nstep": 60,
        "verbosity": "low",
    }
    system = {
        "ecutwfc": 50.0,
        "ecutrho": 400.0,
        "occupations": "smearing",
        "degauss": 0.02,
    }
    if mag:
        system["nspin"] = 2
        # QE 的 namelist 不支持 dict——统一标量初猜（全部元素 0.6，仅初始猜测）
        system["starting_magnetization"] = 0.6
    electrons = {"conv_thr": 1.0e-7, "mixing_beta": 0.3}
    pw = PWInput(structure, pseudo=pseudo, control=control, system=system, electrons=electrons)
    os.makedirs(workdir, exist_ok=True)
    in_path = os.path.join(workdir, f"{prefix}.in")
    pw.write_file(in_path)
    # Fortran namelist 里反斜杠是转义符：Windows 路径必须换成正斜杠（否则 pw.x 静默崩溃）
    text = open(in_path, encoding="utf-8").read().replace("\\", "/")
    open(in_path, "w", encoding="utf-8").write(text)


def parse_pw_output(text: str) -> tuple[float, bool]:
    """pw.x stdout → (总能量 eV, 收敛)。"""
    energies = [
        float(line.split()[-2])
        for line in text.splitlines()
        if line.strip().startswith("!")
    ]
    if not energies:
        raise RuntimeError("pw.x produced no total energy")
    converged = "convergence has been achieved" in text or "End final coordinates" in text
    return energies[-1] * 13.605703976, converged  # Ry → eV


def run_pw(workdir: str, prefix: str) -> tuple[float, bool, float]:
    """执行 pw.x → (总能量 eV, 收敛, 耗时秒)。"""
    t0 = time.time()
    in_file = os.path.join(workdir, f"{prefix}.in")
    out_file = os.path.join(workdir, f"{prefix}.out")
    env = dict(os.environ)
    # MSYS2 的 pw.exe 需要 ucrt64\bin 下的运行时 DLL（libgcc/libgfortran/MPI 等）
    env["PATH"] = os.path.dirname(pw_bin()) + os.pathsep + env.get("PATH", "")
    with open(out_file, "w", encoding="utf-8") as out:
        subprocess.run([pw_bin(), "-in", in_file], stdout=out, stderr=subprocess.STDOUT, check=False, env=env)
    wall = time.time() - t0
    text = open(out_file, encoding="utf-8", errors="replace").read()
    energy, converged = parse_pw_output(text)
    if not converged and "!" not in text:
        raise RuntimeError(f"pw.x produced no total energy for {prefix}; see {out_file}")
    return energy, converged, wall


def qe_endorsement(formula: str, delith_frac: float = 0.3) -> dict:
    """单个组分周期 DFT 背书：满锂 vc-relax + 去锂 relax + Li 金属参考 → 电压。"""
    import tempfile

    from bda.simulators.comp_runner import (
        _seed,
        average_voltage,
        build_doped_structure,
        delithiate,
    )

    workdir = tempfile.mkdtemp(prefix="bda_qe_")
    try:
        struct_full, counts, _ = build_doped_structure(formula)
        n_li_full = sum(1 for s in struct_full if s.specie.symbol == "Li")
        write_inputs(struct_full, workdir, "full", relax_cell=True)
        e_full, conv_full, t_full = run_pw(workdir, "full")
        struct_delith, n_li_delith = delithiate(struct_full, delith_frac, _seed(formula))
        write_inputs(struct_delith, workdir, "delith", relax_cell=False)
        e_delith, conv_delith, t_delith = run_pw(workdir, "delith")
        li = Structure(Lattice.cubic(3.51), ["Li", "Li"], [[0, 0, 0], [0.5, 0.5, 0.5]])
        write_inputs(li, workdir, "li", relax_cell=True)
        e_li_cell, conv_li, t_li = run_pw(workdir, "li")
        e_li = e_li_cell / 2.0
        n_removed = n_li_full - n_li_delith
        voltage = average_voltage(e_full, e_delith, n_removed, e_li)
        return {
            "formula": formula,
            "realized_tm_counts": counts,
            "avg_voltage_v": float(voltage),
            "e_full_ev": e_full,
            "e_delith_ev": e_delith,
            "e_li_metal_ev": e_li,
            "converged": bool(conv_full and conv_delith and conv_li),
            "wall_time_s": t_full + t_delith + t_li,
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def run_qe_endorsement(in_data: dict) -> dict:
    """IN: {"candidates": [{"formula", "name"}]} → OUT: 每候选周期 DFT 背书（含 NMC811 基线）。"""
    cands = in_data.get("candidates", [])
    if not cands:
        raise ValueError("input must contain a non-empty 'candidates' list")
    results = []
    for c in cands:
        formula = str(c.get("formula") or "")
        name = str(c.get("name") or formula)
        try:
            m = qe_endorsement(formula)
            m["name"] = name
            results.append(m)
        except (ValueError, RuntimeError) as exc:
            results.append({"name": name, "formula": formula, "error": str(exc)})
    return {"candidates": results}
