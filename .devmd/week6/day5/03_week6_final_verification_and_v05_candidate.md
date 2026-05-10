---
week: 6
day: 5
slice: "03_week6_final_verification_and_v05_candidate"
title: "Week 6 final verification and v0.5 candidate"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 03_week6_final_verification_and_v05_candidate — Week 6 final verification and v0.5 candidate

## Objective

Run full verification and prepare v0.5 candidate notes.

## Context

Close Week 6 before Week 7 release hardening.

## Dependencies

- Previous slices in order

## Target Files

- CHANGELOG.md
- README.md
- .devmd/week6/**/*.md

## Implementation Steps

1. Run full verification.
2. Run example smoke tests.
3. Run template CLI tests.
4. Fix only blockers.
5. Confirm docs/status sync.
6. Mark completion blocks.

## Acceptance Criteria

- Editable install succeeds.
- pytest passes.
- basic/ir_drop/trajectory examples succeed.
- Template CLI tests pass.

## Verification Commands

```bash
pip install -e ".[dev,dashboard]"
skilllog --help
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 5.
- Keep optional integrations optional; core install must not require heavy ML packages.
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

