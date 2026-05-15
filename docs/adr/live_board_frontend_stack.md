# ADR: Live Board Frontend Stack

## Status

Accepted for SkillLogBoard v1.3.

## Context

SkillLogBoard Live Board is a local-first interface over files already written by the package:
`manifest.yaml`, `metrics.csv`, `events.jsonl`, `skill_trace.jsonl`, report artifacts, and agent
evidence files. v1.2 established the app shell and view-scoped API behavior. v1.3 needs a more
maintainable frontend source layout and a polished UI without changing the installed runtime into a
cloud service.

End users should be able to install the Python package and run `skilllog watch` without having Node
installed. Node is only a development and release build tool.

## Decision

Use React, TypeScript, and Vite for the v1.3 Live Board source application under
`frontend/live-board/`.

Compiled assets are written into the Python package under:

```text
src/skilllogboard/live/static/app/
```

The FastAPI server serves that compiled app when `index.html` is present. During development or in
source checkouts where the frontend has not been built, the server keeps the existing bundled
`live/templates/live.html` fallback.

The frontend consumes the existing local REST endpoints:

```text
GET /api/health
GET /api/config
GET /api/state?view=...
GET /api/compare?metric=...&runs=...&max_runs=...&max_points=...&normalize=...&align=...
```

## Boundaries

SkillLogBoard will not introduce GraphQL, Apollo, Redux, cloud sync, accounts, multi-user auth, or
a database backend for this Live Board layer. Browser state remains scoped to local storage and the
server remains a local file reader.

React component state and small local hooks are enough for the current app shell. If shared state
pressure grows, add a focused reducer or context for the specific workflow rather than a global
store by default.

## Packaging

Source development may require Node:

```bash
cd frontend/live-board
npm install
npm run build
```

Installed runtime must not require Node. Release builds package the compiled files in
`src/skilllogboard/live/static/app/` and FastAPI serves them locally from the wheel. `node_modules`
is never packaged.

## Fallback

If Node tooling is unavailable, contributors can still run and test the Python Live Board through
the legacy bundled template. The fallback keeps v1.2 behavior available while the v1.3 React app is
being developed and packaged.
