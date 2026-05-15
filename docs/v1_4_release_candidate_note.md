# SkillLogBoard v1.4 Release Candidate Note

v1.4 focuses on portable report maturity. Static reports remain offline evidence documents that can
be shared, reviewed, archived, and inspected without running the Live Board.

## Highlights

- Report render modes: `minimal`, `portable_interactive`, and `package`.
- Manifest schema version `2.0` with package and per-output provenance.
- Offline CSS/JS policy with no CDN dependency.
- Chart spec JSON exports for reproducible figure metadata.
- SVG fallback figures for minimal mode when optional plotting dependencies are unavailable.
- CLI helpers for `skilllog report validate`, `skilllog report open`, and
  `skilllog report bundle`.

## Verification

Recommended release checks:

```bash
pip install -e ".[dev,dashboard,report,live]"
ruff check .
pytest -q
python examples/live_demo.py --multi-run --runs 5 --rich
python -m build --no-isolation
```

## Boundary

The Live Board remains a local FastAPI app for active inspection. Portable reports remain static
HTML/Markdown/YAML/table/figure assets with relative paths and offline provenance.
