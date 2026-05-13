---
milestone: "v0.9-cleanup"
phase: "Template Forge Cleanup"
slice: "01_readme_agent_forge_visibility"
title: "README Agent/Forge visibility"
priority: "P0"
status: "completed"
target_version: "v0.9-cleanup"
---

# 01_readme_agent_forge_visibility — README Agent/Forge visibility

## Objective

Improve README visibility for v0.8 Agent Research Layer and v0.9 Template Forge so users can discover the new workflows quickly.

## Context

v0.9 Template Forge is functionally complete and CI is green. This cleanup phase polishes docs, CLI UX, validator depth, and CI maintenance before v1.0 Live Board.

## Target Files

- README.md
- docs/agent_research_layer.md
- docs/template_forge.md
- docs/status_matrix.md

## Implementation Steps

1. Review README top-level feature list and CLI quickstart sections.
2. Add concise sections for Agent Research Layer and Template Forge.
3. Add command examples for `skilllog agent ...` and `skilllog forge ...`.
4. Make clear that SkillLogBoard does not call LLMs or cloud APIs.
5. Link to detailed docs for agent and forge workflows.
6. Keep README concise.

## Acceptance Criteria

- README clearly mentions Agent Research Layer.
- README clearly mentions Template Forge.
- README examples use actual CLI names.
- No text implies built-in LLM inference, cloud sync, or automatic code generation.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('README.md').read_text(encoding='utf-8').lower()
assert 'agent' in text and 'forge' in text
print('README visibility check passed')
PY
```

## Non-goals

- Do not begin v1.0 Live Board implementation.
- Do not add built-in LLM inference, cloud calls, or automatic code generation.
- Do not implement new domain templates directly.
- Do not change public RunLogger APIs.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this cleanup focused.
- Preserve v0.9 behavior and all existing tests.
- If an item is deferred, update docs and record the reason below.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -c "from pathlib import Path; text=Path('README.md').read_text(encoding='utf-8').lower(); assert 'agent' in text and 'forge' in text; print('README visibility check passed')"`; `.venv/bin/python -m ruff check .`  
**Notes:** README now surfaces Agent Research Layer and Template Forge in the feature list, CLI examples, and detailed-doc links.

<!-- AGENT_STATUS: COMPLETED -->
