from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


class FileHandler:
    @staticmethod
    def validate_file_size(content_length: int | None) -> None:
        if content_length and content_length > settings.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    @staticmethod
    def save_upload_file(upload: UploadFile, destination_dir: str, allowed_extensions: set[str]) -> str:
        suffix = Path(upload.filename or "").suffix.lower()
        if suffix not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file extension '{suffix}'. Allowed: {sorted(allowed_extensions)}",
            )

        safe_name = Path(upload.filename or "uploaded_file").name
        destination = Path(destination_dir).resolve()
        destination.mkdir(parents=True, exist_ok=True)
        target = destination / f"{uuid4().hex}_{safe_name}"

        with target.open("wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)

        return str(target.resolve())
