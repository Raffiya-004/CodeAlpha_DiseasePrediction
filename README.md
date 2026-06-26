# Disease Prediction System (CodeAlpha Internship Project)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/streamlit-app-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ml-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/xgboost-ml-green.svg)](https://xgboost.ai/)

A clean, modular, and professional **Disease Prediction System** built for the **CodeAlpha Machine Learning Internship**. 

The application is structured as a streamlined, single-page clinical diagnostics portal. By evaluating standard patient physiological markers and biometrics, it calculates onset risk scores using four machine learning algorithms (**Logistic Regression**, **Random Forest**, **SVM**, and **XGBoost**) across three clinical targets: **Diabetes**, **Heart Disease**, and **Breast Cancer**.

---

## ✨ System Features

* **3 Clinical Target Pipelines**:
  * **🩸 Diabetes**: Models physiological markers from the Pima Indians Database.
  * **❤️ Heart Disease**: Examines cardiovascular and clinical markers from the Cleveland Clinic Database.
  * **🎗️ Breast Cancer**: Classifies malignancy risk profiles using top diagnostic features from the Wisconsin Breast Cancer Dataset.
* **4 ML Classifiers**:
  * **Logistic Regression**: Linear classifier optimized on standardized features.
  * **Random Forest Classifier**: Ensemble bootstrap trees model optimized on raw clinical parameters.
  * **SVM (Support Vector Classifier)**: Maximum-margin classifier fitted with probability estimators.
  * **XGBoost Classifier**: Extreme gradient boosted trees model for high-efficiency tabular modeling.
* **Premium Dark Clinical Screening Portal UI**: 
  * A single-page, responsive, dual-column diagnostic form layout.
  * Centered branding featuring a medical icon and a blue-to-sky gradient title.
  * Segmented horizontal tab/pill selectors for switching between diseases (styled horizontal radio buttons with glowing gradients).
  * Left column: A clean two-column Patient Biometrics Form with dark-slate inputs, custom focus glows, and CSS-hidden spinner controls.
  * Right column: Predict outcomes (Dynamic Red/Green Glowing Alert Banners, Risk Levels: Low/Moderate/High, Confidence Metric Progress Bars, and Clinical Action Recommendations).
* **Automated Best Model Selection**: The backend dynamically evaluates the test accuracies of all four trained models and automatically selects the highest performing model for prediction.
* **Cached Persistence Pipeline**: Estimators and standard scalers are serialized to disk (`models/` folder) and cached in Streamlit resource memory, ensuring zero training lag on start.

---

## 📂 Codebase Architecture

```directory
CodeAlpha_DiseasePrediction/
│
├── .streamlit/
│   └── config.toml           # Enforces dark clinical theme by default
│
├── data/
│   ├── diabetes.csv           # Cleaned Pima Indians Diabetes Dataset
│   └── heart_disease.csv      # Cleaned Cleveland Heart Disease Dataset
│
├── models/                    # Serialized joblib pkl estimators
│   ├── diabetes_*.pkl
│   ├── heart_disease_*.pkl
│   └── breast_cancer_*.pkl
│
├── src/
│   ├── __init__.py
│   ├── download_data.py       # Pre-fetches diabetes and heart datasets
│   ├── data_loader.py         # Imputes missing values and slices Wisconsin features
│   ├── model_trainer.py       # Trains, persists, and evaluates LR/RF/SVM/XGBoost
│   └── utils.py               # Injects dark theme CSS overrides
│
├── app.py                     # Central Streamlit web application
├── requirements.txt           # Dependencies catalog
└── README.md                  # Project documentation
```

---

## 🛠️ Setup and Installation

Follow these steps to run the application locally:

### 1. Clone and Navigate
```bash
git clone https://github.com/your-username/CodeAlpha_DiseasePrediction.git
cd CodeAlpha_DiseasePrediction
```

### 2. Set Up Virtual Environment (Optional)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Pre-fetch Scripts
```bash
python src/download_data.py
```

### 5. Launch the Portal
```bash
streamlit run app.py
```
Open `http://localhost:8501` (or the port specified by Streamlit) in your browser.

---

## 🧠 Clinical Predictor Specs

### 🩸 Diabetes Features
* `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`, `Pedigree Value`, `Age`.

### ❤️ Heart Disease Features
* `Age`, `Sex`, `Chest Pain (CP) Type`, `Resting BP`, `Serum Cholesterol`, `Fasting Blood Sugar`, `Resting ECG`, `Maximum Heart Rate`, `Exercise Induced Angina`, `ST Depression`, `Peak ST Slope`, `Colored Vessels (CA)`, `Thalassemia Profile`.

### 🎗️ Breast Cancer Features
* `Mean Radius`, `Mean Texture`, `Mean Perimeter`, `Mean Area`, `Mean Smoothness`, `Mean Compactness`, `Mean Concavity`, `Mean Concave Points`.

---

## ⚖️ Clinical Disclaimer
This system represents statistical outputs from machine learning models trained on public databases for educational internship demonstrations. It is not intended for clinical use, oncology grading, or medical diagnostics. Consult a licensed medical practitioner for clinical assessments.
