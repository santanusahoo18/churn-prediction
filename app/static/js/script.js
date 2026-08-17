const form = document.getElementById("churnForm");
const resultBox = document.getElementById("result");
const predictionText = document.getElementById("prediction");
const probabilityText = document.getElementById("probability");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const customerData = {
    gender: document.getElementById("gender").value,
    SeniorCitizen: Number(document.getElementById("SeniorCitizen").value),
    Partner: document.getElementById("Partner").value,
    Dependents: document.getElementById("Dependents").value,
    tenure: Number(document.getElementById("tenure").value),
    PhoneService: document.getElementById("PhoneService").value,
    MultipleLines: document.getElementById("MultipleLines").value,
    InternetService: document.getElementById("InternetService").value,
    OnlineSecurity: document.getElementById("OnlineSecurity").value,
    OnlineBackup: document.getElementById("OnlineBackup").value,
    DeviceProtection: document.getElementById("DeviceProtection").value,
    TechSupport: document.getElementById("TechSupport").value,
    StreamingTV: document.getElementById("StreamingTV").value,
    StreamingMovies: document.getElementById("StreamingMovies").value,
    Contract: document.getElementById("Contract").value,
    PaperlessBilling: document.getElementById("PaperlessBilling").value,
    PaymentMethod: document.getElementById("PaymentMethod").value,
    MonthlyCharges: Number(document.getElementById("MonthlyCharges").value),
    TotalCharges: Number(document.getElementById("TotalCharges").value),
  };

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(customerData),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Prediction failed");
    }

    resultBox.classList.remove("hidden");
    predictionText.textContent = "Churn Prediction: " + data.churn_prediction;
    probabilityText.textContent =
      "Churn Probability: " + data.churn_probability + "%";
  } catch (error) {
    resultBox.classList.remove("hidden");
    predictionText.textContent = "Error: " + error.message;
    probabilityText.textContent = "";
  }
});
