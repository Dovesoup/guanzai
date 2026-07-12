# GuanZai Public Alpha Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a privacy-safe, multilingual GuanZai `v0.3.0-alpha.1` repository and GitHub prerelease under `Dovesoup/guanzai`.

**Architecture:** The public tree contains only source, tests, the Codex Skill, governance documents, translations, and CI. Generated artifacts and personal state are excluded. English is the canonical README; translations preserve claims and limitations without marketing expansion.

**Tech Stack:** Python 3.9+, Markdown, GitHub Actions, GitHub CLI, Git.

---

### Task 1: Public-tree hygiene

**Files:** Create `.gitignore`; modify `pyproject.toml`; modify version files.

- [x] Add ignores for build output, egg metadata, caches, virtual environments, local memory, credentials, editor state, and OS files.
- [x] Set version `0.3.0a1`, add project metadata, Python classifiers, repository URLs, and MIT license declaration.
- [x] Run path, credential-pattern, and generated-artifact scans; expect no publishable matches.

### Task 2: Canonical documentation and governance

**Files:** Rewrite `README.md`; create `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`, `PRIOR_ART.md`, `THIRD_PARTY.md`, `docs/ARCHITECTURE.md`, `docs/PRIVACY.md`.

- [x] Write the English canonical README with positioning, quick start, modes, provider boundary, Alpha limitations, roadmap, languages, and acknowledgements.
- [x] Add governance, security reporting, privacy boundaries, architecture, attribution, and release history.
- [x] Check all internal Markdown links resolve.

### Task 3: Multilingual entry points

**Files:** Create `README.zh-CN.md`, `README.ja.md`, `README.ko.md`, `README.es.md`.

- [x] Translate the canonical content without adding capabilities or omitting Alpha limitations.
- [x] Preserve commands, filenames, links, version numbers, and policy names exactly.
- [x] Run a parity check for required headings, commands, language links, and warning text.

### Task 4: GitHub community and CI

**Files:** Create `.github/workflows/ci.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/pull_request_template.md`.

- [x] Configure CI for Python 3.9, 3.11, and 3.13 with unit tests, package build, and Skill validation-compatible checks.
- [x] Add structured bug and feature forms plus a PR checklist covering tests, privacy, attribution, and documentation.
- [x] Validate YAML syntax and run the local CI-equivalent commands.

### Task 5: Repository publication

**Files:** Entire audited public tree.

- [ ] Initialize `main`, stage only intended files, inspect staged paths, and commit `release: GuanZai v0.3.0-alpha.1`.
- [ ] Create public repository `Dovesoup/guanzai`, push `main`, and verify remote visibility.
- [ ] Create annotated tag `v0.3.0-alpha.1`, push it, and publish a GitHub prerelease with limitations and roadmap.
- [ ] Verify repository metadata, default branch, Actions status, tag, release URL, and public file contents.
