# Architecture

GuanZai `v0.3.0-alpha.2` is a deterministic planning core with command-building adapters. Its architecture is deliberately smaller than a full agent runtime.

## Current flow

```text
task text
   |
   v
gate.assess_task                 text policy: value, mutation, impact, audit
   |
   v
router.plan_task                 mode, roles, static model tier, worker limit
   |
   v
planned JSON manifest            every work item says execution = planned
   |
   +--> packets.build_packet     bounded worker instruction
   |
   +--> adapters.*_command       Codex or WorkBuddy argv construction
```

The CLI exposes three operations:

- `guanzai init` writes a project-local seed configuration and empty memory directory.
- `guanzai doctor` detects visible Codex and WorkBuddy command surfaces.
- `guanzai plan` returns the routing manifest.

The package does not currently run the adapter commands.

## Components

| Component | Responsibility |
| --- | --- |
| `gate.py` | Deterministic task signals, orchestration value, action impact, and audit requirement. |
| `router.py` | Mode selection, bounded roles, worker budgets, static model choice, planned manifests. |
| `models.py` | Small provider/model capability and relative-cost seed. |
| `packets.py` | Slim task packets that constrain a worker's objective and expected output. |
| `adapters.py` | Side-effect-free argument-list construction for Codex CLI and WorkBuddy. |
| `config.py` | Privacy-conscious project-local defaults. |
| `cli.py` | User commands and host capability discovery. |
| `skill/guanzai/` | Codex Skill entry point and routing reference. |

## Invariants

1. **Plan is not execution.** A recommendation, detected binary, or built command is never recorded as a completed call.
2. **Impact can override economy.** A required independent audit survives an undersized `max_workers` request.
3. **Volume is not complexity.** Mechanical repetition alone should not summon a team.
4. **Fast mode stays off.** Generated work items use standard speed; WorkBuddy uses `high` reasoning.
5. **Unavailable means unavailable.** GLM is excluded from the current model candidates.
6. **Private state stays project-local.** Configuration and future memory belong under ignored `.guanzai/` state, not the public seed.

## Trust boundaries

GuanZai trusts its own deterministic transformation only to describe a plan. It does not trust task text to be complete, text matching to be semantically correct, a detected executable to be authenticated, or an external agent to obey a packet perfectly.

```text
person / project
      | task text and approval
      v
GuanZai planning boundary
      | inspectable manifest and argv
      v
external CLI / provider boundary
      | credentials, network, model behavior, tool effects
      v
project files and external systems
```

Command execution crosses into provider credential stores, network services, model behavior, and tool permissions. Those effects require explicit review in this Alpha.

## Extension direction

Future execution support should use a provider adapter contract with distinct `detect`, `capabilities`, `plan`, `execute`, `poll`, `cancel`, `normalize`, and `usage` stages. State transitions must be durable and auditable. Provider breadth belongs below the governance gate, so adding an agent does not change the meaning of safety policy.

See [Privacy](PRIVACY.md) for data boundaries and the [README](../README.md) for current limitations.
