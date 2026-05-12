---
milestone: "v0.8-cleanup"
phase: "Agent Research Layer Cleanup"
slice: "01_agent_public_api_exports_and_import_boundary"
title: "agent public API exports and import boundary"
priority: "P0"
status: "completed"
target_version: "v0.8-cleanup"
---

# 01_agent_public_api_exports_and_import_boundary — agent public API exports and import boundary

## Objective

Stabilize the documented public API exported from `skilllogboard.agent` and ensure importing the agent package remains dependency-light.

## Context

v0.8 Agent Research Layer is functionally complete and CI is green. This cleanup phase resolves minor policy, documentation, CLI, and validation issues before starting v0.9 Template Forge.

## Dependencies

- v0.8 Agent Research Layer completed.
- Latest main CI is green.
- v0.7 Report Artifact Layer remains compatible.

## Target Files

- src/skilllogboard/agent/__init__.py
- tests/test_agent_public_api.py
- tests/test_optional_integrations.py
- README.md
- docs/agent_research_layer.md

## Implementation Steps

1. Inspect `src/skilllogboard/agent/__init__.py` and current agent module exports.
2. Export intended public helpers such as `AgentAction`, `append_agent_action`, `read_agent_actions`, `build_agent_handoff`, `check_agent_completion`, and `append_agent_decision` if these names are implemented.
3. Add `__all__` if consistent with package style.
4. Ensure importing `skilllogboard.agent` does not import optional report dependencies or heavy ML/LLM packages.
5. Add `tests/test_agent_public_api.py` to verify documented imports.
6. Update README/docs examples if public names differ from implemented names.

## Acceptance Criteria

- `from skilllogboard.agent import ...` works for documented agent APIs.
- Public API test covers action log, handoff, decision, and check helpers.
- Importing `skilllogboard.agent` succeeds without optional extras.
- No LLM/cloud/heavy dependency is added to core.

## Verification Commands

```bash
pytest -q tests/test_agent_public_api.py tests/test_optional_integrations.py
python - <<'PY'
import skilllogboard.agent as agent
print('agent public import OK:', agent.__name__)
PY
pytest -q tests/test_agent_action_log.py tests/test_agent_handoff.py tests/test_agent_checks.py tests/test_agent_decisions.py
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
**Verification command(s):** `.venv/bin/python -m pytest -q tests/test_agent_public_api.py tests/test_optional_integrations.py tests/test_agent_action_log.py tests/test_agent_handoff.py tests/test_agent_checks.py tests/test_agent_decisions.py`; `.venv/bin/python -c "import skilllogboard.agent as agent; print('agent public import OK:', agent.__name__)"`; `.venv/bin/python -m ruff check .`  
**Notes:** Exported documented agent helpers and lightweight result/data classes from `skilllogboard.agent`.

<!-- AGENT_STATUS: COMPLETED -->
