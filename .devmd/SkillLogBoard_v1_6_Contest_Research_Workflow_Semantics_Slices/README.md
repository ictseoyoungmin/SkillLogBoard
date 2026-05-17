# SkillLogBoard v1.6 Contest / Research Workflow Semantics Slices

## Purpose

v1.6 turns the mosquito alpha-test feedback into implementation slices.

The alpha-test showed that SkillLogBoard's core logging works, but contest/research semantics are still implemented manually:

```text
- threshold-gated submission logic
- OOF/test prediction artifact convention
- fold-aware metrics
- best/non-tree/pseudo-future filter workflows
- report findings from leaderboard deltas
- rule audit for contest policy
- feedback-to-backlog conversion
```

## Product Theme

```text
SkillLogBoard should not become a full competition framework.
It should provide lightweight semantic helpers that make research evidence self-describing.
```

## Included Structure

```text
SkillLogBoard_v1.6_Contest_Research_Workflow_Semantics_DevPlan.md

.devmd/v1.6_contest_research_workflow_semantics/
  README.md
  01_status_consistency_fix.md
  02_artifact_role_metadata.md
  03_submission_gate_helper.md
  04_fold_metrics_and_prediction_bundle_helpers.md
  05_query_negative_filter_and_compact_cli.md
  06_compare_topk_quiet_filter_options.md
  07_report_auto_findings_and_submission_gate_block.md
  08_rule_audit_api_and_report_block.md
  09_feedback_schema_and_product_backlog_compiler.md
  10_mosquito_alpha_test_integration_and_rc.md
```

## Completion Protocol

Each slice has an Agent Completion Block. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partially implemented work.

## Recommended Final Verification

```bash
pip install -e ".[dev,dashboard,report,live]"
ruff check .
pytest -q
python examples/live_demo.py --multi-run --runs 80 --rich
python -m build --no-isolation
```
