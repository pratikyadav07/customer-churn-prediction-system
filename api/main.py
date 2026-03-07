from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from src.predict import predict_churn
from api.auth import authenticate_user, create_access_token, get_current_user

app = FastAPI(title="Customer Churn Prediction API")

# ✅ Optional but recommended (frontend use kare to)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Customer Churn Prediction API is running"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/predict")
def predict(data: dict, user: str = Depends(get_current_user)):
    try:
        result = predict_churn(data)

        # ✅ Directly return result safely
        return {
            "churn": result.get("churn"),
            "probability_yes": result.get("probability_yes"),
            "probability_no": result.get("probability_no"),
            "requested_by": user
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction Failed: {str(e)}"
        )