# GuanZai · 观在

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

> 观而后动，众智自生。
> 深察，而后行动。协力，并持续演进。

> **好钢用在刀刃上。贵模型也是一样。**
> *最精良的钢材，和最昂贵的模型，都该留给真正需要它们的工作。*

> **Codex × WorkBuddy：中西协作，各尽所长。**
> GuanZai 将 Codex 与 WorkBuddy 中可用的高性价比模型协调起来，根据能力、成本和后果为每项任务选择合适路径。

**让高级智能只用在关键之处。** GuanZai 帮助避免不必要的委托，为合适的工作使用低成本模型，并将高级推理和独立审查留给最重要的决策。

中西结合，未必包治百病；但在 Codex 和 WorkBuddy 之间合理分工，确实能让每一份额度更有价值。

> [!WARNING]
> **公开 Alpha — `v0.3.0-alpha.2`。** GuanZai 生成计划和适配器命令；它还不是一个完整、无人值守的执行闭环。使用前请审查每一份清单和命令。接口与策略细节可能会变化。

## 本次发布提供的功能

- 以确定性方式将任务分类为 `solo`、`single`、`team`，或由安全策略覆盖选择的 `audited` 计划。
- 在 JSON 清单中明确呈现编排价值、操作影响和独立审查。
- 根据边界明确的任务包构建显式 Codex CLI 和 WorkBuddy 命令。
- 通过 `guanzai doctor` 检测本地 Codex CLI 和 WorkBuddy CLI 能力。
- 避免将批量机械工作误判为认知复杂性。
- 对当前策略匹配的决策级金融任务和后果重大的变更要求独立审计。
- 随附一个可安装的 Codex Skill，以及 42 项覆盖策略、路由、任务包、CLI 和能力的测试。

GuanZai 目前**不会**启动生成的工作者命令、轮询进度、收集结果，也不会自动闭合“计划–执行–审计”循环。清单中的 `"execution": "planned"` 就是其字面含义。

## 默认策略

- WorkBuddy Hy3 / Hunyuan 3 (`hy3`) 是首选的低成本方案；DeepSeek V4 Pro (`deepseek-v4-pro`) 是下一个 WorkBuddy 层级。
- WorkBuddy 命令始终使用 `high` 推理强度。
- WorkBuddy GLM 被禁用。
- 禁止 Premium Fast/高速模式；生成的工作项使用标准速度。
- 仅当本地 Codex CLI 支持时才可选择 Codex 模型。否则，Codex 协作工作者沿用由宿主管理的模型选择。
- 审计要求可以覆盖请求的工作者预算，因为较小的预算不应在无提示的情况下取消独立检查。

这些是当前代码的默认值，并非对模型质量的普遍判断。

## 安装

GuanZai 需要 Python 3.9 或更高版本。从克隆的仓库中执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

在 Windows 上，请用 `py` 代替 `python3`，并通过 `.venv\Scripts\activate` 激活环境。

Python 包只会安装 `guanzai` CLI。若要让 Codex 使用随附的 Skill，请在仓库根目录中单独安装：

```bash
mkdir -p ~/.codex/skills/guanzai
cp -R skill/guanzai/. ~/.codex/skills/guanzai/
```

安装或更新 Skill 后请重启 Codex。Skill 会指导 Codex 何时调用 GuanZai；它不会把规划出的适配器命令变成自动执行闭环。

## 快速开始

在需要规划的项目中执行：

```bash
guanzai init
guanzai doctor
guanzai plan "Research, design, implement, and verify a privacy-safe export" --json
```

`guanzai init` 会创建 `.guanzai/config.toml` 和一个空的本地记忆目录。若配置已存在，它会拒绝覆盖。

要请求一个受限模式：

```bash
guanzai plan "Rename these files using the existing pattern" --mode solo --json
guanzai plan "Implement the approved parser" --mode single --json
guanzai plan "Research, design, and verify the migration" --mode team --max-workers 3 --json
```

`audited` 由策略选择，不作为命令行覆盖选项。当操作及其影响需要审计时，GuanZai 会至少保留一名执行者和一名审计者。

## 模式

| 模式 | 含义 |
| --- | --- |
| `solo` | 任务由编排者保留；不创建工作项。 |
| `single` | 创建一个边界明确的工作项。 |
| `team` | 当任务广度或验证需求足以支持时，创建互补角色。 |
| `audited` | 对策略匹配、后果重大的工作保留独立审计者，并覆盖不安全的预算。 |

所有路由都具有确定性，并基于当前的文本策略。它可以解释、可以测试，但并不具备语义理解：不寻常的措辞、其他语言或缺失的上下文都可能产生错误计划。

## 能力边界

`guanzai doctor` 报告本地主机能够提供的能力。路由器始终可以创建计划，但可用不等于已执行：

- 当本地存在 `codex` 可执行文件时，Codex CLI 命令生成支持为每条命令设置模型和推理参数。
- 当前 Codex 协作接口不支持为每个子智能体选择模型；这些工作者仍由宿主管理。
- WorkBuddy 发现机制先检查 `PATH` 中的 `codebuddy`，再检查其标准 macOS 应用程序包路径。
- 生成 WorkBuddy 命令并不能证明 WorkBuddy 已安装、已认证，或指定模型可用。

绝不要把推荐或生成的命令当作某个模型已运行的证据。

## 隐私与安全

GuanZai 仓库不包含凭据存储或云服务。项目配置及未来的记忆位于 `.guanzai/` 下。仓库的 `.gitignore` 会排除整个 `.guanzai/` 目录；在其他地方使用 GuanZai 时请保留这条规则，也不要强制添加本地状态。生成的任务包可能包含你提供的任务文本；将它们交给任何外部智能体或提供商前请先检查。

在使用 Alpha 处理敏感工作前，请阅读 [隐私说明](docs/PRIVACY.md) 了解数据边界，并阅读[安全说明](SECURITY.md)。请通过 GitHub 的私密漏洞报告功能报告漏洞，不要提交公开 issue。

## 架构

当前路径刻意保持简短：

```text
task text -> deterministic value/risk gate -> role and model plan
          -> planned manifest -> optional adapter command construction
```

有关不变量、组件和信任边界，请参阅[架构说明](docs/ARCHITECTURE.md)。

## 路线图

- 一个持久执行账本，用于保留 planned、started、completed 和 failed 状态。
- 选择启用的执行、轮询、取消、标准化结果，以及明确的人工批准节点。
- 根据观察到的结果校准能力，而不只依靠静态偏好。
- 通过稳定契约增加提供商适配器，包括 ACP/MCP 兼容路径。
- 版本化路由策略、多语言策略评估和安全回滚。
- 更严格地区分公开种子知识与私有项目记忆。

路线图项目只是意向，并非已发布的能力。

## 开发

```bash
python3 -m unittest discover -s tests -v
```

在 Windows 上，等效命令为 `py -m unittest discover -s tests -v`。

当前测试套件包含 42 项测试。请参阅[贡献指南](CONTRIBUTING.md)、[行为准则](CODE_OF_CONDUCT.md)和[变更日志](CHANGELOG.md)。

## 独立开发与既有工作

GuanZai 是一个独立项目，并非 Superpowers、CC Switch、MCO/Hive、LiteLLM 或 RouteLLM 的分支。本次发布没有复制这些项目的源代码。它们的理念与生态工作帮助厘清了工作流、配置控制平面、多 CLI 执行、网关、预算和路由研究之间的边界。

准确致谢请参阅[既有工作](PRIOR_ART.md)和[第三方声明](THIRD_PARTY.md)。如果未来复制或修改第三方源代码，必须一并保留其许可证和版权声明。

## 许可证

[MIT](LICENSE) © 2026 Dovesoup.
