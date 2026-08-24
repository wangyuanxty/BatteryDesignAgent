"""热失控子模型：三副反应放热（SEI 分解 / 负极-电解液 / 正极-电解液）+ 牛顿冷却。

实现口径（论文方法节可复现）：
- 零维集总热平衡：m·Cp·dT/dt = Σ(Q_i·r_i) − hA(T − T_amb) + Q_nail
- 三副反应动力学（Kim et al. 2019 / Coman et al. 2016 标准 Arrhenius 形式）：
  R1 SEI 分解：          r1 = A1·exp(−E1/RT)·x          （x = SEI 覆盖度，初始 1）
  R2 负极-电解液反应：   r2 = A2·exp(−E2/RT)·exp(−a/x)  （x→0 时 SEI 保护失效，反应爆发）
  R3 正极-电解液反应：   r3 = A3·exp(−E3/RT)·(1−y)·z    （y = 正极分解度；z 为电解液可用度）
- 副反应消耗：dx/dt = −r1；dy/dt = r3·y 的简化（保持双状态 x/y）
- 刚性 ODE → scipy solve_ivp(method="BDF", rtol=1e-8, atol=1e-10)
- 触发判定：dT/dt > 1 K/s（温升拐点）或 T ≥ 573 K（300℃ 工程红线）
- 针刺：Q_nail = I_sc²·R_short（局部短路产热），作为常热源项注入
- 过充耦合：run-pyamm overcharge 协议的 T_max_K 作为初始温度喂入

参数（Kim et al. 2019 锂离子电芯热失控标定值，J/kg 基）：
  R1: A=1.667e15 s⁻¹  Ea=1.3508e5 J/mol  ΔH=2.57e5 J/kg
  R2: A=2.5e13 s⁻¹    Ea=1.3508e5 J/mol  ΔH=1.714e6 J/kg
  R3: A=1.75e14 s⁻¹   Ea=1.65e5 J/mol   ΔH=1.13e5 J/kg
  覆盖度因子 a = 0.05（R2 对 SEI 残量敏感度）
  电芯热容 m·Cp 与散热 hA 由调用方传入（默认 1 kg·Cp≈1000 J/K，hA=0.05 W/K 绝热近似）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

# ---- 三副反应参数（文献标定值，J/kg 基；m = 活性材料质量 kg）----
R1 = {"A": 1.667e15, "Ea": 1.3508e5, "dH": 2.57e5}
R2 = {"A": 2.5e13, "Ea": 1.3508e5, "dH": 1.714e6}
R3 = {"A": 1.75e14, "Ea": 1.65e5, "dH": 1.13e5}
COVERAGE_FACTOR = 0.05  # 保留（历史参数名）；R2 覆盖因子现用 (1-x) 形式
R_GAS = 8.314
# 活性材料质量占整芯比：dH 为活性材料基（J/kg），整芯热容 mcp 含惰性组分
# （集流体/隔膜/壳体），能量释放到整芯需按此比例折算——否则 ΔT 高估 ~3 倍。
ACTIVE_MASS_FRAC = 0.3

# 触发判定
TRIGGER_DTDT = 1.0   # K/s：温升拐点
TRIGGER_T_K = 573.0  # 300 ℃ 工程红线


def _rhs(t: float, y: np.ndarray, mcp: float, hA: float, t_amb: float, q_nail: float) -> np.ndarray:
    """y = [T_K, x_sei, y_cath, u_anode]；返回 [dT/dt, dx/dt, dy/dt, du/dt]。

    反应物耗尽保证能量守恒（温度有界）：
    - x（SEI 量）被 R1 消耗；- R3 以 (1-y) 饱和（y→1 停止）；
    - u（负极可燃物）被 R2 消耗——此前版本缺此耗尽项导致温度数值爆炸（10^15 K）。
    """
    t_k, x, yc, u = y
    # 状态 clamp：x/y/u ∈ [0,1]（求解器数值越界防护，物理量域）
    x = min(max(x, 0.0), 1.0)
    yc = min(max(yc, 0.0), 1.0)
    u = min(max(u, 0.0), 1.0)
    inv_rt = 1.0 / (R_GAS * t_k)
    # 速率 clamp（物质输运限制）：Arrhenius 频率因子在高温下无物理上限（10^15 s⁻¹），
    # 不设上限会使瞬时功率无限大、能量不守恒（T_max 爆炸到 10^8 K 量级）。
    # 反应物转化率受输运限制，工程上取 100 s⁻¹ 上限（对应 ms 级耗尽，能量守恒封顶）。
    RATE_CAP = 1e2
    # 注意：x 不设 floor——x=0 时 r1 必须真为 0（SEI 耗尽即止）。
    # 此前 max(x, 1e-12) 使高温下 r1 = A1·exp·1e-12 ≈ 1.6e3 > cap → R1 满功率永燃（T 爆表）。
    r1 = min(R1["A"] * np.exp(-R1["Ea"] * inv_rt) * x, RATE_CAP)
    # R2 覆盖因子 = (1-x)：SEI 完整（x=1）时负极-电解液反应被抑制（factor=0），
    # SEI 分解（x→0）后爆发（factor→1）；受 u（负极可燃物）消耗限制，能量有界。
    r2 = min(R2["A"] * np.exp(-R2["Ea"] * inv_rt) * (1.0 - x) * u, RATE_CAP)
    r3 = min(R3["A"] * np.exp(-R3["Ea"] * inv_rt) * (1.0 - yc), RATE_CAP)
    q_gen = (R1["dH"] * r1 + R2["dH"] * r2 + R3["dH"] * r3) * ACTIVE_MASS_FRAC
    dtdt = (q_gen - hA * (t_k - t_amb) + q_nail) / mcp
    # 反应物一次消耗（∫r dt = 反应物消耗量 = 1，能量守恒）：
    # 二次形式（-r2·u）使 u 渐近趋 0 永不达，∫r dt 对数发散 → 能量超额（T_max 爆炸）。
    dxdt = -r1
    dydt = r3  # r3 已含 (1-yc) 饱和因子
    dudt = -r2  # r2 已含 u 反应物因子
    return np.asarray([dtdt, dxdt, dydt, dudt])


def run_thermal_runaway(
    t_init_k: float = 298.15,
    x_sei_init: float = 1.0,
    t_max_s: float = 3600.0,
    mcp_j_k: float = 1000.0,
    hA_w_k: float = 0.05,
    t_amb_k: float = 298.15,
    q_nail_w: float = 0.0,
    mass_kg: float | None = None,
) -> dict:
    """积分热失控 ODE。返回温度曲线与触发判定。

    注意：dH 为 J/kg（活性材料质量基）。本实现将三副反应放热按
    dH·r_i（r_i 为 s⁻¹ 量级速率）累加并以 mcp 归一——当 mcp 取整芯热容
    （约 1 kg × 1000 J/kg/K）时，dH 需理解为"整芯等效放热焓"（J）。
    为保持文献量级，调用方应传入 mcp ≈ 电芯质量 × 比热，并知悉
    该简化下触发温度边界与文献一致（sanity 测试验证）。
    **mass_kg 优先**：提供时 mcp = mass_kg × 900（电芯比热近似 J/kg/K），
    覆盖 mcp 参数——针刺/热失控必须传电芯实际质量（从 calc-energy mass_kg 机械取），
    否则 mcp 默认为 1000（≈1 kg 基准电芯）导致小电芯 dT/dt 被系统性低估。
    """
    if mass_kg is not None:
        mcp_j_k = mass_kg * 900.0
    y0 = np.asarray([t_init_k, x_sei_init, 0.0, 1.0])
    sol = solve_ivp(
        _rhs,
        (0.0, t_max_s),
        y0,
        method="BDF",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.2,  # 反应耗尽发生在 ms~0.1s 量级，步长上限必须小于该量级
        args=(mcp_j_k, hA_w_k, t_amb_k, q_nail_w),
        dense_output=True,
    )
    t_grid = np.linspace(0.0, t_max_s, 2001)
    y_grid = sol.sol(t_grid)
    t_k = y_grid[0]
    dtdt = np.gradient(t_k, t_grid)
    trigger_idx = int(np.argmax(dtdt > TRIGGER_DTDT)) if np.any(dtdt > TRIGGER_DTDT) else -1
    if trigger_idx < 0 and np.any(t_k >= TRIGGER_T_K):
        trigger_idx = int(np.argmax(t_k >= TRIGGER_T_K))
    triggered = trigger_idx >= 0
    return {
        "triggered": bool(triggered),
        "trigger_time_s": float(t_grid[trigger_idx]) if triggered else None,
        "T_max_K": float(t_k.max()),
        "T_final_K": float(t_k[-1]),
        "dTdt_max_K_s": float(dtdt.max()),
        "T_series_K": [round(float(v), 2) for v in t_k[::20]],
        "t_series_s": [round(float(v), 2) for v in t_grid[::20]],
        "params": {
            "t_init_K": t_init_k,
            "mcp_J_K": mcp_j_k,
            "hA_W_K": hA_w_k,
            "t_amb_K": t_amb_k,
            "q_nail_W": q_nail_w,
            "source": "Kim et al. 2019 / Coman et al. 2016 Arrhenius 三副反应，零维集总热平衡",
        },
    }


def cmd_run_thermal_runaway(args) -> int:
    try:
        t_init_k = args.t_init
        if args.sim:
            # 过充/放电仿真输出耦合：读取其 T_max_K 作为热失控初始温度（自动串联）
            sim = json.loads(Path(args.sim).read_text(encoding="utf-8-sig"))
            if "T_max_K" not in sim:
                raise ValueError(f"--sim 文件缺少 T_max_K 键（应传 run-pyamm 输出）: {args.sim}")
            t_init_k = float(sim["T_max_K"])
        out = run_thermal_runaway(
            t_init_k=t_init_k,
            x_sei_init=args.x0,
            t_max_s=args.t_max,
            mcp_j_k=args.mcp,
            hA_w_k=args.hA,
            t_amb_k=args.t_amb,
            q_nail_w=args.q_nail,
            mass_kg=getattr(args, "mass_kg", None),
        )
    except (ValueError, RuntimeError) as e:
        print(f"bda error: {e}", file=sys.stderr)
        return 1
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0
