from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, Header, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.dataset_schema import DatasetRead
from app.services.dataset_service import DatasetService
from app.utils.file_handler import FileHandler

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload", response_model=DatasetRead)
def upload_dataset(
    name: str = Form(...),
    type: str = Form(...),
    file: UploadFile = File(...),
    content_length: int | None = Header(default=None),
    db: Session = Depends(get_db),
) -> DatasetRead:
    FileHandler.validate_file_size(content_length)
    allowed = {".csv", ".json", ".zip", ".txt"}
    path = FileHandler.save_upload_file(file, settings.datasets_dir, allowed)

    service = DatasetService(db)
    dataset = service.create(name=name, dataset_type=type, path=path)
    return DatasetRead.model_validate(dataset)
