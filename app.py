import streamlit as st
import joblib
import pandas as pd

# Load trained model
model = joblib.load("model/churn_pipeline.pkl")

st.set_page_config(page_title="Customer Churn Prediction", layout="centered")
st.title("🔮 Customer Churn Prediction (Enterprise App)")

# ---------------- LOGIN ----------------
st.subheader("🔐 Login")

username = st.text_input("Username", value="admin")
password = st.text_input("Password", value="admin123", type="password")

if st.button("Login"):
    if username == "admin" and password == "admin123":
        st.session_state["logged_in"] = True
        st.success("✅ Logged in successfully")
    else:
        st.error("❌ Invalid username or password")

# ---------------- PREDICTION ----------------
if "logged_in" in st.session_state:

    st.divider()
    st.subheader("📊 Customer Details")

    with st.form("prediction_form"):

        gender = st.selectbox("Gender", ["Male", "Female"])
        SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
        tenure = st.slider("Tenure (months)", 0, 72, 12)

        MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0)
        TotalCharges = st.number_input("Total Charges", min_value=0.0)

        Contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )

        PaymentMethod = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

        submitted = st.form_submit_button("🔮 Predict Churn")

    if submitted:

        # Create dataframe with all required columns
        input_data = pd.DataFrame([{
            "Gender": gender,
            "Senior Citizen": SeniorCitizen,
            "Partner": "No",
            "Dependents": "No",
            "tenure": tenure,
            "Phone Service": "Yes",
            "Multiple Lines": "No",
            "Internet Service": "Fiber optic",
            "Online Security": "No",
            "Online Backup": "No",
            "Device Protection": "No",
            "Tech Support": "No",
            "Streaming TV": "No",
            "Streaming Movies": "No",
            "Contract": Contract,
            "Paperless Billing": "Yes",
            "Payment Method": PaymentMethod,
            "Monthly Charges": MonthlyCharges,
            "Total Charges": TotalCharges
        }])

        # Predict
        prediction = model.predict(input_data)[0]

        st.divider()

        if prediction == 1:
            st.error("⚠️ Customer is likely to CHURN")
        else:
            st.success("✅ Customer is NOT likely to churn")
            
