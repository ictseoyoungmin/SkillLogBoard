"""Registry and fallback helpers for report figures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FigureDefinition:
    figure_type: str
    title: str
    requires_metric: bool = False


FIGURE_REGISTRY: dict[str, FigureDefinition] = {
    "metric-curve": FigureDefinition("metric-curve", "Metric Curve", True),
    "metric-curve-overlay": FigureDefinition("metric-curve-overlay", "Metric Curve Overlay", True),
    "seed-errorbar": FigureDefinition("seed-errorbar", "Seed Errorbar", True),
    "ablation-bar": FigureDefinition("ablation-bar", "Ablation Bar", True),
}


def list_figure_types() -> list[str]:
    return sorted(FIGURE_REGISTRY)


def get_figure_definition(figure_type: str) -> FigureDefinition:
    try:
        return FIGURE_REGISTRY[figure_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported report figure type: {figure_type}") from exc


def write_svg_fallback(path: str | Path, title: str, message: str) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    safe_title = _escape_xml(title)
    safe_message = _escape_xml(message)
    out.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360" role="img" aria-label="{safe_title}">
  <rect width="900" height="360" fill="#fbfcfd"/>
  <rect x="24" y="24" width="852" height="312" fill="#ffffff" stroke="#d5dbe3"/>
  <text x="48" y="82" font-family="system-ui, sans-serif" font-size="24" fill="#1f2933">{safe_title}</text>
  <text x="48" y="126" font-family="system-ui, sans-serif" font-size="15" fill="#5f6b7a">{safe_message}</text>
  <polyline points="64,280 220,220 376,240 532,150 688,190 836,112" fill="none" stroke="#2563eb" stroke-width="4"/>
</svg>
""",
        encoding="utf-8",
    )
    return out


def _escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
