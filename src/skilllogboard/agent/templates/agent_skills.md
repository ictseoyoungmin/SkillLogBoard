# Agent Skills

This file gives local workflow guidance to a human or coding agent. SkillLogBoard does not include
built-in LLM inference, cloud sync, or automatic code generation.

## Workflow

1. Read `.skilllog/experiment_plan.md`.
2. Run experiments with `RunLogger`.
3. Log important actions with `skilllog agent log-action`.
4. Generate report artifacts with `skilllog report build`.
5. Generate handoff notes with `skilllog agent handoff`.
6. Run `skilllog agent check` before handing off.

## Do Not

- Do not invent evidence that is not present in local files.
- Do not mark tests as passed unless they were run or explicitly logged.
- Do not add cloud or LLM SDK dependencies to the SkillLogBoard core package.

## Completion Criteria

- Required run files exist.
- Rule trace has no error-level failures.
- Report artifacts are generated when required.
- `agent/actions.jsonl` and `agent/handoff.md` exist.
