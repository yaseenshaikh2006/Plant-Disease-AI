"""
Data Loading & Preprocessing Pipeline
Plant Disease AI
"""

import os
from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def get_data_generators(
    split_dir: Path,
    target_size: Tuple[int, int] = (224, 224),
    batch_size: int = 16
) -> Tuple[Any, Any, Any, Dict[str, int]]:
    """
    Constructs ImageDataGenerators for Train, Val, and Test splits.
    Train split receives comprehensive geometric & photometric augmentation.
    Val and Test splits receive deterministic rescaling only (zero data leakage).
    """
    train_dir = split_dir / "train"
    val_dir = split_dir / "val"
    test_dir = split_dir / "test"

    # Data augmentation for training set
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=20,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.10,
        zoom_range=0.15,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode="nearest"
    )

    # Validation and Test: pure rescaling only
    eval_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    print(f"[INFO] Loading training dataset from: {train_dir}")
    train_gen = train_datagen.flow_from_directory(
        str(train_dir),
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=True
    )

    print(f"[INFO] Loading validation dataset from: {val_dir}")
    val_gen = eval_datagen.flow_from_directory(
        str(val_dir),
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=False
    )

    test_gen = None
    if test_dir.exists():
        print(f"[INFO] Loading held-out test dataset from: {test_dir}")
        test_gen = eval_datagen.flow_from_directory(
            str(test_dir),
            target_size=target_size,
            batch_size=batch_size,
            class_mode="categorical",
            shuffle=False
        )

    class_indices = train_gen.class_indices
    return train_gen, val_gen, test_gen, class_indices


def compute_dataset_class_weights(train_generator) -> Dict[int, float]:
    """
    Computes balanced class weights to offset class distribution skew.
    """
    classes = train_generator.classes
    unique_classes = np.unique(classes)
    weights = compute_class_weight(
        class_weight="balanced",
        classes=unique_classes,
        y=classes
    )
    class_weight_dict = {int(k): float(v) for k, v in zip(unique_classes, weights)}
    print(f"[INFO] Computed class balancing weights: {class_weight_dict}")
    return class_weight_dict
