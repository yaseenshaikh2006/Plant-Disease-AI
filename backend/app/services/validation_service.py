"""
Image Validation Service
Validates file headers, MIME types, dimensions, integrity, and non-botanical edge cases.
Never exposes internal server paths.
"""

import io
from typing import Tuple
from PIL import Image
import numpy as np
import cv2

from app.core.config import (
    MAX_FILE_SIZE,
    ALLOWED_MIME_TYPES,
    ALLOWED_EXTENSIONS,
    MIN_IMAGE_DIM,
    MAX_IMAGE_DIM,
)


class ImageValidationError(Exception):
    """Custom exception for image validation failures with safe user-facing message."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def validate_image_file(file_bytes: bytes, filename: str, content_type: str) -> Tuple[np.ndarray, Image.Image]:
    """
    Validates uploaded raw file bytes.
    Returns (cv2_rgb_image, pil_image) if valid.
    Raises ImageValidationError on invalid input.
    """
    # 1. Size check
    if not file_bytes or len(file_bytes) == 0:
        raise ImageValidationError("The uploaded file is empty (0 bytes). Please upload a valid image.")

    if len(file_bytes) > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE // (1024 * 1024)
        raise ImageValidationError(f"File size exceeds the {max_mb}MB limit. Please upload a smaller image.")

    # 2. Extension check
    if filename:
        ext = "." + filename.split(".")[-1].lower() if "." in filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            allowed = ", ".join(ALLOWED_EXTENSIONS)
            raise ImageValidationError(f"Unsupported file extension '{ext}'. Allowed formats: {allowed}.")

    # 3. MIME type check
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        allowed_mimes = ", ".join(ALLOWED_MIME_TYPES)
        raise ImageValidationError(f"Unsupported MIME type '{content_type}'. Allowed types: {allowed_mimes}.")

    # 4. Integrity and PIL open check
    try:
        pil_img = Image.open(io.BytesIO(file_bytes))
        pil_img.verify()  # Validate file header integrity
    except Exception:
        raise ImageValidationError("The uploaded file is corrupted or not a valid readable image.")

    # Re-open after verify() to load decoded pixels
    try:
        pil_img = Image.open(io.BytesIO(file_bytes))
        pil_img = pil_img.convert("RGB")
    except Exception:
        raise ImageValidationError("Failed to decode image pixels into RGB format.")

    # 5. Dimension checks
    width, height = pil_img.size
    if width < MIN_IMAGE_DIM or height < MIN_IMAGE_DIM:
        raise ImageValidationError(
            f"Image resolution ({width}x{height}) is too small. Minimum required is {MIN_IMAGE_DIM}x{MIN_IMAGE_DIM} pixels."
        )

    if width > MAX_IMAGE_DIM or height > MAX_IMAGE_DIM:
        raise ImageValidationError(
            f"Image resolution ({width}x{height}) exceeds maximum supported dimensions ({MAX_IMAGE_DIM}x{MAX_IMAGE_DIM} pixels)."
        )

    # Convert to OpenCV RGB numpy array
    np_img = np.array(pil_img)

    # 6. Blank / Monochromatic / Pure Noise Image Detection
    std_dev = np.std(np_img)
    if std_dev < 5.0:
        raise ImageValidationError(
            "Uploaded image appears blank or uniform. Please upload a clear photograph of a plant leaf."
        )

    return np_img, pil_img
