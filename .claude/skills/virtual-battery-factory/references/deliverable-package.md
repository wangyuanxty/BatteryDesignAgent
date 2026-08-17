# 交付物格式：交付包索引 `delivery_index.md`（收尾必出，另出 PDF 发布版）

> 由 SKILL.md 第一节第 7 步收尾时按需 Read。索引是全部交付物的"封面 + 受控清单"，把散落的交付物组织为受控设计包；索引只登记**实际生成**的文件（先列目录确认，再逐一写行），不得登记计划中但未产出的文件。

- **封面信息（字段清单，缺一不可）**：
  - 案例名（如 `ed300_4c`）
  - 编号体系：`VBF-<案例ID大写>-<文档码>-<序号>`（案例ID大写时去掉非字母数字字符，如 `ed300_4c` → `ED3004C`；序号为该文档码下的两位流水号，从 `01` 起）
  - 生成日期（`YYYY-MM-DD`）
  - 签署栏：编制/审核/批准三栏，**留空**（供人工签字）
- **文档码对照表（协议固定）**：

  | 文档码 | 含义 | 对应文件 |
  |--------|------|---------|
  | DS | 规格书 | `design_spec.md` |
  | BOM | 物料清单 | `bom.xlsx` |
  | DSH | Datasheet 技术参数表 | `datasheet.docx` |
  | CALC | 计算书 | `calc.xlsx` |
  | DVPR | 设计验证报告 | `dvpr.md` |
  | DFMEA | 失效分析 | `dfmea.md` |
  | CAD | 结构模型 | `cell_model.stl` |

- **文件清单表格式**（每个交付物一行，四列：文件名 / 编号 / 格式 / 来源说明）：
  - 编号：`VBF-ED3004C-DS-01` 形式；同一文件的可编辑源与 PDF 发布版共用**同一编号**，在文件名与格式列区分
  - 格式：`md` / `pdf` / `xlsx` / `docx` / `stl` / `png` / `html` 等实际扩展名
  - 来源说明：该文件由哪一步/哪个工具产出（如"design_spec.md 按 deliverable-design-spec 规范生成"、"xlsx→pdf 由 openpyxl/reportlab 导出"）
  - 附属文件（预览图、图例、报告等）也各占一行，编号用其归属文档码（如 `cell_model_preview.png` 归 CAD、`report.html` 归 DS）
- **PDF 发布版**：用 reportlab（`.venv` 已装）一次性脚本生成 `delivery_index.pdf`，封面配色沿用工程蓝图纸风格 `#14283C`（深蓝底）/`#1E5A8A`（中蓝）/`#C97B3D`（铜橙强调），可简化；内页文件清单表与 md 版逐行一致
- **zip 打包要求**：用 PowerShell `Compress-Archive` 把全部交付物 + `delivery_index.md` + `delivery_index.pdf` 打为 `delivery_package.zip`（放工作区根，不把 zip 自身打包进去）；打完后**必须校验**——解包列出 zip 内容，逐项对照文件清单表，缺一即补打
