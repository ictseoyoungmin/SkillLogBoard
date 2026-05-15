# SkillLogBoard

Portable experiment logging and dashboard package for local-first ML research.

## Current MVP

SkillLogBoard creates local experiment evidence packages, static dashboards, rule audit traces,
and multi-run comparison reports:

- installable `src/skilllogboard` package
- `RunLogger` lifecycle: running, completed, failed
- metrics CSV and event JSONL logging
- config/system/git snapshots
- artifact, image-path, and table logging
- `summary.md` and single-run `dashboard.html`
- Skills.md v0.3 MVP rule checks with `skill_trace.jsonl`
- v0.4 multi-run compare outputs: `compare.csv`, `compare.md`, and `compare.html`
- v1.4 portable report packages: `report.md`, `report.html`, `report_manifest.yaml`,
  local assets, report tables, chart specs, optional figures, and provenance metadata
- v0.8 agent research workflow files: `.skilllog/`, `agent/actions.jsonl`,
  `agent/handoff.md`, and local completion checks
- v0.9 Template Forge: `ResearchBrief.md`, `TemplateSpec.md`, local scaffold generation,
  and template validation
- v1.3 optional local-first Live Board with React/Vite source frontend, app shell views,
  project Overview default, single-run Metric Lab default, and view-scoped lazy state loading
- CLI `init`, `inspect`, `report`, and `dashboard`
- CLI `compare`, `export-table`, `export-figure`, `report build/check`, and `agent`
- CLI `forge init-brief`, `forge plan`, `forge scaffold`, and `forge validate`
- CLI `watch`

## Install

```bash
pip install -e ".[dev,dashboard]"

# Optional PNG figure export for v1.4 report packages.
pip install -e ".[dev,dashboard,report]"

# Optional local Live Board server.
pip install -e ".[dev,dashboard,live]"
```

Live Board frontend source lives in `frontend/live-board/`. Node is a development/build tool only;
the Python package serves compiled local assets when present and falls back to the bundled template
otherwise.

## CLI

```bash
skilllog --help
skilllog init
skilllog inspect runs/demo/{run_id}
skilllog compare runs/demo --metric val/acc --mode max --output-dir runs/demo/compare
skilllog export-table runs/demo --metric val/acc --format md --output runs/demo/compare.md
skilllog report build runs/demo --metric val/acc --mode max --output-dir runs/demo/report --render-mode package
skilllog report validate runs/demo/report --json
skilllog report bundle runs/demo/report --output runs/demo/report.zip
skilllog report check runs/demo/report --required-table leaderboard
skilllog agent init
skilllog forge init-brief --output ResearchBrief.md
skilllog watch runs/demo/{run_id} --no-open
```

## Smoke Test

```bash
python examples/basic_usage.py
```

The example writes a run folder under `runs/demo/{run_id}/`, where `{run_id}` is generated from
the run name and timestamp:

```text
manifest.yaml
config.yaml
system.json
git.json
metrics.csv
events.jsonl
artifact_index.json
summary.md
dashboard.html
skill_trace.jsonl
artifacts/
```

Open the generated dashboard directly from the run folder:

```bash
# Replace {run_id} with the path printed by the example.
python examples/basic_usage.py
# then open runs/demo/{run_id}/dashboard.html in your browser
```

## Minimal Usage

```python
from skilllogboard import RunLogger

logger = RunLogger(
    project="demo",
    run_name="baseline",
    config={"model_name": "TinyNet", "seed": 42, "lr": 1e-3},
    main_metric={"name": "val/acc", "mode": "max"},
)

logger.log_metrics({"train/loss": 1.0, "val/acc": 0.8}, step=0)
logger.log_note("baseline run")
logger.run_skill_checks(skills_path="Skills.md")
logger.finish(build_dashboard=True, build_report=True)
```

## v0.3 Skills.md Rule Engine

Skills.md rule blocks are parsed and executed for MVP rule types:

- `required_config`
- `required_metric`
- `metric_threshold`
- `best_last_gap`
- `artifact_required`

Rule results are written to `skill_trace.jsonl` and displayed in the dashboard Rule Audit section.
Planned rule types such as `dashboard_panel` and `domain_breakdown` are parsed as planned/skipped
metadata and are not executed as MVP checks.

## v0.4 Multi-run Compare

Compare existing run folders under a runs root:

```bash
skilllog compare runs/demo --metric val/acc --mode max --output-dir runs/demo/compare
```

This writes:

```text
compare.csv
compare.md
compare.html
```

Export leaderboard tables for reports:

```bash
skilllog export-table runs/demo --metric val/acc --format csv --output compare.csv
skilllog export-table runs/demo --metric val/acc --format md --output compare.md
skilllog export-table runs/demo --metric val/acc --format latex --output compare.tex
```

Compare includes a leaderboard, config diff, inferred ablation axes, and seed summary. Research
templates build on these static outputs without adding mandatory domain dependencies.

## v1.4 Portable Report Packages

Generate a report-ready artifact package from existing run folders:

```bash
skilllog report build runs/demo --metric val/acc --mode max --output-dir runs/demo/report
```

This writes:

```text
report.md
report.html
report_manifest.yaml
assets/
tables/
figures/
```

Use `--render-mode minimal` for inline CSS, `--render-mode portable_interactive` for inline
offline table filtering, or `--render-mode package` for `report.html` plus local
`assets/report.css` and `assets/report.js`. No mode uses a CDN.

Report tables are available independently through `export-table`:

```bash
skilllog export-table runs/demo --table leaderboard --metric val/acc --format md --output leaderboard.md
skilllog export-table runs/demo --table seed-summary --metric val/acc --group-by model --format csv --output seeds.csv
skilllog export-table runs/demo --table rule-audit --format latex --output rule_audit.tex
```

Figure export is optional and requires the `report` extra:

```bash
skilllog export-figure runs/demo --type metric-curve-overlay --metric val/acc --output curve.png
```

Without the optional plotting dependency, report builds still produce tables, Markdown, HTML, and
`report_manifest.yaml`, while recording a skipped-figure warning. The manifest records file,
metric, column, run, and step-range provenance for generated evidence.

`skilllog report validate REPORT_DIR --json` produces agent-friendly validation output, and
`skilllog report bundle REPORT_DIR --output report.zip` creates a portable handoff archive.

Report APIs can also be imported directly:

```python
from skilllogboard.reports import build_report_package, parse_report_spec_text
```

## v0.8 Agent Research Layer

Initialize local agent workflow files:

```bash
skilllog agent init --root-dir . --template trajectory
```

This creates `.skilllog/agent_skills.md`, `.skilllog/experiment_plan.md`, `.skilllog/rules.md`,
`.skilllog/report_spec.md`, and `.skilllog/README.md`.

For a run folder, agents can log actions, generate handoff notes, and run local completion checks:

```bash
skilllog agent log-action runs/demo/{run_id} --actor codex --action "run tests" --status completed --command "pytest -q" --file-changed tests/test_agent_rules.py
skilllog agent handoff runs/demo/{run_id} --actor codex --task "summarize current run"
skilllog agent check runs/demo/{run_id} --require-report --strict
```

SkillLogBoard v0.8 does not include built-in LLM inference, cloud sync, or automatic code
generation. It provides local files and validation gates that humans or external coding agents can
use. Handoff files list changed files only when they are logged as action evidence; SkillLogBoard
does not infer a git diff automatically.

Detailed workflow: [Agent Research Layer](docs/agent_research_layer.md).

## v0.9 Template Forge

Create a local harness for a custom research template:

```bash
skilllog forge init-brief --output ResearchBrief.md
skilllog forge plan --brief ResearchBrief.md --name custom-task --output TemplateSpec.md
skilllog forge scaffold --spec TemplateSpec.md --root-dir .
skilllog forge validate custom-task --root-dir .
```

Template Forge creates plugin, example, test, docs, and `.skilllog/` scaffold files for an external
agent or human to fill. SkillLogBoard does not call LLMs, does not contact cloud APIs, and does not
generate final domain-specific research code automatically.

Detailed workflow: [Template Forge](docs/template_forge.md).

## v1.2 Live Board

Watch a local run folder with the optional Live Board server:

```bash
pip install -e ".[dev,dashboard,live]"
python examples/live_demo.py
skilllog watch runs/live_demo/{run_id} --no-open
```

The board serves `/`, `/api/state`, `/api/health`, `/api/config`, and project-mode `/api/compare`
from local files only. `/api/state?view=...` supports Overview, Runs, Compare, Metric Lab,
Artifacts, Reports, Agent, and Local Settings. It can read `manifest.yaml`, `metrics.csv`,
`events.jsonl`, `skill_trace.jsonl`, `artifact_index.json`, `monitoring.jsonl`, report package
metadata, and an optional log file:

```bash
python examples/live_demo.py --multi-run
python examples/live_demo.py --multi-run --runs 5 --rich
skilllog watch runs/live_demo/{run_id} --poll-interval 2 --log-file train.log --monitor-system --monitor-gpu
skilllog watch runs/live_demo --project --latest --no-open
```

`skilllog watch PROJECT_DIR --project` opens Overview by default. `skilllog watch RUN_DIR` opens
Metric Lab by default. `--poll-interval` controls both browser refresh timing and active monitor
sampling, with a safe minimum interval. Project mode uses bounded manifest discovery and skips
cache, virtualenv, report, artifact, and hidden directories.

The v1.2 UI is a local app shell: Project contains Overview, Runs, and Compare; Analysis contains
Metric Lab, Artifacts, and Reports; Evidence contains Agent and Local Settings. Overview and Runs
use summary-first payloads and avoid full metric series. Compare and Metric Lab load bounded series
only for the active view and selected metric/runs. Preferences are stored only in browser
`localStorage` with keys scoped by mode and target directory.

Live dependencies are optional. Core logging, static dashboards, reports, compare outputs, and
Template Forge continue to work without FastAPI, uvicorn, psutil, or GPU tooling.

Detailed workflow: [Live Board](docs/live_board.md).

## v0.5 Research Templates

List lightweight research templates:

```bash
skilllog templates
```

Initialize dependency-free template files:

```bash
skilllog init --template ir-drop
skilllog init --template trajectory
python examples/ir_drop_example.py
python examples/trajectory_example.py
python examples/sklearn_example.py
```

Implemented templates are `ir-drop` and `trajectory`. Planned templates are `classification`,
`segmentation`, and `finance-dashboard`. Optional integrations remain optional; core install does
not require torch, lightning, sklearn, pandas, or domain-specific packages.

The `ir-drop` template uses synthetic data and the metric convention `train/loss`, `val/mae`,
`val/high_drop_f1`, and `val/raw_mae`; it does not include a model or private dataset.
The `trajectory` template uses synthetic values and the metric convention `train/loss`,
`val/loss`, `val/pb_score`, and `val/endpoint_error`; model training is user-provided.
The `sklearn_example.py` file is a core `RunLogger` usage example with sklearn-style metrics, not
a required scikit-learn adapter.

## Troubleshooting

- If `pytest` is missing, install the dev extras: `pip install -e ".[dev,dashboard]"`.
- If `skilllog` is not found, activate the virtual environment or reinstall with `pip install -e .`.
- Generated local runs are written to `runs/`, which is ignored by git.
- Skills.md v0.3 executes MVP rules and records results in `skill_trace.jsonl`.

## Release Verification

```bash
bash scripts/smoke_test.sh
bash scripts/verify_fresh_venv.sh
python -m build --no-isolation
```

Before publishing, isolated `python -m build` should pass in CI or Docker. Local environments that
cannot create isolated build environments can use the no-isolation build as a local smoke check.

## Development Priority

1. Keep the run folder schema stable.
2. Keep core logger framework-agnostic.
3. Keep research plugins separate from the core compare/dashboard MVP.
