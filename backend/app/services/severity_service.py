"""
OpenCV Disease Severity Estimation Service
Deterministically segments leaf tissue and calculates necrotic/chlorotic lesion coverage.
"""

import cv2
import numpy as np
from typing import Dict, Any


def estimate_disease_severity(image_rgb: np.ndarray, is_healthy: bool = False) -> Dict[str, Any]:
    """
    Computes disease severity from an RGB image using computer vision contour and color segmentation.
    
    Args:
        image_rgb: Numpy array (H, W, 3) in RGB format.
        is_healthy: Boolean indicating if the model classified the leaf as healthy.
        
    Returns:
        Dict containing:
          - level: "Healthy", "Mild", "Moderate", or "Severe"
          - lesion_percentage: float (0.0 to 100.0)
          - lesion_pixels: int
          - leaf_pixels: int
    """
    if is_healthy:
        return {
            "level": "Healthy",
            "lesion_percentage": 0.0,
            "lesion_pixels": 0,
            "leaf_pixels": int(image_rgb.shape[0] * image_rgb.shape[1] * 0.5)
        }

    # Resize to standard analysis resolution for consistent computational speed
    analysis_img = cv2.resize(image_rgb, (300, 300))
    hsv = cv2.cvtColor(analysis_img, cv2.COLOR_RGB2HSV)

    # 1. Segment Total Plant Foliage (Greens, Yellow-greens, Brownish leaf tissue)
    # Exclude white/bright studio background and extreme dark edges
    lower_foliage_1 = np.array([12, 30, 30])
    upper_foliage_1 = np.array([95, 255, 250])
    leaf_mask = cv2.inRange(hsv, lower_foliage_1, upper_foliage_1)

    # Morphological cleanup of leaf mask (close gaps, remove small isolated noise)
    kernel_leaf = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_CLOSE, kernel_leaf)
    leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_OPEN, kernel_leaf)

    total_leaf_pixels = int(np.count_nonzero(leaf_mask))

    # Fallback if leaf mask segmentation is very small (e.g. extreme dark or macro shot)
    if total_leaf_pixels < 1000:
        total_leaf_pixels = analysis_img.shape[0] * analysis_img.shape[1]
        leaf_mask = np.ones((analysis_img.shape[0], analysis_img.shape[1]), dtype=np.uint8) * 255

    # 2. Segment Lesions & Necrotic Areas:
    # A. Brown / Reddish-brown necrotic tissue
    lower_brown = np.array([5, 40, 25])
    upper_brown = np.array([24, 255, 200])
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)

    # B. Chlorotic Yellow halos / spots
    lower_yellow = np.array([20, 50, 80])
    upper_yellow = np.array([36, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # C. Very dark / black necrotic sori
    gray = cv2.cvtColor(analysis_img, cv2.COLOR_RGB2GRAY)
    mask_black = cv2.inRange(gray, 0, 45)

    # Combine lesion indicators strictly within the segmented leaf mask
    combined_lesion_mask = cv2.bitwise_or(mask_brown, mask_yellow)
    combined_lesion_mask = cv2.bitwise_or(combined_lesion_mask, mask_black)
    lesion_within_leaf = cv2.bitwise_and(combined_lesion_mask, leaf_mask)

    # Morphological cleanup on lesion mask
    kernel_lesion = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    lesion_clean = cv2.morphologyEx(lesion_within_leaf, cv2.MORPH_OPEN, kernel_lesion)

    lesion_pixels = int(np.count_nonzero(lesion_clean))

    # Calculate percentage
    lesion_percentage = round((lesion_pixels / max(total_leaf_pixels, 1)) * 100.0, 2)

    # Clamp to realistic bounds (maximum 95%)
    lesion_percentage = min(lesion_percentage, 95.0)

    # Determine clinical severity grading
    if lesion_percentage < 1.0:
        level = "Mild"  # Early sub-clinical onset
    elif lesion_percentage < 10.0:
        level = "Mild"
    elif lesion_percentage <= 30.0:
        level = "Moderate"
    else:
        level = "Severe"

    return {
        "level": level,
        "lesion_percentage": lesion_percentage,
        "lesion_pixels": lesion_pixels,
        "leaf_pixels": total_leaf_pixels
    }
