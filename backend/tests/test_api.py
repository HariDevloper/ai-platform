import io
import time
from pathlib import Path

from fastapi.testclient import TestClient

from backend.config import DATASETS_UPLOAD_DIR, MODELS_UPLOAD_DIR
from backend.database import Base, engine
from backend.main import app

client = TestClient(app)
MAX_STATUS_POLLS = 40


def setup_function() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    for folder in (MODELS_UPLOAD_DIR, DATASETS_UPLOAD_DIR):
        for file_path in folder.glob("*"):
            if file_path.is_file():
                file_path.unlink()


def test_health_endpoint_response_format():
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert "data" in payload
    assert "message" in payload


def test_model_and_dataset_upload_and_list():
    model_response = client.post(
        "/api/models/upload",
        data={"name": "demo-model", "framework": "pytorch", "model_type": "classification"},
        files={"file": ("model.pt", io.BytesIO(b"weights"), "application/octet-stream")},
    )
    assert model_response.status_code == 200
    assert model_response.json()["data"]["name"] == "demo-model"

    dataset_response = client.post(
        "/api/datasets/upload",
        data={"name": "demo-dataset", "dataset_type": "tabular"},
        files={"file": ("data.csv", io.BytesIO(b"a,b\n1,2\n3,4\n"), "text/csv")},
    )
    assert dataset_response.status_code == 200
    assert dataset_response.json()["data"]["name"] == "demo-dataset"

    models_list = client.get("/api/models")
    datasets_list = client.get("/api/datasets")

    assert models_list.status_code == 200
    assert datasets_list.status_code == 200
    assert len(models_list.json()["data"]) == 1
    assert len(datasets_list.json()["data"]) == 1


def test_evaluation_status_and_results_flow():
    model_id = client.post(
        "/api/models/upload",
        data={"name": "model", "framework": "pytorch", "model_type": "classification"},
        files={"file": ("model.pt", io.BytesIO(b"weights"), "application/octet-stream")},
    ).json()["data"]["id"]

    dataset_id = client.post(
        "/api/datasets/upload",
        data={"name": "dataset", "dataset_type": "tabular"},
        files={"file": ("data.csv", io.BytesIO(b"x,y\n1,0\n"), "text/csv")},
    ).json()["data"]["id"]

    evaluation = client.post(
        "/api/evaluations/create",
        json={
            "model_id": model_id,
            "dataset_id": dataset_id,
            "metrics": ["accuracy"],
            "enable_bias_detection": True,
            "enable_explainability": True,
            "enable_robustness": True,
        },
    )
    assert evaluation.status_code == 200
    evaluation_id = evaluation.json()["data"]["id"]

    for _ in range(MAX_STATUS_POLLS):
        status = client.get(f"/api/evaluations/{evaluation_id}/status")
        assert status.status_code == 200
        if status.json()["data"]["status"] == "completed":
            break
        time.sleep(0.25)
    assert status.json()["data"]["status"] == "completed", "Evaluation did not complete in time"

    results = client.get(f"/api/evaluations/{evaluation_id}/results")
    assert results.status_code == 200
    assert results.json()["success"] is True
    assert "metrics_data" in results.json()["data"]
