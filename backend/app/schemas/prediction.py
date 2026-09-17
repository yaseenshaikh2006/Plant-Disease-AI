"""
Pydantic Schemas for API Request & Response validation
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TopPrediction(BaseModel):
    class_name: str
    crop: str
    disease: str
    confidence: float


class SeverityDetails(BaseModel):
    level: str = Field(..., description="Severity classification: Healthy, Mild, Moderate, or Severe")
    lesion_percentage: float = Field(..., description="Calculated ratio of lesion surface area to total leaf area")
    lesion_pixels: int = Field(0, description="Pixel count of detected necrotic/chlorotic lesions")
    leaf_pixels: int = Field(0, description="Pixel count of total segmented leaf tissue")


class PredictionResponse(BaseModel):
    crop: str
    disease: str
    confidence: float
    severity: str
    description: str
    treatment: List[str]
    fertilizer: List[str]
    irrigation: List[str]
    prevention: List[str]
    # Detailed academic diagnostics
    pathogen: Optional[str] = None
    symptoms: Optional[List[str]] = []
    causes: Optional[List[str]] = []
    recovery_tips: Optional[List[str]] = []
    severity_details: Optional[SeverityDetails] = None
    top_predictions: Optional[List[TopPrediction]] = []


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    model_loaded: bool
    supported_crops: List[str]
    total_classes: int


class DiseaseSummary(BaseModel):
    class_id: str
    crop: str
    disease: str
    pathogen: str
    description: str
    symptoms: List[str]
    treatment: Dict[str, List[str]]
