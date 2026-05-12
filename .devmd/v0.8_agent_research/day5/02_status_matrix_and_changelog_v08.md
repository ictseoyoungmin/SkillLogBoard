---
milestone: "v0.8"
phase: "Agent Research Layer"
day: "5"
slice: "02_status_matrix_and_changelog_v08"
title: "status matrix and changelog v0.8"
priority: "P0"
status: "pending"
target_version: "v0.8-agent-research"
---

# 02_status_matrix_and_changelog_v08 — status matrix and changelog v0.8

## Objective

Update status matrix and changelog for v0.8 while keeping Template Forge and Live Board planned.

## Context

Docs must accurately distinguish implemented v0.8 agent features from planned v0.9/v1.0 features.

## Dependencies

- 01_docs_agent_research_layer

## Target Files

- docs/status_matrix.md
- CHANGELOG.md
- README.md

## Implementation Steps

1. Add CHANGELOG v0.8 entry.
2. Mark Agent Research Layer implemented if tests pass.
3. Mark `.skilllog/agent_skills.md`, `agent/actions.jsonl`, `agent/handoff.md`, and `skilllog agent check` implemented.
4. Keep Template Forge planned.
5. Keep Live Board planned.
6. Keep TensorBoard/W&B import out of scope or planned only if roadmap already says so.

## Acceptance Criteria

- CHANGELOG contains v0.8 entry.
- Status matrix includes agent research features.
- Template Forge remains Planned.
- Live Board remains Planned.
- Docs do not claim built-in LLM support.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
status = Path('docs/status_matrix.md').read_text(encoding='utf-8')
assert 'Agent' in status or 'agent' in status
assert 'Template Forge' not in status or 'Planned' in status
changelog = Path('CHANGELOG.md').read_text(encoding='utf-8')
assert '0.8' in changelog or 'v0.8' in changelog
print('v0.8 status/changelog checks passed')
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

