"""Data loading and submission helpers for the mosquito contest."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import csv

import numpy as np


@dataclass(frozen=True)
class ContestData:
    train_ids: np.ndarray
    train_x: np.ndarray
    train_y: np.ndarray
    test_ids: np.ndarray
    test_x: np.ndarray
    sample_submission_path: Path


def load_contest_data(
    data_root: str | Path,
    cache_dir: str | Path | None = None,
    limit_train: int | None = None,
    limit_test: int | None = None,
    refresh_cache: bool = False,
) -> ContestData:
    """Load contest CSV folders into dense numpy arrays.

    The full dataset is only about 10k x 11 x 3, but 20k small CSV reads are slow on
    WSL-mounted drives. A compressed cache keeps repeated experiments tolerable.
    """

    root = Path(data_root)
    cache_path = _cache_path(cache_dir, limit_train=limit_train, limit_test=limit_test)
    if cache_path and cache_path.exists() and not refresh_cache:
        loaded = np.load(cache_path, allow_pickle=False)
        return ContestData(
            train_ids=loaded["train_ids"],
            train_x=loaded["train_x"],
            train_y=loaded["train_y"],
            test_ids=loaded["test_ids"],
            test_x=loaded["test_x"],
            sample_submission_path=root / "sample_submission.csv",
        )

    labels = _read_labels(root / "train_labels.csv")
    train_ids = list(labels.keys())
    test_ids = _read_submission_ids(root / "sample_submission.csv")
    if limit_train is not None:
        train_ids = train_ids[:limit_train]
    if limit_test is not None:
        test_ids = test_ids[:limit_test]

    train_x = np.stack([_read_xyz(root / "train" / f"{sample_id}.csv") for sample_id in train_ids])
    train_y = np.stack([labels[sample_id] for sample_id in train_ids])
    test_x = np.stack([_read_xyz(root / "test" / f"{sample_id}.csv") for sample_id in test_ids])

    data = ContestData(
        train_ids=np.asarray(train_ids),
        train_x=train_x.astype(np.float32),
        train_y=train_y.astype(np.float32),
        test_ids=np.asarray(test_ids),
        test_x=test_x.astype(np.float32),
        sample_submission_path=root / "sample_submission.csv",
    )
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            cache_path,
            train_ids=data.train_ids,
            train_x=data.train_x,
            train_y=data.train_y,
            test_ids=data.test_ids,
            test_x=data.test_x,
        )
    return data


def write_submission(
    path: str | Path,
    sample_ids: Iterable[str],
    predictions: np.ndarray,
) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "x", "y", "z"])
        for sample_id, xyz in zip(sample_ids, predictions):
            writer.writerow([sample_id, f"{xyz[0]:.9f}", f"{xyz[1]:.9f}", f"{xyz[2]:.9f}"])
    return out


def _cache_path(
    cache_dir: str | Path | None,
    limit_train: int | None,
    limit_test: int | None,
) -> Path | None:
    if cache_dir is None:
        return None
    suffix = f"train{limit_train or 'all'}_test{limit_test or 'all'}"
    return Path(cache_dir) / f"mosquito_arrays_{suffix}.npz"


def _read_xyz(path: Path) -> np.ndarray:
    data = np.loadtxt(path, delimiter=",", skiprows=1, usecols=(1, 2, 3), dtype=np.float32)
    if data.shape != (11, 3):
        raise ValueError(f"{path} expected shape (11, 3), got {data.shape}")
    return data


def _read_labels(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return {
            row["id"]: np.asarray([float(row["x"]), float(row["y"]), float(row["z"])], dtype=np.float32)
            for row in csv.DictReader(f)
        }


def _read_submission_ids(path: Path) -> list[str]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return [row["id"] for row in csv.DictReader(f)]
