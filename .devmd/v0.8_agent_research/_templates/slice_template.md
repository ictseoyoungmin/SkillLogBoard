---
milestone: "v0.8"
phase: "Agent Research Layer"
day: "N"
slice: "NN_slice_name"
title: "Slice Title"
priority: "P0"
status: "pending"
target_version: "v0.8-agent-research"
---

# NN_slice_name — Slice Title

## Objective

Describe the single implementation objective.

## Context

Explain why this slice exists and what should already be available.

## Dependencies

- Previous slices in numeric order.

## Target Files

- path/to/file.py

## Implementation Steps

1. Step one.
2. Step two.

## Acceptance Criteria

- Criterion one.
- Criterion two.

## Verification Commands

```bash
pytest -q
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

