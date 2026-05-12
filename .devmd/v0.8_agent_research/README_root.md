# SkillLogBoard v0.8 Agent Research Layer — Development Slices

This folder splits `SkillLogBoard_v0.8_Agent_Research_Layer_DevPlan.md` into small implementation slices for an agent-driven workflow.

## v0.8 Goal

Implement the Agent Research Layer:

- `.skilllog/agent_skills.md`
- `.skilllog/experiment_plan.md`
- `.skilllog/rules.md` and `.skilllog/report_spec.md` compatibility guidance
- run-level `agent/actions.jsonl`
- run-level `agent/handoff.md`
- run-level `agent/decisions.md`
- `skilllog agent init`
- `skilllog agent log-action`
- `skilllog agent handoff`
- `skilllog agent check`
- agent-specific completion checks/rules
- documentation and tests for agent-assisted research workflows

## Scope Boundary

Allowed:

- project-level `.skilllog/` control plane
- run-level `agent/` evidence folder
- Markdown templates for agent instructions
- JSONL action logs
- handoff and decision documents
- CLI commands under `skilllog agent`
- local validation checks
- tests and docs

Not allowed:

- built-in LLM inference
- automatic code generation
- Template Forge implementation
- Live Board implementation
- cloud sync
- multi-user auth
- TensorBoard/W&B import
- Prometheus/Grafana integration
- model registry
- deployment system
- changing existing RunLogger API unless strictly necessary

## Completion Protocol

Each slice has an **Agent Completion Block**. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for any skipped, deferred, or partially implemented item.

If a slice is blocked by an environment issue, use:

```text
**Status:** COMPLETED_WITH_ENV_LIMITATION
<!-- AGENT_STATUS: COMPLETED_WITH_ENV_LIMITATION -->
```

and explain the limitation in `Notes`.

## Recommended Execution Order

```text
.devmd/v0.8_agent_research/day1/
.devmd/v0.8_agent_research/day2/
.devmd/v0.8_agent_research/day3/
.devmd/v0.8_agent_research/day4/
.devmd/v0.8_agent_research/day5/
```

Within each day, process files in numeric order.

## Final Verification

At the end of v0.8, run:

```bash
pip install -e ".[dev,dashboard]"
skilllog --help
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python -m build --no-isolation
```
