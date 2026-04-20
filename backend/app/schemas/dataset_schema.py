from __future__ import annotations

from pydantic import BaseModel


class DatasetCreate(BaseModel):
    name: str
    type: str
    path: str


class DatasetRead(BaseModel):
    id: int
    name: str
    type: str
    path: str

    model_config = {"from_attributes": True}
