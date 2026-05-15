# Portable Report Artifacts

SkillLogBoard static reports are portable evidence documents. They are not a Live Board clone and
do not require a server, account, database, CDN, or cloud sync.

## Static Outputs

Single-run outputs remain stable:

```text
run_dir/
  dashboard.html
  summary.md
```

Report packages use the mature v1.4 layout:

```text
report/
  report.html
  report.md
  report_manifest.yaml
  assets/
  figures/
  tables/
```

The Live Board is separate: it reads local files through FastAPI for active inspection, while static
reports are reviewable offline by opening `report.html` directly.

## Render Mode Policy

| Render mode | Assets | JavaScript | Portability notes |
|---|---|---|---|
| `minimal` | Inline offline CSS | None | Smallest static HTML mode; prefers SVG fallback figures when optional plotting dependencies are missing. |
| `portable_interactive` | Inline offline CSS | Inline local table filtering | `report.html` remains readable without JavaScript and must not reference external CDNs. |
| `package` | Relative `assets/report.css` and `assets/report.js` | Local `assets/report.js` | Useful when reviewers want inspectable assets next to `report.html`; all links stay relative. |

`report.js` is an enhancement layer for local table filtering. The report body, tables, manifest,
and provenance remain readable without JavaScript.

## Provenance

`report_manifest.yaml` uses schema version `2.0` and records source files, metrics, table columns,
run ids, and metric step ranges where available. Table and figure outputs also carry per-artifact
provenance. Chart specs are exported as JSON so generated charts remain inspectable and reproducible.

`ReportSpec.md` supports baseline/reference/delta metadata fields such as `baseline_run_id`,
`reference_run_id`, and `delta_mode`. In v1.4 these fields are parsed and preserved for report
planning, but generated tables do not yet compute full baseline deltas automatically. Broader
baseline-delta table wiring is deferred to v1.5 Compare and Operational Rules work.

## CLI

```bash
skilllog report build runs/demo --metric val/acc --render-mode minimal
skilllog report build runs/demo --metric val/acc --render-mode portable_interactive
skilllog report build runs/demo --metric val/acc --render-mode package
skilllog report validate runs/demo/report --json
skilllog report open runs/demo/report --dry-run
skilllog report bundle runs/demo/report --output runs/demo/report.zip
```

`skilllog report validate --json` keeps the original `outcome`, `name`, `message`, and `path`
fields and adds `code`, `severity`, and `suggested_action` for lightweight agent parsing. The full
v1.5 agent feedback schema remains future work.

For screenshot review, capture `report.html` at desktop and narrow widths. The report should render
without network access and without external `http://` or `https://` resources.
