import csv
from itertools import islice
from pathlib import Path
from typing import Any
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from backend.utils.exceptions import AppException


async def save_upload_file(file: UploadFile, destination_dir: Path, allowed_extensions: set[str]) -> Path:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in allowed_extensions:
        raise AppException(f"Unsupported file type: {suffix}", status_code=400)

    filename = f"{uuid4().hex}{suffix}"
    destination = destination_dir / filename

    await file.seek(0)
    async with aiofiles.open(destination, "wb") as out_file:
        while chunk := await file.read(1024 * 1024):
            await out_file.write(chunk)

    await file.seek(0)
    return destination


def build_dataset_preview(path: Path, data_type: str, limit: int = 5) -> dict[str, Any]:
    if not path.exists():
        raise AppException("Dataset file not found", status_code=404)

    suffix = path.suffix.lower()
    if data_type == "tabular" or suffix == ".csv":
        with path.open("r", encoding="utf-8", errors="ignore") as file:
            reader = csv.reader(file)
            rows = list(islice(reader, limit))
        return {"type": "tabular", "rows": rows}

    if data_type == "text" or suffix in {".txt", ".json"}:
        with path.open("r", encoding="utf-8", errors="ignore") as file:
            lines = [line.strip() for line in islice(file, limit)]
        return {"type": "text", "lines": lines}

    return {
        "type": "image",
        "file": path.name,
        "size": path.stat().st_size,
    }
