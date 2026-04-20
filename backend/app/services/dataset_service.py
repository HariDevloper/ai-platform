from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.db_models import Dataset


class DatasetService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, name: str, dataset_type: str, path: str) -> Dataset:
        dataset = Dataset(name=name, type=dataset_type, path=path)
        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)
        return dataset

    def get(self, dataset_id: int) -> Dataset | None:
        return self.db.query(Dataset).filter(Dataset.id == dataset_id).first()

    def list(self, skip: int = 0, limit: int = 50) -> list[Dataset]:
        return self.db.query(Dataset).offset(skip).limit(limit).all()

    def delete(self, dataset_id: int) -> bool:
        dataset = self.get(dataset_id)
        if dataset is None:
            return False
        self.db.delete(dataset)
        self.db.commit()
        return True
