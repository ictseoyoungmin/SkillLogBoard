# v1.3 Commercial Live UI Handoff

v1.2 keeps the packaged Live Board dependency-light while introducing the app shell and API
contracts that a React/TypeScript/Vite frontend can consume in v1.3.

## App Shell Decisions

- Project views: Overview, Runs, Compare.
- Analysis views: Metric Lab, Artifacts, Reports.
- Evidence views: Agent, Local Settings.
- Project mode defaults to Overview.
- Single-run mode defaults to Metric Lab.
- Static dashboard/report outputs remain portable files and are not part of the app shell runtime.

## Frontend Components To Extract

- App shell sidebar and current-view router.
- Overview summary cards and run health list.
- Runs table with status, key metric, artifacts, warnings, tags, and branch metadata.
- Compare run picker, metric selector, legend, baseline/latest/best roles, and bounded chart.
- Metric Lab chart controls for smoothing, log scale, relative step alignment, and pins.
- Artifact and report metadata browsers.
- Agent evidence timeline/cards for actions, decisions, handoff, and safety gate files.
- Local Settings surface for refresh interval, target path, local preference reset, and current scope.

## API Contracts

- `/api/config` returns mode, target directory, poll interval, default view, available views, and
  monitor flags.
- `/api/state?view=overview` returns summary-first project state and no full metric series.
- `/api/state?view=runs` returns lightweight run index data.
- `/api/state?view=compare` returns project state with bounded compare series.
- `/api/state?view=lab` returns run/metric-lab state for the selected run or project scope.
- `/api/state?view=artifacts|reports|agent|settings` returns metadata-first local evidence.
- `/api/compare` remains the explicit selected-run/selected-metric endpoint for compare updates.

## Boundaries

- No account, team, invite, organization, avatar, cloud project, remote sync, or multi-user auth
  metaphors.
- No database requirement for v1.3.
- Packaged Python wheels should include compiled static assets so end users do not need Node.
- The frontend can be built with React/Vite, but static dashboard/report HTML remains Jinja-based
  and portable.

## Risks

- A richer frontend must preserve summary-first loading; Overview and Runs should not regress into
  full-series polling.
- Chart and table libraries must not add external CDN dependencies.
- Report/artifact previews must remain metadata-first unless a safe local file-serving policy is
  explicitly designed.
- Browser preferences should stay scoped by mode and target directory.
