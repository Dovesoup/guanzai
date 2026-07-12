# Contributing

Thank you for helping GuanZai become more useful without becoming louder than the problem it serves.

## Before starting

- Search existing issues and keep changes focused.
- For policy changes, describe the task examples that should route differently and why.
- For provider support, separate capability detection, command construction, and actual execution claims.
- Never commit credentials, authentication caches, private memories, chat logs, personal paths, or real confidential task text.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
```

On Windows, use `py` in place of `python3` and activate the environment with `.venv\Scripts\activate`.

Add deterministic tests for behavior changes. Tests should cover both the desired route and a nearby case that must not over-trigger delegation or audit.

## Pull-request checklist

- Run `python3 -m unittest discover -s tests -v` (or `py -m unittest discover -s tests -v` on Windows) and report the result.
- Inspect `git diff --check` and the complete staged diff.
- Search the staged content for API keys, tokens, cookies, OAuth material, home-directory paths, `.guanzai/` state, and private task data.
- Keep manifests honest: `planned` must not be described as executed.
- Update README translations when a user-visible capability or limitation changes.
- Update `PRIOR_ART.md` and `THIRD_PARTY.md` when an external project influenced the design or when third-party material is introduced.
- Preserve every applicable upstream copyright and license notice in copied or modified files.

## Attribution

Ideas may be acknowledged in `PRIOR_ART.md`. Copied or modified code, documentation, assets, or datasets require a license-compatible review and a specific entry in `THIRD_PARTY.md`; retain file-level notices where required. “Inspired by” is not a substitute for complying with a license.

## Scope and conduct

Small, reviewable pull requests are easiest to understand. Product discussion is welcome, especially when grounded in reproducible examples, costs, failure modes, and respect for user control. Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
