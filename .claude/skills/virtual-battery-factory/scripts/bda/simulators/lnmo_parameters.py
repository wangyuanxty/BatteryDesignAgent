"""LNMO（LiNi0.5Mn1.5O4，4.7 V 尖晶石）高电压正极参数集——材料瓶颈自识别验证用。

参数集来源（文献标定）：
- LNMO OCP 曲线（Markovsky et al. / Duncan et al. 4.7 V 平台）：
  富锂端 ~4.4 V → 4.7 V 主平台 → 贫锂端 ~4.85 V；x=0.5 中点 ≈ 4.7 V
- 理论比容量 147 mAh/g；密度 4.4 g/cm3；扩散系数 ~1e-12 m2/s（尖晶石离子导电）
- 其余（负极/电解液/隔膜/几何/热）从 Chen2020 继承——结构设计自由度不变

用法：run-pyamm --base <data/LNMO.json>（run_simulation 检测 base 为文件路径，
Chen2020 基底 + 本覆盖键；OCP 以 pybamm 符号函数绑定）。
"""
from __future__ import annotations

import pybamm


def lnmo_ocp(sto, c_e=1000.0):
    """LNMO 正极 OCP（V vs Li/Li+）——pybamm 符号表达式（求解器符号求值）。

    主平台 4.7 V + 两端平滑坡道（tanh）：x=0.5 中点 ≈ 4.7 V。
    sto ∈ [0,1]（1=贫锂态 4.9V，0=富锂态 4.4V）；stoich 范围由参数集 limits 保证。
    """
    return 4.7 + 0.13 * pybamm.tanh(12.0 * (sto - 0.92)) + 0.17 * pybamm.tanh(12.0 * (0.08 - sto))

