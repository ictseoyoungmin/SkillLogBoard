"""Optional ensembling for already strong candidate predictions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from contest_mosquito.metrics import metric_summary


def run_optional_ensemble(
    candidate_paths: list[str],
    true_y: np.ndarray,
    min_single_score: float,
    min_submission_score: float,
    min_gain: float,
    seed: int,
    trials: int = 4000,
) -> dict[str, Any]:
    candidates = [_load_candidate(path) for path in candidate_paths]
    if not candidates:
        return {"status": "skipped", "reason": "no candidate_paths configured"}
    oofs = np.stack([item["oof_pred"] for item in candidates])
    tests = np.stack([item["test_pred"] for item in candidates])
    single_scores = [metric_summary(pred, true_y, prefix="val")["val/r_hit@1cm"] for pred in oofs]
    best_single = float(max(single_scores))
    if best_single < min_single_score:
        return {
            "status": "skipped",
            "reason": f"best single {best_single:.4f} < {min_single_score:.4f}",
            "best_single_score": best_single,
        }

    rng = np.random.default_rng(seed)
    best = {"score": best_single, "weights": np.eye(len(candidates))[int(np.argmax(single_scores))]}
    for _ in range(max(1, trials)):
        weights = rng.dirichlet(np.ones(len(candidates)))
        pred = np.einsum("m,mnc->nc", weights, oofs)
        score = metric_summary(pred, true_y, prefix="val")["val/r_hit@1cm"]
        if score > best["score"]:
            best = {"score": float(score), "weights": weights}
    gain = float(best["score"] - best_single)
    if best["score"] < min_submission_score or gain < min_gain:
        return {
            "status": "skipped",
            "reason": "ensemble did not clear submission score/gain gate",
            "best_single_score": best_single,
            "ensemble_score": best["score"],
            "gain": gain,
            "weights": np.asarray(best["weights"]).tolist(),
        }
    weights = np.asarray(best["weights"])
    return {
        "status": "ready",
        "best_single_score": best_single,
        "ensemble_score": best["score"],
        "gain": gain,
        "weights": weights.tolist(),
        "oof_pred": np.einsum("m,mnc->nc", weights, oofs),
        "test_pred": np.einsum("m,mnc->nc", weights, tests),
        "candidate_paths": candidate_paths,
    }


def _load_candidate(path: str) -> dict[str, np.ndarray]:
    with np.load(Path(path), allow_pickle=False) as data:
        return {"oof_pred": data["oof_pred"], "test_pred": data["test_pred"]}
