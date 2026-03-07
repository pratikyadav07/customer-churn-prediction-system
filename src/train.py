import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocessing import load_and_clean_data# src/train.py

import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

from src.preprocessing import load_and_clean_data

# ---------- PATHS ----------
DATA_PATH = "data/churn.csv"
MODEL_PATH = "model/churn_pipeline.pkl"

def train_model():
    print("🔹 Loading dataset...")
    df = load_and_clean_data(DATA_PATH)

    if df is None or df.empty:
        raise ValueError("❌ Dataset is empty or not loaded")

    print("✅ Dataset shape:", df.shape)

    # ---------- TARGET CHECK ----------
    if "Churn" not in df.columns:
        raise ValueError("❌ 'Churn' column not found in dataset")

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    # ---------- COLUMN TYPES ----------
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    print("🔢 Numerical columns:", num_cols)
    print("🔤 Categorical columns:", cat_cols)

    # ---------- PREPROCESSOR ----------
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(
                drop="first",
                handle_unknown="ignore",
                sparse_output=False
            ), cat_cols)
        ]
    )

    # ---------- MODEL ----------
    pipeline = Pipeline(steps=[
        ("preprocessing", preprocessor),
        ("model", RandomForestClassifier(
            n_estimators=300,
            max_depth=12,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        ))
    ])

    # ---------- SPLIT ----------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("🚀 Training model...")
    pipeline.fit(X_train, y_train)
    print("✅ Model training completed")

    # ---------- CREATE MODEL DIR ----------
    os.makedirs("model", exist_ok=True)

    # ---------- SAVE MODEL ----------
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    # ---------- VERIFY ----------
    file_size = os.path.getsize(MODEL_PATH)
    if file_size == 0:
        raise RuntimeError("❌ Model file saved but EMPTY!")

    print(f"📦 Model saved at: {MODEL_PATH}")
    print(f"📏 Model file size: {file_size} bytes")
    print("🎯 TRAINING PIPELINE READY FOR PRODUCTION")

if __name__ == "__main__":
    train_model()