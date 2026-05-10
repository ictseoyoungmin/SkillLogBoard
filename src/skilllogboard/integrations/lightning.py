"""Optional Lightning callback skeleton.

This module should import lightning lazily or live behind optional extras.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any, Callable

from skilllogboard.integrations.pytorch import scalar_to_float


def require_lightning(importer: Callable[[str], Any] = import_module) -> Any:
    for module_name in ("lightning.pytorch", "pytorch_lightning"):
        try:
            return importer(module_name)
        except ImportError:
            continue
    raise ImportError(
        "Lightning callback support requires the optional dependency 'lightning' "
        "or 'pytorch_lightning'. Install it separately to use this integration."
    )


def lightning_available(importer: Callable[[str], Any] = import_module) -> bool:
    try:
        require_lightning(importer)
    except ImportError:
        return False
    return True


def create_lightning_callback(logger: Any, importer: Callable[[str], Any] = import_module) -> Any:
    lightning = require_lightning(importer)
    callback_base = getattr(lightning, "Callback", object)

    class SkillLogBoardCallback(callback_base):
        def on_validation_epoch_end(self, trainer: Any, pl_module: Any) -> None:
            metrics = getattr(trainer, "callback_metrics", {}) or {}
            step = getattr(trainer, "global_step", None)
            numeric = {}
            for name, value in metrics.items():
                try:
                    numeric[str(name)] = scalar_to_float(value)
                except (TypeError, ValueError):
                    continue
            if numeric:
                logger.log_metrics(numeric, step=step, integration="lightning")

    return SkillLogBoardCallback()
