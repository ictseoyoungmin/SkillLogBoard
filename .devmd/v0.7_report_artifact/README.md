# SkillLogBoard v0.7 Report Artifact Layer

## Purpose

v0.7 strengthens SkillLogBoard's research-reporting capability by generating structured tables, figures, report manifests, and report validation rules from existing run data.

## Development Days

```text
day1 — Report data contract, manifest, spec parser
day2 — Table builder and table export
day3 — Figure builder and optional report extra
day4 — Report builder and report output package
day5 — Report rules, CLI, docs, final verification
```

## Compatibility Rule

v0.7 must be additive. It must not break:

- existing RunLogger usage
- existing run folders
- existing dashboard/report/compare commands
- existing export-table behavior
- v0.6 template examples
