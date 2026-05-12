# Agent Research Layer

SkillLogBoard v0.8 adds a local-first agent research workflow layer. It does not include built-in
LLM inference, cloud sync, or automatic code generation. It provides inspectable files and
validation gates that humans or external coding agents can use.

## Project Control Plane

Initialize `.skilllog/` files:

```bash
skilllog agent init --root-dir . --template ir-drop
```

Generated files:

- `.skilllog/agent_skills.md`: workflow guidance and completion criteria.
- `.skilllog/experiment_plan.md`: research topic, data, metrics, axes, and required outputs.
- `.skilllog/rules.md`: editable rule guidance aligned with the existing Skills.md philosophy.
- `.skilllog/report_spec.md`: v0.7-compatible report artifact specification.
- `.skilllog/README.md`: control plane file index.

## Run-Level Agent Files

For each run, the agent layer can write:

- `agent/actions.jsonl`: machine-readable evidence of actions taken.
- `agent/handoff.md`: evidence-grounded handoff notes.
- `agent/decisions.md`: Markdown decision log.

## CLI Workflow

```bash
skilllog agent log-action runs/demo/{run_id} --actor codex --action "run tests" --status completed --command "pytest -q"
skilllog agent handoff runs/demo/{run_id} --actor codex --task "finish report review"
skilllog agent check runs/demo/{run_id} --require-report
skilllog agent inspect runs/demo/{run_id}
```

`skilllog agent check` returns a non-zero exit code when error-level completion checks fail. Use
`--json` for machine-readable output.

## Non-Goals

- No built-in LLM calls.
- No automatic code generation.
- No cloud sync.
- No multi-user service.
