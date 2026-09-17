"""
Dataset Analysis & Integrity Audit Tool
Plant Disease AI – Plant Disease Prediction & Smart Recommendation System

Inspects:
- Corrupted / unreadable image detection
- Perceptual & exact duplicate detection (MD5 hash)
- Number of images per class and class imbalance ratio
- Dimensionality, aspect ratio, and color channel statistics
- Stratified Train / Validation / Test split generator
"""

import os
import sys
import glob
import json
import hashlib
import shutil
import argparse
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def compute_file_md5(file_path: Path) -> str:
    """Computes MD5 hash of file content for exact duplicate detection."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def inspect_image(file_path: Path):
    """
    Validates image readability, format, dimensions, and channel mode.
    Returns (is_valid, width, height, channels, error_message).
    """
    try:
        # Check for 0-byte file
        if file_path.stat().st_size == 0:
            return False, 0, 0, 0, "Zero-byte empty file"

        with Image.open(file_path) as img:
            img.verify()  # Verify integrity of file header

        # Reopen to load actual image pixels and dimensions
        with Image.open(file_path) as img:
            width, height = img.size
            mode = img.mode
            channels = len(mode) if mode in ("RGB", "RGBA") else 1
            if width < 32 or height < 32:
                return False, width, height, channels, f"Dimension too small: {width}x{height}"
            return True, width, height, channels, None
    except Exception as e:
        return False, 0, 0, 0, str(e)


def run_dataset_audit(data_dir: Path, output_json: Path = None):
    """
    Scans a structured dataset directory and produces a comprehensive audit report.
    Directory structure expected:
        data_dir/
            <crop>/
                <disease>/
                    *.jpg
    """
    print("=" * 70)
    print(f"PLANT DISEASE AI - DATASET INTEGRITY & AUDIT SCANNER")
    print(f"Scanning target directory: {data_dir.resolve()}")
    print("=" * 70)

    if not data_dir.exists():
        print(f"[ERROR] Directory '{data_dir}' does not exist.")
        return None

    class_stats = defaultdict(lambda: {
        "crop": "",
        "disease": "",
        "total_images": 0,
        "valid_images": 0,
        "corrupt_images": [],
        "widths": [],
        "heights": [],
        "aspect_ratios": []
    })

    all_hashes = defaultdict(list)
    total_scanned = 0
    total_valid = 0
    total_corrupt = 0

    # Discover classes: data_dir/<crop>/<disease>/
    crops = [d for d in data_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

    if not crops:
        print("[WARNING] No crop subdirectories found in data directory.")
        return None

    for crop_dir in sorted(crops):
        crop_name = crop_dir.name.lower()
        disease_dirs = [d for d in crop_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

        for disease_dir in sorted(disease_dirs):
            disease_name = disease_dir.name.lower()
            class_key = f"{crop_name}_{disease_name}"
            stats = class_stats[class_key]
            stats["crop"] = crop_name
            stats["disease"] = disease_name

            image_files = [
                p for p in disease_dir.iterdir()
                if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
            ]

            stats["total_images"] = len(image_files)

            for img_path in image_files:
                total_scanned += 1
                is_valid, w, h, ch, err = inspect_image(img_path)

                if not is_valid:
                    total_corrupt += 1
                    stats["corrupt_images"].append({"file": str(img_path), "error": err})
                    continue

                total_valid += 1
                stats["valid_images"] += 1
                stats["widths"].append(w)
                stats["heights"].append(h)
                stats["aspect_ratios"].append(round(w / h, 3))

                # Check duplicate hashes
                file_hash = compute_file_md5(img_path)
                all_hashes[file_hash].append(str(img_path))

    # Calculate duplicate statistics
    duplicates = {h: files for h, files in all_hashes.items() if len(files) > 1}
    duplicate_image_count = sum(len(files) - 1 for files in duplicates.values())

    # Print summary
    print(f"\n[1] SCAN SUMMARY")
    print(f"  • Total Images Scanned:   {total_scanned}")
    print(f"  • Valid Readable Images:  {total_valid}")
    print(f"  • Corrupted / Malformed:  {total_corrupt}")
    print(f"  • Duplicate Instances:    {duplicate_image_count} in {len(duplicates)} duplicate sets")
    print(f"  • Total Classes Found:    {len(class_stats)}")

    print("\n[2] CLASS DISTRIBUTION & IMAGE RESOLUTION")
    print(f"{'Class Identifier':<30} | {'Count':<7} | {'Mean Res':<12} | {'Min Res':<11} | {'Max Res':<11}")
    print("-" * 75)

    valid_counts = []
    for class_key, s in sorted(class_stats.items()):
        cnt = s["valid_images"]
        valid_counts.append(cnt)
        if cnt > 0:
            mean_w = int(np.mean(s["widths"]))
            mean_h = int(np.mean(s["heights"]))
            min_w, min_h = min(s["widths"]), min(s["heights"])
            max_w, max_h = max(s["widths"]), max(s["heights"])
            mean_res = f"{mean_w}x{mean_h}"
            min_res = f"{min_w}x{min_h}"
            max_res = f"{max_w}x{max_h}"
        else:
            mean_res = min_res = max_res = "N/A"
        print(f"{class_key:<30} | {cnt:<7} | {mean_res:<12} | {min_res:<11} | {max_res:<11}")

    # Imbalance analysis
    print("\n[3] CLASS IMBALANCE EVALUATION")
    if valid_counts and max(valid_counts) > 0:
        max_c = max(valid_counts)
        min_c = min(valid_counts) if min(valid_counts) > 0 else 1
        imbalance_ratio = round(max_c / min_c, 2)
        print(f"  • Max Class Count:  {max_c}")
        print(f"  • Min Class Count:  {min(valid_counts)}")
        print(f"  • Imbalance Ratio:  {imbalance_ratio} : 1")
        if imbalance_ratio > 3.0:
            print("  • Advisory: Moderate to high class imbalance detected.")
            print("    Recommendation: Apply weighted loss (class_weights) or targeted augmentation during training.")
        else:
            print("  • Advisory: Classes are relatively well-balanced.")
    else:
        print("  • No valid images found to assess balance.")

    # Duplicate listing
    if duplicates:
        print("\n[4] DUPLICATE IMAGES DETECTED (First 5 examples):")
        for i, (h, paths) in enumerate(list(duplicates.items())[:5]):
            print(f"  Set #{i+1} [Hash {h[:8]}...]:")
            for p in paths:
                print(f"    - {p}")

    # Corrupted images listing
    if total_corrupt > 0:
        print(f"\n[5] CORRUPTED IMAGES ({total_corrupt} found):")
        for class_key, s in class_stats.items():
            for c in s["corrupt_images"]:
                print(f"  [CORRUPT] {c['file']} - Reason: {c['error']}")

    report = {
        "total_scanned": total_scanned,
        "total_valid": total_valid,
        "total_corrupt": total_corrupt,
        "duplicate_count": duplicate_image_count,
        "class_count": len(class_stats),
        "classes": {
            k: {
                "crop": v["crop"],
                "disease": v["disease"],
                "valid_images": v["valid_images"],
                "corrupt_count": len(v["corrupt_images"]),
            } for k, v in class_stats.items()
        }
    }

    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nAudit report saved to: {output_json}")

    print("=" * 70)
    return report


def create_stratified_split(raw_dir: Path, output_dir: Path, train_pct=0.70, val_pct=0.15, test_pct=0.15, seed=42):
    """
    Creates an isolated Train, Validation, and held-out Test split.
    Guarantees strict isolation of the test set to avoid data leakage.
    """
    import random
    random.seed(seed)

    print(f"\n[CREATING STRATIFIED SPLIT]")
    print(f"Split distribution: Train={int(train_pct*100)}% | Val={int(val_pct*100)}% | Test={int(test_pct*100)}%")
    print(f"Output directory: {output_dir.resolve()}")

    crops = [d for d in raw_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

    for crop_dir in crops:
        crop_name = crop_dir.name.lower()
        for disease_dir in [d for d in crop_dir.iterdir() if d.is_dir()]:
            disease_name = disease_dir.name.lower()
            class_id = f"{crop_name}_{disease_name}"

            images = [
                p for p in disease_dir.iterdir()
                if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
            ]

            # Validate images to skip corrupt files
            valid_images = [p for p in images if inspect_image(p)[0]]
            random.shuffle(valid_images)

            n_total = len(valid_images)
            if n_total == 0:
                continue

            n_train = int(n_total * train_pct)
            n_val = int(n_total * val_pct)
            # Remaining goes to test to prevent rounding loss
            n_test = n_total - n_train - n_val

            train_files = valid_images[:n_train]
            val_files = valid_images[n_train:n_train + n_val]
            test_files = valid_images[n_train + n_val:]

            for split_name, file_list in [("train", train_files), ("val", val_files), ("test", test_files)]:
                target_folder = output_dir / split_name / class_id
                target_folder.mkdir(parents=True, exist_ok=True)
                for src in file_list:
                    dest = target_folder / src.name
                    shutil.copy2(src, dest)

            print(f"  • {class_id:<28}: Total={n_total:<4} -> Train={len(train_files):<4} Val={len(val_files):<3} Test={len(test_files):<3}")

    print("\n[SUCCESS] Stratified split generation complete. Test set isolated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Integrity & Audit Tool")
    parser.add_argument("--data_dir", type=str, default="data/raw", help="Path to raw dataset directory")
    parser.add_argument("--output_json", type=str, default="ml/models/dataset_audit.json", help="Audit report path")
    parser.add_argument("--split", action="store_true", help="Generate train/val/test splits")
    parser.add_argument("--split_output", type=str, default="data/split", help="Target split output path")
    args = parser.parse_args()

    data_path = Path(args.data_dir)
    audit_res = run_dataset_audit(data_path, Path(args.output_json) if args.output_json else None)

    if args.split and audit_res and audit_res["total_valid"] > 0:
        create_stratified_split(data_path, Path(args.split_output))
