"""
Deep Learning Inference Service
Plant Disease AI
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import numpy as np
import cv2

from app.core.config import (
    MODEL_WEIGHTS_PATH,
    CLASS_INDICES_PATH,
    INPUT_IMAGE_SIZE,
    MIN_CONFIDENCE_THRESHOLD,
    SUPPORTED_CROPS,
)


class ModelInferenceService:
    """
    Handles loading the trained Plant Disease AI model
    and performing image-based disease prediction.
    """

    def __init__(self):
        self.model = None
        self.class_indices: Dict[str, int] = {}
        self.idx_to_class: Dict[int, str] = {}
        self.is_loaded = False

        self._load_model_artifacts()

    # ---------------------------------------------------------
    # MODEL LOADING
    # ---------------------------------------------------------

    def _load_model_artifacts(self):
        """Load class mapping and trained Keras model."""

        # Load class mapping
        if CLASS_INDICES_PATH.exists():
            try:
                with open(CLASS_INDICES_PATH, "r", encoding="utf-8") as f:
                    self.class_indices = json.load(f)

                self.idx_to_class = {
                    int(index): class_name
                    for class_name, index in self.class_indices.items()
                }

                print(
                    f"[INFO] Loaded {len(self.class_indices)} "
                    f"class mappings from {CLASS_INDICES_PATH.name}"
                )

            except Exception as e:
                print(f"[ERROR] Failed to load class indices: {e}")

        else:
            print(
                f"[WARNING] Class indices file not found: "
                f"{CLASS_INDICES_PATH.resolve()}"
            )

        # Load trained model
        if MODEL_WEIGHTS_PATH.exists():
            try:
                import tensorflow as tf

                self.model = tf.keras.models.load_model(
                    str(MODEL_WEIGHTS_PATH)
                )

                self.is_loaded = True

                print(
                    f"[INFO] Successfully loaded deep learning model "
                    f"from {MODEL_WEIGHTS_PATH.name}"
                )

                print(
                    f"[INFO] Model input shape: "
                    f"{self.model.input_shape}"
                )

                print(
                    f"[INFO] Model output shape: "
                    f"{self.model.output_shape}"
                )

            except Exception as e:
                print(
                    f"[ERROR] Failed to load trained Keras model: {e}"
                )

        else:
            print(
                f"[ERROR] Trained model not found at "
                f"{MODEL_WEIGHTS_PATH.resolve()}"
            )

    # ---------------------------------------------------------
    # IMAGE PREPROCESSING
    # ---------------------------------------------------------

    def preprocess_image(self, image_rgb: np.ndarray) -> np.ndarray:
        """
        Resize image for MobileNetV3Large.

        IMPORTANT:
        The trained model uses:
            include_preprocessing=True

        Therefore the image MUST remain in the [0, 255] range.
        Do NOT divide by 255 here.

        Output:
            Shape: (1, 224, 224, 3)
            dtype: float32
            range: approximately [0, 255]
        """

        resized = cv2.resize(
            image_rgb,
            INPUT_IMAGE_SIZE,
            interpolation=cv2.INTER_AREA,
        )

        image_array = resized.astype(np.float32)

        return np.expand_dims(image_array, axis=0)

    # ---------------------------------------------------------
    # CROP DETECTION
    # ---------------------------------------------------------

    @staticmethod
    def _get_class_crop(class_id: str) -> str:
        """
        Extract crop name from the actual dataset class naming.

        Examples:
            Strawberry___Leaf_scorch -> strawberry
            Tomato___Early_blight -> tomato
            Bacterialblight -> rice
            Blast -> rice
            Brownspot -> rice
            Tungro -> rice
        """

        normalized = class_id.lower()

        if normalized.startswith("strawberry___"):
            return "strawberry"

        if normalized.startswith("tomato___"):
            return "tomato"

        # Rice dataset classes do not contain "Rice___"
        rice_classes = {
            "bacterialblight",
            "blast",
            "brownspot",
            "tungro",
        }

        if normalized in rice_classes:
            return "rice"

        return "unknown"

    # ---------------------------------------------------------
    # PREDICTION
    # ---------------------------------------------------------

    def predict(
        self,
        image_rgb: np.ndarray,
        crop_hint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute disease prediction.

        Args:
            image_rgb:
                RGB image as NumPy array.

            crop_hint:
                Optional user-selected crop:
                strawberry / rice / tomato

        Returns:
            Prediction dictionary containing:
                class_id
                crop
                disease
                confidence
                is_healthy
                top_predictions
        """

        if not self.is_loaded or self.model is None:
            raise RuntimeError(
                "Model weights are not currently loaded. "
                "Please place best_model.keras inside ml/models/."
            )

        # -----------------------------------------------------
        # PREPROCESS
        # -----------------------------------------------------

        processed_input = self.preprocess_image(image_rgb)

        # -----------------------------------------------------
        # MODEL PREDICTION
        # -----------------------------------------------------

        raw_probs = self.model.predict(
            processed_input,
            verbose=0,
        )[0]

        raw_probs = np.asarray(raw_probs, dtype=np.float32)

        # Safety normalization
        probability_sum = np.sum(raw_probs)

        if probability_sum > 0:
            raw_probs = raw_probs / probability_sum

        effective_probs = raw_probs.copy()

        # -----------------------------------------------------
        # CROP FILTERING
        # -----------------------------------------------------

        selected_crop = None

        if crop_hint:
            selected_crop = crop_hint.strip().lower()

        if selected_crop in {"strawberry", "rice", "tomato"}:

            matching_indices = []

            for idx, class_id in self.idx_to_class.items():

                class_crop = self._get_class_crop(class_id)

                if class_crop == selected_crop:
                    matching_indices.append(idx)

            # Only keep classes belonging to selected crop
            if matching_indices:

                crop_probs = np.zeros_like(effective_probs)

                for idx in matching_indices:
                    crop_probs[idx] = raw_probs[idx]

                crop_probability_sum = np.sum(crop_probs)

                if crop_probability_sum > 0:
                    effective_probs = (
                        crop_probs / crop_probability_sum
                    )

        # -----------------------------------------------------
        # TOP PREDICTION
        # -----------------------------------------------------

        best_idx = int(np.argmax(effective_probs))

        best_confidence = float(effective_probs[best_idx])

        class_id = self.idx_to_class.get(
            best_idx,
            f"unknown_class_{best_idx}",
        )

        # -----------------------------------------------------
        # TOP 3 PREDICTIONS
        # -----------------------------------------------------

        sorted_indices = np.argsort(
            effective_probs
        )[::-1][:3]

        top_predictions = []

        for idx in sorted_indices:

            idx = int(idx)

            probability = float(effective_probs[idx])

            # Ignore zero-probability classes
            if probability <= 0:
                continue

            predicted_class = self.idx_to_class.get(
                idx,
                f"unknown_class_{idx}",
            )

            crop_name, disease_name = self._parse_class_id(
                predicted_class
            )

            top_predictions.append(
                {
                    "class_name": predicted_class,
                    "crop": crop_name,
                    "disease": disease_name,
                    "confidence": round(probability, 4),
                }
            )

        # -----------------------------------------------------
        # HUMAN-READABLE RESULT
        # -----------------------------------------------------

        crop_name, disease_name = self._parse_class_id(
            class_id
        )

        is_healthy = (
            "healthy" in disease_name.lower()
        )

        # -----------------------------------------------------
        # CONFIDENCE STATUS
        # -----------------------------------------------------

        confidence_status = (
            "high"
            if best_confidence >= 0.80
            else "medium"
            if best_confidence >= 0.60
            else "low"
        )

        return {
            "class_id": class_id,
            "crop": crop_name,
            "disease": disease_name,
            "confidence": round(best_confidence, 4),
            "confidence_status": confidence_status,
            "is_healthy": is_healthy,
            "top_predictions": top_predictions,
        }

    # ---------------------------------------------------------
    # CLASS NAME PARSER
    # ---------------------------------------------------------

    @classmethod
    def _parse_class_id(
        cls,
        class_id: str,
    ) -> Tuple[str, str]:
        """
        Convert dataset class name into readable crop/disease.

        Examples:

            Tomato___Early_blight
            ->
            Tomato / Early Blight

            Strawberry___Leaf_scorch
            ->
            Strawberry / Leaf Scorch

            Bacterialblight
            ->
            Rice / Bacterial Blight
        """

        normalized = class_id.strip()

        # Strawberry
        if normalized.lower().startswith(
            "strawberry___"
        ):
            disease = normalized.split(
                "___",
                1,
            )[1]

            return (
                "Strawberry",
                disease.replace("_", " ").title(),
            )

        # Tomato
        if normalized.lower().startswith(
            "tomato___"
        ):
            disease = normalized.split(
                "___",
                1,
            )[1]

            return (
                "Tomato",
                disease.replace("_", " ").title(),
            )

        # Rice
        rice_diseases = {
            "bacterialblight": "Bacterial Blight",
            "blast": "Blast",
            "brownspot": "Brown Spot",
            "tungro": "Tungro",
        }

        if normalized.lower() in rice_diseases:
            return (
                "Rice",
                rice_diseases[normalized.lower()],
            )

        # Unknown class fallback
        return (
            "Unknown Crop",
            normalized.replace("_", " ").title(),
        )


# -------------------------------------------------------------
# SINGLETON INSTANCE
# -------------------------------------------------------------

ml_service = ModelInferenceService()