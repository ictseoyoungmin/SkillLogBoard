from pathlib import Path

import numpy as np

from contest_mosquito.data import load_contest_data, write_submission
from contest_mosquito.metrics import r_hit
from contest_mosquito.models import evaluate_physics
from contest_mosquito.physics import physics_anchor_bank, predict_physics


ROOT = Path(__file__).resolve().parents[1]


def test_loader_shapes_small_sample():
    data = load_contest_data(
        ROOT / "data",
        cache_dir=ROOT / "results" / "cache",
        limit_train=20,
        limit_test=20,
    )
    assert data.train_x.shape == (20, 11, 3)
    assert data.train_y.shape == (20, 3)
    assert data.test_x.shape == (20, 11, 3)


def test_r_hit_contest_radius():
    true = np.zeros((2, 3))
    pred = np.asarray([[0.01, 0.0, 0.0], [0.011, 0.0, 0.0]])
    assert r_hit(pred, true) == 0.5


def test_physics_baseline_is_nontrivial():
    data = load_contest_data(ROOT / "data", cache_dir=ROOT / "results" / "cache", limit_train=200, limit_test=20)
    result = evaluate_physics(data.train_x, data.train_y, data.test_x, method="cv_last1")
    assert result.metrics["val/r_hit@1cm"] > 0.45
    assert result.test_pred.shape == (20, 3)


def test_reference_physics_anchor_bank_contains_ca_last_beta():
    data = load_contest_data(ROOT / "data", cache_dir=ROOT / "results" / "cache", limit_train=20, limit_test=20)
    anchors, names = physics_anchor_bank(data.train_x)
    idx = names.index("ca_last_beta_0.25")
    direct = predict_physics(data.train_x, method="ca_last_beta_0.25")
    assert anchors.shape[0] == 20
    assert anchors.shape[2] == 3
    np.testing.assert_allclose(anchors[:, idx, :], direct, atol=1e-7)


def test_submission_writer_columns(tmp_path):
    out = write_submission(tmp_path / "submission.csv", ["TEST_00001"], np.asarray([[1.0, 2.0, 3.0]]))
    assert out.read_text(encoding="utf-8").splitlines()[0] == "id,x,y,z"
