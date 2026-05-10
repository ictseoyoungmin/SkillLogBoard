"""Optional PyTorch helpers.

Core logger must work without torch installed.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any, Callable


def require_torch(importer: Callable[[str], Any] = import_module) -> Any:
    try:
        return importer("torch")
    except ImportError as exc:
        raise ImportError(
            "PyTorch helpers require the optional dependency 'torch'. "
            "Install torch separately or use SkillLogBoard core APIs without it."
        ) from exc


def torch_available(importer: Callable[[str], Any] = import_module) -> bool:
    try:
        require_torch(importer)
    except ImportError:
        return False
    return True


def scalar_to_float(value: Any) -> float:
    if hasattr(value, "detach"):
        value = value.detach()
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "item"):
        value = value.item()
    return float(value)


def log_torch_metrics(logger: Any, metrics: dict[str, Any], step: int | None = None, **metadata: Any) -> None:
    logger.log_metrics({name: scalar_to_float(value) for name, value in metrics.items()}, step=step, **metadata)
