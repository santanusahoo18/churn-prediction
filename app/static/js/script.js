const form = document.getElementById("churnForm");
const resultBox = document.getElementById("result");
const predictionText = document.getElementById("prediction");
const probabilityText = document.getElementById("probability");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  // Get values from the form
  const gender = Number(document.getElementById("gender").value);
  const SeniorCitizen = Number(document.getElementById("SeniorCitizen").value);
  const Partner = Number(document.getElementById("Partner").value);
  const Dependents = Number(document.getElementById("Dependents").value);
  const tenure = Number(document.getElementById("tenure").value);
  const PhoneService = Number(document.getElementById("PhoneService").value);
  const PaperlessBilling = Number(
    document.getElementById("PaperlessBilling").value,
  );
  const MonthlyCharges = Number(
    document.getElementById("MonthlyCharges").value,
  );
  const TotalCharges = Number(document.getElementById("TotalCharges").value);

  // Multiple Lines
  const multipleLines = document.getElementById("MultipleLines").value;

  const MultipleLines_No_phone_service = multipleLines === "no_phone" ? 1 : 0;

  const MultipleLines_Yes = multipleLines === "yes" ? 1 : 0;

  // Internet Service
  const internet = document.getElementById("InternetService").value;

  const InternetService_Fiber_optic = internet === "fiber" ? 1 : 0;

  const InternetService_No = internet === "no" ? 1 : 0;

  // Online Security
  const onlineSecurity = document.getElementById("OnlineSecurity").value;

  const OnlineSecurity_No_internet_service =
    onlineSecurity === "no_internet" ? 1 : 0;

  const OnlineSecurity_Yes = onlineSecurity === "yes" ? 1 : 0;

  // Online Backup
  const onlineBackup = document.getElementById("OnlineBackup").value;

  const OnlineBackup_No_internet_service =
    onlineBackup === "no_internet" ? 1 : 0;

  const OnlineBackup_Yes = onlineBackup === "yes" ? 1 : 0;

  // Device Protection
  const deviceProtection = document.getElementById("DeviceProtection").value;

  const DeviceProtection_No_internet_service =
    deviceProtection === "no_internet" ? 1 : 0;

  const DeviceProtection_Yes = deviceProtection === "yes" ? 1 : 0;

  // Tech Support
  const techSupport = document.getElementById("TechSupport").value;

  const TechSupport_No_internet_service = techSupport === "no_internet" ? 1 : 0;

  const TechSupport_Yes = techSupport === "yes" ? 1 : 0;

  // Streaming TV
  const streamingTV = document.getElementById("StreamingTV").value;

  const StreamingTV_No_internet_service = streamingTV === "no_internet" ? 1 : 0;

  const StreamingTV_Yes = streamingTV === "yes" ? 1 : 0;

  // Streaming Movies
  const streamingMovies = document.getElementById("StreamingMovies").value;

  const StreamingMovies_No_internet_service =
    streamingMovies === "no_internet" ? 1 : 0;

  const StreamingMovies_Yes = streamingMovies === "yes" ? 1 : 0;

  // Contract
  const contract = document.getElementById("Contract").value;

  const Contract_One_year = contract === "one_year" ? 1 : 0;

  const Contract_Two_year = contract === "two_year" ? 1 : 0;

  // Payment Method
  const payment = document.getElementById("PaymentMethod").value;

  const PaymentMethod_Credit_card_automatic = payment === "credit" ? 1 : 0;

  const PaymentMethod_Electronic_check = payment === "electronic" ? 1 : 0;

  const PaymentMethod_Mailed_check = payment === "mailed" ? 1 : 0;

  // Create data for FastAPI
  const customerData = {
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    PaperlessBilling,
    MonthlyCharges,
    TotalCharges,

    MultipleLines_No_phone_service,
    MultipleLines_Yes,

    InternetService_Fiber_optic,
    InternetService_No,

    OnlineSecurity_No_internet_service,
    OnlineSecurity_Yes,

    OnlineBackup_No_internet_service,
    OnlineBackup_Yes,

    DeviceProtection_No_internet_service,
    DeviceProtection_Yes,

    TechSupport_No_internet_service,
    TechSupport_Yes,

    StreamingTV_No_internet_service,
    StreamingTV_Yes,

    StreamingMovies_No_internet_service,
    StreamingMovies_Yes,

    Contract_One_year,
    Contract_Two_year,

    PaymentMethod_Credit_card_automatic,
    PaymentMethod_Electronic_check,
    PaymentMethod_Mailed_check,
  };

  try {
    const response = await fetch("/predict", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(customerData),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Prediction failed");
    }

    // Show result
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
