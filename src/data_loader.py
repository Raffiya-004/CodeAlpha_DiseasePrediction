import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_and_preprocess_diabetes():
    """Loads and preprocesses the Diabetes dataset."""
    file_path = os.path.join(DATA_DIR, "diabetes.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Diabetes dataset not found at {file_path}. Run download_data.py first.")
        
    df = pd.read_csv(file_path)
    
    zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in zero_cols:
        median_val = df[df[col] != 0][col].median()
        if pd.isna(median_val):
            median_val = df[col].median()
        df[col] = df[col].replace(0, median_val)
        
    X = df.drop(columns=['Outcome'])
    y = df['Outcome']
    
    feature_names = X.columns.tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=feature_names, index=X_train.index)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=feature_names, index=X_test.index)
    
    return {
        'df': df,
        'X': X,
        'y': y,
        'X_train': X_train,
        'X_test': X_test,
        'X_train_scaled': X_train_scaled_df,
        'X_test_scaled': X_test_scaled_df,
        'y_train': y_train,
        'y_test': y_test,
        'scaler': scaler,
        'feature_names': feature_names
    }

def load_and_preprocess_heart():
    """Loads and preprocesses the Heart Disease dataset."""
    file_path = os.path.join(DATA_DIR, "heart_disease.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Heart Disease dataset not found at {file_path}. Run download_data.py first.")
        
    df = pd.read_csv(file_path)
    df = df.replace('?', np.nan)
    
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
            
    target_col = 'target' if 'target' in df.columns else 'Target'
    
    X = df.drop(columns=[target_col])
    y = df[target_col].astype(int)
    
    feature_names = X.columns.tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=feature_names, index=X_train.index)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=feature_names, index=X_test.index)
    
    return {
        'df': df,
        'X': X,
        'y': y,
        'X_train': X_train,
        'X_test': X_test,
        'X_train_scaled': X_train_scaled_df,
        'X_test_scaled': X_test_scaled_df,
        'y_train': y_train,
        'y_test': y_test,
        'scaler': scaler,
        'feature_names': feature_names
    }

def load_and_preprocess_breast_cancer():
    """Loads and preprocesses the Breast Cancer dataset (Wisconsin). Uses top 8 clinical features for UI simplicity."""
    data = load_breast_cancer()
    df_raw = pd.DataFrame(data.data, columns=data.feature_names)
    
    # 0 = Malignant, 1 = Benign in sklearn. We invert to match: 1 = Malignant (At Risk), 0 = Benign (Healthy)
    df_raw['target'] = 1 - data.target
    
    selected_features = [
        'mean radius', 
        'mean texture', 
        'mean perimeter', 
        'mean area', 
        'mean smoothness', 
        'mean compactness', 
        'mean concavity', 
        'mean concave points'
    ]
    
    df = df_raw[selected_features + ['target']]
    X = df.drop(columns=['target'])
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=selected_features, index=X_train.index)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=selected_features, index=X_test.index)
    
    return {
        'df': df,
        'X': X,
        'y': y,
        'X_train': X_train,
        'X_test': X_test,
        'X_train_scaled': X_train_scaled_df,
        'X_test_scaled': X_test_scaled_df,
        'y_train': y_train,
        'y_test': y_test,
        'scaler': scaler,
        'feature_names': selected_features
    }
