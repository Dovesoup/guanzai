# Privacy

GuanZai is local planning software, not a hosted service. This document describes the repository's own behavior in `v0.3.0-alpha.1`; separately installed agent CLIs and model providers have their own data practices.

## Data GuanZai handles

- The task text passed to `guanzai plan` is held in process memory and included in the JSON manifest printed to standard output.
- `guanzai init` creates `.guanzai/config.toml` and an empty `.guanzai/memory/` directory in the current project.
- `guanzai doctor` checks whether local Codex and WorkBuddy executables are visible and prints capability data, including a discovered WorkBuddy executable path.
- Command builders place the task packet in the generated command arguments.

The current package does not provide telemetry, analytics, a cloud account, a credential store, or automatic command execution.

## What may leave the machine

Nothing is sent by GuanZai's planner itself. Data may leave the machine if a person or another host executes a generated Codex or WorkBuddy command. At that point, task text, task packets, selected project files, and tool results may be processed according to that CLI and provider's settings.

Review the generated manifest and command before execution. Do not place secrets or personal data in task text unless the selected provider, account, and policy are appropriate for it.

## Local state

Treat the entire `.guanzai/` directory as private project state. The repository's default `.gitignore` excludes `.guanzai/` recursively, including `config.toml`, memory, and any future state. Preserve that rule in projects using GuanZai and never force-add the directory, even when its current memory directory is empty. Do not commit:

- API keys, OAuth tokens, cookies, auth caches, or provider configuration;
- conversation histories or raw agent transcripts;
- private task text, customer data, or proprietary documents;
- user-specific memory, personal filesystem paths, or machine inventories.

The public repository contains seed policy only. It should never depend on a maintainer's private memory to route a task.

## Logs and shell history

JSON output, generated commands, terminal scrollback, CI logs, and shell history can retain task text and paths. Redirect or share them only when appropriate. A future execution ledger must provide explicit retention and redaction controls before it can be considered suitable for sensitive use.

## Deletion

GuanZai has no remote account to delete. Remove project-local state by deleting that project's `.guanzai/` directory after confirming it contains nothing you need. Copies in shell history, logs, backups, or external provider systems must be handled in those systems.

## Security reports

If a privacy weakness could expose other users, report it privately using [SECURITY.md](../SECURITY.md). Do not include real secrets or affected people's personal data in a report.
