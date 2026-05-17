# v1.6 Contest / Research Workflow Semantics

## Development Order

```text
01_status_consistency_fix
02_artifact_role_metadata
03_submission_gate_helper
04_fold_metrics_and_prediction_bundle_helpers
05_query_negative_filter_and_compact_cli
06_compare_topk_quiet_filter_options
07_report_auto_findings_and_submission_gate_block
08_rule_audit_api_and_report_block
09_feedback_schema_and_product_backlog_compiler
10_mosquito_alpha_test_integration_and_rc
```

## Design Rule

When adding semantics, prefer this path:

```text
small helper API
→ manifest/artifact metadata
→ report block
→ Live Board metadata visibility
→ agent-readable JSON
```

Avoid adding a large framework or hidden automation that makes the run folder harder to inspect.
