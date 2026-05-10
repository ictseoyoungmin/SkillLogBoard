import pytest

from skilllogboard.integrations.lightning import create_lightning_callback, require_lightning
from skilllogboard.integrations.pytorch import log_torch_metrics, require_torch, scalar_to_float


def _missing_importer(name):
    raise ImportError(name)


def test_pytorch_helper_imports_without_torch_and_has_clear_error():
    with pytest.raises(ImportError, match="optional dependency 'torch'"):
        require_torch(importer=_missing_importer)


def test_scalar_to_float_accepts_plain_numbers():
    assert scalar_to_float(1) == 1.0
    assert scalar_to_float(2.5) == 2.5


def test_log_torch_metrics_uses_core_logger_protocol():
    class DummyLogger:
        def __init__(self):
            self.calls = []

        def log_metrics(self, metrics, step=None, **metadata):
            self.calls.append((metrics, step, metadata))

    logger = DummyLogger()
    log_torch_metrics(logger, {"loss": 1}, step=3, phase="train")

    assert logger.calls == [({"loss": 1.0}, 3, {"phase": "train"})]


def test_lightning_helper_imports_without_lightning_and_has_clear_error():
    with pytest.raises(ImportError, match="Lightning callback support requires"):
        require_lightning(importer=_missing_importer)


def test_lightning_callback_factory_uses_lazy_importer():
    class FakeLightning:
        class Callback:
            pass

    class DummyLogger:
        def __init__(self):
            self.logged = []

        def log_metrics(self, metrics, step=None, **metadata):
            self.logged.append((metrics, step, metadata))

    class Trainer:
        callback_metrics = {"val/loss": 0.4}
        global_step = 9

    logger = DummyLogger()
    callback = create_lightning_callback(logger, importer=lambda name: FakeLightning)
    callback.on_validation_epoch_end(Trainer(), object())

    assert logger.logged == [({"val/loss": 0.4}, 9, {"integration": "lightning"})]
