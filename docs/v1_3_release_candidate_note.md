# SkillLogBoard v1.3 Release Candidate Note

v1.3 upgrades the optional Live Board frontend into a maintainable commercial-quality local UI.

## Highlights

- React + TypeScript + Vite source app in `frontend/live-board/`.
- Built static assets packaged under `src/skilllogboard/live/static/app/`.
- FastAPI serves the compiled app when present and falls back to the v1.2 bundled template.
- Componentized Overview, Runs, Compare, Metric Lab, Artifacts, Reports, Agent, and Settings views.
- Command palette, inspector drawer, table component, SVG chart wrapper, and responsive layout.
- REST/local API only: no GraphQL, cloud sync, accounts, server-side UI preferences, or database.

## Verification

```bash
cd frontend/live-board
npm ci
npm run lint
npm run test
npm run build
cd ../..
.venv/bin/python -m pytest -q tests/test_live_packaging.py tests/test_live_server.py tests/test_live_ui_snapshot.py
```
