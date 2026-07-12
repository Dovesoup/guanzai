# GuanZai Public Alpha Release Design

## Purpose

Publish GuanZai as an independent, privacy-safe open-source project at the intersection of humane judgment and agent technology. The release should feel calm, precise, and useful: Eastern restraint without religious imagery or inflated claims.

## Release identity

- Repository: `guanzai`
- Release: `v0.3.0-alpha.1`
- License: MIT
- Primary language: English
- Translations: Simplified Chinese, Japanese, Korean, Spanish
- Motto: `观而后动，众智自生。`
- English line: `Observe deeply. Act together. Evolve continuously.`

## Positioning

GuanZai is a policy and governance layer for local AI agents. It decides when work should stay solo, when delegation earns its cost, and when independent audit is mandatory. It does not compete with every agent harness or rebuild mature development workflows.

The first public release proves four claims:

1. Simple work can remain single-agent.
2. Complex work can be routed to bounded roles and model tiers.
3. Decision-grade finance and consequential mutations cannot silently lose independent audit.
4. Codex and WorkBuddy can participate through explicit, capability-aware adapters.

## Public repository contents

- Python routing core and CLI
- Codex Skill
- Unit and policy tests
- Architecture, privacy, security, and prior-art documentation
- GitHub Actions CI
- Issue and pull-request templates
- MIT license, contribution guide, code of conduct, changelog
- Five language README entry points

Build artifacts, egg metadata, local work files, credentials, private memories, and machine-specific paths are excluded.

## Tone and visual language

Use generous whitespace, short sentences, ink-like neutrals, deep teal, and a restrained cinnabar accent. Do not use Buddha figures, lotus motifs, mystical promises, anthropomorphic hype, or claims of consciousness. Warmth comes from humane defaults: cost restraint, explicit uncertainty, independent review, and respect for user control.

## Attribution

`PRIOR_ART.md` and `THIRD_PARTY.md` name and link:

- Superpowers: software-development workflow, slim task briefs, progress ledger, model-tier guidance
- CC Switch: cross-client provider/configuration control plane
- MCO/Hive: multi-CLI execution adapters and orchestration patterns
- LiteLLM and RouteLLM: gateway, budget, and routing research

The README states that GuanZai is independent and not a fork. Any future copied or modified source retains its original license notice at file and repository level.

## Privacy and security

- No API keys, OAuth tokens, cookies, auth caches, chat logs, or personal paths.
- Public seed configuration contains no user-specific memory.
- WorkBuddy discovery uses a local application path but stores no credential material.
- Adapter manifests distinguish planned from executed work.
- Fast/premium speed mode remains forbidden by policy.
- Alpha status and capability boundaries are visible in every language.

## Publication workflow

1. Build and audit the public tree.
2. Run all unit tests and secret/path scans.
3. Initialize Git with `main` as the default branch.
4. Create a public GitHub repository named `guanzai`.
5. Push one intentional initial commit.
6. Verify GitHub Actions.
7. Create annotated tag `v0.3.0-alpha.1` and a GitHub prerelease.
8. Publish release notes with limitations and roadmap.

## Success criteria

- A new user can understand the project in under three minutes.
- Installation and first plan require no private context.
- All five READMEs agree on features and Alpha limitations.
- CI and local tests pass.
- Repository history contains no personal data or secrets.
- Prior art is acknowledged without diluting GuanZai's original governance focus.
