from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.db_models import Model


class ModelService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, name: str, framework: str, model_type: str, file_path: str) -> Model:
        model = Model(name=name, framework=framework, type=model_type, file_path=file_path)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get(self, model_id: int) -> Model | None:
        return self.db.query(Model).filter(Model.id == model_id).first()

    def list(self, skip: int = 0, limit: int = 50) -> list[Model]:
        return self.db.query(Model).offset(skip).limit(limit).all()

    def delete(self, model_id: int) -> bool:
        model = self.get(model_id)
        if model is None:
            return False
        self.db.delete(model)
        self.db.commit()
        return True
