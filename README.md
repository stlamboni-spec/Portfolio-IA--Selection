# 🏦 Multi-Pipeline AI Production Portfolio (FastAPI & MLOps)

Welcome to my professional AI and MLOps portfolio. This repository contains my core end-to-end Machine Learning pipelines, focusing on modular architecture, strict data validation, and clean code deployment.

## 📂 Project Structure
```text
├── main.py              # Pipeline 10: Credit Scoring API (Logistic Regression)
├── churn_pipeline.py    # Pipeline 11: Customer Churn API (Random Forest / Tree Boosting)
├── requirements.txt     # Production ecosystem dependencies
├── Dockerfile           # Microservice containerization
└── README.md            # Technical documentation
```

---

## 🛠️ Active Production Pipelines

### 📈 Pipeline 10: Automated Credit Scoring Microservice (`main.py`)
- **Description**: Real-time credit risk assessment system designed for banking and Fintech sectors. The pipeline analyzes applicant solvency criteria, calculates the Probability of Default (PD), and handles automated compliance choices.
- **Tech Stack**: Scikit-Learn (Logistic Regression for transparency and full coefficient explainability), Pydantic v2 (Defensive typing prohibiting input injections like negative incomes).

### 🔄 Pipeline 11: Customer Churn Prediction Engine (`churn_pipeline.py`)
- **Description**: Predictive microservice built to detect user attrition risks in subscription-based services, enabling proactive retention marketing campaigns.
- **Tech Stack**: Scikit-Learn Ensemble (Random Forest Classifier simulating tree boosting structures), Pydantic Fields (Strict validation of billing and complaints metrics).

---

## 🚀 Quick Start & Testing

### 1. Installation
```bash
git clone https://github.com
cd Portfolio-IA--Selection
pip install -r requirements.txt
```

### 2. Run the Microservices Locally
To launch the Credit Scoring API:
```bash
uvicorn main:app --reload --port 8000
```
To launch the Churn Prediction API in parallel:
```bash
uvicorn churn_pipeline:app --reload --port 8001
```
