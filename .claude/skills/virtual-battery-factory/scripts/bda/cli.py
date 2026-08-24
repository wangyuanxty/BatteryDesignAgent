import argparse
import json
import os
import sys
from collections.abc import Callable
from pathlib import Path

from bda.store import CaseWorkspace, cache_get, cache_put

TRUE_COMPUTE_COMMANDS = {"run-orca", "run-qe", "run-cp2k", "run-md"}


def _load_json(path: str) -> dict:
    # utf-8-sig：兼容 PowerShell 5.1 Set-Content 写入的带 BOM 文件（实测踩坑）
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def _dump(out: str, data: dict) -> None:
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _workspace_for(out: str) -> CaseWorkspace:
    """Cache workspace root = directory of the --out file (spec 5.2 invariant 3:
    run-* commands consult the store cache before computing)."""
    return CaseWorkspace(".", str(Path(out).resolve().parent), create=False)


def _cached(ws: CaseWorkspace, key: dict, compute: Callable[[], dict]) -> dict:
    """cache_get -> short-circuit; else compute + cache_put."""
    hit = cache_get(ws, key)
    if hit is not None:
        return hit
    result = compute()
    cache_put(ws, key, result)
    return result


def _cmd_run_pyamm(args) -> int:
    from bda.simulators.pybamm_runner import run_simulation
    params = _load_json(args.params)
    key = {"cmd": "run-pyamm", "params": params, "protocol": args.protocol,
           "base": args.base, "mode": args.mode, "thermal": args.thermal,
           "plating": args.plating, "cycles": args.cycles}
    out = _cached(
        _workspace_for(args.out),
        key,
        lambda: run_simulation(params, protocol=args.protocol, base=args.base,
                               mode=args.mode, thermal=args.thermal, plating=args.plating,
                               cycles=args.cycles),
    )
    _dump(args.out, out)
    return 0


def _cmd_run_mlp(args) -> int:
    from bda.simulators.mlp_runner import relax_structure
    data = _load_json(args.in_file)
    ws = _workspace_for(args.out)
    out = []
    for c in data["candidates"]:
        smiles = c["smiles"]
        key = {"cmd": "run-mlp", "smiles": smiles, "model": args.model}
        r = _cached(ws, key, lambda: relax_structure(smiles, model=args.model))
        out.append({"smiles": smiles, "metrics": {"energy_ev": r["energy_ev"], "converged": r["converged"]},
                    "model": args.model})
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_run_xtb(args) -> int:
    from bda.simulators.xtb_runner import xtb_single_point
    data = _load_json(args.in_file)
    ws = _workspace_for(args.out)
    out = []
    for c in data["candidates"]:
        smiles = c["smiles"]
        key = {"cmd": "run-xtb", "smiles": smiles}
        r = _cached(ws, key, lambda: xtb_single_point(smiles))
        out.append({"smiles": smiles, "metrics": {"homo_ev": r["homo_ev"], "lumo_ev": r["lumo_ev"]}})
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_run_comp(args) -> int:
    from bda.simulators.comp_runner import run_composition_screen
    data = _load_json(args.in_file)
    ws = _workspace_for(args.out)
    key = {"cmd": "run-comp", "candidates": data["candidates"]}
    out = _cached(ws, key, lambda: run_composition_screen(data))
    _dump(args.out, out)
    return 0


def _cmd_run_qe(args) -> int:
    from bda.simulators.qe_runner import run_qe_endorsement
    data = _load_json(args.in_file)
    ws = _workspace_for(args.out)
    key = {"cmd": "run-qe", "candidates": data["candidates"]}
    out = _cached(ws, key, lambda: run_qe_endorsement(data))
    _dump(args.out, out)
    return 0


def _cmd_run_cp2k(args) -> int:
    from bda.simulators.cp2k_runner import run_cp2k_endorsement
    data = _load_json(args.in_file)
    ws = _workspace_for(args.out)
    key = {"cmd": "run-cp2k", "candidates": data["candidates"]}
    out = _cached(ws, key, lambda: run_cp2k_endorsement(data))
    _dump(args.out, out)
    return 0


def _cmd_run_orca(args) -> int:
    from bda.simulators.orca_runner import (DEFAULT_FUNCTIONAL, _multiplicity_for,
                                            orca_endorsement)
    data = _load_json(args.in_file)
    ws = _workspace_for(args.out)
    out = []
    for c in data["candidates"]:
        smiles = c["smiles"]
        key = {"cmd": "run-orca", "smiles": smiles, "charge": 0,
               "mult": _multiplicity_for(smiles, 0), "functional": DEFAULT_FUNCTIONAL}
        r = _cached(ws, key, lambda: orca_endorsement(smiles))
        out.append({"smiles": smiles, "endorsement": r})
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_run_md(args) -> int:
    from bda.simulators.md_runner import run_diffusion_md
    box = _load_json(args.box)
    key = {"cmd": "run-md", "box": box, "t_ns": args.t_ns, "engine": args.engine}
    out = _cached(
        _workspace_for(args.out),
        key,
        lambda: run_diffusion_md(box, engine=args.engine, t_ns=args.t_ns),
    )
    _dump(args.out, out)
    return 0


def _cmd_run_tr(args) -> int:
    from bda.simulators.thermal_runaway import cmd_run_thermal_runaway as run
    return run(args)


def _cmd_render(args) -> int:
    from bda.report import render_report
    render_report(args.case_dir, args.out)
    return 0


def _cmd_calc_energy(args) -> int:
    from bda.energy import cmd_calc_energy as run
    return run(args)


def _cmd_verify_deliverables(args) -> int:
    from bda.verify_deliverables import cmd_verify_deliverables as run
    return run(args)


def _cmd_log_evaluate(args) -> int:
    from bda.audit import cmd_log_evaluate as run
    return run(args)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bda", description="Virtual Battery Factory simulation library CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    p_pybamm = sub.add_parser("run-pyamm"); p_pybamm.add_argument("--params", required=True); p_pybamm.add_argument("--protocol", required=True); p_pybamm.add_argument("--base", default="Chen2020"); p_pybamm.add_argument("--mode", default="spme"); p_pybamm.add_argument("--thermal", default="lumped"); p_pybamm.add_argument("--plating", action="store_true"); p_pybamm.add_argument("--cycles", type=int, default=None); p_pybamm.add_argument("--out", required=True)
    p_mlp = sub.add_parser("run-mlp"); p_mlp.add_argument("--in", dest="in_file", required=True); p_mlp.add_argument("--model", default="mace"); p_mlp.add_argument("--out", required=True)
    p_xtb = sub.add_parser("run-xtb"); p_xtb.add_argument("--in", dest="in_file", required=True); p_xtb.add_argument("--out", required=True)
    p_orca = sub.add_parser("run-orca"); p_orca.add_argument("--in", dest="in_file", required=True); p_orca.add_argument("--out", required=True)
    p_comp = sub.add_parser("run-comp"); p_comp.add_argument("--in", dest="in_file", required=True); p_comp.add_argument("--out", required=True)
    p_qe = sub.add_parser("run-qe"); p_qe.add_argument("--in", dest="in_file", required=True); p_qe.add_argument("--out", required=True)
    p_cp2k = sub.add_parser("run-cp2k"); p_cp2k.add_argument("--in", dest="in_file", required=True); p_cp2k.add_argument("--out", required=True)
    p_md = sub.add_parser("run-md"); p_md.add_argument("--box", required=True); p_md.add_argument("--engine", default="gromacs"); p_md.add_argument("--t-ns", type=float, default=10.0); p_md.add_argument("--out", required=True)
    p_tr = sub.add_parser("run-tr")
    p_tr.add_argument("--sim", default="", help="过充/放电仿真输出 JSON：读取 T_max_K 作为热失控初始温度（过充→热失控自动耦合）")
    p_tr.add_argument("--mass-kg", type=float, default=None, help="电芯质量 kg（取 calc-energy 的 mass_kg——mcp = mass×900，针刺/热失控必传）")
    p_tr.add_argument("--t-init", type=float, default=298.15)
    p_tr.add_argument("--x0", type=float, default=1.0)
    p_tr.add_argument("--t-max", type=float, default=3600.0)
    p_tr.add_argument("--mcp", type=float, default=1000.0)
    p_tr.add_argument("--hA", type=float, default=0.05)
    p_tr.add_argument("--t-amb", type=float, default=298.15)
    p_tr.add_argument("--q-nail", type=float, default=0.0)
    p_tr.add_argument("--out", required=True)
    p_render = sub.add_parser("render"); p_render.add_argument("--case-dir", required=True); p_render.add_argument("--out", default="report.html")
    p_energy = sub.add_parser("calc-energy"); p_energy.add_argument("--params", default=""); p_energy.add_argument("--sim", required=True); p_energy.add_argument("--base", default="Chen2020"); p_energy.add_argument("--out", required=True)
    p_verify = sub.add_parser("verify-deliverables"); p_verify.add_argument("--case-dir", required=True)
    p_audit = sub.add_parser("log-evaluate")
    p_audit.add_argument("--case-dir", required=True)
    p_audit.add_argument("--round", type=int, required=True)
    p_audit.add_argument("--outputs", nargs="+", default=None, help="单候选模式：输出文件列表")
    p_audit.add_argument("--candidate", default="")
    p_audit.add_argument("--note", default="")
    p_audit.add_argument("--batch-file", default="", help="批量模式：JSON 文件 [{'candidate','outputs','note','round?'}]，每个候选落一条 evaluate")

    handlers = {"run-pyamm": _cmd_run_pyamm, "run-mlp": _cmd_run_mlp,
                "run-xtb": _cmd_run_xtb, "run-orca": _cmd_run_orca, "run-comp": _cmd_run_comp,
                "run-qe": _cmd_run_qe, "run-cp2k": _cmd_run_cp2k, "run-md": _cmd_run_md,
                "run-tr": _cmd_run_tr,
                "render": _cmd_render, "calc-energy": _cmd_calc_energy,
                "verify-deliverables": _cmd_verify_deliverables,
                "log-evaluate": _cmd_log_evaluate}
    args = parser.parse_args(argv)
    # C1 裸 LLM 对照模式（run.py --bare 设置）：真计算禁用（背书是协议流程的一部分，C1 无协议）
    if args.command in TRUE_COMPUTE_COMMANDS and os.environ.get("BDA_DISABLE_TRUE_COMPUTE"):
        print(f"bda error: 真计算已禁用（C1 对照模式）——{args.command} 不可用", file=sys.stderr)
        return 1
    try:
        return handlers[args.command](args)
    except (ValueError, RuntimeError) as e:
        print(f"bda error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
