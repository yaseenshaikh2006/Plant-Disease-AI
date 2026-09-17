# Dataset Acquisition & Organization Guide

This document provides explicit instructions for downloading, organizing, and verifying public plant disease datasets for the three supported crops: **Strawberry**, **Rice**, and **Tomato**.

---

## 1. Supported Public Datasets

### A. Strawberry & Tomato: PlantVillage Dataset
- **Description**: The gold-standard open-access plant pathology dataset developed by Penn State University and EPFL.
- **License**: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). Completely free for academic, research, and educational use.
- **Official Public Repositories**:
  - Kaggle: [PlantVillage Dataset on Kaggle](https://www.kaggle.com/datasets/emmarex/plantvillage-dataset)
  - GitHub: [PlantVillage Dataset GitHub](https://github.com/spMohanty/PlantVillage-Dataset)
  - Mendeley Data: [PlantVillage Paper Data](https://data.mendeley.com/datasets/tywbtsjrjv/1)

### B. Rice: Rice Leaf Disease Dataset
- **Description**: Public dataset containing high-resolution field photographs of rice leaf diseases collected from real paddy fields.
- **License**: Public Domain / CC0 Open Data.
- **Official Public Repositories**:
  - Kaggle: [Rice Leaf Diseases Dataset](https://www.kaggle.com/datasets/vbookshelf/rice-leaf-diseases)
  - Kaggle Alternative: [Rice Leaf Disease Images](https://www.kaggle.com/datasets/arunrk7/rice-leaf-diseases)
  - UCI Machine Learning Repository: [Rice Disease Dataset](https://archive.ics.uci.edu/)

---

## 2. Directory Layout Requirement

Organize the images inside `data/raw/` (or `dataset/`) matching this exact hierarchy:

```
data/raw/
├── strawberry/
│   ├── healthy/
│   └── leaf_scorch/
├── rice/
│   ├── healthy/
│   ├── bacterial_leaf_blight/
│   ├── brown_spot/
│   └── leaf_smut/
└── tomato/
    ├── healthy/
    ├── bacterial_spot/
    ├── early_blight/
    ├── late_blight/
    ├── septoria_leaf_spot/
    ├── yellow_leaf_curl/
    └── mosaic_virus/
```

---

## 3. Class Name Mapping Table

When extracting from original PlantVillage folder names, map them as follows:

| Crop | Original PlantVillage / Kaggle Folder Name | Target Standard Folder Name |
| :--- | :--- | :--- |
| **Strawberry** | `Strawberry___healthy` | `data/raw/strawberry/healthy` |
| **Strawberry** | `Strawberry___Leaf_scorch` | `data/raw/strawberry/leaf_scorch` |
| **Rice** | `Healthy` | `data/raw/rice/healthy` |
| **Rice** | `Bacterial leaf blight` | `data/raw/rice/bacterial_leaf_blight` |
| **Rice** | `Brown spot` | `data/raw/rice/brown_spot` |
| **Rice** | `Leaf smut` | `data/raw/rice/leaf_smut` |
| **Tomato** | `Tomato___healthy` | `data/raw/tomato/healthy` |
| **Tomato** | `Tomato___Bacterial_spot` | `data/raw/tomato/bacterial_spot` |
| **Tomato** | `Tomato___Early_blight` | `data/raw/tomato/early_blight` |
| **Tomato** | `Tomato___Late_blight` | `data/raw/tomato/late_blight` |
| **Tomato** | `Tomato___Septoria_leaf_spot` | `data/raw/tomato/septoria_leaf_spot` |
| **Tomato** | `Tomato___Tomato_Yellow_Leaf_Curl_Virus` | `data/raw/tomato/yellow_leaf_curl` |
| **Tomato** | `Tomato___Tomato_mosaic_virus` | `data/raw/tomato/mosaic_virus` |

---

## 4. How to Inspect and Prepare the Dataset

Run the automated dataset analysis script:
```powershell
.\.venv\Scripts\python ml/dataset_analysis/analyze_dataset.py --data_dir data/raw
```

The script will automatically:
1. Scan for corrupt, non-readable, or 0-byte images and report them.
2. Check image dimensions and aspect ratios.
3. Compute exact class distributions and detect class imbalance.
4. Detect duplicate images via MD5 and perceptual hashing.
5. Create stratified Train (70%), Validation (15%), and held-out Test (15%) splits in `data/split/`.
