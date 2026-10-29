🏦 Multi-Pipeline AI Production Portfolio (FastAPI & MLOps)

Welcome to my professional AI and MLOps portfolio. This repository contains my core end-to-end Machine Learning and Generative AI pipelines, focusing on modular architecture, strict data validation, and clean code deployment.

## 📂 Project Structure
```text
├── rag_pipeline.py          # Pipeline 1: Production-Ready RAG Architecture (LLM + Cosine)
├── agents_pipeline.py       # Pipeline 2: Multi-Agent Task Orchestrator (Router + Qwen)
├── secure_pipeline.py       # Pipeline 3: Secure AI Microservice Template (API Key + CORS)
├── vector_pipeline.py       # Pipeline 4: Enterprise Vector Database Indexer (Embeddings + Cosine)
├── monitor_pipeline.py      # Pipeline 5: Real-Time AI Metrics Monitor (Prometheus + Grafana layout)
├── main.py                  # Pipeline 10: Credit Scoring API (Logistic Regression)
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

### 🚀 Pipeline 1: Production-Ready RAG Architecture (`rag_pipeline.py`)
- **Description**: Enterprise-grade Retrieval-Augmented Generation system matching query matrices with internal corporate documents using Cosine Similarity before executing localized LLM context parsing.
- **Tech Stack**: Transformers (Qwen-0.5B-Chat), Scikit-Learn (TF-IDF Vectorization Indexing), Pydantic v2 data structure mapping.

### 🤖 Pipeline 2: Multi-Agent Task Orchestrator (`agents_pipeline.py`)
- **Description**: Advanced multi-agent orchestration architecture where a centralized Manager Agent receives user instructions, dynamically routes tasks to specialized factual or creative sub-agents, and produces LLM-driven executive logs.
- **Tech Stack**: Transformers (Qwen-0.5B-Chat Pipeline Layout), Pydantic v2 Object Models, FastAPI Router endpoints.

### 🛡️ Pipeline 3: Secure AI Microservice Template (`secure_pipeline.py`)
- **Description**: Production-grade backend security boilerplate implementing strict API Key authentication, isolated CORS origin restricting, and defensive memory-mapped Rate Limiting mechanisms.
- **Tech Stack**: FastAPI Security layer, CORS Middleware engines, Pydantic v2 schemas mapping.

### 🧠 Pipeline 4: Enterprise Vector Database Indexer (`vector_pipeline.py`)
- **Description**: Specialized production-grade microservice simulating vector databases behavior (Qdrant/Chroma). Computes real-time mathematical Cosine Similarity over high-dimensional vector embeddings spaces.
- **Tech Stack**: NumPy linear algebra engines, FastAPI Router architecture, Pydantic v2 data layers.

### 📊 Pipeline 5: Real-Time AI Metrics Monitor (`monitor_pipeline.py`)
- **Description**: MLOps analytics shield exposing system health logs. Tracking raw inference response latency, estimated token processing consumption, and HTTP request error flags structured for Prometheus/Grafana scrapers.
- **Tech Stack**: FastAPI Core layer, Testing Client engines, Python asynchronous timing modules.

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

To launch the RAG Architecture API (Port 8006):
```bash
uvicorn rag_pipeline:app --reload --port 8006
```

To launch the Multi-Agent Orchestrator API (Port 8007):
```bash
uvicorn agents_pipeline:app --reload --port 8007
```

To launch the Secure AI Template API (Port 8008):
```bash
uvicorn secure_pipeline:app --reload --port 8008
```

To launch the Vector Database Indexer API (Port 8009):
```bash
uvicorn vector_pipeline:app --reload --port 8009
```

To launch the Real-Time Metrics Monitor API (Port 8010):
```bash
uvicorn monitor_pipeline:app --reload --port 8010
```

To launch the Credit Scoring API (Port 8000):
```bash
uvicorn main:app --reload --port 8000
```

To launch the Segmentation API (Port 8003):
```bash
uvicorn segmentation_pipeline:app --reload --port 8003
```

To launch the Recommendation API (Port 8004):
```bash
uvicorn recommandation_pipeline:app --reload --port 8004
```

To launch the PDF Summarizer API (Port 8005):
```bash
uvicorn pdf_summarizer_pipeline:app --reload --port 8005
```
---

## 🚀 Quick Start & Testing

### 1. Installation
```bash
git clone https://github.com
cd Portfolio-IA--Selection
pip install -r requirements.txt
```

### 2. Run the Microservices Locally
To launch the Vector Database Indexer API (Port 8009):
```bash
uvicorn vector_pipeline:app --reload --port 8009
```
To launch the RAG Architecture API (Port 8006):
```bash
uvicorn rag_pipeline:app --reload --port 8006
```

To launch the Multi-Agent Orchestrator API (Port 8007):
```bash
uvicorn agents_pipeline:app --reload --port 8007
```

To launch the Secure AI Template API (Port 8008):
```bash
uvicorn secure_pipeline:app --reload --port 8008
```

To launch the Credit Scoring API (Port 8000):
```bash
uvicorn main:app --reload --port 8000
```

To launch the Segmentation API (Port 8003):
```bash
uvicorn segmentation_pipeline:app --reload --port 8003
```

To launch the Recommendation API (Port 8004):
```bash
uvicorn recommandation_pipeline:app --reload --port 8004
```

To launch the PDF Summarizer API (Port 8005):
```bash
uvicorn pdf_summarizer_pipeline:app --reload --port 8005
```
To launch the Real-Time Metrics Monitor API (Port 8010):
```bash
uvicorn monitor_pipeline:app --reload --port 8010
```
