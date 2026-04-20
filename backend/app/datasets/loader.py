from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class DatasetBundle:
    features: Any
    targets: list[Any]


class DatasetLoader:
    @staticmethod
    def detect_type(path: str) -> str:
        suffix = Path(path).suffix.lower()
        if suffix == ".csv":
            return "tabular"
        if suffix == ".json":
            return "text"
        return "vision"

    @staticmethod
    def load(path: str, dataset_type: str) -> DatasetBundle:
        if dataset_type == "tabular":
            df = pd.read_csv(path)
            if "target" not in df.columns:
                raise ValueError("Tabular dataset must contain a 'target' column")
            features = df.drop(columns=["target"]).fillna(0.0)
            targets = df["target"].tolist()
            return DatasetBundle(features=features.values.tolist(), targets=targets)

        if dataset_type == "text":
            data = pd.read_json(path)
            if "input" not in data.columns or "target" not in data.columns:
                raise ValueError("Text dataset must contain 'input' and 'target' fields")
            return DatasetBundle(features=data["input"].tolist(), targets=data["target"].tolist())

        raise ValueError(f"Unsupported dataset type '{dataset_type}'")
