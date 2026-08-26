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

    def __init__(self, base: str, workspace: Path, task: str = "t1", tmax_limit: float = 333.15):
        self.base = base
        self.workspace = workspace
        self.task = task
        self.tmax_limit = tmax_limit
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory()

    def evaluate(self, params: dict, trial_id: int) -> dict:
        """评估一组结构参数：返回 {objective, energy_density, t_max, plated, ...}。

        task = t1（ED + 4C 安全惩罚）；task = t2（ED + 4C + SEI 100圈 ≤500nm + -20℃ 保持率 ≥90% 惩罚）。
        老化/低温仅 t2 执行（需带 SEI 参数集作为 base——Chen2020/OKane2022；ORegan2022 会 bda error（无老化模型））。
        """
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

        penalties = {}
        if t_max > self.tmax_limit:
            penalties["tmax"] = (t_max - self.tmax_limit) * TMAX_PENALTY_PER_K
        if plated:
            penalties["plated"] = PLATED_PENALTY

        sei_nm = None
        lowt_ret = None
        ret5 = None
        if self.task in ("t2", "t6", "t7"):
            # 老化（100 圈 SEI ≤ 500 nm；t6 同；t7 为 45℃ ≤550 nm）——带 SEI 参数集必须
            try:
                protocol = "aging_1C_100cyc_45C" if self.task == "t7" else "aging_1C_100cyc"
                aging = run_simulation(override, protocol=protocol, base=self.base, mode="spme")
                sei_nm = aging["sei_thickness_nm_end"]
                limit = 550.0 if self.task == "t7" else 500.0
                if sei_nm > limit:
                    penalties["sei"] = (sei_nm - limit) * 0.2
            except Exception:
                penalties["sei"] = PLATED_PENALTY
        if self.task in ("t2", "t4"):
            # 低温（-20℃ 1C 保持率 ≥ 90%（t2）/ ≥95%（t4））
            try:
                lowT = run_simulation(override, protocol="lowT_discharge", base=self.base, mode="spme")
                cap_25c = sim1c["capacity_ah"]
                lowt_ret = lowT["capacity_ah"] / cap_25c * 100.0
                limit = 95.0 if self.task == "t4" else 90.0
                if lowt_ret < limit:
                    penalties["lowt"] = (limit - lowt_ret) * 0.5
            except Exception:
                penalties["lowt"] = PLATED_PENALTY
        # ---- 任务特定指标（在 calc_energy 结果上）----
        import numpy as np
        full = calc_energy(str(params_path), str(sim_path), self.base)
        whl = full["energy_density_wh_l"]
        mass_g = full["mass_kg"] * 1000.0
        power = full["power_density_w_kg"]
        mid_v = full["midpoint_voltage_v"]
        cap_ah = full["capacity_ah"]

        if self.task == "t3":
            # 5C 保持率 ≥95%（DFN——SPMe 5C 不可靠实际为 spme 近似——如实标注；采用 spme 一致性口径）
            try:
                sim5c = run_simulation(override, protocol="5C_discharge", base=self.base, mode="spme")
                ret5 = sim5c["capacity_ah"] / cap_ah * 100.0 if cap_ah else 0.0
                if ret5 < 95.0:
                    penalties["5c"] = (95.0 - ret5) * 2.0
            except Exception:
                penalties["5c"] = PLATED_PENALTY
            if cap_ah < 2.0:
                penalties["cap"] = (2.0 - cap_ah) * 30.0
            if power < 4000.0:
                penalties["power"] = (4000.0 - power) * 0.01
        if self.task == "t4":
            if whl < 880.0:
                penalties["whl"] = (880.0 - whl) * 0.5
        if self.task == "t5":
            pass  # ED + 4C 安全（T_max/plated 已含）
        if self.task == "t6":
            # 体积 ED ≥950 + 电压平台 ≥4.1（BO 用 Chen2020 平台 3.6 级→恒罚——正是能力边界展示）
            if whl < 950.0:
                penalties["whl"] = (950.0 - whl) * 0.5
            if mid_v < 4.1:
                penalties["plateau"] = (4.1 - mid_v) * 100.0
        if self.task == "t7":
            # 针刺 10W 不热失控（自研 run-tr——BO 通过结构无法改变 TR 体积焓——边界展示）
            try:
                tr_out = run_thermal_runaway(t_init_k=t_max, q_nail_w=10.0, mass_kg=mass_g / 1000.0,
                                             hA_w_k=float(params["h_heat"]) * 0.00531)
                if tr_out["triggered"]:
                    penalties["tr"] = PLATED_PENALTY
            except Exception:
                penalties["tr"] = PLATED_PENALTY
        if self.task == "t8":
            # 5C ≥90% + 质量 ≤40g
            try:
                sim5c = run_simulation(override, protocol="5C_discharge", base=self.base, mode="spme")
                ret5 = sim5c["capacity_ah"] / cap_ah * 100.0 if cap_ah else 0.0
                if ret5 < 90.0:
                    penalties["5c"] = (90.0 - ret5) * 2.0
            except Exception:
                penalties["5c"] = PLATED_PENALTY
            if mass_g > 40.0:
                penalties["mass"] = (mass_g - 40.0) * 5.0

        penalty = sum(penalties.values())
        objective = ed - penalty
        result = {
            "trial": trial_id,
            "objective": round(objective, 4),
            "energy_density_wh_kg": round(ed, 4),
            "T_max_K": round(t_max, 4),
            "plated": plated,
            "energy_density_wh_l": round(whl, 2),
            "mass_g": round(mass_g, 2),
            "power_density_w_kg": round(power, 1),
            "midpoint_voltage_v": round(mid_v, 4),
            "params": params,
        }
        if sei_nm is not None:
            result["sei_thickness_nm_end"] = round(sei_nm, 1)
        if lowt_ret is not None:
            result["lowt_retention_pct"] = round(lowt_ret, 2)
        if ret5 is not None:
            result["ret5_pct"] = round(ret5, 2)
        return result


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
    parser.add_argument("--task", default="t1", choices=["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"],
                        help="任务选择：T1/T5 ED+4C安全 / T2/T6/T7 含SEI / T3/T8 含5C / T4 低温+Wh/L / T6 平台 4.1V / T7 针刺")
    parser.add_argument("--tmax-limit", type=float, default=333.15,
                        help="T_max 惩罚上限 K（对齐版：T6 用 323.15 = 50 °C 红线）")
    args = parser.parse_args(argv)
    budget = 5 if args.smoke else args.budget
    ws = Path(args.workspace)
    search = BOSearch(args.base, ws, task=args.task, tmax_limit=args.tmax_limit)
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
