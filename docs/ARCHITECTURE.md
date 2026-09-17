# Technical Architecture Specification
## Plant Disease AI – Plant Disease Prediction & Smart Recommendation System

---

### 1. System Overview
Plant Disease AI is an academic machine learning web application that combines transfer-learning computer vision with deterministic agronomic heuristics to provide leaf diagnosis, lesion severity quantification, and treatment planning across **Strawberry**, **Rice**, and **Tomato**.

---

### 2. High-Level Data Flow

```
[User Browser: React + Vite]
        │  (HTTP Multipart Form: Image + Crop Hint)
        ▼
[FastAPI REST Gateway]
        │
        ├──> [Validation Service] (MIME, Magic Bytes, Dimensions, Noise Filter)
        │
        ├──> [ML Inference Service]
        │       ├── Preprocess: Resize (224x224), ImageNet Scaling
        │       └── Backbone (MobileNetV3-Large / EfficientNetB0) -> Softmax Probabilities
        │
        ├──> [Severity Service (OpenCV)]
        │       ├── HSV Masking: Green Foliage Segment A_leaf
        │       ├── Lesion Masking: Necrotic/Chlorotic Pixels A_lesion
        │       └── Ratio = (A_lesion / A_leaf) * 100% -> Grading (Mild/Mod/Severe)
        │
        └──> [Recommendation Engine]
                ├── Decoupled JSON Agronomic Knowledge Base
                └── Maps Class + Severity -> Curated Treatments, Fertilizers, Irrigation
        │
        ▼
[Structured Health Report JSON Response]
```

---

### 3. Subsystem Breakdown

#### A. Frontend Tier (React + Vite + Tailwind CSS)
- **Home**: Project mission, supported crops, technology overview.
- **Disease Detection**: File drag-and-drop, camera upload, crop selector, demo benchmarks.
- **Diagnosis Dashboard**: Circular visual confidence gauge, severity status indicator, tabbed treatments (organic vs chemical), fertilizer guidelines, irrigation instructions, prevention checklist.
- **Disease Encyclopedia**: Searchable and filterable database of 13 disease classes with etiology and symptoms.
- **About Project**: Academic defense page presenting the 2-stage transfer learning methodology, held-out test split isolation, and real confusion matrix.

#### B. API Tier (FastAPI)
- **POST `/predict`**: Core diagnostic endpoint accepting leaf files and returning structured JSON reports.
- **GET `/health`**: Returns operational status, model availability, and supported crop taxonomy.
- **GET `/crops`**: Metadata on supported agricultural crops.
- **GET `/diseases`**: Full agronomic knowledge base catalog.
- **GET `/evaluation`**: Verified held-out test set evaluation metrics.

#### C. Machine Learning & Vision Tier
- **Backbone**: MobileNetV3-Large pretrained on ImageNet.
- **Classification Head**: GlobalAveragePooling2D + BatchNorm + Dense(256, ReLU, L2 reg) + Dropout(0.35) + Softmax(13).
- **Training**: Two-stage transfer learning with early stopping, learning rate reduction on plateau, and class weighting to eliminate class imbalance bias.
- **Severity Quantification**: HSV color space segmentation measuring necrotic surface ratios.

#### D. Agronomic Knowledge Base
- Fully decoupled from neural network weights to guarantee zero hallucination of chemicals, fungicides, or fertilizers.
- Curated across peer-reviewed plant pathology literature and university agricultural extension guides (Penn State, IRRI, UC Davis IPM).
