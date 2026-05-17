---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "05_query_negative_filter_and_compact_cli"
title: "negative filter and compact CLI"
priority: "P1"
status: "pending"
---

# 05_query_negative_filter_and_compact_cli — negative filter and compact CLI

## Objective

Extend query/filter grammar and CLI output for agent-friendly run discovery.

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

- src/skilllogboard/query.py
- src/skilllogboard/cli/main.py
- src/skilllogboard/index/
- tests/test_query_filter.py
- tests/test_cli_query.py
- tests/test_cli_index.py
- docs/operational_rules.md
- docs/live_board.md

## Implementation Steps

1. Extend query parser to support negative filters: `not tag:x`, `not group:x`, `not status:failed` if feasible.
2. Add explicit CLI alternatives: `--include-tags`, `--exclude-tags`, `--metric`, `--compact`.
3. Apply the same filter grammar to `runs list` and index-derived listings.
4. Design compact output for agent loops: run_id, status, selected metric, tags, group, baseline.
5. Keep `--json` available, but optionally support compact JSON with fewer fields.
6. Add tests for positive tags, negative tags, combined filters, invalid filters, and compact output.
7. Document examples from mosquito feedback: exclude tree runs, list pseudo-future runs, find best completed non-tree run.

## Acceptance Criteria

- `not tag:extra-trees` style filters work.
- `--exclude-tags extra-trees,lightgbm` works or equivalent is documented.
- `runs list --compact --metric val/r_hit@1cm` returns concise output.
- Invalid filter expressions produce clear errors.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_query_filter.py tests/test_cli_query.py tests/test_cli_index.py
python -m skilllogboard.cli.main runs list alpha-test-project/mosquito/results/skilllog/mosquito-contest --filter "status:completed not tag:extra-trees" --compact --metric val/r_hit@1cm || true
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

- The grammar should stay simple. Avoid a full SQL-like language.
- Compact output should help both humans and agents quickly identify candidate runs.

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

