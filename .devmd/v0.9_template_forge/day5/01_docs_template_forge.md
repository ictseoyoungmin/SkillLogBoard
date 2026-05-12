---
milestone: "v0.9"
phase: "Template Forge"
day: "5"
slice: "01_docs_template_forge"
title: "template forge docs"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 01_docs_template_forge — template forge docs

## Objective

Document the Template Forge workflow for users and external coding agents.

## Context

Template Forge must be clear about its scaffold/harness nature and its no-LLM/no-cloud policy.

## Dependencies

- day4 validator CLI completed.

## Target Files

- docs/template_forge.md
- README.md

## Implementation Steps

1. Create or update `docs/template_forge.md`.
2. Document ResearchBrief.md.
3. Document TemplateSpec.md.
4. Document forge init-brief, plan, scaffold, validate commands.
5. Document external agent workflow.
6. State that SkillLogBoard does not call LLMs or cloud APIs.
7. Add README link/section.

## Acceptance Criteria

- Template Forge docs exist.
- Docs include full workflow.
- Docs include CLI examples.
- Docs explicitly state no built-in LLM/code generation/cloud.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/template_forge.md').read_text(encoding='utf-8')
assert 'ResearchBrief' in text
assert 'TemplateSpec' in text
assert 'forge scaffold' in text
assert 'LLM' in text or 'cloud' in text
print('template forge docs check passed')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.8/v0.7/v0.6 public APIs and run folder compatibility.
- Template Forge is a scaffold/harness/validation system. It must not embed LLM inference or call cloud APIs.
- Generated template code must be local, inspectable, dependency-light, and testable with synthetic examples.
- Core install must remain lightweight. Do not add torch, lightning, sklearn, pandas, matplotlib, LLM SDKs, or domain packages to core dependencies.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [ ] Implementation completed
- [ ] Acceptance criteria verified
- [ ] Tests or smoke checks executed
- [ ] No unrelated files changed
- [ ] Notes added below if anything was skipped or deferred

**Status:** PENDING  
**Completed at:**  
**Completed by:**  
**Verification command(s):**  
**Notes:**  

<!-- AGENT_STATUS: PENDING -->

