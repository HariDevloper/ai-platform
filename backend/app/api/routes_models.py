from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, Header, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.model_schema import ModelRead
from app.services.model_service import ModelService
from app.utils.file_handler import FileHandler

router = APIRouter(prefix="/models", tags=["models"])


@router.post("/upload", response_model=ModelRead)
def upload_model(
    name: str = Form(...),
    framework: str = Form(...),
    type: str = Form(...),
    file: UploadFile = File(...),
    content_length: int | None = Header(default=None),
    db: Session = Depends(get_db),
) -> ModelRead:
    FileHandler.validate_file_size(content_length)
    allowed = {".pt", ".pth", ".h5", ".keras", ".zip", ".json"}
    path = FileHandler.save_upload_file(file, settings.models_dir, allowed)

    service = ModelService(db)
    model = service.create(name=name, framework=framework, model_type=type, file_path=path)
    return ModelRead.model_validate(model)
