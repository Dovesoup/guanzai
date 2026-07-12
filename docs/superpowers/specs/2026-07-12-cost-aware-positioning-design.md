# GuanZai Cost-Aware Positioning Design

**Date:** 2026-07-12  
**Status:** Approved direction; copy review pending

## Objective

Make GuanZai's central value visible within seconds: it coordinates Codex and WorkBuddy so that premium-model reasoning is reserved for work that genuinely needs it. Improve GitHub discoverability without claiming unmeasured savings or equivalent quality.

## Positioning

The README hero uses three layers:

1. **Human metaphor**

   > **好钢用在刀刃上。贵模型也是一样。**  
   > *Save your finest steel—and your premium models—for the work that truly needs them.*

2. **Cross-ecosystem distinction**

   > **Codex × WorkBuddy：中西协作，各尽所长。**  
   > *GuanZai coordinates Codex with cost-effective models available through WorkBuddy, routing each task by capability, cost, and consequence.*

3. **Credible product promise**

   > **Spend premium intelligence only where it matters.**  
   > GuanZai helps avoid unnecessary delegation, use lower-cost models for suitable work, and preserve premium reasoning and independent review for the decisions that matter most.

The English README may include this restrained aside after the core promise:

> East meets West—not as a cure-all, but as a practical way to make every premium token count.

The Chinese README may use:

> 中西结合，未必包治百病；但在 Codex 和 WorkBuddy 之间合理分工，确实能让每一份额度更有价值。

Translations preserve the meaning and tone rather than translating the Chinese idioms literally when that would sound unnatural.

## Public Alpha Boundary

The existing Public Alpha warning remains above the first detailed feature section. It must clearly state that GuanZai currently produces plans and adapter commands rather than operating a complete unattended execution loop.

No page or repository metadata may claim:

- a percentage of token or monetary savings;
- equal or unchanged output quality;
- automatic end-to-end execution;
- production-grade reliability;
- universal model-quality rankings.

These claims require a reproducible benchmark and will be reconsidered only after one exists.

## GitHub Metadata

Repository description:

> Cost-aware AI agent routing across Codex and WorkBuddy—save premium intelligence for the work that truly needs it.

Repository topics:

- `agent-routing`
- `ai-audit`
- `ai-governance`
- `codex`
- `cost-optimization`
- `deepseek`
- `developer-tools`
- `human-in-the-loop`
- `hunyuan`
- `llm-routing`
- `model-routing`
- `multi-agent-systems`
- `python`
- `workbuddy`

Topics favor phrases that people already use to search for the problem or ecosystem. They remain below GitHub's 20-topic limit.

## README Changes

- Replace the current two-paragraph opening with the three-layer hero.
- Keep language links at the top.
- Move the Public Alpha warning immediately after the hero and short positioning paragraph.
- Preserve the existing capability list, policy defaults, installation instructions, limitations, privacy guidance, prior-art acknowledgement, and roadmap.
- Apply equivalent positioning to English, Simplified Chinese, Japanese, Korean, and Spanish READMEs.
- Do not add badges or unsupported benchmark numbers in this change.

## Verification

- Check all five READMEs for the premium-intelligence promise, Codex, WorkBuddy, cost/capability/consequence routing, and Public Alpha boundary.
- Check commands, versions, links, and policy names remain unchanged.
- Validate internal Markdown links and trailing whitespace.
- Run all unit tests even though behavior is not changing.
- Independently review the final diff for exaggerated claims and translation drift.
- Update GitHub description and topics only after the repository changes pass review.

## Future Discoverability Work

This change improves the search entry points but does not guarantee attention. A later, separately designed phase may add a reproducible cost/quality benchmark, demo media, launch posts, community outreach, and contribution-friendly issues.
