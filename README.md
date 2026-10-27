# 🏦 Multi-Pipeline AI Production Portfolio (FastAPI & MLOps)

Welcome to my professional AI and MLOps portfolio. This repository contains my core end-to-end Machine Learning pipelines, focusing on modular architecture, strict data validation, and clean code deployment.

## 📂 Project Structure
```text
├── main.py              # Pipeline 10: Credit Scoring API (Logistic Regression)
├── churn_pipeline.py    # Pipeline 11: Customer Churn API (Random Forest / Tree Boosting)
├── nlp_pipeline.py      # Pipeline 12: NLP Text Classification API (TF-IDF + Naive Bayes)
├── requirements.txt     # Production ecosystem dependencies
├── Dockerfile           # Microservice containerization
└── README.md            # Technical documentation
```

---

## 🛠️ Active Production Pipelines

### 📈 Pipeline 10: Automated Credit Scoring Microservice (`main.py`)
- **Description**: Real-time credit risk assessment system designed for banking and Fintech sectors.
- **Tech Stack**: Scikit-Learn (Logistic Regression), Pydantic v2.

### 🔄 Pipeline 11: Customer Churn Prediction Engine (`churn_pipeline.py`)
- **Description**: Predictive microservice built to detect user attrition risks in subscription services.
- **Tech Stack**: Scikit-Learn Ensemble (Random Forest Classifier), Pydantic Fields.

### 🔤 Pipeline 12: NLP Text Classification Engine (`nlp_pipeline.py`)
- **Description**: Natural Language Processing microservice designed to automatically classify customer complaints and route tickets to the correct banking department.
- **Tech Stack**: Scikit-Learn (TF-IDF Vectorizer + Multinomial Naive Bayes Pipeline), Pydantic Defensive Validation.

---

## 🚀 Quick Start & Testing

### 1. Installation
```bash
git clone https://github.com
cd Portfolio-IA--Selection
pip install -r requirements.txt
```

### 2. Run the Microservices Locally
To launch the Credit Scoring API (Port 8000):
```bash
uvicorn main:app --reload --port 8000
```
To launch the Churn Prediction API (Port 8001):
```bash
uvicorn churn_pipeline:app --reload --port 8001
```
To launch the NLP Text Classification API (Port 8002):
```bash
uvicorn nlp_pipeline:app --reload --port 8002
```
