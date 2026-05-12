# Reporting

Use `summary.md` for a compact single-run summary and `skilllog report build` for v0.7 report-ready
artifact packages.

```bash
skilllog report runs/demo/<run_id>
skilllog report build runs/demo --metric val/acc --output-dir runs/demo/report
```

The first command preserves the original single-run summary behavior. The second command builds a
multi-run research report package with structured tables, optional figures, and provenance.
