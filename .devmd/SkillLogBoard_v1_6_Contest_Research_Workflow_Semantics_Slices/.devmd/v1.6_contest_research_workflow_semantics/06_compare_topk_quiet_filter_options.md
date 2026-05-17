---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "06_compare_topk_quiet_filter_options"
title: "compare top-k quiet filter options"
priority: "P1"
status: "pending"
---

# 06_compare_topk_quiet_filter_options — compare top-k quiet filter options

## Objective

Make `skilllog compare` suitable for automated research loops by adding top-k, quiet, and filter options.

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

- src/skilllogboard/compare/
- src/skilllogboard/cli/main.py
- tests/test_compare_cli.py
- tests/test_compare.py
- docs/operational_rules.md
- README.md

## Implementation Steps

1. Review current compare CLI behavior and output verbosity.
2. Add `--top-k` to limit console leaderboard rows while keeping full export files available.
3. Add `--quiet` to suppress verbose full leaderboard output and print only concise summary/path outputs.
4. Add `--filter`, `--include-tags`, and `--exclude-tags` support, reusing the v1.6 query grammar.
5. Ensure CSV/MD/HTML export still contains the intended full or filtered data according to options.
6. Add tests for top-k output, quiet output, filtering, and export file existence.
7. Document agent loop examples.

## Acceptance Criteria

- `skilllog compare --top-k 5` limits console output.
- `skilllog compare --quiet` is useful in automation logs.
- Compare can filter candidate runs by include/exclude tags.
- Exports remain deterministic and discoverable.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_compare_cli.py tests/test_compare.py tests/test_query_filter.py
python -m skilllogboard.cli.main compare alpha-test-project/mosquito/results/skilllog/mosquito-contest --metric val/r_hit@1cm --top-k 5 --quiet || true
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

- Do not remove existing verbose compare behavior; add quiet/top-k as optional modes.
- Clarify whether top-k applies only to console output or also export files.

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

