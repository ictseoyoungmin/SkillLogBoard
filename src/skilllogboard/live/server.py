"""Optional local live board server."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

MIN_POLL_INTERVAL_SECONDS = 0.25
PROJECT_DEFAULT_VIEW = "overview"
RUN_DEFAULT_VIEW = "lab"


class LiveDependencyError(ImportError):
    """Raised when optional live server dependencies are unavailable."""


@dataclass
class LiveServerOptions:
    project: bool = False
    latest: bool = False
    log_file: str | None = None
    poll_interval: float = 1.0
    monitor_system: bool = False
    monitor_gpu: bool = False


def normalized_poll_interval(value: float) -> float:
    return max(MIN_POLL_INTERVAL_SECONDS, float(value))


def require_live_dependencies():
    try:
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse
    except ImportError as exc:
        raise LiveDependencyError(
            "Live Board server requires optional dependencies. "
            'Install with `pip install -e ".[live]"` or `pip install skilllogboard[live]`.'
        ) from exc
    return FastAPI, HTMLResponse


def create_live_app(target_dir: str | Path, options: LiveServerOptions | None = None):
    FastAPI, HTMLResponse = require_live_dependencies()
    from skilllogboard.live.project import build_compare_state, build_live_project_state
    from skilllogboard.live.state import build_live_run_state

    opts = options or LiveServerOptions()
    target = Path(target_dir)
    app = FastAPI(title="SkillLogBoard Live Board")
    config = {
        "mode": "project" if opts.project else "run",
        "default_view": PROJECT_DEFAULT_VIEW if opts.project else RUN_DEFAULT_VIEW,
        "views": ["overview", "runs", "compare", "lab", "artifacts", "reports", "agent", "settings"],
        "target_dir": str(target),
        "poll_interval": normalized_poll_interval(opts.poll_interval),
        "latest": opts.latest,
        "monitor_system": opts.monitor_system,
        "monitor_gpu": opts.monitor_gpu,
    }

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        return {"ok": True, **config}

    @app.get("/api/config")
    def config_endpoint() -> dict[str, Any]:
        return dict(config)

    @app.get("/api/state")
    def state(view: str | None = None) -> dict[str, Any]:
        selected_view = view or config["default_view"]
        if opts.project:
            return build_live_project_state(target, latest=opts.latest, view=selected_view)
        payload = build_live_run_state(target, log_file=opts.log_file).to_dict()
        payload["current_view"] = selected_view
        payload["payload_scope"] = "series" if selected_view in {"lab", "compare"} else "summary"
        return payload

    @app.get("/api/compare")
    def compare(
        metric: str | None = None,
        runs: str | None = None,
        max_runs: int = 6,
        max_points: int = 240,
        normalize: bool = False,
        align: str = "step",
    ) -> dict[str, Any]:
        if not opts.project:
            return {
                "metric": metric,
                "align": align,
                "normalize": normalize,
                "bounds": {"max_runs": max_runs, "max_points": max_points},
                "runs": [],
                "selected_run_ids": [],
                "shared_metrics": [],
                "series": [],
                "warnings": ["compare mode is available in project mode"],
            }
        selected = [item.strip() for item in (runs or "").split(",") if item.strip()]
        return build_compare_state(
            target,
            metric=metric,
            selected_run_ids=selected,
            max_runs=max_runs,
            max_points=max_points,
            normalize=normalize,
            align=align,
            latest=opts.latest,
        )

    @app.get("/", response_class=HTMLResponse)
    def index():
        return HTMLResponse(load_live_template())

    return app


def load_live_template() -> str:
    template_root = resources.files("skilllogboard.live.templates")
    html = template_root.joinpath("live.html").read_text(
        encoding="utf-8"
    )
    css = template_root.joinpath("ui_tokens.css").read_text(encoding="utf-8")
    return html.replace("/* __SKILLLOGBOARD_UI_TOKENS__ */", css)


def run_live_server(
    target_dir: str | Path,
    host: str = "127.0.0.1",
    port: int = 8765,
    options: LiveServerOptions | None = None,
) -> None:
    opts = options or LiveServerOptions()
    try:
        import uvicorn
    except ImportError as exc:
        raise LiveDependencyError(
            "Live Board server requires uvicorn. Install with `pip install -e \".[live]\"`."
        ) from exc
    app = create_live_app(target_dir, options=opts)
    monitor_loop = None
    if not opts.project and (opts.monitor_system or opts.monitor_gpu):
        from skilllogboard.live.monitor_loop import MonitorLoop

        monitor_loop = MonitorLoop(
            target_dir,
            interval=normalized_poll_interval(opts.poll_interval),
            monitor_system=opts.monitor_system,
            monitor_process=opts.monitor_system,
            monitor_gpu=opts.monitor_gpu,
        )
        monitor_loop.start()
    try:
        uvicorn.run(app, host=host, port=port)
    finally:
        if monitor_loop is not None:
            monitor_loop.stop()
