from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EvaluationCreate(BaseModel):
    model_id: int
    dataset_id: int


class EvaluationRead(BaseModel):
    id: int
    model_id: int
    dataset_id: int
    metrics: dict[str, Any] | None
    trust_score: float | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
