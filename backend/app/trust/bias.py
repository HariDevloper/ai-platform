from __future__ import annotations

from typing import Any

import numpy as np


def compute_group_fairness(y_pred: list[Any], groups: list[Any] | None = None) -> dict[str, float]:
    if not groups or len(groups) != len(y_pred):
        return {"demographic_parity_gap": 0.0}

    preds = np.asarray(y_pred)
    group_arr = np.asarray(groups)
    rates: list[float] = []
    for group in np.unique(group_arr):
        mask = group_arr == group
        if mask.any():
            rates.append(float(np.mean(preds[mask])))

    if not rates:
        return {"demographic_parity_gap": 0.0}

    return {"demographic_parity_gap": float(max(rates) - min(rates))}
