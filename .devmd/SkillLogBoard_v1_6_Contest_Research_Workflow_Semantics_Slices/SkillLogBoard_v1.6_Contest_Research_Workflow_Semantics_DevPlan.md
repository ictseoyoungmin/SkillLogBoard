# SkillLogBoard v1.6 Contest / Research Workflow Semantics Development Plan

## 1. Background

The mosquito alpha-test proved that SkillLogBoard can be attached to a real contest-style research workflow. The generated runs, metrics, artifacts, report packages, and Live Board project view were useful.

However, the feedback repeatedly identified that users still have to invent conventions for contest/research semantics:

- OOF prediction vs test prediction
- fold metrics
- submission threshold gate
- best/non-tree/pseudo-future filtering
- compact agent-readable CLI output
- report Key Findings
- project rule audit
- feedback-to-backlog conversion

## 2. Goal

v1.6 should make contest/research workflows self-describing without turning SkillLogBoard into a heavy framework.

The goal is:

```text
manual convention
→ lightweight helper
→ artifact role metadata
→ report/live visibility
→ agent-readable feedback/backlog
```

## 3. Priority

```text
P0:
  status consistency fix

P1:
  artifact role metadata
  submission gate helper
  fold metrics / prediction bundle helpers
  negative tag filter + compact CLI
  compare top-k / quiet / filter options
  report auto findings
  rule audit

P2:
  feedback compiler and product backlog automation
```

## 4. Non-goals

- No cloud sync
- No full Kaggle/DACON framework
- No model training framework abstraction
- No external hosted dashboard
- No automatic AI research claim
- No destructive pruning/deletion behavior

## 5. Completion Criteria

v1.6 is complete when:

1. Completed/failed status is consistent across manifest, summary, dashboard/report.
2. Artifact index supports role metadata.
3. Submission gate can be logged and appears in manifest/report.
4. Fold metrics and prediction bundle helpers reduce contest boilerplate.
5. Query grammar supports negative tag filtering.
6. Index/runs/compare have compact or quiet modes suitable for agent loops.
7. Report can draft Key Findings from leaderboard, delta, warnings, and submission gate.
8. Rule audit can record contest/research policy checks.
9. Feedback files can be converted into deduplicated product backlog.
10. Mosquito alpha-test can use at least the new semantic helpers in one run.
