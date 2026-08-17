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
    version="1.0.0"
)


# =========================================================
# 2. FRONTEND CONFIGURATION
# =========================================================

# CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# HTML templates
templates = Jinja2Templates(
    directory="app/templates"
)


# =========================================================
# 3. LOAD TRAINED MODEL
# =========================================================

artifact = joblib.load(
    "models/telco_churn_model.pkl"
)

model = artifact["model"]
scaler = artifact["scaler"]
feature_columns = artifact["feature_columns"]
binary_cols = artifact["binary_cols"]
multi_cat_cols = artifact["multi_cat_cols"]


# =========================================================
# 4. API HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is running!"
    }


# =========================================================
# 5. FRONTEND HOME PAGE
# =========================================================

@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


# =========================================================
# 6. MODEL INFORMATION
# =========================================================

@app.get("/model-info")
def model_info():

    return {
        "model": type(model).__name__,
        "number_of_features": len(feature_columns),
        "features": feature_columns
    }


# =========================================================
# 7. CUSTOMER INPUT
# =========================================================

class CustomerData(BaseModel):

    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int

    tenure: float

    PhoneService: int
    PaperlessBilling: int

    MonthlyCharges: float
    TotalCharges: float

    MultipleLines_No_phone_service: int
    MultipleLines_Yes: int

    InternetService_Fiber_optic: int
    InternetService_No: int

    OnlineSecurity_No_internet_service: int
    OnlineSecurity_Yes: int

    OnlineBackup_No_internet_service: int
    OnlineBackup_Yes: int

    DeviceProtection_No_internet_service: int
    DeviceProtection_Yes: int

    TechSupport_No_internet_service: int
    TechSupport_Yes: int

    StreamingTV_No_internet_service: int
    StreamingTV_Yes: int

    StreamingMovies_No_internet_service: int
    StreamingMovies_Yes: int

    Contract_One_year: int
    Contract_Two_year: int

    PaymentMethod_Credit_card_automatic: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int


# =========================================================
# 8. PREDICTION API
# =========================================================

@app.post("/predict")
def predict_churn(customer: CustomerData):

    # ---------------------------------------------
    # Get customer data
    # ---------------------------------------------

    data = customer.model_dump()


    # ---------------------------------------------
    # Convert dictionary to DataFrame
    # ---------------------------------------------

    input_data = pd.DataFrame([data])


    # ---------------------------------------------
    # Rename columns to EXACT training columns
    # ---------------------------------------------
    #
    # Example:
    # MultipleLines_No_phone_service
    #        ↓
    # MultipleLines_No phone service
    #
    # The model's feature_columns determine
    # the exact column names and order.
    #

    input_data.columns = feature_columns


    # ---------------------------------------------
    # Scale input using trained scaler
    # ---------------------------------------------

    input_scaled = scaler.transform(input_data)


    # ---------------------------------------------
    # Make prediction
    # ---------------------------------------------

    prediction = model.predict(input_scaled)[0]


    # ---------------------------------------------
    # Get probability
    # ---------------------------------------------

    probability = model.predict_proba(input_scaled)[0][1]


    # ---------------------------------------------
    # Convert prediction to Yes / No
    # ---------------------------------------------

    result = "Yes" if prediction == 1 else "No"


    # ---------------------------------------------
    # Return JSON response
    # ---------------------------------------------

    return {
        "churn_prediction": result,
        "churn_probability": round(
            float(probability) * 100,
            2
        )
    }