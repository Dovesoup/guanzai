# Prior Art and Acknowledgements

GuanZai is an independent project. It is not a fork of the projects below, and the `v0.3.0-alpha.2` repository does not copy their source code. We name them because good boundaries are easier to see when neighboring work is acknowledged clearly.

## Projects that informed the landscape

### [Superpowers](https://github.com/obra/superpowers)

Superpowers demonstrates disciplined software-development workflows around planning, small task briefs, progress tracking, verification, and fit-for-purpose model use. GuanZai's distinct concern is the governance decision above a workflow: whether delegation earns its cost and when independent audit is mandatory.

### [CC Switch](https://github.com/farion1231/cc-switch)

CC Switch demonstrates a cross-client control plane for providers, configuration, proxying, usage, prompts, MCP, and skills. GuanZai does not reproduce that control plane; future compatibility may consume explicit configuration or usage interfaces while keeping governance separate.

### [MCO](https://github.com/mco-org/mco) and Hive

MCO and its evolving Hive direction demonstrate multi-CLI adapters, orchestration patterns, permission mapping, and structured execution results. GuanZai currently constructs only Codex and WorkBuddy commands and does not claim MCO/Hive's execution breadth. A future adapter may use such an execution layer without making it GuanZai's governance core.

### [LiteLLM](https://github.com/BerriAI/litellm)

LiteLLM demonstrates a provider-neutral gateway, routing, budgets, fallbacks, and usage observability across model providers. GuanZai's present router is local and deterministic; it is not a gateway or proxy.

### [RouteLLM](https://github.com/lm-sys/RouteLLM)

RouteLLM explores learned and benchmarked routing between models to balance quality and cost. GuanZai currently uses explicit policy and static model metadata. Outcome-based calibration is roadmap work.

## GuanZai's focus

The project's original focus is the orchestration-value gate, action-impact auditing, capability-aware planning, honest planned-versus-executed state, and an evolvable boundary between public policy and private memory.

Acknowledgement does not imply endorsement, affiliation, or compatibility. If future contributions copy or modify third-party material, they must update [THIRD_PARTY.md](THIRD_PARTY.md) and preserve all required notices.
