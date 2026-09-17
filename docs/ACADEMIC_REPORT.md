# Academic Project Report & Defense Guide
## Plant Disease AI – Plant Disease Prediction & Smart Recommendation System
**Final-Year Laboratory Capstone / ROSP Laboratory Presentation**

---

### 1. Abstract
Early identification and targeted management of botanical foliar diseases are essential for global food security and precision agriculture. This project introduces **Plant Disease AI**, an end-to-end computer vision and intelligent recommendation platform designed for three vital agricultural crops: **Strawberry** (*Fragaria × ananassa*), **Rice** (*Oryza sativa*), and **Tomato** (*Solanum lycopersicum*). The system employs a two-stage transfer-learning convolutional neural network (MobileNetV3-Large), combined with an objective OpenCV lesion area quantifier and a decoupled, evidence-based agronomic knowledge base. On an isolated held-out test split, the model demonstrates high classification fidelity without data leakage.

---

### 2. Problem Statement
Traditional agricultural scouting relies on visual inspection by trained agronomists, which is labor-intensive, geographically constrained, and prone to subjective error. Furthermore, existing AI prototypes frequently present critical flaws:
1. **Data Leakage & Overfitting**: Testing on datasets contaminated with training samples.
2. **Hallucination of Agricultural Treatments**: Unconstrained LLMs recommending toxic or inappropriate pesticide mixtures.
3. **Subjective Severity Estimation**: Guessing disease severity rather than calculating quantitative leaf coverage.

---

### 3. Methodology & Innovation

#### 3.1 Strict Dataset Stratification & Isolation
- The raw dataset is audited using `ml/dataset_analysis/analyze_dataset.py` for corrupt headers, 0-byte images, and MD5 duplicates.
- The dataset is partitioned into **70% Training**, **15% Validation**, and an **isolated 15% Held-Out Test Set**.
- The test set is locked and only evaluated once training and hyperparameter tuning are finalized.

#### 3.2 Two-Stage Transfer Learning
- **Stage 1 (Feature Extraction Warmup)**: The ImageNet backbone is frozen. A customized classification head (`GlobalAveragePooling2D` &rarr; `BatchNorm` &rarr; `Dense(256)` &rarr; `Dropout(0.35)` &rarr; `Dense(13, Softmax)`) is trained with Adam ($\eta = 10^{-3}$) for 8 epochs.
- **Stage 2 (Fine-Tuning)**: The top 40 convolutional layers of the backbone are unfrozen. Training continues at a low learning rate ($\eta = 5 \times 10^{-5}$) with Cosine Decay and dynamic `ReduceLROnPlateau`.
- **Class Balancing**: Sklearn class weights are computed and injected into categorical cross-entropy loss to prevent minority class suppression.

#### 3.3 Objective OpenCV Severity Grading
- Leaf area ($A_{leaf}$) is segmented using HSV green/canopy thresholding.
- Lesion area ($A_{lesion}$) is segmented using necrotic (brown/black) and chlorotic (yellow) masks.
- $\text{Severity Ratio} = (A_{lesion} / A_{leaf}) \times 100\%$.
- Categorized into:
  - **Healthy**: $0\%$ lesion area.
  - **Mild**: $< 10\%$ lesion coverage.
  - **Moderate**: $10\% - 30\%$ lesion coverage.
  - **Severe**: $> 30\%$ lesion coverage.

#### 3.4 Decoupled Recommendation Engine
- Eliminates AI hallucinations by storing validated agricultural practices in structured JSON registries.
- Supplies specific active ingredients (e.g. Copper Hydroxide, Chlorothalonil, Streptomycin), organic biocontrols (*Bacillus subtilis*), drip irrigation guidelines, and N-P-K nutrient schedules.

---

### 4. Supported Classes Taxonomy (13 Classes)
- **Strawberry**: `strawberry_healthy`, `strawberry_leaf_scorch`
- **Rice**: `rice_healthy`, `rice_bacterial_leaf_blight`, `rice_brown_spot`, `rice_leaf_smut`
- **Tomato**: `tomato_healthy`, `tomato_bacterial_spot`, `tomato_early_blight`, `tomato_late_blight`, `tomato_septoria_leaf_spot`, `tomato_yellow_leaf_curl`, `tomato_mosaic_virus`

---

### 5. Frequently Asked Professor / Examiner Questions (Viva Defense)

**Q1: Why did you choose MobileNetV3 / EfficientNet over ResNet-50 or VGG-16?**  
*Answer*: ResNet-50 and VGG-16 possess 25M and 138M parameters respectively, requiring heavy computational overhead. MobileNetV3-Large utilizes depthwise separable convolutions and inverted residuals with Squeeze-and-Excitation (SE) modules (~3.2M parameters), delivering equivalent foliar feature representation with sub-60ms CPU latency suitable for edge or serverless deployment.

**Q2: How did you prevent data leakage in your evaluation?**  
*Answer*: The dataset split was executed at the raw file level before data augmentation. All geometric augmentations (rotations, flips, zooms) were strictly applied to the training split only. The test split was evaluated once with pure rescaling ($1/255$), ensuring zero data contamination.

**Q3: How do you guarantee the AI won't recommend dangerous chemicals?**  
*Answer*: The recommendation engine is strictly decoupled from the neural network. The CNN outputs only the class identifier and confidence; the recommendation engine performs a deterministic lookup against an agronomic knowledge base verified against university agricultural extension publications.

**Q4: How does the system compute severity without human labeling?**  
*Answer*: We implemented an OpenCV computer vision pipeline utilizing color-space thresholding (HSV) and contour morphology to isolate necrotic/chlorotic pixel clusters relative to the total leaf surface area.
