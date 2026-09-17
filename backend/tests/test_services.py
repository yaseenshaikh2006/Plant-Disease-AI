"""
Unit Tests for Plant Disease AI Backend Services
Tests image validation, OpenCV severity estimation, and decoupled recommendation retrieval.
"""

import numpy as np
import pytest
from app.services.validation_service import validate_image_file, ImageValidationError
from app.services.severity_service import estimate_disease_severity
from app.services.recommendation_service import recommendation_engine


def test_recommendation_engine_strawberry():
    rec = recommendation_engine.get_recommendations_for_prediction(
        class_id="strawberry_leaf_scorch",
        severity_level="Moderate"
    )
    assert rec["crop"] == "Strawberry"
    assert rec["disease"] == "Leaf Scorch"
    assert len(rec["treatment"]) > 0
    assert len(rec["fertilizer"]) > 0
    assert len(rec["irrigation"]) > 0
    assert len(rec["prevention"]) > 0


def test_recommendation_engine_healthy():
    rec = recommendation_engine.get_recommendations_for_prediction(
        class_id="tomato_healthy",
        severity_level="Healthy"
    )
    assert rec["crop"] == "Tomato"
    assert "Healthy" in rec["disease"]
    assert len(rec["fertilizer"]) > 0


def test_opencv_severity_estimation_healthy():
    # Green image simulating healthy leaf
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :] = [34, 139, 34]  # Forest Green
    res = estimate_disease_severity(img, is_healthy=True)
    assert res["level"] == "Healthy"
    assert res["lesion_percentage"] == 0.0


def test_opencv_severity_estimation_lesion():
    # Leaf with simulated brown necrotic spots
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :] = [40, 160, 40]  # Green leaf blade
    # Add brown necrotic patch
    img[50:150, 50:150] = [139, 69, 19]  # Saddle Brown
    res = estimate_disease_severity(img, is_healthy=False)
    assert res["level"] in ["Mild", "Moderate", "Severe"]
    assert res["lesion_percentage"] > 0.0


def test_validation_empty_bytes():
    with pytest.raises(ImageValidationError):
        validate_image_file(b"", "leaf.jpg", "image/jpeg")


def test_validation_invalid_type():
    with pytest.raises(ImageValidationError):
        validate_image_file(b"random text", "document.pdf", "application/pdf")
