# SkillLogBoard v0.9 Template Forge — Development Slices

This folder splits the `SkillLogBoard_v0.9_Template_Forge_DevPlan` into small implementation slices for an agent-driven workflow.

## v0.9 Goal

Implement Template Forge:

- `ResearchBrief.md` contract
- `.skilllog/template_harness.md`
- `.skilllog/template_spec.md`
- TemplateSpec parser/validator
- plugin/template scaffold generation
- synthetic example scaffold
- test scaffold
- docs scaffold
- template validation gate
- agent-facing prompt/harness documents
- CLI commands for scaffold/validate/plan

## Product Rule

SkillLogBoard does **not** generate research code by itself in v0.9.

SkillLogBoard provides:

- schemas
- harness Markdown
- scaffold files
- validation gates
- CLI commands

External coding agents such as Codex, Claude, Cursor, or other agents can read these files and fill in the template implementation.

## Scope Boundary

Allowed:

- local Markdown-based research brief
- local Markdown-based template spec
- scaffold files with placeholders
- template validation checks
- synthetic example requirements
- plugin descriptor scaffold
- tests/docs scaffold
- agent-safe instructions

Not allowed:

- built-in LLM inference
- cloud API calls
- automatic code generation by SkillLogBoard itself
- Live Board implementation
- TensorBoard/W&B import
- Prometheus/Grafana integration
- multi-user auth
- adding heavy ML dependencies to core
- implementing many domain templates directly

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
.devmd/v0.9_template_forge/day1/
.devmd/v0.9_template_forge/day2/
.devmd/v0.9_template_forge/day3/
.devmd/v0.9_template_forge/day4/
.devmd/v0.9_template_forge/day5/
```

Within each day, process files in numeric order.

## Final Verification

At the end of v0.9, run:

```bash
pip install -e ".[dev,dashboard]"
skilllog --help
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python -m build --no-isolation
```
