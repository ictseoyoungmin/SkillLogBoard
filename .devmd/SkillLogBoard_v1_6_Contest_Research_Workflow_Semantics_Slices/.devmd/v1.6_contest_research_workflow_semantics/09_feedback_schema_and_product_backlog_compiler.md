---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "09_feedback_schema_and_product_backlog_compiler"
title: "feedback schema and product backlog compiler"
priority: "P2"
status: "pending"
---

# 09_feedback_schema_and_product_backlog_compiler — feedback schema and product backlog compiler

## Objective

Improve alpha-test feedback collection by converting raw feedback into deduplicated product backlog items.

## Context

v1.6 is motivated by the mosquito alpha-test feedback. The core finding is that SkillLogBoard can already collect experiment evidence, but contest/research workflow semantics are still encoded as user conventions.

This milestone should promote repeated contest/research patterns into first-class SkillLogBoard concepts:

```text
submission gate
OOF/test prediction roles
fold metrics
artifact role metadata
negative tag filtering
compact/quiet agent-friendly CLI
auto findings draft
rule audit
structured feedback backlog
```

## Dependencies

- v1.5 Performance, Retention, and Operational Rules cleanup completed.
- alpha-test-project/mosquito feedback exists and is used as product evidence.
- Static report package and Live Board remain separate product surfaces.

## Target Files

- Feedback.md
- src/skilllogboard/feedback/
- src/skilllogboard/cli/main.py
- tests/test_feedback_schema.py
- tests/test_feedback_backlog.py
- alpha-test-project/mosquito/results/backlog/skilllog_alpha_feedback.md
- alpha-test-project/mosquito/results/backlog/skilllog_feature_feedback.md
- alpha-test-project/mosquito/results/backlog/skilllog_product_backlog.md
- alpha-test-project/mosquito/results/backlog/agent_feedback.jsonl

## Implementation Steps

1. Define feedback event schema with fields: source, run_id, product_area, type, priority, title, evidence, suggested_solution, acceptance.
2. Create a lightweight parser for JSONL feedback events.
3. Optionally support extracting backlog-like sections from Markdown, but keep JSONL as canonical for machine parsing.
4. Add CLI command such as `skilllog feedback compile BACKLOG_DIR --output skilllog_product_backlog.md`.
5. Deduplicate items by normalized title/product area/type.
6. Generate a product backlog Markdown grouped by P0/P1/P2 and product area.
7. Update Feedback.md with the new canonical structure.
8. Add tests with mosquito-like feedback examples.

## Acceptance Criteria

- agent_feedback.jsonl schema is documented and tested.
- Feedback compiler can produce deduplicated `skilllog_product_backlog.md`.
- Repeated boilerplate feedback does not create many duplicate backlog items.
- Generated backlog includes acceptance criteria when provided.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_feedback_schema.py tests/test_feedback_backlog.py
python -m skilllogboard.cli.main feedback compile alpha-test-project/mosquito/results/backlog --output alpha-test-project/mosquito/results/backlog/skilllog_product_backlog.md || true
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not publish to TestPyPI/PyPI in this milestone.
- Do not make static reports depend on the Live Board server.
- Do not require external CDN/network access for portable reports.
- Do not weaken local-first file-backed behavior.

## Additional Notes

- This should be a small local utility, not a project management system.
- Prioritize machine-readable JSONL for agents; Markdown can remain human-readable.

## Handoff Notes

- Keep changes focused on contest/research semantics, not generic MLOps sprawl.
- Preserve backward compatibility for existing runs and report packages.
- Prefer explicit artifact roles and manifest metadata over filename-only conventions.
- Keep helpers lightweight: they should reduce boilerplate, not impose a full contest framework.
- If an item is deferred, record the reason in the Agent Completion Block.
- Update docs, examples, and alpha-test feedback/backlog when user-visible behavior changes.

---

## Agent Completion Block

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

