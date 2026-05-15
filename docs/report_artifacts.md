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

`minimal` embeds offline CSS and prefers SVG fallback figures when optional plotting dependencies are
missing. This is the smallest portable mode.

`portable_interactive` embeds offline CSS and small inline JavaScript for local table filtering. It
must not reference external CDNs.

`package` writes `assets/report.css` and `assets/report.js` next to `report.html` using relative
paths. It is useful when reviewers want inspectable assets rather than a single HTML file.

## Provenance

`report_manifest.yaml` uses schema version `2.0` and records source files, metrics, table columns,
run ids, and metric step ranges where available. Table and figure outputs also carry per-artifact
provenance. Chart specs are exported as JSON so generated charts remain inspectable and reproducible.

## CLI

```bash
skilllog report build runs/demo --metric val/acc --render-mode minimal
skilllog report build runs/demo --metric val/acc --render-mode portable_interactive
skilllog report build runs/demo --metric val/acc --render-mode package
skilllog report validate runs/demo/report --json
skilllog report open runs/demo/report --dry-run
skilllog report bundle runs/demo/report --output runs/demo/report.zip
```

For screenshot review, capture `report.html` at desktop and narrow widths. The report should render
without network access and without external `http://` or `https://` resources.
