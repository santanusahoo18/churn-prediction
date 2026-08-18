# 📊 Telco Customer Churn Prediction

> **An end-to-end Machine Learning project that predicts telecom customer churn and serves predictions through a FastAPI web application.**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi\&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker\&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🚀 Project Overview

Customer churn is a major challenge for subscription-based businesses.

This project predicts whether a telecom customer is likely to **churn (cancel their service)** based on factors such as:

* Customer tenure
* Contract type
* Internet service
* Payment method
* Monthly charges
* Total charges
* Support services
* Customer demographics

The project goes beyond a simple Jupyter Notebook by taking the complete workflow into a usable application:

**Data → Analysis → Model → API → Web Application → Deployment**

---

## 🌐 Live Demo

### 🚀 Try the Application

**Live Website:**
https://churn-prediction-1-jwrm.onrender.com/

**API Documentation:**
https://churn-prediction-1-jwrm.onrender.com/docs

---

# 📸 Project Screenshots


## 🏠 Web Application

<img width="517" height="747" alt="image" src="https://github.com/user-attachments/assets/eb8468a6-79e8-422d-b3f0-4d8a91f076cc" />



---

## 📊 Exploratory Data Analysis

<img width="1015" height="529" alt="Screenshot 2026-08-18 203055" src="https://github.com/user-attachments/assets/0f426768-e4f4-435f-9b1e-c897977f4080" />
<img width="1333" height="552" alt="Screenshot 2026-08-18 203127" src="https://github.com/user-attachments/assets/c63d18f7-83c1-4982-b79a-21bd6b9f0aa1" />
<img width="1110" height="528" alt="Screenshot 2026-08-18 203158" src="https://github.com/user-attachments/assets/b5a21763-d1eb-4af3-986e-78c5f1fceb10" />
<img width="1075" height="546" alt="Screenshot 2026-08-18 203225" src="https://github.com/user-attachments/assets/9cce9c27-3a6f-43aa-b6f5-cdbf26173da2" />
<img width="1325" height="658" alt="Screenshot 2026-08-18 203332" src="https://github.com/user-attachments/assets/46e7e0d7-52fa-4183-b1ed-5ed6712e7736" />
<img width="1192" height="580" alt="Screenshot 2026-08-18 203355" src="https://github.com/user-attachments/assets/f64c4a65-464a-4441-8758-9295abbaeaaf" />
<img width="1332" height="377" alt="Screenshot 2026-08-18 203418" src="https://github.com/user-attachments/assets/ea240d30-1a40-485c-9b46-dce5581aee32" />



---

## 📈 Model Evaluation

<img width="1150" height="575" alt="image" src="https://github.com/user-attachments/assets/571a0f7e-b13c-460f-a6b9-33db7dfe7bd0" />
<img width="815" height="510" alt="image" src="https://github.com/user-attachments/assets/210fe740-fc75-44eb-a773-c78cda077d8a" />




---

# 🎯 Key Results

| Metric                   |     Score |
| ------------------------ | --------: |
| **ROC-AUC**              | **0.846** |
| **Recall (Churn Class)** |   **78%** |
| **Precision**            |   **50%** |
| **Accuracy**             |   **74%** |

### Why Recall?

For churn prediction, identifying customers who are actually likely to leave is important.

Since most customers in the dataset do not churn, a model could achieve reasonable accuracy by predicting "No Churn" for most customers.

Therefore, this project prioritizes **Recall for the churn class** to identify as many potential churners as possible.

---

# 🔍 What Drives Customer Churn?

The analysis revealed several important patterns:

### 📄 Contract Type

Month-to-month customers have a significantly higher churn rate than customers with long-term contracts.

### ⏳ Customer Tenure

Customers with shorter tenure are more likely to churn.

### 🌐 Internet Service

Fiber optic customers represent an important higher-risk segment, especially when additional support and security services are absent.

### 💳 Payment Method

Customers using electronic checks show higher churn rates compared with customers using automatic payment methods.

---

# 🤖 Machine Learning

I compared four classification algorithms:

| Model                   | Purpose                        |
| ----------------------- | ------------------------------ |
| **Logistic Regression** | Interpretable classification   |
| **Decision Tree**       | Non-linear decision boundaries |
| **Random Forest**       | Ensemble learning              |
| **Gradient Boosting**   | Strong predictive performance  |

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

Hyperparameter tuning was performed using:

```python
GridSearchCV
```

Class imbalance was addressed using:

```python
class_weight="balanced"
```

### Why Logistic Regression?

Logistic Regression provided a strong balance between:

* Predictive performance
* Interpretability
* Simplicity
* Easy deployment

For customer churn prediction, interpretability is important because it helps explain **why a customer is considered high-risk**.

---

# 🧠 Machine Learning Pipeline

```text
Raw Customer Data
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Data Preprocessing
        ↓
Model Training
        ↓
Model Comparison
        ↓
Hyperparameter Tuning
        ↓
Model Evaluation
        ↓
Saved Model
        ↓
FastAPI
        ↓
Web Application
        ↓
Deployment
```

---

# 🛠️ Tech Stack

| Layer                | Tools                     |
| -------------------- | ------------------------- |
| **Programming**      | Python                    |
| **Data Processing**  | Pandas, NumPy             |
| **Visualization**    | Matplotlib, Seaborn       |
| **Machine Learning** | Scikit-learn              |
| **API**              | FastAPI, Pydantic         |
| **Server**           | Uvicorn                   |
| **Frontend**         | HTML, CSS, JavaScript     |
| **Model Storage**    | Joblib                    |
| **Containerization** | Docker                    |
| **Development**      | Jupyter Notebook, VS Code |

---

# 🔌 API

The trained machine learning model is exposed through a **FastAPI REST API**.

### Endpoint

```text
POST /predict
```

### Example Response

```json
{
  "churn_prediction": "Yes",
  "churn_probability": 0.81,
  "risk_level": "High risk"
}
```

The API returns:

* **Churn prediction**
* **Churn probability**
* **Risk level**

Interactive API documentation is available through the live `/docs` endpoint.

---

# 📚 Dataset

### Telco Customer Churn Dataset

* **7,043 customers**
* **21 features**
* Binary classification problem
* Target variable: `Churn`
* Originally published by IBM

**Dataset:**
https://www.kaggle.com/datasets/blastchar/telco-customer-churn



