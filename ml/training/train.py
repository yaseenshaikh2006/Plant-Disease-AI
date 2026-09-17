"""
Transfer Learning Training Pipeline
Plant Disease AI – Plant Disease Prediction & Smart Recommendation System

Two-Stage Training:
- Stage 1: Feature Extraction (Backbone frozen, train dense classification head)
- Stage 2: Fine-Tuning (Unfreeze top layers of backbone, train with low learning rate)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Tuple

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import tensorflow as tf
from tensorflow.keras import layers, models, regularizers, optimizers

from ml.preprocessing.dataloader import get_data_generators, compute_dataset_class_weights
from ml.training.callbacks import get_training_callbacks


def build_model(
    num_classes: int,
    input_shape=(224, 224, 3),
    dropout_rate: float = 0.35,
    dense_units: int = 256,
    l2_reg: float = 1e-4,
    backbone_type: str = "MobileNetV3Large"
) -> Tuple[tf.keras.Model, tf.keras.Model]:
    """
    Constructs transfer learning model with ImageNet backbone and custom classification head.
    Returns (full_model, base_backbone).
    """
    if backbone_type == "EfficientNetB0":
        base_model = tf.keras.applications.EfficientNetB0(
            include_top=False,
            weights="imagenet",
            input_shape=input_shape
        )
    else:
        # Default to MobileNetV3Large (optimized for CPU/GPU mobile performance)
        base_model = tf.keras.applications.MobileNetV3Large(
            include_top=False,
            weights="imagenet",
            input_shape=input_shape,
            minimalistic=False
        )

    # Freeze base model for initial warm-up training phase
    base_model.trainable = False

    inputs = tf.keras.Input(shape=input_shape, name="input_leaf_image")
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.BatchNormalization(name="head_batch_norm")(x)
    x = layers.Dense(
        dense_units,
        activation="relu",
        kernel_regularizer=regularizers.l2(l2_reg),
        name="dense_feature_layer"
    )(x)
    x = layers.Dropout(dropout_rate, name="head_dropout")(x)
    outputs = layers.Dense(
        num_classes,
        activation="softmax",
        dtype="float32",
        name="disease_predictions"
    )(x)

    model = models.Model(inputs=inputs, outputs=outputs, name=f"PlantDisease_{backbone_type}")
    return model, base_model


def train_pipeline(
    split_dir: str = "data/split",
    output_model_path: str = "ml/models/best_model.keras",
    class_indices_path: str = "ml/models/class_indices.json",
    csv_log_path: str = "ml/models/training_log.csv",
    batch_size: int = 16,
    warmup_epochs: int = 8,
    finetune_epochs: int = 15,
    unfreeze_layers: int = 40,
    backbone: str = "MobileNetV3Large"
):
    split_path = Path(split_dir)
    model_path = Path(output_model_path)
    indices_path = Path(class_indices_path)
    csv_path = Path(csv_log_path)

    print("=" * 70)
    print("PLANT DISEASE AI – TRANSFER LEARNING TRAINING")
    print(f"Backbone: {backbone} | Batch Size: {batch_size}")
    print("=" * 70)

    # 1. Load Data Generators
    train_gen, val_gen, test_gen, class_indices = get_data_generators(
        split_dir=split_path,
        target_size=(224, 224),
        batch_size=batch_size
    )

    num_classes = len(class_indices)
    print(f"[INFO] Discovered {num_classes} classes across crops:")
    for cls_name, idx in sorted(class_indices.items(), key=lambda x: x[1]):
        print(f"  [{idx}] {cls_name}")

    # Save class indices for inference mapping
    indices_path.parent.mkdir(parents=True, exist_ok=True)
    with open(indices_path, "w") as f:
        json.dump(class_indices, f, indent=2)
    print(f"[INFO] Saved class indices map to: {indices_path}")

    # Compute class weights to counteract imbalance
    class_weights = compute_dataset_class_weights(train_gen)

    # 2. Build Model
    model, base_model = build_model(
        num_classes=num_classes,
        input_shape=(224, 224, 3),
        backbone_type=backbone
    )

    # 3. Stage 1: Warmup Training (Frozen Backbone)
    print("\n" + "=" * 50)
    print("STAGE 1: FEATURE EXTRACTION (Backbone Frozen)")
    print("=" * 50)

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")]
    )

    callbacks = get_training_callbacks(
        checkpoint_path=model_path,
        csv_log_path=csv_path,
        early_stopping_patience=5,
        reduce_lr_patience=2
    )

    history_warmup = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=warmup_epochs,
        callbacks=callbacks,
        class_weight=class_weights
    )

    # 4. Stage 2: Fine-Tuning Phase (Unfreeze top layers)
    print("\n" + "=" * 50)
    print(f"STAGE 2: FINE-TUNING (Unfreezing top {unfreeze_layers} layers)")
    print("=" * 50)

    base_model.trainable = True
    # Freeze all layers except the last `unfreeze_layers`
    for layer in base_model.layers[:-unfreeze_layers]:
        layer.trainable = False

    trainable_count = sum(len(layer.trainable_variables) for layer in model.layers)
    print(f"[INFO] Fine-tuning active. Trainable variable count: {trainable_count}")

    # Recompile with very low learning rate for gentle weight adjustments
    model.compile(
        optimizer=optimizers.Adam(learning_rate=5e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")]
    )

    # Continue training from current epoch
    initial_epoch = len(history_warmup.history["loss"])
    total_epochs = initial_epoch + finetune_epochs

    history_finetune = model.fit(
        train_gen,
        validation_data=val_gen,
        initial_epoch=initial_epoch,
        epochs=total_epochs,
        callbacks=callbacks,
        class_weight=class_weights
    )

    print("\n[SUCCESS] Model training complete.")
    print(f"[SUCCESS] Optimal model saved to: {model_path.resolve()}")
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plant Disease AI Model Training")
    parser.add_argument("--split_dir", type=str, default="data/split", help="Path to split data")
    parser.add_argument("--output_model", type=str, default="ml/models/best_model.keras", help="Target model path")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--warmup_epochs", type=int, default=8, help="Warmup epochs")
    parser.add_argument("--finetune_epochs", type=int, default=15, help="Fine-tuning epochs")
    parser.add_argument("--backbone", type=str, default="MobileNetV3Large", help="Backbone CNN architecture")
    args = parser.parse_args()

    train_pipeline(
        split_dir=args.split_dir,
        output_model_path=args.output_model,
        batch_size=args.batch_size,
        warmup_epochs=args.warmup_epochs,
        finetune_epochs=args.finetune_epochs,
        backbone=args.backbone
    )
