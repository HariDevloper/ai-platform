from __future__ import annotations

from typing import Any, Callable

import numpy as np


Predictor = Callable[[Any], dict[str, list[Any]]]


def evaluate_robustness(features: Any, predictor: Predictor, baseline_metric: float) -> dict[str, float]:
    data = np.asarray(features)
    if not np.issubdtype(data.dtype, np.number):
        return {"degradation": 0.0}

    noise = np.random.normal(0, 0.01, data.shape)
    noisy = data + noise
    noisy_output = predictor(noisy.tolist())
    noisy_preds = noisy_output.get("predictions", [])
    noisy_score = float(np.mean(noisy_preds)) if noisy_preds else 0.0

    degradation = max(0.0, baseline_metric - noisy_score)
    return {"degradation": float(degradation)}
