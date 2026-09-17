# Plant Disease AI – Plant Disease Prediction & Smart Recommendation System

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-v4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Final-Year Laboratory Capstone / ROSP Laboratory Presentation Project**  
> *"Detect Early. Treat Smart. Grow Better."*

---

## 1. Project Overview

**Plant Disease AI** is a real working end-to-end agricultural machine learning web application that diagnoses foliar diseases across three economic crops (**Strawberry**, **Rice**, and **Tomato**).

Unlike superficial UI mockups or black-box classifiers, this system incorporates:
1. **Transfer-Learning CNN Classification** (MobileNetV3-Large / EfficientNetB0).
2. **Deterministic OpenCV Severity Estimation** (quantitative leaf lesion surface ratio via HSV color-space segmentation).
3. **Decoupled Agronomic Recommendation Engine** (zero AI hallucination of chemical dosages or fungicides).
4. **Strict Academic Rigor** (held-out test split isolation, zero data leakage, and real confusion matrix evaluation).

---

## 2. Problem Statement & Objectives

### Problem Statement
Foliar diseases destroy up to 40% of global agricultural harvest annually. Traditional manual field scouting is labor-intensive, geographically limited, and prone to misdiagnosis. Furthermore, existing AI prototypes often hallucinate dangerous chemical dosages or evaluate models on contaminated training splits.

### Key Objectives
- Accurately detect 13 distinct pathological foliar conditions across Strawberry, Rice, and Tomato.
- Eliminate model hallucination by separating neural classification from verified agronomic knowledge bases.
- Quantitatively compute leaf disease severity into clinical tiers (*Healthy*, *Mild*, *Moderate*, *Severe*) using computer vision contour analysis.
- Provide practical treatment, fertilizer, irrigation, and prevention advice for farmers and agricultural extension officers.
- Deliver an academic-grade defense codebase with reproducible training, real confusion matrices, and OpenAPI-compliant REST services.

---

## 3. Supported Crops & Disease Classes Taxonomy

The model supports **13 classes** across 3 high-impact agricultural crops:

| Crop | Class Identifier | Pathology / Scientific Name | Pathogen Vector |
| :--- | :--- | :--- | :--- |
| **Strawberry** | `strawberry_healthy` | Healthy Strawberry Leaf | None |
| | `strawberry_leaf_scorch` | Leaf Scorch (*Diplocarpon earlianum*) | Fungus |
| **Rice** | `rice_healthy` | Healthy Rice Leaf | None |
| | `rice_bacterial_leaf_blight` | Bacterial Leaf Blight (*Xanthomonas oryzae*) | Bacterium |
| | `rice_brown_spot` | Brown Spot (*Bipolaris oryzae*) | Fungus |
| | `rice_leaf_smut` | Leaf Smut (*Entyloma oryzae*) | Fungus |
| **Tomato** | `tomato_healthy` | Healthy Tomato Leaf | None |
| | `tomato_bacterial_spot` | Bacterial Spot (*Xanthomonas spp.*) | Bacterium |
| | `tomato_early_blight` | Early Blight (*Alternaria solani*) | Fungus |
| | `tomato_late_blight` | Late Blight (*Phytophthora infestans*) | Oomycete |
| | `tomato_septoria_leaf_spot` | Septoria Leaf Spot (*Septoria lycopersici*) | Fungus |
| | `tomato_yellow_leaf_curl` | Yellow Leaf Curl Virus (TYLCV) | Virus (*Bemisia tabaci*) |
| | `tomato_mosaic_virus` | Tomato Mosaic Virus (ToMV) | Virus (Mechanical contact) |

---

## 4. System Architecture

```
[User Browser (React + Vite)]
        │  (HTTP Multipart Upload: Image + Crop Hint)
        ▼
[FastAPI REST Backend]
        ├──> [Validation Service] (MIME, Magic Bytes, File Size, Noise Filter)
        │
        ├──> [ML Inference Service]
        │       ├── Preprocess (224x224, ImageNet Normalization)
        │       └── MobileNetV3-Large Backbone ──> Softmax Probabilities
        │
        ├──> [Severity Service (OpenCV)]
        │       ├── HSV Masking: Leaf Canopy Area (A_leaf)
        │       ├── Lesion Masking: Necrotic & Chlorotic Area (A_lesion)
        │       └── Ratio = (A_lesion / A_leaf) * 100% ──> [Healthy, Mild, Moderate, Severe]
        │
        └──> [Recommendation Engine]
                ├── Structured Agronomic Knowledge Base (JSON Rules Engine)
                └── Deterministic Mapping ──> Treatments, Fertilizers, Irrigation, Prevention
        │
        ▼
[Structured Diagnostic Health Report JSON]
```

---

## 5. Machine Learning Methodology

### Convolutional Backbone
- **Architecture**: `MobileNetV3-Large` pretrained on ImageNet-1k (~3.2M parameters).
- **Inference Latency**: < 60ms on standard CPUs.
- **Classification Head**:
  ```python
  x = GlobalAveragePooling2D()(base_features)
  x = BatchNormalization()(x)
  x = Dense(256, activation='relu', kernel_regularizer=l2(1e-4))(x)
  x = Dropout(0.35)(x)
  outputs = Dense(13, activation='softmax', dtype='float32')(x)
  ```

### Two-Stage Transfer Learning
1. **Stage 1 (Warmup)**: Backbone is frozen; train the dense classification head with Adam ($\eta = 10^{-3}$) for initial feature adaptation.
2. **Stage 2 (Fine-Tuning)**: Unfreeze the top 40 convolutional layers of the backbone; train with a lower learning rate ($\eta = 5 \times 10^{-5}$) using Cosine Decay.
3. **Class Balancing**: Sklearn `compute_class_weight` calculates balanced loss multipliers per class to eliminate frequency bias.
4. **Regularization & Callbacks**:
   - `ModelCheckpoint` saving optimal weights on minimum `val_loss`.
   - `EarlyStopping` (patience=5).
   - `ReduceLROnPlateau` (factor=0.2, patience=2).

---

## 6. Deterministic OpenCV Severity Quantification

Rather than guessing disease severity, the system deterministically analyzes pixels:
1. **Leaf Area Extraction**: Image is converted to HSV; a color threshold `H:[12, 95], S:[30, 255], V:[30, 250]` isolates leaf canopy ($A_{leaf}$).
2. **Lesion Area Extraction**: Targeted masks for necrotic brown (`H:[5, 24]`), chlorotic yellow halos (`H:[20, 36]`), and dark black sori ($A_{lesion}$).
3. **Severity Calculation**:
   $$\text{Lesion Ratio} = \left(\frac{A_{lesion}}{A_{leaf}}\right) \times 100\%$$
4. **Clinical Grading**:
   - **Healthy**: $0\%$ lesion area.
   - **Mild**: $< 10\%$ surface coverage.
   - **Moderate**: $10\% - 30\%$ surface coverage.
   - **Severe**: $> 30\%$ systemic foliage blighting.

---

## 7. Decoupled Agronomic Knowledge Base

The recommendation engine strictly accesses verified records stored in `knowledge_base/<crop>_diseases.json`:
- **Symptoms**: Visible pathology markers.
- **Causes**: Optimal temperature, humidity, and vectors.
- **Severity Rules**: Action thresholds.
- **Treatment**: Tiered into **Organic** (*Bacillus subtilis*, copper octanoate, neem) and **Chemical Protectants** (Chlorothalonil, Mancozeb, Propiconazole).
- **Fertilizer Guidance**: N-P-K adjustments, nitrogen suppression during fungal pressure, and silica/calcium replenishment.
- **Irrigation Advice**: Subsurface drip irrigation timing, foliage dry-down, and prevention of waterlogging.
- **Sanitation**: Tool sterilization, host-free intervals, and infected leaf roguing.

---

## 8. Installation & Setup Guide

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Node.js v18+ and npm

### 1. Clone & Set Up Python Environment
```powershell
# Navigate to project root
cd Plant-Disease-AI

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install backend & ML dependencies
pip install -r backend/requirements.txt
```

### 2. Set Up React Frontend
```powershell
# Navigate to frontend directory
cd frontend

# Install Node modules
npm install
```

---

## 9. How to Run the Application

### Start the FastAPI Backend
```powershell
# From project root
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```
- API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

### Start the React Frontend
```powershell
# In a separate terminal
cd frontend
npm run dev
```
- Web Application: [http://localhost:5173](http://localhost:5173)

---

## 10. How to Audit, Train, and Evaluate the Model

### Step 1: Audit Dataset and Generate Stratified Splits
```powershell
.\.venv\Scripts\python ml/dataset_analysis/analyze_dataset.py --data_dir data/raw --split
```

### Step 2: Train Transfer Learning Model
```powershell
.\.venv\Scripts\python ml/training/train.py --split_dir data/split --batch_size 16 --warmup_epochs 4 --finetune_epochs 6
```

### Step 3: Evaluate Model on Isolated Test Set
```powershell
.\.venv\Scripts\python ml/evaluation/evaluate.py
```
This automatically outputs:
- Real Accuracy, Precision, Recall, and F1-Score.
- Normalized confusion matrix heatmap (`ml/models/confusion_matrix.png`).
- Loss and accuracy convergence curves (`ml/models/training_curves.png`).
- Metrics JSON (`ml/models/evaluation_results.json`) displayed in the frontend About page.

---

## 11. API Documentation

### `POST /api/predict` (or `/predict`)
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: Leaf image file (`image/jpeg`, `image/png`, `image/webp`).
  - `crop` *(optional)*: `'strawberry'`, `'rice'`, or `'tomato'`.
- **Response**:
```json
{
  "crop": "Tomato",
  "disease": "Early Blight",
  "confidence": 0.9412,
  "severity": "Moderate",
  "description": "Characterized by distinctive target-board concentric circular rings...",
  "treatment": [
    "[Organic] Foliar applications of copper hydroxide...",
    "[Chemical Protectant] Apply Chlorothalonil or Mancozeb..."
  ],
  "fertilizer": [
    "Maintain adequate nitrogen and potassium; plants deficient in N or K are dramatically more susceptible."
  ],
  "irrigation": [
    "Drip irrigation strictly; eliminate water contact with foliage."
  ],
  "prevention": [
    "Plant early-blight tolerant cultivars; prune bottom 12-18 inches of leaves."
  ],
  "severity_details": {
    "level": "Moderate",
    "lesion_percentage": 18.4,
    "lesion_pixels": 4210,
    "leaf_pixels": 22880
  },
  "top_predictions": [
    { "class_name": "tomato_early_blight", "crop": "Tomato", "disease": "Early Blight", "confidence": 0.9412 },
    { "class_name": "tomato_septoria_leaf_spot", "crop": "Tomato", "disease": "Septoria Leaf Spot", "confidence": 0.0410 }
  ]
}
```

### `GET /api/health`
- Verifies backend server health and model weights loaded state.

### `GET /api/diseases`
- Returns entire encyclopedic knowledge base across all supported crops.

### `GET /api/evaluation`
- Returns verified metrics from held-out test split evaluation.

---

## 12. Assumptions & Limitations
- **Illumination Sensitivity**: Overexposed specular reflection or deep shadows may affect color thresholding in the OpenCV severity estimator.
- **Single-Leaf Focus**: Images should capture a single representative leaf rather than an entire canopy.
- **Regulatory Compliance**: Chemical recommendations cite standard active ingredients; local agricultural regulations must be verified prior to field application.

---

## 13. Future Scope
- Integration with edge drone imagery for aerial canopy multispectral analysis.
- Multi-lingual translation support for regional agricultural dialects.
- Weather API integration to forecast fungal spore dispersal conditions based on humidity and temperature.
