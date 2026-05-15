# Reporting

Use `summary.md` for a compact single-run summary and `skilllog report build` for v1.4 portable
evidence packages.

```bash
skilllog report runs/demo/{run_id}
skilllog report build runs/demo --metric val/acc --output-dir runs/demo/report --render-mode package
```

The first command preserves the original single-run summary behavior. The second command builds a
multi-run research report package with structured tables, optional figures, local assets, and
manifest provenance. Rendering modes are `minimal`, `portable_interactive`, and `package`; all are
offline-friendly and avoid external CDNs.

Validate and bundle a package for handoff:

```bash
skilllog report validate runs/demo/report --json
skilllog report bundle runs/demo/report --output runs/demo/report.zip
```

See [Portable Report Artifacts](report_artifacts.md) for the static report and Live Board boundary.
