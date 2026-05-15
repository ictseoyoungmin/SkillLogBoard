# SkillLogBoard v1.4 Portable Report Maturity Development Plan

## 1. Purpose

v1.4 makes SkillLogBoard's static evidence outputs mature enough for research review, portfolio sharing, and reproducible handoff.

## 2. Target Outputs

```text
run_dir/
  dashboard.html
  summary.md
  report/
    report.html
    report.md
    report_manifest.yaml
    assets/
    figures/
    tables/
```

## 3. Rendering Modes

```text
minimal:
  pure HTML/CSS/SVG where possible
  smallest and most portable

portable_interactive:
  vendored/inline JS for richer charts
  still no CDN

package:
  report.html + assets/*.css/js
  local relative paths
```

## 4. Provenance Policy

v1.4 should provide file/metric/column/step-range provenance by default.

Line-level provenance may remain optional.

## 5. Completion Criteria

v1.4 is complete when:

1. Static dashboard/report outputs render without external CDN.
2. Report package contains manifest, figures, tables, and provenance metadata.
3. Chart specs or figure metadata are reproducible and inspectable.
4. Portable/package modes are documented and tested.
5. Live Board remains separate from static evidence outputs.
