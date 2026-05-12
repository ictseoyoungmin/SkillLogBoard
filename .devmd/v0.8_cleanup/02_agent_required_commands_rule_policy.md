---
milestone: "v0.8-cleanup"
phase: "Agent Research Layer Cleanup"
slice: "02_agent_required_commands_rule_policy"
title: "agent_required_commands rule policy"
priority: "P0"
status: "completed"
target_version: "v0.8-cleanup"
---

# 02_agent_required_commands_rule_policy — agent_required_commands rule policy

## Objective

Decide whether `agent_required_commands` is implemented in v0.8 cleanup or explicitly documented as planned.

## Context

v0.8 Agent Research Layer is functionally complete and CI is green. This cleanup phase resolves minor policy, documentation, CLI, and validation issues before starting v0.9 Template Forge.

## Dependencies

- v0.8 Agent Research Layer completed.
- Latest main CI is green.
- v0.7 Report Artifact Layer remains compatible.

## Target Files

- src/skilllogboard/skills/agent_rules.py
- tests/test_agent_rules.py
- docs/agent_research_layer.md
- docs/status_matrix.md
- README.md

## Implementation Steps

1. Inspect current agent rule types: `agent_handoff_required`, `agent_actions_required`, and `agent_no_error_rules`.
2. Decide path A or B: A) implement `agent_required_commands`, B) document it as planned/optional.
3. Preferred path A if simple: read `agent/actions.jsonl` and check whether required command substrings were logged with passed/completed status.
4. If implementing path A, support `keys: [pytest -q]` style matching from rules.
5. If using path B, update docs/status matrix to avoid implying it is implemented.
6. Add or update tests for the chosen behavior.

## Acceptance Criteria

- The status of `agent_required_commands` is unambiguous.
- If implemented, it detects missing required commands and passes when commands are logged.
- If deferred, docs/status matrix clearly mark it as planned.
- Existing agent rule tests still pass.

## Verification Commands

```bash
pytest -q tests/test_agent_rules.py tests/test_skills_rules.py
python - <<'PY'
from pathlib import Path
text = Path('docs/status_matrix.md').read_text(encoding='utf-8')
assert 'agent' in text.lower()
print('agent rule status docs check passed')
PY
```

## Non-goals

- Do not begin v0.9 Template Forge implementation.
- Do not implement Live Board.
- Do not add built-in LLM inference, cloud calls, or automatic code generation.
- Do not change public RunLogger APIs.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this cleanup focused.
- Preserve v0.8 behavior and all existing tests.
- If an item is intentionally deferred, update docs and record the reason in the Agent Completion Block.
- Core install must remain lightweight.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-12  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -m pytest -q tests/test_agent_rules.py tests/test_skills_rules.py`; `.venv/bin/python -c "from pathlib import Path; text=Path('docs/status_matrix.md').read_text(encoding='utf-8'); assert 'agent_required_commands' in text; print('agent rule status docs check passed')"`; `.venv/bin/python -m ruff check .`  
**Notes:** Implemented `agent_required_commands` using action-log command substring matches with successful statuses.

<!-- AGENT_STATUS: COMPLETED -->
