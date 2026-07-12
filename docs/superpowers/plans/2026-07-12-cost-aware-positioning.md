# GuanZai Cost-Aware Positioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make GuanZai's cost-aware Codex × WorkBuddy positioning immediately visible and improve its GitHub search entry points without unsupported performance claims.

**Architecture:** Keep English as the canonical README and mirror its hero meaning in four translations. Treat GitHub description and topics as a separate search surface updated only after local content passes parity, link, test, and claim reviews.

**Tech Stack:** Markdown, Git, GitHub CLI, Python unittest, WorkBuddy CLI

---

### Task 1: Canonical English positioning

**Files:**
- Modify: `README.md`

- [ ] Replace the opening prose after the language links with the approved three-layer hero: the steel metaphor, Codex × WorkBuddy distinction, and “Spend premium intelligence only where it matters.”
- [ ] Add the restrained “East meets West” aside without promising equal quality or quantified savings.
- [ ] Keep the Public Alpha warning directly after the positioning and preserve its execution boundary.
- [ ] Run `git diff --check` and verify `README.md` still contains `v0.3.0-alpha.1`, `execution`, `planned`, `Codex`, and `WorkBuddy`.
- [ ] Commit the canonical copy as `docs: sharpen cost-aware positioning`.

### Task 2: Translation parity

**Files:**
- Modify: `README.zh-CN.md`
- Modify: `README.ja.md`
- Modify: `README.ko.md`
- Modify: `README.es.md`

- [ ] Adapt the approved three-layer hero naturally in each language while preserving the Chinese proverb as a cultural signature.
- [ ] Preserve the restrained aside in meaning, using the approved Chinese wording in `README.zh-CN.md`.
- [ ] Keep the Public Alpha warning and all existing capability limits unchanged.
- [ ] Check every README contains `Codex`, `WorkBuddy`, `v0.3.0-alpha.1`, and an equivalent premium-intelligence promise.
- [ ] Use WorkBuddy DeepSeek V4 Pro at high effort for a read-only parity and overclaim review.
- [ ] Commit translations as `docs: localize cost-aware positioning`.

### Task 3: Local release gate

**Files:**
- Verify: all tracked files

- [ ] Run the internal Markdown-link validator against all tracked Markdown files.
- [ ] Run `python3 -m unittest discover -s tests -v`; expect 28 passing tests.
- [ ] Run `git diff --check`; expect no whitespace errors.
- [ ] Search the staged history for unsupported percentages, equal-quality promises, credentials, and personal absolute paths.
- [ ] Review the complete diff against `docs/superpowers/specs/2026-07-12-cost-aware-positioning-design.md`.

### Task 4: GitHub search surfaces and publication

**Files:**
- External metadata: `Dovesoup/guanzai` description and topics

- [ ] Push reviewed commits to `origin/main` and wait for GitHub Actions to pass.
- [ ] Set the description to `Cost-aware AI agent routing across Codex and WorkBuddy—save premium intelligence for the work that truly needs it.`
- [ ] Replace repository topics with the 14 approved topics from the design specification.
- [ ] Verify repository visibility, default branch, description, topics, README URL, and successful CI.
- [ ] Confirm the local worktree is clean and tracks `origin/main`.
