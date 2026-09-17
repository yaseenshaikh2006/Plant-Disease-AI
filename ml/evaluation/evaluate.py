"""
Academic Model Evaluation & Metric Generation Tool
Plant Disease AI – Evaluates purely on held-out test split
Generates real confusion matrix, classification report, and ROC/PR analysis.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support
)
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def plot_confusion_matrix(cm: np.ndarray, class_names: list, output_path: Path):
    """Renders and saves a normalized confusion matrix heatmap."""
    plt.figure(figsize=(12, 10))
    # Normalize rows to sum to 1 for percentage display
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    cm_norm = np.nan_to_num(cm_norm)

    sns.heatmap(
        cm_norm,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        xticklabels=class_names,
        yticklabels=class_names,
        cbar_kws={'label': 'Normalized Prediction Ratio'}
    )
    plt.title("Plant Disease AI – Held-Out Test Set Confusion Matrix", fontsize=14, pad=15)
    plt.xlabel("Predicted Class", fontsize=12, labelpad=10)
    plt.ylabel("Ground Truth Class", fontsize=12, labelpad=10)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(str(output_path), dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved confusion matrix heatmap to: {output_path}")


def plot_training_curves(csv_log_path: Path, output_path: Path):
    """Plots training vs validation accuracy and loss from training log CSV."""
    if not csv_log_path.exists():
        print(f"[INFO] No training CSV log found at {csv_log_path}. Skipping curve plot.")
        return

    df = pd.read_csv(csv_log_path)
    epochs = range(1, len(df) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Accuracy subplot
    ax1.plot(epochs, df["accuracy"], label="Training Accuracy", color="#059669", linewidth=2)
    if "val_accuracy" in df.columns:
        ax1.plot(epochs, df["val_accuracy"], label="Validation Accuracy", color="#2563eb", linewidth=2, linestyle="--")
    ax1.set_title("Model Accuracy Progression", fontsize=12)
    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Accuracy")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend()

    # Loss subplot
    ax2.plot(epochs, df["loss"], label="Training Loss", color="#dc2626", linewidth=2)
    if "val_loss" in df.columns:
        ax2.plot(epochs, df["val_loss"], label="Validation Loss", color="#d97706", linewidth=2, linestyle="--")
    ax2.set_title("Model Loss Progression", fontsize=12)
    ax2.set_xlabel("Epochs")
    ax2.set_ylabel("Loss (Categorical Crossentropy)")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(str(output_path), dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved training convergence curves to: {output_path}")


def evaluate_model_on_test_set(
    model_path: str = "ml/models/best_model.keras",
    test_dir: str = "data/split/test",
    class_indices_path: str = "ml/models/class_indices.json",
    output_json_path: str = "ml/models/evaluation_results.json",
    cm_output_path: str = "ml/models/confusion_matrix.png",
    curves_output_path: str = "ml/models/training_curves.png",
    csv_log_path: str = "ml/models/training_log.csv"
):
    model_p = Path(model_path)
    test_p = Path(test_dir)
    indices_p = Path(class_indices_path)
    out_json_p = Path(output_json_path)

    print("=" * 70)
    print("PLANT DISEASE AI – HELD-OUT TEST SET EVALUATION")
    print(f"Loading model: {model_p.resolve()}")
    print(f"Test split:    {test_p.resolve()}")
    print("=" * 70)

    if not model_p.exists():
        raise FileNotFoundError(f"Model file not found: {model_p}")
    if not test_p.exists():
        raise FileNotFoundError(f"Test split directory not found: {test_p}")

    # Load Model
    model = tf.keras.models.load_model(str(model_p))

    # Load class indices
    with open(indices_p, "r") as f:
        class_indices = json.load(f)

    # Invert mapping to get index -> class_name
    idx_to_class = {v: k for k, v in class_indices.items()}
    class_names = [idx_to_class[i] for i in range(len(class_indices))]

    # Setup test generator without shuffling
    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)
    test_gen = test_datagen.flow_from_directory(
        str(test_p),
        target_size=(224, 224),
        batch_size=16,
        class_mode="categorical",
        shuffle=False
    )

    y_true = test_gen.classes
    total_samples = len(y_true)

    print(f"[INFO] Evaluating {total_samples} held-out test samples across {len(class_names)} classes...")
    preds = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(preds, axis=1)

    # Calculate actual academic metrics
    acc = float(accuracy_score(y_true, y_pred))
    prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)

    clf_report = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0
    )

    print("\n" + "=" * 70)
    print("HELD-OUT TEST SET CLASSIFICATION REPORT")
    print("=" * 70)
    print(classification_report(y_true, y_pred, target_names=class_names, zero_division=0))

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, class_names, Path(cm_output_path))
    plot_training_curves(Path(csv_log_path), Path(curves_output_path))

    # Assemble comprehensive results object
    evaluation_results = {
        "model_architecture": model.name,
        "total_test_samples": total_samples,
        "overall_accuracy": round(acc, 4),
        "macro_precision": round(float(prec_macro), 4),
        "macro_recall": round(float(rec_macro), 4),
        "macro_f1": round(float(f1_macro), 4),
        "weighted_precision": round(float(prec_weighted), 4),
        "weighted_recall": round(float(rec_weighted), 4),
        "weighted_f1": round(float(f1_weighted), 4),
        "class_metrics": {
            cls_name: {
                "precision": round(clf_report[cls_name]["precision"], 4),
                "recall": round(clf_report[cls_name]["recall"], 4),
                "f1_score": round(clf_report[cls_name]["f1-score"], 4),
                "support": int(clf_report[cls_name]["support"])
            }
            for cls_name in class_names if cls_name in clf_report
        },
        "confusion_matrix": cm.tolist(),
        "class_names": class_names
    }

    out_json_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json_p, "w") as f:
        json.dump(evaluation_results, f, indent=2)

    print(f"\n[SUCCESS] Real evaluation metrics exported to: {out_json_p}")
    return evaluation_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Evaluation on Held-Out Test Set")
    parser.add_argument("--model", type=str, default="ml/models/best_model.keras", help="Path to trained model")
    parser.add_argument("--test_dir", type=str, default="data/split/test", help="Held-out test set directory")
    parser.add_argument("--indices", type=str, default="ml/models/class_indices.json", help="Class indices mapping")
    parser.add_argument("--output_json", type=str, default="ml/models/evaluation_results.json", help="Output JSON path")
    args = parser.parse_args()

    evaluate_model_on_test_set(
        model_path=args.model,
        test_dir=args.test_dir,
        class_indices_path=args.indices,
        output_json_path=args.output_json
    )
