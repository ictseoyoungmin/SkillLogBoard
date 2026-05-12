# Report Artifact Layer

SkillLogBoard v0.7 adds a local-first report package on top of existing run folders.
It is additive: existing `summary.md`, `dashboard.html`, compare outputs, and RunLogger usage remain valid.

## Build A Report Package

```bash
skilllog report build runs/demo --metric val/acc --mode max --output-dir runs/demo/report
```

The package contains:

```text
report.md
report.html
report_manifest.yaml
tables/
figures/
```

`report_manifest.yaml` records source runs, generated outputs, parameters, and warnings.

## Tables

```bash
skilllog export-table runs/demo --table leaderboard --metric val/acc --format md --output leaderboard.md
skilllog export-table runs/demo --table seed-summary --metric val/acc --group-by model --format csv --output seeds.csv
skilllog export-table runs/demo --table ablation-summary --metric val/acc --format latex --output ablation.tex
skilllog export-table runs/demo --table rule-audit --format json --output rule_audit.json
```

Supported table types are `leaderboard`, `seed-summary`, `ablation-summary`, `config-diff`, and
`rule-audit`.

## Figures

Figure export uses optional plotting dependencies:

```bash
pip install -e ".[report]"
skilllog export-figure runs/demo --type metric-curve-overlay --metric val/acc --output curve.png
```

When the optional dependency is missing, report builds keep going and record a warning plus a
skipped figure entry in `report_manifest.yaml` instead of failing the table and report generation
path.

## ReportSpec Blocks

`ReportSpec.md` can use simple Markdown blocks:

```markdown
## TABLE-LEADERBOARD
- type: leaderboard
- metric: val/acc
- mode: max
- output: report/tables/leaderboard.md

## FIG-CURVE
- type: metric-curve-overlay
- metric: val/acc
- output: report/figures/curve.png
```

Supported `FIG-*` blocks are executed by `skilllog report build`. Supported figure types are
`metric-curve`, `metric-curve-overlay`, `seed-errorbar`, and `ablation-bar`. Unsupported figure
types are recorded as skipped warnings in `report_manifest.yaml`.

The parser intentionally stays small and ignores unrelated Markdown.

## Public API

```python
from skilllogboard.reports import (
    build_report_package,
    build_report_table,
    parse_report_spec_text,
    read_report_manifest,
)
```

## Validation

```bash
skilllog report check runs/demo/report --required-table leaderboard --required-figure metric-curve-overlay
```

Report checks validate `report_manifest.yaml` and required table/figure artifacts with readable
pass, warning, and error output.
