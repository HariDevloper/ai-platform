from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: T | Dict[str, Any] | List[Any]
    message: str
    error: Optional[str] = None


class ModelRead(BaseModel):
    id: int
    name: str
    path: str
    framework: str
    model_type: str
    size: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetRead(BaseModel):
    id: int
    name: str
    path: str
    data_type: str
    size: int
    rows_samples: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EvaluationCreate(BaseModel):
    model_id: int
    dataset_id: int
    metrics: List[str] = Field(default_factory=list)
    enable_bias_detection: bool = True
    enable_explainability: bool = True
    enable_robustness: bool = True


class EvaluationRead(BaseModel):
    id: int
    model_id: int
    dataset_id: int
    status: str
    progress: float
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class RobustnessRequest(BaseModel):
    evaluation_id: int
    strength: float = Field(default=0.1, ge=0.0, le=1.0)
    attack_type: Optional[str] = "fgsm"
