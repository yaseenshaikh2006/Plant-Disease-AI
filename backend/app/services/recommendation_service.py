"""
Agronomic Recommendation Service

Maps the trained model's class IDs to the existing crop knowledge bases.

Important:
- Recommendations are retrieved only from the local knowledge base.
- No treatment or dosage is invented when a knowledge-base record is missing.
- The current trained model contains 13 classes.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from app.core.config import KNOWLEDGE_BASE_DIR, SUPPORTED_CROPS


class RecommendationEngine:
    """
    Loads crop disease knowledge bases and provides deterministic
    recommendations for model predictions.
    """

    # Exact mapping:
    # trained model class ID -> knowledge-base class ID
    CLASS_TO_KB_MAPPING = {
        # Rice
        "Bacterialblight": "rice_bacterial_leaf_blight",
        "Brownspot": "rice_brown_spot",

        # These two model classes currently have no KB records.
        "Blast": None,
        "Tungro": None,

        # Strawberry
        "Strawberry___healthy": "strawberry_healthy",
        "Strawberry___Leaf_scorch": "strawberry_leaf_scorch",

        # Tomato
        "Tomato___healthy": "tomato_healthy",
        "Tomato___Bacterial_spot": "tomato_bacterial_spot",
        "Tomato___Early_blight": "tomato_early_blight",
        "Tomato___Late_blight": "tomato_late_blight",
        "Tomato___Septoria_leaf_spot": "tomato_septoria_leaf_spot",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "tomato_yellow_leaf_curl",
        "Tomato___Tomato_mosaic_virus": "tomato_mosaic_virus",
    }

    def __init__(self, kb_dir: Path = KNOWLEDGE_BASE_DIR):
        self.kb_dir = kb_dir
        self.kb_data: Dict[str, Dict[str, Any]] = {}

        self._load_knowledge_bases()

    # ---------------------------------------------------------
    # LOAD KNOWLEDGE BASES
    # ---------------------------------------------------------

    def _load_knowledge_bases(self) -> None:
        """Load all available crop knowledge-base JSON files."""

        for crop in SUPPORTED_CROPS:
            kb_file = self.kb_dir / f"{crop}_diseases.json"

            if not kb_file.exists():
                print(f"[WARNING] Knowledge base not found: {kb_file}")
                continue

            try:
                with open(kb_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, dict):
                    self.kb_data[crop.lower()] = data
                    print(
                        f"[INFO] Loaded {len(data)} knowledge-base records "
                        f"for {crop}"
                    )
                else:
                    print(
                        f"[ERROR] Invalid knowledge-base format: {kb_file}"
                    )

            except json.JSONDecodeError as e:
                print(
                    f"[ERROR] Invalid JSON in knowledge base "
                    f"{kb_file}: {e}"
                )

            except Exception as e:
                print(
                    f"[ERROR] Failed to load knowledge base "
                    f"{kb_file}: {e}"
                )

    # ---------------------------------------------------------
    # MODEL CLASS -> KB CLASS
    # ---------------------------------------------------------

    def _get_kb_class_id(self, model_class_id: str) -> Optional[str]:
        """
        Convert the trained model's class ID into the corresponding
        knowledge-base class ID.

        Returns None when no knowledge-base record exists.
        """

        if model_class_id in self.CLASS_TO_KB_MAPPING:
            return self.CLASS_TO_KB_MAPPING[model_class_id]

        return None

    # ---------------------------------------------------------
    # CROP DETECTION
    # ---------------------------------------------------------

    def _get_crop_from_class(self, class_id: str) -> str:
        """Determine crop name from the trained model class ID."""

        if class_id.startswith("Strawberry___"):
            return "Strawberry"

        if class_id.startswith("Tomato___"):
            return "Tomato"

        if class_id in {
            "Bacterialblight",
            "Blast",
            "Brownspot",
            "Tungro",
        }:
            return "Rice"

        return "Unknown"

    # ---------------------------------------------------------
    # DISEASE DISPLAY NAME
    # ---------------------------------------------------------

    def _get_disease_name(self, class_id: str) -> str:
        """Convert model class ID into a human-readable disease name."""

        display_names = {
            "Bacterialblight": "Bacterial Leaf Blight",
            "Blast": "Blast",
            "Brownspot": "Brown Spot",
            "Tungro": "Tungro",

            "Strawberry___healthy": "Healthy",
            "Strawberry___Leaf_scorch": "Leaf Scorch",

            "Tomato___healthy": "Healthy",
            "Tomato___Bacterial_spot": "Bacterial Spot",
            "Tomato___Early_blight": "Early Blight",
            "Tomato___Late_blight": "Late Blight",
            "Tomato___Septoria_leaf_spot": "Septoria Leaf Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus": (
                "Yellow Leaf Curl Virus"
            ),
            "Tomato___Tomato_mosaic_virus": "Tomato Mosaic Virus",
        }

        return display_names.get(
            class_id,
            class_id.replace("___", " ").replace("_", " ").title()
        )

    # ---------------------------------------------------------
    # GET DISEASE INFORMATION
    # ---------------------------------------------------------

    def get_disease_info(
        self,
        class_id: str,
        crop_hint: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve the exact knowledge-base record corresponding
        to the model class ID.

        No fuzzy matching is used because fuzzy matching can return
        the wrong disease record.
        """

        kb_class_id = self._get_kb_class_id(class_id)

        if not kb_class_id:
            return None

        # Determine crop from the model class first.
        model_crop = self._get_crop_from_class(class_id).lower()

        # If model crop exists in loaded KB, use it.
        if model_crop in self.kb_data:
            record = self.kb_data[model_crop].get(kb_class_id)

            if record:
                return record

        # Optional crop hint fallback.
        if crop_hint:
            crop_key = crop_hint.lower().strip()

            if crop_key in self.kb_data:
                record = self.kb_data[crop_key].get(kb_class_id)

                if record:
                    return record

        return None

    # ---------------------------------------------------------
    # SAFE MISSING-KB RESPONSE
    # ---------------------------------------------------------

    def _missing_knowledge_base_response(
        self,
        class_id: str,
        severity_level: str
    ) -> Dict[str, Any]:
        """
        Safe response when a disease has no knowledge-base record.

        IMPORTANT:
        No treatment, chemical dosage, fertilizer prescription,
        or irrigation prescription is invented here.
        """

        crop_name = self._get_crop_from_class(class_id)
        disease_name = self._get_disease_name(class_id)

        return {
            "crop": crop_name,
            "disease": disease_name,
            "pathogen": "Knowledge-base information unavailable",
            "description": (
                f"The model detected {disease_name} in {crop_name}. "
                "A detailed agronomic recommendation for this disease "
                "is not currently available in the local knowledge base."
            ),
            "symptoms": [],
            "causes": [],
            "treatment": [
                "Detailed treatment recommendation is currently unavailable."
            ],
            "fertilizer": [
                "No disease-specific fertilizer recommendation is currently available."
            ],
            "irrigation": [
                "No disease-specific irrigation recommendation is currently available."
            ],
            "prevention": [
                "Consult a qualified agricultural expert for disease-specific management."
            ],
            "recovery_tips": [
                "Continue monitoring the affected crop and obtain "
                "crop-specific expert guidance."
            ],
            "knowledge_base_available": False,
            "knowledge_base_class_id": None,
            "severity": severity_level,
        }

    # ---------------------------------------------------------
    # MAIN RECOMMENDATION FUNCTION
    # ---------------------------------------------------------

    def get_recommendations_for_prediction(
        self,
        class_id: str,
        severity_level: str = "Mild",
        crop_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build the recommendation payload for a model prediction.
        """

        record = self.get_disease_info(
            class_id=class_id,
            crop_hint=crop_hint
        )

        # No KB record -> safe response
        if record is None:
            return self._missing_knowledge_base_response(
                class_id=class_id,
                severity_level=severity_level
            )

        treatment_dict = record.get("treatment", {})

        organic_list = treatment_dict.get("organic", [])
        chemical_list = treatment_dict.get("chemical", [])

        # Ensure lists are actually lists.
        if not isinstance(organic_list, list):
            organic_list = []

        if not isinstance(chemical_list, list):
            chemical_list = []

        severity = severity_level.lower().strip()

        # Healthy plants
        if severity == "healthy":
            if organic_list:
                combined_treatment = organic_list
            else:
                combined_treatment = [
                    "No disease-specific curative treatment required."
                ]

        # Severe disease
        elif severity == "severe":
            combined_treatment = (
                [f"[Priority Action] {item}" for item in chemical_list]
                + [f"[Cultural Care] {item}" for item in organic_list]
            )

        # Mild / Moderate
        else:
            combined_treatment = (
                [f"[Organic] {item}" for item in organic_list]
                + [f"[Chemical Protectant] {item}" for item in chemical_list]
            )

        return {
            "crop": record.get(
                "crop",
                self._get_crop_from_class(class_id)
            ),

            "disease": record.get(
                "disease",
                self._get_disease_name(class_id)
            ),

            "pathogen": record.get("pathogen", ""),

            "description": record.get("description", ""),

            "symptoms": record.get("symptoms", []),

            "causes": record.get("causes", []),

            "treatment": combined_treatment,

            "fertilizer": record.get("fertilizer", []),

            "irrigation": record.get("irrigation", []),

            "prevention": record.get("prevention", []),

            "recovery_tips": record.get("recovery_tips", []),

            "knowledge_base_available": True,

            "knowledge_base_class_id": (
                self._get_kb_class_id(class_id)
            ),

            "severity": severity_level,
        }

    # ---------------------------------------------------------
    # DISEASE CATALOG
    # ---------------------------------------------------------

    def get_all_diseases(self) -> List[Dict[str, Any]]:
        """
        Return all diseases currently available in the
        knowledge bases.
        """

        catalog: List[Dict[str, Any]] = []

        for crop, diseases in self.kb_data.items():

            for key, data in diseases.items():

                catalog.append({
                    "class_id": key,

                    "crop": data.get(
                        "crop",
                        crop.capitalize()
                    ),

                    "disease": data.get(
                        "disease",
                        key
                    ),

                    "pathogen": data.get(
                        "pathogen",
                        "N/A"
                    ),

                    "description": data.get(
                        "description",
                        ""
                    ),

                    "symptoms": data.get(
                        "symptoms",
                        []
                    ),

                    "causes": data.get(
                        "causes",
                        []
                    ),

                    "treatment": data.get(
                        "treatment",
                        {}
                    ),

                    "fertilizer": data.get(
                        "fertilizer",
                        []
                    ),

                    "irrigation": data.get(
                        "irrigation",
                        []
                    ),

                    "prevention": data.get(
                        "prevention",
                        []
                    ),

                    "recovery_tips": data.get(
                        "recovery_tips",
                        []
                    ),
                })

        return catalog


# -------------------------------------------------------------
# SINGLETON
# -------------------------------------------------------------

recommendation_engine = RecommendationEngine()