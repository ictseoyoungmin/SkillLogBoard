"""Bundle portable report packages."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def bundle_report_zip(report_dir: str | Path, output_path: str | Path | None = None) -> Path:
    root = Path(report_dir)
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Report directory not found: {root}")
    if not (root / "report_manifest.yaml").exists():
        raise ValueError(f"report_manifest.yaml not found in report directory: {root}")
    out = Path(output_path) if output_path else root.with_suffix(".zip")
    out.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(out, "w", compression=ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.resolve() != out.resolve():
                zf.write(path, path.relative_to(root).as_posix())
    return out
