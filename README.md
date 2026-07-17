# GuanZai · 观在

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

> 观而后动，众智自生。
> Observe deeply. Act together. Evolve continuously.

> **好钢用在刀刃上。贵模型也是一样。**
> *Save your finest steel—and your premium models—for the work that truly needs them.*

> **Codex × WorkBuddy：中西协作，各尽所长。**
> GuanZai coordinates Codex with cost-effective models available through WorkBuddy, routing each task by capability, cost, and consequence.

**Spend premium intelligence only where it matters.** GuanZai helps avoid unnecessary delegation, use lower-cost models for suitable work, and preserve premium reasoning and independent review for the decisions that matter most.

East meets West—not as a cure-all, but as a practical way to make every premium token count.

> [!WARNING]
> **Public Alpha — `v0.3.0-alpha.1`.** GuanZai produces plans and adapter commands; it is not yet a complete, unattended execution loop. Review every manifest and command before use. Interfaces and policy details may change.

## What this release does

- Classifies tasks deterministically into `solo`, `single`, `team`, or safety-overriding `audited` plans.
- Makes orchestration value, action impact, and independent review visible in a JSON manifest.
- Builds explicit Codex CLI and WorkBuddy commands from bounded task packets.
- Detects local Codex CLI and WorkBuddy CLI capabilities with `guanzai doctor`.
- Keeps bulk mechanical work from being mistaken for cognitive complexity.
- Requires independent audit for decision-grade finance and consequential mutations matched by the current policy.
- Ships an installable Codex Skill and 42 policy, routing, packet, CLI, and capability tests.

GuanZai does **not** currently launch the generated worker commands, poll their progress, collect results, or close the plan–execute–audit loop automatically. A manifest saying `"execution": "planned"` means exactly that.

## Policy defaults

- WorkBuddy Hy3 / Hunyuan 3 (`hy3`) is the first low-cost choice; DeepSeek V4 Pro (`deepseek-v4-pro`) is the next WorkBuddy tier.
- WorkBuddy commands always use `high` reasoning effort.
- WorkBuddy GLM is blocked.
- Premium Fast/speed mode is forbidden; generated work items use standard speed.
- Codex model selection is available only where the local Codex CLI supports it. Codex collaboration workers otherwise inherit host-managed model selection.
- An audit requirement can override a requested worker budget, because a small budget must not silently remove an independent check.

These are current code defaults, not universal claims about model quality.

## Install

GuanZai requires Python 3.9 or later. From a clone:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

On Windows, use `py` in place of `python3` and activate the environment with `.venv\Scripts\activate`.

The Python package installs the `guanzai` CLI only. To make the bundled Skill available to Codex, install it separately from the repository root:

```bash
mkdir -p ~/.codex/skills/guanzai
cp -R skill/guanzai/. ~/.codex/skills/guanzai/
```

Restart Codex after installing or updating the Skill. The Skill guides Codex on when to invoke GuanZai; it does not turn planned adapter commands into an automatic execution loop.

## Quick start

In the project you want to plan for:

```bash
guanzai init
guanzai doctor
guanzai plan "Research, design, implement, and verify a privacy-safe export" --json
```

`guanzai init` creates `.guanzai/config.toml` and an empty local memory directory. It refuses to overwrite an existing configuration.

To request a bounded mode:

```bash
guanzai plan "Rename these files using the existing pattern" --mode solo --json
guanzai plan "Implement the approved parser" --mode single --json
guanzai plan "Research, design, and verify the migration" --mode team --max-workers 3 --json
```

`audited` is selected by policy rather than offered as a command-line override. When action and impact require it, GuanZai preserves at least an executor and an auditor.

## Modes

| Mode | Meaning |
| --- | --- |
| `solo` | Keep the task with the orchestrator; create no worker item. |
| `single` | Create one bounded worker item. |
| `team` | Create complementary roles when breadth or verification justifies them. |
| `audited` | Preserve an independent auditor for policy-matched consequential work, overriding an unsafe budget. |

All routing is deterministic and based on the current text policy. It is explainable and testable, but it is not semantic understanding: unusual wording, other languages, or missing context can produce the wrong plan.

## Capability boundary

`guanzai doctor` reports what the local host can expose. The router can always create a plan, but availability is not execution:

- Codex CLI command generation supports per-command model and reasoning settings when a local `codex` executable is present.
- The current Codex collaboration interface does not expose per-subagent model selection; those workers remain host-managed.
- WorkBuddy discovery checks `codebuddy` on `PATH`, then its standard macOS application bundle path.
- WorkBuddy command generation does not prove that WorkBuddy is installed, authenticated, or that a named model is available.

Never treat a recommendation or generated command as evidence that a model ran.

## Privacy and security

GuanZai's repository contains no credential store or cloud service. Project configuration and future memory live under `.guanzai/`. The repository's `.gitignore` excludes the entire `.guanzai/` directory; keep that rule when using GuanZai elsewhere, and do not force-add local state. Generated task packets can contain the task text you provide; inspect them before passing them to any external agent or provider.

Read [Privacy](docs/PRIVACY.md) for the data boundary and [Security](SECURITY.md) before using the Alpha with sensitive work. Please report vulnerabilities through GitHub's private vulnerability reporting rather than a public issue.

## Architecture

The current path is intentionally short:

```text
task text -> deterministic value/risk gate -> role and model plan
          -> planned manifest -> optional adapter command construction
```

See [Architecture](docs/ARCHITECTURE.md) for invariants, components, and trust boundaries.

## Roadmap

- A durable execution ledger that preserves planned, started, completed, and failed states.
- Opt-in execution, polling, cancellation, normalized results, and explicit human approval points.
- Capability calibration from observed outcomes rather than static preference alone.
- Additional provider adapters through stable contracts, including ACP/MCP-compatible paths.
- Versioned routing policies, multilingual policy evaluation, and safe rollback.
- Stronger separation between public seed knowledge and private project memory.

Roadmap items are intentions, not shipped capabilities.

## Development

```bash
python3 -m unittest discover -s tests -v
```

On Windows, the equivalent command is `py -m unittest discover -s tests -v`.

The current suite contains 42 tests. See [Contributing](CONTRIBUTING.md), [Code of Conduct](CODE_OF_CONDUCT.md), and the [Changelog](CHANGELOG.md).

## Independent work and prior art

GuanZai is an independent project, not a fork of Superpowers, CC Switch, MCO/Hive, LiteLLM, or RouteLLM. No source code from those projects is copied into this release. Their ideas and ecosystem work helped clarify the boundaries around workflows, configuration control planes, multi-CLI execution, gateways, budgets, and routing research.

See [Prior Art](PRIOR_ART.md) and [Third-Party Notice](THIRD_PARTY.md) for precise acknowledgements. If future work copies or modifies third-party source, its license and copyright notices must travel with it.

## License

[MIT](LICENSE) © 2026 Dovesoup.
