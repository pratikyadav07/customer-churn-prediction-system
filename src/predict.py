import pickle
import pandas as pd

MODEL_PATH = "model/churn_pipeline.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict_churn(input_data: dict) -> dict:
    try:
        # 🔹 Create input data matching training features
        data = {
            "Gender": str(input_data.get("gender", "Male")),
            "Senior Citizen": int(input_data.get("SeniorCitizen", 0)),
            "Partner": "No",
            "Dependents": "No",
            "tenure": int(input_data.get("tenure", 12)),
            "Phone Service": "Yes",
            "Multiple Lines": "No",
            "Internet Service": "Fiber optic",
            "Online Security": "No",
            "Online Backup": "No",
            "Device Protection": "No",
            "Tech Support": "No",
            "Streaming TV": "No",
            "Streaming Movies": "No",
            "Contract": str(input_data.get("Contract", "Month-to-month")),
            "Paperless Billing": "Yes",
            "Payment Method": str(input_data.get("PaymentMethod", "Electronic check")),
            "Monthly Charges": float(input_data.get("MonthlyCharges", 70.0)),
            "Total Charges": float(input_data.get("TotalCharges", 840.0)),
        }

        df = pd.DataFrame([data])

        # 🔹 Ensure numeric columns are numeric
        numeric_cols = [
            "Senior Citizen",
            "tenure",
            "Monthly Charges",
            "Total Charges"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # 🔥 Match column order with training
        df = df[model.feature_names_in_]

        # 🔮 Get probabilities
        probabilities = model.predict_proba(df)[0]

        prob_yes = float(probabilities[1])
        prob_no = float(probabilities[0])

        # 🔥 Threshold logic (0.5)
        churn_label = "Yes" if prob_yes >= 0.5 else "No"

        return {
            "churn": churn_label,
            "probability_yes": round(prob_yes, 3),
            "probability_no": round(prob_no, 3),
        }

    except Exception as e:
        raise Exception(f"Prediction Error: {str(e)}")