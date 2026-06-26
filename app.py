import streamlit as st
import pandas as pd
import numpy as np
import os

# Set page config before any other streamlit elements
st.set_page_config(
    page_title="Disease Prediction Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Imports
from src.data_loader import (
    load_and_preprocess_diabetes, 
    load_and_preprocess_heart, 
    load_and_preprocess_breast_cancer
)
from src.model_trainer import get_complete_model_results
from src.utils import inject_custom_css

# Inject premium dark theme styling
inject_custom_css()

# Session state setup
if 'predicted' not in st.session_state:
    st.session_state.predicted = False
if 'prediction_results' not in st.session_state:
    st.session_state.prediction_results = {}
if 'last_disease' not in st.session_state:
    st.session_state.last_disease = ""
if 'force_retrain' not in st.session_state:
    st.session_state.force_retrain = False

@st.cache_resource
def get_dataset_and_models(disease_type, force_retrain=False):
    """Loads and preprocesses the dataset and trains/loads models with caching."""
    if disease_type == "Diabetes":
        data = load_and_preprocess_diabetes()
    elif disease_type == "Heart Disease":
        data = load_and_preprocess_heart()
    else: # Breast Cancer
        data = load_and_preprocess_breast_cancer()
    
    results = get_complete_model_results(disease_type, data, force_retrain=force_retrain)
    return data, results

# --- HEADER SECTION ---
st.markdown(
    """
    <div class="clinical-header">
        <div class="medical-icon">🩺</div>
        <h1 class="gradient-title">Disease Prediction System</h1>
        <p class="clinical-subtitle">Clinical Screening Tool for Early Risk Assessment</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- TOP BAR: DISEASE SELECTION ---
disease_sel = st.radio(
    "Select Target Disease", 
    ["Diabetes", "Heart Disease", "Breast Cancer"], 
    horizontal=True,
    label_visibility="collapsed"
)

# Reset prediction state if disease selection changes
if disease_sel != st.session_state.last_disease:
    st.session_state.predicted = False
    st.session_state.prediction_results = {}
    st.session_state.last_disease = disease_sel

# Load data and models
data_dict, model_results = get_dataset_and_models(disease_sel, force_retrain=st.session_state.force_retrain)
st.session_state.force_retrain = False # Reset flag

# Automatically find the best model based on test accuracy
best_model_name = max(model_results, key=lambda name: model_results[name]['metrics']['accuracy'])
active_model_details = model_results[best_model_name]
active_model = active_model_details['model']
active_metrics = active_model_details['metrics']

# --- DIAGNOSTIC STATUS BANNER ---
if not st.session_state.predicted:
    st.markdown(
        """
        <div class="status-banner status-awaiting">
            <span class="status-dot">🟡</span> <strong>Diagnostic Status:</strong> Awaiting Patient Data
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="status-banner status-complete">
            <span class="status-dot">🟢</span> <strong>Diagnostic Status:</strong> Analysis Complete
        </div>
        """,
        unsafe_allow_html=True
    )

# --- MAIN SECTION: 60-40 HORIZONTAL GRID ---
col_left, col_right = st.columns([6, 4], gap="large")

# --- LEFT COLUMN: PATIENT INPUT FORM ---
with col_left:
    patient_inputs = {}
    
    st.markdown("### **Patient Information**")
    with st.container(border=True):
        if disease_sel == "Diabetes":
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                patient_inputs['Pregnancies'] = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
                patient_inputs['BMI'] = st.number_input("BMI (kg/m²)", min_value=0.0, max_value=70.0, value=30.5, step=0.1)
                patient_inputs['Insulin'] = st.number_input("Insulin (μU/mL)", min_value=0, max_value=1000, value=80)
                patient_inputs['SkinThickness'] = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=23)
            with row1_col2:
                patient_inputs['Glucose'] = st.number_input("Glucose (mg/dL)", min_value=0, max_value=300, value=110)
                patient_inputs['Age'] = st.number_input("Age (Years)", min_value=1, max_value=120, value=33)
                patient_inputs['BloodPressure'] = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=200, value=72)
                patient_inputs['DiabetesPedigreeFunction'] = st.number_input("Pedigree Value", min_value=0.01, max_value=3.00, value=0.47, step=0.01)
                
        elif disease_sel == "Heart Disease":
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                patient_inputs['age'] = st.number_input("Age (Years)", min_value=1, max_value=120, value=54)
                sex_val = st.selectbox("Sex", ["Male", "Female"])
                patient_inputs['sex'] = 1 if sex_val == "Male" else 0
                cp_val = st.selectbox("Chest Pain (CP) Type", ["Asymptomatic", "Non-anginal", "Atypical", "Typical"])
                cp_mapping = {"Typical": 0, "Atypical": 1, "Non-anginal": 2, "Asymptomatic": 3}
                patient_inputs['cp'] = cp_mapping[cp_val]
                patient_inputs['trestbps'] = st.number_input("Resting BP (mmHg)", min_value=50, max_value=250, value=130)
                patient_inputs['chol'] = st.number_input("Cholesterol (mg/dL)", min_value=50, max_value=700, value=240)
                fbs_val = st.selectbox("Fasting Sugar > 120", ["No", "Yes"])
                patient_inputs['fbs'] = 1 if fbs_val == "Yes" else 0
                restecg_val = st.selectbox("Resting ECG", ["Normal", "ST-T Anomaly", "LV Hypertrophy"])
                restecg_mapping = {"Normal": 0, "ST-T Anomaly": 1, "LV Hypertrophy": 2}
                patient_inputs['restecg'] = restecg_mapping[restecg_val]
            with row1_col2:
                patient_inputs['thalach'] = st.number_input("Max Heart Rate", min_value=50, max_value=250, value=150)
                exang_val = st.selectbox("Exercise Angina", ["No", "Yes"])
                patient_inputs['exang'] = 1 if exang_val == "Yes" else 0
                patient_inputs['oldpeak'] = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
                slope_val = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])
                slope_mapping = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}
                patient_inputs['slope'] = slope_mapping[slope_val]
                patient_inputs['ca'] = st.selectbox("Vessels by Fluoroscopy", [0, 1, 2, 3, 4])
                thal_val = st.selectbox("Thalassemia Profile", ["Normal", "Fixed Defect", "Reversable Defect", "Undefined"])
                thal_mapping = {"Undefined": 0, "Normal": 1, "Fixed Defect": 2, "Reversable Defect": 3}
                patient_inputs['thal'] = thal_mapping[thal_val]
                
        else: # Breast Cancer
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                patient_inputs['mean radius'] = st.number_input("Mean Radius", min_value=1.0, max_value=50.0, value=14.1, step=0.1)
                patient_inputs['mean perimeter'] = st.number_input("Mean Perimeter", min_value=10.0, max_value=300.0, value=92.0, step=0.1)
                patient_inputs['mean smoothness'] = st.number_input("Mean Smoothness", min_value=0.01, max_value=0.50, value=0.10, step=0.01)
                patient_inputs['mean concavity'] = st.number_input("Mean Concavity", min_value=0.00, max_value=1.00, value=0.09, step=0.01)
            with row1_col2:
                patient_inputs['mean texture'] = st.number_input("Mean Texture", min_value=1.0, max_value=60.0, value=19.3, step=0.1)
                patient_inputs['mean area'] = st.number_input("Mean Area", min_value=50.0, max_value=4000.0, value=654.0, step=1.0)
                patient_inputs['mean compactness'] = st.number_input("Mean Compactness", min_value=0.01, max_value=0.80, value=0.10, step=0.01)
                patient_inputs['mean concave points'] = st.number_input("Mean Concave Points", min_value=0.00, max_value=0.50, value=0.05, step=0.01)

    run_prediction = st.button("🩺 Run Disease Analysis", type="primary", use_container_width=True)

    if run_prediction:
        input_df = pd.DataFrame([patient_inputs])
        input_df = input_df[data_dict['feature_names']]
        
        # Scale for LR & SVM
        if best_model_name in ['Logistic Regression', 'SVM']:
            input_processed = data_dict['scaler'].transform(input_df)
            input_processed_df = pd.DataFrame(input_processed, columns=data_dict['feature_names'])
            prediction = active_model.predict(input_processed_df)[0]
            probabilities = active_model.predict_proba(input_processed_df)[0]
        else:
            prediction = active_model.predict(input_df)[0]
            probabilities = active_model.predict_proba(input_df)[0]
            
        prob_risk = probabilities[1]
        prob_healthy = probabilities[0]
        confidence = (prob_risk if prediction == 1 else prob_healthy) * 100
        
        # Risk level determination
        if prob_risk < 0.35:
            risk_level = "Low Risk"
            risk_color = "healthy"
        elif prob_risk < 0.70:
            risk_level = "Moderate Risk"
            risk_color = "warning"
        else:
            risk_level = "High Risk"
            risk_color = "risk"
            
        st.session_state.predicted = True
        st.session_state.prediction_results = {
            'prediction': prediction,
            'confidence': confidence,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'model_name': best_model_name
        }
        st.rerun()

# --- RIGHT COLUMN: PREDICTION RESULT & ADVICE ---
with col_right:
    st.markdown("### **Prediction Result**")
    
    if st.session_state.predicted:
        res = st.session_state.prediction_results
        prediction = res['prediction']
        confidence = res['confidence']
        risk_level = res['risk_level']
        risk_color = res['risk_color']
        model_name = res['model_name']
        
        # Determine CSS classes based on outcome
        card_class = "result-healthy" if prediction == 0 else "result-risk"
        title_class = "result-healthy-title" if prediction == 0 else "result-risk-title"
        badge = "🟢 Low Risk Detected" if prediction == 0 else "🔴 High Risk Detected"
        fill_class = "confidence-fill-healthy" if prediction == 0 else "confidence-fill-risk"
        
        # Clinical Recommendations
        if disease_sel == "Diabetes":
            recs = [
                "Recommend diagnostic validation via fasting blood glucose or HbA1c screening.",
                "Advise tracking daily nutritional indices, emphasizing glycemic levels."
            ] if prediction == 1 else [
                "Maintain standard periodic diabetic profiles based on clinical age groups.",
                "Advise standard cardiovascular fitness maintenance."
            ]
        elif disease_sel == "Heart Disease":
            recs = [
                "Schedule a clinical stress validation test and echocardiogram.",
                "Confirm vital markers: lipid levels and systolic/diastolic blood pressure."
            ] if prediction == 1 else [
                "Maintain standard preventative screening plans based on patient risk groups.",
                "Advise monitoring resting heart rate and blood pressure regularly."
            ]
        else: # Breast Cancer
            recs = [
                "Schedule a mammography or ultrasound examination for clinical validation.",
                "Coordinate immediate consult with oncology specialists."
            ] if prediction == 1 else [
                "Maintain standard age-appropriate breast health screening programs.",
                "Advise periodic self-assessments and monitoring."
            ]
            
        # Avoid indentation in HTML block to prevent Streamlit Markdown parser from treating lines as code blocks
        st.markdown(
            f"""<div class="result-card {card_class}">
<div class="result-header {title_class}">{badge}</div>
<div class="result-detail-row">
<span class="result-detail-label">Assessed Target:</span>
<span class="result-detail-value">{disease_sel}</span>
</div>
<div class="result-detail-row">
<span class="result-detail-label">Risk Assessment:</span>
<span class="result-detail-value">{risk_level}</span>
</div>
<div class="result-detail-row" style="border-bottom:none;">
<span class="result-detail-label">Diagnostic Model:</span>
<span class="result-detail-value">{model_name}</span>
</div>
<div class="confidence-container">
<div class="confidence-label">
<span>Diagnostic Confidence Score</span>
<span>{confidence:.1f}%</span>
</div>
<div class="confidence-bar-bg">
<div class="confidence-bar-fill {fill_class}" style="width: {confidence:.1f}%;"></div>
</div>
</div>
</div>""",
            unsafe_allow_html=True
        )
        
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        
        # Recommendations Card
        with st.container(border=True):
            st.markdown("#### **Clinical Action Recommendations**")
            for r in recs:
                st.markdown(f"• {r}")
            st.caption("⚠️ **Disclaimer:** Statistical risk assessment tool. Results must be validated by clinical professionals.")
            st.caption(f"*Prediction Generated Using {model_name}*")
    else:
        st.markdown(
            """<div style="background-color: #151b2d; border: 1px dashed #2e3a52; border-radius: 8px; padding: 24px; text-align: center; color: #94a3b8;">
<div style="font-size: 32px; margin-bottom: 8px;">📋</div>
<h4 style="margin: 0 0 4px 0; color: #ffffff;">Awaiting Clinical Analysis</h4>
<p style="font-size: 13px; margin: 0; color: #94a3b8;">Provide patient biometrics on the left and click <strong>Run Disease Analysis</strong> to generate screening report.</p>
</div>""",
            unsafe_allow_html=True
        )
