---
milestone: "v0.8"
phase: "Agent Research Layer"
day: "5"
slice: "01_docs_agent_research_layer"
title: "agent research layer docs"
priority: "P0"
status: "pending"
target_version: "v0.8-agent-research"
---

# 01_docs_agent_research_layer — agent research layer docs

## Objective

Document the v0.8 Agent Research Layer workflow.

## Context

Users and coding agents need clear instructions for `.skilllog/`, action logs, handoff, and checks.

## Dependencies

- day4 agent check/rules completed.

## Target Files

- docs/agent_research_layer.md
- docs/agent_workflow.md
- README.md

## Implementation Steps

1. Create `docs/agent_research_layer.md`.
2. Document `.skilllog/` control files.
3. Document run-level `agent/` files.
4. Document CLI commands: init, log-action, handoff, check.
5. Explain that SkillLogBoard does not include built-in LLM/code generation.
6. Add README section or link.

## Acceptance Criteria

- Agent research docs exist.
- Docs explain project-level and run-level files.
- Docs include CLI examples.
- Docs clearly state non-goals: no built-in LLM, no cloud sync, no auto codegen.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/agent_research_layer.md').read_text(encoding='utf-8')
assert 'skilllog agent init' in text
assert 'handoff' in text.lower()
assert 'LLM' in text or 'code generation' in text
print('agent docs check passed')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.7/v0.6 public APIs and run folder compatibility.
- Do not introduce built-in LLM inference, cloud calls, or automatic code generation.
- Core install must remain lightweight. Do not add torch, lightning, sklearn, pandas, matplotlib, LLM SDKs, or domain packages to core dependencies.
- Agent files must be local, inspectable Markdown/JSONL/YAML-compatible artifacts.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-12
**Completed by:** Codex
**Verification command(s):** .venv/bin/ruff check .; .venv/bin/pytest -q; .venv/bin/pytest -q tests/test_agent_action_log.py tests/test_agent_init.py tests/test_agent_handoff.py tests/test_agent_checks.py tests/test_agent_rules.py tests/test_cli_agent.py; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation; .venv/bin/skilllog --version
**Notes:** Implemented v0.8 Agent Research Layer as a local-first file workflow with no built-in LLM, cloud sync, or automatic code generation. Template-specific agent init uses existing template metadata for implemented templates.

<!-- AGENT_STATUS: COMPLETED -->

