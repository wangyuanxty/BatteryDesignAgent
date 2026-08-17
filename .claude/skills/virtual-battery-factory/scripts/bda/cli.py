import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path

from bda.store import CaseWorkspace, cache_get, cache_put


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
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


def _cmd_bridge(args) -> int:
    from bda.bridge import map_micro_to_pybamm
    props = _load_json(args.props)
    _dump(args.out, map_micro_to_pybamm(props))
    return 0


def _cmd_filter(args) -> int:
    from bda.funnel import apply_rules
    data = _load_json(args.in_file)
    rules = _load_json(args.rules)
    out = apply_rules(data["candidates"], rules)
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_consensus(args) -> int:
    from bda.funnel import check_consensus
    data = _load_json(args.in_file)
    out = check_consensus(data["candidates"])
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_run_pyamm(args) -> int:
    from bda.simulators.pybamm_runner import run_simulation
    params = _load_json(args.params)
    key = {"cmd": "run-pyamm", "params": params, "protocol": args.protocol,
           "base": args.base, "mode": args.mode, "thermal": args.thermal,
           "plating": args.plating}
    out = _cached(
        _workspace_for(args.out),
        key,
        lambda: run_simulation(params, protocol=args.protocol, base=args.base,
                               mode=args.mode, thermal=args.thermal, plating=args.plating),
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


def _cmd_run_orca(args) -> int:
    from bda.candidates import validate_smiles
    from bda.simulators.orca_runner import (DEFAULT_FUNCTIONAL, _multiplicity_for,
                                            orca_endorsement)
    data = _load_json(args.in_file)
    ws = _workspace_for(args.out)
    out = []
    for c in data["candidates"]:
        smiles = c["smiles"]
        if not validate_smiles(smiles):
            raise ValueError(f"invalid SMILES: {smiles!r}")
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


def _cmd_render(args) -> int:
    from bda.report import render_report
    render_report(args.case_dir, args.out)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bda", description="Virtual Battery Factory simulation library CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    p_bridge = sub.add_parser("bridge"); p_bridge.add_argument("--props", required=True); p_bridge.add_argument("--out", required=True)
    p_filter = sub.add_parser("filter"); p_filter.add_argument("--in", dest="in_file", required=True); p_filter.add_argument("--rules", required=True); p_filter.add_argument("--out", required=True)
    p_cons = sub.add_parser("consensus"); p_cons.add_argument("--in", dest="in_file", required=True); p_cons.add_argument("--out", required=True)
    p_pybamm = sub.add_parser("run-pyamm"); p_pybamm.add_argument("--params", required=True); p_pybamm.add_argument("--protocol", required=True); p_pybamm.add_argument("--base", default="Chen2020"); p_pybamm.add_argument("--mode", default="spme"); p_pybamm.add_argument("--thermal", default="lumped"); p_pybamm.add_argument("--plating", action="store_true"); p_pybamm.add_argument("--out", required=True)
    p_mlp = sub.add_parser("run-mlp"); p_mlp.add_argument("--in", dest="in_file", required=True); p_mlp.add_argument("--model", default="mace"); p_mlp.add_argument("--out", required=True)
    p_xtb = sub.add_parser("run-xtb"); p_xtb.add_argument("--in", dest="in_file", required=True); p_xtb.add_argument("--out", required=True)
    p_orca = sub.add_parser("run-orca"); p_orca.add_argument("--in", dest="in_file", required=True); p_orca.add_argument("--out", required=True)
    p_md = sub.add_parser("run-md"); p_md.add_argument("--box", required=True); p_md.add_argument("--engine", default="gromacs"); p_md.add_argument("--t-ns", type=float, default=10.0); p_md.add_argument("--out", required=True)
    p_render = sub.add_parser("render"); p_render.add_argument("--case-dir", required=True); p_render.add_argument("--out", default="report.html")

    handlers = {"bridge": _cmd_bridge, "filter": _cmd_filter, "consensus": _cmd_consensus,
                "run-pyamm": _cmd_run_pyamm, "run-mlp": _cmd_run_mlp, "run-xtb": _cmd_run_xtb,
                "run-orca": _cmd_run_orca, "run-md": _cmd_run_md, "render": _cmd_render}
    args = parser.parse_args(argv)
    try:
        return handlers[args.command](args)
    except (ValueError, RuntimeError) as e:
        print(f"bda error: {e}", file=sys.stderr)
        return 1
