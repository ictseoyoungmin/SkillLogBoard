# Agent Workflow

1. Run `skilllog agent init` once per project.
2. Edit `.skilllog/experiment_plan.md` with the research goal.
3. Run experiments with `RunLogger`.
4. Log important steps with `skilllog agent log-action`; add `--file-changed` when a handoff should list edited files.
5. Build report artifacts with `skilllog report build`.
6. Write handoff notes with `skilllog agent handoff`.
7. Gate completion with `skilllog agent check`; add `--strict` when warnings should fail the check.

The workflow is file-based so another human or external coding agent can inspect and continue the
work without relying on hidden state.

Handoff files are generated from local run artifacts and logged agent actions. Files changed are
manual/action-log evidence, not an automatic git diff.
