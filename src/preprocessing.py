# src/preprocessing.py

import pandas as pd

def load_and_clean_data(path: str) -> pd.DataFrame:
    # ---------- LOAD ----------
    df = pd.read_csv(path)

    print("📌 Columns in dataset:")
    print(df.columns.tolist())

    # ---------- TARGET ----------
    if "Churn" not in df.columns:
        raise ValueError("❌ 'Churn' column not found in dataset")

    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0}).fillna(df["Churn"])

    # ---------- OPTIONAL NUMERIC COLUMNS ----------
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    if "MonthlyCharges" in df.columns:
        df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")

    if "tenure" in df.columns:
        df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce")

    # ---------- DROP ID ----------
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)

    # ---------- HANDLE MISSING ----------
    df = df.dropna().reset_index(drop=True)

    print("✅ Cleaned dataset shape:", df.shape)

    return df