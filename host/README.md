# host — Agent SDK 薄启动器

`host/run.py` 是虚拟电池工厂协议的执行宿主：加载 `skills/virtual-battery-factory/SKILL.md`
全文作为系统提示，注入案例上下文，经 Agent SDK 运行设计闭环。宿主本身**不注册任何自定义工具**，
协议要求的仿真全部通过内置 Bash 工具调用 `python -m bda` CLI 完成。

## 安装

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[host]"
```

## 运行

```powershell
.venv\Scripts\python.exe host/run.py --config cases/fast_charge_v1.yaml
```

`--config` 指向案例 YAML（**按所给路径直接加载，文件名不限于 config.yaml**，如
`cases/fast_charge_v1.yaml`）；其**所在目录即工作区**（`log.jsonl`、`session_id`、
`report.html` 与 CaseWorkspace 子目录 `candidates/bridge/cell/validation/csv` 均落在此目录）。
案例 YAML 本身不被复制或改名。

冒烟（连通性自检，单次 query）：

```powershell
.venv\Scripts\python.exe host/run.py --smoke-test
```

## 续跑（resume）

session id 保存在工作区的 `session_id` 文件中；重跑同一条 `--config` 命令即自动
resume 该会话（无需人工传 id）。删除 `session_id` 文件则从零开始新会话。

## Step-1 验证结论：SDK 直连可行（无需 OpenAI 回退）

实测（2026-08-16，claude-agent-sdk 0.2.139）：

- 本机 Claude Code 会话经代理运行于 deepseek-v4-pro，环境变量
  `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic` + `ANTHROPIC_AUTH_TOKEN`。
- DeepSeek 提供 **Anthropic 兼容端点**（`/anthropic`），Agent SDK（Anthropic 形状）
  直连即可工作，无需 OpenAI 兼容循环回退（设计文档 §12.1 备用方案未启用）。
- 实测证据：
  - SDK `query()`（async generator，末条消息为 `ResultMessage`）单次文本 query 返回
    `is_error: False, result: 'smoke ok'`；
  - 仅从 `.env` 的 `DEEPSEEK_API_KEY` 引导环境变量（清除会话继承的 ANTHROPIC_* 后）
    同样返回 `smoke ok` —— 证明宿主可独立于交互会话运行；
  - 带 `allowed_tools=[Bash,...]` + `permission_mode="acceptEdits"` 的无头 Bash 工具
    调用实测通过（`permission_denials: []`）。
- 已知噪音：CLI 输出一条 `[claude-code:unrecognized_model] {"model":"deepseek-v4-pro"}`，
  仅为模型名白名单警告，不影响执行。

### 工作配置（环境引导，密钥不落盘）

启动时 `run.py` 按序引导（全部可被已存在的环境变量覆盖）：

| 变量 | 缺省值 | 说明 |
|---|---|---|
| `ANTHROPIC_BASE_URL` | `https://api.deepseek.com/anthropic` | Anthropic 兼容端点；指向其他代理时覆盖 |
| `ANTHROPIC_MODEL` | `deepseek-v4-pro` | 模型名 |
| `ANTHROPIC_AUTH_TOKEN` | 取 `.env` 的 `DEEPSEEK_API_KEY` | 凭证；已有 `ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_API_KEY` 则不再读 `.env` |

认证方式：Bearer token（DeepSeek API key，存于项目 `.env`，已 git 忽略）。
host 自身只把它注入子进程环境变量，不写入任何文件、不打印。

## 测试

```powershell
.venv\Scripts\python.exe -m pytest tests/test_host.py -v
```

冒烟测试在检测不到任何 API 凭证时自动 skip（诚实降级）；有凭证则真实发起一次 query。
