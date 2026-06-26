import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn import metrics

# Setup directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def get_model_path(disease, model_name):
    clean_disease = disease.lower().replace(' ', '_')
    clean_model = model_name.lower().replace(' ', '_')
    return os.path.join(MODELS_DIR, f"{clean_disease}_{clean_model}.pkl")

def get_scaler_path(disease):
    clean_disease = disease.lower().replace(' ', '_')
    return os.path.join(MODELS_DIR, f"{clean_disease}_scaler.pkl")

def evaluate_model(model, X_test, y_test):
    """Evaluates a model and returns prediction classification and probabilites."""
    y_pred = model.predict(X_test)
    
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    else:
        y_prob = y_pred
        
    accuracy = metrics.accuracy_score(y_test, y_pred)
    
    try:
        roc_auc = metrics.roc_auc_score(y_test, y_prob)
    except ValueError:
        roc_auc = 0.5
        
    return {
        'accuracy': accuracy,
        'roc_auc': roc_auc,
        'y_prob': y_prob.tolist(),
        'y_pred': y_pred.tolist()
    }

def train_and_save_models(disease_type, data_dict):
    """Trains all four models for the specified disease and saves them to disk."""
    print(f"Training models for {disease_type}...")
    
    X_train = data_dict['X_train']
    X_train_scaled = data_dict['X_train_scaled']
    y_train = data_dict['y_train']
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'XGBoost': XGBClassifier(eval_metric='logloss', random_state=42)
    }
    
    trained_models = {}
    
    for name, model in models.items():
        # Train on scaled features for LR and SVM; raw features for tree-based models
        if name in ['Logistic Regression', 'SVM']:
            model.fit(X_train_scaled, y_train)
        else:
            model.fit(X_train, y_train)
            
        # Save to disk
        joblib.dump(model, get_model_path(disease_type, name))
        trained_models[name] = model
        
    # Save scaler
    joblib.dump(data_dict['scaler'], get_scaler_path(disease_type))
    
    print(f"All models for {disease_type} saved successfully.")
    return trained_models

def load_or_train_models(disease_type, data_dict, force_retrain=False):
    """Loads models from disk if available, otherwise trains and saves them."""
    model_names = ['Logistic Regression', 'Random Forest', 'SVM', 'XGBoost']
    models_exist = all(os.path.exists(get_model_path(disease_type, name)) for name in model_names)
    scaler_exists = os.path.exists(get_scaler_path(disease_type))
    
    if models_exist and scaler_exists and not force_retrain:
        loaded_models = {}
        for name in model_names:
            loaded_models[name] = joblib.load(get_model_path(disease_type, name))
        loaded_scaler = joblib.load(get_scaler_path(disease_type))
        data_dict['scaler'] = loaded_scaler
        return loaded_models
    else:
        return train_and_save_models(disease_type, data_dict)

def get_complete_model_results(disease_type, data_dict, force_retrain=False):
    """Loads/trains models, evaluates them, and returns metrics."""
    models = load_or_train_models(disease_type, data_dict, force_retrain=force_retrain)
    
    results = {}
    for name, model in models.items():
        if name in ['Logistic Regression', 'SVM']:
            eval_metrics = evaluate_model(model, data_dict['X_test_scaled'], data_dict['y_test'])
        else:
            eval_metrics = evaluate_model(model, data_dict['X_test'], data_dict['y_test'])
            
        results[name] = {
            'model': model,
            'metrics': eval_metrics
        }
        
    return results
