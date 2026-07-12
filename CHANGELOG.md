# Changelog

Notable changes are recorded here. Versions follow [Semantic Versioning](https://semver.org/), including prerelease identifiers.

## [0.3.0-alpha.1] - 2026-07-12

First Public Alpha.

### Added

- Deterministic orchestration-value and action-impact gate.
- `solo`, `single`, `team`, and policy-selected `audited` planning.
- Slim planned work-item manifests with role, model, reasoning, speed, and execution state.
- Codex CLI and WorkBuddy command construction.
- Local Codex and WorkBuddy capability discovery through `guanzai doctor`.
- Project initialization with privacy-conscious local configuration defaults.
- Installable Codex Skill and 28 tests.

### Policy

- WorkBuddy Hy3 / Hunyuan 3 and DeepSeek V4 Pro use `high` reasoning effort.
- WorkBuddy GLM is blocked and Fast mode is forbidden.
- Consequential, policy-matched work preserves independent audit despite an undersized worker budget.

### Known limitations

- Generated commands are not automatically executed, polled, cancelled, or collected.
- Routing is a deterministic text policy and can misclassify unfamiliar wording or languages.
- Provider discovery does not prove authentication or named-model availability.

[0.3.0-alpha.1]: https://github.com/Dovesoup/guanzai/releases/tag/v0.3.0-alpha.1
