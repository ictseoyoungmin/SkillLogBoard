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
| Local-first Live Board | Planned | Not implemented | v1.0 |
