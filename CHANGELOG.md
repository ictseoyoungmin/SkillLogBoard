# Changelog

## 1.4.0-dev portable report maturity candidate

- Added v1.4 portable report rendering modes: `minimal`, `portable_interactive`, and `package`.
- Added report `assets/` layout support with local `report.css` and `report.js` for package mode.
- Expanded `report_manifest.yaml` provenance with source files, metric, columns, run IDs, and step range metadata.
- Added chart spec export, SVG fallback figures, report validation JSON, report opening, and zip bundling.
- Kept report HTML offline-friendly and CDN-free across all rendering modes.
- Cleanup: synchronized package/CLI version to `1.4.0.dev0`, documented baseline-delta support
  boundaries, and added `code`, `severity`, and `suggested_action` to report validation JSON.

## 1.3.0-dev commercial Live UI candidate

- Added React, TypeScript, and Vite source frontend for the local Live Board.
- Added packaged compiled assets under `skilllogboard.live.static.app` with server fallback to the
  v1.2 bundled template when the build is absent.
- Added componentized commercial views, a command palette, inspector drawer, reusable table, and
  SVG chart wrapper while keeping REST/local API boundaries.

## 1.2.0-dev app shell refactor candidate

- Added a Live Board app shell with Overview, Runs, Compare, Metric Lab, Artifacts, Reports, Agent, and Local Settings views.
- Added project/run default view policy: project mode opens Overview and single-run mode opens Metric Lab.
- Added `/api/state?view=...` for view-scoped state loading, with summary-first Overview/Runs payloads and bounded series payloads for Compare/Metric Lab.
- Reworked project state to use lightweight metric summaries and an mtime-invalidated in-memory cache instead of loading full metric series for every project view.
- Updated Live Board docs, status matrix, and UI guidance for local-first app-shell language and performance boundaries.

## 1.1.2-dev showcase visual parity candidate

- Added `python examples/live_demo.py --multi-run --runs 5 --rich` for deterministic baseline, best, overfit, failed, and current local demo runs.
- Expanded rich demo metrics, events, rule traces, report/table/figure artifacts, and agent evidence so project compare and drawers look populated with real local files.
- Added Live Board capability summaries derived from run/project state for run counts, metric counts, shared metrics, artifacts, warnings, and agent evidence.
- Added compact capability hints, selected metric chips, compare-mode banner, chart affordance text, guided empty states, artifact grouping, and agent evidence cards.
- Kept the Live Board dependency-light and bounded by capping compare points and panel rendering work for better perceived refresh speed.

## 1.1.1-dev UI polish compare candidate

- Added project-mode `/api/compare` with bounded local metric series, selected runs, raw/normalized values, and step/relative alignment.
- Added compare candidates with best/latest/baseline roles, run picker drawer, overlay legend visibility toggles, and scoped browser preferences.
- Polished the Live Board layout with a collapsed bottom tray, compact side panel toggle, loading/empty compare states, and interaction data attributes.
- Expanded report package discovery for `report/`, `reports/`, `tables/`, and `figures/` metadata plus a metadata-only artifact preview drawer.
- Added a multi-run Live Board demo fixture and v1.1.1 contract tests for project compare state, server API, and UI snippets.

## 1.1.0-dev UI/UX redesign candidate

- Redesigned the optional Live Board into a minimal command center with a chart-first Metric Workspace.
- Added metric catalog, deterministic selection, pinning, smoothing, scale, x-axis alignment, compare toggle, and full-screen Metric Lab UI.
- Added context markers, report artifact summaries, and agent workspace summaries to the run-mode Live Board state.
- Added drawer, tray, project overview, artifact/report browser, local-only UI preference persistence, and accessibility labels.
- Added packaged UI design tokens without external CDN, font, or frontend build-tool dependencies.

## 1.0.0-dev live board candidate

- Added optional local-first Live Board package with run and project state readers.
- Added `skilllog watch` with host, port, project, latest, log tail, system monitor, GPU monitor, and browser-open controls.
- Added packaged self-contained Live Board HTML served by optional FastAPI/uvicorn dependencies.
- Added `monitoring.jsonl` helpers plus optional psutil and `nvidia-smi` monitor sampling.
- Added `examples/live_demo.py`, Live Board docs, and live-extra CI coverage.
- Kept static dashboards, reports, compare outputs, Template Forge, and core logging independent from live dependencies.
- Cleanup: exposed `/api/config` and poll interval config to the UI, bounded project-mode discovery, restored HTTP smoke coverage without `httpx`, and made empty or malformed GPU monitor output visible as skipped warnings.

## 0.9.0-dev template forge candidate

- Added Template Forge contracts for `ResearchBrief.md` and `TemplateSpec.md`.
- Added package-accessible harness documents and scaffold templates for external coding agents.
- Added deterministic brief-to-spec planning without LLM or cloud calls.
- Added `skilllog forge init-brief`, `plan`, `scaffold`, and `validate`.
- Added validation checks for scaffold file presence, plugin descriptor shape, synthetic examples, docs, status, and core dependency policy.
- Kept Template Forge additive with no heavy core dependencies and no automatic domain-code generation.
- Cleanup: improved README discoverability, forge CLI help/error messages, docs/status wording, and filled-template static validator checks.

## 0.8.0-dev agent research layer candidate

- Added local-first agent action logs with `agent/actions.jsonl`.
- Added `.skilllog/` project control plane generation with agent skills, experiment plan, rules, and report spec templates.
- Added evidence-grounded `agent/handoff.md` generation and `agent/decisions.md` helpers.
- Added agent completion checks and agent-specific rule executors.
- Added `skilllog agent init`, `log-action`, `handoff`, `check`, and `inspect`.
- Cleanup: exported the documented `skilllogboard.agent` public API, added `agent_required_commands`, `skilllog agent check --strict`, and action-log files-changed evidence for handoffs.
- Documented that v0.8 does not include built-in LLM inference, cloud sync, or automatic code generation.

## 0.7.0-dev report artifact layer candidate

- Added report artifact schemas, `report_manifest.yaml` read/write helpers, and a simple `ReportSpec.md` parser.
- Added report table builders for leaderboard, seed summary, ablation summary, config diff, and rule audit outputs.
- Added optional figure builders behind the `report` extra so matplotlib is not a core dependency.
- Added `skilllog report build`, `skilllog report check`, `skilllog export-figure`, and extended `export-table --table ...`.
- Added static `report.md` and `report.html` package generation with provenance and skipped-figure warnings.
- Cleanup: exported documented report APIs, aligned `ReportSpec.md` FIG block execution with report builds, and added optional report-extra figure CI coverage.

## 0.6.0-dev release hardening candidate

- Started Week 7 release hardening for packaging metadata, optional extras, build verification, CI, and release documentation.
- Normalized package version metadata for the v0.6 candidate.
- Added package-data and optional-dependency verification coverage.
- Added release checklist, release notes draft, smoke scripts, wheel install verification, and optional Docker test file.

## 0.5.0-dev research templates candidate

- Added dependency-free research template descriptors and registry.
- Added `skilllog templates` and `skilllog init --template` for implemented/planned templates.
- Added implemented `ir-drop` and `trajectory` templates with default configs and Skills.md rules.
- Added synthetic IR-drop, trajectory, and sklearn-style examples plus smoke tests.
- Added optional PyTorch and Lightning helper skeletons with lazy imports.

## 0.4.0-dev compare candidate

- Added Week 5 multi-run run discovery and manifest/config/metric indexing.
- Added compare leaderboard, config diff, ablation axis extraction, and seed summary helpers.
- Added static `compare.csv`, `compare.md`, and `compare.html` report generation.
- Added working `skilllog compare` and `skilllog export-table` commands.

## 0.3.0-dev rule engine candidate

- Added Week 4 Skills.md RULE block parser and RuleSpec/RuleResult schema.
- Added MVP rules: required_config, required_metric, metric_threshold, best_last_gap, artifact_required.
- Added RuleEngine execution, `skill_trace.jsonl` logging, `RunLogger.run_skill_checks`, and dashboard Rule Audit.

## v0.2 dashboard candidate

- Added Week 3 static single-run dashboard, dashboard data loaders, CLI refinements, packaging checks, and dashboard smoke tests.

## v0.1 MVP

- Initial Week 1 project skeleton.
- Added package layout, CLI placeholder, manifest/event/writer placeholders.
- Added Week 2 v0.1 MVP RunLogger lifecycle, metric/config logging, artifact/image/table logging, summary generation, and integration tests.
