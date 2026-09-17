"""
FastAPI REST API Routes
Endpoints:
- POST /predict: Leaf image diagnosis, severity estimation & agronomic recommendations
- GET /health: API and model operational health check
- GET /crops: List of supported crops
- GET /diseases: Complete encyclopedia catalog
- GET /evaluation: Model performance metrics, confusion matrix & reports
"""

import json
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.config import EVALUATION_METRICS_PATH, SUPPORTED_CROPS
from app.schemas.prediction import (
    PredictionResponse,
    HealthResponse,
    SeverityDetails,
    TopPrediction
)
from app.services.validation_service import validate_image_file, ImageValidationError
from app.services.severity_service import estimate_disease_severity
from app.services.recommendation_service import recommendation_engine
from app.services.ml_service import ml_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health Check"])
async def health_check():
    """Returns system status, model availability, and supported crop taxonomy."""
    return {
        "status": "healthy",
        "service": "Plant Disease AI – Prediction & Recommendation Engine",
        "version": "1.0.0",
        "model_loaded": ml_service.is_loaded,
        "supported_crops": [c.capitalize() for c in SUPPORTED_CROPS],
        "total_classes": len(ml_service.class_indices)
    }


@router.post("/predict", response_model=PredictionResponse, tags=["Disease Diagnosis"])
async def predict_plant_disease(
    file: UploadFile = File(..., description="Uploaded leaf photograph (JPEG, PNG, WEBP)"),
    crop: Optional[str] = Form(None, description="Optional crop hint: 'strawberry', 'rice', or 'tomato'")
):
    """
    Core Diagnosis Pipeline:
    1. Validates file integrity, dimensions, and botanical plausibility
    2. Executes deep learning classification to predict crop and disease
    3. Calculates objective disease severity via OpenCV color & contour segmentation
    4. Retrieves verified agronomic recommendations from the decoupled knowledge base
    """
    try:
        file_bytes = await file.read()
        np_image, pil_image = validate_image_file(
            file_bytes=file_bytes,
            filename=file.filename or "",
            content_type=file.content_type or ""
        )
    except ImageValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to process uploaded image. Please ensure it is a valid photograph."
        )

    # Clean crop parameter
    crop_hint = crop.strip().lower() if crop and crop.strip().lower() in SUPPORTED_CROPS else None

    # Execute ML Inference
    try:
        ml_result = ml_service.predict(np_image, crop_hint=crop_hint)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Machine learning inference pipeline encountered an internal error."
        )

    class_id = ml_result["class_id"]
    predicted_crop = ml_result["crop"]
    predicted_disease = ml_result["disease"]
    confidence = ml_result["confidence"]
    is_healthy = ml_result["is_healthy"]

    # Execute Severity Estimation (OpenCV)
    severity_info = estimate_disease_severity(np_image, is_healthy=is_healthy)
    severity_level = severity_info["level"]

    # Retrieve Decoupled Recommendations from Knowledge Base
    rec = recommendation_engine.get_recommendations_for_prediction(
        class_id=class_id,
        severity_level=severity_level,
        crop_hint=predicted_crop
    )

    # Build response conforming strictly to required API schema
    return {
        "crop": predicted_crop,
        "disease": predicted_disease,
        "confidence": confidence,
        "severity": severity_level,
        "description": rec["description"],
        "treatment": rec["treatment"],
        "fertilizer": rec["fertilizer"],
        "irrigation": rec["irrigation"],
        "prevention": rec["prevention"],
        # Extended academic diagnostics
        "pathogen": rec.get("pathogen", ""),
        "symptoms": rec.get("symptoms", []),
        "causes": rec.get("causes", []),
        "recovery_tips": rec.get("recovery_tips", []),
        "severity_details": SeverityDetails(**severity_info),
        "top_predictions": [TopPrediction(**p) for p in ml_result.get("top_predictions", [])]
    }


@router.get("/crops", tags=["Taxonomy"])
async def get_supported_crops():
    """Returns list of supported agricultural crops and their taxonomy."""
    return {
        "crops": [
            {
                "id": "strawberry",
                "name": "Strawberry",
                "scientific_name": "Fragaria × ananassa",
                "family": "Rosaceae",
                "diseases_supported": ["Healthy", "Leaf Scorch"]
            },
            {
                "id": "rice",
                "name": "Rice",
                "scientific_name": "Oryza sativa",
                "family": "Poaceae",
                "diseases_supported": ["Healthy", "Bacterial Leaf Blight", "Brown Spot", "Leaf Smut"]
            },
            {
                "id": "tomato",
                "name": "Tomato",
                "scientific_name": "Solanum lycopersicum",
                "family": "Solanaceae",
                "diseases_supported": [
                    "Healthy", "Bacterial Spot", "Early Blight", "Late Blight",
                    "Septoria Leaf Spot", "Yellow Leaf Curl Virus", "Mosaic Virus"
                ]
            }
        ]
    }


@router.get("/diseases", tags=["Encyclopedia"])
async def get_disease_catalog():
    """Returns entire knowledge base encyclopedia of plant diseases."""
    catalog = recommendation_engine.get_all_diseases()
    return {"total": len(catalog), "diseases": catalog}


@router.get("/evaluation", tags=["Academic Evaluation"])
async def get_evaluation_metrics():
    """Returns actual academic evaluation metrics computed on held-out test split."""
    if not EVALUATION_METRICS_PATH.exists():
        return {
            "status": "pending_evaluation",
            "message": "Model evaluation has not yet been executed on the held-out test split."
        }

    try:
        with open(EVALUATION_METRICS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"status": "available", "metrics": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read evaluation report: {e}")
