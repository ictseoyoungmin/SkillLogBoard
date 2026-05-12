# Agent Workflow

1. Run `skilllog agent init` once per project.
2. Edit `.skilllog/experiment_plan.md` with the research goal.
3. Run experiments with `RunLogger`.
4. Log important steps with `skilllog agent log-action`.
5. Build report artifacts with `skilllog report build`.
6. Write handoff notes with `skilllog agent handoff`.
7. Gate completion with `skilllog agent check`.

The workflow is file-based so another human or external coding agent can inspect and continue the
work without relying on hidden state.
