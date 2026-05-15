# Docs / Implementation Status Matrix

| Feature | Docs Status | Implementation Status | Target |
|---|---|---|---|
| RunLogger lifecycle | Supported | Implemented | v0.1 |
| Metrics CSV + events JSONL | Supported | Implemented | v0.1 |
| Config/system/git snapshot | Supported | Implemented | v0.1 |
| Artifact/image/table logging | Supported | Implemented MVP | v0.1 |
| Summary report | Supported | Implemented MVP | v0.1 |
| Static Dashboard | Supported | Implemented single-run MVP | v0.2 |
| Skills.md Rule Engine | Supported | Implemented MVP rules | v0.3 |
| skill_trace.jsonl | Supported | Implemented rule trace output | v0.3 |
| RunLogger.run_skill_checks | Supported | Implemented API hook | v0.3 |
| Dashboard Rule Audit | Supported | Implemented MVP | v0.3 |
| Multi-run Compare | Supported | Implemented MVP | v0.4 |
| compare.csv / compare.md / compare.html | Supported | Implemented static exports | v0.4 |
| export-table CSV/Markdown/LaTeX | Supported | Implemented MVP | v0.4 |
| Template registry | Supported | Implemented dependency-free descriptors | v0.5 |
| `skilllog templates` | Supported | Implemented CLI listing | v0.5 |
| `skilllog init --template` | Supported | Implemented for v0.5 templates | v0.5 |
| IR-drop Template | Supported | Implemented lightweight template and synthetic example | v0.5 |
| Trajectory Template | Supported | Implemented lightweight template and synthetic example | v0.5 |
| Classification Template | Planned | Not implemented | v0.5+ |
| Segmentation Template | Planned | Not implemented | v0.5+ |
| Finance Dashboard Template | Planned | Not implemented | v0.5+ |
| domain_breakdown | Planned | Not implemented | v0.5+ |
| dashboard_panel | Planned | Not implemented | v0.5+ |
| scikit-learn-style example | Core logger example | Implemented lightweight example, not a dedicated adapter | v0.5 |
| ReportArtifact / ReportManifest schema | Supported | Implemented | v0.7 |
| ReportSpec.md parser | Supported | Implemented simple Markdown block parser | v0.7 |
| Report tables | Supported | Implemented leaderboard, seed summary, ablation summary, config diff, rule audit | v0.7 |
| `skilllog export-table --table ...` | Supported | Implemented extended table types and CSV/Markdown/LaTeX/HTML/JSON | v0.7 |
| Optional report figures | Supported | Implemented with optional `report` extra and skipped-warning fallback | v0.7 |
| `skilllog export-figure` | Supported | Implemented optional figure command | v0.7 |
| `skilllog report build` | Supported | Implemented report package builder | v0.7 |
| `skilllog report check` | Supported | Implemented report artifact validation checks | v0.7 |
| Portable report render modes | Supported | Implemented minimal, portable_interactive, and package modes | v1.4 |
| Report manifest schema v2 | Supported | Implemented output and package provenance metadata | v1.4 |
| Report chart specs | Supported | Implemented JSON chart spec exports for generated figure records | v1.4 |
| Report offline asset policy | Supported | Implemented inline/package CSS and JS with no CDN references | v1.4 |
| `skilllog report validate/open/bundle` | Supported | Implemented JSON validation, local open helper, and zip bundling | v1.4 |
| Agent-readable report validation JSON | Supported | Implemented `code`, `severity`, and `suggested_action` fields while preserving existing fields | v1.4-cleanup |
| ReportSpec baseline/reference/delta metadata | Supported | Parsed and preserved in spec items; generated baseline-delta tables deferred to v1.5 | v1.4-cleanup |
| Agent Research Layer | Supported | Implemented local file workflow | v0.8 |
| `.skilllog/agent_skills.md` | Supported | Implemented project control file | v0.8 |
| `.skilllog/experiment_plan.md` | Supported | Implemented project control file | v0.8 |
| `.skilllog/rules.md` / `.skilllog/report_spec.md` | Supported | Implemented default generated files | v0.8 |
| `agent/actions.jsonl` | Supported | Implemented append/read helpers and CLI | v0.8 |
| `agent/handoff.md` | Supported | Implemented evidence-grounded handoff builder; files changed come from action-log/manual evidence | v0.8 |
| `agent/decisions.md` | Supported | Implemented append helper | v0.8 |
| `agent_required_commands` | Supported | Implemented command substring checks against successful agent actions | v0.8-cleanup |
| `skilllog agent init` | Supported | Implemented | v0.8 |
| `skilllog agent log-action` | Supported | Implemented with optional `--file-changed` evidence | v0.8-cleanup |
| `skilllog agent handoff` | Supported | Implemented | v0.8 |
| `skilllog agent check` | Supported | Implemented readable, JSON, and `--strict` output policy | v0.8-cleanup |
| `skilllog agent inspect` | Supported | Implemented compact inspection | v0.8 |
| Template Forge | Supported | Implemented local scaffold and validation layer | v0.9 |
| `ResearchBrief.md` | Supported | Implemented contract, template, parser, and `forge init-brief` | v0.9 |
| `TemplateSpec.md` | Supported | Implemented contract, parser, renderer, and deterministic draft generation | v0.9 |
| Template Forge harness assets | Supported | Implemented package-accessible Markdown and scaffold templates | v0.9 |
| `skilllog forge init-brief` | Supported | Implemented | v0.9 |
| `skilllog forge plan` | Supported | Implemented deterministic brief-to-spec planning | v0.9 |
| `skilllog forge scaffold` | Supported | Implemented plugin/example/test/docs scaffold generation | v0.9 |
| `skilllog forge validate` | Supported | Implemented file, scaffold, docs, status, and core dependency checks | v0.9 |
| Built-in LLM template generation | Not planned | Explicit non-goal; external agents may fill local scaffolds | v0.9 |
| Cloud sync / multi-user auth | Out of scope | Not implemented | v1.0+ |
| TensorBoard/W&B import | Out of scope | Not implemented as a built-in importer | v1.0+ |
| Prometheus/Grafana integration | Out of scope | Not implemented | v1.0+ |
| Local-first Live Board | Supported | Implemented optional FastAPI/uvicorn extra over local run files | v1.0 |
| `skilllog watch` | Supported | Implemented run/project modes with optional browser open | v1.0 |
| `/api/state` / `/api/health` / `/api/config` | Supported | Implemented for run and project Live Board state/config | v1.0-cleanup |
| `monitoring.jsonl` | Supported | Implemented optional system/process/GPU sampling with skipped warnings | v1.0 |
| Live Board bounded project discovery | Supported | Implemented depth-limited manifest walk with ignored cache/non-run folders | v1.0-cleanup |
| Live Board HTTP smoke coverage | Supported | Implemented uvicorn/urllib smoke test when live dependencies are installed | v1.0-cleanup |
| GPU empty parse warning | Supported | Implemented skipped warning for empty or malformed `nvidia-smi` output | v1.0-cleanup |
| Live Board Metric Workspace | Supported | Implemented metric catalog, selection, pins, transforms, compare toggle, context tray, drawer, and full-screen lab | v1.1 |
| Live Board local UI preferences | Supported | Implemented browser-only localStorage state; no server sessions | v1.1 |
| Live Board project compare overlay | Supported | Implemented `/api/compare`, bounded metric series, run picker, overlay legend, and best/latest/baseline roles | v1.1.1 |
| Live Board report artifact preview | Supported | Implemented metadata discovery for report/table/figure artifacts and metadata-only preview drawer | v1.1.1 |
| Live Board compact polish | Supported | Implemented collapsed bottom tray, compact side panel toggle, scoped localStorage key, and interaction data attributes | v1.1.1 |
| Live Board rich showcase demo | Supported | Implemented deterministic `--rich` multi-run fixture with shared metrics, statuses, events, rules, artifacts, and agent evidence | v1.1.2 |
| Live Board capability hints | Supported | Implemented local-state-derived run, metric, shared metric, artifact, warning, compare, and agent evidence summaries | v1.1.2 |
| Live Board visual parity polish | Supported | Implemented compact hint rows, metric chips, compare banner, chart affordance legend, guided empty states, grouped artifacts, and agent evidence cards | v1.1.2 |
| Live Board app shell views | Supported | Implemented Overview, Runs, Compare, Metric Lab, Artifacts, Reports, Agent, and Local Settings navigation | v1.2 |
| Live Board default view policy | Supported | Implemented project-mode Overview default and single-run Metric Lab default | v1.2 |
| Live Board view-scoped state | Supported | Implemented `/api/state?view=...` with summary-first Overview/Runs and bounded Compare/Metric Lab series | v1.2 |
| Live Board project summary cache | Supported | Implemented mtime-invalidated metric summary cache for local project payloads | v1.2 |
| Live Board React frontend source | Supported | Implemented Vite/React/TypeScript source app with packaged static output | v1.3 |
| Live Board commercial views | Supported | Implemented componentized Overview, Runs, Compare, Metric Lab, Artifacts, Reports, Agent, and Settings views | v1.3 |
| Live Board command palette and inspector | Supported | Implemented local keyboard palette and metadata inspector drawer | v1.3 |
