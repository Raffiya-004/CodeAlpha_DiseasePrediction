import os
import pandas as pd
import numpy as np
import urllib.request

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Dataset URLs
DIABETES_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
HEART_URL = "https://raw.githubusercontent.com/amankharwal/Website-data/master/heart.csv"

def generate_fallback_diabetes():
    """Generates a realistic Diabetes dataset with proper clinical correlations if offline."""
    print("Generating fallback Diabetes dataset...")
    np.random.seed(42)
    n_samples = 768
    
    # Generate features
    pregnancies = np.random.poisson(3.8, n_samples)
    
    # Base glucose centered around 110 for healthy, 150 for diabetic
    outcome = np.random.binomial(1, 0.35, n_samples)
    
    glucose = np.where(outcome == 1, 
                       np.random.normal(145, 25, n_samples), 
                       np.random.normal(110, 20, n_samples))
    glucose = np.clip(glucose, 44, 199).astype(int)
    
    blood_pressure = np.random.normal(69, 12, n_samples)
    # Some zero values like the original dataset to test preprocessing
    zero_bp_indices = np.random.choice(n_samples, size=35, replace=False)
    blood_pressure[zero_bp_indices] = 0
    blood_pressure = np.clip(blood_pressure, 0, 122).astype(int)
    
    skin_thickness = np.where(outcome == 1,
                              np.random.normal(28, 10, n_samples),
                              np.random.normal(19, 8, n_samples))
    zero_skin_indices = np.random.choice(n_samples, size=220, replace=False)
    skin_thickness[zero_skin_indices] = 0
    skin_thickness = np.clip(skin_thickness, 0, 99).astype(int)
    
    insulin = np.where(outcome == 1,
                       np.random.normal(180, 120, n_samples),
                       np.random.normal(68, 45, n_samples))
    zero_insulin_indices = np.random.choice(n_samples, size=370, replace=False)
    insulin[zero_insulin_indices] = 0
    insulin = np.clip(insulin, 0, 846).astype(int)
    
    bmi = np.where(outcome == 1,
                   np.random.normal(35.2, 6.0, n_samples),
                   np.random.normal(30.8, 6.5, n_samples))
    zero_bmi_indices = np.random.choice(n_samples, size=11, replace=False)
    bmi[zero_bmi_indices] = 0.0
    bmi = np.clip(bmi, 0, 67.1).round(1)
    
    dpf = np.where(outcome == 1,
                   np.random.beta(2, 5, n_samples) * 1.8 + 0.1,
                   np.random.beta(1.5, 5, n_samples) * 1.5 + 0.08)
    dpf = np.clip(dpf, 0.078, 2.42).round(3)
    
    age = np.where(outcome == 1,
                   np.random.normal(37, 10, n_samples),
                   np.random.normal(31, 10, n_samples))
    age = np.clip(age, 21, 81).astype(int)
    
    df = pd.DataFrame({
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'SkinThickness': skin_thickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'Age': age,
        'Outcome': outcome
    })
    
    df.to_csv(os.path.join(DATA_DIR, "diabetes.csv"), index=False)
    print("Fallback Diabetes dataset saved.")

def generate_fallback_heart():
    """Generates a realistic Heart Disease dataset with proper clinical correlations if offline."""
    print("Generating fallback Heart Disease dataset...")
    np.random.seed(42)
    n_samples = 303
    
    target = np.random.binomial(1, 0.54, n_samples)
    
    age = np.where(target == 1,
                   np.random.normal(56.6, 9.0, n_samples),
                   np.random.normal(52.5, 9.5, n_samples))
    age = np.clip(age, 29, 77).astype(int)
    
    # 1 = male, 0 = female (target is higher for males in typical datasets)
    sex = np.where(target == 1,
                   np.random.binomial(1, 0.8, n_samples),
                   np.random.binomial(1, 0.5, n_samples))
    
    # cp: chest pain type (0-3). Angina is higher in target == 1
    cp = np.where(target == 1,
                  np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.2, 0.1, 0.4, 0.3]),
                  np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.7, 0.1, 0.15, 0.05]))
    
    trestbps = np.where(target == 1,
                        np.random.normal(134, 18, n_samples),
                        np.random.normal(129, 16, n_samples))
    trestbps = np.clip(trestbps, 94, 200).astype(int)
    
    chol = np.where(target == 1,
                    np.random.normal(250, 50, n_samples),
                    np.random.normal(240, 48, n_samples))
    chol = np.clip(chol, 126, 564).astype(int)
    
    fbs = np.random.binomial(1, 0.15, n_samples)
    
    restecg = np.random.choice([0, 1, 2], size=n_samples, p=[0.5, 0.48, 0.02])
    
    thalach = np.where(target == 1,
                       np.random.normal(139, 20, n_samples),
                       np.random.normal(158, 18, n_samples))
    thalach = np.clip(thalach, 71, 202).astype(int)
    
    exang = np.where(target == 1,
                     np.random.binomial(1, 0.55, n_samples),
                     np.random.binomial(1, 0.14, n_samples))
    
    oldpeak = np.where(target == 1,
                       np.random.normal(1.5, 1.2, n_samples),
                       np.random.normal(0.5, 0.7, n_samples))
    oldpeak = np.clip(oldpeak, 0.0, 6.2).round(1)
    
    slope = np.where(target == 1,
                     np.random.choice([0, 1, 2], size=n_samples, p=[0.1, 0.6, 0.3]),
                     np.random.choice([0, 1, 2], size=n_samples, p=[0.05, 0.25, 0.7]))
    
    ca = np.where(target == 1,
                  np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.2, 0.3, 0.25, 0.15, 0.1]),
                  np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.75, 0.15, 0.06, 0.03, 0.01]))
    
    thal = np.where(target == 1,
                    np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.02, 0.1, 0.2, 0.68]),
                    np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.01, 0.8, 0.15, 0.04]))
    
    df = pd.DataFrame({
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg,
        'thalach': thalach,
        'exang': exang,
        'oldpeak': oldpeak,
        'slope': slope,
        'ca': ca,
        'thal': thal,
        'target': target
    })
    
    df.to_csv(os.path.join(DATA_DIR, "heart_disease.csv"), index=False)
    print("Fallback Heart Disease dataset saved.")

def download_diabetes():
    target_path = os.path.join(DATA_DIR, "diabetes.csv")
    try:
        print("Downloading Diabetes dataset...")
        urllib.request.urlretrieve(DIABETES_URL, target_path)
        # Add headers as standard Pima Indians has no header
        df = pd.read_csv(target_path, header=None)
        df.columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
        df.to_csv(target_path, index=False)
        print("Diabetes dataset downloaded and headers added successfully.")
    except Exception as e:
        print(f"Error downloading diabetes dataset: {e}")
        generate_fallback_diabetes()

def download_heart():
    target_path = os.path.join(DATA_DIR, "heart_disease.csv")
    try:
        print("Downloading Heart Disease dataset...")
        urllib.request.urlretrieve(HEART_URL, target_path)
        # Rename 'target' column to 'Target' or standard for consistency
        df = pd.read_csv(target_path)
        # The URL has columns: age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target
        df.to_csv(target_path, index=False)
        print("Heart Disease dataset downloaded successfully.")
    except Exception as e:
        print(f"Error downloading Heart Disease dataset: {e}")
        generate_fallback_heart()

if __name__ == "__main__":
    download_diabetes()
    download_heart()
