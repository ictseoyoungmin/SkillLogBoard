# Design Notes

## Week 1 Design Priorities

1. Stable run folder standard.
2. Append-only event and metric logs.
3. Atomic manifest updates.
4. Framework-agnostic core package.
5. Dashboard/report generated from stored files.

## Week 2 v0.1 MVP Behavior

1. `RunLogger` owns a single run folder lifecycle and keeps manifest status consistent.
2. `finish()` and `fail()` are idempotent for notebook and script cleanup safety.
3. Metrics are scalar-only in v0.1 and are written to both `metrics.csv` and `events.jsonl`.
4. Config updates use shallow merge semantics and refresh manifest metadata fields.
5. Artifact, image-path, and table logging share `artifact_index.json` as the v0.1 index.
6. `summary.md` reads stored files and remains useful without pandas, torch, or a web server.
