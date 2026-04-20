from __future__ import annotations

from typing import Any

import numpy as np


def compute_feature_importance(features: Any, predictions: list[Any]) -> dict[str, float]:
    array = np.asarray(features)
    pred = np.asarray(predictions, dtype=float)
    if array.ndim != 2 or len(array) == 0:
        return {}

    scores: dict[str, float] = {}
    for i in range(array.shape[1]):
        column = array[:, i]
        if np.std(column) == 0:
            scores[f"feature_{i}"] = 0.0
            continue
        corr = np.corrcoef(column.astype(float), pred)[0, 1]
        scores[f"feature_{i}"] = float(abs(corr)) if not np.isnan(corr) else 0.0
    return scores
