from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Model Evaluation Platform"
    app_env: str = "development"
    debug: bool = False

    database_url: str = "sqlite:///./app.db"

    storage_root: str = "backend/app/storage"
    models_dir: str = "backend/app/storage/models"
    datasets_dir: str = "backend/app/storage/datasets"
    results_dir: str = "backend/app/storage/results"

    max_upload_size_mb: int = 250
    log_level: str = "INFO"
    log_file: str = "backend/app/platform.log"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def ensure_storage_dirs(self) -> None:
        for path in (self.storage_root, self.models_dir, self.datasets_dir, self.results_dir):
            Path(path).mkdir(parents=True, exist_ok=True)


settings = Settings()
