# Security Policy

GuanZai is a Public Alpha. It generates plans and commands that may be handed to powerful local agents. Treat every generated command as untrusted until a person has reviewed its task packet, tools, model, working directory, and write permissions.

## Supported versions

Only the latest published prerelease receives security fixes during the Alpha period.

## Reporting a vulnerability

**GitHub private vulnerability reporting will be enabled when the public repository is created.** Use the repository's **Security** tab and select **Report a vulnerability**. This private path is preferred over public issues and does not require publishing sensitive details.

Include, when safe:

- the affected version and environment;
- a minimal reproduction;
- the plausible impact and affected trust boundary;
- whether credentials, private task text, or local files may have been exposed;
- any temporary mitigation you found.

Do not include live credentials or unnecessary personal data. Please allow maintainers a reasonable period to investigate and coordinate a fix before public disclosure. If **Report a vulnerability** is not visible, a public issue may only request a private reporting channel. Never disclose vulnerability details, reproduction steps, affected data, or exploit material in that issue.

## Current security boundaries

- GuanZai does not store provider credentials, but invoked provider CLIs may use their own credential stores.
- `guanzai plan` only emits a plan; the current package does not automatically execute its adapter commands.
- Generated builder commands can request write-capable tools. Review before execution.
- WorkBuddy and Codex installation, authentication, provider transport, and model behavior are outside GuanZai's trust boundary.
- Text-based routing can misclassify a task. `audited` reduces some risks; it is not a security guarantee.

For data handling guidance, see [Privacy](docs/PRIVACY.md).
