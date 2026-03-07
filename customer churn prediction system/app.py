import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Customer Churn Prediction", layout="centered")
st.title("🔮 Customer Churn Prediction (Enterprise App)")

# ---------------- LOGIN ----------------
st.subheader("🔐 Login")

username = st.text_input("Username", value="admin")
password = st.text_input("Password", value="admin123", type="password")

if st.button("Login"):
    try:
        res = requests.post(
            f"{API_URL}/login",
            data={"username": username, "password": password},
            timeout=5
        )

        if res.status_code == 200 and res.headers.get("content-type", "").startswith("application/json"):
            data = res.json()
            st.session_state["token"] = data["access_token"]
            st.success("✅ Logged in successfully")
        else:
            st.error(f"❌ Login failed (Status: {res.status_code})")
            st.text(res.text)

    except requests.exceptions.ConnectionError:
        st.error("🚫 Backend API is not running (start uvicorn)")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

# ---------------- PREDICTION ----------------
if "token" in st.session_state:
    st.divider()
    st.subheader("📊 Customer Details")

    with st.form("prediction_form"):
        gender = st.selectbox("Gender", ["Male", "Female"])
        SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
        tenure = st.slider("Tenure (months)", 0, 72, 12)
        MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0)
        TotalCharges = st.number_input("Total Charges", min_value=0.0)
        Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
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
        payload = {
            "gender": gender,
            "SeniorCitizen": SeniorCitizen,
            "tenure": tenure,
            "MonthlyCharges": MonthlyCharges,
            "TotalCharges": TotalCharges,
            "Contract": Contract,
            "PaymentMethod": PaymentMethod
        }

        headers = {
            "Authorization": f"Bearer {st.session_state['token']}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                headers=headers,
                timeout=5
            )

            if response.status_code == 200 and response.headers.get("content-type", "").startswith("application/json"):
                result = response.json()
                st.success("✅ Prediction successful")
                st.json(result)
            else:
                st.error(f"❌ Prediction failed (Status: {response.status_code})")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error("🚫 Backend API is not running")
        except Exception as e:
            st.error(f"Unexpected error: {e}")