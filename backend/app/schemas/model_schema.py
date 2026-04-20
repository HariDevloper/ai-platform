from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ModelCreate(BaseModel):
    name: str
    framework: str
    type: str
    file_path: str


class ModelRead(BaseModel):
    id: int
    name: str
    framework: str
    type: str
    file_path: str
    created_at: datetime

    model_config = {"from_attributes": True}
