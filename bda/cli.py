import argparse
import json
import sys


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _dump(out: str, data: dict) -> None:
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _cmd_bridge(args) -> int:
    from bda.bridge.mapper import map_micro_to_pybamm
    props = _load_json(args.props)
    _dump(args.out, map_micro_to_pybamm(props))
    return 0


def _cmd_filter(args) -> int:
    from bda.funnel.filter import apply_rules
    data = _load_json(args.in_file)
    rules = _load_json(args.rules)
    out = apply_rules(data["candidates"], rules)
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_consensus(args) -> int:
    from bda.funnel.consistency import check_consensus
    data = _load_json(args.in_file)
    out = check_consensus(data["candidates"])
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_run_pyamm(args) -> int:
    from bda.simulators.pybamm_runner import run_simulation
    params = _load_json(args.params)
    out = run_simulation(params, protocol=args.protocol, mode=args.mode,
                         thermal=args.thermal, plating=args.plating)
    _dump(args.out, out)
    return 0


def _cmd_run_mlp(args) -> int:
    from bda.simulators.mlp_runner import relax_structure
    data = _load_json(args.in_file)
    out = []
    for c in data["candidates"]:
        r = relax_structure(c["smiles"], model=args.model)
        out.append({"smiles": c["smiles"], "metrics": {"energy_ev": r["energy_ev"], "converged": r["converged"]},
                    "model": args.model})
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_run_xtb(args) -> int:
    from bda.simulators.xtb_runner import xtb_single_point
    data = _load_json(args.in_file)
    out = []
    for c in data["candidates"]:
        r = xtb_single_point(c["smiles"])
        out.append({"smiles": c["smiles"], "metrics": {"homo_ev": r["homo_ev"], "lumo_ev": r["lumo_ev"]}})
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_run_orca(args) -> int:
    from bda.simulators.orca_runner import orca_endorsement
    data = _load_json(args.in_file)
    out = []
    for c in data["candidates"]:
        r = orca_endorsement(c["smiles"])
        out.append({"smiles": c["smiles"], "endorsement": r})
    _dump(args.out, {"candidates": out})
    return 0


def _cmd_run_md(args) -> int:
    from bda.simulators.md_runner import run_diffusion_md
    box = _load_json(args.box)
    _dump(args.out, run_diffusion_md(box, t_ns=args.t_ns))
    return 0


def _cmd_render(args) -> int:
    from bda.report.render import render_report
    render_report(args.case_dir, args.out)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bda", description="Virtual Battery Factory simulation library CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    p_bridge = sub.add_parser("bridge"); p_bridge.add_argument("--props", required=True); p_bridge.add_argument("--out", required=True)
    p_filter = sub.add_parser("filter"); p_filter.add_argument("--in", dest="in_file", required=True); p_filter.add_argument("--rules", required=True); p_filter.add_argument("--out", required=True)
    p_cons = sub.add_parser("consensus"); p_cons.add_argument("--in", dest="in_file", required=True); p_cons.add_argument("--out", required=True)
    p_pybamm = sub.add_parser("run-pyamm"); p_pybamm.add_argument("--params", required=True); p_pybamm.add_argument("--protocol", required=True); p_pybamm.add_argument("--mode", default="spme"); p_pybamm.add_argument("--thermal", default="lumped"); p_pybamm.add_argument("--plating", action="store_true"); p_pybamm.add_argument("--out", required=True)
    p_mlp = sub.add_parser("run-mlp"); p_mlp.add_argument("--in", dest="in_file", required=True); p_mlp.add_argument("--model", default="mace"); p_mlp.add_argument("--out", required=True)
    p_xtb = sub.add_parser("run-xtb"); p_xtb.add_argument("--in", dest="in_file", required=True); p_xtb.add_argument("--out", required=True)
    p_orca = sub.add_parser("run-orca"); p_orca.add_argument("--in", dest="in_file", required=True); p_orca.add_argument("--out", required=True)
    p_md = sub.add_parser("run-md"); p_md.add_argument("--box", required=True); p_md.add_argument("--t-ns", type=float, default=10.0); p_md.add_argument("--out", required=True)
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
