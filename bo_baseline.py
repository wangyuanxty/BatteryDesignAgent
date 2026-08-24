"""bo_baseline.py：C2 BO 基线——Ax 贝叶斯优化在结构参数空间搜索。

复刻 Battery-Sim-Agent (KDD 2026) 的 BO 配置：Sobol 初始化 → GPEI(SingleTaskGP, Matern)
+ LogNEI，warmup = 2×d，seed 1234。评估器与 agent 协议模式同源（同 run-pyamm / calc-energy），
目标 = 能量密度 − 安全惩罚（T_max 超限 / 析锂）。

用法：
    python bo_baseline.py --budget 50 --base ORegan2022 --workspace runs/exp/c2_t1_r1
    python bo_baseline.py --budget 5 --smoke        # 冒烟：快速验证链路
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

from bda.energy import calc_energy
from bda.simulators.pybamm_runner import run_simulation

# ---- T1 结构参数空间（Ax 参数名 → PyBaMM 参数名 + 缩放因子）----
# 厚度类用 µm 缩放（Ax 对极小范围数值敏感——实测报数值错误），评估时转回 m
PARAM_SPACE = {
    "pos_thickness": {"bounds": [50, 100], "scale": 1e-6, "pybamm": "Positive electrode thickness [m]"},
    "neg_thickness": {"bounds": [60, 150], "scale": 1e-6, "pybamm": "Negative electrode thickness [m]"},
    "pos_porosity": {"bounds": [0.20, 0.45], "scale": 1.0, "pybamm": "Positive electrode porosity"},
    "neg_porosity": {"bounds": [0.20, 0.45], "scale": 1.0, "pybamm": "Negative electrode porosity"},
    "sep_thickness": {"bounds": [8, 20], "scale": 1e-6, "pybamm": "Separator thickness [m]"},
    "sep_porosity": {"bounds": [0.30, 0.60], "scale": 1.0, "pybamm": "Separator porosity"},
    "pos_cc": {"bounds": [8, 20], "scale": 1e-6, "pybamm": "Positive current collector thickness [m]"},
    "neg_cc": {"bounds": [8, 20], "scale": 1e-6, "pybamm": "Negative current collector thickness [m]"},
    "h_heat": {"bounds": [10.0, 100.0], "scale": 1.0, "pybamm": "Total heat transfer coefficient [W.m-2.K-1]"},
    "neg_rp": {"bounds": [2.0, 6.0], "scale": 1e-6, "pybamm": "Negative particle radius [m]"},
}

T_MAX_LIMIT_K = 333.15
PLATED_PENALTY = 50.0      # 析锂一次性惩罚（Wh/kg）
TMAX_PENALTY_PER_K = 5.0   # 每超温 1K 惩罚（Wh/kg）


class BOSearch:
    """C2 BO 搜索：评估器 = 与 agent 协议模式同源的仿真 + 合同口径能量密度。"""

    def __init__(self, base: str, workspace: Path):
        self.base = base
        self.workspace = workspace
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory()

    def evaluate(self, params: dict, trial_id: int) -> dict:
        """评估一组结构参数：返回 {objective, energy_density, t_max, plated}。"""
        override = {spec["pybamm"]: params[name] * spec["scale"] for name, spec in PARAM_SPACE.items()}
        params_path = Path(self.tmp.name) / f"p{trial_id}.json"
        params_path.write_text(json.dumps(override), encoding="utf-8")

        # 1C 放电 → 合同口径能量密度
        sim1c = run_simulation(override, protocol="1C_discharge", base=self.base, mode="spme")
        sim_path = Path(self.tmp.name) / f"s{trial_id}.json"
        sim_path.write_text(json.dumps({k: sim1c[k] for k in ("time_s", "voltage_v", "capacity_ah")}), encoding="utf-8")
        ed = calc_energy(str(params_path), str(sim_path), self.base)["energy_density_wh_kg"]

        # 4C 快充 → 安全（热 + 析锂）
        sim4c = run_simulation(
            override, protocol="4C_charge_45C", base=self.base, mode="spme", thermal="lumped", plating=True
        )
        t_max = sim4c["T_max_K"]
        plated = bool(min(sim4c["anode_potential_v"]) < 0.0)

        penalty = 0.0
        if t_max > T_MAX_LIMIT_K:
            penalty += (t_max - T_MAX_LIMIT_K) * TMAX_PENALTY_PER_K
        if plated:
            penalty += PLATED_PENALTY
        objective = ed - penalty
        return {
            "trial": trial_id,
            "objective": round(objective, 4),
            "energy_density_wh_kg": round(ed, 4),
            "T_max_K": round(t_max, 4),
            "plated": plated,
            "params": params,
        }


def run_bo(search: BOSearch, budget: int, seed: int = 1234, smoke: bool = False) -> list[dict]:
    # Ax 1.1.0：AxClient 默认生成策略即 Sobol 初始化 + BoTorch BO（Sobol+BoTorch），
    # 与 Battery-Sim-Agent 同库同策略族；随机种子固定保证可复现
    from ax.service.ax_client import AxClient
    from ax.service.utils.instantiation import ObjectiveProperties

    client = AxClient(random_seed=seed)
    client.create_experiment(
        name="c2_bo",
        parameters=[
            {"name": name, "type": "range", "bounds": list(spec["bounds"]), "value_type": "float"}
            for name, spec in PARAM_SPACE.items()
        ],
        objectives={"objective": ObjectiveProperties(minimize=False)},
    )
    trajectory: list[dict] = []
    for trial in range(budget):
        trial_params, _ = client.get_next_trial()
        result = search.evaluate(trial_params, trial)
        client.complete_trial(trial_index=trial, raw_data=result["objective"])
        trajectory.append(result)
        print(f"trial {trial + 1}/{budget}: objective={result['objective']} "
              f"ED={result['energy_density_wh_kg']} T_max={result['T_max_K']} plated={result['plated']}",
              flush=True)
    return trajectory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bo_baseline.py", description="C2 BO 基线（Ax，复刻 Battery-Sim-Agent 配置）")
    parser.add_argument("--budget", type=int, default=50, help="总评估次数（仿真预算）")
    parser.add_argument("--base", default="ORegan2022", help="PyBaMM 参数集（T1 基线体系）")
    parser.add_argument("--workspace", required=True, help="工作区（轨迹输出目录）")
    parser.add_argument("--seed", type=int, default=1234, help="随机种子（Battery-Sim-Agent 同款 1234）")
    parser.add_argument("--smoke", action="store_true", help="冒烟：budget=5 快速验证链路")
    args = parser.parse_args(argv)
    budget = 5 if args.smoke else args.budget
    ws = Path(args.workspace)
    search = BOSearch(args.base, ws)
    try:
        trajectory = run_bo(search, budget, args.seed, args.smoke)
    except Exception as e:
        print(f"bo error: {e}", file=sys.stderr)
        return 1
    out = ws / "bo_trajectory.json"
    out.write_text(json.dumps(trajectory, ensure_ascii=False, indent=2), encoding="utf-8")
    best = max(trajectory, key=lambda t: t["objective"])
    print(f"BO 完成：{len(trajectory)} 次评估，最优 objective={best['objective']} "
          f"(ED {best['energy_density_wh_kg']} Wh/kg, T_max {best['T_max_K']} K, plated={best['plated']})")
    print(f"轨迹已存：{out}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
