---
name: guanzai
description: Use when a task may benefit from multiple agents, cost-aware model routing, WorkBuddy collaboration, finance evidence review, project-local memory planning, or choosing reasoning effort across providers.
---

# GuanZai

Observe before acting. Always assess; rarely spawn. Use the lowest-cost capable worker only when delegation value exceeds startup overhead.

## Workflow

1. Run `guanzai doctor`. Never claim execution or model selection that the host does not expose.
2. For a new project, run `guanzai init` once. Do not overwrite an existing `.guanzai/config.toml`.
3. Run `guanzai plan "<task>" --json`. A `solo` decision means continue inline and spawn nobody.
4. Execute only through available adapters. Planned routing is not proof of execution.
5. Require independent review for financial, security, irreversible, or otherwise critical conclusions.
6. Treat `.guanzai/memory/` as reserved local state for a future validated-memory workflow; the Alpha does not yet read, write, or promote lessons automatically.

## Invariants

- Never use premium fast mode or any 1.5× speed multiplier.
- Roles do not own models; route each work item independently.
- Prefer free Hunyuan 3, then DeepSeek V4 Pro in WorkBuddy. Both always use `high` reasoning; domestic-model credits are not a reason to downgrade. GLM is blocked in this Alpha.
- Use Codex high/xhigh only for critical planning, difficult implementation, risk review, or conflict resolution.
- Do not invent providers, model names, credentials, or cross-app permissions.
- A simple task may remain single-agent. Multi-agent overhead must earn its cost.
- Treat volume separately from cognitive complexity; mechanical bulk work does not justify a team by itself.
- Trigger mandatory audit from action plus impact, not a sensitive keyword alone. Decision-grade finance remains auditable.

## Modes

- `auto` (default): deterministic gate selects solo, single, team, or audited.
- `solo`: no external workers; still report recommended safety review.
- `single`: one cheap worker.
- `team`: multiple bounded workers, capped by `--max-workers`.

Safety precedence is: mandatory audit, then delegation-value threshold, then ordinary mode selection. Escalate progressively after failed verification or unresolved disagreement; never start with the full organization.

Read [routing-policy.md](references/routing-policy.md) when changing providers, reasoning tiers, escalation, or memory policy.

## Quick reference

| Need | Action |
|---|---|
| New repository | `guanzai init` |
| See host authority | `guanzai doctor` |
| Plan work | `guanzai plan "任务" --json` |
| Force no delegation | `guanzai plan "任务" --mode solo --json` |
| Cap the team | `guanzai plan "任务" --max-workers 2 --json` |
| New model | Update the versioned registry; keep roles unchanged |
| Provider unavailable | Mark planned, report the boundary, use the next allowed adapter |

## Common mistakes

- Treating a routing manifest as completed work.
- Spawning five roles for a one-step request.
- Binding “frontend”, “finance”, or “audit” permanently to one model.
- Saving personal data in the public repository or promoting a lesson after one anecdote.
