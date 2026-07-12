# WorkBuddy Hy3 routing-gate evaluation

Date: 2026-07-11

The bundled WorkBuddy `codebuddy` CLI was invoked directly with Hy3, low reasoning, no tools, one turn, and JSON output. It completed successfully with 6,619 input tokens, 1,893 output tokens, 8,512 total tokens, and zero credits.

Useful findings adopted into v0.2 tests:

- Mechanical volume is not cognitive complexity; a 50-file patterned rename does not earn a team.
- Audit triggers should use action plus impact, not sensitive keywords alone.
- A read-only security report can use one worker; a one-line billing formula mutation requires audit.
- Documented, tested dependencies should not inflate a task into team mode.
- A tested rollback changes an "irreversible" classification.
- Safety precedence is mandatory audit, then delegation economics, then ordinary mode selection.

Observed boundary: WorkBuddy itself loaded 6,619 prompt tokens for a bounded prompt even with tools disabled. It is cheaper than the measured standalone Codex worker overhead but still unsuitable for trivial work.
