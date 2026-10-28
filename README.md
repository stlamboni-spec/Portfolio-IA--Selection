# 🏦 Multi-Pipeline AI Production Portfolio (FastAPI & MLOps)

Welcome to my professional AI and MLOps portfolio. This repository contains my core end-to-end Machine Learning pipelines, focusing on modular architecture, strict data validation, and clean code deployment.

## 📂 Project Structure
```text
── main.py                  # Pipeline 10: Credit Scoring API (Logistic Regression)
├── churn_pipeline.py        # Pipeline 11: Customer Churn API (Random Forest)
├── nlp_pipeline.py          # Pipeline 12: NLP Text Classification API (Naive Bayes)
├── segmentation_pipeline.py # Pipeline 13: Customer Segmentation API (K-Means)
├── recommandation_pipeline.py # Pipeline 14: Product Recommendation API (Cosine Similarity)
├── pdf_summarizer_pipeline.py # Pipeline 15: AI-Powered PDF Summarizer API (LLM Qwen)
├── requirements.txt         # Production ecosystem dependencies
├── Dockerfile               # Microservice containerization
└── README.md                # Technical documentation
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
- **Description**: Natural Language Processing microservice designed to automatically classify customer complaints and route tickets.
- **Tech Stack**: Scikit-Learn (TF-IDF Vectorizer + Multinomial Naive Bayes Pipeline).

### 📊 Pipeline 13: Customer Segmentation Engine (`segmentation_pipeline.py`)
- **Description**: Unsupervised Machine Learning microservice built to dynamically group customers based on purchase behavioral patterns.
- **Tech Stack**: Scikit-Learn (K-Means Clustering), Pydantic v2 validation.

### 🎯 Pipeline 14: Product Recommendation Engine (`recommandation_pipeline.py`)
- **Description**: Content-based recommendation microservice calculating product suggestions using vectors math structures.
- **Tech Stack**: Scikit-Learn Metrics (Cosine Similarity Matrix), NumPy array layout.

  ### 📄 Pipeline 15: AI-Powered PDF Summarizer Engine (`pdf_summarizer_pipeline.py`)
- **Description**: Generative AI microservice that extracts raw text from uploaded PDF files and applies a localized Large Language Model (LLM) to perform abstractive document summarization.
- **Tech Stack**: Transformers (Qwen-0.5B-Chat), PyPDF Document Extraction layout, FastAPI Async Files architecture.

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

To launch the Segmentation API (Port 8003):
```bash
uvicorn segmentation_pipeline:app --reload --port 8003

``

To launch the Recommendation API (Port 8004):
```bash
uvicorn recommandation_pipeline:app --reload --port 8004

To launch the PDF Summarizer API (Port 8005):
bash uvicorn pdf_summarizer_pipeline:app --reload --port 8005
---

### 📤 Étape 5 : Enregistrer
Une fois les modifications terminées, descendez tout en bas de la page GitHub et cliquez sur le gros bouton vert **Commit changes** (Valider les modifications).

<FollowUp>
Dites-moi si vous avez réussi à éditer le fichier et à l'enregistrer avec le bouton vert, ou si vous préférez que je vous donne le texte complet du **README.md** d'un seul bloc pour tout remplacer d'un coup !
</FollowUp>
Poser
```
