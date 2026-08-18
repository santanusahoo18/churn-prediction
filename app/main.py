from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import pandas as pd


# =========================================================
# 1. CREATE FASTAPI APP
# =========================================================

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting telecom customer churn",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# =========================================================
# 2. LOAD TRAINED MODEL
# =========================================================

artifact = joblib.load("models/telco_churn_model.pkl")

model = artifact["model"]
scaler = artifact["scaler"]
feature_columns = artifact["feature_columns"]   # exact training column order


# =========================================================
# 3. INPUT SCHEMA — plain, human-readable values from the form.
#    (No one-hot flags here. The backend does that encoding below,
#    exactly the way the notebook did it, so it can never drift
#    out of sync with what the model actually expects.)
# =========================================================

class CustomerData(BaseModel):
    gender: str                 # "Male" | "Female"
    SeniorCitizen: int          # 0 | 1
    Partner: str                # "Yes" | "No"
    Dependents: str             # "Yes" | "No"
    tenure: float
    PhoneService: str           # "Yes" | "No"
    MultipleLines: str          # "Yes" | "No" | "No phone service"
    InternetService: str        # "DSL" | "Fiber optic" | "No"
    OnlineSecurity: str         # "Yes" | "No" | "No internet service"
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str               # "Month-to-month" | "One year" | "Two year"
    PaperlessBilling: str       # "Yes" | "No"
    PaymentMethod: str          # "Electronic check" | "Mailed check" |
                                 # "Bank transfer (automatic)" | "Credit card (automatic)"
    MonthlyCharges: float
    TotalCharges: float


# =========================================================
# 4. ENCODE — reproduces the notebook's preprocessing exactly,
#    then reindexes to feature_columns BY NAME so the order in
#    the trained model is always respected, regardless of how
#    this dict was built.
# =========================================================

def encode_customer(data: dict) -> pd.DataFrame:
    row = {
        "gender": 1 if data["gender"] == "Male" else 0,
        "SeniorCitizen": data["SeniorCitizen"],
        "Partner": 1 if data["Partner"] == "Yes" else 0,
        "Dependents": 1 if data["Dependents"] == "Yes" else 0,
        "tenure": data["tenure"],
        "PhoneService": 1 if data["PhoneService"] == "Yes" else 0,
        "PaperlessBilling": 1 if data["PaperlessBilling"] == "Yes" else 0,
        "MonthlyCharges": data["MonthlyCharges"],
        "TotalCharges": data["TotalCharges"],

        "MultipleLines_No phone service": 1 if data["MultipleLines"] == "No phone service" else 0,
        "MultipleLines_Yes": 1 if data["MultipleLines"] == "Yes" else 0,

        "InternetService_Fiber optic": 1 if data["InternetService"] == "Fiber optic" else 0,
        "InternetService_No": 1 if data["InternetService"] == "No" else 0,

        "Contract_One year": 1 if data["Contract"] == "One year" else 0,
        "Contract_Two year": 1 if data["Contract"] == "Two year" else 0,

        "PaymentMethod_Credit card (automatic)": 1 if data["PaymentMethod"] == "Credit card (automatic)" else 0,
        "PaymentMethod_Electronic check": 1 if data["PaymentMethod"] == "Electronic check" else 0,
        "PaymentMethod_Mailed check": 1 if data["PaymentMethod"] == "Mailed check" else 0,
    }

    # the six "no internet service / yes" style columns share the same pattern
    for col in ["OnlineSecurity", "OnlineBackup", "DeviceProtection",
                "TechSupport", "StreamingTV", "StreamingMovies"]:
        row[f"{col}_No internet service"] = 1 if data[col] == "No internet service" else 0
        row[f"{col}_Yes"] = 1 if data[col] == "Yes" else 0

    df = pd.DataFrame([row])

    # This line is the actual bug fix: align columns BY NAME to the
    # trained model's exact order, filling anything unexpected with 0.
    df = df.reindex(columns=feature_columns, fill_value=0)

    return df


# =========================================================
# 5. ROUTES
# =========================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request}
    )


@app.get("/status")
def status():
    return {"message": "Customer Churn Prediction API is running!"}


@app.get("/model-info")
def model_info():
    return {
        "model": type(model).__name__,
        "number_of_features": len(feature_columns),
        "features": feature_columns,
    }


@app.post("/predict")
def predict_churn(customer: CustomerData):
    input_df = encode_customer(customer.model_dump())
    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    return {
        "churn_prediction": "Yes" if prediction == 1 else "No",
        "churn_probability": round(float(probability) * 100, 2),
    }