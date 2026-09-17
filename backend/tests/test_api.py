"""
FastAPI Integration Tests
Verifies /health, /crops, /diseases, /evaluation, and /predict input validation & response schema.
"""

import io
from PIL import Image
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert "Strawberry" in data["supported_crops"]
    assert "Rice" in data["supported_crops"]
    assert "Tomato" in data["supported_crops"]


def test_crops_endpoint():
    response = client.get("/api/crops")
    assert response.status_code == 200
    data = response.json()
    crops = [c["id"] for c in data["crops"]]
    assert "strawberry" in crops
    assert "rice" in crops
    assert "tomato" in crops


def test_diseases_endpoint():
    response = client.get("/api/diseases")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 13
    assert len(data["diseases"]) >= 13


def test_evaluation_endpoint():
    response = client.get("/api/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "available"
    assert "metrics" in data
    assert "overall_accuracy" in data["metrics"]


def test_predict_invalid_extension():
    fake_file = io.BytesIO(b"Hello world PDF content")
    response = client.post(
        "/predict",
        files={"file": ("test.pdf", fake_file, "application/pdf")}
    )
    assert response.status_code == 400
    assert "Unsupported" in response.json()["detail"]


def test_predict_valid_leaf_image():
    # Create valid synthetic RGB leaf test image
    img = Image.new("RGB", (256, 256), color=(40, 140, 45))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    response = client.post(
        "/predict",
        files={"file": ("leaf.jpg", buf, "image/jpeg")},
        data={"crop": "tomato"}
    )
    assert response.status_code == 200
    data = response.json()
    # Check all required fields from user prompt
    assert "crop" in data
    assert "disease" in data
    assert "confidence" in data
    assert "severity" in data
    assert "description" in data
    assert isinstance(data["treatment"], list)
    assert isinstance(data["fertilizer"], list)
    assert isinstance(data["irrigation"], list)
    assert isinstance(data["prevention"], list)
    assert 0.0 <= data["confidence"] <= 1.0
