# 🏦 AI-Powered Credit Scoring Microservice (FastAPI & Logistic Regression)

## 📝 Description
Development of a credit risk assessment microservice designed for the banking and Fintech sectors. The API analyzes an applicant's solvency criteria in real-time, calculates their probability of default (PD), and returns an automated approval or rejection decision, fully compliant with algorithmic explainability requirements.

## 🛠️ Technologies & Architecture

- **Financial Modeling**: Logistic Regression model (**Scikit-Learn**) to ensure transparency and full explainability of approval coefficients.
- **Defensive Typing**: Integration of security filters using **Pydantic Fields** to prohibit input injections, such as debt-to-income ratios exceeding 100% or negative income values.
- **Industrial Inference**: Extraction of calibrated inference probabilities (`predict_proba`) delivered in structured JSON format for internal banking decision systems.

## 📂 Project Structure
```text
├── main.py              # FastAPI application & ML Inference pipeline
├── requirements.txt     # Production dependencies
└── README.md            # Technical documentation
```

## 🚀 Quick Start

### 1. Installation
Clone this repository and install the required dependencies:
```bash
git clone https://github.com
cd credit-scoring-fastapi
pip install -r requirements.txt
```

### 2. Run the API Locally
Launch the asynchronous microservice server using Uvicorn:
```bash
uvicorn main:app --reload
```

### 3. Interactive API Testing
Open your browser and navigate to:
👉 **http://127.0.0** to access the interactive Swagger UI and test live JSON payloads.
