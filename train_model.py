import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

print("Current Working Directory:", os.getcwd())

# Load dataset
df = pd.read_csv("data/churn.csv")

print("Columns:", df.columns)

# Drop Customer ID
df = df.drop("Customer ID", axis=1)

# Convert Total Charges to numeric
df["Total Charges"] = pd.to_numeric(df["Total Charges"], errors="coerce")
df = df.dropna()

# Split features & target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Identify column types
categorical_cols = X.select_dtypes(include="object").columns
numeric_cols = X.select_dtypes(exclude="object").columns

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols),
    ]
)

# Create full pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", RandomForestClassifier(
    random_state=42,
    class_weight="balanced",
    n_estimators=200
))
    ]
)

# Train
pipeline.fit(X, y)

print("Training completed")
from sklearn.metrics import classification_report

y_pred = pipeline.predict(X)
print(classification_report(y, y_pred))

# Create model folder
os.makedirs("model", exist_ok=True)

# Save full pipeline
model_path = "model/churn_pipeline.pkl"
with open(model_path, "wb") as f:
    pickle.dump(pipeline, f)

print("✅ Model saved at:", model_path)