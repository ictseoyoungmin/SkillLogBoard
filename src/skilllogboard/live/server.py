"""Optional local live board server."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any


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
    from skilllogboard.live.project import build_live_project_state
    from skilllogboard.live.state import build_live_run_state

    opts = options or LiveServerOptions()
    target = Path(target_dir)
    app = FastAPI(title="SkillLogBoard Live Board")

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        return {"ok": True, "mode": "project" if opts.project else "run", "target_dir": str(target)}

    @app.get("/api/state")
    def state() -> dict[str, Any]:
        if opts.project:
            return build_live_project_state(target, latest=opts.latest)
        return build_live_run_state(target, log_file=opts.log_file).to_dict()

    @app.get("/", response_class=HTMLResponse)
    def index():
        return HTMLResponse(load_live_template())

    return app


def load_live_template() -> str:
    return resources.files("skilllogboard.live.templates").joinpath("live.html").read_text(
        encoding="utf-8"
    )


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
            interval=opts.poll_interval,
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
