from __future__ import annotations

from typing import Any

import numpy as np


def preprocess_features(features: Any) -> Any:
    array = np.asarray(features)
    if np.issubdtype(array.dtype, np.number):
        return np.nan_to_num(array).tolist()
    return features
