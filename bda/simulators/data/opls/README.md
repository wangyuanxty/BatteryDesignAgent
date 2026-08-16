# OPLS-AA 拓扑模板目录（bda/simulators/data/opls/）

`bda/simulators/md_runner.py` 的确定性盒子构建器 `_build_box` 会把本目录下所需的
`.itp` 模板复制到运行工作目录并在 `topol.top` 中 `#include`。

> **本目录不随代码附带 `.itp` 文件**（需人工生成一次：LigParGen 是交互式网页、
> ilff 参数需手工整理）。行为约定：
>
> - 未装 GROMACS：slow 测试在 `shutil.which("gmx")` 检查处即跳过，完全不受影响；
> - 已装 GROMACS 但缺模板：`_build_box` 以 `RuntimeError` 快速失败并指向本说明；
> - 模板齐全：`_build_box` 将 .itp 复制进运行目录并正确 include。

## 代码期望的文件名与 moleculetype 名

| 组分  | 期望文件   | 期望 `[moleculetype]` 名 | 生成工具  |
|-------|-----------|--------------------------|-----------|
| EC    | `ec.itp`  | `EC`                     | LigParGen |
| EMC   | `emc.itp` | `EMC`                    | LigParGen |
| PF6⁻  | `pf6.itp` | `PF6`                    | ilff 仓库 |
| Li⁺   | `li.itp`  | `Li`                     | ilff 仓库 |

`_build_box` 写出的 `[molecules]` 段使用上表的名称（`EC`/`EMC`/`PF6`/`Li`），
生成后请核对 .itp 内 `[moleculetype]` 名称一致（不一致时手工改名即可）。

## EC / EMC：LigParGen 生成步骤

1. 打开 <https://zarbi.chem.yale.edu/ligpargen/>（交互式表单，无 API，勿尝试脚本化）。
2. 分别提交 SMILES：
   - EC：`C1COC(=O)O1`
   - EMC：`CCOC(=O)OC`
3. 电荷模型选 **1.14*CM1A-LBCC**（OPLS-AA 推荐默认）；输出格式选 **GROMACS**。
4. 下载产物（`.itp` 与可选 `.prm`/`.gro`）。
5. **使用 standalone 形式**的 .itp（内嵌 `[atomtypes]` 与 `[nonbond_params]`）：
   `topol.top` 只 include 本目录的四个 .itp，不再 include `oplsaa.ff/forcefield.itp`。
   若 LigParGen 给的 .itp 顶部有 `#include "oplsaa.ff/..."`，请改为合并参数成独立
   .itp，或自行在运行目录旁放置该力场目录。
6. `[moleculetype]` 名改为 `EC` / `EMC`，文件存为本目录 `ec.itp` / `emc.itp`。

## PF6 / Li：ilff 仓库参数

1. 克隆 <https://github.com/agiliopadua/ilff>。
2. 在仓库内定位 PF6 与 Li⁺ 的参数（ilff 以 `.zmat`/`.ff` 文本组织，参见其 README；
   如仅提供 DL_POLY/LAMMPS 格式，按仓库说明转换，或从 IL/CL&P 文献附表整理）。
3. 整理成独立 GROMACS `.itp`（内嵌 atomtypes/nonbond_params 与 `[moleculetype]`），
   moleculetype 名分别为 `PF6` 与 `Li`，存为 `pf6.itp` / `li.itp`。

## 0.8 电荷标定说明

OPLS-AA 与 ilff 混合体系的通行做法是把离子与溶剂的部分电荷统一缩放（模拟极化
效应、避免静电过强导致扩散偏慢或异常聚集）：

- PF6⁻ 各原子电荷 × 0.8（离子净电荷由 −1e 变为 **−0.8e**）；
- Li⁺ 电荷 +1e → **+0.8e**；
- 若 LigParGen 原子类型与 ilff 不一致，用 0.8 标定统一：EC/EMC 原子电荷同样按
  0.8 倍缩放。

缩放须在 .itp 中手工完成，并复核体系总电荷为 0：
`N_PF6 × (−0.8) + N_Li × (+0.8) = 0`（溶剂分子电中性）。

## 验证

- 无 GROMACS 环境：`pytest tests/test_md_runner.py` 只跑确定性单元测试，slow 跳过；
- 安装 GROMACS 后（`winget install GROMACS.GROMACS` 或
  `conda install -c conda-forge gromacs`）：
  `pytest tests/test_md_runner.py -m slow` 运行 0.1 ns 短轨迹（约 10~20 分钟），
  断言返回 `D_Li_m2_s`。
