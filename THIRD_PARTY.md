# Third-Party Notice

## Bundled material

GuanZai `v0.3.0-alpha.1` contains no source code copied or modified from Superpowers, CC Switch, MCO/Hive, LiteLLM, or RouteLLM. Those projects are acknowledged as prior art in [PRIOR_ART.md](PRIOR_ART.md), not included as dependencies or vendored components.

The runtime package declares no third-party Python dependencies. Python's standard library and the user's separately installed Codex CLI or WorkBuddy application are not redistributed by this repository.

## Referenced external projects

| Project | Relationship in this release |
| --- | --- |
| [Superpowers](https://github.com/obra/superpowers) | Prior-art reference for software-development workflow patterns. |
| [CC Switch](https://github.com/farion1231/cc-switch) | Prior-art reference for cross-client provider and configuration control planes. |
| [MCO](https://github.com/mco-org/mco) / Hive | Prior-art reference for multi-CLI adapters and orchestration. |
| [LiteLLM](https://github.com/BerriAI/litellm) | Prior-art reference for gateways, budgets, and provider routing. |
| [RouteLLM](https://github.com/lm-sys/RouteLLM) | Prior-art reference for cost/quality routing research. |

Each external project remains governed by its own license and notices. A link or command adapter does not grant a license to redistribute that project's software.

## Contribution rule

Before introducing copied or modified third-party code, documentation, assets, schemas, or datasets:

1. confirm that its license is compatible with GuanZai's MIT distribution;
2. retain required copyright and license text at file and repository level;
3. identify the exact material, source, version or commit, license, and modifications here; and
4. avoid implying that an external project endorses GuanZai.

When this notice and a bundled component's license differ, the component's license controls that component.
