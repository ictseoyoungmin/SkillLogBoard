"""Archive-before-delete helper."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import zipfile


def archive_runs(run_dirs: list[str | Path], output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    archive_path = out_dir / f"skilllogboard-archive-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.zip"
    manifest: dict[str, Any] = {"created_at": datetime.now(timezone.utc).isoformat(), "runs": []}
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for raw in run_dirs:
            run_dir = Path(raw)
            manifest["runs"].append(str(run_dir))
            if not run_dir.exists():
                continue
            for path in run_dir.rglob("*"):
                if path.is_file():
                    zf.write(path, arcname=f"{run_dir.name}/{path.relative_to(run_dir).as_posix()}")
        zf.writestr("archive_manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
    return archive_path
