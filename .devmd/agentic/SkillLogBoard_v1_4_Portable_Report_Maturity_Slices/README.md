# SkillLogBoard v1.4 Portable Report Maturity Slices

## Purpose

v1.4 matures the static dashboard/report layer into a portable evidence document system.

v1.2/v1.3 focus on the local Live Board app. v1.4 focuses on the files that survive after a run is complete:

```text
dashboard.html
report.html
summary.md
report_manifest.yaml
figures/
tables/
artifacts/
```

## Product Decision

Static outputs must remain separate from the Live Board app.

```text
Static dashboard/report:
  portable, offline-friendly, shareable evidence package

Live Board:
  local interactive app for exploration
```

## v1.4 Goal

```text
run folder
→ portable dashboard/report package
→ offline rendering
→ figures/tables/provenance
→ reproducible evidence bundle
```

## Included Structure

```text
SkillLogBoard_v1.4_Portable_Report_Maturity_DevPlan.md

.devmd/v1.4_portable_report_maturity/
  README.md
  day1/
  day2/
  day3/
  day4/
  day5/
  day6/
  day7/
```

## Final Verification

```bash
pip install -e ".[dev,dashboard,report]"
ruff check .
pytest -q
python examples/basic_usage.py
python examples/live_demo.py --multi-run --runs 5 --rich
python -m build --no-isolation
```
