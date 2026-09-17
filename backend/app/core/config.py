"""
Core Configuration Settings
Plant Disease AI
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
MODELS_DIR = BASE_DIR / "ml" / "models"
DATA_DIR = BASE_DIR / "data"

# Supported target crops
SUPPORTED_CROPS = ["strawberry", "rice", "tomato"]

# Maximum allowed file upload size in bytes (15 MB)
MAX_FILE_SIZE = 15 * 1024 * 1024

# Allowed image MIME types and extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}

# Minimum and maximum image dimensions (px)
MIN_IMAGE_DIM = 64
MAX_IMAGE_DIM = 4096

# Machine Learning model paths & parameters
MODEL_WEIGHTS_PATH = MODELS_DIR / "best_model.keras"
CLASS_INDICES_PATH = MODELS_DIR / "class_indices.json"
EVALUATION_METRICS_PATH = MODELS_DIR / "evaluation_results.json"
INPUT_IMAGE_SIZE = (224, 224)

# Minimum confidence threshold for asserting valid leaf disease
MIN_CONFIDENCE_THRESHOLD = 0.35
